import bpy
import math
from . import selection_sets


def transfer_names():
    user_active = bpy.context.view_layer.objects.active
    is_user_in_edit_mode = False
    if bpy.context.view_layer.objects.active.mode == 'EDIT':
        is_user_in_edit_mode = True
        bpy.ops.object.mode_set(mode='OBJECT')

    objects_selected = selection_sets.meshes_in_selection()
    for obj in objects_selected:
        bpy.context.view_layer.objects.active = obj
        mesh = obj.data
        mesh.name = obj.name

    bpy.context.view_layer.objects.active = user_active
    if is_user_in_edit_mode:
        bpy.ops.object.mode_set(mode='EDIT')

    return {'FINISHED'}


def set_autosmooth(user_angle):
    user_active = bpy.context.view_layer.objects.active
    is_user_in_edit_mode = False
    if bpy.context.view_layer.objects.active.mode == 'EDIT':
        is_user_in_edit_mode = True
        bpy.ops.object.mode_set(mode='OBJECT')

    objects_selected = selection_sets.meshes_in_selection()
    for obj in objects_selected:
        bpy.context.view_layer.objects.active = obj
        mesh = obj.data
        if mesh.has_custom_normals:
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
        mesh.use_auto_smooth = True
        mesh.auto_smooth_angle = math.radians(user_angle)
        bpy.ops.object.shade_smooth()

    bpy.context.view_layer.objects.active = user_active
    if is_user_in_edit_mode:
        bpy.ops.object.mode_set(mode='EDIT')

    return {'FINISHED'}
