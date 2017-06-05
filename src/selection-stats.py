import bpy
import bmesh

#thanks to https://github.com/sambler/addonsByMe/blob/master/mesh_summary.py for some piece of code



class tmpPanel(bpy.types.Panel):
    bl_label = "tmpPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Addons"

    def draw(self, context):
        layout = self.layout

        scriptBox = layout.box()
        scriptBox.label(text = "scriptBox")
        row = scriptBox.row(align = True)
        row.label(text = "Object")
        row.label(text = "Verts")
        row.label(text = "Tris")
        
        selectedMeshes = [o for o in bpy.context.selected_objects if o.type == 'MESH']
        
        for element in selectedMeshes:
            triCount = 0
            for poly in element.data.polygons:
                if len(poly.vertices) == 3:
                    triCount += 1
                if len(poly.vertices) == 4:
                    triCount += 2
            row = scriptBox.row(align = True)
            row.label(text = "%s" % (element.data.name))
            row.label(text = "%i " % (len(element.data.vertices)))
            row.label(text = "%i" % (triCount))
                  
           # scriptBox.label(text = "%s - %i VERTS - %i FACES" % (element.data.name, len(element.data.vertices), len(element.data.polygons)))
          #  bpy.data.meshes.remove(tempMesh, True)
          #  bm = bmesh.new()
           # bm.from_object(mo[0], context.scene)
          #  scriptBox.label(text="("+us(len(bm.verts))+")")
           # bm.free()
        

def register():
    bpy.utils.register_class(tmpPanel)

def unregister():
    bpy.utils.unregister_class(tmpPanel)

if __name__ == "__main__":
    register()
