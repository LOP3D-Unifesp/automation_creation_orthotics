import bpy
import bmesh
from ...utils import validate_mesh, mesh_volume


class ACO_OT_repair_mesh(bpy.types.Operator):
    bl_idname = "aco.repair_mesh"
    bl_label = "Reparar malha"
    bl_description = "Funde vértices sobrepostos e fecha buracos da malha"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        
        bpy.ops.aco.processing_time_start("EXEC_DEFAULT",
                name_task="Mesh Repair")

        if not obj or obj.type != "MESH":
            self.report({"ERROR"}, "Selecione um objeto do tipo Mesh.")
            return {"CANCELLED"}

        if obj.mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")

        try:
            # Captura estado inicial
            verts_before = len(obj.data.vertices)
            faces_before = len(obj.data.polygons)
            vol_valid_before, volume_before = mesh_volume(obj.data)

            # Operações de reparo
            """ bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_all(action="SELECT")
            bpy.ops.mesh.remove_doubles(threshold=0.001)
            bpy.ops.mesh.fill_holes(sides=0)
            bpy.ops.object.mode_set(mode="OBJECT")  """
            
            # Cria uma cópia dos dados da malha para o BMesh
            me = obj.data
            bm = bmesh.new()
            bm.from_mesh(me)

            # Remove vértices duplicados baseados em uma distância mínima
            bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)

            # Recalcula normais
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

            # Remove vértices isolados
            cleanup_verts = [v for v in bm.verts if not v.link_edges]
            bmesh.ops.delete(bm, geom=cleanup_verts, context='VERTS')

            # Escreve de volta as alterações para a malha original
            bm.to_mesh(me)
            me.update()
            bm.free()

            # Captura estado final
            verts_after = len(obj.data.vertices)
            faces_after = len(obj.data.polygons)
            
            vol_valid_after, volume_after = mesh_volume(obj.data)

            # Atualiza diagnósticos
            diag = context.scene.aco_diagnostics
            diag.vertices = verts_after
            diag.faces = faces_after

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

            # Atualiza dados de volume e progresso
            repair = context.scene.aco_repair
            volume_valid = vol_valid_before and vol_valid_after and volume_before > 0
            repair.volume_before = volume_before if vol_valid_before else 0.0
            repair.volume_after = volume_after if vol_valid_after else 0.0
            repair.volume_valid = volume_valid
            
            repair.volume_change_percent = (
                (volume_after - volume_before) / volume_before * 100.0
                if volume_valid else 0.0
            )
            repair.progress = 1.0

            self.report(
                {"INFO"},
                f"Reparo: {verts_before - verts_after} vértices fundidos, "
                f"{faces_after - faces_before} faces adicionadas.",
            )
            
        except Exception as exc:
            if obj.mode != "OBJECT":
                bpy.ops.object.mode_set(mode="OBJECT")
            self.report({"ERROR"}, f"Erro durante reparo: {exc}")
            return {"CANCELLED"}
        
        bpy.ops.aco.processing_time_stop('EXEC_DEFAULT')

        return {"FINISHED"}