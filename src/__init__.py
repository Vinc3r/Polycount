bl_info = {
    "name": "Nothing-is-3D tools",
    "description": "Some scripts 3D realtime workflow oriented.",
    "author": "Vincent (V!nc3r) Lamy",
    "category": "3D View",
    "wiki_url": 'https://github.com/Vinc3r/BlenderScripts',
    "tracker_url": 'https://github.com/Vinc3r/BlenderScripts/issues',
    "version": (1, 1, 0),
    "blender": (2, 80, 0)
}

"""A bunch of Thanks for some snippets, ideas, inspirations, to:
    - of course, Ton & all Blender devs,
    - Henri Hebeisen (henri-hebeisen.com), Pitiwazou (pitiwazou.com), Pistiwique (github.com/pistiwique),
    - and finally all Blender community and the ones I forget.
"""

import bpy
from bpy.props import (
    BoolProperty,
    IntProperty,
    EnumProperty,
    StringProperty,
)

if "bpy" in locals():
    import importlib
    if "meshes" in locals():
        importlib.reload(meshes)
    if "selection_sets" in locals():
        importlib.reload(selection_sets)
else:
    from .meshes import *
    from .selection_sets import *

class NTHG3D_PT_mesh_panel(bpy.types.Panel):
    bl_label = "Meshes"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Nthg is 3D"

    def draw(self, context):
        layout = self.layout
        UVchanBox = layout.box()
        UVchanBox.label(text="UV channels :")
        row = UVchanBox.row(align=True)
        row.label(text="Select:")
        row.operator("nothing3d.mesh_buttons", text="1").action = "select_UV1"
        row.operator("nothing3d.mesh_buttons", text="2").action = "select_UV2"
        row = UVchanBox.row()
        row.operator("nothing3d.mesh_buttons",
                     text="Rename channels").action = "rename_UV"


class NTHG3D_OT_MeshButtons(bpy.types.Operator):
    # note: no uppercase char in idname, use _ instead!
    bl_idname = "nothing3d.mesh_buttons"
    bl_label = "Add mesh panel buttons"
    action = bpy.props.StringProperty()

    def execute(self, context):
        if self.action == "rename_UV":
            meshes.rename_UV_channels()
        if self.action == "select_UV1":
            meshes.activate_UV_channels(0)
        if self.action == "select_UV2":
            meshes.activate_UV_channels(1)
        return{'FINISHED'}

classes = (
    NTHG3D_OT_MeshButtons,
    NTHG3D_PT_MeshPanel,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()