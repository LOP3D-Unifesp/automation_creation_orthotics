bl_info = {
    "name": "Orthosis Creation Automation",
    "author": "Tamires Morais Rodrigues - LO&P 3D",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Tools",
    "description": "Automatizar o processo de criação de Órteses",
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
    bpy.types.Scene.align_limb_props = bpy.props.PointerProperty(type=AlignAxisProperties)


def _unregister_scene_properties():
    for attribute_name in ("align_limb_props", "faces", "vertices"):
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