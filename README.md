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

## Roadmap

- Guided sales mode (scripted viewpoints and prompts)
- Real glTF furniture — the mutator functions stay the same, only selectors change
- A second room, and saveable/shareable configuration links
