import bpy
import bmesh
print("+++++++++++++++++")
for obj in bpy.context.view_layer.objects:    
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    has_ngon = False
    area = 0
    for face in bm.faces:
        area += face.calc_area()
        if len(face.edges) > 4:
            has_ngon = True
    verts = len(bm.verts)
    tri = len(bm.calc_loop_triangles())
    faces = len(bm.faces)
    area = round(area,1)
    polycount = [verts, tri, faces, has_ngon, area]
    print(obj.name)
    print("  verts: {}".format(polycount[0]))
    print("  tri: {}".format(polycount[1]))
    print("  faces: {}".format(polycount[2]))
    print("  ngon: {}".format(polycount[3]))
    print("  area: {}".format(polycount[4]))
    bm.free()