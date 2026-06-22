import bpy
from bpy.types import Operator
import time
from ...external.google_sheets import update_google_sheet


class ACO_OT_processing_time_start(Operator):
    bl_idname = "aco.processing_time_start"
    bl_label = "Iniciar"
    bl_description = "Inicia a contagem de tempo para a tarefa atual"
 
    _timer = None
    name_task: bpy.props.StringProperty(name="Tarefa", default="")
 
    def modal(self, context, event):
        ts = context.scene.process_timer
 
        if not ts.running:
            # foi finalizado pelo operador "stop" -> limpa o timer e sai
            self.cancel(context)
            return {'FINISHED'}
 
        if event.type == 'TIMER':
            if not ts.paused:
                ts.elapsed = ts.accumulated + (time.monotonic() - ts.start_timestamp)
            if context.area:
                context.area.tag_redraw()
 
        return {'PASS_THROUGH'}
 
    def execute(self, context):
        ts = context.scene.process_timer
        ts.task_type = self.name_task.strip()

        if not ts.task_type:
            self.report({'WARNING'}, "Não foi possivel iniciar o tempo: nenhum processo foi definido.")
            return {'CANCELLED'}
        
        today = time.strftime("%d/%m/%Y", time.localtime()) 
        ts.date = today
        ts.running = True
        ts.paused = False
        ts.accumulated = 0.0
        ts.elapsed = 0.0
        ts.start_timestamp = time.monotonic()
 
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}
 
    def cancel(self, context):
        wm = context.window_manager
        if self._timer:
            wm.event_timer_remove(self._timer)
            self._timer = None
 
 
class ACO_OT_toggle_pause(Operator):
    bl_idname = "aco.toggle_pause"
    bl_label = "Pausar/Retomar"
    bl_description = "Pausa ou retoma a contagem do tempo"
 
    @classmethod
    def poll(cls, context):
        return context.scene.process_timer.running
 
    def execute(self, context):
        ts = context.scene.process_timer
        if ts.paused:
            ts.start_timestamp = time.monotonic()  # novo ponto de referência
            ts.paused = False
        else:
            ts.accumulated += time.monotonic() - ts.start_timestamp
            ts.paused = True
        return {'FINISHED'}


class ACO_OT_processing_time_stop(Operator):
    bl_idname = "aco.processing_time_stop"
    bl_label = "Finalizar"
    bl_description = "Finaliza a tarefa e salva o tempo total registrado"
 
    @classmethod
    def poll(cls, context):
        return context.scene.process_timer.running
 
    def execute(self, context):
        ts = context.scene.process_timer
 
        total = ts.accumulated
        if not ts.paused:
            total += time.monotonic() - ts.start_timestamp
 
        item = ts.log.add()
        item.task_type = ts.task_type
        item.duration = total

        today = time.strftime("%d/%m/%Y", time.localtime()) 

        try:
            update_google_sheet([item.task_type, ts.date, today, f"{item.duration:.1f}"])
        except Exception as e:
            self.report({'ERROR'}, f"Falha ao enviar para Google Sheets: {e}")
                
 
        ts.running = False
        ts.paused = False
        ts.elapsed = 0.0
        ts.accumulated = 0.0
 
        self.report({'INFO'}, f"'{item.task_type}' registrada: {total:.1f}s")
        return {'FINISHED'}
