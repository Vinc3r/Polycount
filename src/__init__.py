bl_info = {
    "name": "Nothing-is-3D tools",
    "description": "Some scripts 3D realtime workflow oriented.",
    "author": "Vincent (V!nc3r) Lamy",
    "category": "Object",
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

if "bpy" in locals():
    print("---- DEBUG HELP LINE ----")
    import importlib

    importlib.reload(meshes)
    importlib.reload(selection_sets)
else:
    from . import meshes, selection_sets

import bpy
from bpy.props import (
    FloatVectorProperty,
    IntProperty,
    BoolProperty,
    StringProperty,
    FloatProperty,
    EnumProperty,
)


class NTHG3D_PT_mesh_panel(bpy.types.Panel):
    bl_label = "Meshes"
    bl_idname = "NTHG3D_PT_mesh_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Nothing-is-3D"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        # UV chan part
        row.label(text="UV channels :")
        box = layout.box()
        row = box.row(align=True)
        row.label(text="Active:")
        row.operator("nothing3d.mesh_panel_buttons", text="1").action = "select_UV1"
        row.operator("nothing3d.mesh_panel_buttons", text="2").action = "select_UV2"
        row = box.row(align=True)
        row.operator("nothing3d.mesh_panel_buttons", text="Rename channels").action = "rename_UV"
        row = box.row(align=True)
        row.operator("nothing3d.mesh_panel_buttons", text="Report no UV").action = "report_no_UV"


class NTHG3D_OT_mesh_panel_buttons(bpy.types.Operator):
    bl_idname = "nothing3d.mesh_panel_buttons"
    bl_label = "Buttons in meshes panel"
    action: StringProperty()

    def execute(self, context):
        if self.action == "rename_UV":
            meshes.rename_uv_channels()
        if self.action == "select_UV1":
            meshes.activate_uv_channels(0)
        if self.action == "select_UV2":
            meshes.activate_uv_channels(1)
        if self.action == "report_no_UV":
            meshes.report_no_uv(self)
        return {'FINISHED'}


classes = (
    NTHG3D_PT_mesh_panel,
    NTHG3D_OT_mesh_panel_buttons,
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
