import math

import bmesh
import bpy

from ..utils import object_has_to_be_activated, validate_mesh


PRESET_VALUES = {
    "LIGHT": {"reduction_percent": 30, "iterations": 1, "angle": 5},
    "MEDIUM": {"reduction_percent": 55, "iterations": 2, "angle": 10},
    "STRONG": {"reduction_percent": 75, "iterations": 3, "angle": 15},
}


def _mesh_volume_bu3(mesh):
    if not mesh:
        return False, 0.0

    bm = bmesh.new()
    try:
        bm.from_mesh(mesh)
        if len(bm.faces) == 0:
            return False, 0.0

        # signed=False returns absolute volume for stable comparison.
        volume = bm.calc_volume(signed=False)
        if volume <= 0:
            return False, 0.0

        return True, float(volume)
    except Exception:
        return False, 0.0
    finally:
        bm.free()


def _build_reduction_stack(obj, reduction):
    """Builds the modifier stack from a MeshReductionProperties instance."""
    step_labels = []
    modifier_names = []

    if reduction.use_collapse:
        collapse = obj.modifiers.new(name="ACO_Reduce_Collapse", type="DECIMATE")
        collapse.decimate_type = "COLLAPSE"
        ratio = 1.0 - (max(0, min(99, reduction.collapse_percent)) / 100.0)
        ratio = max(0.03, min(1.0, ratio))
        collapse.ratio = ratio
        collapse.use_collapse_triangulate = True
        reduction.collapse_ratio = ratio
        step_labels.append("Decima\u00e7\u00e3o")
        modifier_names.append(collapse.name)

    if reduction.use_unsubdivide:
        unsubdivide = obj.modifiers.new(name="ACO_Reduce_Unsubdivide", type="DECIMATE")
        unsubdivide.decimate_type = "UNSUBDIV"
        unsubdivide.iterations = max(1, min(100, reduction.unsubdiv_iterations))
        step_labels.append("Un-Subdivide")
        modifier_names.append(unsubdivide.name)

    if reduction.use_planar:
        planar = obj.modifiers.new(name="ACO_Reduce_Planar", type="DECIMATE")
        planar.decimate_type = "DISSOLVE"
        planar.angle_limit = math.radians(max(0, min(180, reduction.planar_angle)))
        planar.use_dissolve_boundaries = False
        step_labels.append("Planar")
        modifier_names.append(planar.name)

    return step_labels, modifier_names


def _warn_mesh_health(operator, obj):
    health = validate_mesh(obj)
    if not health["is_valid"]:
        issues = []
        if health["non_manifold_edges"]:
            issues.append(f"{health['non_manifold_edges']} arestas n\u00e3o-manifold")
        if health["loose_vertices"]:
            issues.append(f"{health['loose_vertices']} v\u00e9rtices soltos")
        if health["zero_area_faces"]:
            issues.append(f"{health['zero_area_faces']} faces com \u00e1rea zero")
        operator.report(
            {"WARNING"},
            f"Malha com problemas: {', '.join(issues)}. A opera\u00e7\u00e3o continuar\u00e1, mas o resultado pode ser impreciso.",
        )


class ACO_OT_apply_reduction_preset(bpy.types.Operator):
    bl_idname = "aco.apply_reduction_preset"
    bl_label = "Aplicar preset de redu\u00e7\u00e3o"
    bl_options = {"REGISTER", "UNDO"}

    preset: bpy.props.EnumProperty(
        name="Preset",
        items=(
            ("LIGHT", "Leve", "Preserva mais forma com redu\u00e7\u00e3o moderada"),
            ("MEDIUM", "M\u00e9dio", "Equil\u00edbrio entre redu\u00e7\u00e3o e preserva\u00e7\u00e3o"),
            ("STRONG", "Forte", "Redu\u00e7\u00e3o mais agressiva dentro do perfil seguro"),
        ),
        default="MEDIUM",
        options={"SKIP_SAVE"},
    )

    def execute(self, context):
        values = PRESET_VALUES.get(self.preset)
        if not values:
            bpy.ops.aco.alert_error_popup("INVOKE_DEFAULT", message="Preset de redu\u00e7\u00e3o inv\u00e1lido.")
            return {"CANCELLED"}

        reduction = context.scene.aco_reduction
        reduction.collapse_percent = values["reduction_percent"]
        reduction.unsubdiv_iterations = values["iterations"]
        reduction.planar_angle = values["angle"]

        self.report(
            {"INFO"},
            (
                f"Preset {self.preset.title()} aplicado: "
                f"{values['reduction_percent']}%, Itera\u00e7\u00f5es {values['iterations']}, \u00c2ngulo {values['angle']}."
            ),
        )
        return {"FINISHED"}


class ACO_OT_apply_mesh_reduction_pipeline(bpy.types.Operator):
    bl_idname = "aco.apply_mesh_reduction_pipeline"
    bl_label = "Aplicar redu\u00e7\u00e3o da malha"
    bl_options = {"REGISTER", "UNDO"}

    @object_has_to_be_activated
    def execute(self, context):
        scene = context.scene
        obj = context.active_object
        reduction = scene.aco_reduction
        diag = scene.aco_diagnostics

        if not obj or obj.type != "MESH":
            bpy.ops.aco.alert_error_popup("INVOKE_DEFAULT", message="Selecione um objeto Mesh ativo.")
            return {"CANCELLED"}

        if not (reduction.use_collapse or reduction.use_unsubdivide or reduction.use_planar):
            bpy.ops.aco.alert_error_popup(
                "INVOKE_DEFAULT",
                message="Selecione pelo menos uma etapa de redu\u00e7\u00e3o.",
            )
            return {"CANCELLED"}

        _warn_mesh_health(self, obj)

        before_valid, volume_before = _mesh_volume_bu3(obj.data)

        try:
            # Undo-safe flow: apply decimation modifiers directly on active object.
            context.view_layer.objects.active = obj
            if not obj.select_get():
                obj.select_set(True)
            if obj.mode != "OBJECT":
                bpy.ops.object.mode_set(mode="OBJECT")

            executed_steps, modifier_names = _build_reduction_stack(obj, reduction)

            for modifier_name in modifier_names:
                bpy.ops.object.modifier_apply(modifier=modifier_name)

            diag.vertices = len(obj.data.vertices)
            diag.faces = len(obj.data.polygons)

            health = validate_mesh(obj)
            diag.non_manifold_edges = health["non_manifold_edges"]
            diag.loose_vertices = health["loose_vertices"]
            diag.zero_area_faces = health["zero_area_faces"]
            diag.health_valid = health["is_valid"]
            diag.boundary_edges = health["boundary_edges"]
            diag.duplicate_vertices = health["duplicate_vertices"]
            diag.flipped_faces = health["flipped_faces"]
            diag.self_intersecting_faces = health["self_intersecting_faces"]
            diag.health_analyzed = True

            after_valid, volume_after = _mesh_volume_bu3(obj.data)
            volume_valid = before_valid and after_valid and volume_before > 0

            reduction.volume_before = volume_before if before_valid else 0.0
            reduction.volume_after = volume_after if after_valid else 0.0
            reduction.volume_valid = volume_valid

            if volume_valid:
                change_percent = ((volume_after - volume_before) / volume_before) * 100.0
                reduction.volume_change_percent = change_percent
                self.report(
                    {"INFO"},
                    (
                        f"Redu\u00e7\u00e3o aplicada: {', '.join(executed_steps)} | "
                        f"Volume: {volume_before:.4f} -> {volume_after:.4f} BU\u00b3 ({change_percent:+.2f}%)."
                    ),
                )
            else:
                reduction.volume_change_percent = 0.0
                self.report(
                    {"INFO"},
                    (
                        f"Redu\u00e7\u00e3o aplicada: {', '.join(executed_steps)} | "
                        "Volume indispon\u00edvel para esta malha."
                    ),
                )

            return {"FINISHED"}
        except Exception as e:
            bpy.ops.aco.alert_error_popup("INVOKE_DEFAULT", message=str(e))
            return {"CANCELLED"}


class ACO_OT_apply_quad_remesh(bpy.types.Operator):
    bl_idname = "aco.apply_quad_remesh"
    bl_label = "Aplicar Quad Remesh"
    bl_options = {"REGISTER", "UNDO"}

    @object_has_to_be_activated
    def execute(self, context):
        scene = context.scene
        obj = context.active_object
        qr = scene.aco_quad_remesh
        diag = scene.aco_diagnostics

        _warn_mesh_health(self, obj)

        volume_before_valid, volume_before = _mesh_volume_bu3(obj.data)

        try:
            modifier = obj.modifiers.new(name="QuadRemeshPreview", type="REMESH")
            modifier.mode = "VOXEL"
            modifier.voxel_size = qr.voxel_size
            modifier.use_smooth_shade = qr.smooth_shade

            bpy.ops.object.modifier_apply(modifier=modifier.name)

            diag.vertices = len(obj.data.vertices)
            diag.faces = len(obj.data.polygons)

            health = validate_mesh(obj)
            diag.non_manifold_edges = health["non_manifold_edges"]
            diag.loose_vertices = health["loose_vertices"]
            diag.zero_area_faces = health["zero_area_faces"]
            diag.health_valid = health["is_valid"]
            diag.boundary_edges = health["boundary_edges"]
            diag.duplicate_vertices = health["duplicate_vertices"]
            diag.flipped_faces = health["flipped_faces"]
            diag.self_intersecting_faces = health["self_intersecting_faces"]
            diag.health_analyzed = True

            volume_after_valid, volume_after = _mesh_volume_bu3(obj.data)
            volume_valid = volume_before_valid and volume_after_valid and volume_before > 0

            qr.volume_before = volume_before if volume_before_valid else 0.0
            qr.volume_after = volume_after if volume_after_valid else 0.0
            qr.volume_valid = volume_valid

            if volume_valid:
                change_percent = ((volume_after - volume_before) / volume_before) * 100.0
                qr.volume_change_percent = change_percent

                self.report(
                    {"INFO"},
                    (
                        f"Remesh aplicado (voxel {qr.voxel_size:.3f}, "
                        f"suaviza\u00e7\u00e3o {'ligada' if qr.smooth_shade else 'desligada'}). "
                        f"Volume: {volume_before:.4f} -> {volume_after:.4f} BU\u00b3 ({change_percent:+.2f}%)."
                    ),
                )
            else:
                qr.volume_change_percent = 0.0
                self.report(
                    {"INFO"},
                    (
                        f"Remesh aplicado (voxel {qr.voxel_size:.3f}, "
                        f"suaviza\u00e7\u00e3o {'ligada' if qr.smooth_shade else 'desligada'}). "
                        "Volume indispon\u00edvel para esta malha."
                    ),
                )

            return {"FINISHED"}
        except Exception as e:
            bpy.ops.aco.alert_error_popup("INVOKE_DEFAULT", message=str(e))
            return {"CANCELLED"}
