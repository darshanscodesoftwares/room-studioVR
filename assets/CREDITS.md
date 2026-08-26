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

## cat-realistic.obj + cat-diffuse.jpg / cat-bump.jpg — Cat v1 L3

- **Licence: unknown.** The pack shipped no licence file.
- **Source pack:** `Cat_v1_L3.123cb1b1943a-...`, exported from 3ds Max, 2011
- 35,290 verts / 35,288 faces, real UVs, diffuse + bump at 1024px
- Authored Z-up with the head at -Y; corrected with a single -90 X rotation
- **No rig or animation** — it glides along the patrol path; the walk cycle
  belongs to the stylised variant

Treat as uncleared until its origin is established.

---

## sophia.gltf + sophia-*.jpg — Sophia Animated 003 Idling

- **Author / vendor:** Renderpeople
- **Licence: RESTRICTED — the strictest asset in this repo.** Renderpeople's
  terms permit using their people in renders and visualisations but **prohibit
  redistributing the 3D data itself**. Serving `sophia.gltf` and
  `sophia-buffer.bin` from a public URL *is* redistribution: anyone can fetch
  the files.
- **Source pack:** `35-rp_sophia_animated_003_idling_fbx`
- 10,000 polygons, 88-joint skin, one 20.3s idle clip

**Status: blocking for any public deploy.** Read the licence that shipped with
the download before this reaches the Render URL. Options: keep it for local and
headset-on-your-own-network demos only, buy the appropriate licence, or replace
the figure with a CC0 alternative.

Processing applied (originals not redistributed here):

| Output | From | Notes |
| --- | --- | --- |
| `sophia.gltf` + `sophia-buffer.bin` | `.fbx` | via FBX2glTF 0.9.7; landed in metres, Y-up, feet at y=0 — no correction needed |
| `sophia-dif.jpg` | `tex/*_dif.jpg` | 6.8MB → 182KB at 1024px |
| `sophia-norm.jpg` | `tex/*_norm.jpg` | 14.8MB → 265KB at 1024px |
| `sophia-rough.jpg` | `tex/*_gloss.jpg` | **inverted** — glTF has no gloss channel, roughness is its complement |

The `mask01`/`mask02` maps were not used. 47MB of source became 1.8MB of web
assets.

---

## nathan.gltf + nathan-*.jpg — Nathan Animated 003 Walking

- **Author / vendor:** Renderpeople — **same RESTRICTED terms as Sophia above.**
  Redistributing the 3D data is prohibited; a public URL is redistribution.
- **Source pack:** `55-rp_nathan_animated_003_walking_fbx`
- 10,000 polygons, 88-joint skin, one 2.25s walk cycle

Processing applied (originals not redistributed here):

| Output | From | Notes |
| --- | --- | --- |
| `nathan.gltf` + `nathan-buffer.bin` | `.fbx` | via FBX2glTF 0.9.7; metres, Y-up, feet at y=0 |
| `nathan-dif.jpg` | `tex/*_dif.jpg` | 5.3MB → 202KB at 1024px |
| `nathan-norm.jpg` | `tex/*_norm.jpg` | 11.7MB → 309KB at 1024px |
| `nathan-rough.jpg` | `tex/*_gloss.jpg` | 13.3MB → 108KB, **inverted** from gloss |

**Root motion stripped.** The clip walks the figure 2.884m forward over 2.25s
— a native ground speed of 1.282 m/s — and snaps back on every loop. That
channel was removed at build time so `path-walk` can drive the travel instead.

---

## tv-mi.obj — MI Smart TV

- **Licence: unknown.** No licence file in the pack.
- **Source pack:** `32-fbxobj-formats`
- Shipped as a **pedestal** unit. The base and neck were stripped at build
  time — 27,140 of its 44,085 vertices — leaving only the panel, which is what
  can hang on a wall. 5.7MB became 379KB.
- Its `.mtl` defines colour-only material slots and no texture maps, so the
  screen and bezel materials are assigned at runtime.

## tv-smart.gltf — SmartTV

- **Licence: unknown.** No licence file in the pack.
- **Source pack:** `wa5ztx5h5jb4-SmartTV`
- Converted from FBX via FBX2glTF. Authored on its side with the stand at -X,
  so it is rolled 90 degrees upright in the scene.
- Its FBX never referenced the bundled `Texture.jpg`, so the screen texture is
  applied at runtime.

---

## bedroom.gltf + bedroom-*.jpg — Modern Bedroom

- **Licence: not verified.** The pack has a Sketchfab-style layout (source zip
  + textures) but shipped no licence file — check the download page it came
  from before any public deploy.
- **Source pack:** `modern-bedroom` (125MB), FBX + per-piece PBR texture sets
- Ten primitives with named materials: Structure, Meshes, Pillows, BedFrame,
  Chair, Carpet, Painting, EndTables, EndLamps, Duvet
- Structure (the model's own architecture) and Meshes (its curtains) are
  hidden at runtime — the room shell is built in-scene instead, so the
  bedroom's walls, floor and ceiling stay on the shared palettes
- The Duvet material shipped untextured, so it takes a real colour palette
- Converted with FBX2glTF; texture references did not survive (the FBX pointed
  at its .fbm folder), so materials are rebuilt at runtime by name
- 125MB of source became 3.1MB of web assets

---

## cupboard.gltf + cup-*.jpg — Innova H06

- **Licence: unknown.** No licence file in the pack.
- **Source pack:** `innova-h06` (6.7MB), FBX + four PBR texture sets
- 2.15 x 0.60 x 0.50m sideboard with **two lift-up doors and a real 4.38s
  opening animation** — eight channels, a hinge swing plus a lift travel per
  door
- Material names are the Russian originals: Fasad (doors), Korpus (carcass),
  Ru4ki (handles), Podbemnik (lift arms), Mexanizm (hinges, no albedo — given
  a plain metal finish)
- Converted with FBX2glTF; texture references did not resolve, so materials
  are rebuilt at runtime by name. 6.7MB of source became 2.3MB of web assets

## Replacing these

Prefer glTF/GLB with an explicit licence. [Poly Haven](https://polyhaven.com)
is CC0 throughout, which is unambiguous for commercial work.
[Sketchfab](https://sketchfab.com) can be filtered to CC0 and CC-BY, but the
licence is per-model and must be checked each time.
