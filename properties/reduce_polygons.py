import bpy

class ReducePolygonsProperties(bpy.types.PropertyGroup):
    ratio: bpy.props.FloatProperty(
        name="Ratio",
        description="ParÃ¢metro para controlar a porcentagem de reduÃ§Ã£o",
        default=0.5
    )
    iterations: bpy.props.IntProperty(
        name="Iterations",
        description="ParÃ¢metro que remove a quantidade de etapas de subdivisÃ£o",
        default=1
    )
    angle_limit: bpy.props.IntProperty(  # â† Corrigido aqui
        name="Angle Limit",
        description="Junta faces que estÃ£o quase planas seguindo o angulo",
        default=10,
        min=0,
        max=180
    )

