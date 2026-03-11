import bpy


class AlignAxisProperties(bpy.types.PropertyGroup):
    axis: bpy.props.EnumProperty(name="Eixo", description="Escolha o eixo de alinhamento",
                                items=[
                                    ('X',  'X',  'Alinhar no eixo X'),
                                    ('Y',  'Y',  'Alinhar no eixo Y'),
                                    ('Z',  'Z',  'Alinhar no eixo Z'),
                                ],
                                default='X'
                                )