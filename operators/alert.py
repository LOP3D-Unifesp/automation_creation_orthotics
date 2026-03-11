import bpy 



class ACO_OT_alert_error_popup(bpy.types.Operator):
    bl_idname = "aco.alert_error_popup"
    bl_label = "Aviso importante!"

    message: bpy.props.StringProperty(
        name="Message",
        default="Ocorreu um erro ao tentar executar essa ação!"
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text=self.message, icon='ERROR')

    def execute(self, context):
        self.report({'INFO'}, "Popup de Erro fechado.")
        return {'FINISHED'}




class ACO_OT_alert_info_popup(bpy.types.Operator):
    bl_idname = "aco.alert_info_popup"
    bl_label = "Aviso importante!"

    message_info: bpy.props.StringProperty(
        name="Information Message",
        default = "A ação foi executada com sucesso!"
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text=self.message_info, icon="INFO")

    def execute(self, context):
        self.report({'INFO'}, "Popup de Info Fechado.")
        return {'FINISHED'}
    
