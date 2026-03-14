import textwrap

import bpy


def _safe_icon_name(primary, fallback="NONE"):
    icon_enum = bpy.types.UILayout.bl_rna.functions["label"].parameters["icon"].enum_items.keys()
    return primary if primary in icon_enum else fallback


def _wrapped_lines(text, region_width, horizontal_padding=36):
    approx_char_px = 7
    usable_width = max(120, region_width - horizontal_padding)
    max_chars = max(16, usable_width // approx_char_px)
    return textwrap.wrap(text, width=max_chars, break_long_words=False, break_on_hyphens=False)


def _draw_wrapped_label(layout, text, region_width, horizontal_padding=36):
    for line in _wrapped_lines(text, region_width, horizontal_padding=horizontal_padding):
        layout.label(text=line)


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
        buttons_column.enabled = False
        buttons_column.operator("aco.number_of_vertices_and_face", text="Preparar Ambiente", icon="PREFERENCES")
        buttons_column.operator("aco.number_of_vertices_and_face", text="Importar STL", icon="IMPORT")
        buttons_column.operator("aco.number_of_vertices_and_face", text="Scan de Exemplo", icon="FILE_3D")


class ACO_PT_OrthosisPrepareModel(bpy.types.Panel):
    bl_label = "Preparar modelo"
    bl_idname = "ACO_PT_orthosis_prepare_model"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Automa\u00e7\u00e3o de \u00d3rteses"
    bl_options = {"DEFAULT_CLOSED"}

    def draw_header(self, context):
        self.layout.label(text="", icon="MOD_REMESH")

    def _draw_model_diagnostics(self, layout, scene):
        box = layout.box()
        box.label(text="Diagn\u00f3stico do modelo", icon="MESH_DATA")

        row = box.row(align=True)
        row.label(text=f"V\u00e9rtices: {scene.vertices}")
        row.label(text=f"Faces: {scene.faces}")

        box.operator("aco.number_of_vertices_and_face", text="Atualizar an\u00e1lise", icon="FILE_REFRESH")

    def _draw_model_alignment(self, layout, scene):
        box = layout.box()
        box.label(text="Orienta\u00e7\u00e3o do modelo", icon="ORIENTATION_GLOBAL")

        center_row = box.row(align=True)
        center_row.scale_y = 1.15
        center_row.operator(
            "aco.prepare_model_auto",
            text="Centralizar",
            icon=_safe_icon_name("VIEW_PAN", "FULLSCREEN_ENTER"),
        )

        axis_row = box.row(align=True)
        axis_row.prop(scene.align_limb_props, "axis_x", text="X", toggle=True)
        axis_row.prop(scene.align_limb_props, "axis_y", text="Y", toggle=True)
        axis_row.prop(scene.align_limb_props, "axis_z", text="Z", toggle=True)

        has_axis_selected = scene.align_limb_props.axis_x or scene.align_limb_props.axis_y or scene.align_limb_props.axis_z

        align_row = box.row(align=True)
        align_row.enabled = has_axis_selected
        align_row.operator(
            "aco.align_limb_axis",
            text="Alinhar modelo",
            icon=_safe_icon_name("ORIENTATION_GLOBAL", "DRIVER_ROTATIONAL_DIFFERENCE"),
        )

        if not has_axis_selected:
            box.label(text="Selecione ao menos um eixo para alinhar.", icon="ERROR")

    def _draw_reduction_operation(self, container, scene, context, title, icon, prop_name, prop_label, toggle_prop, hint):
        title_row = container.row(align=True)
        title_row.label(text=title, icon=icon)
        title_row.prop(scene, toggle_prop, text="", toggle=True)

        controls_row = container.row(align=True)
        controls_row.scale_y = 1.05
        controls_row.enabled = getattr(scene, toggle_prop)
        controls_row.prop(scene, prop_name, text=prop_label, slider=True)

        _draw_wrapped_label(container, hint, context.region.width, horizontal_padding=52)

    def _draw_reduction_presets(self, box):
        box.label(text="Presets de redu\u00e7\u00e3o", icon=_safe_icon_name("PRESET", "SETTINGS"))

        row = box.row(align=True)

        op_light = row.operator("aco.apply_reduction_preset", text="Leve", icon="DOT")
        op_light.preset = "LIGHT"

        op_medium = row.operator("aco.apply_reduction_preset", text="M\u00e9dio", icon="DOT")
        op_medium.preset = "MEDIUM"

        op_strong = row.operator("aco.apply_reduction_preset", text="Forte", icon="DOT")
        op_strong.preset = "STRONG"

    def _draw_auto_cleanup(self, context, layout, scene):
        box = layout.box()

        header = box.row(align=True)
        header.label(text="Limpeza autom\u00e1tica", icon="MOD_REMESH")

        toggle = header.row(align=True)
        toggle.alignment = "RIGHT"
        toggle.prop(
            scene,
            "show_quad_remesh_options",
            text="",
            icon="TRIA_DOWN" if scene.show_quad_remesh_options else "TRIA_RIGHT",
            emboss=False,
        )

        if not scene.show_quad_remesh_options:
            box.label(text="Expandir para ajustar a limpeza autom\u00e1tica.", icon="INFO")
            return

        controls = box.row(align=True)
        controls.scale_y = 1.05
        controls.prop(scene, "quad_remesh_voxel_size", text="Resolu\u00e7\u00e3o da malha", slider=True)

        smooth_row = box.row(align=True)
        smooth_row.prop(scene, "quad_remesh_smooth_shade", text="Suavizar")

        apply_row = box.row(align=True)
        apply_row.operator_context = "EXEC_DEFAULT"
        apply_row.operator("aco.apply_quad_remesh", text="Aplicar Quad Remesh", icon="CHECKMARK")

        _draw_wrapped_label(
            box,
            "Valores maiores simplificam mais; valores menores preservam mais detalhes.",
            context.region.width,
            horizontal_padding=52,
        )
        _draw_wrapped_label(
            box,
            "Boa op\u00e7\u00e3o para limpar a malha antes do design da \u00f3rtese.",
            context.region.width,
            horizontal_padding=52,
        )

    def _cleanup_interpretation(self, change_percent):
        absolute_change = abs(change_percent)
        if absolute_change <= 3.0:
            return "Baixa altera\u00e7\u00e3o geom\u00e9trica"
        if absolute_change <= 8.0:
            return "Preserva\u00e7\u00e3o global moderada"
        return "Altera\u00e7\u00e3o geom\u00e9trica elevada"

    def _draw_cleanup_result(self, layout, scene):
        box = layout.box()
        box.label(text="Resultado da limpeza", icon="INFO")

        row_before = box.row(align=True)
        row_before.label(text="Volume antes")
        row_before.label(text=f"{scene.quad_remesh_volume_before:.4f} BU\u00b3")

        row_after = box.row(align=True)
        row_after.label(text="Volume depois")
        row_after.label(text=f"{scene.quad_remesh_volume_after:.4f} BU\u00b3")

        row_change = box.row(align=True)
        row_change.label(text="Varia\u00e7\u00e3o")
        if scene.quad_remesh_volume_valid:
            row_change.label(text=f"{scene.quad_remesh_volume_change_percent:+.2f}%")
            box.label(text=self._cleanup_interpretation(scene.quad_remesh_volume_change_percent), icon="CHECKMARK")
        else:
            row_change.label(text="N/A")
            box.label(text="Volume indispon\u00edvel para esta malha.", icon="ERROR")

    def _draw_advanced_reduction(self, context, layout, scene):
        box = layout.box()

        header = box.row(align=True)
        header.label(text="Redu\u00e7\u00e3o da malha", icon="MOD_DECIM")

        toggle = header.row(align=True)
        toggle.alignment = "RIGHT"
        toggle.prop(
            scene,
            "show_prepare_advanced",
            text="",
            icon="TRIA_DOWN" if scene.show_prepare_advanced else "TRIA_RIGHT",
            emboss=False,
        )

        if not scene.show_prepare_advanced:
            box.label(text="Expandir para presets, Decima\u00e7\u00e3o, Un-Subdivide e Planar.", icon="INFO")
            return

        box.operator_context = "EXEC_DEFAULT"

        self._draw_reduction_presets(box)
        box.separator(factor=0.5)

        self._draw_reduction_operation(
            container=box,
            scene=scene,
            context=context,
            title="Decima\u00e7\u00e3o",
            icon="MOD_TRIANGULATE",
            prop_name="decimate_collapse_reduction_percent",
            prop_label="Redu\u00e7\u00e3o (%)",
            toggle_prop="reduction_use_collapse",
            hint="90% reduz ~90% das faces (mant\u00e9m ~10%).",
        )

        box.separator(factor=0.3)

        self._draw_reduction_operation(
            container=box,
            scene=scene,
            context=context,
            title="Un-Subdivide",
            icon="MOD_SUBSURF",
            prop_name="decimate_unsubdivide_iterations",
            prop_label="Itera\u00e7\u00f5es",
            toggle_prop="reduction_use_unsubdivide",
            hint="Maior valor remove mais subdivis\u00f5es regulares.",
        )

        box.separator(factor=0.3)

        self._draw_reduction_operation(
            container=box,
            scene=scene,
            context=context,
            title="Planar",
            icon=_safe_icon_name("SNAP_FACE", "MODIFIER"),
            prop_name="decimate_planar_angle",
            prop_label="\u00c2ngulo",
            toggle_prop="reduction_use_planar",
            hint="Maior \u00e2ngulo simplifica mais \u00e1reas quase planas.",
        )

        has_any_step = scene.reduction_use_collapse or scene.reduction_use_unsubdivide or scene.reduction_use_planar
        apply_row = box.row(align=True)
        apply_row.enabled = has_any_step
        apply_row.operator("aco.apply_mesh_reduction_pipeline", text="Aplicar redu\u00e7\u00e3o da malha", icon="CHECKMARK")

        if not has_any_step:
            box.label(text="Marque ao menos uma etapa para aplicar.", icon="ERROR")

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        self._draw_model_diagnostics(layout, scene)
        self._draw_model_alignment(layout, scene)
        self._draw_auto_cleanup(context, layout, scene)
        self._draw_cleanup_result(layout, scene)
        self._draw_advanced_reduction(context, layout, scene)


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
        _draw_wrapped_label(layout, "1. Encontrar landmarks anat\u00f4micos", context.region.width, horizontal_padding=36)
        _draw_wrapped_label(layout, "2. Rigging", context.region.width, horizontal_padding=36)
        _draw_wrapped_label(layout, "3. Reposicionamento anat\u00f4mico", context.region.width, horizontal_padding=36)
