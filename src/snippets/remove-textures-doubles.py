import bpy

print("++++ remove textures doubles ++++")

def remove_textures_doubles():
    
    single_img_instance = []
    D = bpy.data

    # check all images
    for i in D.images:
        # first considering img not already used
        is_already_in_list = False
        # of course, we need to start with a list containing some shit
        if single_img_instance == []:
            single_img_instance.append(i.filepath)
            is_already_in_list = True
        # ask if img is already used
        for img in single_img_instance:
            if i.filepath == img:
                # ach nein! img already used!
                is_already_in_list = True
        if not is_already_in_list:
           # lets add to the list
           single_img_instance.append(i.filepath)
        
    print(single_img_instance)
    
    if bpy.context.scene.render.engine == "BLENDER_RENDER":
        print("porut")
    elif bpy.context.scene.render.engine == 'CYCLES':
        print("Cycles not (yet) supported")
    else:
        print("render engine not supported")
        
remove_textures_doubles()