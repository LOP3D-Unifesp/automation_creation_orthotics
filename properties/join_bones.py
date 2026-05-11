import bpy
from bpy.types import PropertyGroup



#Grupos dos pontos de referência (landmarks) para cada dedo e antebraço, usados para gerar os bones.
FINGER_DEFS = [
    ("wrist",  "Pulso",     ["wrist"]),
    ("thumb",  "Polegar",   ["thumb_mcp",   "thumb_pip",   "thumb_ip",    "thumb_tip"]),
    ("index",  "Indicador", ["index_mcp",   "index_pip",   "index_dip",   "index_tip"]),
    ("middle", "Médio",     ["middle_mcp",  "middle_pip",  "middle_dip",  "middle_tip"]),
    ("ring",   "Anelar",    ["ring_mcp",    "ring_pip",    "ring_dip",    "ring_tip"]),
    ("pinky",  "Mínimo",    ["pinky_mcp",   "pinky_pip",   "pinky_dip",   "pinky_tip"]),
    ("forearm", "Antebraço", ["elbow", "wrist_fa"])
]


# Rótulos de pontos de referência (landmarks) específicos.
NEXT_POINT_LABELS = {
    "wrist":   ["Pulso"],
    "thumb":   ["MCP - (base do dedo)", "PIP - (meio do dedo)", "IP - (última articulação)", "Ponta"],
    "index":   ["MCP - (base do dedo)", "PIP - (meio do dedo)", "DIP - (última articulação)", "Ponta"],
    "middle":  ["MCP - (base do dedo)", "PIP - (meio do dedo)", "DIP - (última articulação)", "Ponta"],
    "ring":    ["MCP - (base do dedo)", "PIP - (meio do dedo)", "DIP - (última articulação)", "Ponta"],
    "pinky":   ["MCP - (base do dedo)", "PIP - (meio do dedo)", "DIP - (última articulação)", "Ponta"],
    "forearm": ["Cotovelo", "Pulso"],
}


class AcoJointPoint(PropertyGroup):
    co: bpy.props.FloatVectorProperty(size=3, default=(0, 0, 0))
    group: bpy.props.StringProperty(default="")
    
    

class AcoRigHand(PropertyGroup):
    show_options:    bpy.props.BoolProperty(default=False)
    # dedo ativo no momento
    active_finger:   bpy.props.StringProperty(default="")

    # Coleção dos pontos de referência   
    joint_points:    bpy.props.CollectionProperty(type=AcoJointPoint)

    #Remover osso de um dedo especifico
    group_to_remove: bpy.props.EnumProperty(name="Para ser removido", description="Selecione o dedo cujo bone será removido", items=[
        ('NONE', 'Selecione...', 'Escolha uma opção'),
        ("thumb", "Polegar", "Remove o bone do polegar"),
        ("index", "Indicador", "Remove o bone do dedo indicador"),
        ("middle", "Médio", "Remove o bone do dedo médio"),
        ("ring", "Anelar", "Remove o bone do dedo anelar"),
        ("pinky", "Mindinho", "Remove o bone do dedo mínimo"),
        ("forearm", "Antebraço", "Remove o bone do antebraço")
    ], default="NONE"
)

    # Indica na interface se o rig foi gerado ou não
    generated:       bpy.props.BoolProperty(default=False)
    progress:        bpy.props.FloatProperty(default=0.0, min=0.0, max=1.0, subtype="FACTOR")



