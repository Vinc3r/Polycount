# Nothing-is-3D Tools

A Blender add-on made to work faster, often oriented 3D realtime workflow.

- Download or update the addon from the [release page](https://github.com/Vinc3r/BlenderScripts/releases/).

- Changelog [available here](https://github.com/Vinc3r/BlenderScripts/blob/master/changelog.md).

- You can also find some [snippets](https://github.com/Vinc3r/BlenderScripts/tree/master/snippets), supposed to be merged on the main add-on later (and then deleted), or not.

- You can make feedbacks by creating a github issue here, or contact me through [my website](https://www.nothing-is-3d.com/contact) or even [Twitter](https://twitter.com/Vinc3r).

**Table of content**

1. <a href="#main-features">Main Features</a>
2. <a href="#installation">Installation</a>
3. <a href="#usage">Usage</a>
    1. <a href="#usage-meshes">Meshes part</a>  
    2. <a href="#usage-materials">Materials part</a>  
    3. <a href="#usage-stats">Stats part</a>
    
## [Main Features](#main-features)

- quick switch to activate UV1 & UV2 on selected objects
- clean FBX imported materials (only on Blender Render for now)
- get stats about objects polycount

## [Installation](#installation)

1. download [nothing-is-3d tools](https://github.com/Vinc3r/BlenderScripts/releases/)

2. in Blender go to *File* > *User Preferences* > *Add-ons* Tab

3. remove previous installation if needed (search *nothing* to easily find it)

4. install by using *Install from File...* in *Blender User Preferences* > *Add-ons* tab

Tools will be placed on:
- Tools panel of 3DView, in *Nthg is 3D* tab.
- Scene panel in Properties, in *Stats* panel

## [Usage](#usage)

By default, tools are applied on selected objects.

### [*Meshes* part](#usage-meshes)

#### UV channels

- **Select** allow to quickly switch active UV. Usefull when you're in Material shading viewport
- **Rename channels** rename first channel to *UVMap*, second to *UV2*, third to UV3, etc. Usefull when importing meshes from other 3D softwares.

<img src="https://raw.githubusercontent.com/Vinc3r/BlenderScripts/master/_readmeAssets_/demo-UV-chans.gif" height="280">

---

### [*Materials* part](#usage-materials)

#### Import cleaner

*only on Blender Render for now*

- **intensity** set diffuse intensity to 1
- **color** set color to white
- **alpha** reset alpha params
- **spec** set specular to black and its intensity to 1

<img src="https://raw.githubusercontent.com/Vinc3r/BlenderScripts/master/_readmeAssets_/demo-reset-mtl.gif" height="280">



### [*Stats* part](#usage-stats)

- show **polycount** as vertices & triangles. Add **±** when nGons are found.
- clicking on the object name make it active.

<img src="https://raw.githubusercontent.com/Vinc3r/BlenderScripts/master/_readmeAssets_/demo-stats.gif" height="280">
