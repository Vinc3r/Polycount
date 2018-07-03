import bpy

print("+++ SWITCH MATERIALS LINK TYPE +++")

objList = [o for o in bpy.context.scene.objects if o.type == 'MESH' and o.material_slots]


def switch_materials_link_type(switchType, overwriteMaterial):
    
    """ Data link is the default type.
            switchType == True: switch materials from Data to Object link.
            switchType == False: switch materials from Object to Data link.
            
            overwriteMaterial == True: copy the material from the current link type to the current
            overwriteMaterial == False: keep the slot data as it is
    """
    
    for obj in objList:
        for matSlot in obj.material_slots:
            currentMaterial = matSlot.material
    
            # link: Data > Object
            if switchType:
                if matSlot.link == 'OBJECT':
                    matConsoleName = "UNNAMED"
                    if currentMaterial is not None:
                        matConsoleName = currentMaterial.name
                    print(">>> already on OBJECT link type for {} on {}".format(matConsoleName, obj.name))
                if matSlot.link == 'DATA':
                    matSlot.link = 'OBJECT'
                    if overwriteMaterial:
                        matSlot.material = currentMaterial
                    
            # link: Object > Data (= equal default value)
            elif not switchType:
                if matSlot.link == 'DATA':
                    matConsoleName = "UNNAMED"
                    if currentMaterial is not None:
                        matConsoleName = currentMaterial.name
                    print(">>> already on DATA link type for {} on {}".format(matConsoleName, obj.name))
                if matSlot.link == 'OBJECT':
                    matSlot.link = 'DATA'
                    if overwriteMaterial:
                        matSlot.material = currentMaterial
        
    print("> switch is done")
    
switch_materials_link_type(False, False)