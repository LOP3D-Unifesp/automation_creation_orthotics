bl_info = {
    "name":"Orthosis Creation Automation",
    "author":"Tamires Morais Rodrigues - LO&P 3D",
    "version":(1, 0, 0),
    "blender":(3, 0, 0),
    "location":"View3D > Tools",
    "description":"Automatizar o processo de criação de Órteses",
    "category":"Mesh"
}

import bpy
from .properties import AlignAxisProperties
from .operators import ACO_OT_align_limb_axis, ACO_OT_decimate_un_subdivide, ACO_OT_decimate_collapse, ACO_OT_decimate_planar, ACO_OT_alert_error_popup, ACO_OT_alert_info_popup, ACO_OT_number_of_vertices_and_faces
from .panels import ACO_PT_OrthosisAutomation


GEOMETRY_TYPES = {'MESH', 'CURVE', 'SURFACE'}


def register():

    bpy.utils.register_class(AlignAxisProperties)

    bpy.utils.register_class(ACO_OT_alert_error_popup)
    bpy.utils.register_class(ACO_OT_alert_info_popup)
    bpy.utils.register_class(ACO_OT_align_limb_axis)
    bpy.utils.register_class(ACO_OT_decimate_un_subdivide)
    bpy.utils.register_class(ACO_OT_decimate_planar)
    bpy.utils.register_class(ACO_OT_decimate_collapse)
    bpy.utils.register_class(ACO_OT_number_of_vertices_and_faces)

    bpy.utils.register_class(ACO_PT_OrthosisAutomation)

    bpy.types.Scene.vertices = bpy.props.IntProperty(default=0)
    bpy.types.Scene.faces = bpy.props.IntProperty(default=0)
    bpy.types.Scene.align_limb_props = bpy.props.PointerProperty(type=AlignAxisProperties)


    #PENSAR EM UM MECANISMO PARA SEMPRE ATIVAR O OBJETO ANTES DE QUALQUER AÇÃO


    #add_handler_depsgraph(geometry_types=GEOMETRY_TYPES)

    #obj = bpy.context.active_object

    #chance_for_mode("EDIT")

    #Preencher lacunas
    #fill_in_the_blanks(obj)


    #chance_for_mode("OBJECT")
    


def unregister():

    del bpy.types.Scene.vertices
    del bpy.types.Scene.faces
    del bpy.types.Scene.align_limb_props
    
    bpy.utils.unregister_class(ACO_PT_OrthosisAutomation)
    bpy.utils.unregister_class(ACO_OT_number_of_vertices_and_faces)
    bpy.utils.unregister_class(ACO_OT_decimate_collapse)
    bpy.utils.unregister_class(ACO_OT_decimate_planar)
    bpy.utils.unregister_class(ACO_OT_decimate_un_subdivide)
    bpy.utils.unregister_class(ACO_OT_align_limb_axis)
    bpy.utils.unregister_class(ACO_OT_alert_info_popup)
    bpy.utils.unregister_class(ACO_OT_alert_error_popup)

    bpy.utils.unregister_class(AlignAxisProperties)


if __name__ == "__main__":
    register()
