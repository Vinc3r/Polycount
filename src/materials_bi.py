import bpy
from . import selection_sets


def reset_intensity():
    objects_list = selection_sets.meshes_with_materials()
    for obj in objects_list:
        for mat in obj.data.materials:
            mat.diffuse_intensity = 1
    return {'FINISHED'}


def reset_color_value():
    objects_list = selection_sets.meshes_with_materials()
    for obj in objects_list:
        for mat in obj.data.materials:
            mat.diffuse_color = (1, 1, 1)
    return {'FINISHED'}


def reset_spec_value():
    objects_list = selection_sets.meshes_with_materials()
    for obj in objects_list:
        for mat in obj.data.materials:
            mat.specular_color = (0, 0, 0)
            mat.specular_intensity = 1
    return {'FINISHED'}

def reset_alpha_value():
    objects_list = selection_sets.meshes_with_materials()
    for obj in objects_list:
        for mat in obj.data.materials:
            mat.transparency_method = 'Z_TRANSPARENCY'
            mat.alpha = 1
            mat.use_transparency = False
    return {'FINISHED'}


if __name__ == "__main__":
    reset_intensity()
    reset_color_value()
