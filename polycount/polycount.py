import bpy
import bmesh
import datetime
from bpy.types import Scene
from bpy.props import (
    EnumProperty,
    BoolProperty,
    StringProperty
)
from bpy.utils import user_resource

# some variables have to be accessible from anywhere
objects_polycount, total_polycount = [], []
last_user_refresh = "never"
polycount_sorting_ascending = True
polycount_sorting = 'TRIS'
object_with_ngons = []


def calculate_mesh_polycount():
    # thanks to sambler for some piece of code https://github.com/sambler/addonsByMe/blob/master/mesh_summary.py

    # using global variables
    global objects_polycount
    global total_polycount
    global polycount_sorting
    global polycount_sorting_ascending
    global object_with_ngons

    total_tris_in_selection = 0
    total_verts_in_selection = 0
    total_area = 0
    objects_to_compute = []
    object_with_ngons = []
    user_preferences = bpy.context.preferences.addons[__package__].preferences

    if bpy.context.scene.polycount_use_selection:
        objects_to_compute = [
            o for o in bpy.context.selected_objects if o.type == 'MESH']
    else:
        objects_to_compute = [
            o for o in bpy.context.view_layer.objects if o.type == 'MESH']

    """
    trying to get rid of instances
    """
    # objects_to_compute_name = []
    # for obj in objects_to_compute:
    #     # bypassing instances, as polycount is obviously the same
    #     objects_to_compute_name.append(obj.name)
    # objects_to_compute_name.sort(reverse=False)
    # instance_list = []
    # for name in objects_to_compute_name:
    #     current_object = bpy.data.objects.get(name)
    #     if current_object.data.users == 1:
    #         # no instance
    #         continue
    #     if current_object.data.name not in instance_list:
    #         print("not in")
    #         instance_list.append(current_object.data.name)
    #     print("instance_list: ",instance_list)
    #     for existing_name in instance_list:
    #         # if original mesh on the list, we can erase this current instance
    #         print("3")
    #         print("current_object.name:",current_object.name)
    #         print("existing_name",existing_name)
    #         if str(current_object.data.name) == str(existing_name):
    #             print("yepyepyep")
    #             continue
    #         print("nopenopenope")
    #         objects_to_compute.remove(current_object)
    # print("final")
    # print(objects_to_compute)
    # reset the table

    """
        thanks to glTF developpers for piece of code about normals,
        allowing realistic vertex count
        https://github.com/KhronosGroup/glTF-Blender-IO/blob/master/addons/io_scene_gltf2/blender/exp/gltf2_blender_gather_nodes.py#L268
    """

    objects_polycount = []
    total_polycount = []
    modifier_normal_types = [
        'NORMAL_EDIT',
        'WEIGHTED_NORMAL',
        # 'BEVEL',
        'EDGE_SPLIT'
    ]
    # calculate only selected objects
    for obj in objects_to_compute:

        auto_smooth = obj.data.use_auto_smooth
        edge_split_tmp = None
        # checking if obj have normals modifier
        have_some_normals_modifier = any([m in modifier_normal_types for m in [
                                         mod.type for mod in obj.modifiers]])

        # if only autosmooth, we can add a temp edgesplit modifier
        if auto_smooth and not have_some_normals_modifier:
            edge_split_tmp = obj.modifiers.new(
                'Temporary_Auto_Smooth', 'EDGE_SPLIT')
            edge_split_tmp.split_angle = obj.data.auto_smooth_angle
            edge_split_tmp.use_edge_angle = not obj.data.has_custom_normals
            obj.data.use_auto_smooth = False
            bpy.context.view_layer.update()

        # updating all this stuff that's I'm not sure what it is
        depsgraph = bpy.context.evaluated_depsgraph_get()
        blender_mesh = obj.evaluated_get(depsgraph).to_mesh(
            preserve_all_data_layers=True, depsgraph=depsgraph)

        bm = bmesh.new()
        bm.from_mesh(blender_mesh)
        bm.faces.ensure_lookup_table()
        # tri
        tris_count = 0
        if user_preferences.show_tris:
            tris_count = len(bm.calc_loop_triangles())
        # verts
        exceed_16bmesh_buffer_limit = False
        verts_count = 0
        if user_preferences.show_verts:
            verts_count = len(bm.verts)
            if verts_count > 65535:
                exceed_16bmesh_buffer_limit = True
        # area
        has_ngon = False
        area = 0
        for face in bm.faces:
            if user_preferences.show_area:
                area += face.calc_area()
                area = round(area, 2)
            if len(face.edges) > 4:
                has_ngon = True
        if has_ngon:
            object_with_ngons.append(obj)
        # adding obj polycount to total count
        total_tris_in_selection += tris_count
        total_verts_in_selection += verts_count
        total_area += area
        # generate table
        objects_polycount.append([
            obj.name,
            verts_count,
            tris_count,
            has_ngon,
            area,
            exceed_16bmesh_buffer_limit
        ])

        # removing temp edge split modifier
        if auto_smooth and not have_some_normals_modifier:
            obj.data.use_auto_smooth = True
            obj.modifiers.remove(edge_split_tmp)

        bm.free()

    total_polycount = [total_verts_in_selection,
                       total_tris_in_selection, total_area]

    def sortList(item):
        if polycount_sorting == 'NAME':
            return item[0].casefold()
        elif polycount_sorting == 'VERTS':
            return item[1]
        elif polycount_sorting == 'TRIS':
            return item[2]
        elif polycount_sorting == 'AREA':
            return item[4]
        else:
            # tris by default
            return item[2]

    if polycount_sorting == 'NAME':
        name_ascending = not polycount_sorting_ascending
        objects_polycount.sort(
            key=sortList, reverse=name_ascending)
    else:
        objects_polycount.sort(
            key=sortList, reverse=polycount_sorting_ascending)

    return {'FINISHED'}


def select_objects_with_ngons():
    # print(object_with_ngons)
    if len(object_with_ngons) > 0:
        for obj in bpy.context.view_layer.objects:
            if obj.type != 'MESH':
                continue
            obj.select_set(False)
        for obj in object_with_ngons:
            if obj.type != 'MESH':
                continue
            obj.select_set(True)
        bpy.context.view_layer.objects.active = object_with_ngons[0]
    return {'FINISHED'}
    
def trim_numbers(number):
    """ Take a number as entry, return a string formated
    """
    user_preferences = bpy.context.preferences.addons[__package__].preferences
    numberAsString = "{}".format(number)
    if (number < 1000
        or user_preferences.trim_numbers == False
    ):
        return numberAsString
    else:
        numberAsString = "{:,.2f}k".format(round(number/1000, 2)).replace(",", " ")
    return numberAsString

class POLYCOUNT_PT_gui(bpy.types.Panel):
    bl_label = "Polycount"
    bl_idname = "POLYCOUNT_PT_gui"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        global last_user_refresh
        global polycount_sorting_ascending
        global polycount_sorting

        user_preferences = context.preferences.addons[__package__].preferences

        """
            refresh
        """

        row = layout.row()
        row.operator("polycount.user_interaction",
                     text="Refresh (last: {})".format(last_user_refresh), icon="FILE_REFRESH").refresh = True

        """
            options
        """

        box = layout.box()
        row = box.row()
        row.prop(context.scene, "polycount_use_selection", text="Only selected")

        if not context.scene.polycount_options_unfold:
            row.operator("polycount.fast_options_unfold",
                         icon='TRIA_RIGHT', text="Options", depress=False).unfold = True
        else:
            row.operator("polycount.fast_options_unfold",
                         icon='TRIA_DOWN', text="Options", depress=True).unfold = False
            subbox = box.box()
            row = subbox.row()
            row.operator("polycount.fast_options_sel_ngons",
                         text="Select nGons objects")

        """
            show total polycount
        """

        col_flow = layout.column_flow(
            columns=0, align=True)
        row = col_flow.row(align=True)
        row.label(text="Total")
        if len(total_polycount) > 0:
            if user_preferences.show_verts:
                row.label(text="{}".format(trim_numbers(total_polycount[0])))
            if user_preferences.show_tris:
                row.label(text="{}".format(trim_numbers(total_polycount[1])))
            if user_preferences.show_area:
                row.label(text="{}".format(trim_numbers(total_polycount[2])))
        else:
            if user_preferences.show_verts:
                row.label(text="-")
            if user_preferences.show_tris:
                row.label(text="-")
            if user_preferences.show_area:
                row.label(text="-")

        """
            show individuals polycount
        """

        row = col_flow.row(align=True)

        # buttons layout

        # Object name

        if polycount_sorting == 'NAME':
            if polycount_sorting_ascending:
                row.operator("polycount.user_interaction",
                             text="Object", icon="TRIA_DOWN").poly_sort = 'NAME'
            else:
                row.operator("polycount.user_interaction",
                             text="Object", icon="TRIA_UP").poly_sort = 'NAME'
        else:
            row.operator("polycount.user_interaction",
                         text="Object").poly_sort = 'NAME'

        # Verts

        if user_preferences.show_verts:
            if polycount_sorting == 'VERTS':
                if polycount_sorting_ascending:
                    row.operator("polycount.user_interaction",
                                 text="Verts", icon="TRIA_DOWN").poly_sort = 'VERTS'
                else:
                    row.operator("polycount.user_interaction",
                                 text="Verts", icon="TRIA_UP").poly_sort = 'VERTS'
            else:
                row.operator("polycount.user_interaction",
                             text="Verts").poly_sort = 'VERTS'

        # Tris

        if user_preferences.show_tris:
            if polycount_sorting == 'TRIS':
                if polycount_sorting_ascending:
                    row.operator("polycount.user_interaction",
                                 text="Tris", icon="TRIA_DOWN").poly_sort = 'TRIS'
                else:
                    row.operator("polycount.user_interaction",
                                 text="Tris", icon="TRIA_UP").poly_sort = 'TRIS'
            else:
                row.operator("polycount.user_interaction",
                             text="Tris").poly_sort = 'TRIS'

        # Area

        if user_preferences.show_area:
            if polycount_sorting == 'AREA':
                if polycount_sorting_ascending:
                    row.operator("polycount.user_interaction",
                                 text="Area", icon="TRIA_DOWN").poly_sort = 'AREA'
                else:
                    row.operator("polycount.user_interaction",
                                 text="Area", icon="TRIA_UP").poly_sort = 'AREA'
            else:
                row.operator("polycount.user_interaction",
                             text="Area").poly_sort = 'AREA'

        # objects stats layout

        if len(objects_polycount) > 0:
            for obj in objects_polycount:
                row = col_flow.row(align=True)
                # show if active
                if context.view_layer.objects.active and context.view_layer.objects.active.name == str(obj[0]):
                    row.operator("polycount.user_interaction",
                                 text=str(obj[0]), depress=True).make_active = obj[0]
                else:
                    row.operator("polycount.user_interaction",
                                 text=str(obj[0]), depress=False).make_active = obj[0]
                # show verts
                if user_preferences.show_verts:
                    verts_number = trim_numbers(obj[1])
                    if not obj[5]:
                        # no mesh vertex buffer limit
                        row.label(text=verts_number)
                    else:
                        row.label(text="{}*".format(verts_number))
                # show tri & ngon
                if user_preferences.show_tris:
                    tris_number = trim_numbers(obj[2])
                    if not obj[3]:
                        # no ngons
                        row.label(text=tris_number)
                    else:
                        row.label(text="± {}".format(tris_number))
                if user_preferences.show_area:
                    # show area
                    row.label(text=trim_numbers(obj[4]))


class POLYCOUNT_OT_user_interaction(bpy.types.Operator):
    bl_idname = "polycount.user_interaction"
    bl_label = "Show polycount in Scene properties panel"
    bl_description = "Show polycount in Scene properties panel"
    make_active: StringProperty(default="")
    poly_sort: EnumProperty(items=[
        ('NAME', "Name", ""),
        ('VERTS', "Verts", ""),
        ('TRIS', "Tris", ""),
        ('AREA', "Area", "")
    ], default='TRIS')
    refresh: BoolProperty(default=False)

    @classmethod
    def poll(cls, context):
        return len(context.view_layer.objects) > 0

    def execute(self, context):
        global last_user_refresh
        global polycount_sorting_ascending
        global polycount_sorting

        if self.refresh:
            # no need to check shits if we only want data refresh
            self.refresh = False
            pass
        else:
            if (self.make_active != ""
                    and bpy.data.objects.get(str(self.make_active)) != None):
                # if we only want to make select an object, no need to change sorting
                context.view_layer.objects.active = bpy.data.objects[str(
                    self.make_active)]
                context.view_layer.objects.active.select_set(True)
            else:
                if last_user_refresh != "never":
                    if self.poly_sort == polycount_sorting:
                        # if we want to toogle sorting type
                        polycount_sorting_ascending = not polycount_sorting_ascending
                    else:
                        # if we change sort
                        polycount_sorting = self.poly_sort
            # resetting the active param
            self.make_active = ""

        # doing the calculation
        calculate_mesh_polycount()

        # getting the time
        now = datetime.datetime.now()
        last_user_refresh = "{:02d}:{:02d}".format(
            now.hour, now.minute)

        return {'FINISHED'}


class POLYCOUNT_OT_fast_options_unfold(bpy.types.Operator):
    bl_idname = "polycount.fast_options_unfold"
    bl_label = "Fast-access options for Polycount"
    bl_description = "Fast-access options for Polycount"
    unfold: BoolProperty(default=False)

    def execute(self, context):
        context.scene.polycount_options_unfold = self.unfold
        return {'FINISHED'}

class POLYCOUNT_OT_fast_options_sel_ngons(bpy.types.Operator):
    bl_idname = "polycount.fast_options_sel_ngons"
    bl_label = "Select objects having nGons"
    bl_description = "Select objects having nGons"

    def execute(self, context):
        bpy.ops.polycount.user_interaction(refresh=True)
        select_objects_with_ngons()
        return {'FINISHED'}


classes = (
    POLYCOUNT_PT_gui,
    POLYCOUNT_OT_user_interaction,
    POLYCOUNT_OT_fast_options_unfold,
    POLYCOUNT_OT_fast_options_sel_ngons,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    Scene.polycount_use_selection = BoolProperty(
        name="Use selected only",
        description="Compute stats only for selected objects",
        default=True
    )
    Scene.polycount_options_unfold = BoolProperty(
        name="Fast options",
        description="Fast options",
        default=False
    )


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del Scene.polycount_use_selection
    del Scene.polycount_options_unfold


if __name__ == "__main__":
    register()
