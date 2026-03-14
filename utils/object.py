import bpy

from .ui import activated_an_object
from .ui import chance_for_mode


def decimate_by_type(decimate_type: str, parameter):
    activated_an_object()
    chance_for_mode("OBJECT")

    obj = bpy.context.view_layer.objects.active
    mod = obj.modifiers.new(name="Decimate", type='DECIMATE')
    mod.decimate_type = decimate_type

    if decimate_type == 'COLLAPSE':
        mod.ratio = parameter
        mod.use_collapse_triangulate = True
    elif decimate_type == 'DISSOLVE':
        import math

        mod.angle_limit = math.radians(parameter)
        mod.use_dissolve_boundaries = False
    elif decimate_type == 'UNSUBDIV':
        mod.iterations = parameter

    bpy.ops.object.modifier_apply(modifier=mod.name)


def centroid(verts, matrix_world):
    import mathutils

    sum_coords = [0.0, 0.0, 0.0]
    for v in verts:
        sum_coords[0] += v.co.x
        sum_coords[1] += v.co.y
        sum_coords[2] += v.co.z

    center_local = []
    for coordinate in sum_coords:
        center_local.append(coordinate / len(verts))

    center_world = matrix_world @ mathutils.Vector(center_local)

    print(f"O centr\u00f3ide \u00e9: {center_world}")

    return center_world


def object_size_by_axis(axis: str):
    obj = bpy.context.active_object

    verts = obj.data.vertices
    if not verts:
        return

    axis_index = {'X': 0, 'Y': 1, 'Z': 2}.get(axis)

    first_value = verts[0].co[axis_index]
    coordinate_min = first_value
    coordinate_max = first_value

    for v in verts[1:]:
        value = v.co[axis_index]
        if value < coordinate_min:
            coordinate_min = value
        elif value > coordinate_max:
            coordinate_max = value

    return {'co_max': coordinate_max, 'co_min': coordinate_min, 'size': coordinate_max - coordinate_min}


def create_bones_with_position(positions: list[int] = []):
    from .mesh import create_first_bone, create_new_armature, create_outhers_bones

    armature = create_new_armature()
    edit_bones = armature.data.edit_bones
    bone = create_first_bone(edit_bones=edit_bones, head_pos=positions[1], tail_pos=positions[0])

    size = len(positions) - 1

    for index in range(2, size):
        bone = create_outhers_bones(edit_bones=edit_bones, tail_pos=positions[index], previous_bone=bone, index=index)

    return armature
