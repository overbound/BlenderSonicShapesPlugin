bl_info = {
    "name": "Sine Slope",
    "author": "jnphgs",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > Sine Slope",
    "description": "Adds a Sine Slope",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "category": "Add Sine Slope",
}

import bpy
import math
from bpy.types import Operator
from bpy.props import IntProperty, FloatProperty, FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

def add_sine_slope(self, context):
    verts = []
    edges = []
    faces = []
    res = self.Resolution
    amplitude = self.Amplitude
    wavelength = self.Wavelength
    length = self.Length / 2.0

    # Create the vertices for the sine slope
    for i in range(res + 1):  # +1 to include the last point
        x = (length * 2) * i / res - length  # Linearly interpolate along the x-axis
        z = amplitude * math.sin(2 * math.pi * x / wavelength)  # Sine function for the z-axis
        verts.append(Vector((x, 0, z)))

    for i in range(res + 1):
        x = (length * 2) * i / res - length  # Same x as above
        z = amplitude * math.sin(2 * math.pi * x / wavelength)  # Same sine function for the z-axis
        verts.append(Vector((x, self.Height, z)))
    
    # Create faces
    for i in range(res):
        faces.append([i, i + 1, res + 1 + i + 1, res + 1 + i])

    # Create the mesh
    mesh = bpy.data.meshes.new(name="Sine Slope")
    mesh.from_pydata(verts, edges, faces)
    mesh.update()
    object_data_add(context, mesh, operator=self)

class OBJECT_OT_Add_Sine_Slope(Operator, AddObjectHelper):
    bl_idname = "mesh.add_sine_slope"
    bl_label = "Add Sine Slope"
    bl_options = {'REGISTER', 'UNDO'}

    Resolution: IntProperty(
        name="Resolution",
        description="Number of subdivisions along the slope.",
        default=8,
        min=4,
        max=256
    )

    Amplitude: FloatProperty(
        name="Amplitude",
        description="Amplitude of the sine wave.",
        default=4.0,
        min=0.01
    )
    
    Wavelength: FloatProperty(
        name="Wavelength",
        description="Wavelength of the sine wave.",
        default=60,
        min=0.01
    )

    Length: FloatProperty(
        name="Length",
        description="Length of the sine slope.",
        default=32.0,
        min=0.01
    )
    

    Height: FloatProperty(
        name="Height",
        description="Height of the sine slope.",
        default=5.0,
        min=0.01
    )

    def execute(self, context):
        add_sine_slope(self, context)
        return {'FINISHED'}

def menu_fn(self, context):
    self.layout.operator(
        OBJECT_OT_Add_Sine_Slope.bl_idname,
        text="Add Sine Slope",
        icon='PLUGIN')

def register():
    bpy.utils.register_class(OBJECT_OT_Add_Sine_Slope)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_fn)
    print("register: sine slope addon")


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_Add_Sine_Slope)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_fn)
    print("unregister: sine slope addon")


if __name__ == "__main__":
    register()
