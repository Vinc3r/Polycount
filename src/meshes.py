import bpy
from . import selection_sets


def mesh_transfer_names():
    objects_list = selection_sets.meshes_in_selection()
    current_active = bpy.context.view_layer.objects.active
    for obj in objects_list:
        bpy.context.view_layer.objects.active = obj
        mesh = obj.data
        mesh.name = obj.name
    bpy.context.view_layer.objects.active = current_active
    return {'FINISHED'}
