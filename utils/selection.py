import bpy


def activate_object(obj):
    try:
        # Limpa seleção atual
        bpy.ops.object.select_all(action='DESELECT')

        # Seleciona o objeto
        obj.select_set(True)

        # Define como ativo
        bpy.context.view_layer.objects.active = obj

    except Exception as e:
        print(f"Ocorreu um erro ao tentar ativar um objeto: {e}")


def create_parent_deform(armature):
    
    mesh = [obj for obj in bpy.data.objects if obj.type == 'MESH'][0]

    if mesh and mesh.type != "MESH":
        raise ValueError("O objeto deve ser do tipo Mesh para associar à armature. ")
    
    mesh.select_set(True)
    armature.select_set(True)
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')



def change_mode(mode: str):
    obj = bpy.context.active_object
    if not obj:
        return

    bpy.ops.object.mode_set(mode=mode)



####ENTRAR NO MODO EDIÇÃO ARMATURE