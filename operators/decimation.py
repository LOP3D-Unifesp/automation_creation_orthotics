import bpy
from ..utils import decimate_by_type, object_has_to_be_activated


class ACO_OT_decimate_planar(bpy.types.Operator):
    bl_idname = "aco.reduce_polygonos_by_planar"
    bl_label = "Decimação Planar"
    bl_options = {'REGISTER', 'UNDO'}

    angle_limit: bpy.props.IntProperty( 
        name="Angle Limit",
        description="Junta faces que estão quase planas seguindo o angulo",
        default=10,
        min=0,
        max=180
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)

    def draw(self, context):
        layout = self.layout
        
        layout.label(text="Limite de ângulo entre faces planas: ")
        layout.prop(self, "angle_limit")

    @object_has_to_be_activated
    def execute(self, context):

        try:
        
            decimate_by_type('DISSOLVE', self.angle_limit)

            print(f" Decimação Planar: {self.angle_limit}")
        
        except Exception as e:

            bpy.ops.aco.alert_error_popup('INVOKE_DEFAULT', message=e)

        return {'FINISHED'}





class ACO_OT_decimate_collapse(bpy.types.Operator):
    bl_idname = "aco.reduce_polygonos_by_collapse"
    bl_label = "Decimação Collapse"
    bl_options = {'REGISTER', 'UNDO'}

    ratio: bpy.props.FloatProperty(
        name="Ratio",
        description="Parâmetro para controlar a porcentagem de redução",
        default=0.5
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)

    def draw(self, context):
        layout = self.layout
        
        layout.label(text="Proporção de faces a manter: ")
        layout.prop(self, "ratio")

    @object_has_to_be_activated
    def execute(self, context):
        
        try:

            decimate_by_type('COLLAPSE', self.ratio)

            print(f" Decimação Collapse: {self.ratio}")
        
        except Exception as e:
            bpy.ops.aco.alert_error_popup('INVOKE_DEFAULT', message=e)
        
        return {'FINISHED'}
    



class ACO_OT_decimate_un_subdivide(bpy.types.Operator):
    bl_idname = "aco.reduce_polygonos_by_un_subdivide"
    bl_label = "Decimação Un-Subdivide"
    bl_options = {'REGISTER', 'UNDO'}

    iterations: bpy.props.IntProperty(
        name="Iterations",
        description="Parâmetro que remove a quantidade de etapas de subdivisão",
        default=1
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_popup(self, event)

    def draw(self, context):
        layout = self.layout

        layout.label(text="Quantas vezes reduzir: ")
        layout.prop(self, "iterations")

    @object_has_to_be_activated
    def execute(self, context):
        
        try:

            decimate_by_type('UNSUBDIV', self.iterations)

            print(f" Decimação Un-Subdivide: {self.iterations}")
        
        except Exception as e:
            bpy.ops.aco.alert_error_popup('INVOKE_DEFAULT', message=e)

        return {'FINISHED'}




class ACO_OT_number_of_vertices_and_faces(bpy.types.Operator):
    bl_idname = "aco.number_of_vertices_and_face"
    bl_label = "Números de Vértices e Faces do Objeto Ativo"

    @object_has_to_be_activated
    def execute(self, context):

        obj = context.active_object

        if not obj or obj.type != 'MESH' :
            num_vertices = 0
            face_count = 0

            bpy.ops.aco.alert_error_popup('INVOKE_DEFAULT', message="Não foi possivel realizar a contagem das vértices e faces do objeto 3D.")
        
        else:

            num_vertices = len(obj.data.vertices)
            face_count = len(obj.data.polygons)

        
        context.scene.vertices = num_vertices
        context.scene.faces = face_count

        return {'FINISHED'}
        

        

        

        




