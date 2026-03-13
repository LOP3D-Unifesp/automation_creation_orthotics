import bpy

def object_has_to_be_activated(func):
    def wrapper(self, context, *args, **kwargs):
        object = context.active_object

        if not object or object.type != 'MESH':
            bpy.ops.aco.alert_error_popup('INVOKE_DEFAULT', message="Nenhum objeto selecionado.\nSelecione um objeto do tipo Mesh na cena.")
            return {'CANCELLED'}
        
        if object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        return func(self, context, *args, **kwargs)

    return wrapper
