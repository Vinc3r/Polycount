import bpy
from . import selection_sets


def rename_uv_channels():
    objects_list = selection_sets.meshes_in_selection()
    for obj in objects_list:
        mesh = obj.data
        if len(mesh.uv_layers) < 0:
            continue
        for uv_chan in range(len(mesh.uv_layers)):
            if uv_chan == 0:
                mesh.uv_layers[0].name = "UVMap"
            else:
                mesh.uv_layers[uv_chan].name = "UV{}".format((uv_chan + 1))
    return {'FINISHED'}


def activate_uv_channels(uv_chan):
    objects_list = selection_sets.meshes_in_selection()
    for obj in objects_list:
        mesh = obj.data
        if len(mesh.uv_layers) == 0:
            print("{} has no UV".format(obj.name))
            continue
        if len(mesh.uv_layers) <= uv_chan:
            print("{} has no UV{}".format(obj.name, (uv_chan + 1)))
            continue
        obj.data.uv_layers[uv_chan].active = True
    return {'FINISHED'}


def report_no_uv(operator):
    objects_list = selection_sets.meshes_without_uv()
    obj_names: str = ""
    for obj in objects_list:
        obj_names += "{}".format(obj.name)
        if objects_list.index(obj) < (len(objects_list) - 1):
            obj_names += ", "
    message = "no UV chan' on: {}".format(obj_names)
    operator.report({'WARNING'}, message)
    return {'FINISHED'}
