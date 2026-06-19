import bpy
from bpy.types import Operator
from ...utils import update_progress



class ACO_OT_undo_point(Operator):
    bl_idname = "aco.undo_point"
    bl_label  = "Desfazer último ponto"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return len(context.scene.aco_rig_hand.joint_points) > 0

    def execute(self, context):
        rig = context.scene.aco_rig_hand
        idx = len(rig.joint_points) - 1
        last_group = rig.joint_points[idx].group
        rig.joint_points.remove(idx)
        rig.active_finger = last_group   # volta o foco para o dedo desfeito
        bpy.ops.aco.delete_one_score_markers()  # deleta o marcador do ponto desfeito
        update_progress(rig)
        return {"FINISHED"}