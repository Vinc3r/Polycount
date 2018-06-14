import bpy

D = bpy.data

"""
    This little script show in the Blender console materials used by
    more than 1 object
"""

print("+++ multiusers materials +++")

for mtl in D.materials:
    if mtl.users > 1:
        print("{} is used by {} objects".format(mtl.name, mtl.users))
