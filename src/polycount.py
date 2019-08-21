import bpy
import bmesh
from . import selection_sets
from bpy.types import Scene
from bpy.props import (
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
    BoolProperty,
    IntProperty,
    StringProperty
)


def calculate_mesh_polycount():
    # thanks to sambler for some piece of code https://github.com/sambler/addonsByMe/blob/master/mesh_summary.py

    total_tris_in_selection = 0
    total_verts_in_selection = 0
    objects_polycount = []
    total_polycount = 0
    total_area = 0

    # calculate only selected objects
    for obj in selection_sets.meshes_in_selection():
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bm.faces.ensure_lookup_table()
        tris_count = len(bm.calc_loop_triangles())
        verts_count = len(bm.verts)
        has_ngon = False
        area = 0
        for face in bm.faces:
            area += face.calc_area()
            if len(face.edges) > 4:
                has_ngon = True
        area = round(area, 1)
        # adding obj polycount to total count
        total_tris_in_selection += tris_count
        total_verts_in_selection += verts_count
        total_area += area
        # generate table
        objects_polycount.append([
            obj.name,
            verts_count,
            tris_count,
            has_ngon,
            area
        ])
        bm.free()
    total_polycount = [total_verts_in_selection,
                       total_tris_in_selection, total_area]

    def sortList(item):
        polycount_sorting = bpy.context.scene.polycount_sorting
        if polycount_sorting == 'TRIS':
            # check default first
            return item[2]
        elif polycount_sorting == 'NAME':
            return item[0].casefold()
        elif polycount_sorting == 'VERTS':
            return item[1]
        elif polycount_sorting == 'AREA':
            return item[4]
        else:
            # tris by default
            return item[2]
    objects_polycount.sort(
        key=sortList, reverse=bpy.context.scene.polycount_sorting_reversed)

    return objects_polycount, total_polycount


class NTHG3D_PT_polycount_panel(bpy.types.Panel):
    bl_label = "Polycount"
    bl_idname = "NTHG3D_PT_polycount_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        if not scene.is_polycount_enable:
            # show enable button
            row = layout.row()
            row.operator("nothing3d.polycount_panel_table",
                         text="Enable", depress=False).show_polycount = True
        else:
            row = layout.row()
            row.operator("nothing3d.polycount_panel_table",
                         text="Disable", depress=True).show_polycount = False
            polycount_table, total_polycount_table = calculate_mesh_polycount()
            box = layout.box()
            col_flow = box.column_flow(
                columns=0, align=True)
            row = col_flow.row(align=True)
            # row.label(text="Object")
            row.operator("nothing3d.polycount_panel_table",
                         text="Object").poly_sort = 'NAME'
            # row.label(text="Verts")
            row.operator("nothing3d.polycount_panel_table",
                         text="Verts").poly_sort = 'VERTS'
            # row.label(text="Tris")
            row.operator("nothing3d.polycount_panel_table",
                         text="Tris").poly_sort = 'TRIS'
            # row.label(text="Area")
            row.operator("nothing3d.polycount_panel_table",
                         text="Area").poly_sort = 'AREA'
            if len(polycount_table) > 0:
                for obj in polycount_table:
                    row = col_flow.row(align=True)
                    # show if active
                    if context.view_layer.objects.active.name == str(obj[0]):
                        row.operator("nothing3d.polycount_panel_table",
                                     text=str(obj[0]), depress=True).mesh_to_select = obj[0]
                    else:
                        row.operator("nothing3d.polycount_panel_table",
                                     text=str(obj[0]), depress=False).mesh_to_select = obj[0]
                    # show verts
                    row.label(text=str(obj[1]))
                    # show tri & ngon
                    if not obj[3]:
                        row.label(text=str(obj[2]))
                    else:
                        row.label(text="± %i" % (obj[2]))
                    row.label(text=str(obj[4]))
            # show total polycount
            box = layout.box()
            row = box.row(align=True)
            row.label(text="Total")
            if len(total_polycount_table) > 0:
                row.label(text="%i" % (total_polycount_table[0]))
                row.label(text="%i" % (total_polycount_table[1]))
                row.label(text="%i" % (total_polycount_table[2]))
            else:
                row.label(text="-")
                row.label(text="-")
                row.label(text="-")


class NTHG3D_OT_polycount_panel_table(bpy.types.Operator):
    bl_idname = "nothing3d.polycount_panel_table"
    bl_label = "Show polycount in Scene properties panel"
    bl_description = "Show polycount in Scene properties panel"
    show_polycount: BoolProperty(default=True)
    mesh_to_select: StringProperty()
    poly_sort: EnumProperty(items=[
        ('NAME', "Name", ""),
        ('VERTS', "Verts", ""),
        ('TRIS', "Tris", ""),
        ('AREA', "Area", "")
    ], default='TRIS')

    @classmethod
    def poll(cls, context):
        return len(context.view_layer.objects) > 0 and \
            bpy.context.view_layer.objects.active and \
            bpy.context.view_layer.objects.active.mode == 'OBJECT'

    def execute(self, context):
        context.scene.is_polycount_enable = self.show_polycount
        if self.poly_sort == context.scene.polycount_sorting:
            # user can toogle sorting by clicking multiple times on button
            context.scene.polycount_sorting_reversed = not context.scene.polycount_sorting_reversed
        else:
            # switching the sort key
            if self.poly_sort == 'NAME':
                # user expect naming sort starting from a to b
                context.scene.polycount_sorting_reversed = False
            else:
                # but numbers starting from higher to lower
                context.scene.polycount_sorting_reversed = True
            context.scene.polycount_sorting = self.poly_sort
        if self.mesh_to_select is not "":
            context.view_layer.objects.active = bpy.data.objects[str(
                self.mesh_to_select)]

        return {'FINISHED'}


classes = (
    NTHG3D_PT_polycount_panel,
    NTHG3D_OT_polycount_panel_table,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    Scene.is_polycount_enable = BoolProperty(default=False)
    Scene.polycount_sorting = EnumProperty(items=[
        ('NAME', "Name", ""),
        ('VERTS', "Verts", ""),
        ('TRIS', "Tris", ""),
        ('AREA', "Area", "")
    ], default='TRIS')
    Scene.polycount_sorting_reversed = BoolProperty(default=True)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del Scene.polycount_sorting_reversed
    del Scene.polycount_sorting
    del Scene.is_polycount_enable


if __name__ == "__main__":
    register()
