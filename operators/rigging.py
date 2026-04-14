import bpy
from bpy.types import Operator
from ..utils import points_for, get_defs, is_ready_to_generate


class ACO_OT_generate_bones(Operator):
    bl_idname  = "aco.generate_hand_bones"
    bl_label   = "Gerar bones"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        rig = context.scene.aco_rig_hand
        
        return is_ready_to_generate(rig) and not rig.generated

    def execute(self, context):
        rig   = context.scene.aco_rig_hand
        scene = context.scene
        obj   = context.active_object
        defs  = get_defs()

        # Coleta pontos agrupados em ordem
        grouped = {}

        for item in defs:
            key = item[0]  # pega o primeiro valor da tupla

            lista_pontos = []

            # percorre os pontos desse dedo
            for p in points_for(rig, key):
                print(p.co[:])

                lista_pontos.append(p.co[:])

            print(lista_pontos)
            grouped[key] = lista_pontos

        # container de dados que vai armazenar os ossos
        arm_data = bpy.data.armatures.new("Hand_Armature")
        #Armature um tipo especial de objeto, precisa estar associado a um objeto para aparecer 
        arm_obj  = bpy.data.objects.new("Hand_Rig", arm_data)
        
        #Adiciona o objeto "Hand_Rig" à coleção da cena, para ficar visível
        scene.collection.objects.link(arm_obj)

        arm_obj.show_in_front = True # Faz o rig aparecer na frente da malha
        
        #As operações seguintes vão agir sobre ele
        context.view_layer.objects.active = arm_obj
        bpy.ops.object.mode_set(mode="EDIT")

        eb        = arm_data.edit_bones
        bone_map  = {}  

        # Pulso: ponto único, bone apontando para cima
        wrist_co = grouped.get("wrist", [None])[0]

        for key, _, names in defs:
            pts = grouped.get(key, [])
            if key in ("wrist", "forearm"):
                continue # Esses casos são tratados depois


            for i in range(3):
                if i + 1 >= len(pts):
                    break

                if not pts[i] or not pts[i + 1]:
                    continue

                name = names[i]
                
                b      = eb.new(name)
                b.head = pts[i]
                b.tail = pts[i + 1]
                bone_map[name] = b

            # Criar um osso conectando o pulso ao primeiro osso do dedo
            if wrist_co and names and len(pts) > 0:
                connect_name = f"{key}_root" 
                b = eb.new(connect_name)
                b.head = wrist_co              # começa no pulso
                b.tail = pts[0]                # vai até a base do dedo (MCP)
                bone_map[connect_name] = b

                # Definir hierarquia: root → MCP
                if names[0] in bone_map:
                    bone_map[names[0]].parent      = bone_map[connect_name]
                    bone_map[names[0]].use_connect = True


            # Parentesco e hierarquia do dedo (MCP→PIP→DIP→TIP)

            for i in range(1, 3):
                child_n  = names[i]
                parent_n = names[i - 1]
                if child_n in bone_map and parent_n in bone_map:
                    bone_map[child_n].parent      = bone_map[parent_n]
                    bone_map[child_n].use_connect = True
        
        
        # Criar osso do antebraço (2 pontos → 1 osso)
        pts = grouped.get("forearm", [])
        if len(pts) >= 2:
            b = eb.new("forearm")
            b.head = pts[0]  
            b.tail = pts[1]   
            bone_map["forearm"] = b



        bpy.ops.object.mode_set(mode="OBJECT")

        # Parenteia malha
        if obj:
            obj.select_set(True)
            arm_obj.select_set(True)
            context.view_layer.objects.active = arm_obj
            bpy.ops.object.parent_set(type="ARMATURE_AUTO")

        rig.generated = True
        self.report({"INFO"}, f"{len(bone_map)} bones gerados.")
        return {"FINISHED"}
