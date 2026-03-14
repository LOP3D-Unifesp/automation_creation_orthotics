import bpy


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


set_active_mode = change_mode
