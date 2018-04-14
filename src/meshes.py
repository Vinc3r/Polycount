import bpy


def renameUVChannels(selectedObjects):
    for obj in selectedObjects:
        if len(obj.data.uv_textures) > 0:
            for uvChan in range(len(obj.data.uv_textures)):
                if uvChan == 0:
                    obj.data.uv_textures[0].name = "UVMap"
                else:
                    obj.data.uv_textures[uvChan].name = "UV{}".format(
                        (uvChan + 1))
    return {'FINISHED'}


def selectUVChannels(selectedObjects, uvChan):
    for obj in selectedObjects:
        if len(obj.data.uv_textures) > uvChan:
            obj.data.uv_textures[uvChan].active = True
        else:
            print("{} has no UV{}".format(obj.name, (uvChan + 1)))
    return {'FINISHED'}


if __name__ == "__main__":
    renameUVChannels(
        [o for o in bpy.context.selected_objects if o.type == 'MESH'])
    selectUVChannels(
        [o for o in bpy.context.selected_objects if o.type == 'MESH'], 1)
