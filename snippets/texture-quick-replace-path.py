import bpy
import os

D = bpy.data

"""
    This little script quicly update images path.
    In this example we tell Blender to use the A: drive instead of network path.
"""

wrongPath = r"\\my-wrong-path"
correctPath = r"//textures"

print("+++ path correction +++")

for img in D.images:
    img.filepath = img.filepath.replace(wrongPath, correctPath)

# check in the console what's rest to fix
for img in D.images:
    if not img.filepath.startswith(correctPath):        
        print("wrong path: {} {}".format(img.name, img.filepath))