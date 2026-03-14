import bpy


class MeshReductionProperties(bpy.types.PropertyGroup):
    # Visibilidade
    show_advanced: bpy.props.BoolProperty(
        name="Mostrar redução da malha",
        description="Exibe as operações manuais de redução da malha",
        default=False,
    )

    # Etapas ativas no pipeline
    use_collapse: bpy.props.BoolProperty(
        name="Aplicar Decimação",
        description="Inclui Decimação no pipeline de redução",
        default=True,
    )
    use_unsubdivide: bpy.props.BoolProperty(
        name="Aplicar Un-Subdivide",
        description="Inclui Un-Subdivide no pipeline de redução",
        default=True,
    )
    use_planar: bpy.props.BoolProperty(
        name="Aplicar Planar",
        description="Inclui Planar no pipeline de redução",
        default=True,
    )

    # Parâmetros de redução
    collapse_ratio: bpy.props.FloatProperty(
        name="Collapse Ratio",
        description="Proporção de faces para manter (campo interno)",
        default=0.5,
        min=0.0,
        max=1.0,
    )
    collapse_percent: bpy.props.IntProperty(
        name="Redução (%)",
        description="Percentual de redução da malha no modo Decimação",
        default=50,
        min=0,
        max=99,
        subtype="PERCENTAGE",
    )
    unsubdiv_iterations: bpy.props.IntProperty(
        name="Un-Subdivide Iterations",
        description="Quantidade de iterações no modo Un-Subdivide",
        default=1,
        min=1,
        max=100,
    )
    planar_angle: bpy.props.IntProperty(
        name="Planar Angle",
        description="Ângulo em graus usado na decimação Planar",
        default=10,
        min=0,
        max=180,
    )

    # Rastreamento de volume
    volume_before: bpy.props.FloatProperty(
        name="Volume Antes",
        description="Volume antes do pipeline de redução (BU³)",
        default=0.0,
        precision=4,
    )
    volume_after: bpy.props.FloatProperty(
        name="Volume Depois",
        description="Volume depois do pipeline de redução (BU³)",
        default=0.0,
        precision=4,
    )
    volume_change_percent: bpy.props.FloatProperty(
        name="Variação de Volume (%)",
        description="Variação percentual de volume após a redução",
        default=0.0,
        precision=3,
    )
    volume_valid: bpy.props.BoolProperty(
        name="Volume Válido",
        description="Indica se o volume antes/depois da redução é confiável",
        default=False,
    )
