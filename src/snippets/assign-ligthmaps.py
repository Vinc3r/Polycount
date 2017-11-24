import bpy
import os.path

print("++++++")

# get engine name
## print(bpy.context.scene.render.engine)

LIGHTMAP_FOLDER_PATH = "//textures\HD\LM\T5"
PATTERN_FILENAME = "{{OBJ_NAME}}.LM.png"

def assign_lightmap():
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH' and obj.data.uv_textures[1] is not None:
            LIGHTMAP_FILENAME = PATTERN_FILENAME.replace("{{OBJ_NAME}}", obj.name)
            for mat in obj.data.materials:
                LM_FOUND = False
                for slot in mat.texture_slots:
                    if slot is not None and slot.texture is not None and slot.texture.image is not None:
                        if slot.texture.image.name == LIGHTMAP_FILENAME and slot.use_map_ambient:
                            print(slot.texture.name)
                            LM_FOUND = True
            if not LM_FOUND:
                texture_file_path = os.path.join(LIGHTMAP_FOLDER_PATH, LIGHTMAP_FILENAME)
                texture_file_fullpath = bpy.path.abspath(texture_file_path)
                if os.path.exists(texture_file_fullpath):
                    new_image = bpy.data.images.load(texture_file_path, check_existing=True)
                    new_image.name = LIGHTMAP_FILENAME
                    if bpy.data.textures[LIGHTMAP_FILENAME] is not None:
                        new_tex = bpy.data.textures[LIGHTMAP_FILENAME]
                    else:
                        new_tex = bpy.data.textures.new(LIGHTMAP_FILENAME, 'IMAGE')                   
                    new_tex.name = LIGHTMAP_FILENAME
                    new_tex.image = new_image 
                    slot = mat.texture_slots.add()
                    slot.use_map_color_diffuse = False
                    slot.use_map_ambient = True
                    slot.ambient_factor = 1.0
                    slot.texture = new_tex                    
                    slot.uv_layer = obj.data.uv_textures[1].name

assign_lightmap()
