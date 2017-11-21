import bpy
import os

# yep, that's ugly code

D = bpy.data

for img in D.images:
    if ".emit" in img.name:
        print("removed file emit "+str(img.name))
        # delete image, unlink it
        D.images.remove(img, True)
        
    elif ".LM" in img.name:
        print("removed file LM "+str(img.name))
        D.images.remove(img, True)
        
    elif "AO_" in img.name:
        print("removed file AO "+str(img.name))
        D.images.remove(img, True)

for img in D.textures:
    if ".emit" in img.name:
        print("removed texture emit "+str(img.name))
        D.textures.remove(img, True)
        
    elif ".LM" in img.name:
        print("removed texture LM "+str(img.name))
        D.textures.remove(img, True)
        
    elif "AO_" in img.name:
        print("removed texture AO "+str(img.name))
        D.textures.remove(img, True)
