import bpy
from . import selection_sets
"""todo for optimisation:
        first run:
            custom property for each objects containing stats data
        then updating each time user get back from edit mode:
            update only custom stats from object just edited
"""


def test():
    bpy.context.scene.stats_enabled != bpy.context.scene.stats_enabled
    return {'FINISHED'}
