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

from .registration import *
from .properties import FINGER_DEFS, NEXT_POINT_LABELS



def register():
    register_classes()    


def unregister():
    unregister_classes()
    


if __name__ == "__main__":
    register()
