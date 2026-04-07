import bpy

class ReducePolygonsProperties(bpy.types.PropertyGroup):
    ratio: bpy.props.FloatProperty(
        name="Ratio",
        description="Par\u00e2metro para controlar a porcentagem de redu\u00e7\u00e3o",
        default=0.5
    )
    iterations: bpy.props.IntProperty(
        name="Iterations",
        description="Par\u00e2metro que remove a quantidade de etapas de subdivis\u00e3o",
        default=1
    )
    angle_limit: bpy.props.IntProperty(  # \u2190 Corrigido aqui
        name="Angle Limit",
        description="Junta faces que est\u00e3o quase planas seguindo o angulo",
        default=10,
        min=0,
        max=180
    )

