import bpy


class DiagnosticsProperties(bpy.types.PropertyGroup):
    vertices: bpy.props.IntProperty(
        name="Vértices",
        description="Número de vértices da malha ativa",
        default=0,
    )
    faces: bpy.props.IntProperty(
        name="Faces",
        description="Número de faces da malha ativa",
        default=0,
    )

    # Saúde da malha
    non_manifold_edges: bpy.props.IntProperty(
        name="Arestas Não-Manifold",
        description="Número de arestas não-manifold na malha ativa",
        default=0,
    )
    loose_vertices: bpy.props.IntProperty(
        name="Vértices Soltos",
        description="Número de vértices sem arestas na malha ativa",
        default=0,
    )
    zero_area_faces: bpy.props.IntProperty(
        name="Faces com Área Zero",
        description="Número de faces com área < 1e-8 na malha ativa",
        default=0,
    )
    health_valid: bpy.props.BoolProperty(
        name="Malha Saudável",
        description="True se a malha não tem problemas detectados",
        default=True,
    )

    # Diagnósticos adicionais (informativos)
    boundary_edges: bpy.props.IntProperty(
        name="Arestas de Borda",
        description="Número de arestas de borda (buracos na malha)",
        default=0,
    )
    duplicate_vertices: bpy.props.IntProperty(
        name="Vértices Sobrepostos",
        description="Número de vértices com posição duplicada (threshold 1e-4)",
        default=0,
    )
    flipped_faces: bpy.props.IntProperty(
        name="Faces com Normais Invertidas",
        description="Número de faces cuja normal aponta para o interior da malha",
        default=0,
    )
    self_intersecting_faces: bpy.props.IntProperty(
        name="Faces Auto-Intersectantes",
        description="Número de faces que se intersectam com outras partes da malha",
        default=0,
    )
    health_analyzed: bpy.props.BoolProperty(
        name="An\u00e1lise Realizada",
        description="True se a an\u00e1lise de sa\u00fade foi executada ao menos uma vez",
        default=False,
    )
