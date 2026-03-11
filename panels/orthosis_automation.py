import bpy


class ACO_PT_OrthosisAutomation(bpy.types.Panel):
    bl_label = "Automação na Criação de Órteses"
    bl_name = "VIEW3D_PT_OrthosisAutomation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Automação de Órteses'


    def draw(self, context):
        layout = self.layout
        scene = context.scene

        align_axis = scene.align_limb_props


        layout.label(text="Decimação: ")
        row = layout.row()
        row.operator("aco.reduce_polygonos_by_collapse", text="Collapse")
        row.operator("aco.reduce_polygonos_by_un_subdivide", text="Un-Subdivide")
        row.operator("aco.reduce_polygonos_by_planar", text="Planar")


        layout.label(text=f"Números de Vértices: {context.scene.vertices} e Faces: {context.scene.faces}")
        layout.operator("my.vertex_count", text="Atualizar Contagem")


        layout.separator(factor=2.0)


        layout.label(text="Eixo de Alinhamento: ")
        layout.prop(align_axis, "axis", expand=True)
        # Botão do operador
        layout.operator("aco.align_limb_axis", text="Alinhar", icon="FULLSCREEN_ENTER")


        layout.separator(factor=2.0)

        #Tratar o erro se o objeto não estiver ativo

       


        #layout.label(text="")
