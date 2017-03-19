import bpy

C = bpy.context
D = bpy.data

UVtoSelect = 1

for obj in C.selected_objects:
    if obj.type == 'MESH':
        try:
            obj.data.uv_textures[UVtoSelect].active = True
        except:
            print("no UV2 on "+str(obj.name))
            pass