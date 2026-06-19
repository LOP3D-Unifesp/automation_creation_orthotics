import os

import bpy

from ...utils import validate_mesh

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
_ASSETS_DIR = os.path.join(BASE_DIR, "assets")

_EXAMPLE_SCANS = {
    "SCAN_1": "ScanMaoEspastica.stl",
    "SCAN_2": "ScanMaoEspastica_2.stl",
}


def _run_initial_analysis(context):
    
    obj = context.active_object
    if not obj or obj.type != "MESH":
        return
    diag = context.scene.aco_diagnostics
    diag.vertices = len(obj.data.vertices)
    diag.faces = len(obj.data.polygons)
    health = validate_mesh(obj)
    diag.non_manifold_edges = health["non_manifold_edges"]
    diag.loose_vertices = health["loose_vertices"]
    diag.zero_area_faces = health["zero_area_faces"]
    diag.health_valid = health["is_valid"]
    diag.boundary_edges = health["boundary_edges"]
    diag.duplicate_vertices = health["duplicate_vertices"]
    diag.flipped_faces = health["flipped_faces"]
    diag.self_intersecting_faces = health["self_intersecting_faces"]
    diag.health_analyzed = True


class ACO_OT_prepare_environment(bpy.types.Operator):
    bl_idname = "aco.prepare_environment"
    bl_label = "Preparar Ambiente"
    bl_description = "Abre o template de ambiente para cria\u00e7\u00e3o de \u00f3rteses"
    bl_options = {"REGISTER"}

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self)

    def draw(self, context):
        layout = self.layout
        
        layout.label(text="Ferramentas de Ambiente")
        
        layout.operator("wm.call_panel", text="Ir para Câmera", icon='CAMERA_DATA').name = "VIEW3D_PT_view3d_properties"
        layout.operator("wm.call_panel", text="Ajustar Eixos",  icon='CURSOR').name = "VIEW3D_PT_view3d_cursor"

    def execute(self, context):  
        return {"FINISHED"}


class ACO_OT_load_example_scan(bpy.types.Operator):
    bl_idname = "aco.load_example_scan"
    bl_label = "Scan de Exemplo"
    bl_description = "Importa um scan de exemplo dos assets do addon"
    bl_options = {"REGISTER", "UNDO"}

    scan: bpy.props.EnumProperty(
        name="Scan",
        items=(
            ("SCAN_1", "Scan M\u00e3o Esp\u00e1stica", "Primeiro scan de exemplo"),
            ("SCAN_2", "Scan M\u00e3o Esp\u00e1stica 2", "Segundo scan de exemplo"),
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
            self.report({"ERROR"}, f"Scan n\u00e3o encontrado: {scan_path}")
            return {"CANCELLED"}

        bpy.ops.import_mesh.stl(filepath=scan_path)
        _run_initial_analysis(context)
        return {"FINISHED"}


class ACO_OT_import_stl(bpy.types.Operator):
    bl_idname = "aco.import_stl"
    bl_label = "Importar STL"
    bl_description = "Abre o seletor de arquivo para importar um arquivo STL"
    bl_options = {"REGISTER", "UNDO"}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filter_glob: bpy.props.StringProperty(default="*.stl;*.STL", options={"HIDDEN"})

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        if not self.filepath:
            self.report({"ERROR"}, "Nenhum arquivo selecionado.")
            return {"CANCELLED"}

        bpy.ops.import_mesh.stl(filepath=self.filepath)
        _run_initial_analysis(context)
        return {"FINISHED"}
