import bpy 


class ACO_PT_OrthosisInitialization(bpy.types.Panel):
    bl_label = "Inicializa\u00e7\u00e3o"
    bl_idname = "ACO_PT_orthosis_initialization"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Automa\u00e7\u00e3o de \u00d3rteses"

    def draw_header(self, context):
        self.layout.label(text="", icon="TOOL_SETTINGS")

    def draw(self, context):
        layout = self.layout

        buttons_column = layout.column(align=True)
        buttons_column.operator("aco.prepare_environment", text="Preparar Ambiente", icon="PREFERENCES")
        buttons_column.operator("aco.import_stl", text="Importar STL", icon="IMPORT")
        buttons_column.operator("aco.load_example_scan", text="Scan de Exemplo", icon="FILE_3D")

