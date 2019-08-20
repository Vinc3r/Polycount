import bpy
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


class NTHG3D_PT_stats_panel(bpy.types.Panel):
    bl_label = "Stats"
    bl_idname = "NTHG3D_PT_stats_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"

    def draw(self, context):
        scene = context.scene

        layout = self.layout

        if not scene.are_stats_enabled:
            row = layout.row()
            row.operator("nothing3d.stats_panel_table",
                         text="Enable", depress=False).show_stats = True
        else:
            row = layout.row()
            row.operator("nothing3d.stats_panel_table",
                         text="Disable", depress=True).show_stats = False
            stats_table, total_stats_table = calculate_mesh_stats()
            box = layout.box()
            row = box.row(align=True)
            row.label(text="Object")
            row.label(text="Verts")
            row.label(text="Tris")
            if stats_table is not None:
                for obj in stats_table:
                    row = box.row(align=True)
                    if context.view_layer.objects.active.name == str(obj[0]):
                        row.operator("nothing3d.stats_panel_table", text=str(obj[0]), depress=True).mesh_to_select = \
                            obj[0]
                    else:
                        row.operator("nothing3d.stats_panel_table", text=str(obj[0]),
                                     depress=False).mesh_to_select = \
                            obj[0]
                    row.label(text=str(obj[1]))
                    if not obj[3]:
                        row.label(text=str(obj[2]))
                    else:
                        # visual indicator if ngon
                        row.label(text="± %i" % (obj[2]))
            # show total stats
            box = layout.box()
            row = box.row(align=True)
            row.label(text="Total")
            if total_stats_table != 0:
                row.label(text="%i" % (total_stats_table[0]))
                row.label(text="%i" % (total_stats_table[1]))
            else:
                row.label(text="-")
                row.label(text="-")


class NTHG3D_OT_stats_panel_table(bpy.types.Operator):
    bl_idname = "nothing3d.stats_panel_table"
    bl_label = "Show Stats in Scene properties panel"
    bl_description = "Show Stats in Scene properties panel"
    show_stats: BoolProperty()
    mesh_to_select: StringProperty()

    @classmethod
    def poll(cls, context):
        return context.view_layer.objects.active.mode == 'OBJECT'

    def execute(self, context):
        context.scene.are_stats_enabled = self.show_stats
        if self.mesh_to_select is not "":
            context.view_layer.objects.active = bpy.data.objects[str(
                self.mesh_to_select)]

        return {'FINISHED'}


classes = (
    NTHG3D_PT_stats_panel,
    NTHG3D_OT_stats_panel_table,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    Scene.are_stats_enabled = BoolProperty()


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del Scene.are_stats_enabled


if __name__ == "__main__":
    register()
