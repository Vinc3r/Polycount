import bpy

class tmpPanel(bpy.types.Panel):
    bl_label = "tmpPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Addons"

    def draw(self, context):
        layout = self.layout

        scriptBox = layout.box()
        scriptBox.label(text = "scriptBox")
        

def register():
    bpy.utils.register_class(tmpPanel)

def unregister():
    bpy.utils.unregister_class(tmpPanel)

if __name__ == "__main__":
    register()
