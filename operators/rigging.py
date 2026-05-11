import bpy
from bpy.types import Operator
from ..utils import get_defs, is_ready_to_generate, change_mode, collect_grouped_points, create_finger_bones, create_forearm_bone


class ACO_OT_generate_bones(Operator):
    bl_idname  = "aco.generate_hand_bones"
    bl_label   = "Gerar todos os bones"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context): 
        rig = context.scene.aco_rig_hand
               
        return is_ready_to_generate(rig)

    def execute(self, context):
        rig   = context.scene.aco_rig_hand
        scene = context.scene
        obj   = context.active_object
        defs  = get_defs()
        
        if rig.group_to_remove == "NONE":
            
            grouped = collect_grouped_points(rig=rig, items=defs, is_tuple=True)
            
            # container de dados que vai armazenar os ossos
            arm_data = bpy.data.armatures.new("Hand_Armature")
            
            #Armature um tipo especial de objeto, precisa estar associado a um objeto para aparecer 
            arm_obj  = bpy.data.objects.new("Hand_Rig", arm_data)
            
            #Adiciona o objeto "Hand_Rig" à coleção da cena, para ficar visível
            scene.collection.objects.link(arm_obj)

            arm_obj.show_in_front = True # Faz o rig aparecer na frente da malha, facilitando a visualização e seleção dos ossos durante a edição.
        
            
        else:
            
            groups = ["wrist", rig.group_to_remove] if rig.group_to_remove != "forearm" else [rig.group_to_remove]
            grouped = collect_grouped_points(rig=rig, items=groups)
            
            arm_obj = bpy.data.objects["Hand_Rig"]
            arm_data = arm_obj.data
            

        #As operações seguintes vão agir sobre ele
        context.view_layer.objects.active = arm_obj
        change_mode("EDIT")

        eb        = arm_data.edit_bones
        bone_map  = {}  

        # Pulso: ponto único, bone apontando para cima
        wrist_co = grouped.get("wrist", [None])[0]
    
            
        for key, _, names in defs:
            
            pts = grouped.get(key, [])
            
            create_finger_bones(eb, bone_map, key, pts, names, wrist_co)
            
        
        create_forearm_bone(eb, bone_map, grouped)
           

        change_mode("OBJECT")


        # Parenteia malha
        if obj and rig.group_to_remove == "NONE":
            obj.select_set(True)
            arm_obj.select_set(True)
            context.view_layer.objects.active = arm_obj
            bpy.ops.object.parent_set(type="ARMATURE_AUTO")

        rig.generated = True
        self.report({"INFO"}, f"{len(bone_map)} bones gerados.")
        return {"FINISHED"}
