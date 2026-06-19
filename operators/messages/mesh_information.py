import bpy
from bpy.types import Operator

class ACO_current_mesh_information(Operator):
    bl_idname = "aco.current_mesh_information"
    bl_label = "Informação da Malha"
    bl_description = "Abre o template de informação do estado da malha"
    bl_options = {"REGISTER"}

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=350)

    def _draw_section(self, layout, title, icon, manipulation_info):
        box = layout.box()

        # Cabeçalho
        header = box.row()
        header.label(text=title, icon=icon)

        # Volume antes
        row = box.row(align=True)
        row.label(text="Volume antes:")
        row.label(text=f"{manipulation_info.volume_before:.4f} BU³")

        # Volume depois
        row = box.row(align=True)
        row.label(text="Volume depois:")
        row.label(text=f"{manipulation_info.volume_after:.4f} BU³")

        # Variação
        row = box.row(align=True)
        row.label(text="Variação:")
        if manipulation_info.volume_valid:
            row.label(text=f"{manipulation_info.volume_change_percent:+.2f}%")
            box.label(
                text=self._volume_interpretation(manipulation_info.volume_change_percent),
                icon="CHECKMARK"
            )
        else:
            row.label(text="N/A")
            box.label(text="Volume indisponível para esta malha.", icon="ERROR")

    def _volume_interpretation(self, percent):
        if abs(percent) < 0.5:
            return "Volume praticamente inalterado"
        elif percent > 0:
            return f"Volume aumentou {percent:.2f}%"
        else:
            return f"Volume reduziu {abs(percent):.2f}%"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Informações da Malha", icon="MESH_DATA")
        layout.separator()

        self._draw_section(layout, "Reparo",   "TOOL_SETTINGS", scene.aco_repair)
        self._draw_section(layout, "Limpeza",  "BRUSH_DATA",    scene.aco_quad_remesh)
        self._draw_section(layout, "Redução",  "MOD_DECIM",     scene.aco_reduction)

    def execute(self, context):
        return {"FINISHED"}