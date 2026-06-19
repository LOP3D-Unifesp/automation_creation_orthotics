import bpy

from .ui import activated_an_object, change_mode
from .mesh import points_for


def decimate_by_type(decimate_type: str, parameter):
    activated_an_object()
    change_mode("OBJECT")

    obj = bpy.context.view_layer.objects.active
    mod = obj.modifiers.new(name="Decimate", type='DECIMATE')
    mod.decimate_type = decimate_type

    if decimate_type == 'COLLAPSE':
        mod.ratio = parameter
        mod.use_collapse_triangulate = True
    elif decimate_type == 'DISSOLVE':
        import math

        mod.angle_limit = math.radians(parameter)
        mod.use_dissolve_boundaries = False
    elif decimate_type == 'UNSUBDIV':
        mod.iterations = parameter

    bpy.ops.object.modifier_apply(modifier=mod.name)




def centroid(verts, matrix_world):
    import mathutils

    sum_coords = [0.0, 0.0, 0.0]
    for v in verts:
        sum_coords[0] += v.co.x
        sum_coords[1] += v.co.y
        sum_coords[2] += v.co.z

    center_local = []
    for coordinate in sum_coords:
        center_local.append(coordinate / len(verts))

    center_world = matrix_world @ mathutils.Vector(center_local)

    print(f"O centr\u00f3ide \u00e9: {center_world}")

    return center_world


def object_size_by_axis(axis: str):
    obj = bpy.context.active_object

    verts = obj.data.vertices
    if not verts:
        return

    axis_index = {'X': 0, 'Y': 1, 'Z': 2}.get(axis)

    first_value = verts[0].co[axis_index]
    coordinate_min = first_value
    coordinate_max = first_value

    for v in verts[1:]:
        value = v.co[axis_index]
        if value < coordinate_min:
            coordinate_min = value
        elif value > coordinate_max:
            coordinate_max = value

    return {'co_max': coordinate_max, 'co_min': coordinate_min, 'size': coordinate_max - coordinate_min}


def collect_grouped_points(rig, items, is_tuple=False):
    # Coleta pontos agrupados em ordem
    grouped = {}

    for item in items:
        key = item[0] if is_tuple else item  # pega o primeiro valor da tupla

        lista_pontos = []

        # percorre os pontos desse dedo
        for p in points_for(rig, key):
            #print(p.co[:])

            lista_pontos.append(p.co[:])

        print(f"Lista de pontos dos bones: {lista_pontos}")
        grouped[key] = lista_pontos
        
    return grouped


def create_finger_bones(eb, bone_map, key, pts, names, wrist_co=None):
    if key in ("wrist", "forearm"):
        return # Esses casos são tratados depois
    
    for i in range(3):
        if i + 1 >= len(pts):
            break

        if not pts[i] or not pts[i + 1]:
            continue

        name = names[i]

        b      = eb.new(name)
        b.head = pts[i]
        b.tail = pts[i + 1]
        bone_map[name] = b
    
     # Criar um osso conectando o pulso ao primeiro osso do dedo
    if wrist_co and names and len(pts) > 0:
        connect_name = f"{key}_root" 
        b = eb.new(connect_name)
        b.head = wrist_co        # começa no pulso
        b.tail = pts[0]        # vai até a base do dedo (MCP)
        bone_map[connect_name] = b

        # Definir hierarquia: root → MCP
        if names[0] in bone_map:
            bone_map[names[0]].parent      = bone_map[connect_name]
            bone_map[names[0]].use_connect = True


    # Parentesco e hierarquia do dedo (MCP→PIP→DIP→TIP)

    for i in range(1, 3):
        child_n  = names[i]
        parent_n = names[i - 1]
        if child_n in bone_map and parent_n in bone_map:
            bone_map[child_n].parent      = bone_map[parent_n]
            bone_map[child_n].use_connect = True


def create_forearm_bone(eb, bone_map, grouped):

    try:
        # Criar osso do antebraço 
        pts = grouped.get("forearm", [])
        if len(pts) >= 2:
            b = eb.new("forearm")
            b.head = pts[0]  
            b.tail = pts[1]   
            bone_map["forearm"] = b
            
    except Exception as e:
        return
    
    
    


def add_point_marker(point_world, radius=1.5):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=point_world)
    marker = bpy.context.active_object
    marker.name = name
    return marker

def clear_markers():
    pass