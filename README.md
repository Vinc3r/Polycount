# Nothing-is-3D tools
Some little scripts needed to work faster, often oriented 3D realtime workflow.

Help to navigate between UV1 & 2, clean FBX import, and keep informed about object polycount.

[download](https://raw.githubusercontent.com/Vinc3r/BlenderScripts/master/nothing-is-3D-tools.py) - [changelog](https://github.com/Vinc3r/BlenderScripts/blob/master/changelog.md) - you may want try the beta-but-stable version for now, check the [release page](https://github.com/Vinc3r/BlenderScripts/releases/) for that.

## Installation

* download [nothing-is-3D-tools.py](https://raw.githubusercontent.com/Vinc3r/BlenderScripts/master/nothing-is-3D-tools.py)
* remove previous installation if needed (search  _nothing_ to easily find it)
* install by using _Install from File..._ in _Blender User Preferences_ > _Add-ons_ tab

Tools will be placed on Tools panel of 3DView, in _Addons_ tab.

![nothing-is-3d_tools_default](https://raw.githubusercontent.com/Vinc3r/BlenderScripts/master/README-assets/nothing-is-3d-tools_default.png)

## Usage

### Nothing-is-3D Tools

#### UV channels

- _Select_ allow to quickly switch active UV. Usefull when you're in Material shading viewport, or when set render list in Baketool plugin. Apply on selection.

#### Import cleaner :

- _Rename UV channels_ rename UV1 to _UVMap_ and UV2 to _UV2_. Usefull when import meshes from other 3D softwares. Next button disable auto-smoothing. Apply on selection,
- in Blender Render, _Diffuse intensity_ set diffuse intensity to 1, next button set color to white, next reset alpha params. Apply on selection.

### Nothing-is-3D Tools : Stats

- list meshes in selection, show vertices & triangles number. Add **±** when nGons are found.
