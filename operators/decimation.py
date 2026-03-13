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


def _show_success_popup(message):
    bpy.ops.aco.alert_info_popup("INVOKE_DEFAULT", message_info=message)


class ACO_OT_decimate_planar(bpy.types.Operator):
    bl_idname = "aco.reduce_polygonos_by_planar"
    bl_label = "Decimacao Planar"
    bl_options = {"REGISTER", "UNDO"}

    angle_limit: bpy.props.IntProperty(
        name="Angle Limit",
        description="Junta faces quase planas com base no angulo",
        default=10,
        min=0,
        max=180,
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Limite de angulo entre faces planas:")
        layout.prop(self, "angle_limit")

    @object_has_to_be_activated
    def execute(self, context):
        try:
            decimate_by_type("DISSOLVE", self.angle_limit)
            _update_scene_counts(context)
            _show_success_popup(f"Decimacao Planar aplicada (angulo: {self.angle_limit} graus).")
        except Exception as e:
            bpy.ops.aco.alert_error_popup("INVOKE_DEFAULT", message=str(e))

        return {"FINISHED"}


class ACO_OT_decimate_collapse(bpy.types.Operator):
    bl_idname = "aco.reduce_polygonos_by_collapse"
    bl_label = "Decimacao Collapse"
    bl_options = {"REGISTER", "UNDO"}

    ratio: bpy.props.FloatProperty(
        name="Ratio",
        description="Parametro para controlar a porcentagem de reducao",
        default=0.5,
        min=0.0,
        max=1.0,
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Proporcao de faces a manter:")
        layout.prop(self, "ratio")

    @object_has_to_be_activated
    def execute(self, context):
        try:
            decimate_by_type("COLLAPSE", self.ratio)
            _update_scene_counts(context)
            _show_success_popup(f"Decimacao Collapse aplicada (ratio: {self.ratio:.3f}).")
        except Exception as e:
            bpy.ops.aco.alert_error_popup("INVOKE_DEFAULT", message=str(e))

        return {"FINISHED"}


class ACO_OT_decimate_un_subdivide(bpy.types.Operator):
    bl_idname = "aco.reduce_polygonos_by_un_subdivide"
    bl_label = "Decimacao Un-Subdivide"
    bl_options = {"REGISTER", "UNDO"}

    iterations: bpy.props.IntProperty(
        name="Iterations",
        description="Quantidade de etapas de subdivisao a remover",
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
            _show_success_popup(f"Decimacao Un-Subdivide aplicada (iteracoes: {self.iterations}).")
        except Exception as e:
            bpy.ops.aco.alert_error_popup("INVOKE_DEFAULT", message=str(e))

        return {"FINISHED"}


class ACO_OT_number_of_vertices_and_faces(bpy.types.Operator):
    bl_idname = "aco.number_of_vertices_and_face"
    bl_label = "Numeros de Vertices e Faces do Objeto Ativo"

    @object_has_to_be_activated
    def execute(self, context):
        obj = context.active_object

        if not obj or obj.type != "MESH":
            num_vertices = 0
            face_count = 0
            bpy.ops.aco.alert_error_popup(
                "INVOKE_DEFAULT",
                message="Nao foi possivel realizar a contagem de vertices e faces do objeto 3D.",
            )
        else:
            num_vertices = len(obj.data.vertices)
            face_count = len(obj.data.polygons)

        context.scene.vertices = num_vertices
        context.scene.faces = face_count

        return {"FINISHED"}

