import bpy
from . import selection_sets


def calculate_mesh_stats():
    # thanks to sambler for some piece of code https://github.com/sambler/addonsByMe/blob/master/mesh_summary.py

    total_tris_in_selection = 0
    total_verts_in_selection = 0
    meshes_stats = []
    total_stats = 0

    # test only selected meshes
    selected_meshes = selection_sets.meshes_in_selection()

    for element in selected_meshes:
        tris_count = 0
        has_ngon = False
        for poly in element.data.polygons:
            # first check if quad
            if len(poly.vertices) == 4:
                tris_count += 2
            # or tri
            elif len(poly.vertices) == 3:
                tris_count += 1
            # or oops, ngon here, alert!
            else:
                tris_count += 3
                has_ngon = True
        # adding element stats to total count
        total_tris_in_selection += tris_count
        total_verts_in_selection += len(element.data.vertices)
        # generate table
        current_mesh_stats = [element.name, len(
            element.data.vertices), tris_count, has_ngon]
        meshes_stats.append(current_mesh_stats)
        total_stats = [total_verts_in_selection, total_tris_in_selection]

    return meshes_stats, total_stats
