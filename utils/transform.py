import bpy

from .object import centroid


def align_to_axis(axis: str):
    try:
        obj = bpy.context.active_object
        if not obj or obj.type != 'MESH':
            raise Exception("Objeto ativo invÃ¡lido")

        verts = obj.data.vertices
        if not verts:
            return

        center_world = centroid(verts=verts, matrix_world=obj.matrix_world)

        if axis == "X":
            obj.location.x -= center_world.x
        elif axis == "Y":
            obj.location.y -= center_world.y
        elif axis == "Z":
            obj.location.z -= center_world.z

    except Exception as e:
        print(f"Ocorreu um erro ao alinhar o objeto ao eixo {axis}: {e}")


def reset_rotation_axis(axis: str):
    obj = bpy.context.active_object

    if axis == "X":
        obj.location.x = 0
    elif axis == "Y":
        obj.location.y = 0
    elif axis == "Z":
        obj.location.z = 0


align_active_object_to_axis = align_to_axis
reset_active_object_axis_rotation = reset_rotation_axis
