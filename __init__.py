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
from .properties import (
    AlignAxisProperties,
    DiagnosticsProperties,
    MeshReductionProperties,
    QuadRemeshProperties,
    RepairProperties,
    AcoRigHand,
    FINGER_DEFS,
    NEXT_POINT_LABELS, 
    CLASSES as PROPERTY_CLASSES,
)


CLASSES = PROPERTY_CLASSES + OPERATOR_CLASSES + PANEL_CLASSES 


def _register_scene_properties():
    bpy.types.Scene.aco_diagnostics = bpy.props.PointerProperty(type=DiagnosticsProperties)
    bpy.types.Scene.aco_reduction = bpy.props.PointerProperty(type=MeshReductionProperties)
    bpy.types.Scene.aco_quad_remesh = bpy.props.PointerProperty(type=QuadRemeshProperties)
    bpy.types.Scene.aco_repair = bpy.props.PointerProperty(type=RepairProperties)
    bpy.types.Scene.align_limb_props = bpy.props.PointerProperty(type=AlignAxisProperties)
    bpy.types.Scene.aco_rig_hand = bpy.props.PointerProperty(type=AcoRigHand)

def _unregister_scene_properties():
    for attribute_name in (
        "align_limb_props",
        "aco_repair",
        "aco_quad_remesh",
        "aco_reduction",
        "aco_diagnostics",
        "aco_rig_hand",
    ):
        if hasattr(bpy.types.Scene, attribute_name):
            delattr(bpy.types.Scene, attribute_name)


def register():
    for cls in CLASSES:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            try:
                bpy.utils.unregister_class(cls)
            except RuntimeError:
                pass
            bpy.utils.register_class(cls)

    _register_scene_properties()


def unregister():
    _unregister_scene_properties()

    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
