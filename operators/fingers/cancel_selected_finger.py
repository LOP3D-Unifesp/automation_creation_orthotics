import bpy 
from bpy.types import Operator


class ACO_OT_cancel_selected_finger(Operator):
    bl_idname = "aco.cancel_selected_finger"
    bl_label = "Cancelar"
    bl_description = "Cancela a operação e limpa a seleção"
    
    def execute(self, context):
        
        # Reseta para o primeiro item disponível
        context.scene.aco_rig_hand.property_unset("group_to_remove")
        
        return {'FINISHED'}

