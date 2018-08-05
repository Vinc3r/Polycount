import bpy  

# from https://blender.stackexchange.com/questions/36523/how-can-i-delete-uv-layers-with-python

selection = bpy.context.selected_objects

for obj in selection:
    uv_textures = obj.data.uv_textures
    try:
        uv_textures.remove(uv_textures[1])
    except:
        print("")