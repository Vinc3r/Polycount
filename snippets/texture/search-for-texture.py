import bpy
import os

D = bpy.data

"""
    This little script show in the Blender console textures paths 
    that not conform to the reference one.
"""

searchPath = r"partOfTextureName"

print("+++ search paths +++")

for img in D.images:
    if img.filepath.endswith(searchPath) or img.name.endswith(searchPath):
        print("found {} {}".format(img.name, img.filepath))
        
print("---")
        
for mat in bpy.data.materials:
    if mat.node_tree is not None and len(mat.node_tree.nodes) > 0:
        nodes = mat.node_tree.nodes
        for node in nodes:
            if type(node).__name__ == "ShaderNodeTexImage":
                for out in node.outputs:
                    text_img = node.image
                    if text_img is not None and searchPath in text_img.filepath:
                        print("found on: {} > {} {}".format(mat.name, text_img.name, text_img.filepath))