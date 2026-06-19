import bpy
from bpy.types import PropertyGroup


class PointToScore(PropertyGroup):
    point_world: bpy.props.FloatVectorProperty(size=3, default=(0,0,0))
    name: bpy.props.StringProperty(default="")
    radius: bpy.props.FloatProperty(default=1.5)

class PointMarkers(PropertyGroup):
    markers: bpy.props.CollectionProperty(type=PointToScore)
    


