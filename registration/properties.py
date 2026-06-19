import bpy

from ..properties import (
    AlignAxisProperties,
    DiagnosticsProperties,
    MeshReductionProperties,
    QuadRemeshProperties,
    RepairProperties,
    AcoRigHand,
    PointMarkers,
    ProcessingTime_State,
)


def register_scene_properties():
    bpy.types.Scene.aco_diagnostics = bpy.props.PointerProperty(type=DiagnosticsProperties)
    bpy.types.Scene.aco_reduction = bpy.props.PointerProperty(type=MeshReductionProperties)
    bpy.types.Scene.aco_quad_remesh = bpy.props.PointerProperty(type=QuadRemeshProperties)
    bpy.types.Scene.aco_repair = bpy.props.PointerProperty(type=RepairProperties)
    bpy.types.Scene.align_limb_props = bpy.props.PointerProperty(type=AlignAxisProperties)
    bpy.types.Scene.aco_rig_hand = bpy.props.PointerProperty(type=AcoRigHand)
    bpy.types.Scene.aco_point_marker = bpy.props.PointerProperty(type=PointMarkers)
    bpy.types.Scene.process_timer = bpy.props.PointerProperty(type=ProcessingTime_State)


def unregister_scene_properties():
    for attribute_name in (
        "align_limb_props",
        "aco_repair",
        "aco_quad_remesh",
        "aco_reduction",
        "aco_diagnostics",
        "aco_rig_hand",
        "aco_point_marker",
    ):
        if hasattr(bpy.types.Scene, attribute_name):
            delattr(bpy.types.Scene, attribute_name)
