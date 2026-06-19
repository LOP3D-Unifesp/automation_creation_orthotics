import bpy 
from bpy.types import PropertyGroup
from bpy.props import StringProperty, FloatProperty, BoolProperty, CollectionProperty, IntProperty

class ProcessingTime(PropertyGroup):
    task_type: StringProperty(name="Tarefa", default="")
    duration: FloatProperty(name="Duração (s)")


class ProcessingTime_State(PropertyGroup):
    task_type: StringProperty(
        name="Tarefa",
        description="Nome da tarefa que está sendo cronometrada",
    )
    running: BoolProperty(default=False)
    paused: BoolProperty(default=False)
    date: StringProperty(name="Data", default="")
    start_timestamp: FloatProperty(default=0.0)
    accumulated: FloatProperty(default=0.0)   # tempo já somado antes da pausa atual
    elapsed: FloatProperty(default=0.0)       # só para exibir na UI em tempo real
    log: CollectionProperty(type=ProcessingTime)
    log_index: IntProperty(default=0)