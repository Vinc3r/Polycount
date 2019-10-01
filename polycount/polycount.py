import bpy, bmesh, datetime
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

# polycount have to be accessible from anywhere
objects_polycount, total_polycount = [], []

last_user_refresh = "never"


def calculate_mesh_polycount():
    # thanks to sambler for some piece of code https://github.com/sambler/addonsByMe/blob/master/mesh_summary.py

    # using global variables
    global objects_polycount
    global total_polycount
    global last_user_refresh
    # and reset the table
    objects_polycount = []
    total_polycount = []

    total_tris_in_selection = 0
    total_verts_in_selection = 0
    total_area = 0

    # calculate only selected objects
    for obj in selection_sets.meshes_in_selection():
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bm.faces.ensure_lookup_table()
        tris_count = len(bm.calc_loop_triangles())
        exceed_16bmesh_buffer_limit = False
        verts_count = len(bm.verts)
        if verts_count > 65535:
            exceed_16bmesh_buffer_limit = True
        has_ngon = False
        area = 0
        for face in bm.faces:
            area += face.calc_area()
            if len(face.edges) > 4:
                has_ngon = True
        area = round(area, 2)
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
            area,
            exceed_16bmesh_buffer_limit
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

    return {'FINISHED'}


class POLYCOUNT_PT_gui(bpy.types.Panel):
    bl_label = "Polycount"
    bl_idname = "POLYCOUNT_PT_gui"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        global last_user_refresh

        row = layout.row()
        row.operator("polycount.user_interaction",
                        text="Refresh (last: {})".format(last_user_refresh), icon="FILE_REFRESH")
        # polycount_table, total_polycount_table = calculate_mesh_polycount()
        box = layout.box()
        col_flow = box.column_flow(
            columns=0, align=True)
        row = col_flow.row(align=True)
        polycount_sorting = context.scene.polycount_sorting
        polycount_sorting_reversed = context.scene.polycount_sorting_reversed
        # Object button
        if polycount_sorting == 'NAME':
            if polycount_sorting_reversed:
                row.operator("polycount.user_interaction",
                                text="Object", icon="TRIA_UP").poly_sort = 'NAME'
            else:
                row.operator("polycount.user_interaction",
                                text="Object", icon="TRIA_DOWN").poly_sort = 'NAME'
        else:
            row.operator("polycount.user_interaction",
                            text="Object").poly_sort = 'NAME'
        # Verts button
        if polycount_sorting == 'VERTS':
            if polycount_sorting_reversed:
                row.operator("polycount.user_interaction",
                                text="Verts", icon="TRIA_DOWN").poly_sort = 'VERTS'
            else:
                row.operator("polycount.user_interaction",
                                text="Verts", icon="TRIA_UP").poly_sort = 'VERTS'
        else:
            row.operator("polycount.user_interaction",
                            text="Verts").poly_sort = 'VERTS'
        # Tris button
        if polycount_sorting == 'TRIS':
            if polycount_sorting_reversed:
                row.operator("polycount.user_interaction",
                                text="Tris", icon="TRIA_DOWN").poly_sort = 'TRIS'
            else:
                row.operator("polycount.user_interaction",
                                text="Tris", icon="TRIA_UP").poly_sort = 'TRIS'
        else:
            row.operator("polycount.user_interaction",
                            text="Tris").poly_sort = 'TRIS'
        # Area button
        if polycount_sorting == 'AREA':
            if polycount_sorting_reversed:
                row.operator("polycount.user_interaction",
                                text="Area", icon="TRIA_DOWN").poly_sort = 'AREA'
            else:
                row.operator("polycount.user_interaction",
                                text="Area", icon="TRIA_UP").poly_sort = 'AREA'
        else:
            row.operator("polycount.user_interaction",
                            text="Area").poly_sort = 'AREA'

        if len(objects_polycount) > 0:
            for obj in objects_polycount:
                row = col_flow.row(align=True)
                # show if active
                if context.view_layer.objects.active and context.view_layer.objects.active.name == str(obj[0]):
                    row.operator("polycount.user_interaction",
                                    text=str(obj[0]), depress=True).make_active = obj[0]
                else:
                    row.operator("polycount.user_interaction",
                                    text=str(obj[0]), depress=False).make_active = obj[0]
                # show verts
                if not obj[5]:
                    # no mesh vertex buffer limit
                    row.label(text=str(obj[1]))
                else:
                    row.label(text="%i*" % obj[1])
                # show tri & ngon
                if not obj[3]:
                    # no ngons
                    row.label(text=str(obj[2]))
                else:
                    row.label(text="± %i" % (obj[2]))
                # show area
                row.label(text=str(obj[4]))
        # show total polycount
        box = layout.box()
        row = box.row(align=True)
        row.label(text="Total")
        if len(total_polycount) > 0:
            row.label(text="%i" % (total_polycount[0]))
            row.label(text="%i" % (total_polycount[1]))
            row.label(text="%i" % (total_polycount[2]))
        else:
            row.label(text="0")
            row.label(text="0")
            row.label(text="0")


class POLYCOUNT_OT_user_interaction(bpy.types.Operator):
    bl_idname = "polycount.user_interaction"
    bl_label = "Show polycount in Scene properties panel"
    bl_description = "Show polycount in Scene properties panel"
    make_active: StringProperty()
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
        now = datetime.datetime.now()        
        global last_user_refresh
        last_user_refresh = "{:02d}:{:02d}".format(now.hour, now.minute)

        if self.poly_sort == context.scene.polycount_sorting and self.make_active == "":
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
        if self.make_active is not "":
            context.view_layer.objects.active = bpy.data.objects[str(
                self.make_active)]

        calculate_mesh_polycount()

        return {'FINISHED'}


classes = (
    POLYCOUNT_PT_gui,
    POLYCOUNT_OT_user_interaction,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
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


if __name__ == "__main__":
    register()
