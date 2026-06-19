import bpy
from ...utils import object_has_to_be_activated, validate_mesh, build_reduction_stack, mesh_volume, warn_mesh_health

class ACO_OT_apply_quad_remesh(bpy.types.Operator):
    bl_idname = "aco.apply_quad_remesh"
    bl_label = "Aplicar Quad Remesh"
    bl_options = {"REGISTER", "UNDO"}

    @object_has_to_be_activated
    def execute(self, context):
        scene = context.scene
        obj = context.active_object
        qr = scene.aco_quad_remesh
        diag = scene.aco_diagnostics

        warn_mesh_health(self, obj)

        volume_before_valid, volume_before = mesh_volume(obj.data)
        
        bpy.ops.aco.processing_time_start("EXEC_DEFAULT",
                name_task="Quad Remesher")

        try:
            modifier = obj.modifiers.new(name="QuadRemeshPreview", type="REMESH")
            modifier.mode = "VOXEL"
            modifier.voxel_size = qr.voxel_size
            modifier.use_smooth_shade = qr.smooth_shade

            bpy.ops.object.modifier_apply(modifier=modifier.name)

            diag.vertices = len(obj.data.vertices)
            diag.faces = len(obj.data.polygons)

            health = validate_mesh(obj)
            diag.non_manifold_edges = health["non_manifold_edges"]
            diag.loose_vertices = health["loose_vertices"]
            diag.zero_area_faces = health["zero_area_faces"]
            diag.health_valid = health["is_valid"]
            diag.boundary_edges = health["boundary_edges"]
            diag.duplicate_vertices = health["duplicate_vertices"]
            diag.flipped_faces = health["flipped_faces"]
            diag.self_intersecting_faces = health["self_intersecting_faces"]
            diag.health_analyzed = True

            volume_after_valid, volume_after = mesh_volume(obj.data)
            volume_valid = volume_before_valid and volume_after_valid and volume_before > 0

            qr.volume_before = volume_before if volume_before_valid else 0.0
            qr.volume_after = volume_after if volume_after_valid else 0.0
            qr.volume_valid = volume_valid

            if volume_valid:
                change_percent = ((volume_after - volume_before) / volume_before) * 100.0
                qr.volume_change_percent = change_percent

                self.report(
                    {"INFO"},
                    (
                        f"Remesh aplicado (voxel {qr.voxel_size:.3f}, "
                        f"suaviza\u00e7\u00e3o {'ligada' if qr.smooth_shade else 'desligada'}). "
                        f"Volume: {volume_before:.4f} -> {volume_after:.4f} BU\u00b3 ({change_percent:+.2f}%)."
                    ),
                )
            else:
                qr.volume_change_percent = 0.0
                self.report(
                    {"INFO"},
                    (
                        f"Remesh aplicado (voxel {qr.voxel_size:.3f}, "
                        f"suaviza\u00e7\u00e3o {'ligada' if qr.smooth_shade else 'desligada'}). "
                        "Volume indispon\u00edvel para esta malha."
                    ),
                )
            
            bpy.ops.aco.processing_time_stop('EXEC_DEFAULT')

            return {"FINISHED"}
        
        except Exception as e:
            
            bpy.ops.aco.alert_error_popup("INVOKE_DEFAULT", message=str(e))
            return {"CANCELLED"}
