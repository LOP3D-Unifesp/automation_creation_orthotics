import math
import bmesh
import bpy

from .object import centroid


def align_to_axis(axis: str):
    try:
        obj = bpy.context.active_object
        if not obj or obj.type != 'MESH':
            raise Exception("Objeto ativo inv\u00e1lido")

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


def build_reduction_stack(obj, reduction):

    step_labels = []
    modifier_names = []

    if reduction.use_collapse:
        collapse = obj.modifiers.new(name="ACO_Reduce_Collapse", type="DECIMATE")
        collapse.decimate_type = "COLLAPSE"
        ratio = 1.0 - (max(0, min(99, reduction.collapse_percent)) / 100.0)
        ratio = max(0.03, min(1.0, ratio))
        collapse.ratio = ratio
        collapse.use_collapse_triangulate = True
        reduction.collapse_ratio = ratio
        step_labels.append("Decima\u00e7\u00e3o")
        modifier_names.append(collapse.name)

    if reduction.use_unsubdivide:
        unsubdivide = obj.modifiers.new(name="ACO_Reduce_Unsubdivide", type="DECIMATE")
        unsubdivide.decimate_type = "UNSUBDIV"
        unsubdivide.iterations = max(1, min(100, reduction.unsubdiv_iterations))
        step_labels.append("Un-Subdivide")
        modifier_names.append(unsubdivide.name)

    if reduction.use_planar:
        planar = obj.modifiers.new(name="ACO_Reduce_Planar", type="DECIMATE")
        planar.decimate_type = "DISSOLVE"
        planar.angle_limit = math.radians(max(0, min(180, reduction.planar_angle)))
        planar.use_dissolve_boundaries = False
        step_labels.append("Planar")
        modifier_names.append(planar.name)

    return step_labels, modifier_names

def mesh_volume(mesh):
    if not mesh:
        return False, 0.0

    bm = bmesh.new()
    try:
        bm.from_mesh(mesh)
        if len(bm.faces) == 0:
            return False, 0.0

        # signed=False returns absolute volume for stable comparison.
        volume = bm.calc_volume(signed=False)
        if volume <= 0:
            return False, 0.0

        return True, float(volume)
    except Exception:
        return False, 0.0
    finally:
        bm.free()

align_active_object_to_axis = align_to_axis
reset_active_object_axis_rotation = reset_rotation_axis
