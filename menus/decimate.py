import bpy



class ACO_MT_decimate_collapse(bpy.types.Menu):
    bl_label = "Collapse"
    bl_idname = "ACO_MT_decimate_collapse"


    def draw(self, context):
        layout = self.layout

        layout.operator("aco.reduce_polygonos_by_collapse", text="Collapse")
        



class ACO_MT_decimate_un_subdivide(bpy.types.Menu):
    bl_label = "Un-Subdivide"
    bl_idname = "ACO_MT_decimate_un_subdivide"


    def draw(self, context):
        layout = self.layout

        layout.operator("aco.reduce_polygonos_by_un_subdivide", text="Un-Subdivide")
        



class ACO_MT_decimate_planar(bpy.types.Menu):
    bl_label = "Planar"
    bl_idname = "ACO_MT_decimate_planar"


    def draw(self, context):
        layout = self.layout

        layout.operator("aco.reduce_polygonos_by_planar", text="Planar")
        


