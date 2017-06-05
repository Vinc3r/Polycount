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
    """Rename the first two UV channels as UVMap and UV2"""
    bl_idname = "nothing3d.rename_uv_channel"
    bl_label = "Rename UV channels"
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                try:
                    obj.data.uv_textures[0].name = "UVMap"
                    try:
                        obj.data.uv_textures[1].name = "UV2"
                    except:
                        print("nothingIs3dTools : no UV2 on "+str(obj.name))
                        pass
                except:
                    print("nothingIs3dTools : no UV on "+str(obj.name))
                    pass
        return {'FINISHED'}

class SelectUVChannel(bpy.types.Operator):
    """Select the desired UV channel"""
    bl_idname = "nothing3d.select_uv_channel"
    bl_label = "Select the desired UV channel"
    select_UV = bpy.props.IntProperty()
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                try:
                    obj.data.uv_textures[self.select_UV].active = True
                except:
                    print("nothingIs3dTools : no UV2 on "+str(obj.name))
                    pass
        return {'FINISHED'}

class BImtlSetIntensity(bpy.types.Operator):
    """Set intensity value to 1"""
    bl_idname = "nothing3d.bi_mtl_set_intensity"
    bl_label = "Set intensity value to 1"
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                if len(obj.data.materials) > 0:
                    for mat in obj.data.materials:
                        mat.diffuse_intensity = 1
                else:
                    print("nothingIs3dTools : no material on "+str(obj.name))
        return {'FINISHED'}
    
class BImtlSetWhite(bpy.types.Operator):
    """Set diffuse color to white"""
    bl_idname = "nothing3d.bi_mtl_set_white"
    bl_label = "Set diffuse color to white"
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                if len(obj.data.materials) > 0:
                    for mat in obj.data.materials:
                        mat.diffuse_color = (1,1,1)
                else:
                    print("nothingIs3dTools : no material on "+str(obj.name))
        return {'FINISHED'}
    
class BImtlResetAlpha(bpy.types.Operator):
    """Reset transparency parameters"""
    bl_idname = "nothing3d.bi_mtl_reset_alpha"
    bl_label = "Reset transparency parameters"
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                if len(obj.data.materials) > 0:
                    for mat in obj.data.materials:
                        mat.transparency_method = 'Z_TRANSPARENCY'
                        mat.alpha = 1
                        mat.use_transparency = False
                else:
                    print("nothingIs3dTools : no material on "+str(obj.name))
        return {'FINISHED'}
    
class disableAutosmooth(bpy.types.Operator):
    """Disable mesh Auto Smoothing"""
    bl_idname = "nothing3d.disable_auto_smooth"
    bl_label = "Disable mesh Auto Smoothing"
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                obj.data.use_auto_smooth = False
                #obj.modifier_add(type='EDGE_SPLIT')
                #obj.modifiers["EdgeSplit"].split_angle = 1.48353
        return {'FINISHED'}

class Nothing3DPanel(bpy.types.Panel):
    bl_label = "Nothing-is-3D tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Addons"

    def draw(self, context):
        layout = self.layout

        UVchanBox = layout.box()
        UVchanBox.label(text = "UV channels :")
        
        row = UVchanBox.row(align = True)
        row.label(text = "Select ")
        row.operator("nothing3d.select_uv_channel", text = "UV1").select_UV = 0
        row.operator("nothing3d.select_uv_channel", text = "UV2").select_UV = 1
        
        importHelperBox = layout.box()
        importHelperBox.label(text = "Import cleaner :")
        
        row = importHelperBox.row(align = True)
        row.operator("nothing3d.rename_uv_channel", text = "Rename UV channels")
        row.operator("nothing3d.disable_auto_smooth", text = "", icon = "MOD_EDGESPLIT")
        
        row = importHelperBox.row(align = True)
        row.operator("nothing3d.bi_mtl_set_intensity", text = "Diffuse intensity")
        row.operator("nothing3d.bi_mtl_set_white", text = "", icon = "SOLID")
        row.operator("nothing3d.bi_mtl_reset_alpha", text = "", icon = "MATCAP_24")
        

def register():
    bpy.utils.register_class(renameUVChannel)
    bpy.utils.register_class(SelectUVChannel)
    bpy.utils.register_class(BImtlSetIntensity)
    bpy.utils.register_class(BImtlSetWhite)
    bpy.utils.register_class(BImtlResetAlpha)
    bpy.utils.register_class(disableAutosmooth)
    bpy.utils.register_class(Nothing3DPanel)

def unregister():
    bpy.utils.unregister_class(renameUVChannel)
    bpy.utils.unregister_class(SelectUVChannel)
    bpy.utils.unregister_class(BImtlSetIntensity)
    bpy.utils.unregister_class(BImtlSetWhite)
    bpy.utils.unregister_class(BImtlResetAlpha)
    bpy.utils.unregister_class(disableAutosmooth)
    bpy.utils.unregister_class(Nothing3DPanel)

if __name__ == "__main__":
    register()
