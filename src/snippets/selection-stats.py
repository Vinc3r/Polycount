import bpy
#import bmesh

# thanks to sambler for some piece of code https://github.com/sambler/addonsByMe/blob/master/mesh_summary.py

class tmpPanel(bpy.types.Panel):
    bl_label = "tmpPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Addons"

    def draw(self, context):
        layout = self.layout

        scriptBox = layout.box()
        row = scriptBox.row(align = True)
        row.label(text = "Object")
        row.label(text = "Verts")
        row.label(text = "Tris")

        # test only meshes
        selectedMeshes = [o for o in bpy.context.selected_objects if o.type == 'MESH']
        
        totalTriInSelection = 0
        totalVertsInSelection = 0

        for element in selectedMeshes:
            triCount = 0
            hasNGon = False
            for poly in element.data.polygons:
                # first check if quad
                if len(poly.vertices) == 4:
                    triCount += 2
                # or tri
                elif len(poly.vertices) == 3:
                    triCount += 1
                # or oops, ngon here, alert !
                else:
                    triCount += 3
                    hasNGon = True
            # adding element stats to total count
            totalTriInSelection += triCount
            totalVertsInSelection += len(element.data.vertices)
            # generate table
            row = scriptBox.row(align = True)
            row.label(text = "%s" % (element.name))
            row.label(text = "%i " % (len(element.data.vertices)))
            if not hasNGon:
                row.label(text = "%i" % (triCount))
            else:
                # visual indicator if ngon
                row.label(text = "± %i" % (triCount))
        # show total stats                
        scriptBox.row().separator() 
        row = scriptBox.row(align = True)
        row.label(text = "TOTAL")
        row.label(text = "%i" % (totalVertsInSelection))
        row.label(text = "%i" % (totalTriInSelection))

           # scriptBox.label(text = "%s - %i VERTS - %i FACES" % (element.data.name, len(element.data.vertices), len(element.data.polygons)))
           # bpy.data.meshes.remove(tempMesh, True)
           # bm = bmesh.new()
           # bm.from_object(mo[0], context.scene)
           # scriptBox.label(text="("+us(len(bm.verts))+")")
           # bm.free()

def register():
    bpy.utils.register_class(tmpPanel)

def unregister():
    bpy.utils.unregister_class(tmpPanel)

if __name__ == "__main__":
    register()