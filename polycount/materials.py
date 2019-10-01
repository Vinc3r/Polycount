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
                            # ok we're sure about this node, let's make it active
                            node.select = True
                            mat.node_tree.nodes.active = node
    return {'FINISHED'}


def gltf_fix_colorspace():
    objects_selected = selection_sets.meshes_with_materials()

    for obj in objects_selected:
        mesh = obj.data
        for mat in mesh.materials:
            if mat.use_nodes:
                for node in mat.node_tree.nodes:
                    if node.type != 'TEX_IMAGE' or not node.image:
                        # node have to pass first tests
                        continue
                    for out in node.outputs:
                        if out.type != 'RGBA':
                            # output have to pass test
                            continue
                        for link in out.links:
                            if link.to_node.type == 'BSDF_PRINCIPLED':
                                node.image.colorspace_settings.name = 'sRGB'
                            else:
                                node.image.colorspace_settings.name = 'Non-Color'
    return {'FINISHED'}

def gltf_fix_uvnode_naming(operator):
    objects_selected = selection_sets.meshes_with_materials()
    materials_error = ""

    for obj in objects_selected:
        mesh = obj.data
        for mat in mesh.materials:
            if mat.use_nodes:
                naming_issue = False
                for node in mat.node_tree.nodes:
                    if node.type != 'UVMAP' or node.uv_map == '':
                        # node have to pass first tests
                        continue
                    # get gltf UV chan id: "TEXCOORD_0" give us "0" as int
                    channel_number = str(node.uv_map)[-1:]
                    try:
                        node.uv_map = obj.data.uv_layers[int(channel_number)].name
                    except:
                        naming_issue = True
                if naming_issue:
                    materials_error += "{}, ".format(mat.name)
    if materials_error != "":
        # removing ", " charz
        operator.report({'WARNING'}, "Can't be parsed: {}".format(materials_error[:-2]))
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
                    if exclude != "mute":
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
        # misc
        box = layout.box()
        row = box.row(align=True)
        # backface culling
        row.label(text="BackFace:")
        row.operator("nothing3d.material_backface", text="On").toogle = True
        row.operator("nothing3d.material_backface", text="Off").toogle = False
        row = box.row(align=True)
        # active texture node
        row.label(text="Activate texture:")
        row = box.row(align=True)
        row.operator("nothing3d.material_active_texture",
                     text="albedo").texture_type = "albedo"
        row = layout.row()
        # glTF workflow
        row.label(text="glTF workflow:")
        box = layout.box()
        row = box.row()
        # muting textures
        row.label(text="Mute textures except:")
        grid = box.grid_flow(
            row_major=True, even_columns=True, even_rows=True, align=True)
        row = grid.row(align=True)
        row.operator("nothing3d.material_gltf_mute",
                     text="Albedo").exclude = "albedo"
        row = grid.row(align=True)
        row.operator("nothing3d.material_gltf_mute",
                     text="ORM").exclude = "orm"
        row = grid.row(align=True)
        row.operator("nothing3d.material_gltf_mute",
                     text="Normal").exclude = "normal"
        row = grid.row(align=True)
        row.operator("nothing3d.material_gltf_mute",
                     text="Emissive").exclude = "emit"
        grid = box.grid_flow(
            row_major=True, even_columns=True, even_rows=True, align=True)
        row = grid.row(align=True)
        row.operator("nothing3d.material_gltf_mute",
                     text="Mute all").exclude = "mute"
        row = grid.row(align=True)
        row.operator("nothing3d.material_gltf_mute",
                     text="Unmute all").exclude = "unmute"
        # fixing
        row = box.row()
        row.label(text="Fix:")
        grid = box.grid_flow(
            row_major=True, columns = 2, even_columns=True, even_rows=True, align=True)
        row = grid.row(align=True)
        row.operator("nothing3d.material_gltf_colorspace", text="Colorspace")
        row = grid.row(align=True)
        row.operator("nothing3d.material_gltf_uvnode_naming", text="UV nodes")


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

class NTHG3D_OT_material_gltf_colorspace(bpy.types.Operator):
    bl_idname = "nothing3d.material_gltf_colorspace"
    bl_label = "Fix gltf textures colorspace"
    bl_description = "Fix gltf textures colorspace"

    def execute(self, context):
        gltf_fix_colorspace()
        return {'FINISHED'}

class NTHG3D_OT_material_gltf_uvnode_naming(bpy.types.Operator):
    bl_idname = "nothing3d.material_gltf_uvnode_naming"
    bl_label = "Relink TEXCOORD_x naming to actual mesh uv names"
    bl_description = "Relink TEXCOORD_x naming to actual mesh uv names"

    def execute(self, context):
        gltf_fix_uvnode_naming(self)
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
    NTHG3D_OT_material_gltf_colorspace,
    NTHG3D_OT_material_gltf_uvnode_naming,
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
