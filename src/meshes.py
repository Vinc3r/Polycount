import bpy
from . import selection_sets


def rename_UV_channels():
    objects_list = selection_sets.meshes_in_selection()
    for obj in objects_list:
        if len(obj.data.uv_textures) < 0:
            continue
        for uv_chan in range(len(obj.data.uv_textures)):
            if uv_chan == 0:
                obj.data.uv_textures[0].name = "UVMap"
            else:
                obj.data.uv_textures[uv_chan].name = "UV{}".format(
                    (uv_chan + 1))
    return {'FINISHED'}


def activate_UV_channels(uv_chan):
    objects_list = commons.get_meshes_in_selection()
    for obj in objects_list:
        if len(obj.data.uv_textures) < uv_chan:
            print("{} has no UV{}".format(obj.name, (uv_chan + 1)))
            continue
        obj.data.uv_textures[uv_chan].active = True
    return {'FINISHED'}

def test():
    print(selection_sets.meshes_without_uv())

if __name__ == "__main__":
    rename_UV_channels()
    activate_UV_channels(1)
