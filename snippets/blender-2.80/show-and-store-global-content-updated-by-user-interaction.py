bl_info = {
    "name": "Hello World!",
    "category": "Object",
    "version": (0, 0, 0),
    "blender": (2, 80, 0)
}


import bpy
import bmesh
from bpy.types import Scene
from bpy.props import (
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
    BoolProperty,
    IntProperty,
    StringProperty
)

thats_a_default_array = []

def do_something_on_meshes():
    total_tris_in_selection = 0
    total_verts_in_selection = 0

    # calculate only selected objects
    for obj in [o for o in bpy.context.selected_objects if o.type == 'MESH']:
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        verts_count = len(bm.verts)
        thats_a_default_array.append([
            obj.name,
            verts_count
        ])
        bm.free()

    return {'FINISHED'}


class Hello_PT_HelloWorldPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Hello World Panel"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Hello"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="objects list: ")
        row = layout.row()
        row.label(text=obj.name)
        row = layout.row()
        if len(thats_a_default_array) == 0:
            row.label(text="NEINNEIN")
        else:
            row.label(text="JAJAJAJ")

        row = layout.row()
        row.operator("hello.do_something", text="Refresh", icon="FILE_REFRESH").action = True

class Hello_OT_HelloWorldPanel(bpy.types.Operator):
    bl_idname = "hello.do_something"
    bl_label = "hello world operations"
    action: BoolProperty(default=False)

    def execute(self, context):
        if self.action:
            print("user interaction")
            do_something_on_meshes()
            self.action = False
        return {'FINISHED'}

def register():
    bpy.utils.register_class(Hello_PT_HelloWorldPanel)
    bpy.utils.register_class(Hello_OT_HelloWorldPanel)


def unregister():
    bpy.utils.unregister_class(Hello_OT_HelloWorldPanel)
    bpy.utils.unregister_class(Hello_PT_HelloWorldPanel)


if __name__ == "__main__":
    register()