import bpy
import bmesh
from bpy.types import Operator
from ...utils import get_specifics_defs, points_for, expected


class ACO_OT_create_bone_score_markers(Operator):
    bl_idname = "aco.create_bone_score_markers"
    bl_label = "Marcadores de pontos dos bones"
    bl_description = "Indicadores de localização dos bones"
  
    def execute(self, context):
        rig = context.scene.aco_rig_hand
        
        point_markers = context.scene.aco_point_marker.markers

        finger_info_list = get_specifics_defs(rig.active_finger)
        points = points_for(rig, rig.active_finger)

        if not finger_info_list or not points:
            return {'CANCELLED'}

        finger_info = finger_info_list[0]
        
        names = finger_info[2]
        
        name = names[len(points) - 1]
               
        marker = point_markers.add()
        marker.name = f"Marker_{name}"
        marker.point_world = rig.joint_points[-1].co
        marker.radius = 2.5
        
        mesh = bpy.data.meshes.new(marker.name + "_Mesh") 
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=marker.radius)
        bm.to_mesh(mesh)
        bm.free()

        # Criar o objeto com o nome do marker
        obj = bpy.data.objects.new(marker.name, mesh)
        
        # Linkar o objeto à coleção da cena para que ele seja visível
        bpy.context.collection.objects.link(obj)

        obj.location = marker.point_world

        #bpy.ops.mesh.primitive_uv_sphere_add(radius=marker.radius, location=marker.point_world)
        
        
        return {"FINISHED"}



class ACO_OT_delete_bone_score_markers(Operator):
    bl_idname = "aco.delete_bone_score_markers"
    bl_label = "Deletar marcadores de pontos dos bones"
    bl_description = "Deletar os indicadores de localização dos bones"
  
    def execute(self, context):
        point_markers = context.scene.aco_point_marker.markers
        
        for marker in point_markers:
            obj = bpy.data.objects.get(marker.name)
            if obj:
                bpy.data.objects.remove(obj, do_unlink=True)

        point_markers.clear()
        
        return {"FINISHED"}
    

    
class ACO_OT_delete_one_score_markers(Operator):
    bl_idname  = "aco.delete_one_score_markers"
    bl_label   = "Deleta o último marcador de ponto"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        point_markers = context.scene.aco_point_marker.markers
        
        if point_markers:
            last_marker = point_markers[-1]
            obj = bpy.data.objects.get(last_marker.name)
            if obj:
                bpy.data.objects.remove(obj, do_unlink=True)
            point_markers.remove(len(point_markers) - 1)
        
        return {"FINISHED"}
        
        
        
        
        
        
        
        
        
        
        
    
    
    