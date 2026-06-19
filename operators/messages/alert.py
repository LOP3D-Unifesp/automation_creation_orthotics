import textwrap

import bpy


_POPUP_WIDTH = 420
_WRAP_WIDTH = 58


def _split_and_wrap_message(message, wrap_width=_WRAP_WIDTH):
    text = str(message or "")
    lines = []

    # Preserve explicit line breaks and wrap each logical line.
    for raw_line in text.splitlines() or [""]:
        wrapped = textwrap.wrap(raw_line, width=wrap_width, break_long_words=False, break_on_hyphens=False)
        lines.extend(wrapped or [""])

    return lines


def _draw_message(layout, message, icon):
    box = layout.box()
    lines = _split_and_wrap_message(message)

    if not lines:
        box.label(text="", icon=icon)
        return

    box.label(text=lines[0], icon=icon)
    for line in lines[1:]:
        box.label(text=line)


class ACO_OT_alert_error_popup(bpy.types.Operator):
    bl_idname = "aco.alert_error_popup"
    bl_label = "Aviso importante!"

    message: bpy.props.StringProperty(
        name="Message",
        default="Ocorreu um erro ao tentar executar esta a\u00e7\u00e3o!",
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=_POPUP_WIDTH)

    def draw(self, context):
        _draw_message(self.layout, self.message, "ERROR")

    def execute(self, context):
        self.report({"INFO"}, "Popup de erro fechado.")
        return {"FINISHED"}


class ACO_OT_alert_info_popup(bpy.types.Operator):
    bl_idname = "aco.alert_info_popup"
    bl_label = "Aviso importante!"

    message_info: bpy.props.StringProperty(
        name="Information Message",
        default="A a\u00e7\u00e3o foi executada com sucesso!",
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=_POPUP_WIDTH)

    def draw(self, context):
        _draw_message(self.layout, self.message_info, "INFO")

    def execute(self, context):
        self.report({"INFO"}, "Popup de informa\u00e7\u00e3o fechado.")
        return {"FINISHED"}