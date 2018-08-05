import bpy

mat = bpy.data.materials.get("cycles_default")
if mat is None:
    # create material
    mat = bpy.data.materials.new(name="cycles_default")

for obj in bpy.context.selected_objects:
    for matslot in obj.material_slots:
        # options are 'DATA' or 'OBJECT'
        matslot.link = 'OBJECT'
        matslot.material = mat