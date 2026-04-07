import bpy
from ..utils import activate_object, align_to_axis, change_mode, reset_rotation_axis, object_has_to_be_activated


def _frame_active_object_in_viewports(context):
    # Best effort: frame selected object in available VIEW_3D areas.
    for window in context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type != "VIEW_3D":
                continue
            for region in area.regions:
                if region.type != "WINDOW":
                    continue
                try:
                    with context.temp_override(window=window, screen=screen, area=area, region=region):
                        bpy.ops.view3d.view_selected(use_all_regions=False)
                except Exception:
                    pass


class ACO_OT_align_limb_axis(bpy.types.Operator):
    bl_idname = "aco.align_limb_axis"
    bl_label = "Alinhar membro no eixo"
    bl_options = {"REGISTER", "UNDO"}

    show_feedback: bpy.props.BoolProperty(default=True, options={"SKIP_SAVE"})
    force_all_axes: bpy.props.BoolProperty(default=False, options={"SKIP_SAVE"})

    @staticmethod
    def _selected_axes(scene, force_all_axes=False):
        if force_all_axes:
            return ["X", "Y", "Z"]

        props = scene.align_limb_props
        axes = []
        if getattr(props, "axis_x", False):
            axes.append("X")
        if getattr(props, "axis_y", False):
            axes.append("Y")
        if getattr(props, "axis_z", False):
            axes.append("Z")
        return axes

    @object_has_to_be_activated
    def execute(self, context):
        scene = context.scene
        selected_axes = self._selected_axes(scene, force_all_axes=self.force_all_axes)

        if not selected_axes:
            bpy.ops.aco.alert_error_popup("INVOKE_DEFAULT", message="Selecione pelo menos um eixo para alinhar.")
            return {"CANCELLED"}

        obj = context.active_object

        try:
            activate_object(obj)

            change_mode("OBJECT")
            change_mode("EDIT")

            for axis in selected_axes:
                align_to_axis(axis=axis)

            change_mode("OBJECT")

            bpy.ops.object.origin_set(type="ORIGIN_CENTER_OF_MASS", center="MEDIAN")

            for axis in selected_axes:
                reset_rotation_axis(axis)

            _frame_active_object_in_viewports(context)

            if self.show_feedback:
                axes_text = ", ".join(selected_axes)
                self.report({"INFO"}, f"Alinhado aos eixos: {axes_text}.")

        except Exception as e:
            bpy.ops.aco.alert_error_popup("INVOKE_DEFAULT", message=str(e))

        return {"FINISHED"}
