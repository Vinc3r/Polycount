import bpy

objectSelection = [o for o in bpy.context.selected_objects if o.type == 'MESH']

def renameUVChannels(objectSelection):
    for obj in objectSelection:
        if len(obj.data.uv_textures) > 0 :
            obj.data.uv_textures[0].name = "UVMap"
            if len(obj.data.uv_textures) > 1:
                obj.data.uv_textures[1].name = "UV2"
    return {'FINISHED'}
        
if __name__ == "__main__":
    renameUVChannels(objectSelection)