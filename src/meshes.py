import bpy
import math
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


def transfer_names():
    # handling active object
    user_active = bpy.context.view_layer.objects.active
    is_user_in_edit_mode = False
    if bpy.context.view_layer.objects.active.mode == 'EDIT':
        is_user_in_edit_mode = True
        bpy.ops.object.mode_set(mode='OBJECT')

    # function core
    objects_selected = selection_sets.meshes_in_selection()
    for obj in objects_selected:
        bpy.context.view_layer.objects.active = obj
        mesh = obj.data
        mesh.name = obj.name

    # handling active object
    bpy.context.view_layer.objects.active = user_active
    if is_user_in_edit_mode:
        bpy.ops.object.mode_set(mode='EDIT')

    return {'FINISHED'}


def set_autosmooth(user_angle):
    # handling active object
    user_active = bpy.context.view_layer.objects.active
    is_user_in_edit_mode = False
    if bpy.context.view_layer.objects.active.mode == 'EDIT':
        is_user_in_edit_mode = True
        bpy.ops.object.mode_set(mode='OBJECT')

    # function core
    objects_selected = selection_sets.meshes_in_selection()
    for obj in objects_selected:
        bpy.context.view_layer.objects.active = obj
        mesh = obj.data
        if mesh.has_custom_normals:
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
        mesh.use_auto_smooth = True
        mesh.auto_smooth_angle = math.radians(user_angle)
        bpy.ops.object.shade_smooth()

    # handling active object
    bpy.context.view_layer.objects.active = user_active
    if is_user_in_edit_mode:
        bpy.ops.object.mode_set(mode='EDIT')

    return {'FINISHED'}


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
        row = layout.row(align=True)
        row.operator("nothing3d.mesh_set_autosmooth", text="Set autosmooth")
        row.prop(context.scene, "autosmooth_angle", text="", slider=True)


class NTHG3D_OT_mesh_transfer_names(bpy.types.Operator):
    bl_idname = "nothing3d.mesh_transfer_names"
    bl_label = "Copy Object name to its Data name"
    bl_description = "Copy Object name to its Data name"

    @classmethod
    def poll(cls, context):
        return len(context.view_layer.objects) > 0

    def execute(self, context):
        transfer_names()
        return {'FINISHED'}


class NTHG3D_OT_mesh_set_autosmooth(bpy.types.Operator):
    bl_idname = "nothing3d.mesh_set_autosmooth"
    bl_label = "Set autosmooth to 85° and delete custom normals"
    bl_description = "Set autosmooth to 85° and delete custom normals"

    @classmethod
    def poll(cls, context):
        return len(context.view_layer.objects) > 0

    def execute(self, context):
        set_autosmooth(context.scene.autosmooth_angle)
        return {'FINISHED'}


classes = (
    NTHG3D_PT_mesh_panel,
    NTHG3D_OT_mesh_transfer_names,
    NTHG3D_OT_mesh_set_autosmooth,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    Scene.autosmooth_angle = FloatProperty(
        name="autosmooth angle",
        description="autosmooth angle",
        default=85.0,
        min=0.0,
        max=180.0,
    )


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del Scene.autosmooth_angle


if __name__ == "__main__":
    register()
