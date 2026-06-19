import bpy 
from bpy.types import Operator

from ...utils import change_mode, get_defs


class ACO_OT_redo_finger_bone(Operator):
    bl_idname = "aco.redo_finger_bone"
    bl_label = "Refazer os ossos do dedo"
    bl_description = "Refaz os ossos do dedo selecionado"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return len(context.scene.aco_rig_hand.joint_points) > 0
    

    def execute(self, context):
        rig = context.scene.aco_rig_hand
        group = rig.group_to_remove
        
        # Verifica se o rig foi gerado
        if not group or group == "wrist":
            self.report({'ERROR'}, "Não foi selecionado nenhum dedo ou membro superior")
            return {'CANCELLED'}
        
        print(f"O valor do dedo selecionado para remover {group}")
        
        name_groups = []
        
        try:
            for key, _, bones in get_defs():
                
                if key == group:
                    name_groups = [b for b in bones if not b.endswith("_tip")]
                    break
                
        except Exception as e:
            
            self.report({'ERROR'}, f"Ocorreu um erro inesperado: {e}")
            return {'CANCELLED'}
        
        arm_obj = context.scene.objects["Hand_Rig"]

        # Torna o objeto ativo e entra no modo edição
        bpy.context.view_layer.objects.active = arm_obj
        change_mode("EDIT")

        edit_bones = arm_obj.data.edit_bones

        # Remover um bone pelo nome
        names_in_rig = [name for name in name_groups if name in edit_bones]

        if not names_in_rig:
            self.report({"ERROR"}, "Nenhum bone encontrado.")
            return {"CANCELLED"}
        

        for name in names_in_rig:
            edit_bones.remove(edit_bones[name])
        
        
       # Coleta os índices do grupo, em ordem de inserção
        index_group = [
            i for i, p in enumerate(rig.joint_points)
            if p.group == group
        ]

        # Pula o primeiro índice — ele é o base do dedo
        index_to_remove = index_group[1:]

        # Remove de trás para frente para não deslocar os índices anteriores
        for i in reversed(index_to_remove):
            rig.joint_points.remove(i)
                
        change_mode("OBJECT")
        
        bpy.context.view_layer.objects.active = arm_obj        
                
        rig.generated = False
        rig.active_finger = ""

        return {"FINISHED"}