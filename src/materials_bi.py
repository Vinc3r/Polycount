import bpy


def resetIntensity(selectedObjects):
    for obj in selectedObjects:
        if not obj.data.materials:
            continue
        for mat in obj.data.materials:
            mat.diffuse_intensity = 1
    return {'FINISHED'}

def resetColorValue(selectedObjects):
    for obj in selectedObjects:
        if not obj.data.materials:
            continue
        for mat in obj.data.materials:
            mat.diffuse_color = (1,1,1)
    return {'FINISHED'}

def resetSpecValue(selectedObjects):
    for obj in selectedObjects:
        if not obj.data.materials:
            continue
        for mat in obj.data.materials:
            mat.specular_color = (0, 0, 0)
            mat.specular_intensity = 1
    return {'FINISHED'}

if __name__ == "__main__":
    resetIntensity([o for o in bpy.context.selected_objects if o.type == 'MESH'])
    resetColorValue([o for o in bpy.context.selected_objects if o.type == 'MESH'])
