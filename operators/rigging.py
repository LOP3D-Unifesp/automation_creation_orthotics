import bpy
from ..utils.decorator import object_has_to_be_activated
from ..utils.mesh import positions_of_the_bones
from ..utils.object import create_bones_with_position
from ..utils.selection import change_mode, create_parent_deform

class ACO_OT_creation_bones(bpy.types.Operator):
    bl_idname = "aco.creation_bones"
    bl_label = "CriaÃ§Ã£o de Bones"

    @object_has_to_be_activated
    def execute(self, context):
        scene = context.scene

        axis = scene.align_limb_props.axis
        number_bones = scene.number_bones

        try:
            positions = positions_of_the_bones(axis=axis, num_bones=number_bones)

            armature = create_bones_with_position(positions=positions)

            bpy.context.view_layer.objects.active = armature

            change_mode('OBJECT')

            create_parent_deform(armature=armature)

            change_mode('POSE')

        except Exception as e:
            bpy.ops.aco.alert_error_popup('INVOKE_DEFAULT', message=e)

        return {'FINISHED'}




