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

import bpy

print("++++ nothing-is-3D tools loaded ++++")

nthg3D_prefix = "nthg3D:"

# from https://wiki.blender.org/index.php/Dev:Py/Scripts/Cookbook/Code_snippets/Multi-File_packages
if "bpy" in locals():
    from importlib import reload
    if "meshes" in locals():
        reload(meshes)
    print("{} Reloaded multifiles".format(nthg3D_prefix))
else:
    from . import meshes
    print("Imported multifiles")
        
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
        
        row = UVchanBox.row()
        row.operator("nothing3d.meshButtons", text = "Rename UV channels").action = "renameUV"
        
class OBJECT_OT_MeshButtons(bpy.types.Operator):
    bl_idname = "nothing3d.meshButtons"
    bl_label = "Add mesh panel buttons"
    action = bpy.props.StringProperty()
    
    def execute(self, context):
        if self.action == "renameUV":
            meshes.renameUVChannels([o for o in bpy.context.selected_objects if o.type == 'MESH'])
        
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()