# Transition + SFX Driven Scenes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add per-scene `in`/`out` props (transition + SFX) to the video pipeline so AR-matching landscape images can be shown full-frame and static, with visual energy coming from auto-selected transitions and selective sound effects at the cut points.

**Architecture:** Scenes default to static `contain` images (zero crop); a minority of high-impact scenes get subtle `cover_subtle` motion. The shared Remotion template (`src/`) resolves one transition per cut from the config and layers `@remotion/sfx` sounds inside each scene. `build_config.py` auto-emits the new schema. Both agent docs document it.

**Tech Stack:** Remotion 4.0.448 (`@remotion/transitions`, `@remotion/sfx`, `@remotion/media`), React 19, TypeScript (strict), Python 3 (`build_config.py`).

**Verification reality:** No unit-test framework exists in this repo. Gates are `npm run lint` (= `eslint src && tsc`) for TypeScript and a `python -c` JSON check for the generator, then the final render.

---

### Task 1: Install `@remotion/sfx` and confirm export names

**Files:**
- Modify: `package.json` (dependencies)

- [ ] **Step 1: Install the package pinned to the Remotion version**

Run:
```bash
npm install @remotion/sfx@4.0.448
```
Expected: `package.json` gains `"@remotion/sfx": "4.0.448"`; `node_modules/@remotion/sfx` exists.

- [ ] **Step 2: Print the actual named exports (used in Task 3)**

Run:
```bash
node -e "const s=require('@remotion/sfx'); console.log(Object.keys(s).sort().join('\n'))"
```
Expected: a list of camelCase names. Record which of these exist (the Task 3 map must only reference confirmed names): `whoosh`, `whip`, `pageTurn`, `ding`, `vineBoom`, `triggered`, `uiSwitch`, `mouseClick`, `shutterModern`, `shutterOld`, `bruh`, `windowsXpError`. If a name above is absent, drop it from the Task 3 `SFX_MAP`; if extra useful names appear, they may be added.

- [ ] **Step 3: Commit**

```bash
git add package.json package-lock.json
git commit -m "build: add @remotion/sfx dependency"
```

---

### Task 2: Add `"none"` (static) motion effect to `SceneImage`

**Files:**
- Modify: `src/SceneImage.tsx`

- [ ] **Step 1: Add `"none"` to the `MotionEffect` union**

In `src/SceneImage.tsx`, change the type:
```tsx
export type MotionEffect =
  | "zoom_in"
  | "zoom_out"
  | "pan_left_right"
  | "pan_right_left"
  | "pan_up_down"
  | "pan_down_up"
  | "ken_burns"
  | "none";
```

- [ ] **Step 2: Handle `"none"` in both branches of `computeMotion`**

In `computeMotion`, add a `none` case to the `cover_full` switch (right after `case "zoom_in":`) and to the `cover_subtle` switch. The case returns an identity transform:
```tsx
      case "none":
        return { scale: 1, translateX: "0%", translateY: "0%" };
```
Add the identical case to **both** switch statements so TypeScript exhaustiveness is satisfied and a static scene applies `scale(1) translate(0%, 0%)` (a no-op).

- [ ] **Step 3: Verify lint + types pass**

Run:
```bash
npm run lint
```
Expected: PASS (no eslint errors, `tsc` exits 0).

- [ ] **Step 4: Commit**

```bash
git add src/SceneImage.tsx
git commit -m "feat(template): add 'none' static motion effect"
```

---

### Task 3: Add SFX map and per-cut transitions + SFX to `Main`

**Files:**
- Create: `src/sfx.ts`
- Modify: `src/Main.tsx`

- [ ] **Step 1: Create the SFX name→URL map**

Create `src/sfx.ts` (include only export names confirmed in Task 1 Step 2; the set below is the expected baseline):
```ts
import {
  whoosh,
  whip,
  pageTurn,
  ding,
  vineBoom,
  triggered,
  uiSwitch,
  mouseClick,
} from "@remotion/sfx";

// Maps a scene-config `sfx` string to a @remotion/sfx hosted URL.
// Keys are the strings used in scene-config.json `in.sfx` / `out.sfx`.
export const SFX_MAP: Record<string, string> = {
  whoosh,
  whip,
  pageTurn,
  ding,
  vineBoom,
  triggered,
  uiSwitch,
  mouseClick,
};
```

- [ ] **Step 2: Rewrite `src/Main.tsx` with per-cut transitions + SFX**

Replace the entire contents of `src/Main.tsx` with:
```tsx
import { AbsoluteFill, Sequence, staticFile } from "remotion";
import { Audio } from "@remotion/media";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import type { TransitionPresentation } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { wipe } from "@remotion/transitions/wipe";
import { flip } from "@remotion/transitions/flip";
import { clockWipe } from "@remotion/transitions/clock-wipe";
import { none } from "@remotion/transitions/none";
import { SceneImage } from "./SceneImage";
import type { MotionEffect, RenderMode } from "./SceneImage";
import { CaptionOverlay } from "./CaptionOverlay";
import type { CaptionStyle } from "./CaptionOverlay";
import { SFX_MAP } from "./sfx";

const FPS = 30;
const DEFAULT_TRANSITION_FRAMES = 15;
const SFX_OUT_LEAD = 12; // frames before scene end that out.sfx fires (~0.4s)
const SFX_VOLUME = 0.6;

export interface SceneTransition {
  transition?: string | null;
  durationInFrames?: number;
  sfx?: string | null;
}

export interface SceneConfig {
  sceneNumber: number;
  imagePath: string;
  audioPath: string;
  durationSeconds: number;
  motionEffect: MotionEffect;
  renderMode?: RenderMode;
  in?: SceneTransition;
  out?: SceneTransition;
}

interface Props {
  sceneConfig: SceneConfig[];
  withCaptions: boolean;
  captionStyle?: CaptionStyle;
  renderMode?: RenderMode;
  frameWidth: number;
  frameHeight: number;
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function buildPresentation(
  name: string | null | undefined,
  frameWidth: number,
  frameHeight: number,
): TransitionPresentation<any> {
  switch (name) {
    case "slide-from-left":
      return slide({ direction: "from-left" });
    case "slide-from-right":
      return slide({ direction: "from-right" });
    case "slide-from-top":
      return slide({ direction: "from-top" });
    case "slide-from-bottom":
      return slide({ direction: "from-bottom" });
    case "wipe-from-left":
      return wipe({ direction: "from-left" });
    case "wipe-from-right":
      return wipe({ direction: "from-right" });
    case "wipe-from-top":
      return wipe({ direction: "from-top" });
    case "wipe-from-bottom":
      return wipe({ direction: "from-bottom" });
    case "flip":
      return flip();
    case "clock-wipe":
      return clockWipe({ width: frameWidth, height: frameHeight });
    case "none":
      return none();
    case "fade":
    default:
      return fade();
  }
}

// Resolve the single transition used at the cut between cur and next.
// Precedence: next.in.transition -> cur.out.transition -> "fade".
function resolveCut(cur: SceneConfig, next: SceneConfig) {
  const fromNext = next.in?.transition;
  if (fromNext) {
    return {
      name: fromNext,
      durationInFrames: next.in?.durationInFrames ?? DEFAULT_TRANSITION_FRAMES,
    };
  }
  const fromCur = cur.out?.transition;
  if (fromCur) {
    return {
      name: fromCur,
      durationInFrames: cur.out?.durationInFrames ?? DEFAULT_TRANSITION_FRAMES,
    };
  }
  return { name: "fade", durationInFrames: DEFAULT_TRANSITION_FRAMES };
}

export const Main: React.FC<Props> = ({
  sceneConfig,
  withCaptions,
  captionStyle = "tiktok",
  renderMode: defaultRenderMode = "auto",
  frameWidth,
  frameHeight,
}) => {
  const children: React.ReactNode[] = [];
  sceneConfig.forEach((scene, index) => {
    const isLast = index === sceneConfig.length - 1;
    const sceneDurationInFrames = Math.round(scene.durationSeconds * FPS);
    // The cut after this scene (null for the last scene).
    const cut = isLast ? null : resolveCut(scene, sceneConfig[index + 1]);
    // Extend the scene by exactly this cut's transition frames so the
    // TransitionSeries overlap cancels: total == sum(round(D*FPS)).
    const durationInFrames =
      sceneDurationInFrames + (cut ? cut.durationInFrames : 0);
    const sceneRenderMode = scene.renderMode ?? defaultRenderMode;

    const inSfx = scene.in?.sfx ? SFX_MAP[scene.in.sfx] : undefined;
    const outSfx = scene.out?.sfx ? SFX_MAP[scene.out.sfx] : undefined;

    children.push(
      <TransitionSeries.Sequence
        key={`scene-${scene.sceneNumber}`}
        durationInFrames={durationInFrames}
      >
        <AbsoluteFill>
          <SceneImage
            imagePath={scene.imagePath}
            effect={scene.motionEffect}
            sceneDurationInFrames={sceneDurationInFrames}
            renderMode={sceneRenderMode}
            frameWidth={frameWidth}
            frameHeight={frameHeight}
          />
          {inSfx && <Audio src={inSfx} volume={SFX_VOLUME} />}
          {outSfx && (
            <Sequence
              from={Math.max(0, sceneDurationInFrames - SFX_OUT_LEAD)}
              layout="none"
            >
              <Audio src={outSfx} volume={SFX_VOLUME} />
            </Sequence>
          )}
        </AbsoluteFill>
      </TransitionSeries.Sequence>,
    );

    if (cut) {
      children.push(
        <TransitionSeries.Transition
          key={`transition-${scene.sceneNumber}`}
          presentation={buildPresentation(cut.name, frameWidth, frameHeight)}
          timing={linearTiming({ durationInFrames: cut.durationInFrames })}
        />,
      );
    }
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <Audio src={staticFile("audio_full.mp3")} />
      <TransitionSeries>{children}</TransitionSeries>
      {withCaptions && <CaptionOverlay captionStyle={captionStyle} />}
    </AbsoluteFill>
  );
};
```

Note: `Root.tsx` imports `SceneConfig` from `Main.tsx`, so the added optional `in`/`out` fields propagate automatically — **no change to `Root.tsx`** and total-frames math (`sum(round(D*FPS))`) stays valid.

- [ ] **Step 3: Verify lint + types pass**

Run:
```bash
npm run lint
```
Expected: PASS. If `tsc` complains that a `clockWipe` argument or `slide`/`wipe` direction type is wrong, consult the installed types: `node -e "console.log(require.resolve('@remotion/transitions/package.json'))"` and adjust the call to match — do not loosen with `any` beyond the single documented `buildPresentation` return.

- [ ] **Step 4: Commit**

```bash
git add src/sfx.ts src/Main.tsx
git commit -m "feat(template): per-cut transitions and per-scene SFX from config"
```

---

### Task 4: Emit the new schema from `build_config.py`

**Files:**
- Modify: `.agents/skills/srt-to-scenes/scripts/build_config.py`

- [ ] **Step 1: Replace `build_config.py` with the schema-aware generator**

Replace the entire contents of `.agents/skills/srt-to-scenes/scripts/build_config.py` with:
```python
#!/usr/bin/env python3
"""Generate scene-config.json for Remotion compilation.

Reads audio_durations.json and per-scene prompt_N.txt to build the full
scene configuration for the shared Remotion template. Scenes default to
static, full-frame `contain` images (motionEffect "none", renderMode
"contain_blur"); a capped minority of high-impact scenes get subtle motion.
Visual energy comes from auto-selected per-scene `in` transitions and
selective SFX.

Usage:
    python build_config.py <project_folder> [--orientation landscape|portrait]
                           [--motion-cap 0.2] [--no-sfx]
"""

import argparse
import json
import sys
from pathlib import Path

ORIENTATIONS = {
    "landscape": {"width": 1920, "height": 1080},
    "portrait": {"width": 1080, "height": 1920},
}

# Transition selection from prompt content. The transition is the one used to
# ENTER the scene (its `in.transition`). Scene 1 gets null (nothing precedes it).
TRANSITION_MAP = [
    (["action", "movement", "running", "chase", "speed", "fight",
      "dynamic", "energetic", "boxing", "crush", "collaps", "break"], "slide"),
    (["momentum", "accelerat", "growth", "rising", "launch", "rocket",
      "upgrade", "scaling", "expand", "timeline", "progress"], "wipe"),
    (["reveal", "introduction", "hero", "unveil", "appear", "emerge",
      "payoff", "twist", "fallen", "crown", "warning", "shocked"], "reveal"),
]
SLIDE_DIRS = ["from-left", "from-right"]
WIPE_DIRS = ["from-left", "from-right"]
REVEAL_TRANS = ["flip", "clock-wipe"]
DEFAULT_TRANSITION = "fade"

# Subtle-motion signals — scenes whose prompt matches may be promoted to
# cover_subtle motion (capped). Maps signal -> subtle motion effect.
MOTION_SIGNAL_MAP = [
    (["close-up", "close up", "detail", "macro", "face", "eyes", "portrait"], "zoom_in"),
    (["wide", "establishing", "landscape", "skyline", "aerial", "map", "panoram"], "zoom_out"),
    (["emotional", "dramatic", "cinematic", "hero", "reveal", "monologue"], "ken_burns"),
]


def select_transition(prompt: str, state: dict) -> str:
    t = prompt.lower()
    for kws, kind in TRANSITION_MAP:
        if any(k in t for k in kws):
            if kind == "slide":
                d = SLIDE_DIRS[state["slide"] % 2]
                state["slide"] += 1
                return f"slide-{d}"
            if kind == "wipe":
                d = WIPE_DIRS[state["wipe"] % 2]
                state["wipe"] += 1
                return f"wipe-{d}"
            if kind == "reveal":
                r = REVEAL_TRANS[state["reveal"] % 2]
                state["reveal"] += 1
                return r
    return DEFAULT_TRANSITION


def select_in_sfx(transition: str, state: dict, use_sfx: bool) -> str:
    """Selective SFX: not every cut. Avoids repeating the same sfx back-to-back."""
    if not use_sfx:
        return None
    candidate = None
    if transition.startswith("slide") or transition.startswith("wipe"):
        # Only every other qualifying cut, to avoid density.
        if state["shift_count"] % 2 == 0:
            candidate = ["whoosh", "whip"][state["whoosh"] % 2]
            state["whoosh"] += 1
        state["shift_count"] += 1
    elif transition in ("flip", "clock-wipe"):
        candidate = "ding"
    if candidate is not None and candidate == state["last_sfx"]:
        candidate = None  # never twice in a row
    if candidate is not None:
        state["last_sfx"] = candidate
    return candidate


def subtle_motion_for(prompt: str):
    t = prompt.lower()
    for kws, effect in MOTION_SIGNAL_MAP:
        if any(k in t for k in kws):
            return effect
    return None


def build_config(project_dir: Path, orientation: str, motion_cap: float, use_sfx: bool) -> None:
    dims = ORIENTATIONS[orientation]

    dur_path = project_dir / "audio_durations.json"
    if not dur_path.exists():
        print(
            f"[ERROR] audio_durations.json not found in {project_dir}\n"
            "        Run split_audio.py (SRT mode) or generate_tts.py (TTS mode) first.",
            file=sys.stderr,
        )
        sys.exit(1)

    durations = json.loads(dur_path.read_text(encoding="utf-8"))
    durations = {str(k): v for k, v in durations.items()}

    scene_dirs = sorted(
        [d for d in project_dir.iterdir() if d.is_dir() and d.name.startswith("scene_")],
        key=lambda d: int(d.name.split("_")[1]),
    )
    if not scene_dirs:
        print(f"[ERROR] No scene_N/ folders found in {project_dir}", file=sys.stderr)
        sys.exit(1)

    # First pass: gather valid scenes + prompts.
    raw = []
    for scene_dir in scene_dirs:
        n = int(scene_dir.name.split("_")[1])
        image_path = scene_dir / f"image_{n}.jpeg"
        audio_path = scene_dir / f"audio_{n}.mp3"
        prompt_path = scene_dir / f"prompt_{n}.txt"
        if not image_path.exists():
            print(f"[WARN] image_{n}.jpeg missing - skipping scene {n}")
            continue
        if not audio_path.exists():
            print(f"[WARN] audio_{n}.mp3 missing - skipping scene {n}")
            continue
        duration = durations.get(str(n))
        if duration is None:
            print(f"[WARN] No duration for scene {n} - using 12s default")
            duration = 12.0
        prompt_text = prompt_path.read_text(encoding="utf-8") if prompt_path.exists() else ""
        raw.append({"n": n, "duration": duration, "prompt": prompt_text})

    if not raw:
        print("[ERROR] No complete scenes found.", file=sys.stderr)
        sys.exit(1)

    # Decide subtle-motion scenes, capped.
    cap = max(1, int(len(raw) * motion_cap))
    motion_assigned = 0
    motion_for = {}
    for item in raw:
        if motion_assigned >= cap:
            break
        eff = subtle_motion_for(item["prompt"])
        if eff:
            motion_for[item["n"]] = eff
            motion_assigned += 1

    state = {"slide": 0, "wipe": 0, "reveal": 0, "whoosh": 0,
             "shift_count": 0, "last_sfx": None}

    scenes = []
    log = []
    for idx, item in enumerate(raw):
        n = item["n"]
        # `in` transition = transition INTO this scene. Scene 1 has none.
        if idx == 0:
            in_transition = None
        else:
            in_transition = select_transition(item["prompt"], state)
        in_sfx = select_in_sfx(in_transition, state, use_sfx) if in_transition else None

        if n in motion_for:
            motion = motion_for[n]
            render_mode = "cover_subtle"
        else:
            motion = "none"
            render_mode = "contain_blur"

        scene = {
            "sceneNumber": n,
            "imagePath": f"scene_{n}/image_{n}.jpeg",
            "audioPath": f"scene_{n}/audio_{n}.mp3",
            "durationSeconds": item["duration"],
            "motionEffect": motion,
            "renderMode": render_mode,
            "in": {"transition": in_transition, "durationInFrames": 15, "sfx": in_sfx},
            "out": {"transition": None, "durationInFrames": 15, "sfx": None},
        }
        scenes.append(scene)
        log.append(
            f"scene_{n:02d}: motion={motion:9s} mode={render_mode:12s} "
            f"in={str(in_transition):16s} sfx={str(in_sfx)}"
        )
        print(f"  {log[-1]}")

    config = {
        "videoConfig": {
            "orientation": orientation,
            "width": dims["width"],
            "height": dims["height"],
            "renderMode": "contain_blur",
        },
        "scenes": scenes,
    }
    config_path = project_dir / "scene-config.json"
    config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[OK] scene-config.json written ({len(scenes)} scenes, "
          f"{motion_assigned} subtle-motion, {orientation} {dims['width']}x{dims['height']})")

    log_path = project_dir / "remotion_motions.txt"
    log_path.write_text("\n".join(log), encoding="utf-8")
    print("[OK] remotion_motions.txt written")


def main():
    parser = argparse.ArgumentParser(
        description="Generate scene-config.json (transition + SFX schema)."
    )
    parser.add_argument("project_folder")
    parser.add_argument("--orientation", choices=["landscape", "portrait"], default="landscape")
    parser.add_argument("--motion-cap", type=float, default=0.2,
                        help="Max fraction of scenes that get subtle motion (default 0.2)")
    parser.add_argument("--no-sfx", action="store_true", help="Disable SFX assignment")
    args = parser.parse_args()

    project_dir = Path(args.project_folder)
    if not project_dir.exists():
        print(f"[ERROR] Project folder not found: {project_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"[OK] Building config for: {project_dir} (orientation={args.orientation})")
    build_config(project_dir, args.orientation, args.motion_cap, not args.no_sfx)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Smoke-check the generator against the real project (no overwrite of the live config yet)**

Run it on a temp copy to confirm it produces valid schema:
```bash
python .agents/skills/srt-to-scenes/scripts/build_config.py output/20260618_upnormal --orientation landscape
python -c "import json; c=json.load(open('output/20260618_upnormal/scene-config.json')); s=c['scenes']; assert all('in' in x and 'out' in x and 'motionEffect' in x for x in s); print('OK', len(s), 'scenes;', sum(1 for x in s if x['motionEffect']!='none'), 'with motion;', sum(1 for x in s if x['in']['sfx']) , 'with in.sfx')"
```
Expected: prints `OK <N> scenes; <=20% with motion; <some> with in.sfx`, scene 1's `in.transition` is `null`. (This regenerates the upnormal config, which is intended — Task 6 renders from it.)

- [ ] **Step 3: Commit**

```bash
git add .agents/skills/srt-to-scenes/scripts/build_config.py output/20260618_upnormal/scene-config.json output/20260618_upnormal/remotion_motions.txt
git commit -m "feat(config): emit in/out transition + SFX schema, static-by-default landscape"
```

---

### Task 5: Update both agent docs

**Files:**
- Modify: `.github/agents/remotion-compilation.agent.md`
- Modify: `.github/agents/image-video-gen.agent.md`

- [ ] **Step 1: Update `remotion-compilation.agent.md` — scene-config Format B**

In the "Scene fields" list (the bulleted list under Format B), add after the `renderMode` bullet:
```markdown
- `in` (optional) — transition + SFX used to ENTER this scene: `{ "transition": <name|null>, "durationInFrames": <int, default 15>, "sfx": <sfxName|null> }`
- `out` (optional) — transition + SFX as this scene EXITS: same shape as `in`
```
And add `motionEffect` value `none` to its bullet: change the `motionEffect` line to list `none` (static, no transform) as an allowed value and the recommended default for AR-matching landscape.

- [ ] **Step 2: Add the conflict-resolution + duration note**

Immediately after the Format B "Scene fields" list, add:
```markdown
**Cut resolution (one transition per cut):** the transition between scene N and N+1 = `scenes[N+1].in.transition` if set, else `scenes[N].out.transition` if set, else `fade`. The cut duration follows whichever side supplied the transition (`durationInFrames`, default 15). SFX is independent: `in.sfx` fires at the scene's first frame (at the cut in), `out.sfx` fires ~12 frames before the scene ends. Variable per-cut transition durations keep total frames at `sum(round(D*FPS))` (audio stays in sync) because each scene is extended by exactly its own cut's frames.

**Transition values:** `fade`, `slide-from-left|right|top|bottom`, `wipe-from-left|right|top|bottom`, `flip`, `clock-wipe`, `none`.
**SFX values:** `@remotion/sfx` export names (`whoosh`, `whip`, `pageTurn`, `ding`, `vineBoom`, `triggered`, `uiSwitch`, `mouseClick`) or `null`.
```

- [ ] **Step 3: Update the Motion Effect Reference table**

In the "Effect Catalogue" table, add a row:
```markdown
| `none` | Static, full image (no transform) — recommended for AR-matching landscape | identity transform; pair with `contain_blur` |
```

- [ ] **Step 4: Add a Transition + SFX Selection section**

After the "Motion Selection from Prompt" table, add:
```markdown
## Transition + SFX Selection from Prompt

For each scene (scene 1 gets no `in.transition`), read `prompt_{x}.txt` and assign the `in` transition + selective SFX:

| Prompt signal | in.transition | in.sfx (selective) |
|---------------|---------------|--------------------|
| Action, movement, speed, fight, collapse | `slide-from-left` / `slide-from-right` (alternate) | `whoosh` / `whip` (every other cut) |
| Momentum, growth, launch, scaling, timeline | `wipe-from-left` / `wipe-from-right` (alternate) | `whoosh` / `whip` (every other cut) |
| Reveal, hero, payoff, twist, warning | `flip` / `clock-wipe` (alternate) | `ding` |
| Calm narration / continuation (default) | `fade` | none |

Rules: never repeat the same SFX on consecutive scenes; most cuts carry no SFX. Energy comes from transition variety, not constant sound.
```

- [ ] **Step 5: Update `image-video-gen.agent.md` Phase 5.7**

In Phase 5.7 (Build Scene Config), after the `build_config.py` command block, add:
```markdown
`build_config.py` now emits the **transition + SFX schema**: each scene gets `motionEffect` (default `"none"` = static full image, `renderMode: "contain_blur"`), an `in` object (transition into the scene + optional SFX), and an `out` object. A capped minority (default ≤20%, `--motion-cap`) of high-impact scenes (establishing / hero / emotional / reveal) are promoted to subtle motion (`cover_subtle`). This is the fix for AR-matching landscape images: full images shown statically, with energy from auto-selected transitions and selective `@remotion/sfx` sounds at the cuts. Use `--no-sfx` to disable SFX.
```

- [ ] **Step 6: Verify the docs render (no broken code fences) and commit**

Run:
```bash
grep -c '```' .github/agents/remotion-compilation.agent.md
```
Expected: an even number (balanced fences).

```bash
git add .github/agents/remotion-compilation.agent.md .github/agents/image-video-gen.agent.md
git commit -m "docs(agents): document in/out transition + SFX schema and static-landscape strategy"
```

---

### Task 6: Regenerate `upnormal` config and render (no captions) in background

**Files:**
- Modify: `output/20260618_upnormal/scene-config.json` (already regenerated in Task 4 Step 2)
- Output: `output/20260618_upnormal/remotion_compiled_no_captions.mp4`

- [ ] **Step 1: Confirm the regenerated config is the new format**

Run:
```bash
python -c "import json;c=json.load(open('output/20260618_upnormal/scene-config.json'));print('scenes',len(c['scenes']));print('scene1.in',c['scenes'][0]['in']);print('motion!=none',sum(1 for s in c['scenes'] if s['motionEffect']!='none'))"
```
Expected: scene1.in.transition is `None/null`; motion-count ≤ ~20% of scenes.

- [ ] **Step 2: Start the no-captions render in the background**

Run (background):
```bash
REMOTION_PUBLIC_DIR=./output/20260618_upnormal ./node_modules/.bin/remotion render main-no-captions \
  --output ./output/20260618_upnormal/remotion_compiled_no_captions.mp4 --codec h264
```
This renders ~538s of video and takes ~10–15 min. Run it with `run_in_background: true`.

- [ ] **Step 3: Wait for completion, then verify the output**

When the render finishes, verify:
```bash
ls -la output/20260618_upnormal/remotion_compiled_no_captions.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 output/20260618_upnormal/remotion_compiled_no_captions.mp4
```
Expected: file exists, non-trivial size (hundreds of MB), duration ≈ 538s (matches `audio_full.mp3`). If the render errors on a missing `@remotion/sfx` URL fetch, confirm network access and that `SFX_MAP` only references valid export URLs (Task 1 Step 2).

- [ ] **Step 4: Report results**

Report: resolved folder, scene count, number of subtle-motion scenes, number of SFX cuts, transition variety, output file size + duration.

---

## Self-Review Notes

- **Spec coverage:** schema (Task 3 + 4), `none` motion (Task 2), template per-cut transition + SFX (Task 3), `@remotion/sfx` install (Task 1), `build_config.py` (Task 4), both agent docs (Task 5), regenerate + background no-captions render (Task 6). All spec sections mapped.
- **Type consistency:** `SceneConfig.in/out` typed as `SceneTransition` in `Main.tsx`; `MotionEffect` includes `none` in `SceneImage.tsx` and is consumed by `Main.tsx`; `SFX_MAP` keys match the `sfx` strings emitted by `build_config.py` (`whoosh`, `whip`, `ding`).
- **No-placeholder check:** all code blocks are complete; verification uses real repo gates (`npm run lint`, `python -c`, `ffprobe`) since no test framework exists.
```
