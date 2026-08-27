# room-studioVR

A browser-based WebXR interior-design preview. One furnished room the customer
walks through and customises live — wall paint, flooring, sofa fabric, chair
style and decor — opened in a headset from a URL, with no app install.

Single self-contained file: [`index.html`](index.html). A-Frame 1.7.0 from CDN,
no build step, all furniture built from primitives so nothing can fail to load.

## Run it

**Desktop (development):** open `index.html` with the VS Code Live Server
extension. Drag to look, WASD to walk.

**Headset:** the page must be served over **HTTPS** — plain HTTP will not enter
VR. Push to GitHub and enable Pages (or deploy as a Render Static Site), then
open the resulting URL in the headset browser and tap the VR button. Keep
`index.html` at the repo root; both hosts are then zero-config.

## Controls in VR

| Input | Action |
| --- | --- |
| Left trigger (or grip) | Teleport — hold to aim the arc, release to move |
| Left thumbstick | Smooth walk (can be switched off) |
| Right thumbstick | Snap turn, 30° |
| Right trigger | Click the floating panel |
| Y or B button | Summon / dismiss the customiser on the left controller |

In VR the customiser is controller-attached, X-Plane style: it floats above
the left controller at 38% scale and travels with the visitor, summoned and
dismissed with Y/B or its HIDE tab, clicked with the right laser. On desktop it
keeps its wall pose. The follow runs per-frame on the object3D rather than
reparenting the DOM, which would re-initialise every dynamically built control,
and only a real headset pulls it off the wall — desktop fullscreen also fires
enter-vr and must not.

Both locomotion styles ship together on purpose: the desktop panel can switch
smooth walking off mid-session, so smooth and teleport can be compared with the
same build during a buyer test.

## Customisation

Wall paint, flooring and sofa fabric each have six options; the accent chair has
two styles; rug, plant and wall art toggle on and off. All of it is reachable
from both the desktop overlay and the in-VR panel, driven from one shared
`PALETTE` definition so the two cannot disagree.

**Finish packages** apply a complete named look in one click — Studio, Warm Oak,
Cool Minimal — defined in `PACKAGES`. **Reset to default** restores the Studio
package and returns the visitor to the entrance.

**Lighting** has three presets — Day, Evening, Night — each driving the ambient
and directional lights, the window glass and the daylight spill together, plus a
separate floor-lamp switch. Lighting is deliberately independent of the finish
package, so one finish can be judged across the day without losing the package.

## Visual fidelity

The ceiling here is the headset GPU, not the framework — A-Frame *is* Three.js,
so moving to raw Three.js or Babylon would buy control, not fidelity. What is
implemented:

**Renderer.** ACES filmic tone mapping, colour management, exposure 1.1,
`highRefreshRate` and foveation level 1. Tone mapping is the single largest
perceived-realism change in the file: it stops highlights clipping to flat
white, which is what makes untuned WebGL look cheap.

**Image-based lighting.** The `image-based-lighting` component builds a
sky/horizon/ground gradient with a soft sun on a canvas and runs it through
`PMREMGenerator`, so every PBR surface gets reflections and ambient bounce with
no asset to download and nothing that can fail. To use a real captured
environment instead, drop an equirectangular **LDR JPG** into `assets/` and set
`image-based-lighting="src: assets/env.jpg"` on the scene — an LDR JPG loads
with the plain `TextureLoader`, so no extra loader has to be bundled. The
environment intensity dims with the lighting preset, or night looks like a lit
studio set.

**Shadows.** One shadow-casting directional light — affordable on a mobile GPU,
where three would not be — with a 2048 map and the shadow camera clamped tight
to the room so none of it is wasted on empty space outside the walls. Casting
and receiving policy lives in `setupShadows()` rather than scattered across
entity attributes.

**Materials.** Per-surface roughness and metalness: sealed floor at 0.55 so it
catches the environment, matte plaster at 0.94, fabric at 0.92, a lacquered
table top at 0.28 to carry the window reflection, dark metal legs at 0.4 with
metalness 0.6.

### Rounded upholstery

Sofa cushions, arms, chair upholstery and the table top use a `rounded-box`
geometry rather than `<a-box>`. Furniture has no sharp arrises — a sofa arm with
a knife edge reads as a crate no matter how good the fabric on it is. The
component builds a rounded rectangle and extrudes it with a matching bevel, so
all twelve edges are radiused and catch a soft highlight along their length.

`ExtrudeGeometry` emits UVs in object units rather than 0..1 per face; that is
flagged on the geometry so the skin layer tiles by metres, which also keeps
texel density consistent across parts of very different sizes.

### Procedural skins

Every finish carries a material skin generated at runtime on a canvas — no
files, no CORS, no repo weight, no pop-in, nothing that can 404 in front of a
customer. Six generators in `ProcTex`: plaster tooth, plank seams with grain,
furniture wood grain, fabric weave, rug pile, tile with grout. A normal map is
derived from each by Sobel, so the detail catches light instead of being a flat
picture of texture.

Every map is greyscale and multiplies over the palette colour, so one weave
serves all six fabrics: the hex stays the paint, the skin adds the material.
Tile counts are computed per mesh from its own bounding box, so a 6m floor and a
20cm chair leg do not end up at the same texel density, and textures are cached
per (kind, repeat) rather than cloned per mesh.

Four more generators skin the fixed props: fired-clay **terracotta** with
throwing rings, potting **soil**, **bark** with vertical fissures, and **foliage**
built from overlapping leaf blades so a smooth sphere reads as a canopy rather
than a green ball. Those are applied once in `skinFixtures()`, which states tile
counts explicitly — a cylinder's circumference and its height are very different
lengths under the same 0..1 UV, and letting the bounding box decide stretches the
grain.

The plant is a flowering bonsai: tapered terracotta pot on a drip saucer, torus
lip, earth mounded above the rim with surface roots flaring from the trunk base,
a three-segment S-curved trunk, and five flattened canopy pads whose spread runs
about twice the pot width — the classic proportion. Blossoms sit on the pad
surfaces, fallen petals ring the pot, and moss patches the soil, all scattered
from a fixed seed so the tree looks the same to every visitor and in every
screenshot.

One API landmine worth recording: `<a-cylinder>` silently ignores
`radius-top`/`radius-bottom` (that is `<a-cone>` API) and falls back to the 1m
default radius — the original pot rendered as a 2m disc because of exactly this.
Tapered cylinders must be truncated cones.

Seven palettes now drive the room — walls, **ceiling**, flooring, rug, sofa,
chair fabric and table top. Ceiling is its own finish rather than following the
walls, so a timber or charcoal ceiling can be tried against any wall colour.

In VR they are split across **Room** and **Furniture** tabs. The room tab needed
a fourth row for the ceiling, so the whole panel was re-laid out and the board
grew to 2.70m. Both tab layouts are verified against a collision check that
walks the panel top to bottom, since a 2cm text overlap is invisible in code and
obvious in a headset.

These are a floor, not a ceiling. Scanned PBR sets slot in over them via the
`tex` path below.

### Adding downloaded textures

You do not need Blender for this — A-Frame primitives already have UVs, so a
tiling texture drops straight on. Free CC0 sources: [ambientCG](https://ambientcg.com),
[Poly Haven](https://polyhaven.com/textures), [3dtextures.me](https://3dtextures.me).

Download the files into `assets/` — hotlinking will fail CORS and give you a
black surface — then add the maps to the palette entry:

```js
{ id: 'oak', name: 'Oak', hex: '#b98b5e',
  tex:    'assets/oak_color.jpg',
  normal: 'assets/oak_normal.jpg',
  rough:  'assets/oak_rough.jpg',
  repeat: '6 6' }
```

Both panels, the packages and reset keep working unchanged, and entries without
maps stay flat colour — so finishes can be textured one at a time. If a texture
404s the material falls back to its `hex`, which preserves the "nothing can fail
to load" property. Preload the files in `<a-assets>` so surfaces do not pop in
while a customer is standing there. Use 1K JPGs, and skip ambient-occlusion and
displacement maps — they will cost more framerate than they return.

### Baked lighting — the next step, and the one that needs Blender

Real-time lights cannot produce bounce light or contact shadows at mobile
framerates. Baking precomputes them. The `lightmap` component is already wired
in and dormant:

```html
<a-entity id="room" lightmap="src: assets/room_bake.jpg"></a-entity>
```

Bake to **greyscale only** — ambient occlusion, contact shadows and light
falloff — so it multiplies over whatever albedo the customer has selected. Bake
the colours in and switching the sofa to olive leaves terracotta bounce light on
the floor. You lose coloured bounce; you keep live customisation, which is the
product.

This tier does need Blender, not for modelling but for the UV2 unwrap and the
Cycles bake. It is a one-time job per room, not an ongoing pipeline.

### Performance budget (Quest 3)

| Constraint | Target |
| --- | --- |
| Draw calls | under ~150 — **matters more than triangle count** |
| Visible triangles | 300–500k |
| Textures | 2K for floor and hero furniture, 1K elsewhere |
| Format | KTX2/Basis over JPG once real assets land |
| Meshes | Draco or Meshopt compression on every glTF |
| Framerate | lock 72fps and never drop |

Above the standalone browser there are only two real options: **cloud pixel
streaming** (Unreal + Pixel Streaming over WebRTC — unlimited fidelity, but a
GPU server per concurrent viewer and hard latency sensitivity), and **Gaussian
splatting** (photoreal for a captured real room, but you cannot repaint a wall
in a splat, so it is incompatible with customisation).

## Session telemetry

Every visitor action is logged locally: finish selections, package applies,
lighting changes, decor toggles, teleports, resets, VR enter/exit. The desktop
panel shows a live readout, and the log exports as JSON (download or clipboard).

Nothing is sent anywhere and nothing identifies the visitor — the log holds
timings, selections and a truncated user-agent string. A facilitator can also
read it from the console:

```js
RoomStudio.session()   // full payload: summary + event list
RoomStudio.summary()   // counts only
RoomStudio.state()     // current room configuration
```

Read the output as interaction counts, not as evidence of preference strength or
intent. A finish may be clicked repeatedly because it sits nearest the panel.

## Known caveat to verify on-device

Thumbstick forward/back sign differs between WebXR runtimes. If pushing forward
walks backwards on the headset, set `invertForward: true` on the
`thumbstick-locomotion` component on `#handLeft`.

Controller mapping uses `meta-touch-controls` (Quest). For Pico or WMR, swap in
`laser-controls` on `#handLeft`.

## The cat

The cat slot switches between the built one and a 35k-triangle scanned model
with diffuse and bump maps. The scanned one carries no rig, so it glides —
a bob and roll on the stride phase keeps it from reading as a prop on rails,
but the actual gait belongs to the stylised variant. That is the trade the
slot makes visible: shape fidelity against motion fidelity.

Fur on the stylised variant is a normal-only strand map: relief in the lighting, colour left clean.
Two things were tried and reverted, both worth recording. A greyscale colour
map at cat scale reads as grime, not fur. And shell rendering — concentric
alpha-masked copies, the textbook fluff technique — needs strand tips far
finer than a 256px mask gives on a 13cm body, so it rendered as mottled
lumps. Volumetric fur wants a real groom, not primitives.


A primitive-built cat patrols a hardcoded waypoint loop that threads the
clear floor lanes: along the west wall, through the gap between sofa and
coffee table, up the window side, and back across the entrance. The path is
collision-checked against every furniture footprint. `cat-walk` drives a
diagonal-gait leg swing, body bob, tail sway, and dwell pauses at three
corners where the cat sits, looks around, and turns toward its next leg
before setting off. Everything runs off elapsed time with no randomness, so
the cat is deterministic. The Cat decor toggle hides it (patrol suspends
while hidden).

Why primitives: the downloaded `.skp` cat could not be used — no browser
loader exists for SketchUp files, and SketchUp has no skeletal animation, so
the file holds a statue. To upgrade later: source an *animated* GLB (check
the Sketchfab "Animated" filter and licence), keep the `cat-walk` path
logic, and drive `THREE.AnimationMixer` from the model's walk clip instead
of the procedural leg swing.

## Model variants

Sofa, plant and cat are **slots**, not fixed objects: each holds interchangeable
models of the same piece of furniture, chosen from a dropdown in the desktop
panel or a **Models** tab in VR. Variants share an anchor, so switching swaps in
place instead of moving furniture across the room.

All variants live in the scene at once and are shown one at a time. That keeps
switching instant with no load hitch mid-demo; the trade is memory, and at these
polycounts it is the right way round. Adding a variant means putting its entity
in the markup and adding a row to `MODELS` — both panels pick it up with no
further wiring.

This is the direct answer to the brief's *"one showroom presents multiple
configurations"*: finish packages change the surfaces, model variants change the
furniture itself, and both are logged.

## The second room

A 6×5m bedroom now adjoins the living room through a cased doorway in the
south wall. The shell — walls, ceiling, floor, and a matching east window — is
built in-scene rather than taken from the bedroom model, which is what keeps
every surface on the same palettes as the living room: one wall colour, one
flooring, one ceiling finish across the flat.

The furniture is the Modern Bedroom pack: bed, duvet, pillows, end tables,
lamps, chair, carpet and a painting, placed so the bed faces the doorway. The
model's own architecture and curtains are hidden at runtime. Its **duvet
shipped as an untextured material**, so it takes a true colour palette —
six options on the desktop panel and the VR furniture tab — while the
photo-textured pieces are tintable and toggleable per piece by material name.

The model's own walls, shoji window and curtains stay hidden for a reason:
they are baked scenery, and using them would freeze the room. Their character
is rebuilt instead as customisable pieces — a paintable **accent wall** panel
behind the bed, **curtains** flanking both windows on the shared curtain
palette, and a bedroom rug on the living room's rug palette. The lamp shades
glow softly via emissive. The VR panel gains a fourth **Bedroom** tab carrying
accent wall, curtains and duvet.

Walkable space is now a union of regions — living room, bedroom, and the
doorway strip — rather than one clamped square. Blocked moves slide along the
wall instead of stopping dead, which is also what funnels a visitor through
the doorway naturally. Teleport aims with the same rule, so the arc goes red
over the doorway wall but lands in either room.

## The gun range

A doorway near the living room's south-west corner opens onto a corridor that
runs 6.9m west and then turns right for another 7.5m, with the shooting range
at the end of that second leg — roofed over the firing side,
open sky over the targets, concrete throughout and deliberately not on the
finish palettes. The dog-leg is the point. A straight run let the living room see all the way
down to the range, and no amount of dimming stops a lit room being visible at
the end of a tube. Around a corner there is no sight line at all — which is a
geometry answer to a lighting problem, and the only one that cannot regress.

The actual bleed was subtler and worth recording: point lights ignore walls
entirely, and the living room's own window light had a 9m radius from x=2.4,
so it reached 3.6m *past* the west wall and lit whatever was behind it. Both
window lights are now sized to stop just inside their own rooms.

There is no game: a shooting stand, a backstop with paper target faces, a
lane to walk, and one rifle that can be picked up.

The rifle is **grabbable from either hand** and needs no second raycaster for
it: pull a trigger while that hand is within reach and it comes to that hand.
The right laser and the desktop mouse also work through a plain click, so the
same object is reachable in a headset and at a desk. Releasing returns it to
the bench rather than dropping it in mid air — there is no physics here, and a
rifle hanging in space reads as a bug rather than as a dropped object.

Teleport asks the grab system before firing, so reaching for the rifle with
the left hand does not also fling the visitor across the room.

### The corridor door

A hinged door hangs in the opening, clicked to swing. The pivot sits on the
jamb with the leaf hung off it, so it moves like a door rather than spinning
about its own middle, and the swing is eased so it settles into the jamb. It
opens into the living room because the corridor is only a metre wide.

Shutting it removes the walkable strip through the opening, so it genuinely
blocks the way rather than looking shut. Two details make that safe: the strip
is dropped the moment the door starts closing, so nobody walks through a door
swinging into their face; and the leaf is a solid box, so the laser hits it
from either side and a visitor in the corridor can always open it again.

### Switching the range off

The whole wing is a toggle. **Range** off hides the corridor, the range and
the doorway casing, reveals a fill panel that seals the west wall — on the
wall palette, so it paints with everything else — and drops the range's
walkable regions, leaving the flat exactly as it was before. Off is the safe
direction, so it also ends any game in progress and walks a visitor who is out
there back inside: otherwise they would be standing in a region that no longer
exists, unable to move in any direction.

Like the figures, the range is a wing rather than decor, so finish packages
leave it alone.

## Interactive furniture

A sideboard with two lift-up doors stands against the bedroom's west wall
below the portrait. Its FBX carried a genuine 4.38s opening take, so it is
driven by **click** rather than looped: point at it and pull the trigger to
open, again to close. It joins the same raycaster the panel uses, so the
right-hand laser works on it without any new input plumbing, and it answers
the pointer with a hover glow — a surface that responds is what tells a
visitor this one object is interactive.

A tall wardrobe stands on the doorway wall beside it, forming an L in the
corner, on the same click-to-open handling.

Both units ship showcase round trips rather than openings, so `openAt` marks
where each is fully open — 44.7% for the sideboard, 46.0% for the wardrobe.
The wardrobe's was found by sampling all 34 channels and measuring total
deviation from the start pose, since staggered drawers peak at different
times and eyeballing one channel would have been wrong.

The clip is not played as a clip. The mixer is seeked by hand each frame from
a progress value the click flips between 0 and 1, which is what lets the doors
**reverse mid-swing**: click again halfway and they come back down from where
they are, rather than snapping to an end and restarting. It also decouples the
pace from the take — the source runs 4.38s, slow to watch twice, so the
component retimes it to 1.6s without touching the data.

## The human figure

A 1.69m animated figure stands off the west side of the room, playing a 20.3s
idle loop through `gltf-animation` — a small `THREE.AnimationMixer` wrapper
written here rather than pulled from aframe-extras, to keep the file
dependency-free. A person at true scale is the fastest way for a buyer to read
room proportions, which is the core claim of the real-estate track.

Converted from Renderpeople FBX with FBX2glTF; it landed already in metres,
already Y-up with feet on the ground plane, so it needs no correction
transform. Its normal and roughness maps ride alongside the glTF rather than
inside it, because the originals are 15MB and 4MB and downsizing them
separately keeps the model file small. Gloss was inverted to roughness at build
time, since glTF has no gloss channel.

A second figure — a 1.86m man — moves between stops and waits at each,
his own walk clip supplying the gait. A continuous loop reads as a mannequin on
a track; the giveaway is that he never stops. So each stop carries its own dwell
(12–20s) and something to look at while waiting: he stands at the window looking
out, beside the woman turned toward her, and in front of the TV. Zero-dwell
waypoints between them keep his route clear of the furniture — the room's
circulation runs as a ring around the seating, and a straight line between two
stops would otherwise cut through the sofa. With nothing
specified he turns toward wherever he is heading next, so leaving reads as
intentional. Over a cycle he spends 65 seconds standing and 9 walking, which is
roughly how people actually occupy a room.

The pack ships a walk clip and no idle, so standing is built in three parts.

First the pose. Every frame of a walk is mid-step, including the one where the
feet are closest — one knee is bent and the weight is on a single foot, which
is exactly how it looked. But the model's *bind* pose is a real standing stance
from the waist down: legs straight to within 2.5 degrees, feet 21cm apart. So
on stopping, everything below the shoulders is returned to the bind pose and he
settles onto both feet. The arms are deliberately left on the animated frame,
because the bind pose puts those in a T — arms hanging mid-swing read as
standing, a T-pose does not.

Then the motion, because a held pose is a statue. While standing the mixer
stops running entirely — it would stamp the frozen pose back over everything
each frame — and a procedural idle drives the bones directly: breathing on the
spine at roughly one breath per 4.3s, a slow weight shift between the feet over
13s, and the head drifting on two unrelated periods. Everything is a few
degrees at most and layered on the standing pose. The periods share no common
factor, so the loop takes about nine minutes to repeat and never reads as
mechanical.

The woman's idle was the obvious source to borrow instead, and was rejected:
her clip is a distinctly feminine stance and retargeting it would have him
posing like her. **People** is a model slot with three
choices: Woman, Man, or **Both**, from the dropdown on desktop or the Models tab
in VR. It is the first variant that maps to more than one entity, which the slot
mechanism now supports generally.

His clip carries baked root motion — 2.884m of travel in 2.25s, a native ground
speed of 1.282 m/s — which was stripped at build time; left in, he walks 2.9m
and snaps back on every loop. `path-walk` drives the travel instead and scales
the clip by `speed / clipSpeed`, so travel and gait can never drift apart and
the feet never skate. His route is verified clear of all furniture and of the
standing figure.

The **People** toggle hides both. Finish packages deliberately leave them alone:
they are scale references, not decor.

> **Licence blocks public deploy.** Renderpeople prohibits redistributing the
> 3D data, and serving the glTF from a public URL is redistribution. See
> [assets/CREDITS.md](assets/CREDITS.md).

## The TVs

A wall-mounted screen hangs on the north wall above the sofa, switchable
between two models from the **TV** slot. Both are scaled to the same 1.25m
screen width so the switch compares the screens rather than their sizes.

The MI model ships as a pedestal unit, which cannot hang on anything. Its OBJ
groups separate cleanly, so the base and neck were stripped at build time —
27,140 of its 44,085 vertices — leaving the panel alone and taking the file
from 5.7MB to 379KB. The SmartTV was authored on its side and is rolled upright
in the scene.

Neither pack carries usable materials: the MI `.mtl` has colour-only slots and
the SmartTV's FBX never referenced its own bundled texture. So both get their
surfaces assigned at runtime, the screen identified as the largest flat face in
the model and given a low roughness so an off screen reads as glass catching
the window rather than as dark paint.

## Loaded models

The second sofa (`assets/koltuk-sofa.obj`, 896 vertices) is the first real 3D
asset in the scene, facing the primitive sofa across the coffee table. It proves
the roadmap claim that the customisation functions survive the
primitive-to-model swap: `setSofaColor` drives both sofas from the same palette,
telling the model's parts apart by mesh name (`Cylinder*` runner rails get the
dark frame finish, everything else is fabric).

The model ships with **no UV coordinates** — and neither does the FBX or the
`.blend` in that pack, so it was not an export mistake. `boxProjectUVs()`
generates them at load: each vertex is projected onto whichever world axis its
normal points at most, in metres.

That works because the skins are *tiling* materials, and a tiling material needs
a projection, not an unwrap. A real unwrap packs every triangle into one atlas,
which is only required for baked per-triangle imagery — a painted colour map, or
a lightmap. Box projection gives consistent texel density across parts of any
size and hides its seams on the corners where the projection axis flips.

For the two jobs projection cannot do, [tools/blend_to_glb.py](tools/blend_to_glb.py)
unwraps a `.blend` headless and exports GLB. It needs Blender installed
(`sudo snap install blender --classic`) and is untested — Blender is not on this
machine.

A second loaded model, `assets/eb-house-plant.obj` (602 tris), stands by the
window. Unlike the sofa it ships with real UVs and a full PBR set, so it needs
no projection — just the maps wired up. Two details its pack dictates:
roughness, metal and opacity were packed into one image's R, G and B channels
and are split at build time (metal measured zero and was dropped), and it was
authored for Unreal, so the normal map's green channel is inverted to convert
DirectX green-down to the OpenGL green-up three.js expects. Leaves are
alpha-cutout with a matching `customDepthMaterial`, without which every leaf
card throws a solid rectangular shadow.

> **Licences are not cleared.** The house plant is marked **NOT FOR COMMERCIAL
> USE** by its author, and the sofa shipped with no licence at all. This POC is
> deployed to a public URL, which is redistribution. See
> [assets/CREDITS.md](assets/CREDITS.md) before any buyer demo or public deploy.

## Roadmap

- Guided sales mode (scripted viewpoints and prompts)
- More glTF/OBJ furniture — pattern proven with the second sofa; prefer glTF
  with UVs so skins and textures apply
- A second room, and saveable/shareable configuration links
