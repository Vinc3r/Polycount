# Nothing-is-3D Tools

Some little scripts needed to work faster, often oriented 3D realtime workflow.

Download or update the addon from the [release page](https://github.com/Vinc3r/BlenderScripts/releases/) or though the *zip* above.
[changelog](https://github.com/Vinc3r/BlenderScripts/blob/master/changelog.md)

![nothing-is-3d_tools_default](https://raw.githubusercontent.com/Vinc3r/BlenderScripts/master/_readmeAssets_/nothing-is-3d-tools_default.png)

## Main Features

- quickly switch between UV1 & UV2
- clean FBX import
- keep informed about objects polycount

## Installation

* download [nothing-is-3d tools](https://github.com/Vinc3r/BlenderScripts/releases/)
* remove previous installation if needed (search *nothing* to easily find it)
* install by using *Install from File...* in *Blender User Preferences* > *Add-ons* tab

Tools will be placed on Tools panel of 3DView, in *Nthg is 3D* tab.

## Usage

By default, tools are apply on current selection.

### *Meshes* part

#### UV channels

- **Select** allow to quickly switch active UV. Usefull when you're in Material shading viewport, or when set render list in Baketool plugin.
- **Rename UV channels** rename UV1 to *UVMap* and UV2 to*UV2*. Usefull when importing meshes from other 3D softwares.

### *Materials* part

#### Blender Render

- **Diffuse intensity** set diffuse intensity to 1, next button set color to white, next reset alpha params, next set specular to black and its intensity to 1
- The two buttons below helps to set diffuse or ambient textures as TexFace (user have to set himself viewport shading to *Textured Solid*)

### *Stats* part

- show **polycount** as vertices & triangles. Add **±** when nGons are found.
- clicking on the object name make him active.
