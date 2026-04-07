import bpy


class QuadRemeshProperties(bpy.types.PropertyGroup):
    # Visibilidade
    show_options: bpy.props.BoolProperty(
        name="Mostrar Quad Remesh",
        description="Exibe as configurações opcionais de Quad Remesh",
        default=False,
    )

    # Parâmetros
    voxel_size: bpy.props.FloatProperty(
        name="Voxel Size",
        description="Tamanho do voxel usado no remesh",
        default=4.0,
        min=0.01,
        soft_max=10.0,
        precision=3,
    )
    smooth_shade: bpy.props.BoolProperty(
        name="Suavizar",
        description="Aplica smooth shading após o remesh",
        default=True,
    )

    # Rastreamento de volume
    volume_before: bpy.props.FloatProperty(
        name="Volume Antes",
        description="Volume antes de aplicar Quad Remesh (BU³)",
        default=0.0,
        precision=4,
    )
    volume_after: bpy.props.FloatProperty(
        name="Volume Depois",
        description="Volume depois de aplicar Quad Remesh (BU³)",
        default=0.0,
        precision=4,
    )
    volume_change_percent: bpy.props.FloatProperty(
        name="Variação de Volume (%)",
        description="Variação percentual de volume após Quad Remesh",
        default=0.0,
        precision=3,
    )
    volume_valid: bpy.props.BoolProperty(
        name="Volume Válido",
        description="Indica se o volume antes/depois do Quad Remesh é confiável",
        default=False,
    )
