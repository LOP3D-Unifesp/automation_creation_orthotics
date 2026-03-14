import bpy

class MessagesPopup(bpy.types.PropertyGroup):
    message: bpy.props.StringProperty(
        name="Message",
        default="Ocorreu um erro ao tentar executar essa a\u00e7\u00e3o!"
    )
    message_info: bpy.props.StringProperty(
        name="Information Message",
        default = "A a\u00e7\u00e3o foi executada com sucesso!"
    )

 

