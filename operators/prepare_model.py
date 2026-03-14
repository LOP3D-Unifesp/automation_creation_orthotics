import bpy
from ..utils import object_has_to_be_activated


class ACO_OT_prepare_model_auto(bpy.types.Operator):
    bl_idname = "aco.prepare_model_auto"
    bl_label = "Preparar modelo automaticamente"
    bl_options = {"REGISTER", "UNDO"}

    @object_has_to_be_activated
    def execute(self, context):
        # Automatic flow: force XYZ alignment, adjust origin, frame view and refresh diagnostics.
        bpy.ops.aco.align_limb_axis("EXEC_DEFAULT", force_all_axes=True, show_feedback=False)
        bpy.ops.aco.number_of_vertices_and_face("EXEC_DEFAULT")

        self.report({"INFO"}, "Centraliza\u00e7\u00e3o conclu\u00edda: alinhamento XYZ e an\u00e1lise atualizada.")
        return {"FINISHED"}
