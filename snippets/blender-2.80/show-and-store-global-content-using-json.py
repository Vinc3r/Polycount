bl_info = {
    "name": "Hello World! using json",
    "category": "Object",
    "version": (0, 0, 0),
    "blender": (2, 80, 0)
}

"""
    thanks to Elreenys & tricotou on https://blenderartists.org/t/how-to-store-global-variable/1183164/
    
    
    
    this one isn't working for now
"""

import bpy
import bmesh
import json
from bpy.types import Scene
from bpy.props import (
    BoolProperty,
    StringProperty
)



def do_something_on_meshes():
    total_tris_in_selection = 0
    total_verts_in_selection = 0
    thats_a_default_json = StringProperty(default="{}")
    bpy.context.scene.thats_a_global_scene_variable = json.dumps({})

    # calculate only selected objects
    for obj in [o for o in bpy.context.selected_objects if o.type == 'MESH']:
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        verts_count = len(bm.verts)
        thats_a_default_json.append({
            "name": obj.name,
            "verts": verts_count
        })            
        bm.free()

    # my_data = {"hello":True, "cool" : [0,1,2,3]}
    bpy.context.scene.thats_a_global_scene_variable = json.dumps(thats_a_default_json)

    return {'FINISHED'}


class HelloJson_PT_HelloWorldPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Hello Json World Panel"
    bl_idname = "OBJECT_PT_hellojson"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Hello"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="objects list: ")
        if json.loads(context.scene.thats_a_global_scene_variable) == "{}":
            row = layout.row(align=True)
            row.label(text="no objects names to show")
            print("thats_a_global_scene_variable is empty")
        else:
            col_flow = layout.column_flow(align=True)
            for data in json.loads(context.scene.thats_a_global_scene_variable).items():
                row = col_flow.row(align=True)
                row.label(text=str(data[0]))
                row.label(text=str(data[1]))

        row = layout.row()
        row.operator("hellojson.do_something", text="Refresh", icon="FILE_REFRESH").action = True

class HelloJson_OT_HelloWorldPanel(bpy.types.Operator):
    bl_idname = "hellojson.do_something"
    bl_label = "hello json world operations"
    action: BoolProperty(default=False)

    def execute(self, context):
        if self.action:
            print("user interaction")
            do_something_on_meshes()
            self.action = False
        return {'FINISHED'}

def register():
    bpy.utils.register_class(HelloJson_PT_HelloWorldPanel)
    bpy.utils.register_class(HelloJson_OT_HelloWorldPanel)
    Scene.thats_a_global_scene_variable = StringProperty(default="{}")


def unregister():
    del Scene.thats_a_global_scene_variable
    bpy.utils.unregister_class(HelloJson_OT_HelloWorldPanel)
    bpy.utils.unregister_class(HelloJson_PT_HelloWorldPanel)

if __name__ == "__main__":
    register()