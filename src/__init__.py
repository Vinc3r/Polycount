bl_info = {
    "name": "Nothing-is-3D tools",
    "description": "Some scripts 3D realtime workflow oriented.",
    "author": "Vincent (V!nc3r) Lamy, nothing-is-3d.com",
    "location": "3D view toolshelf > Nthg-is-3D tab",
    "category": "3D View",
    "wiki_url": 'https://github.com/Vinc3r/BlenderScripts',
    "tracker_url": 'https://github.com/Vinc3r/BlenderScripts/issues',
    "version": (1, 0, 0),
}

"""A bunch of Thanks for some snippets, ideas, inspirations, to:
    - of course, Ton & all Blender devs,
    - Henri Hebeisen (henri-hebeisen.com), Pitiwazou (pitiwazou.com), Pistiwique (github.com/pistiwique),
    - and finally all Blender community and the ones I forget.
"""

# from https://wiki.blender.org/index.php/Dev:Py/Scripts/Cookbook/Code_snippets/Multi-File_packages
if "bpy" in locals():
    from importlib import reload
    if "meshes" in locals():
        reload(meshes)
    if "materials_bi" in locals():
        reload(materials_bi)
    if "commons" in locals():
        reload(selection_sets)
    print("addOn Nothing-is-3D tools reloaded")
else:
    from . import meshes, materials_bi, selection_sets
    print("addOn Nothing-is-3D tools imported")

import bpy


class NTHG3D_PT_material_bi_panel(bpy.types.Panel):
    bl_label = "Materials"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Nthg is 3D"

    @classmethod
    def poll(cls, context):
        return bpy.context.scene.render.engine == "BLENDER_RENDER"

    def draw(self, context):
        layout = self.layout
        fbxCleanerBox = layout.box()
        fbxCleanerBox.label(text="FBX cleaner:")
        row = fbxCleanerBox.row(align=True)
        row.operator("nothing3d.mtl_bi_buttons",
                     text="intensity", icon="ANTIALIASED").action = "reset_intensity"
        row.operator("nothing3d.mtl_bi_buttons",
                     text="color", icon="MATSPHERE").action = "reset_color"
        row.operator("nothing3d.mtl_bi_buttons",
                     text="spec", icon="MESH_CIRCLE").action = "reset_spec"
        row.operator("nothing3d.mtl_bi_buttons",
                     text="alpha", icon="IMAGE_RGB_ALPHA").action = "reset_alpha"


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
        row.label(text="Activate UV:")
        row.operator("nothing3d.mesh_buttons", text="1").action = "select_UV1"
        row.operator("nothing3d.mesh_buttons", text="2").action = "select_UV2"
        row = UVchanBox.row()
        row.operator("nothing3d.mesh_buttons",
                     text="Rename channels").action = "rename_UV"
        row = UVchanBox.row()
        row.operator("nothing3d.mesh_buttons",
                     text="TEST").action = "TEST"



class NTHG3D_OT_mesh_buttons(bpy.types.Operator):
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
        if self.action == "TEST":
            meshes.test()
        return{'FINISHED'}


class NTHG3D_OT_material_bi_buttons(bpy.types.Operator):
    # note: no uppercase char in idname, use _ instead!
    bl_idname = "nothing3d.mtl_bi_buttons"
    bl_label = "Add material Blender Internal panel buttons"
    action = bpy.props.StringProperty()

    def execute(self, context):
        if self.action == "reset_intensity":
            materials_bi.reset_intensity()
        if self.action == "reset_color":
            materials_bi.reset_color_value()
        if self.action == "reset_spec":
            materials_bi.reset_spec_value()
        if self.action == "reset_alpha":
            materials_bi.reset_alpha_value()
        return{'FINISHED'}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
