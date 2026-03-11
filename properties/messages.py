import bpy

class MessagesPopup(bpy.types.PropertyGroup):
    message: bpy.props.StringProperty(
        name="Message",
        default="Ocorreu um erro ao tentar executar essa ação!"
    )
    message_info: bpy.props.StringProperty(
        name="Information Message",
        default = "A ação foi executada com sucesso!"
    )

 
