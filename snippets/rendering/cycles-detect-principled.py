import bpy

for obj in bpy.context.selected_objects:
    for mat in obj.data.materials:
        if mat.use_nodes:
            if mat.node_tree.nodes[1].type == 'BSDF_PRINCIPLED':
                print("material {} use Principled".format(mat.name))
                if mat.node_tree.nodes[1].inputs['Base Color'].is_linked:
                    print("   and have a texture")
            else:                
               print("/!\ material {} doesn't use Principled".format(mat.name))
        else:
           print("/!\ material {} doesn't use node".format(mat.name))