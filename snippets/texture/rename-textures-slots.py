import bpy
import os

D = bpy.data

for img in D.images:
	textureFilename = bpy.path.display_name(img.filepath)
	img.name = textureFilename
