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
        row = layout.row()
        row.operator("nothing3d.mesh_transfer_names", text="Transfer names")
        row = layout.row()
        row.operator("nothing3d.mesh_set_autosmooth", text="Set autosmooth")


class NTHG3D_OT_mesh_transfer_names(bpy.types.Operator):
    bl_idname = "nothing3d.mesh_transfer_names"
    bl_label = "Copy Object name to its Data name"
    bl_description = "Copy Object name to its Data name"

    @classmethod
    def poll(cls, context):
        return context.view_layer.objects.active.mode == 'OBJECT'

    def execute(self, context):
        meshes.transfer_names()
        return {'FINISHED'}


class NTHG3D_OT_mesh_set_autosmooth(bpy.types.Operator):
    bl_idname = "nothing3d.mesh_set_autosmooth"
    bl_label = "Set autosmooth to 85° and delete custom normals"
    bl_description = "Set autosmooth to 85° and delete custom normals"

    @classmethod
    def poll(cls, context):
        return context.view_layer.objects.active.mode == 'OBJECT'

    def execute(self, context):
        meshes.set_autosmooth()
        return {'FINISHED'}


class NTHG3D_PT_material_panel(bpy.types.Panel):
    bl_idname = "NTHG3D_PT_material_panel"
    bl_label = "Materials"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Nothing-is-3D"

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        row = box.row(align=True)
        row.label(text="BackFace:")
        row.operator("nothing3d.material_backface", text="on").toogle = True
        row.operator("nothing3d.material_backface", text="off").toogle = False


class NTHG3D_OT_material_backface(bpy.types.Operator):
    bl_idname = "nothing3d.material_backface"
    bl_label = "Turn backFaceCulling on/off"
    bl_description = "Turn backFaceCulling on/off"
    toogle: BoolProperty()

    def execute(self, context):
        materials.set_backface_culling(self.toogle)
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
            row.operator("nothing3d.stats_panel_table", text="Enable", depress=False).show_stats = True
        else:
            row = layout.row()
            row.operator("nothing3d.stats_panel_table", text="Disable", depress=True).show_stats = False
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
                        row.operator("nothing3d.stats_panel_table", text=str(obj[0]), depress=True).mesh_to_select = \
                            obj[0]
                    else:
                        row.operator("nothing3d.stats_panel_table", text=str(obj[0]), depress=False).mesh_to_select = \
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
        row.operator("nothing3d.uv_activate_channel", text="1").channel = 0
        row.operator("nothing3d.uv_activate_channel", text="2").channel = 1
        row = layout.row(align=True)
        row.operator("nothing3d.uv_rename_channel", text="Rename channels")
        row = layout.row(align=True)
        row.operator("nothing3d.uv_report_none", text="Report no UV")


class NTHG3D_OT_uv_activate_channel(bpy.types.Operator):
    bl_idname = "nothing3d.uv_activate_channel"
    bl_label = "Set active UV"
    bl_description = "Set active UV"
    channel: IntProperty()

    def execute(self, context):
        uvs.activate_uv_channels(self.channel)
        return {'FINISHED'}

class NTHG3D_OT_uv_rename_channel(bpy.types.Operator):
    bl_idname = "nothing3d.uv_rename_channel"
    bl_label = "Normalize UV channels naming"
    bl_description = "Normalize UV channels naming (UVMap, then UV2, UV3...)"

    def execute(self, context):
        uvs.rename_uv_channels()
        return {'FINISHED'}

class NTHG3D_OT_uv_report_none(bpy.types.Operator):
    bl_idname = "nothing3d.uv_report_none"
    bl_label = "Report object without UV chan"
    bl_description = "Report object without UV chan, both in console and Info editor"

    @classmethod
    def poll(cls, context):
        return context.view_layer.objects.active.mode == 'OBJECT'

    def execute(self, context):
        uvs.report_no_uv(self)
        return {'FINISHED'}


classes = (
    NTHG3D_PT_mesh_panel,
    NTHG3D_OT_mesh_transfer_names,
    NTHG3D_OT_mesh_set_autosmooth,
    NTHG3D_PT_material_panel,
    NTHG3D_OT_material_backface,
    NTHG3D_PT_stats_panel,
    NTHG3D_OT_stats_panel_table,
    NTHG3D_PT_uv_panel,
    NTHG3D_OT_uv_activate_channel,
    NTHG3D_OT_uv_rename_channel,
    NTHG3D_OT_uv_report_none,
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
