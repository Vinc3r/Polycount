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


def set_backface_culling(mode):
    objects_selected = selection_sets.meshes_with_materials()
    for obj in objects_selected:
        for mat in obj.data.materials:
            if mat is not None:
                mat.use_backface_culling = mode
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
        set_backface_culling(self.toogle)

        return {'FINISHED'}


classes = (
    NTHG3D_PT_material_panel,
    NTHG3D_OT_material_backface,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
