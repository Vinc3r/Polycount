# Nothing-is-3D Tools

A Blender add-on needed to work faster, often oriented 3D realtime workflow.

Download or update the addon from the [release page](https://github.com/Vinc3r/BlenderScripts/releases/) or through the *zip* above.

Changelog [available here](https://github.com/Vinc3r/BlenderScripts/blob/master/changelog.md).

![nothing-is-3d_tools_default](https://raw.githubusercontent.com/Vinc3r/BlenderScripts/master/_readmeAssets_/nothing-is-3d-tools_default.png)

You can also find some [snippets](https://github.com/Vinc3r/BlenderScripts/tree/master/snippets), supposed to be merged on the main add-on later (and then deleted), or not.

You can make feedbacks by creating a github issue here, or contact me through [my website](https://www.nothing-is-3d.com/contact) or even [Twitter](https://twitter.com/Vinc3r).

**Table of content**

1. <a href="#main-features">Main Features</a>
2. <a href="#installation">Installation</a>
3. <a href="#usage">Usage</a>
    1. <a href="#usage-meshes">Meshes part</a>  
    2. <a href="#usage-materials">Materials part</a>  
    3. <a href="#usage-stats">Stats part</a>
    
---

## [Main Features](#main-features)

- quickly switch between UV1 & UV2
- clean FBX import
- keep informed about objects polycount

---

## [Installation](#installation)

* download [nothing-is-3d tools](https://github.com/Vinc3r/BlenderScripts/releases/)
* in Blender go to *File* > *User Preferences* > *Add-ons* Tab
* remove previous installation if needed (search *nothing* to easily find it)
* install by using *Install from File...* in *Blender User Preferences* > *Add-ons* tab

Tools will be placed on Tools panel of 3DView, in *Nthg is 3D* tab.

---

## [Usage](#usage)

By default, tools are applied on the current objects selection.

---

### [*Meshes* part](#usage-meshes)

#### UV channels

- **Select** allow to quickly switch active UV. Usefull when you're in Material shading viewport, or when set render list in Baketool plugin.
- **Rename UV channels** rename UV1 to *UVMap* and UV2 to*UV2*. Usefull when importing meshes from other 3D softwares.

<img src="https://raw.githubusercontent.com/Vinc3r/BlenderScripts/master/_readmeAssets_/demo-UV-chans.gif" height="280">

---

### [*Materials* part](#usage-materials)

#### Blender Render

- **Diffuse intensity** set diffuse intensity to 1, next button set color to white, next reset alpha params, next set specular to black and its intensity to 1

<img src="https://raw.githubusercontent.com/Vinc3r/BlenderScripts/master/_readmeAssets_/demo-reset-mtl.gif" height="280">

- The two buttons below helps to set diffuse or ambient textures as TexFace (user have to set himself viewport shading to *Textured Solid*)

<img src="https://raw.githubusercontent.com/Vinc3r/BlenderScripts/master/_readmeAssets_/demo-texface.gif" height="280">

### [*Stats* part](#usage-stats)

- show **polycount** as vertices & triangles. Add **±** when nGons are found.
- clicking on the object name make him active.

<img src="https://raw.githubusercontent.com/Vinc3r/BlenderScripts/master/_readmeAssets_/demo-stats.gif" height="280">
