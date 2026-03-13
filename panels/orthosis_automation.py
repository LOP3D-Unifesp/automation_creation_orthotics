import textwrap

import bpy


def _wrapped_lines(text, region_width, horizontal_padding=36):
    approx_char_px = 7
    usable_width = max(120, region_width - horizontal_padding)
    max_chars = max(16, usable_width // approx_char_px)
    return textwrap.wrap(text, width=max_chars, break_long_words=False, break_on_hyphens=False)


def _draw_wrapped_label(layout, text, region_width, horizontal_padding=36):
    for line in _wrapped_lines(text, region_width, horizontal_padding=horizontal_padding):
        layout.label(text=line)


class ACO_PT_OrthosisInitialization(bpy.types.Panel):
    bl_label = "Inicialização"
    bl_idname = "ACO_PT_orthosis_initialization"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Automação de Órteses"

    def draw_header(self, context):
        self.layout.label(text="", icon="TOOL_SETTINGS")

    def draw(self, context):
        layout = self.layout

        buttons_column = layout.column(align=True)
        buttons_column.enabled = False
        buttons_column.operator("aco.number_of_vertices_and_face", text="Preparar Ambiente", icon="PREFERENCES")
        buttons_column.operator("aco.number_of_vertices_and_face", text="Importar STL", icon="IMPORT")
        buttons_column.operator("aco.number_of_vertices_and_face", text="Scan de Exemplo", icon="FILE_3D")

        _draw_wrapped_label(
            layout,
            "Carrega o scan de exemplo (ScanMaoEspastica.stl).",
            context.region.width,
            horizontal_padding=36,
        )


class ACO_PT_OrthosisPrepareModel(bpy.types.Panel):
    bl_label = "Preparar modelo"
    bl_idname = "ACO_PT_orthosis_prepare_model"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Automação de Órteses"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label(text="", icon="MOD_REMESH")

    def _draw_decimation_block(self, context, layout, scene):
        box = layout.box()
        box.label(text="Decimação", icon="MOD_DECIM")

        box.label(text="Collapse")
        box.prop(scene, "decimate_collapse_ratio", text="Ratio")
        collapse_col = box.column(align=True)
        collapse_col.operator_context = "EXEC_DEFAULT"
        collapse_operator = collapse_col.operator(
            "aco.reduce_polygonos_by_collapse",
            text="Aplicar Collapse",
            icon="CHECKMARK",
        )
        collapse_operator.ratio = scene.decimate_collapse_ratio
        _draw_wrapped_label(box, "Reduz polígonos mantendo a forma geral.", context.region.width, horizontal_padding=52)

        box.separator(factor=0.5)
        box.label(text="Un-Subdivide")
        box.prop(scene, "decimate_unsubdivide_iterations", text="Iterações")
        unsubdivide_col = box.column(align=True)
        unsubdivide_col.operator_context = "EXEC_DEFAULT"
        unsubdivide_operator = unsubdivide_col.operator(
            "aco.reduce_polygonos_by_un_subdivide",
            text="Aplicar Un-Subdivide",
            icon="CHECKMARK",
        )
        unsubdivide_operator.iterations = scene.decimate_unsubdivide_iterations
        _draw_wrapped_label(box, "Tenta desfazer subdivisões regulares.", context.region.width, horizontal_padding=52)

        box.separator(factor=0.5)
        box.label(text="Planar")
        box.prop(scene, "decimate_planar_angle", text="Ângulo")
        planar_col = box.column(align=True)
        planar_col.operator_context = "EXEC_DEFAULT"
        planar_operator = planar_col.operator(
            "aco.reduce_polygonos_by_planar",
            text="Aplicar Planar",
            icon="CHECKMARK",
        )
        planar_operator.angle_limit = scene.decimate_planar_angle
        _draw_wrapped_label(box, "Simplifica áreas quase planas.", context.region.width, horizontal_padding=52)

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        info_box = layout.box()
        info_box.label(text=f"Vértices: {scene.vertices}")
        info_box.label(text=f"Faces: {scene.faces}")
        info_box.operator("aco.number_of_vertices_and_face", text="Atualizar Contagem", icon="FILE_REFRESH")

        self._draw_decimation_block(context, layout, scene)

        alignment_box = layout.box()
        alignment_box.label(text="Alinhamento", icon="ORIENTATION_GLOBAL")
        alignment_box.prop(scene.align_limb_props, "axis", expand=True)
        alignment_box.operator("aco.align_limb_axis", text="Alinhar", icon="CON_TRANSFORM")


class ACO_PT_OrthosisRoadmap(bpy.types.Panel):
    bl_label = "Roadmap"
    bl_idname = "ACO_PT_orthosis_roadmap"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Automação de Órteses"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label(text="", icon="INFO")

    def draw(self, context):
        layout = self.layout
        _draw_wrapped_label(layout, "1. Encontrar landmarks anatômicos", context.region.width, horizontal_padding=36)
        _draw_wrapped_label(layout, "2. Rigging", context.region.width, horizontal_padding=36)
        _draw_wrapped_label(layout, "3. Reposicionamento anatômico", context.region.width, horizontal_padding=36)