import bpy
import math

"""
    This batch custom normals deletion on selected objects, and also activate autosmooth with 85°
"""

print("+++++ DELETE Normals Custom Data +++++")

objects = [o for o in bpy.context.selected_objects if o.type == 'MESH']

for obj in range(len(objects)):
    current_object = objects[obj]
    mesh = current_object.data
    if mesh.has_custom_normals:
        print("%i of %i - processing %s" % ((obj+1), len(objects), current_object.name))
        bpy.context.scene.objects.active = current_object
        bpy.ops.mesh.customdata_custom_splitnormals_clear()
        mesh.use_auto_smooth = True
        mesh.auto_smooth_angle = math.radians(85)