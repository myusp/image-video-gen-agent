#!/usr/bin/env python3
"""Split the full audio into per-scene audio files using FFmpeg.

Reads scene timing from scene_times.json (written by setup_scenes.py),
then trims audio_full.mp3 into scene_N/audio_N.mp3 for each scene.
Measures actual durations with ffprobe and writes audio_durations.json.

Usage:
    python split_audio.py <project_folder>

Example:
    python .agents/skills/srt-to-scenes/scripts/split_audio.py \
        output/20260417_my-video

Prerequisites:
    - scene_times.json must exist in the project folder (run setup_scenes.py first)
    - audio_full.mp3 must exist in the project folder
    - ffmpeg and ffprobe must be installed and on PATH
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def split_audio(project_dir: Path, scene_times: list) -> list:
    """Split audio_full.mp3 into per-scene clips. Returns list of (n, start, end, dur)."""
    full_audio = project_dir / "audio_full.mp3"
    if not full_audio.exists():
        print(f"[ERROR] audio_full.mp3 not found in {project_dir}", file=sys.stderr)
        sys.exit(1)

    generated = []
    for i, (start, end) in enumerate(scene_times, 1):
        scene_dir = project_dir / f"scene_{i}"
        scene_dir.mkdir(exist_ok=True)
        out_path = scene_dir / f"audio_{i}.mp3"

        if out_path.exists():
            print(f"[SKIP] audio_{i}.mp3 already exists")
            generated.append((i, start, end, round(end - start, 3)))
            continue

        duration = end - start
        cmd = [
            "ffmpeg", "-y",
            "-i", str(full_audio),
            "-ss", str(start),
            "-t", str(duration),
            "-acodec", "libmp3lame",
            "-q:a", "2",
            str(out_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[OK] audio_{i}.mp3  ({start:.2f}s - {end:.2f}s, {duration:.2f}s)")
            generated.append((i, start, end, round(duration, 3)))
        else:
            print(f"[ERR] Failed audio_{i}: {result.stderr[-300:]}", file=sys.stderr)

    print(f"\n[DONE] Split {len(generated)} audio files")
    return generated


def measure_durations(project_dir: Path, n_scenes: int) -> dict:
    """Measure actual duration of each audio file using ffprobe."""
    durations = {}
    for i in range(1, n_scenes + 1):
        audio_path = project_dir / f"scene_{i}" / f"audio_{i}.mp3"
        if not audio_path.exists():
            print(f"[WARN] audio_{i}.mp3 not found — skipping duration measurement")
            continue
        cmd = [
            "ffprobe", "-v", "quiet",
            "-show_entries", "format=duration",
            "-of", "csv=p=0",
            str(audio_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            dur = float(result.stdout.strip())
            durations[str(i)] = round(dur, 3)
        else:
            print(f"[WARN] Could not measure duration for audio_{i}.mp3")
    return durations


def main():
    parser = argparse.ArgumentParser(
        description="Split audio_full.mp3 into per-scene clips using scene_times.json."
    )
    parser.add_argument("project_folder", help="Project folder containing scene_times.json and audio_full.mp3")
    args = parser.parse_args()

    project_dir = Path(args.project_folder)

    times_path = project_dir / "scene_times.json"
    if not times_path.exists():
        print(
            f"[ERROR] scene_times.json not found in {project_dir}\n"
            "        Run setup_scenes.py first to generate it.",
            file=sys.stderr,
        )
        sys.exit(1)

    scene_times = json.loads(times_path.read_text(encoding="utf-8"))
    print(f"[OK] Loaded {len(scene_times)} scene time ranges from scene_times.json")

    # Split audio
    split_audio(project_dir, scene_times)

    # Measure actual durations
    print("\nMeasuring actual audio durations via ffprobe...")
    durations = measure_durations(project_dir, len(scene_times))

    dur_path = project_dir / "audio_durations.json"
    dur_path.write_text(json.dumps(durations, indent=2), encoding="utf-8")
    print(f"[OK] Saved durations to {dur_path}")

    for i_str, dur in sorted(durations.items(), key=lambda x: int(x[0])):
        print(f"  scene_{int(i_str):02d}: {dur:.3f}s")

    print(f"\n[DONE] {len(durations)} durations written to audio_durations.json")
    print(f"       Next step: Generate image prompts (prompt_N.txt) per scene,")
    print(f"                  then run build_config.py to create scene-config.json")


if __name__ == "__main__":
    main()
