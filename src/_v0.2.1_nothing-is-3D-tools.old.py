

def Nthg3DMeshStats():
    # thanks to sambler for some piece of code https://github.com/sambler/addonsByMe/blob/master/mesh_summary.py

    totalTriInSelection = 0
    totalVertsInSelection = 0
    meshesStats = []
    totalStats = 0

    # test only selected meshes
    selectedMeshes = [o for o in bpy.context.selected_objects if o.type == 'MESH']

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
            # or oops, ngon here, alert!
            else:
                triCount += 3
                hasNGon = True
        # adding element stats to total count
        totalTriInSelection += triCount
        totalVertsInSelection += len(element.data.vertices)
        # generate table
        currentMeshStats = [element.name, len(element.data.vertices), triCount, hasNGon]
        meshesStats.append(currentMeshStats)
        totalStats = [totalVertsInSelection, totalTriInSelection]
    return meshesStats, totalStats


class Nthg3DStatsPanel(bpy.types.Panel):
    bl_label = "Stats"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Nthg is 3D"

    def draw(self, context):
        layout = self.layout

        statsTable, totalStatsTable = Nthg3DMeshStats()

        box = layout.box()
        row = box.row(align = True)
        row.label(text = "Object")
        row.label(text = "Verts")
        row.label(text = "Tris")
        if statsTable is not None:
            for obj in statsTable:
                row = box.row(align = True)
                row.operator("nothing3d.make_object_active", text=str(obj[0]), emboss=False).mesh_to_select = obj[0]
                row.label(text = str(obj[1]))
                if not obj[3]:
                    row.label(text = str(obj[2]))
                else:
                    # visual indicator if ngon
                    row.label(text = "± %i" % (obj[2]))
        # show total stats
        row = box.row(align = True)
        row.label(text = "TOTAL")
        if totalStatsTable != 0:
            row.label(text = "%i" % (totalStatsTable[0]))
            row.label(text = "%i" % (totalStatsTable[1]))
        else:
            row.label(text = "-")
            row.label(text = "-")

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
