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


def set_active_texture(type="albedo"):

    # texture_condition = [node.type, node.output.type, node.output.link.to_node.type]
    # default: albedo
    texture_condition = ['TEX_IMAGE', 'RGBA', 'BSDF_PRINCIPLED']

    objects_selected = selection_sets.meshes_with_materials()

    for obj in objects_selected:
        mesh = obj.data
        for mat in mesh.materials:
            if mat.use_nodes:
                for node in mat.node_tree.nodes:
                    if node.type != texture_condition[0]:
                        # node have to pass first tests
                        continue
                    for out in node.outputs:
                        if out.type != texture_condition[1]:
                            # output have to pass test
                            continue
                        for link in out.links:
                            if link.to_node.type != texture_condition[2]:
                                # link have to pass test
                                continue
                            # ok we're sure about this node, let's make it last selected
                            node.select = False
                            node.select = True
    return {'FINISHED'}


def gltf_mute_textures(exclude="albedo"):

    # no_muting_condition = [node.type, node.output.type, node.output.link.to_node.type]
    # default: albedo
    no_muting_condition = ['TEX_IMAGE', 'RGBA', 'BSDF_PRINCIPLED']
    if exclude == "orm":
        no_muting_condition = ['TEX_IMAGE', 'RGBA', 'SEPRGB']
    elif exclude == "normal":
        no_muting_condition = ['TEX_IMAGE', 'RGBA', 'NORMAL_MAP']
    elif exclude == "emit":
        no_muting_condition = ['TEX_IMAGE', 'RGBA', 'EMISSION']

    objects_selected = selection_sets.meshes_with_materials()

    for obj in objects_selected:
        mesh = obj.data
        for mat in mesh.materials:
            if mat.use_nodes:
                for node in mat.node_tree.nodes:
                    if node.type != no_muting_condition[0]:
                        # node have to pass first tests
                        continue
                    if exclude == "unmute":
                        # in case we jsut want unmuting, no need to go further
                        node.mute = False
                        continue
                    # muting by default, then unmute exception
                    node.mute = True
                    for out in node.outputs:
                        if out.type != no_muting_condition[1]:
                            # output have to pass test
                            continue
                        for link in out.links:
                            if link.to_node.type != no_muting_condition[2]:
                                # link have to pass test
                                continue
                            # ok we're sure about this node, let's unmute
                            node.mute = False
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
        row = box.row(align=True)
        row.label(text="Activate texture:")
        row = box.row(align=True)
        row.operator("nothing3d.material_active_texture",
                     text="albedo").texture_type = "albedo"
        row = layout.row()
        row.label(text="glTF workflow:")
        box = layout.box()
        row = box.row()
        row.label(text="Mute textures except:")
        row = box.row(align=True)
        row.operator("nothing3d.material_gltf_mute",
                     text="albedo").exclude = "albedo"
        row.operator("nothing3d.material_gltf_mute",
                     text="ORM").exclude = "orm"
        row = box.row(align=True)
        row.operator("nothing3d.material_gltf_mute",
                     text="nm").exclude = "normal"
        row.operator("nothing3d.material_gltf_mute",
                     text="emit").exclude = "emit"
        row = box.row(align=True)
        row.operator("nothing3d.material_gltf_mute",
                     text="unmute").exclude = "unmute"
        row = box.row()
        row.label(text="Fix:")
        row.label(text="color space")
        #row.operator("nothing3d.material_todo", text="color space")


class NTHG3D_OT_material_backface(bpy.types.Operator):
    bl_idname = "nothing3d.material_backface"
    bl_label = "Turn backFaceCulling on/off"
    bl_description = "Turn backFaceCulling on/off"
    toogle: BoolProperty()

    def execute(self, context):
        set_backface_culling(self.toogle)
        return {'FINISHED'}


class NTHG3D_OT_material_gltf_mute(bpy.types.Operator):
    bl_idname = "nothing3d.material_gltf_mute"
    bl_label = "Mute textures for baking process"
    bl_description = "Mute textures for baking process"
    exclude: StringProperty()

    def execute(self, context):
        gltf_mute_textures(self.exclude)
        return {'FINISHED'}


class NTHG3D_OT_material_active_texture(bpy.types.Operator):
    bl_idname = "nothing3d.material_active_texture"
    bl_label = "Activate a texture to be shown in viewport Solid Texture mode"
    bl_description = "Activate a texture to be shown in viewport Solid Texture mode"
    texture_type: StringProperty()

    def execute(self, context):
        set_active_texture(self.texture_type)
        return {'FINISHED'}


classes = (
    NTHG3D_PT_material_panel,
    NTHG3D_OT_material_backface,
    NTHG3D_OT_material_gltf_mute,
    NTHG3D_OT_material_active_texture,
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
