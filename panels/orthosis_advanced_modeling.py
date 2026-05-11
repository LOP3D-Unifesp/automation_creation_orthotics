import bpy
from ..utils import get_defs, points_for, expected, is_ready_to_generate
from ..properties import NEXT_POINT_LABELS

#Modificar o nome da classe em outros arquivos
class ACO_PT_OrthosisAdvancedModeling(bpy.types.Panel):
    bl_label = "Modelagem Avançada"
    bl_idname = "ACO_PT_orthosis_advanced_modeling"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Automação de Órteses"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label(text="", icon="MOD_BUILD")
        
        
    # -------------------------------------------------------------------------
    # Rigging da Mão
    # -------------------------------------------------------------------------
        
    def _draw_rigging_upper_limb(self, layout, scene):
        
        box = layout.box()
        rig = scene.aco_rig_hand
        defs = get_defs()

        # Cabeçalho
        header = box.row(align=True)
        header.label(text="Rigging do membro superior", icon="MOD_ARMATURE")
        toggle = header.row(align=True)
        toggle.alignment = "RIGHT"
        toggle.prop(
            rig, "show_options", 
            text="",
            icon="TRIA_DOWN" if rig.show_options else "TRIA_RIGHT",
            emboss=False,
        )

        if not rig.show_options:
            return

        # Instrução contextual
        if rig.generated:
            box.label(text="Gerado. Limpe para recomeçar.", icon="CHECKMARK")
        elif not rig.active_finger:
            if rig.group_to_remove == "None":
                box.label(text="Selecione um segmento abaixo.", icon="INFO")
            else:
                alert_row = box.row()
                alert_row.alert = True
                alert_row.label(
                    text="Para reseleção, selecione a malha primeiro.",
                    icon="ERROR",
                )
        else:
            
            # Pega qual dedo está ativo
            key = rig.active_finger

            # Pega os pontos já criados para esse dedo
            pts = points_for(rig, key)

            # Quantos pontos deveriam existir
            exp = expected(key)

            # Verifica se ainda faltam pontos
            if len(pts) < exp:
                labels = NEXT_POINT_LABELS.get(key, [])
                proximo = labels[len(pts)]
            else:
                proximo = "—"

            # Cria um dicionário com os nomes dos dedos
            label_map = {}
            for k, lbl, _ in defs:
                label_map[k] = lbl

            # Mostra a mensagem na interface
            texto = (
                label_map.get(key, key)
                + ': clique em "' + proximo + '" na malha '
                + f'({len(pts)+1}/{exp})'
            )

            box.label(text=texto, icon="RADIOBUT_ON")

        # Barra de progresso
        prog_row = box.row()
        prog_row.prop(rig, "progress", text="Progresso", slider=True)
        prog_row.enabled = False

        # Lista de dedos
        col = box.column(align=True)
        for key, label, names in defs:
            
            #Calcula progresso do dedo
            pts = points_for(rig, key)
            exp = len(names)
            done = len(pts) >= exp

            row = col.row(align=True)
            #True se o dedo está parcialmente preenchido

            row.alert = (0 < len(pts) < exp)

            #depress, deixa o botão “pressionado” se o dedo ativo e não está completo
            op = row.operator(
                "aco.select_finger",
                text=label,
                icon=(
                    "LAYER_ACTIVE" if done else
                    "RADIOBUT_ON"  if rig.active_finger == key else
                    "LAYER_USED"   if len(pts) > 0 else
                    "LAYER_ACTIVE"
                ),
                depress=(rig.active_finger == key and not done),
            )
            #Passa a chave do dedo para o operador
            op.finger = key
            row.label(text=f"{len(pts)}/{exp}")

        box.separator(factor=0.5)

        # Ações
        action_row = box.row(align=True)
        

        if len(rig.joint_points) > 0:
            action_row.operator("aco.undo_point", text="", icon="LOOP_BACK")
            
            box.operator("aco.clear_joint_points", text="Limpar tudo", icon="X")

        ##Adicionar operador para criar apenas um bone
        if is_ready_to_generate(rig):
            
                
            action_row.operator(
                "aco.generate_hand_bones",
                text="Gerar bones",
                icon="OUTLINER_OB_ARMATURE",
            )
            
                 
           
            if rig.generated:
                
                col = layout.column(align=True)
                col.label(text="Dedo selecionado", icon="HAND")
                col.prop(rig, "group_to_remove", text="")
                
                action_row.separator(factor=0.5)
                
                col_remove = layout.row()
                col_remove.alert = True
                col_remove.operator("aco.redo_finger_bone", text="Remover Bone Selecionado", icon="X")
                col_remove.alert = False
                col_remove.operator("aco.cancel_selected_finger", text="Cancelar seleção", icon="LOOP_BACK")
                
                col_remove.separator(factor=0.5)
                
                               
                #action_row.operator("wm.call_menu", text="Gerar único bone").name = "ACO_MT_list_of_fingers_hand"

        
        
        
        
        
        

    def draw(self, context):                          
        scene = context.scene                         
        layout = self.layout
        
        self._draw_rigging_upper_limb(layout, scene)

       

       
    