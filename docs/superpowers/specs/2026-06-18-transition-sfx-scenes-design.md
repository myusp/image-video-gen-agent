# Design: Transition + SFX Driven Scenes (in/out props)

**Date:** 2026-06-18
**Status:** Approved (design phase)
**Scope:** `image-video-gen.agent.md`, `remotion-compilation.agent.md`, shared Remotion template (`src/`), `build_config.py`, plus a regenerate+render pass for `output/20260618_upnormal`.

## Problem

AI-generated scene images are 16:9. When the target video is also 16:9 landscape (AR matches the frame), per-scene motion is a lose-lose:

- **`cover_*` modes** — motion (zoom/pan) works, but it *requires* zooming, which crops the image. A 16:9 image on a 16:9 frame cannot pan or zoom without losing content. Result: the image is never shown in full.
- **`contain_blur` mode** — the foreground image is shown in full (`objectFit: contain`), but in the current `SceneImage.tsx` the motion transform is applied **only to the blurred background layer**; the foreground content image is completely static. So the "motion" is wasted on the blur and the actual content feels flat.

Net effect for `20260618_upnormal` (landscape, `contain_blur`): every content image is static and the video feels lifeless.

## Solution

Move the source of visual energy **out of per-scene internal motion and into the cut points** — auto-selected **transitions** plus selective **SFX** between scenes. Scenes default to **static, full-frame `contain` images** (zero crop). A minority of high-impact scenes may receive **subtle motion** (`cover_subtle`, ~3-5% crop) as seasoning. The rhythm of varied transitions + sound effects every ~10s carries the video.

Decisions confirmed with the user:
- Scene treatment: **mostly static `contain` (no crop)**, with **subtle motion allowed on selected scenes** (not pure static everywhere).
- Transition selection: **auto per-scene from prompt content**, default `fade`.
- SFX: **`@remotion/sfx` package** (named URL exports), applied **selectively** (not every cut).

## Schema: `scene-config.json` per-scene `in` / `out`

```jsonc
{
  "sceneNumber": 1,
  "imagePath": "scene_1/image_1.jpeg",
  "audioPath": "scene_1/audio_1.mp3",
  "durationSeconds": 10.96,
  "motionEffect": "none",          // NEW allowed value: "none" = fully static
  "renderMode": "contain_blur",
  "in":  { "transition": "fade", "durationInFrames": 15, "sfx": "whoosh" },
  "out": { "transition": null, "durationInFrames": 15, "sfx": null }
}
```

All `in` / `out` fields are **optional** → existing configs (no `in`/`out`) keep working unchanged.

### Field reference
- `motionEffect` — existing values plus `"none"` (static, no transform).
- `in.transition` / `out.transition` — one of:
  `fade`, `slide-from-left`, `slide-from-right`, `slide-from-top`, `slide-from-bottom`,
  `wipe-from-left`, `wipe-from-right`, `wipe-from-top`, `wipe-from-bottom`, `flip`, `clock-wipe`, `none`.
- `in.durationInFrames` / `out.durationInFrames` — transition length in frames (default `15`).
- `in.sfx` / `out.sfx` — an `@remotion/sfx` export name string (`whoosh`, `whip`, `pageTurn`, `ding`, `vineBoom`, `triggered`, `uiSwitch`, `mouseClick`, …) or `null`.

### Conflict-resolution rule (one transition per cut)
A `TransitionSeries` has exactly **one** transition element between scene N and scene N+1. To avoid `in`/`out` describing the same cut twice:

> **Cut transition between scene N and N+1** = `scenes[N+1].in.transition` if set, else `scenes[N].out.transition` if set, else global default `fade`.
> **Cut duration** = the matching side's `durationInFrames` (default 15).

SFX is independent of the transition:
- `in.sfx` plays at the scene's **first local frame** (i.e. at the cut into the scene).
- `out.sfx` plays a few frames **before the scene ends** (lead-out, e.g. a riser/ding before a reveal).
- Both default `null`; most scenes carry no SFX.

## Template changes (`src/`)

### `package.json`
- Add dependency `@remotion/sfx@4.0.448` (match the existing Remotion 4.0.448 pin). Run `npm install`.

### `SceneImage.tsx`
- Add `"none"` to the `MotionEffect` union.
- When `effect === "none"`, render the image with **no transform** (static) in both `contain_blur` and `cover_subtle` paths. In `contain_blur` + `none`, the blurred background is also static → full image, no crop, no wasted motion.

### `Main.tsx`
- Replace the single hard-coded `fade()` / fixed `TRANSITION_FRAMES` with a **per-cut** transition resolved from config:
  - A `resolveTransition(sceneN, sceneN+1)` helper returns `{ presentation, durationInFrames }` from the strings (mapping each string to the `@remotion/transitions` factory: `fade()`, `slide({direction})`, `wipe({direction})`, `flip()`, `clockWipe()`, `none()`).
  - Build the `TransitionSeries.Transition` for each cut using that result.
- Inject **per-scene SFX** as `<Audio>` from `@remotion/media` with `src` from the `@remotion/sfx` export, mapped by a string→export lookup:
  - `in.sfx` → `<Audio>` at scene local frame 0.
  - `out.sfx` → `<Audio>` inside a `<Sequence from={sceneFrames - lead}>` near the scene end.
  - SFX `volume` ≈ `0.6` so it sits under the narration.
- **Duration math:** each non-last scene's `durationInFrames = round(D·fps) + T_cut`, where `T_cut` is *that specific cut's* transition duration (not a fixed 15). The `TransitionSeries` overlap subtracts exactly `T_cut`, so each scene contributes `round(D·fps)` and the total stays `sum(round(D·fps))` = audio length. Verified the cancellation holds for variable `T_cut`.

### `Root.tsx`
- Extend the `SceneConfig` interface with optional `in?` / `out?` objects.
- Total-frames calculation is **unchanged** (`sum(round(D·fps))`), since per-cut overlaps still cancel.

## Config generator (`build_config.py`)

Extend to emit the new schema:
- For **landscape AR-matching** images: default `motionEffect: "none"` + `renderMode: "contain_blur"` (full image, no crop).
- Promote a **minority** of high-impact scenes to **subtle motion**: when the prompt signals an establishing/hero/emotional/reveal beat, set a gentle `motionEffect` (e.g. `ken_burns`, `zoom_in`) + `renderMode: "cover_subtle"`. Cap the proportion so most scenes stay static.
- Auto-select `in.transition` per scene from prompt content, reusing the existing keyword→signal mapping:
  - calm / narration / continuation → `fade`
  - action / movement / speed → `slide-from-left|right` (alternate direction)
  - momentum / narrative push → `wipe-from-left`
  - reveal / introduction / payoff → `flip` or `clock-wipe`
- Assign SFX **selectively**: `whoosh` / `whip` on strong topic/scene shifts, `ding` on reveals/payoffs, `null` on calm continuations. Never on every cut (avoid repetition). Vary so the same sfx doesn't repeat back-to-back.
- Keep writing `remotion_motions.txt`, extended to log the chosen transition + sfx per scene.

## Agent doc updates

### `image-video-gen.agent.md`
- Phase 5.7 (Build Scene Config): document the `in`/`out` schema, the `motionEffect: "none"` static-landscape default, the subtle-motion-on-selected-scenes rule, and the SFX/transition auto-selection guidance.

### `remotion-compilation.agent.md`
- `scene-config.json Format` section: add the `in`/`out` fields and the conflict-resolution rule.
- Add a **Transition + SFX Selection** reference table (prompt signal → transition + sfx).
- Update the **Motion Effect Reference** to include `none` (static, recommended default for AR-matching landscape).
- Note the variable-transition duration math and that total frames stay `sum(D·fps)`.

## Execution (after implementation)

1. Regenerate `output/20260618_upnormal/scene-config.json` in the new format (static-by-default + auto transitions + selective SFX, subtle motion on a few scenes).
2. Render **no captions** in the background:
   `REMOTION_PUBLIC_DIR=./output/20260618_upnormal ./node_modules/.bin/remotion render main-no-captions --output ./output/20260618_upnormal/remotion_compiled_no_captions.mp4 --codec h264`
3. Wait ~10–15 min for completion; report output size + duration.

## Out of scope
- No changes to TTS, image generation, scripting, or caption components.
- No new transition library beyond `@remotion/transitions` (already installed) and `@remotion/sfx`.
- Portrait pipeline behavior is unchanged except that `none` becomes an allowed `motionEffect`.

## Verification
- `npm run lint` (eslint + tsc) passes after template changes.
- A no-captions render of `20260618_upnormal` completes with duration ≈ audio length (`sum(D)` ≈ 538s) and full (uncropped) images on static scenes.
