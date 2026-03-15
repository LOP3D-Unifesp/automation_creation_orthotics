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
        buttons_column.operator("aco.prepare_environment", text="Preparar Ambiente", icon="PREFERENCES")
        buttons_column.operator("aco.import_stl", text="Importar STL", icon="IMPORT")
        buttons_column.operator("aco.load_example_scan", text="Scan de Exemplo", icon="FILE_3D")


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
        diag = scene.aco_diagnostics

        row = box.row(align=True)
        row.label(text=f"V\u00e9rtices: {diag.vertices}")
        row.label(text=f"Faces: {diag.faces}")

        box.operator("aco.number_of_vertices_and_face", text="Atualizar an\u00e1lise", icon="FILE_REFRESH")

        if diag.vertices > 0 and diag.health_analyzed:
            if diag.health_valid:
                box.label(text="Malha sem problemas detectados", icon="CHECKMARK")
            else:
                if diag.non_manifold_edges > 0:
                    box.label(text=f"{diag.non_manifold_edges} arestas n\u00e3o-manifold", icon="ERROR")
                if diag.loose_vertices > 0:
                    box.label(text=f"{diag.loose_vertices} v\u00e9rtices soltos", icon="ERROR")
                if diag.zero_area_faces > 0:
                    box.label(text=f"{diag.zero_area_faces} faces com \u00e1rea zero", icon="ERROR")
            if diag.boundary_edges > 0:
                box.label(text=f"{diag.boundary_edges} arestas de borda (buracos)", icon="ERROR")
            if diag.duplicate_vertices > 0:
                box.label(text=f"{diag.duplicate_vertices} v\u00e9rtices sobrepostos", icon="ERROR")
            if diag.flipped_faces > 0:
                box.label(text=f"{diag.flipped_faces} faces com normais invertidas", icon="INFO")
            if diag.self_intersecting_faces > 0:
                box.label(text=f"{diag.self_intersecting_faces} faces auto-intersectantes", icon="ERROR")

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

        has_axis_selected = (
            scene.align_limb_props.axis_x
            or scene.align_limb_props.axis_y
            or scene.align_limb_props.axis_z
        )

        align_row = box.row(align=True)
        align_row.enabled = has_axis_selected
        align_row.operator(
            "aco.align_limb_axis",
            text="Alinhar modelo",
            icon=_safe_icon_name("ORIENTATION_GLOBAL", "DRIVER_ROTATIONAL_DIFFERENCE"),
        )

        if not has_axis_selected:
            box.label(text="Selecione ao menos um eixo para alinhar.", icon="ERROR")

    def _cleanup_interpretation(self, change_percent):
        absolute_change = abs(change_percent)
        if absolute_change <= 3.0:
            return "Baixa altera\u00e7\u00e3o geom\u00e9trica"
        if absolute_change <= 8.0:
            return "Preserva\u00e7\u00e3o global moderada"
        return "Altera\u00e7\u00e3o geom\u00e9trica elevada"

    # -------------------------------------------------------------------------
    # Reparo de malha
    # -------------------------------------------------------------------------

    def _draw_repair_section(self, context, layout, scene):
        box = layout.box()
        repair = scene.aco_repair
        diag = scene.aco_diagnostics

        header = box.row(align=True)
        header.label(text="Reparar malha", icon="TOOL_SETTINGS")

        toggle = header.row(align=True)
        toggle.alignment = "RIGHT"
        toggle.prop(
            repair,
            "show_options",
            text="",
            icon="TRIA_DOWN" if repair.show_options else "TRIA_RIGHT",
            emboss=False,
        )

        if diag.health_analyzed and (diag.non_manifold_edges > 0 or diag.boundary_edges > 0):
            box.label(
                text="Malha com buracos \u2014 remesh pode produzir resultado incorreto.",
                icon="ERROR",
            )

        if repair.show_options:
            if 0.0 < repair.progress < 1.0:
                box.prop(repair, "progress", text="Progresso", slider=True)
            else:
                apply_row = box.row(align=True)
                apply_row.operator("aco.repair_mesh", text="Reparar malha", icon="CHECKMARK")

                self._draw_repair_result(box, scene)

    def _draw_repair_result(self, layout, scene):
        box = layout.box()
        box.label(text="Resultado do reparo", icon="INFO")
        repair = scene.aco_repair

        row_before = box.row(align=True)
        row_before.label(text="Volume antes")
        row_before.label(text=f"{repair.volume_before:.4f} BU\u00b3")

        row_after = box.row(align=True)
        row_after.label(text="Volume depois")
        row_after.label(text=f"{repair.volume_after:.4f} BU\u00b3")

        row_change = box.row(align=True)
        row_change.label(text="Varia\u00e7\u00e3o")
        if repair.volume_valid:
            row_change.label(text=f"{repair.volume_change_percent:+.2f}%")
            box.label(text=self._cleanup_interpretation(repair.volume_change_percent), icon="CHECKMARK")
        else:
            row_change.label(text="N/A")
            box.label(text="Volume indispon\u00edvel para esta malha.", icon="ERROR")

    # -------------------------------------------------------------------------
    # Limpeza automática (Quad Remesh)
    # -------------------------------------------------------------------------

    def _draw_auto_cleanup(self, context, layout, scene):
        box = layout.box()
        qr = scene.aco_quad_remesh

        header = box.row(align=True)
        header.label(text="Limpeza autom\u00e1tica", icon="MOD_REMESH")

        toggle = header.row(align=True)
        toggle.alignment = "RIGHT"
        toggle.prop(
            qr,
            "show_options",
            text="",
            icon="TRIA_DOWN" if qr.show_options else "TRIA_RIGHT",
            emboss=False,
        )

        if qr.show_options:
            controls = box.row(align=True)
            controls.scale_y = 1.05
            controls.prop(qr, "voxel_size", text="Resolu\u00e7\u00e3o da malha", slider=True)

            smooth_row = box.row(align=True)
            smooth_row.prop(qr, "smooth_shade", text="Suavizar")

            apply_row = box.row(align=True)
            apply_row.operator_context = "EXEC_DEFAULT"
            apply_row.operator("aco.apply_quad_remesh", text="Aplicar Quad Remesh", icon="CHECKMARK")

            self._draw_cleanup_result(box, scene)

    def _draw_cleanup_result(self, layout, scene):
        box = layout.box()
        box.label(text="Resultado da limpeza", icon="INFO")
        qr = scene.aco_quad_remesh

        row_before = box.row(align=True)
        row_before.label(text="Volume antes")
        row_before.label(text=f"{qr.volume_before:.4f} BU\u00b3")

        row_after = box.row(align=True)
        row_after.label(text="Volume depois")
        row_after.label(text=f"{qr.volume_after:.4f} BU\u00b3")

        row_change = box.row(align=True)
        row_change.label(text="Varia\u00e7\u00e3o")
        if qr.volume_valid:
            row_change.label(text=f"{qr.volume_change_percent:+.2f}%")
            box.label(text=self._cleanup_interpretation(qr.volume_change_percent), icon="CHECKMARK")
        else:
            row_change.label(text="N/A")
            box.label(text="Volume indispon\u00edvel para esta malha.", icon="ERROR")

    # -------------------------------------------------------------------------
    # Redução avançada
    # -------------------------------------------------------------------------

    def _draw_reduction_operation(self, container, reduction, context, title, icon, prop_name, prop_label, toggle_prop, hint):
        title_row = container.row(align=True)
        title_row.label(text=title, icon=icon)
        title_row.prop(reduction, toggle_prop, text="", toggle=True)

        controls_row = container.row(align=True)
        controls_row.scale_y = 1.05
        controls_row.enabled = getattr(reduction, toggle_prop)
        controls_row.prop(reduction, prop_name, text=prop_label, slider=True)

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

    def _draw_advanced_reduction(self, context, layout, scene):
        box = layout.box()
        reduction = scene.aco_reduction

        header = box.row(align=True)
        header.label(text="Redu\u00e7\u00e3o da malha", icon="MOD_DECIM")

        toggle = header.row(align=True)
        toggle.alignment = "RIGHT"
        toggle.prop(
            reduction,
            "show_advanced",
            text="",
            icon="TRIA_DOWN" if reduction.show_advanced else "TRIA_RIGHT",
            emboss=False,
        )

        if reduction.show_advanced:
            box.operator_context = "EXEC_DEFAULT"

            self._draw_reduction_presets(box)
            box.separator(factor=0.5)

            self._draw_reduction_operation(
                container=box,
                reduction=reduction,
                context=context,
                title="Decima\u00e7\u00e3o",
                icon="MOD_TRIANGULATE",
                prop_name="collapse_percent",
                prop_label="Redu\u00e7\u00e3o (%)",
                toggle_prop="use_collapse",
                hint="90% reduz ~90% das faces (mant\u00e9m ~10%).",
            )

            box.separator(factor=0.3)

            self._draw_reduction_operation(
                container=box,
                reduction=reduction,
                context=context,
                title="Un-Subdivide",
                icon="MOD_SUBSURF",
                prop_name="unsubdiv_iterations",
                prop_label="Itera\u00e7\u00f5es",
                toggle_prop="use_unsubdivide",
                hint="Maior valor remove mais subdivis\u00f5es regulares.",
            )

            box.separator(factor=0.3)

            self._draw_reduction_operation(
                container=box,
                reduction=reduction,
                context=context,
                title="Planar",
                icon=_safe_icon_name("SNAP_FACE", "MODIFIER"),
                prop_name="planar_angle",
                prop_label="\u00c2ngulo",
                toggle_prop="use_planar",
                hint="Maior \u00e2ngulo simplifica mais \u00e1reas quase planas.",
            )

            has_any_step = reduction.use_collapse or reduction.use_unsubdivide or reduction.use_planar
            apply_row = box.row(align=True)
            apply_row.enabled = has_any_step
            apply_row.operator("aco.apply_mesh_reduction_pipeline", text="Aplicar redu\u00e7\u00e3o da malha", icon="CHECKMARK")

            if not has_any_step:
                box.label(text="Marque ao menos uma etapa para aplicar.", icon="ERROR")

            self._draw_reduction_result(box, scene)

    def _draw_reduction_result(self, layout, scene):
        box = layout.box()
        box.label(text="Resultado da redu\u00e7\u00e3o", icon="INFO")
        reduction = scene.aco_reduction

        row_before = box.row(align=True)
        row_before.label(text="Volume antes")
        row_before.label(text=f"{reduction.volume_before:.4f} BU\u00b3")

        row_after = box.row(align=True)
        row_after.label(text="Volume depois")
        row_after.label(text=f"{reduction.volume_after:.4f} BU\u00b3")

        row_change = box.row(align=True)
        row_change.label(text="Varia\u00e7\u00e3o")
        if reduction.volume_valid:
            row_change.label(text=f"{reduction.volume_change_percent:+.2f}%")
            box.label(text=self._cleanup_interpretation(reduction.volume_change_percent), icon="CHECKMARK")
        else:
            row_change.label(text="N/A")
            box.label(text="Volume indispon\u00edvel para esta malha.", icon="ERROR")

    # -------------------------------------------------------------------------
    # draw()
    # -------------------------------------------------------------------------

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        self._draw_model_diagnostics(layout, scene)
        self._draw_model_alignment(layout, scene)
        self._draw_repair_section(context, layout, scene)
        self._draw_auto_cleanup(context, layout, scene)
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
