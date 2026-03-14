bl_info = {
    "name": "Orthosis Creation Automation",
    "author": "Tamires Morais Rodrigues - LO&P 3D",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Tools",
    "description": "Automatizar o processo de cria\u00e7\u00e3o de \u00d3rteses",
    "category": "Mesh",
}

import bpy

from .operators import CLASSES as OPERATOR_CLASSES
from .panels import CLASSES as PANEL_CLASSES
from .properties import AlignAxisProperties, CLASSES as PROPERTY_CLASSES

CLASSES = PROPERTY_CLASSES + OPERATOR_CLASSES + PANEL_CLASSES


def _register_scene_properties():
    bpy.types.Scene.vertices = bpy.props.IntProperty(default=0)
    bpy.types.Scene.faces = bpy.props.IntProperty(default=0)

    # Legacy/internal field kept for operator compatibility.
    bpy.types.Scene.decimate_collapse_ratio = bpy.props.FloatProperty(
        name="Collapse Ratio",
        description="Propor\u00e7\u00e3o de faces para manter no modo Collapse",
        default=0.5,
        min=0.0,
        max=1.0,
    )

    # User-facing field: reduction percentage (90 => reduce 90%).
    bpy.types.Scene.decimate_collapse_reduction_percent = bpy.props.IntProperty(
        name="Redu\u00e7\u00e3o (%)",
        description="Percentual de redu\u00e7\u00e3o da malha no modo Decima\u00e7\u00e3o",
        default=50,
        min=0,
        max=99,
        subtype="PERCENTAGE",
    )

    bpy.types.Scene.decimate_unsubdivide_iterations = bpy.props.IntProperty(
        name="Un-Subdivide Iterations",
        description="Quantidade de itera\u00e7\u00f5es no modo Un-Subdivide",
        default=1,
        min=1,
        max=100,
    )

    bpy.types.Scene.decimate_planar_angle = bpy.props.IntProperty(
        name="Planar Angle",
        description="\u00c2ngulo em graus usado na decima\u00e7\u00e3o Planar",
        default=10,
        min=0,
        max=180,
    )

    bpy.types.Scene.show_prepare_advanced = bpy.props.BoolProperty(
        name="Mostrar redu\u00e7\u00e3o da malha",
        description="Exibe as opera\u00e7\u00f5es manuais de redu\u00e7\u00e3o da malha",
        default=False,
    )

    bpy.types.Scene.reduction_use_collapse = bpy.props.BoolProperty(
        name="Aplicar Decima\u00e7\u00e3o",
        description="Inclui Decima\u00e7\u00e3o no clique \u00fanico de redu\u00e7\u00e3o",
        default=True,
    )

    bpy.types.Scene.reduction_use_unsubdivide = bpy.props.BoolProperty(
        name="Aplicar Un-Subdivide",
        description="Inclui Un-Subdivide no clique \u00fanico de redu\u00e7\u00e3o",
        default=True,
    )

    bpy.types.Scene.reduction_use_planar = bpy.props.BoolProperty(
        name="Aplicar Planar",
        description="Inclui Planar no clique \u00fanico de redu\u00e7\u00e3o",
        default=True,
    )

    bpy.types.Scene.mesh_reduction_volume_before = bpy.props.FloatProperty(
        name="Volume Antes (Reducao)",
        description="Volume antes do pipeline de redu\u00e7\u00e3o da malha (BU^3)",
        default=0.0,
        precision=4,
    )

    bpy.types.Scene.mesh_reduction_volume_after = bpy.props.FloatProperty(
        name="Volume Depois (Reducao)",
        description="Volume depois do pipeline de redu\u00e7\u00e3o da malha (BU^3)",
        default=0.0,
        precision=4,
    )

    bpy.types.Scene.mesh_reduction_volume_change_percent = bpy.props.FloatProperty(
        name="Variacao de Volume Reducao (%)",
        description="Varia\u00e7\u00e3o percentual de volume no pipeline de redu\u00e7\u00e3o",
        default=0.0,
        precision=3,
    )

    bpy.types.Scene.mesh_reduction_volume_valid = bpy.props.BoolProperty(
        name="Volume Reducao Valido",
        description="Indica se o volume antes/depois da redu\u00e7\u00e3o \u00e9 confi\u00e1vel",
        default=False,
    )

    bpy.types.Scene.show_quad_remesh_options = bpy.props.BoolProperty(
        name="Mostrar Quad Remesh",
        description="Exibe as configura\u00e7\u00f5es opcionais de Quad Remesh",
        default=False,
    )

    bpy.types.Scene.quad_remesh_voxel_size = bpy.props.FloatProperty(
        name="Voxel Size",
        description="Tamanho do voxel usado no remesh opcional",
        default=2.0,
        min=0.01,
        soft_max=10.0,
        precision=3,
    )

    bpy.types.Scene.quad_remesh_smooth_shade = bpy.props.BoolProperty(
        name="Suavizar",
        description="Aplica smooth shading ap\u00f3s o remesh",
        default=True,
    )

    bpy.types.Scene.quad_remesh_volume_before = bpy.props.FloatProperty(
        name="Volume Antes",
        description="Volume antes de aplicar Quad Remesh (BU^3)",
        default=0.0,
        precision=4,
    )

    bpy.types.Scene.quad_remesh_volume_after = bpy.props.FloatProperty(
        name="Volume Depois",
        description="Volume depois de aplicar Quad Remesh (BU^3)",
        default=0.0,
        precision=4,
    )

    bpy.types.Scene.quad_remesh_volume_change_percent = bpy.props.FloatProperty(
        name="Variacao de Volume (%)",
        description="Varia\u00e7\u00e3o percentual de volume ap\u00f3s Quad Remesh",
        default=0.0,
        precision=3,
    )

    bpy.types.Scene.quad_remesh_volume_valid = bpy.props.BoolProperty(
        name="Volume Valido",
        description="Indica se o volume antes/depois do Quad Remesh \u00e9 confi\u00e1vel",
        default=False,
    )

    bpy.types.Scene.align_limb_props = bpy.props.PointerProperty(type=AlignAxisProperties)


def _unregister_scene_properties():
    for attribute_name in (
        "align_limb_props",
        "quad_remesh_volume_valid",
        "quad_remesh_volume_change_percent",
        "quad_remesh_volume_after",
        "quad_remesh_volume_before",
        "quad_remesh_smooth_shade",
        "quad_remesh_voxel_size",
        "show_quad_remesh_options",
        "mesh_reduction_volume_valid",
        "mesh_reduction_volume_change_percent",
        "mesh_reduction_volume_after",
        "mesh_reduction_volume_before",
        "reduction_use_planar",
        "reduction_use_unsubdivide",
        "reduction_use_collapse",
        "show_prepare_advanced",
        "decimate_planar_angle",
        "decimate_unsubdivide_iterations",
        "decimate_collapse_reduction_percent",
        "decimate_collapse_ratio",
        "faces",
        "vertices",
    ):
        if hasattr(bpy.types.Scene, attribute_name):
            delattr(bpy.types.Scene, attribute_name)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)

    _register_scene_properties()


def unregister():
    _unregister_scene_properties()

    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
