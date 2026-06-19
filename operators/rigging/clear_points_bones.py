import bpy 

from bpy.types import Operator


class ACO_OT_clear_points_bones(Operator):
    """Limpa todos os pontos de articulação marcados."""
    bl_idname = "aco.clear_joint_points"
    bl_label  = "Limpar marcações"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        rig = context.scene.aco_rig_hand
        rig.joint_points.clear()
        rig.active_finger = ""
        rig.generated     = False
        rig.progress      = 0.0
        return {"FINISHED"}

