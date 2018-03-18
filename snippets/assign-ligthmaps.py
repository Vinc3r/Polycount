import bpy
import os.path

print("++++++ASSIGN LIGHTMAPS++++++")

# get engine name
# print(bpy.context.scene.render.engine)
"""
 different cases to handle:
    - no UV2 on obj > skip
    - if a texture slot already use ambient and UV2, we have to overwrite it
"""

lightmapFolderPath = r"//lightmaps"
patternFilename = r"OBJ_NAME.LM.png"
D = bpy.data
C = bpy.context

def assign_lightmap():
    for obj in C.selected_objects:
        # check if object is mesh and have UV2
        if obj.type == 'MESH' and \
           len(obj.data.uv_textures) > 1:
            lightmapFilename = patternFilename.replace("OBJ_NAME", obj.name)
            lightmapFilepath = os.path.join(lightmapFolderPath, lightmapFilename)
            print(obj.name+": lightmap filepath: "+lightmapFilepath)
            for mat in obj.data.materials:
                # check if a lightmap is already assigned
                for slot in mat.texture_slots:
                    if slot is not None and \
                       slot.texture is not None and \
                       slot.texture.image is not None and \
                       slot.use_map_ambient:
                        print("lightmap already exist in "+obj.name)
                        if slot.texture.image.name != lightmapFilename:
                            print("but path was wrong")
                            slot.texture.image.filepath = lightmapFilepath
                        # lets be sure UV2 is used
                        slot.uv_layer = obj.data.uv_textures[1].name
                        lightmapFound = True
            if not lightmapFound:
                texture_file_fullpath = bpy.path.abspath(lightmapFilepath)
                if os.path.exists(texture_file_fullpath):
                    print("texture exist")
                    isTextureExist = False
                    for t in D.textures:
                        if t.name == lightmapFilename:
                            new_tex = bpy.data.textures[lightmapFilename]
                            isTextureExist = True
                            continue
                    if not isTextureExist:
                        new_tex = bpy.data.textures.new(lightmapFilename, 'IMAGE')
                        new_tex.name = lightmapFilename
                    if bpy.data.images[lightmapFilename] is not None:
                        new_image = bpy.data.images[lightmapFilename]
                    else:
                        new_image = bpy.data.images.load(lightmapFilepath, check_existing=True)
                        new_image.name = lightmapFilename
                    new_tex.image = new_image 
                    slot = mat.texture_slots.add()
                    slot.use_map_color_diffuse = False
                    slot.use_map_ambient = True
                    slot.ambient_factor = 1.0
                    slot.texture = new_tex                    
                    slot.uv_layer = obj.data.uv_textures[1].name
                else:
                    print("/!\ lightmap file for {} doesn't exist".format(obj.name))
        else:
            print("/!\ {} not prepared for lightmaps".format(obj.name))
                        

assign_lightmap()
