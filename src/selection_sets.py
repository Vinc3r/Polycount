import bpy


def meshes_in_selection():
    return [o for o in bpy.context.selected_objects if o.type == 'MESH']


def meshes_without_uv():
    objects_selected = meshes_in_selection()
    objects_without_uv = []
    objects_without_uv2 = []
    for obj in objects_selected:
        mesh = obj.data
        if len(mesh.uv_layers) > 2:
            # have more than 2 uv
            continue
        if len(mesh.uv_layers) == 0:
            # no uv at all
            objects_without_uv.append(obj)
            continue
        if len(mesh.uv_layers) == 1:
            # only one chan
            objects_without_uv2.append(obj)
            continue
    return objects_without_uv, objects_without_uv2


def meshes_with_materials():
    objects_selected = meshes_in_selection()
    objects_with_mtl = []
    for obj in objects_selected:
        if len(obj.data.materials) == 0:
            continue
        objects_with_mtl.append(obj)
    return objects_with_mtl


def meshes_without_materials():
    objects_selected = meshes_in_selection()
    objects_without_mtl = []
    for obj in objects_selected:
        if not obj.data.materials:
            objects_without_mtl.append(obj)
    return objects_without_mtl


def make_object_active(self, context):
    context.scene.objects.active = bpy.data.objects[str(self.mesh_to_select)]
    return {'FINISHED'}
