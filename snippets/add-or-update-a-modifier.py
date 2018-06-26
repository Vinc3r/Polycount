import bpy

for obj in bpy.data.objects:
    if obj.type == 'MESH': 
        bpy.context.scene.objects.active = obj
        edgeSplit = None
        if obj.modifiers.get("EdgeSplit"):
            edgeSplit = obj.modifiers.get("EdgeSplit")
        else:
            edgeSplit = obj.modifiers.new("EdgeSplit", type = "EDGE_SPLIT")
        edgeSplit.split_angle = 0
        bpy.context.scene.update()