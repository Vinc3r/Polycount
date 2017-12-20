bl_info = {
    "name": "Nothing-is-3D tools",
    "description": "Some scripts 3D realtime workflow oriented",
    "author": "Vincent (Vinc3r) Lamy - Thanks for some example or piece of code from Wazou, Pistiwique, Alexander Milovsky, all Blender community",
    "location": "3D view toolshelf - Nthg is 3D tab",
    "category": "Mesh",	
    "wiki_url": 'https://github.com/Vinc3r/BlenderScripts',
    "tracker_url": 'https://github.com/Vinc3r/BlenderScripts/issues',
    "version": (2017, 11, 29, 2127),
}

import bpy

print("++++ nothing-is-3D tools loaded ++++")

class renameUVChannel(bpy.types.Operator):
    """Rename the first two UV channels as UVMap and UV2"""
    bl_idname = "nothing3d.rename_uv_channel"
    bl_label = "Rename UV channels"
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH' and len(obj.data.uv_textures) > 0 :
                obj.data.uv_textures[0].name = "UVMap"
                if len(obj.data.uv_textures) > 1:
                    obj.data.uv_textures[1].name = "UV2"
        return {'FINISHED'}

class SelectUVChannel(bpy.types.Operator):
    """Select the desired UV channel"""
    bl_idname = "nothing3d.select_uv_channel"
    bl_label = "Select the desired UV channel"
    select_UV = bpy.props.IntProperty()
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH' \
            and len(obj.data.uv_textures) > 0 \
            and len(obj.data.uv_textures) >= self.select_UV:
                obj.data.uv_textures[self.select_UV].active = True
        return {'FINISHED'}

class BImtlSetIntensity(bpy.types.Operator):
    """Set intensity value to 1"""
    bl_idname = "nothing3d.bi_mtl_set_intensity"
    bl_label = "Set intensity value to 1"
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH' and len(obj.data.materials) > 0:
                for mat in obj.data.materials:
                    mat.diffuse_intensity = 1
        return {'FINISHED'}
    
class BImtlSetWhite(bpy.types.Operator):
    """Set diffuse color to white"""
    bl_idname = "nothing3d.bi_mtl_set_white"
    bl_label = "Set diffuse color to white"
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH' and len(obj.data.materials) > 0 :
                for mat in obj.data.materials:
                    mat.diffuse_color = (1,1,1)
        return {'FINISHED'}
    
class BImtlSetSpec(bpy.types.Operator):
    """Set specular color to dark gray"""
    bl_idname = "nothing3d.bi_mtl_set_spec"
    bl_label = "Set default spec color"
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH' and len(obj.data.materials) > 0 :
                for mat in obj.data.materials:
                    mat.specular_color = (.1,.1,.1)
                    mat.specular_intensity = 1
        return {'FINISHED'}
    
class BImtlResetAlpha(bpy.types.Operator):
    """Reset transparency parameters"""
    bl_idname = "nothing3d.bi_mtl_reset_alpha"
    bl_label = "Reset transparency parameters"
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH' and len(obj.data.materials) > 0 :
                for mat in obj.data.materials:
                    mat.transparency_method = 'Z_TRANSPARENCY'
                    mat.alpha = 1
                    mat.use_transparency = False
        return {'FINISHED'}
    
class BImtlTexSolid(bpy.types.Operator):
    """Set diffuse texture on Textured Solid"""
    bl_idname = "nothing3d.bi_tex_solid"
    bl_label = "Set texture face"
    # 0 = diffuse mode, 1 = lightmap mode
    set_texture_type = bpy.props.IntProperty()
    
    def execute(self, context):
        # get object selected
        for obj in context.selected_objects:
            #only meshes with at least one material
            if obj.type == 'MESH' and len(obj.data.materials) > 0:
                mesh = obj.data
                is_editmode = (obj.mode == 'EDIT')
                
                # if in EDIT Mode switch to OBJECT
                if is_editmode:
                    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)                
                
                
                for matID in range(len(obj.data.materials)):
                    mat = mesh.materials[matID]
                    
                    # this set active texture for each material face assignation
                    
                    for texSlot in range(len(mat.texture_slots)):
                        # diffuse mode
                        if self.set_texture_type == 0:
                            # check if : there is a texture, if it used diffuse channel, if it use uv coord, if mesh has an uv chan
                            if mat.texture_slots[texSlot] != None \
                            and mat.texture_slots[texSlot].use_map_color_diffuse \
                            and mat.texture_slots[texSlot].texture_coords == "UV" \
                            and len(mesh.uv_textures) > 0 \
                            and obj.data.uv_textures[self.set_texture_type] is not None:
                                # select mesh first UV channel
                                mesh.uv_textures[0].active = True
                                # set active texture as diffuse texture
                                mat.active_texture_index = texSlot
                        # lightmap mode
                        if self.set_texture_type == 1:
                            if mat.texture_slots[texSlot] != None \
                            and mat.texture_slots[texSlot].use_map_ambient \
                            and mat.texture_slots[texSlot].texture_coords == "UV" \
                            and len(mesh.uv_textures) > 1 \
                            and obj.data.uv_textures[self.set_texture_type] is not None:
                                # select mesh UV2 channel
                                mesh.uv_textures[1].active = True
                                # set active texture as ambient texture
                                mat.active_texture_index = texSlot
                
                    # if no UVtex - create it
                    if not mesh.uv_textures:
                        uvtex = bpy.ops.mesh.uv_texture_add()

                    uvtex = mesh.uv_textures.active
                    uvtex.active_render = True                
                    img = None    
                    aspect = 1.0
                    
                    # this set texture face
                    
                    if mat.active_texture != None:
                        texSlot = mat.active_texture_index
                        img = mat.active_texture
                        # some check to sync active UVmap and images associate
                        if not is_editmode and img.type == "IMAGE" \
                        and (mat.texture_slots[texSlot].uv_layer == mesh.uv_layers.active.name \
                        or mat.texture_slots[texSlot].uv_layer == ""):
                            # assign image according to material assignation
                            for f in mesh.polygons:
                                if f.material_index == matID:
                                    uvtex.data[f.index].image = img.image
                            
                # Back to EDIT Mode
                if is_editmode:
                    bpy.ops.object.mode_set(mode='EDIT', toggle=False)

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

class Nthg3DMeshPanel(bpy.types.Panel):
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
        row.label(text = "Select ")
        row.operator("nothing3d.select_uv_channel", text = "UV1").select_UV = 0
        row.operator("nothing3d.select_uv_channel", text = "UV2").select_UV = 1
        
        row = UVchanBox.row()
        row.operator("nothing3d.rename_uv_channel", text = "Rename UV channels")

class Nothing3DMaterialPanel(bpy.types.Panel):
    bl_label = "Materials"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Nthg is 3D"

    def draw(self, context):
        # Blender Render
        if bpy.context.scene.render.engine == "BLENDER_RENDER":
            layout = self.layout
            row = layout.row(align = True)
            row.operator("nothing3d.bi_mtl_set_intensity", text = "Diffuse intensity to 1")
            row.operator("nothing3d.bi_mtl_set_white", text = "", icon = "SOLID")
            row.operator("nothing3d.bi_mtl_reset_alpha", text = "", icon = "MATCAP_24")
            row.operator("nothing3d.bi_mtl_set_spec", text = "", icon = "BRUSH_TEXFILL")
            row = layout.row(align = True)
            row.operator("nothing3d.bi_tex_solid", text = "", icon = "TEXTURE").set_texture_type = 0
            row.operator("nothing3d.bi_tex_solid", text = "", icon = "BRUSH_SMEAR").set_texture_type = 1
        # Cycles
        elif bpy.context.scene.render.engine == "CYCLES":
            print("Nothing is 3D : Cycles not yet supported")
        else:
            print("Nothing is 3D : Render engine not supported")

class Nthg3DStatsPanel(bpy.types.Panel):
    bl_label = "Stats"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Nthg is 3D"

    def draw(self, context):
        layout = self.layout
        
        """ Selection stats box """
        # thanks to sambler for some piece of code https://github.com/sambler/addonsByMe/blob/master/mesh_summary.py
        
        selectionStatsBox = layout.box()
        row = selectionStatsBox.row(align = True)
        row.label(text = "Object")
        row.label(text = "Verts")
        row.label(text = "Tris")

        # test only selected meshes
        selectedMeshes = [o for o in bpy.context.selected_objects if o.type == 'MESH']
              
        totalTriInSelection = 0
        totalVertsInSelection = 0

        for element in selectedMeshes:
            triCount = 0
            hasNGon = False
            for poly in element.data.polygons:
                # first check if quad
                if len(poly.vertices) == 4:
                    triCount += 2
                # or tri
                elif len(poly.vertices) == 3:
                    triCount += 1
                # or oops, ngon here, alert!
                else:
                    triCount += 3
                    hasNGon = True
            # adding element stats to total count
            totalTriInSelection += triCount
            totalVertsInSelection += len(element.data.vertices)
            # generate table
            row = selectionStatsBox.row(align = True)
            row.label(text = "%s" % (element.name))
            row.label(text = "%i " % (len(element.data.vertices)))
            if not hasNGon:
                row.label(text = "%i" % (triCount))
            else:
                # visual indicator if ngon
                row.label(text = "± %i" % (triCount))
        # show total stats                
        selectionStatsBox.row().separator() 
        row = selectionStatsBox.row(align = True)
        row.label(text = "TOTAL")
        row.label(text = "%i" % (totalVertsInSelection))
        row.label(text = "%i" % (totalTriInSelection))        

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
