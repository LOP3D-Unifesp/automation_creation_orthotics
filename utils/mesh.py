import bpy
from .object import centroid, object_size_by_axis


#def activated_an_object(obj: bpy_prop_collection[Object]):


def get_coordinates_by_range(obj, coordinate: float, axis: str, interval: float = 0.1):
    verts = obj.data.vertices
    if not verts:
        return

    axis_index = {'X': 0, 'Y': 1, 'Z': 2}.get(axis)

    coordinates = []

    co_min = coordinate - interval
    co_max = coordinate + interval

    for v in verts:
        value = v.co[axis_index]
        if co_min <= value <= co_max:
            coordinates.append(v)

    return coordinates


def positions_of_the_bones(axis: str, num_bones: int):
    obj = bpy.context.active_object

    size_object = object_size_by_axis(axis)

    level = size_object["size"] / num_bones
    initial_coordernate = size_object["co_min"]
    positions = []

    positions.append(initial_coordernate)

    for index in range(1, num_bones):
        coordinates = get_coordinates_by_range(obj=obj, coordinate=initial_coordernate, axis=axis)

        center_world = centroid(verts=coordinates, matrix_world=obj.matrix_world)

        positions.append(center_world)
        initial_coordernate += level

    positions.append(size_object["co_max"])

    return positions


def create_new_armature():
    bpy.ops.object.armature_add(enter_editmode=True)

    armature = bpy.context.object

    return armature


def create_first_bone(edit_bones, head_pos, tail_pos):
    from mathutils import Vector

    bone = edit_bones[0]
    bone.name = "Bone 1"
    bone.head = Vector(head_pos)
    bone.tail = Vector(tail_pos)

    return bone


def create_outhers_bones(edit_bones, tail_pos, previous_bone, index=1):
    from mathutils import Vector

    bone = edit_bones.new(f"Bone {index}")
    bone.head = previous_bone.tail
    bone.tail = Vector(tail_pos)
    bone.parent = previous_bone
    bone.use_connect = True

    return bone
