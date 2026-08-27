# room-studioVR — state of play

Working notes for picking this up cold. [README.md](README.md) explains how
each feature works; this is what shape the project is in, what cost time, and
what is still open.

## What it is

A WebXR interior-design preview: a customer walks a furnished flat in a
headset from a URL and re-finishes it live. Built for the real-estate and
interiors track of a VR R&D portfolio.

**One file** — [index.html](index.html), ~4,600 lines, A-Frame 1.7 from CDN, no
build step. 19MB of assets. 69 commits.

## The spaces

| | |
| --- | --- |
| **Living room** | 6×6m. Sofa, coffee table, accent chair, rug, lamp, bonsai, wall art, wall-mounted TV. |
| **Bedroom** | 6×5m through a doorway. Bed, side tables, lamps, chair, sideboard, wardrobe, portrait. |
| **Gun range** | Behind a door, down a dog-leg corridor. Bench, backstop, one grabbable AK. **No game** — it was built, then removed on request. Off by default. |

## What a visitor can do

- **12 palettes** — walls, ceiling, flooring, rug, sofa, chair fabric, table
  top, duvet, accent wall, curtains. One shared definition drives the desktop
  panel and the VR panel so they cannot disagree.
- **5 model slots** — sofa, plant, people, TV, cat. Each switches between real
  loaded models; a variant can name several entities (People → Woman / Man /
  Both).
- **3 finish packages**, 3 lighting presets, decor toggles, reset.
- **Interactive** — click-to-open sideboard and wardrobe, a hinged door that
  genuinely blocks passage, a grabbable rifle.
- **Live** — a cat patrols; two animated figures stand, walk between stops and
  breathe while idle.

## How it is built

- **Textures are generated at runtime on a canvas** — plaster, plank, weave,
  silk, fur, soil, bark, foliage, tile — with normal maps derived by Sobel.
  No files to download, nothing that can 404 mid-demo. Greyscale, so they
  multiply over whatever palette colour is chosen.
- **Loaded models** were converted FBX→glTF with **FBX2glTF** (fetched to the
  scratchpad; re-download if missing), textures downsized with **PIL**, and
  materials rebuilt at runtime **by material name** because the converter
  almost never preserves texture references.
- **Movement** is a union of walkable rectangles with slide-along-walls,
  shared by smooth locomotion and teleport.
- **The VR panel** floats on the left controller, tabbed (Room / Furniture /
  Bedroom / Decor / Models).

## Gotchas that cost real time

Read these before debugging anything similar.

1. **`Box3.setFromObject` returns a WORLD box.** Subtracting its centre from an
   object's *local* `position` flings it as far as its parent is from the
   origin. Guns landed 10m outside the room. Measure in the model's own space.
2. **`visible: false` does not stop raycasts.** Hidden VR tabs kept catching
   the laser and stealing clicks. Hidden things must also be moved out of reach.
3. **Point lights ignore walls.** A light in one room lights every room. The
   fix that finally worked was geometry — a dog-leg corridor, so there is no
   sight line at all.
4. **Every `MeshStandardMaterial` has `emissiveIntensity: 1`** with a black
   emissive. A guard testing `emissiveIntensity > 0` matches *everything* — one
   such guard silently disabled a whole function for days.
5. **Product-showcase animations are usually round trips.** The cupboard,
   wardrobe and TV clips all open *and* close. Find the peak-open moment by
   sampling every channel; do not read one channel by eye.
6. **`<a-cylinder>` silently ignores `radius-top`/`radius-bottom`** (that is
   `<a-cone>`) and falls back to a 1m radius. A plant pot rendered as a 2m disc.
7. **Model node transforms compose.** A TV read as portrait from its accessor
   bounds but its mesh node carried a 90° rotation and a 1m offset — it
   rendered behind the wall. Always compose the node hierarchy.
8. **In A-Frame text, a larger `width` means larger glyphs.** Raising it to
   "shrink" labels does the opposite.
9. **A duplicate component name throws and kills the whole script.** A-Frame
   already owns `grabbable`; registering a second one threw at that line, so
   every definition after it — including `boot()` — never ran. The scene still
   rendered, just raw and unskinned, which reads like a lighting bug rather
   than a fatal error. Check a new component name against `aframe.min.js`
   first, and read the console before theorising.

The method that made these tractable: **measure, don't guess.** Vertex
clustering to find which way a cat faces, keyframe sampling for animation
ranges, bounding boxes to normalise guns spanning 0.45×–100× scale, and a
plan-view clearance check for every furniture placement and walking route.

## Open items

- **Licences block a public deploy.** Both Renderpeople figures prohibit
  redistributing the 3D data; the house plant is marked not-for-commercial-use;
  several packs shipped no licence at all. Fine for local and same-network
  headset demos. See [assets/CREDITS.md](assets/CREDITS.md).
- **Rifle grip offset is a guess** — check how it sits in the hand. The firing
  animation is wired now (trigger fires while held, grip releases); the offset
  is the one number left that needs a headset to judge.
- Roadmap leftovers: guided sales mode, saveable configuration links.
- The shooting mini-game was removed in `a5aceb8`; the space came back in
  `d179c28`. History has both if it returns.
