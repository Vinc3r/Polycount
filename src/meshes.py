import bpy
import math
from . import selection_sets


def transfer_names():
    objects_selected = selection_sets.meshes_in_selection()
    user_active = bpy.context.view_layer.objects.active
    for obj in objects_selected:
        bpy.context.view_layer.objects.active = obj
        mesh = obj.data
        mesh.name = obj.name
    bpy.context.view_layer.objects.active = user_active
    return {'FINISHED'}

def set_autosmooth():
    objects_selected = selection_sets.meshes_in_selection()
    user_active = bpy.context.view_layer.objects.active
    for obj in objects_selected:
        bpy.context.view_layer.objects.active = obj
        mesh = obj.data
        if mesh.has_custom_normals:
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
        mesh.use_auto_smooth = True
        mesh.auto_smooth_angle = math.radians(85)
        bpy.ops.object.shade_smooth()
    bpy.context.view_layer.objects.active = user_active
    return {'FINISHED'}
