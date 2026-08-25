# Asset credits and licences

**Read this before any public deploy, buyer demo, or commercial use.**
Both models below are third-party downloads. Neither has been cleared for
commercial distribution.

---

## eb-house-plant.obj + plant-*.jpg — House Plant 01

- **Author:** Ernesto Bezera (ernestbezera@gmail.com)
- **Licence:** **NOT FOR COMMERCIAL USE** — stated verbatim in the pack's
  `READ_ME.txt`
- **Source pack:** `c30lumexfif4-eb_house_plant_01`
- 602 triangles, real UVs, PBR maps authored for Unreal

**Status: blocking for commercial use.** This POC sits in the real-estate and
interiors track of a commercial R&D portfolio, and it is deployed to a public
URL. A public deploy is redistribution. Before this is shown to a buyer or left
on a public host, either replace the model or obtain written permission from the
author at the address above.

Processing applied (originals not redistributed here):

| Output | From | Notes |
| --- | --- | --- |
| `plant-c.jpg` | `_c.tga` | colour, 2048 → 1024 |
| `plant-n.jpg` | `_n.tga` | normal, **green channel inverted** — DirectX (Unreal) to OpenGL (three.js) |
| `plant-rough.jpg` | `_g.tga` red channel | roughness |
| `plant-alpha.jpg` | `_g.tga` blue channel | opacity mask |

The `_g.tga` green channel held the metal map; it measured zero throughout, so
it was dropped. 37.5MB of TGA became 258KB of JPG — browsers cannot load TGA at
all.

---

## koltuk-sofa.obj — Koltuk sofa

- **Licence: unknown.** The pack shipped no licence file.
- **Source pack:** `78-koltuksofa`
- 896 vertices, no UVs anywhere in the pack (OBJ, FBX or `.blend`), no `.mtl`
  despite the OBJ referencing one

UVs are generated at runtime by box projection; see `boxProjectUVs()` in
`index.html`. Unknown licence is not the same as permissive — treat it as
uncleared until its origin is established.

---

## Replacing these

Prefer glTF/GLB with an explicit licence. [Poly Haven](https://polyhaven.com)
is CC0 throughout, which is unambiguous for commercial work.
[Sketchfab](https://sketchfab.com) can be filtered to CC0 and CC-BY, but the
licence is per-model and must be checked each time.
