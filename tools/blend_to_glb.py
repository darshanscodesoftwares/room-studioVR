# Blender headless: .blend -> UV-unwrapped .glb
#
# The runtime box projection in index.html covers tiling skins, so this is
# only needed for the two jobs a projection cannot do:
#   1. carrying a real painted/scanned colour map on a model
#   2. baking a lightmap, which needs every triangle in its own atlas space
#
# Install Blender first (not present on this machine):
#   sudo snap install blender --classic
#
# Then, from the repo root:
#   blender --background ~/Downloads/78-koltuksofa/Koltuk.blend \
#           --python tools/blend_to_glb.py -- assets/koltuk-sofa.glb
#
# Swap the <a-asset-item> in index.html to the .glb and change obj-model to
# gltf-model. Nothing else in the customisation code has to change.
#
# NOTE: untested here — Blender is not installed on this machine. Blender's
# Python API moves between major versions; if smart_project rejects its
# arguments, check `angle_limit` (radians in 3.x+, degrees in some 2.8x
# builds) against your version.

import bpy
import sys
import os

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
out = os.path.abspath(argv[0] if argv else "out.glb")

# start from a known selection state
bpy.ops.object.select_all(action='DESELECT')

unwrapped = 0
for obj in bpy.context.scene.objects:
    if obj.type != 'MESH':
        continue

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # only unwrap what has no UVs, so a model that already carries a good
    # unwrap is never overwritten with a worse automatic one
    if not obj.data.uv_layers:
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(
            angle_limit=1.15,      # ~66 degrees, in radians
            island_margin=0.02     # padding so mip levels do not bleed
        )
        bpy.ops.object.mode_set(mode='OBJECT')
        unwrapped += 1

    obj.select_set(False)

print("[blend_to_glb] unwrapped %d mesh(es)" % unwrapped)

bpy.ops.export_scene.gltf(
    filepath=out,
    export_format='GLB',
    export_apply=True,     # bake modifiers into the exported mesh
    export_yup=True        # glTF is Y-up, same as A-Frame
)

print("[blend_to_glb] wrote %s" % out)
