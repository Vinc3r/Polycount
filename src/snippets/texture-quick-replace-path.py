import bpy
import os

D = bpy.data

"""
    This little script quicly update images path.
    In this example we tell Blender to use the A: drive instead of network path.
"""

for img in D.images:
    img.filepath = img.filepath.replace("\\\\my-network-path-example", "A:")
    
