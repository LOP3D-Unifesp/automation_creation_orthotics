import bpy

from ..utils import validate_mesh
from .reduction_tools import _mesh_volume_bu3


class ACO_OT_repair_mesh(bpy.types.Operator):
    bl_idname = "aco.repair_mesh"
    bl_label = "Reparar malha"
    bl_description = "Funde v\u00e9rtices sobrepostos e fecha buracos da malha"
    bl_options = {"REGISTER", "UNDO"}

    _timer = None
    _step = 0
    _verts_before = 0
    _faces_before = 0
    _volume_before = 0.0
    _volume_before_valid = False

    def invoke(self, context, event):
        obj = context.active_object
        if not obj or obj.type != "MESH":
            bpy.ops.aco.alert_error_popup(
                "INVOKE_DEFAULT",
                message="Nenhum objeto selecionado.\nSelecione um objeto do tipo Mesh na cena.",
            )
            return {"CANCELLED"}
        if obj.mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")

        repair = context.scene.aco_repair
        repair.progress = 0.0
        self._step = 0
        self._verts_before = 0
        self._faces_before = 0
        self._volume_before = 0.0
        self._volume_before_valid = False

        self._timer = context.window_manager.event_timer_add(0.05, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        if event.type != "TIMER":
            return {"RUNNING_MODAL"}

        repair = context.scene.aco_repair
        obj = context.active_object

        if not obj or obj.type != "MESH":
            context.window_manager.event_timer_remove(self._timer)
            self._timer = None
            self.report({"ERROR"}, "Objeto inv\u00e1lido durante reparo.")
            return {"CANCELLED"}

        try:
            if self._step == 0:
                self._verts_before = len(obj.data.vertices)
                self._faces_before = len(obj.data.polygons)
                self._volume_before_valid, self._volume_before = _mesh_volume_bu3(obj.data)
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.ops.mesh.select_all(action="SELECT")
                repair.progress = 0.10

            elif self._step == 1:
                bpy.ops.mesh.remove_doubles(threshold=0.001)
                repair.progress = 0.40

            elif self._step == 2:
                bpy.ops.mesh.fill_holes(sides=0)
                repair.progress = 0.65

            elif self._step == 3:
                bpy.ops.object.mode_set(mode="OBJECT")
                repair.progress = 0.80

            elif self._step == 4:
                after_valid, volume_after = _mesh_volume_bu3(obj.data)
                verts_after = len(obj.data.vertices)
                faces_after = len(obj.data.polygons)
                verts_merged = self._verts_before - verts_after
                faces_added = faces_after - self._faces_before

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

                volume_valid = self._volume_before_valid and after_valid and self._volume_before > 0
                repair.volume_before = self._volume_before if self._volume_before_valid else 0.0
                repair.volume_after = volume_after if after_valid else 0.0
                repair.volume_valid = volume_valid
                if volume_valid:
                    repair.volume_change_percent = (
                        (volume_after - self._volume_before) / self._volume_before
                    ) * 100.0
                else:
                    repair.volume_change_percent = 0.0

                repair.progress = 1.0
                context.window_manager.event_timer_remove(self._timer)
                self._timer = None

                self.report(
                    {"INFO"},
                    f"Reparo: {verts_merged} v\u00e9rtices fundidos, {faces_added} faces adicionadas.",
                )

                for area in context.screen.areas:
                    area.tag_redraw()
                return {"FINISHED"}

        except Exception as exc:
            context.window_manager.event_timer_remove(self._timer)
            self._timer = None
            repair.progress = 0.0
            if obj.mode != "OBJECT":
                bpy.ops.object.mode_set(mode="OBJECT")
            self.report({"ERROR"}, f"Erro durante reparo: {exc}")
            return {"CANCELLED"}

        self._step += 1
        for area in context.screen.areas:
            area.tag_redraw()
        return {"RUNNING_MODAL"}
