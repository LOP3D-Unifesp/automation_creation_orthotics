import bpy
from ..properties import FINGER_DEFS




#Retorna a lista de grupos de pontos de referência (landmarks)
def get_defs():
    defs = list(FINGER_DEFS)
    return defs



def get_specifics_defs(keys):
    defs = list(FINGER_DEFS)

    defs_specific = [d for d in defs if d[0] in keys]
    
    return defs_specific

        

#retorna todos os pontos do rig salvos na lista que pertencem a um grupo específico
def points_for(rig, key):
    points = []

    for p in rig.joint_points:
        if p.group == key:
            points.append(p)

    return points



def expected(key):

    # valor ignorado (underscore é usado para indicar que não será usado)
    for k, _, names in [*FINGER_DEFS]:
        if k == key:
            # retorna quantos nomes estão definidos para aquele grupo
            return len(names)
    return 0


#Mede o quanto já foi realizado e atualiza rig.progress

def update_progress(rig):
    defs = get_defs()

    total = 0
    for item in defs:
        names = item[2]
        total = total + len(names)

    marked = 0
    for item in defs:
        key = item[0]
        points = points_for(rig, key)
        marked = marked + len(points)

    if total > 0:
        rig.progress = marked / total
    else:
        rig.progress = 0.0




def next_incomplete(rig):
    """Retorna a chave do próximo dedo que ainda tem pontos faltando."""
    for key, _, names in get_defs():
        if len(points_for(rig, key)) < len(names):
            return key
    return ""