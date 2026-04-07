import bpy
from bpy.types import Operator
from bpy_extras.view3d_utils import region_2d_to_origin_3d, region_2d_to_vector_3d
from ..utils import next_incomplete, update_progress, points_for, expected


class ACO_OT_select_finger(Operator):
    bl_idname  = "aco.select_finger"
    bl_label   = "Selecionar dedo"
    bl_options = {"REGISTER", "UNDO"}

    finger: bpy.props.StringProperty()

    def execute(self, context):
        rig = context.scene.aco_rig_hand
        #conta os pontos já existem e compara quantos pontos deveriam existir
        if len(points_for(rig, self.finger)) < expected(self.finger):
            rig.active_finger = self.finger

            # Operador modal rodando em loop, capturando eventos (como cliques na malha) até ser finalizado.
            bpy.ops.aco.mark_point_modal("INVOKE_DEFAULT")
        return {"FINISHED"}


class ACO_OT_mark_point_modal(Operator):
    """Modal: clique na malha para registrar pontos do dedo ativo."""
    bl_idname  = "aco.mark_point_modal"
    bl_label   = "Marcar pontos (modal)"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        rig = context.scene.aco_rig_hand
        return bool(rig.active_finger)

    def invoke(self, context, event):
        rig = context.scene.aco_rig_hand
        if not rig.active_finger:
            self.report({"WARNING"}, "Nenhum dedo selecionado.")
            return {"CANCELLED"}

        #Instrui o gerenciador de janelas do Blender a direcionar os eventos do usuário (como cliques de mouse ou teclas pressionadas) para o modal() da classe (self)
        context.window_manager.modal_handler_add(self)
        context.area.header_text_set(
            f"Clique na malha para marcar pontos — ESC para sair"
        )
        return {"RUNNING_MODAL"}




    def modal(self, context, event):
        rig = context.scene.aco_rig_hand

        # Sai do modal se não há mais dedo ativo ou todos completos
        if not rig.active_finger:
            self._finish(context)
            return {"FINISHED"}

        # Cancela com ESC ou botão direito
        if event.type in {"ESC", "RIGHTMOUSE"} and event.value == "PRESS":
            rig.active_finger = ""
            #cancela e sai do modal
            self._finish(context)
            return {"CANCELLED"}

        # Registra ponto com clique esquerdo
        if event.type == "LEFTMOUSE" and event.value == "PRESS":
            obj = context.active_object
            if not obj or obj.type != "MESH":
                self.report({"WARNING"}, "Selecione uma malha primeiro.")
                return {"RUNNING_MODAL"}
            
            # Coordenadas do mouse na região
            coord      = event.mouse_region_x, event.mouse_region_y
            region     = context.region
            rv3d       = context.region_data

            if not region or not rv3d:
                return {"RUNNING_MODAL"}

            # Calcula a origem do raio (ponto no espaço 3D)
            ray_origin    = region_2d_to_origin_3d(region, rv3d, coord)
            ray_direction = region_2d_to_vector_3d(region, rv3d, coord)
            
            #tras coordenadas do mundo para dentro do objeto poi no blender um objeto tem sua própria origem (0,0,0)
            mwi           = obj.matrix_world.inverted()
            
            #Detecta se e onde atinge a superficie da malha 
            result, loc, *_  = obj.ray_cast(mwi @ ray_origin, mwi.to_3x3() @ ray_direction)

            if not result:
                self.report({"WARNING"}, "Nenhuma superfície sob o cursor.")
                return {"RUNNING_MODAL"}

            # Salva o ponto
            pt       = rig.joint_points.add()
            pt.co    = obj.matrix_world @ loc
            pt.group = rig.active_finger

            update_progress(rig)

            # Verifica se o dedo ativo já foi totalmente marcado
            if len(points_for(rig, rig.active_finger)) >= expected(rig.active_finger):
                self._finish(context)
                return {"FINISHED"}

            # Força redesenho do painel
            for area in context.screen.areas:
                area.tag_redraw()

            return {"RUNNING_MODAL"}

        # Passa qualquer outro evento adiante (navegação do viewport, etc.)
        return {"PASS_THROUGH"}

    def _finish(self, context):
        context.area.header_text_set(None)  # restaura o header padrão