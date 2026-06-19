import math

import bmesh
import bpy

from ...utils import object_has_to_be_activated, validate_mesh, build_reduction_stack, mesh_volume, warn_mesh_health


PRESET_VALUES = {
    "LIGHT": {"reduction_percent": 30, "iterations": 1, "angle": 5},
    "MEDIUM": {"reduction_percent": 55, "iterations": 2, "angle": 10},
    "STRONG": {"reduction_percent": 75, "iterations": 3, "angle": 15},
}

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
        
        bpy.ops.aco.processing_time_start("EXEC_DEFAULT",
                name_task="Mesh Decimation")

        if not obj or obj.type != "MESH":
            bpy.ops.aco.alert_error_popup("INVOKE_DEFAULT", message="Selecione um objeto Mesh ativo.")
            return {"CANCELLED"}

        if not (reduction.use_collapse or reduction.use_unsubdivide or reduction.use_planar):
            bpy.ops.aco.alert_error_popup(
                "INVOKE_DEFAULT",
                message="Selecione pelo menos uma etapa de redu\u00e7\u00e3o.",
            )
            return {"CANCELLED"}

        warn_mesh_health(self, obj)

        before_valid, volume_before = mesh_volume(obj.data)

        try:
            # Undo-safe flow: apply decimation modifiers directly on active object.
            context.view_layer.objects.active = obj
            if not obj.select_get():
                obj.select_set(True)
            if obj.mode != "OBJECT":
                bpy.ops.object.mode_set(mode="OBJECT")

            executed_steps, modifier_names = build_reduction_stack(obj, reduction)

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

            after_valid, volume_after = mesh_volume(obj.data)
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
                
            bpy.ops.aco.processing_time_stop('EXEC_DEFAULT')

            return {"FINISHED"}
        except Exception as e:
            bpy.ops.aco.alert_error_popup("INVOKE_DEFAULT", message=str(e))
            return {"CANCELLED"}

