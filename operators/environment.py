import os

import bpy

_ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
_TEMPLATE_PATH = os.path.join(_ASSETS_DIR, "template.blend")
_EXAMPLE_SCANS = {
    "SCAN_1": "ScanMaoEspastica.stl",
    "SCAN_2": "ScanMaoEspastica_2.stl",
}


class ACO_OT_prepare_environment(bpy.types.Operator):
    bl_idname = "aco.prepare_environment"
    bl_label = "Preparar Ambiente"
    bl_description = "Abre o template de ambiente para criação de órteses"
    bl_options = {"REGISTER"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if not os.path.isfile(_TEMPLATE_PATH):
            self.report({"ERROR"}, f"Template não encontrado: {_TEMPLATE_PATH}")
            return {"CANCELLED"}

        bpy.ops.wm.open_mainfile(filepath=_TEMPLATE_PATH)
        return {"FINISHED"}


class ACO_OT_load_example_scan(bpy.types.Operator):
    bl_idname = "aco.load_example_scan"
    bl_label = "Scan de Exemplo"
    bl_description = "Importa um scan de exemplo dos assets do addon"
    bl_options = {"REGISTER", "UNDO"}

    scan: bpy.props.EnumProperty(
        name="Scan",
        items=(
            ("SCAN_1", "Scan Mão Espástica", "Primeiro scan de exemplo"),
            ("SCAN_2", "Scan Mão Espástica 2", "Segundo scan de exemplo"),
        ),
        default="SCAN_1",
        options={"SKIP_SAVE"},
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=280)

    def draw(self, context):
        self.layout.prop(self, "scan", text="Escolher scan")

    def execute(self, context):
        filename = _EXAMPLE_SCANS[self.scan]
        scan_path = os.path.join(_ASSETS_DIR, filename)

        if not os.path.isfile(scan_path):
            self.report({"ERROR"}, f"Scan não encontrado: {scan_path}")
            return {"CANCELLED"}

        bpy.ops.import_mesh.stl(filepath=scan_path)
        return {"FINISHED"}


class ACO_OT_import_stl(bpy.types.Operator):
    bl_idname = "aco.import_stl"
    bl_label = "Importar STL"
    bl_description = "Abre o seletor de arquivo para importar um arquivo STL"
    bl_options = {"REGISTER"}

    def execute(self, context):
        bpy.ops.import_mesh.stl("INVOKE_DEFAULT")
        return {"FINISHED"}
