#!/usr/bin/env python3
"""Generate scene-config.json for Remotion compilation.

Reads audio_durations.json and per-scene prompt_N.txt to build the full
scene configuration for the shared Remotion template. Supports both
portrait (1080×1920) and landscape (1920×1080) orientations.

Usage:
    python build_config.py <project_folder> [--orientation landscape|portrait]

Examples:
    python .agents/skills/srt-to-scenes/scripts/build_config.py \
        output/20260417_my-video --orientation landscape

    python .agents/skills/srt-to-scenes/scripts/build_config.py \
        output/20260417_my-video --orientation portrait

Prerequisites:
    - audio_durations.json must exist (run split_audio.py or generate_tts.py first)
    - scene_N/image_N.jpeg and scene_N/audio_N.mp3 must exist for each scene
    - scene_N/prompt_N.txt should exist for motion-effect selection
      (scenes without a prompt fall back to the default motion)
"""

import argparse
import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Motion effect selection — keyword → effect mapping
# ---------------------------------------------------------------------------
MOTION_MAP = [
    (
        ["action", "movement", "running", "chase", "speed", "fight",
         "dynamic", "energetic", "flow"],
        "pan_left_right",
    ),
    (
        ["close-up", "detail", "macro", "face", "eyes", "texture",
         "close up", "zoom into", "portrait"],
        "zoom_in",
    ),
    (
        ["wide", "establishing", "landscape", "skyline", "crowd",
         "panoramic", "panorama", "aerial", "map"],
        "zoom_out",
    ),
    (
        ["reveal", "introduction", "hero", "character", "emerge",
         "appear", "unroll", "unveiling"],
        "ken_burns",
    ),
    (
        ["falling", "descending", "underwater", "rain", "drain",
         "siphon", "pouring"],
        "pan_up_down",
    ),
    (
        ["rising", "flying", "sky", "ascending", "hope", "rocket",
         "launching", "upward", "growth"],
        "pan_down_up",
    ),
    (
        ["dramatic", "emotional", "cinematic", "monologue", "dilemma",
         "question", "reflection"],
        "ken_burns",
    ),
]

DEFAULT_MOTION = "zoom_in"

ORIENTATIONS = {
    "landscape": {"width": 1920, "height": 1080},
    "portrait":  {"width": 1080, "height": 1920},
}


def select_motion(prompt_text: str) -> str:
    """Return a motion effect name based on keywords in the prompt."""
    text_lower = prompt_text.lower()
    for keywords, effect in MOTION_MAP:
        if any(kw in text_lower for kw in keywords):
            return effect
    return DEFAULT_MOTION


def build_config(project_dir: Path, orientation: str) -> None:
    dims = ORIENTATIONS[orientation]

    # Load audio durations
    dur_path = project_dir / "audio_durations.json"
    if not dur_path.exists():
        print(
            f"[ERROR] audio_durations.json not found in {project_dir}\n"
            "        Run split_audio.py (SRT mode) or generate_tts.py (TTS mode) first.",
            file=sys.stderr,
        )
        sys.exit(1)

    durations = json.loads(dur_path.read_text(encoding="utf-8"))
    # Support both int keys (legacy) and string keys
    durations = {str(k): v for k, v in durations.items()}

    scene_dirs = sorted(
        [d for d in project_dir.iterdir() if d.is_dir() and d.name.startswith("scene_")],
        key=lambda d: int(d.name.split("_")[1]),
    )

    if not scene_dirs:
        print(f"[ERROR] No scene_N/ folders found in {project_dir}", file=sys.stderr)
        sys.exit(1)

    scenes = []
    motion_log = []

    for scene_dir in scene_dirs:
        n = int(scene_dir.name.split("_")[1])

        image_path = scene_dir / f"image_{n}.jpeg"
        audio_path = scene_dir / f"audio_{n}.mp3"
        prompt_path = scene_dir / f"prompt_{n}.txt"

        if not image_path.exists():
            print(f"[WARN] image_{n}.jpeg missing — skipping scene {n}")
            continue
        if not audio_path.exists():
            print(f"[WARN] audio_{n}.mp3 missing — skipping scene {n}")
            continue

        duration = durations.get(str(n))
        if duration is None:
            print(f"[WARN] No duration for scene {n} in audio_durations.json — using 12s default")
            duration = 12.0

        prompt_text = prompt_path.read_text(encoding="utf-8") if prompt_path.exists() else ""
        motion = select_motion(prompt_text)

        scenes.append({
            "sceneNumber": n,
            "imagePath": f"scene_{n}/image_{n}.jpeg",
            "audioPath": f"scene_{n}/audio_{n}.mp3",
            "durationSeconds": duration,
            "motionEffect": motion,
        })

        motion_log.append(f"scene_{n:02d}: {motion} ({duration:.3f}s)")
        print(f"  scene_{n:02d}: {motion:20s}  {duration:.3f}s")

    if not scenes:
        print("[ERROR] No complete scenes found (need image_N.jpeg + audio_N.mp3 per scene).", file=sys.stderr)
        sys.exit(1)

    # Write scene-config.json
    config = {
        "videoConfig": {
            "orientation": orientation,
            "width": dims["width"],
            "height": dims["height"],
        },
        "scenes": scenes,
    }

    config_path = project_dir / "scene-config.json"
    config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[OK] scene-config.json written  ({len(scenes)} scenes, {orientation} {dims['width']}×{dims['height']})")

    # Write motion log
    log_path = project_dir / "remotion_motions.txt"
    log_path.write_text("\n".join(motion_log), encoding="utf-8")
    print(f"[OK] remotion_motions.txt written")

    print(f"\n[DONE] Ready to render with Remotion:")
    print(f"       REMOTION_PUBLIC_DIR=./{project_dir} npm run render:captions \\")
    print(f"         --output ./{project_dir}/remotion_compiled.mp4")


def main():
    parser = argparse.ArgumentParser(
        description="Generate scene-config.json for Remotion from audio_durations.json + scene assets."
    )
    parser.add_argument("project_folder", help="Project folder containing scene_N/ subfolders")
    parser.add_argument(
        "--orientation",
        choices=["landscape", "portrait"],
        default="landscape",
        help="Video orientation (default: landscape)",
    )
    args = parser.parse_args()

    project_dir = Path(args.project_folder)
    if not project_dir.exists():
        print(f"[ERROR] Project folder not found: {project_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"[OK] Building config for: {project_dir}  (orientation={args.orientation})")
    build_config(project_dir, args.orientation)


if __name__ == "__main__":
    main()
