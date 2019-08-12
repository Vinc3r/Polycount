import bpy

curves = [c for c in bpy.context.selected_objects if c.type == 'CURVE']

for c in curves:
    c.data.bevel_object = None