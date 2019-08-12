import bpy
import os

D = bpy.data

pattern = ".LM"

print("+++ remove texture files +++")

for img in D.images:
    if pattern in img.name:
        print("removed file "+str(img.name))
        D.images.remove(img, True)

for img in D.textures:
    if pattern in img.name:
        print("removed texture "+str(img.name))
        D.textures.remove(img, True)
