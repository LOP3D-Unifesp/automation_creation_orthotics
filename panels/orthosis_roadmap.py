import bpy
from ..utils import _draw_wrapped_label


class ACO_PT_OrthosisRoadmap(bpy.types.Panel):
    bl_label = "Roadmap"
    bl_idname = "ACO_PT_orthosis_roadmap"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Automa\u00e7\u00e3o de \u00d3rteses"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label(text="", icon="INFO")

    def draw(self, context):
        layout = self.layout
        _draw_wrapped_label(layout, "1. Reposicionamento anat\u00f4mico", context.region.width, horizontal_padding=36)
        _draw_wrapped_label(layout, "2. Calcular e mostrar a angula\u00e7\u00e3o de cada articula\u00e7\u00e3o", context.region.width, horizontal_padding=36)

        
