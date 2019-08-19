import bpy
from . import selection_sets


def rename_uv_channels():
    objects_selected = selection_sets.meshes_in_selection()
    for obj in objects_selected:
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
    objects_selected = selection_sets.meshes_in_selection()
    for obj in objects_selected:
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
    objects_no_uv = []
    obj_no_uv_names: str = ""
    message_suffix = "no UV  on:"
    if operator.channel == 1:
        # UV2 check
        objects_no_uv = selection_sets.meshes_without_uv()[1]
        message_suffix = "no UV2 on:"
    else:
        # ask to report no UV at all
        objects_no_uv = selection_sets.meshes_without_uv()[0]
    for obj in objects_no_uv:
        obj_no_uv_names += "{}".format(obj.name)
        if objects_no_uv.index(obj) < (len(objects_no_uv) - 1):
            obj_no_uv_names += ", "
    message = "{} {}".format(message_suffix, obj_no_uv_names)
    operator.report({'WARNING'}, message)
    return {'FINISHED'}
