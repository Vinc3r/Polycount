# Polycount changelog

## In production

Current development additions, available through [last source code](https://github.com/Vinc3r/Polycount/tree/master/polycount) - use it at your own risks:
- vertex buffer limit fixed (65 535 in place of 65 536, [testfile](https://github.com/Vinc3r/BlenderScripts/blob/master/_testFiles_/16b-mesh-vertex-buffer-limitation.glb) to play with [sandbox](https://sandbox.babylonjs.com/)) 
- an arrow show the current sorting way
- fix active button doing mess in sort
- deleting an object no longer thrown an error
- calculation can now be made even in edit mode
- user can choose if polycount is made in selection or whole scene
- resfresh button no longer put mess in sort

## [v1.1.0](https://github.com/Vinc3r/Polycount/releases/tag/v1.1.0)

- huge performance gain: polycount is now refreshed only by user interaction, not anymore on each interface draw

## [v1.0.0](https://github.com/Vinc3r/Polycount/releases/tag/v1.0.0)

- ability to sort by name/verts/tri/area
- when passing out 16b mesh vertex buffer, `*` is shown near verts count
