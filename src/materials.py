import bpy
from . import selection_sets


def set_backface_culling(mode):
    objects_selected = selection_sets.meshes_with_materials()
    for obj in objects_selected:
        for mat in obj.data.materials:
            if mat is not None:
                mat.use_backface_culling = mode
    return {'FINISHED'}
