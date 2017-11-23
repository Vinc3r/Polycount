import bpy

print("++++++")

print(bpy.context.scene.render.engine)

def assign_lightmap():
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH' and obj.data.uv_textures[1] is not None:
            for mat in obj.data.materials:
                for tex in mat.texture_slots:
                    if tex is not None:
                        print(tex)
                        
assign_lightmap()
