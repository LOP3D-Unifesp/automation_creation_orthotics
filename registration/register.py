import bpy

from .classes import CLASSES
from .properties import register_scene_properties, unregister_scene_properties


def register_classes():
    for cls in CLASSES:
        try:
            bpy.utils.register_class(cls)
        except Exception as e:
            print(f"ERRO AO REGISTRAR: {cls}")
            print(e)
            raise

    register_scene_properties()

def unregister_classes():
    unregister_scene_properties()

    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)