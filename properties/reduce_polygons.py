import bpy

class ReducePolygonsProperties(bpy.types.PropertyGroup):
    ratio: bpy.props.FloatProperty(
        name="Ratio",
        description="Parâmetro para controlar a porcentagem de redução",
        default=0.5
    )
    iterations: bpy.props.IntProperty(
        name="Iterations",
        description="Parâmetro que remove a quantidade de etapas de subdivisão",
        default=1
    )
    angle_limit: bpy.props.IntProperty(  # ← Corrigido aqui
        name="Angle Limit",
        description="Junta faces que estão quase planas seguindo o angulo",
        default=10,
        min=0,
        max=180
    )
