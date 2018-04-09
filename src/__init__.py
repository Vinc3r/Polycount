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
    - Henri Hebeisen (henri-hebeisen.com), Pitiwazou (pitiwazou.com), Pistiwique (github.com/pistiwique), Alexander Milovsky,
    - and finally all Blender community and the ones I forget.
"""

# from https://wiki.blender.org/index.php/Dev:Py/Scripts/Cookbook/Code_snippets/Multi-File_packages
if "bpy" in locals():
    from importlib import reload
    if "meshes" in locals():
        reload(meshes)
    print("addOn Nothing-is-3D tools reloaded")
else:
    from . import meshes
    print("addOn Nothing-is-3D tools imported")

import bpy
        
class MeshPanel(bpy.types.Panel):
    bl_label = "Meshes"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Nthg is 3D"

    def draw(self, context):
        layout = self.layout
        
        """ UV Channels box """

        UVchanBox = layout.box()
        UVchanBox.label(text = "UV channels :")
        
        row = UVchanBox.row(align = True)
        row.label(text = "Select UV")
        row.operator("nothing3d.mesh_buttons", text = "1").action = "selectUV1"
        row.operator("nothing3d.mesh_buttons", text = "2").action = "selectUV2"
        row = UVchanBox.row()
        row.operator("nothing3d.mesh_buttons", text = "Rename channels").action = "renameUV"
        
class NTHG3D_OT_MeshButtons(bpy.types.Operator):
    # note: no uppercase char in idname, use _ instead!
    bl_idname = "nothing3d.mesh_buttons"
    bl_label = "Add mesh panel buttons"
    action = bpy.props.StringProperty()
    
    def execute(self, context):
        if self.action == "renameUV":
            meshes.renameUVChannels([o for o in bpy.context.selected_objects if o.type == 'MESH'])
        if self.action == "selectUV1":
            meshes.selectUVChannels([o for o in bpy.context.selected_objects if o.type == 'MESH'], 0)
        if self.action == "selectUV2":
            meshes.selectUVChannels([o for o in bpy.context.selected_objects if o.type == 'MESH'], 1)
        return{'FINISHED'}
        
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()