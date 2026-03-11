import bpy


def remove_depsgraph():
    try:
        bpy.app.handlers.depsgraph_update_post.remove(detect_import)
    except ValueError:
        pass


def detect_import(depsgraph):
    print("Mudança detectada no depsgraph.")

    limbs = bpy.data.objects
    
    #Verifica se existe apenas um objeto e irá ativa-lo
    if len(limbs) == 1:
        activated_an_object(limbs[0])
        
    else:
        #Caso tenha mais que um objeto, o usuário deve selecionar o que deseja fazer alterações para EDIT MODE
        pass


    for obj in bpy.data.objects:
        print(obj.name, obj.type, obj.location)

    remove_depsgraph()
   

def is_scene_empty(geometry_types: dict):
    return not any(obj.type in geometry_types for obj in bpy.context.scene.objects)


def add_handler_depsgraph(geometry_types: dict):        
    # Evita adicionar o mesmo handler várias vezes
    if detect_import not in bpy.app.handlers.depsgraph_update_post and is_scene_empty(geometry_types):
        bpy.app.handlers.depsgraph_update_post.append(detect_import)


def activated_an_object():

    obj = bpy.context.view_layer.objects.active

    # Já existe objeto ativo
    if obj is not None:
        return

    objs = list(bpy.context.scene.objects)

    # Nenhum objeto
    if len(objs) == 0:
        raise Exception("Nenhum objeto encontrado na cena.")

    # Mais de um objeto
    if len(objs) > 1:
        raise Exception(
            "Há mais de um objeto na cena. "
            "Ative apenas um objeto para continuar.\n"
            "Vá para o Object Mode e clique no objeto desejado."
        )


    single_obj = objs[0]

    # Limpa seleção
    bpy.ops.object.select_all(action='DESELECT')

    # Seleciona e ativa
    single_obj.select_set(True)
    bpy.context.view_layer.objects.active = single_obj


  


def chance_for_mode(mode: str):
    # Troca o modo ativo do objeto selecionado
    bpy.ops.object.mode_set(mode=mode)



