import bpy

from ..utils import decimate_by_type, object_has_to_be_activated


def _update_scene_counts(context):
    obj = context.active_object
    if not obj or obj.type != "MESH":
        context.scene.vertices = 0
        context.scene.faces = 0
        return

    context.scene.vertices = len(obj.data.vertices)
    context.scene.faces = len(obj.data.polygons)


def _count_faces(obj):
    if not obj or obj.type != "MESH":
        return 0
    return len(obj.data.polygons)


class ACO_OT_decimate_planar(bpy.types.Operator):
    bl_idname = "aco.reduce_polygonos_by_planar"
    bl_label = "Decima\u00e7\u00e3o Planar"
    bl_options = {"REGISTER", "UNDO"}

    angle_limit: bpy.props.IntProperty(
        name="Angle Limit",
        description="Junta faces quase planas com base no \u00e2ngulo",
        default=10,
        min=0,
        max=180,
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Limite de \u00e2ngulo entre faces planas:")
        layout.prop(self, "angle_limit")

    @object_has_to_be_activated
    def execute(self, context):
        try:
            decimate_by_type("DISSOLVE", self.angle_limit)
            _update_scene_counts(context)
            self.report({"INFO"}, f"Planar aplicado (\u00e2ngulo: {self.angle_limit} graus).")
        except Exception as e:
            bpy.ops.aco.alert_error_popup("INVOKE_DEFAULT", message=str(e))

        return {"FINISHED"}


class ACO_OT_decimate_collapse(bpy.types.Operator):
    bl_idname = "aco.reduce_polygonos_by_collapse"
    bl_label = "Decima\u00e7\u00e3o Collapse"
    bl_options = {"REGISTER", "UNDO"}

    ratio: bpy.props.FloatProperty(
        name="Ratio",
        description="Propor\u00e7\u00e3o de faces a manter",
        default=0.5,
        min=0.0,
        max=1.0,
    )

    target_reduction_percent: bpy.props.IntProperty(
        name="Target Reduction Percent",
        description="Meta de redu\u00e7\u00e3o percentual por faces (0 a 99)",
        default=-1,
        min=-1,
        max=99,
        options={"SKIP_SAVE"},
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Propor\u00e7\u00e3o de faces a manter:")
        layout.prop(self, "ratio")

    @object_has_to_be_activated
    def execute(self, context):
        try:
            obj = context.active_object
            initial_faces = _count_faces(obj)

            if initial_faces <= 0:
                bpy.ops.aco.alert_error_popup("INVOKE_DEFAULT", message="Objeto sem faces para decimar.")
                return {"CANCELLED"}

            target_percent = self.target_reduction_percent

            if target_percent >= 0:
                target_percent = max(0, min(99, target_percent))
                # Fast mode for large scans: direct mapping from target reduction to keep ratio.
                self.ratio = 1.0 - (target_percent / 100.0)
                self.ratio = max(0.03, min(1.0, self.ratio))
                context.scene.decimate_collapse_ratio = self.ratio
            else:
                self.ratio = max(0.0, min(1.0, self.ratio))

            decimate_by_type("COLLAPSE", self.ratio)
            _update_scene_counts(context)

            final_faces = context.scene.faces
            achieved_reduction = (1.0 - (final_faces / initial_faces)) * 100.0

            if target_percent >= 0:
                self.report(
                    {"INFO"},
                    (
                        f"Decima\u00e7\u00e3o aplicada: alvo {target_percent}% | obtido {achieved_reduction:.1f}% "
                        f"({initial_faces} -> {final_faces} faces)."
                    ),
                )
            else:
                self.report({"INFO"}, f"Collapse aplicado (ratio: {self.ratio:.3f}).")

        except Exception as e:
            bpy.ops.aco.alert_error_popup("INVOKE_DEFAULT", message=str(e))

        return {"FINISHED"}


class ACO_OT_decimate_un_subdivide(bpy.types.Operator):
    bl_idname = "aco.reduce_polygonos_by_un_subdivide"
    bl_label = "Decima\u00e7\u00e3o Un-Subdivide"
    bl_options = {"REGISTER", "UNDO"}

    iterations: bpy.props.IntProperty(
        name="Iterations",
        description="Quantidade de etapas de subdivis\u00e3o a remover",
        default=1,
        min=1,
        max=100,
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Quantas vezes reduzir:")
        layout.prop(self, "iterations")

    @object_has_to_be_activated
    def execute(self, context):
        try:
            decimate_by_type("UNSUBDIV", self.iterations)
            _update_scene_counts(context)
            self.report({"INFO"}, f"Un-Subdivide aplicado (itera\u00e7\u00f5es: {self.iterations}).")
        except Exception as e:
            bpy.ops.aco.alert_error_popup("INVOKE_DEFAULT", message=str(e))

        return {"FINISHED"}


class ACO_OT_number_of_vertices_and_faces(bpy.types.Operator):
    bl_idname = "aco.number_of_vertices_and_face"
    bl_label = "N\u00fameros de V\u00e9rtices e Faces do Objeto Ativo"

    @object_has_to_be_activated
    def execute(self, context):
        obj = context.active_object

        if not obj or obj.type != "MESH":
            num_vertices = 0
            face_count = 0
            bpy.ops.aco.alert_error_popup(
                "INVOKE_DEFAULT",
                message="N\u00e3o foi poss\u00edvel realizar a contagem de v\u00e9rtices e faces do objeto 3D.",
            )
        else:
            num_vertices = len(obj.data.vertices)
            face_count = len(obj.data.polygons)

        context.scene.vertices = num_vertices
        context.scene.faces = face_count

        return {"FINISHED"}
