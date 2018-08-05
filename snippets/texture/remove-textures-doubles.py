import bpy

print("++++ remove textures doubles ++++")

def remove_textures_doubles():
    
    D = bpy.data
    
    if bpy.context.scene.render.engine == "BLENDER_RENDER":
              
        # check all images
        for i in D.images:            
            imgName = i.filepath
            imgNameSplit = imgName.split("/")
            imgName = imgNameSplit[len(imgNameSplit)-1]
            if i.name != imgName:
                i.name = imgName
                
        # now check all texture slots in materials
        for mat in D.materials:
            for texSlot in range(len(mat.texture_slots)):
                activeTexSlot = mat.texture_slots[texSlot]
                if activeTexSlot != None \
                and activeTexSlot.texture.image != None:
                    imgFilePath = activeTexSlot.texture.image.filepath
                    for img in D.images:
                        # if img use the same path
                        # so lets assign it and break the loop
                        if imgFilePath == img.filepath:
                            activeTexSlot.texture.image = img
                            continue                    
        
    elif bpy.context.scene.render.engine == 'CYCLES':
        print("Cycles not (yet) supported")
    else:
        print("render engine not supported")
        
remove_textures_doubles()