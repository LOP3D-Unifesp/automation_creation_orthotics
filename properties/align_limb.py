import bpy


class AlignAxisProperties(bpy.types.PropertyGroup):
    # Legacy single-axis selector kept for compatibility with existing flows (e.g. rigging).
    axis: bpy.props.EnumProperty(
        name="Eixo",
        description="Escolha o eixo de alinhamento",
        items=[
            ("X", "X", "Alinhar no eixo X"),
            ("Y", "Y", "Alinhar no eixo Y"),
            ("Z", "Z", "Alinhar no eixo Z"),
        ],
        default="X",
    )

    # New multi-axis toggles used by the Prepare Model UI.
    axis_x: bpy.props.BoolProperty(name="X", description="Alinhar no eixo X", default=True)
    axis_y: bpy.props.BoolProperty(name="Y", description="Alinhar no eixo Y", default=False)
    axis_z: bpy.props.BoolProperty(name="Z", description="Alinhar no eixo Z", default=False)