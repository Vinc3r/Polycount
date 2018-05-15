import bpy
import os

D = bpy.data

"""
    This little script show in the Blender console textures paths 
    that not conform to the reference one.
"""

correctPath = r"//textures"

print("+++ wrong paths +++")

for img in D.images:
    if not img.filepath.startswith(correctPath):        
        print("wrong path: {} {}".format(img.name, img.filepath))
