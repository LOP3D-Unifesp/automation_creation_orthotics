import bpy
from .mesh import get_defs, points_for


def activate_object(obj):
    try:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
    except Exception as e:
        print(f"Ocorreu um erro ao tentar ativar um objeto: {e}")


def create_parent_deform(armature):
    mesh = [obj for obj in bpy.data.objects if obj.type == 'MESH'][0]

    if mesh and mesh.type != "MESH":
        raise ValueError("O objeto deve ser do tipo Mesh para associar \u00e0 armature. ")

    mesh.select_set(True)
    armature.select_set(True)
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')



def change_mode(mode: str):
    obj = bpy.context.active_object
    if not obj:
        return

    bpy.ops.object.mode_set(mode=mode)
    
    

def is_ready_to_generate(rig) -> bool:

    defs = get_defs()

    wrist_def = next((d for d in defs if d[0] == "wrist"), None)
    if not wrist_def:
        return False

    wrist_completo = len(points_for(rig, "wrist")) >= len(wrist_def[2])
    if not wrist_completo:
        return False

    fingers = [d for d in defs if d[0] not in [ "wrist", "forearm"]]
    algum_dedo_completo = any(
        len(points_for(rig, key)) >= len(names)
        for key, _, names in fingers
    )

    return algum_dedo_completo






set_active_mode = change_mode
