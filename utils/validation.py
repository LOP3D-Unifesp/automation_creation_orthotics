import bmesh
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree


def validate_mesh(obj):
    """Analisa a saúde da malha do objeto.

    Retorna um dict com:
        non_manifold_edges (int): arestas conectadas a != 2 faces.
        loose_vertices (int): vértices sem nenhuma aresta.
        zero_area_faces (int): faces com área < 1e-8.
        boundary_edges (int): arestas de borda (buracos) — somente 1 face ligada.
        duplicate_vertices (int): vértices sobrepostos (threshold 1e-4).
        flipped_faces (int): faces com normal divergente da recalculada por topologia.
        self_intersecting_faces (int): faces que se intersectam com outras partes da malha.
        is_valid (bool): True se non_manifold, loose e zero_area forem zero.
    """
    result = {
        "non_manifold_edges": 0,
        "loose_vertices": 0,
        "zero_area_faces": 0,
        "boundary_edges": 0,
        "duplicate_vertices": 0,
        "flipped_faces": 0,
        "self_intersecting_faces": 0,
        "is_valid": True,
    }

    if not obj or obj.type != "MESH":
        return result

    bm = bmesh.new()
    try:
        bm.from_mesh(obj.data)
        bm.edges.ensure_lookup_table()
        bm.verts.ensure_lookup_table()
        bm.faces.ensure_lookup_table()

        # Checks originais (determinam is_valid)
        result["non_manifold_edges"] = sum(1 for e in bm.edges if not e.is_manifold)
        result["loose_vertices"] = sum(1 for v in bm.verts if not v.link_edges)
        result["zero_area_faces"] = sum(1 for f in bm.faces if f.calc_area() < 1e-8)

        result["is_valid"] = (
            result["non_manifold_edges"] == 0
            and result["loose_vertices"] == 0
            and result["zero_area_faces"] == 0
        )

        # Buracos: arestas com apenas 1 face ligada
        result["boundary_edges"] = sum(1 for e in bm.edges if len(e.link_faces) == 1)

        # Vértices sobrepostos via KDTree
        num_verts = len(bm.verts)
        if num_verts > 0:
            kd = KDTree(num_verts)
            for v in bm.verts:
                kd.insert(v.co, v.index)
            kd.balance()

            visited = set()
            duplicates = 0
            for v in bm.verts:
                if v.index in visited:
                    continue
                neighbors = kd.find_range(v.co, 1e-4)
                extras = [idx for (_, idx, _) in neighbors if idx != v.index and idx not in visited]
                if extras:
                    duplicates += len(extras)
                    visited.update(extras)
                visited.add(v.index)
            result["duplicate_vertices"] = duplicates

        # Faces com normais invertidas via recalc topológico
        if len(bm.faces) > 0:
            bm_copy = bm.copy()
            try:
                bmesh.ops.recalc_face_normals(bm_copy, faces=bm_copy.faces)
                bm_copy.normal_update()
                result["flipped_faces"] = sum(
                    1 for f, fc in zip(bm.faces, bm_copy.faces)
                    if f.normal.dot(fc.normal) < 0
                )
            finally:
                bm_copy.free()

        # Auto-interseções via BVHTree
        if len(bm.faces) > 0:
            bvh = BVHTree.FromBMesh(bm, epsilon=1e-6)
            overlaps = bvh.overlap(bvh)

            adjacent = [set() for _ in bm.faces]
            for e in bm.edges:
                fl = list(e.link_faces)
                for i in range(len(fl)):
                    for j in range(i + 1, len(fl)):
                        adjacent[fl[i].index].add(fl[j].index)
                        adjacent[fl[j].index].add(fl[i].index)

            self_int = set()
            for (i, j) in overlaps:
                if i != j and j not in adjacent[i]:
                    self_int.add(i)
                    self_int.add(j)
            result["self_intersecting_faces"] = len(self_int)

    except Exception:
        pass
    finally:
        bm.free()

    return result
