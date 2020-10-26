import bpy
from bpy.props import (
    BoolProperty
)


class POLYCOUNT_PT_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    myBool: BoolProperty(
        name="Example Boolean",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="myBool")
        row = layout.row()
        row.prop(self, "myBool", text="this is a test")


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
