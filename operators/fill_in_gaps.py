import bpy
from bpy.types import Object
import bmesh




def detect_gaps_activated_object():

    try:

        #Detectar arestas abertas ou regiões problemáticas da malha
        bpy.ops.mesh.select_non_manifold()

        sel = [v for v in bpy.context.object.data.vertices if v.select]

        return len(sel)
    
    except Exception as e:
        print(f"Ocorreu um erro ao detectar lacunas na malha: {e}")



def fill_in_the_blanks(obj: Object):

    blanks = detect_gaps_activated_object()

    if not blanks:
        #Não existe lacunas no objeto deve notificar o usuário
        return


    # Criar um bmesh a partir da malha atual
    bm = bmesh.from_edit_mesh(obj.data)

    # Suponha que você tenha uma lista de arestas selecionadas para os loops que você deseja preencher.
    # Essas arestas devem estar conectadas de forma adequada para a operação grid_fill funcionar.
    # Aqui, vamos pegar as arestas selecionadas como exemplo.
    edges = [e for e in bm.edges if e.select]


    bmesh.ops.fill_grid(bm, edges=edges, mat_nr=0, use_smooth=False, use_interp_simple=False)

    # Atualize a malha com as novas faces criadas
    bmesh.update_edit_mesh(obj.data) 



#Realizar uma classe de operador