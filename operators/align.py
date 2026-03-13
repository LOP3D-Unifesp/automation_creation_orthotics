import bpy 
from ..utils import activate_object, align_to_axis, change_mode, reset_rotation_axis, object_has_to_be_activated


class ACO_OT_align_limb_axis(bpy.types.Operator):
    bl_idname = "aco.align_limb_axis"
    bl_label = "Alinhar membro no eixo"

    @object_has_to_be_activated
    def execute(self, context):
        scene = context.scene
        
        #Obtem o eixo escolhido pelo botÃ£o
        axis = scene.align_limb_props.axis

        obj = context.active_object

        try:

            # Ativa o objeto
            activate_object(obj)      

            # Object â†’ Edit
            change_mode("OBJECT")
            change_mode("EDIT") 

            align_to_axis(axis=axis)

            # Volta para Object Mode
            change_mode("OBJECT")

            print("O objeto deve estar alinhado ao eixo escolhido!")

            # Ajusta origem
            bpy.ops.object.origin_set(type="ORIGIN_CENTER_OF_MASS", center="MEDIAN")

            # O zero final precisa acontecer depois de recentrar a origem.
            reset_rotation_axis(axis)

            bpy.ops.aco.alert_info_popup('INVOKE_DEFAULT', message_info=f"Alinhado com sucesso ao eixo {axis}")
        
        except Exception as e:
            
            bpy.ops.aco.alert_error_popup('INVOKE_DEFAULT', message=e)


        return {'FINISHED'}
