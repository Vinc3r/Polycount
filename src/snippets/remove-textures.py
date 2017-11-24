import bpy
import os

D = bpy.data

pattern = "AO_"

for img in D.images:
    if pattern in img.name:
        print("removed file AO "+str(img.name))
        D.images.remove(img, True)

for img in D.textures:
    if pattern in img.name:
        print("removed texture AO "+str(img.name))
        D.textures.remove(img, True)
