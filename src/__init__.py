bl_info = {
    "name": "Nothing-is-3D tools",
    "description": "Some scripts 3D realtime workflow oriented.",
    "author": "Vincent (V!nc3r) Lamy",
    "category": "Object",
    "wiki_url": 'https://github.com/Vinc3r/BlenderScripts',
    "tracker_url": 'https://github.com/Vinc3r/BlenderScripts/issues',
    "version": (1, 1, 0),
    "blender": (2, 80, 0)
}

"""A bunch of Thanks for some snippets, ideas, inspirations, to:
    - of course, Ton & all Blender devs,
    - Henri Hebeisen (henri-hebeisen.com), Pitiwazou (pitiwazou.com), Pistiwique (github.com/pistiwique),
    - and finally all Blender community and the ones I forget.
"""

if "bpy" in locals():
    print("---- DEBUG HELP LINE ----")
    import importlib

    importlib.reload(selection_sets)
    importlib.reload(meshes)
    importlib.reload(materials)
    importlib.reload(stats)
    importlib.reload(uvs)
else:
    from . import selection_sets, meshes, materials, stats, uvs

import bpy
from bpy.types import (
    Scene,
)
from bpy.props import (
    FloatVectorProperty,
    IntProperty,
    BoolProperty,
    StringProperty,
    FloatProperty,
    EnumProperty,
)


class NTHG3D_PT_mesh_panel(bpy.types.Panel):
    bl_label = "Meshes"
    bl_idname = "NTHG3D_PT_mesh_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Nothing-is-3D"

    def draw(self, context):
        layout = self.layout
        # Object to Data naming
        row = layout.row()
        row.operator("nothing3d.mesh_panel_buttons", text="Transfer names").action = "transfer_names"


class NTHG3D_OT_mesh_panel_buttons(bpy.types.Operator):
    bl_idname = "nothing3d.mesh_panel_buttons"
    bl_label = "Buttons in Meshes panel"
    action: StringProperty()

    def execute(self, context):
        if self.action == "transfer_names":
            meshes.mesh_transfer_names()
        return {'FINISHED'}


class NTHG3D_PT_material_panel(bpy.types.Panel):
    bl_label = "Materials"
    bl_idname = "NTHG3D_PT_material_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Nothing-is-3D"

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        row = box.row(align=True)
        row.label(text="BackFace:")
        row.operator("nothing3d.material_panel_buttons", text="on").action = "bfc_on"
        row.operator("nothing3d.material_panel_buttons", text="off").action = "bfc_off"


class NTHG3D_OT_material_panel_buttons(bpy.types.Operator):
    bl_idname = "nothing3d.material_panel_buttons"
    bl_label = "Buttons in Materials panel"
    action: StringProperty()

    def execute(self, context):
        if self.action == "bfc_on":
            materials.set_backface_culling(True)
        if self.action == "bfc_off":
            materials.set_backface_culling(False)
        return {'FINISHED'}


class NTHG3D_PT_stats_panel(bpy.types.Panel):
    bl_label = "Stats"
    bl_idname = "NTHG3D_PT_stats_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"

    def draw(self, context):
        scene = context.scene

        layout = self.layout

        if scene.are_stats_enabled == False:
            row = layout.row()
            row.operator("nothing3d.stats_panel_buttons", text="Enable", depress=False).show_stats = True
        else:
            row = layout.row()
            row.operator("nothing3d.stats_panel_buttons", text="Disable", depress=True).show_stats = False
            stats_table, total_stats_table = stats.calculate_mesh_stats()
            box = layout.box()
            row = box.row(align=True)
            row.label(text="Object")
            row.label(text="Verts")
            row.label(text="Tris")
            if stats_table is not None:
                for obj in stats_table:
                    row = box.row(align=True)
                    if context.view_layer.objects.active.name == str(obj[0]):
                        row.operator("nothing3d.stats_panel_buttons", text=str(obj[0]), depress=True).mesh_to_select = \
                        obj[0]
                    else:
                        row.operator("nothing3d.stats_panel_buttons", text=str(obj[0]), depress=False).mesh_to_select = \
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


class NTHG3D_OT_stats_panel_buttons(bpy.types.Operator):
    bl_idname = "nothing3d.stats_panel_buttons"
    bl_label = "Buttons in Stats panel"
    show_stats: BoolProperty()
    mesh_to_select: StringProperty()

    def execute(self, context):
        scene = context.scene
        if self.show_stats == True:
            scene.are_stats_enabled = True
        if self.show_stats == False:
            scene.are_stats_enabled = False
        if self.mesh_to_select is not "":
            context.view_layer.objects.active = bpy.data.objects[str(self.mesh_to_select)]
        return {'FINISHED'}


class NTHG3D_PT_uv_panel(bpy.types.Panel):
    bl_label = "UVs"
    bl_idname = "NTHG3D_PT_uv_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Nothing-is-3D"

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.label(text="Active:")
        row.operator("nothing3d.uv_panel_buttons", text="1").action = "select_UV1"
        row.operator("nothing3d.uv_panel_buttons", text="2").action = "select_UV2"
        row = layout.row(align=True)
        row.operator("nothing3d.uv_panel_buttons", text="Rename channels").action = "rename_UV"
        row = layout.row(align=True)
        row.operator("nothing3d.uv_panel_buttons", text="Report no UV").action = "report_no_UV"


class NTHG3D_OT_uv_panel_buttons(bpy.types.Operator):
    bl_idname = "nothing3d.uv_panel_buttons"
    bl_label = "Buttons in UVs panel"
    action: StringProperty()

    def execute(self, context):
        if self.action == "rename_UV":
            uvs.rename_uv_channels()
        if self.action == "select_UV1":
            uvs.activate_uv_channels(0)
        if self.action == "select_UV2":
            uvs.activate_uv_channels(1)
        if self.action == "report_no_UV":
            uvs.report_no_uv(self)
        return {'FINISHED'}


classes = (
    NTHG3D_PT_mesh_panel,
    NTHG3D_OT_mesh_panel_buttons,
    NTHG3D_PT_material_panel,
    NTHG3D_OT_material_panel_buttons,
    NTHG3D_PT_stats_panel,
    NTHG3D_OT_stats_panel_buttons,
    NTHG3D_PT_uv_panel,
    NTHG3D_OT_uv_panel_buttons,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    Scene.are_stats_enabled = BoolProperty(
        name="Enable Statistics",
        description="Are stats enabled or not?",
        default=False)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del Scene.are_stats_enabled


if __name__ == "__main__":
    register()
