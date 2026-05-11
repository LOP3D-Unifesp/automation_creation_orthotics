import bpy
from bpy.types import Operator
from ..utils import points_for, change_mode, get_specifics_defs

class ACO_OT_rigging_one(Operator):
    bl_idname = "aco.finger_rigging"
    bl_label = "Gerar único bone"
    bl_option = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        rig = context.scene.aco_rig_hand
        
        return rig.group_to_remove != "NONE"  
    
    
    def execute(self, context):
        layout = context.layout
        
        rig = context.scene.aco_rig_hand
        
        grouped = {}
        
        groups = ["wrist", rig.group_to_remove] if rig.group_to_remove != "forearm" else [rig.group_to_remove]
                        
        
        for key in groups:
            
            list_points = []
            
            for p in points_for(rig, key):
                list_points.append(p.co[:])
            
            grouped[key] = list_points
        
        
        arm_obj = bpy.data.objects["Hand_Rig"]
        arm_data = arm_obj.data
        
        bpy.context.view_layer.objects.active = arm_obj
        change_mode("EDIT")
        
        
        eb        = arm_data.edit_bones
        bone_map  = {}  
     
        
        wrist_co = grouped.get("wrist", [None])[0]
        
        defs = get_specifics_defs(groups)
        
        for key, _, names in defs:
            pts = groups.get(key, [])
            
            
            
        
        
        
        
            
            
            
            
            