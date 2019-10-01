bl_info = {
    "name": "Polycount",
    "description": "Know about your scene polycount",
    "author": "Vincent (V!nc3r) Lamy",
    "category": "Scene",
    "wiki_url": 'https://github.com/Vinc3r/Polycount/wiki',
    "tracker_url": 'https://github.com/Vinc3r/Polycount/issues',
    "version": (1, 0, 0),
    "blender": (2, 80, 0)
}

modulesNames = ['polycount', 'selection_sets']

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
