bl_info = {
    "name": "Custom Cube",
    "author": "jnphgs",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > Custom Cube",
    "description": "Adds a Cube with specific dimensions and corner origin",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "category": "Add Custom Cube",
}

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

def add_custom_cube(self, context):
    verts = []
    edges = []
    faces = []

    size = self.Size  # Full size for defining the cube dimensions

    # Define the vertices of the cube with origin at the bottom-front-left corner
    verts = [
        Vector((0, 0, 0)),  # Bottom-front-left corner (origin)
        Vector((size[0], 0, 0)),  # Bottom-front-right corner
        Vector((size[0], size[1], 0)),  # Top-front-right corner
        Vector((0, size[1], 0)),  # Top-front-left corner
        Vector((0, 0, size[2])),  # Bottom-back-left corner
        Vector((size[0], 0, size[2])),  # Bottom-back-right corner
        Vector((size[0], size[1], size[2])),  # Top-back-right corner
        Vector((0, size[1], size[2])),  # Top-back-left corner
    ]

    # Define the faces of the cube using the vertices
    faces = [
        [0, 1, 2, 3],  # Front face
        [4, 5, 6, 7],  # Back face
        [0, 3, 7, 4],  # Left face
        [1, 2, 6, 5],  # Right face
        [0, 1, 5, 4],  # Bottom face
        [2, 3, 7, 6],  # Top face
    ]

    # Create the mesh
    mesh = bpy.data.meshes.new(name="Custom Cube")
    mesh.from_pydata(verts, edges, faces)
    mesh.update()
    object_data_add(context, mesh, operator=self)

class OBJECT_OT_Add_Custom_Cube(Operator, AddObjectHelper):
    bl_idname = "mesh.add_custom_cube"
    bl_label = "Add Custom Cube"
    bl_options = {'REGISTER', 'UNDO'}

    Size: FloatVectorProperty(
        name="Size",
        description="Dimensions of the cube (Width, Height, Depth).",
        default=(5.0, 5.0, 5.0),
        min=0.01,
        subtype='XYZ',
    )

    def execute(self, context):
        add_custom_cube(self, context)
        return {'FINISHED'}

def menu_fn(self, context):
    self.layout.operator(
        OBJECT_OT_Add_Custom_Cube.bl_idname,
        text="Add Custom Cube",
        icon='PLUGIN')

def register():
    bpy.utils.register_class(OBJECT_OT_Add_Custom_Cube)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_fn)
    print("register: custom cube addon")


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_Add_Custom_Cube)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_fn)
    print("unregister: custom cube addon")


if __name__ == "__main__":
    register()
