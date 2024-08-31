bl_info = {
    "name": "Quarter Pipe",
    "author": "jnphgs",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > Quarter Pipe",
    "description": "Adds a Quarter Pipe",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "category": "Add Quarter Pipe",
}


import bpy
import math
from bpy.types import Operator
from bpy.props import IntProperty, FloatProperty, FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
from mathutils import Matrix


def add_object(self, context):
    verts = []
    edges = []
    faces = []
    res = self.Resolution
    height = self.Height / 2.0
    radius = self.Radius

    # Create the vertices for the quarter pipe
    for i in range(res + 1):  # +1 to include the last point of the quarter circle
        theta = (math.pi / 2) * i / res  # Only go from 0 to pi/2
        verts.append(Vector((radius * math.cos(theta), 0, radius * math.sin(theta))))
    
    for i in range(res + 1):
        theta = (math.pi / 2) * i / res
        verts.append(Vector((radius * math.cos(theta), height, radius * math.sin(theta))))
    
    # Create faces
    for i in range(res):
        faces.append([i, i + 1, res + 1 + i + 1, res + 1 + i])

    # Create the mesh
    mesh = bpy.data.meshes.new(name="Quarter Pipe")
    mesh.from_pydata(verts, edges, faces)
    mesh.update()
    matrix = Matrix.Scale(-1, 4, (0, 0, 1))  # Scale by -1 on the Z axis
    mesh.transform(matrix)
    object_data_add(context, mesh, operator=self)


class OBJECT_OT_Add_Custom_Mesh(Operator, AddObjectHelper):
    bl_idname = "mesh.add_custom_mesh"
    bl_label = "Add Custom Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    Resolution: IntProperty(
        name="Resolution",
        description="division count.",
        default=6,
        min=3,
        max=256
    )

    Height: FloatProperty(
        name="Height",
        description="height of poll.",
        default=1.0,
        min=0.0001
    )
    Radius: FloatProperty(
        name="Height",
        description="height of poll.",
        default=1.0,
        min=0.0001
    )

    def execute(self, context):
        add_object(self, context)
        return {'FINISHED'}

def menu_fn(self, context):
    self.layout.operator(
        OBJECT_OT_Add_Custom_Mesh.bl_idname,
        text="Add Custom Mesh",
        icon='PLUGIN')

def register():
    bpy.utils.register_class(OBJECT_OT_Add_Custom_Mesh)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_fn)
    print("register: custom mesh addon")


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_Add_Custom_Mesh)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_fn)
    print("unregister: custom mesh addon")


if __name__ == "__main__":
    register()