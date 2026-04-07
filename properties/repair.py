import bpy


class RepairProperties(bpy.types.PropertyGroup):
    show_options: bpy.props.BoolProperty(
        name="Mostrar op\u00e7\u00f5es",
        description="Exibe as op\u00e7\u00f5es de reparo de malha",
        default=True,
    )

    volume_before: bpy.props.FloatProperty(
        name="Volume Antes",
        description="Volume antes de reparar a malha (BU\u00b3)",
        default=0.0,
        precision=4,
    )
    volume_after: bpy.props.FloatProperty(
        name="Volume Depois",
        description="Volume depois de reparar a malha (BU\u00b3)",
        default=0.0,
        precision=4,
    )
    volume_change_percent: bpy.props.FloatProperty(
        name="Varia\u00e7\u00e3o de Volume (%)",
        description="Varia\u00e7\u00e3o percentual de volume ap\u00f3s o reparo",
        default=0.0,
        precision=3,
    )
    volume_valid: bpy.props.BoolProperty(
        name="Volume V\u00e1lido",
        description="Indica se o volume antes/depois do reparo \u00e9 confi\u00e1vel",
        default=False,
    )
    progress: bpy.props.FloatProperty(
        name="Progresso",
        description="Progresso da opera\u00e7\u00e3o de reparo (0.0\u20131.0)",
        default=0.0,
        min=0.0,
        max=1.0,
        precision=2,
    )
