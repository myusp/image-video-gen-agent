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


def select_in_sfx(transition: str, state: dict, use_sfx: bool):
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

    # Decide subtle-motion scenes, capped. Collect ALL candidate scenes whose
    # prompt signals motion, then spread the capped selection EVENLY across the
    # timeline so motion is seasoning distributed through the whole video, not
    # front-loaded onto the first scenes.
    cap = max(1, int(len(raw) * motion_cap))
    candidates = [
        (item["n"], subtle_motion_for(item["prompt"]))
        for item in raw
        if subtle_motion_for(item["prompt"]) is not None
    ]
    motion_for = {}
    if candidates:
        if len(candidates) <= cap:
            chosen = candidates
        else:
            stride = len(candidates) / cap
            chosen = [candidates[int(k * stride)] for k in range(cap)]
        for n, eff in chosen:
            motion_for[n] = eff
    motion_assigned = len(motion_for)

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
