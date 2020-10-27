bl_info = {
    "name": "Polycount",
    "description": "Know about your scene polycount",
    "author": "Vincent (V!nc3r) Lamy ; thanks for some bits of code to: sambler, glTF developpers",
    "category": "Scene",
    "wiki_url": 'https://github.com/Vinc3r/Polycount/wiki',
    "tracker_url": 'https://github.com/Vinc3r/Polycount/issues',
    "version": (2020, 10, 27),
    "blender": (2, 90, 0)
}

modulesNames = ['preferences', 'polycount']

modulesFullNames = []
for currentModuleName in modulesNames:
    modulesFullNames.append('{}.{}'.format(__name__, currentModuleName))

import bpy
import sys
import importlib

for currentModuleFullName in modulesFullNames:
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(
            currentModuleFullName)
        setattr(globals()[currentModuleFullName],
                'modulesNames', modulesFullNames)


def register():
    for currentModuleName in modulesFullNames:
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()


def unregister():
    for currentModuleName in modulesFullNames:
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()


if __name__ == "__main__":
    register()
