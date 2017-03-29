bl_info = {
    "name": "Nothing-is-3D tools",
    "description": "Some scripts 3D realtime workflow oriented",
    "author": "Vincent Lamy",
    "location": "3D view toolshelf - Addons tab",
    "category": "Mesh",	
    'wiki_url': 'https://github.com/Vinc3r/BlenderScripts',
    'tracker_url': 'https://github.com/Vinc3r/BlenderScripts/issues',
}

import bpy

class renameUVChannel(bpy.types.Operator):
    """Normalize UV channel naming"""
    bl_idname = "nothing3d.rename_uv_channel"
    bl_label = "Rename UV chans as UVMap and UV2"
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                try:
                    obj.data.uv_textures[0].name = "UVMap"
                    try:
                        obj.data.uv_textures[1].name = "UV2"
                    except:
                        print("no UV2 on "+str(obj.name))
                        pass
                except:
                    print("no UV on "+str(obj.name))
                    pass
        return {'FINISHED'}

class SelectUVChannel(bpy.types.Operator):
    """Select desired UV channel"""
    bl_idname = "nothing3d.select_uv_channel"
    bl_label = "Select desired UV channel"
    select_UV = bpy.props.IntProperty()
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                try:
                    obj.data.uv_textures[self.select_UV].active = True
                except:
                    print("no UV2 on "+str(obj.name))
                    pass
        return {'FINISHED'}
    
class Nothing3DPanel(bpy.types.Panel):
    bl_label = "Nothing-is-3D tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Addons"

    def draw(self, context):
        layout = self.layout

        box1 = layout.box()
        box1.label(text = "UV channels")
        
        row = box1.row(align = True)
        row.label(text = "Select ")
        row.operator("nothing3d.select_uv_channel", text = "UV1").select_UV = 0
        row.operator("nothing3d.select_uv_channel", text = "UV2").select_UV = 1
        
        row = box1.row()
        row.operator("nothing3d.rename_uv_channel", text = "Normalize naming")
        

def register():
    bpy.utils.register_class(renameUVChannel)
    bpy.utils.register_class(SelectUVChannel)
    bpy.utils.register_class(Nothing3DPanel)

def unregister():
    bpy.utils.unregister_class(renameUVChannel)
    bpy.utils.unregister_class(SelectUVChannel)
    bpy.utils.unregister_class(Nothing3DPanel)

if __name__ == "__main__":
    register()
