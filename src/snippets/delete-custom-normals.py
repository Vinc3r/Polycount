import bpy
import math

"""
    This batch custom normal deletion on selected objects, and also activate autosmooth with 85°
"""

print("+++++ DELETE Normals Custom Data +++++")

objects = [o for o in bpy.context.selected_objects if o.type == 'MESH']

for obj in objects:
    mesh = obj.data
    if mesh.has_custom_normals:
        bpy.context.scene.objects.active = obj
        bpy.ops.mesh.customdata_custom_splitnormals_clear()
        mesh.use_auto_smooth = True
        mesh.auto_smooth_angle = math.radians(85)