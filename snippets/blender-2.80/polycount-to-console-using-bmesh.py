import bpy
import bmesh
print("+++++++++++++++++")
for obj in bpy.context.selected_objects:    
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    has_ngon = False
    area = 0
    for face in bm.faces:
        area += face.calc_area()
        if len(face.edges) > 4:
            has_ngon = True
    print(obj.name)
    tri = len(bm.calc_loop_triangles())
    faces = len(bm.faces)
    print("  verts: ",len(bm.verts))
    print("  tri: ", tri)
    print("  faces: ", faces)
    print("  ngon: {}".format(has_ngon))
    print("  area: {}".format(round(area,1)))
    bm.free()