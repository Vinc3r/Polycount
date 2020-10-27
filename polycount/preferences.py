import bpy
from bpy.props import (
    BoolProperty
)


class POLYCOUNT_PT_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    show_verts: BoolProperty(
        name="Compute vertices count",
        default=True,
    )
    show_tris: BoolProperty(
        name="Compute triangles count",
        default=True,
    )
    show_area: BoolProperty(
        name="Compute area count",
        default=True,
    )
    trim_numbers: BoolProperty(
        name="Trim large numbers",
        default=True,
    )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Show only:")
        row.prop(self, "show_verts", text="Verts")
        row.prop(self, "show_tris", text="Tri")
        row.prop(self, "show_area", text="Area")
        row = layout.row()
        row.prop(self, "trim_numbers", text="Trim large numbers")


classes = (
    POLYCOUNT_PT_Preferences,
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
