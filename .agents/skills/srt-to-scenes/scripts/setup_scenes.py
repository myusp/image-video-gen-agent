#!/usr/bin/env python3
"""Setup scene folders from an SRT transcript + optional audio file.

Groups SRT entries into scenes at natural sentence breaks,
creates scene_N/ folders, writes per-scene subtitles_N.txt and subtitle_N.srt,
optionally copies the full audio as audio_full.mp3, and writes scene_times.json
for use by split_audio.py.

Usage:
    python setup_scenes.py <project_folder> --srt <path/to/file.srt> \
        [--audio <path/to/audio.mp3>] \
        [--target-duration 13] \
        [--max-duration 15]

Examples:
    python .agents/skills/srt-to-scenes/scripts/setup_scenes.py \
        output/20260417_my-video \
        --srt "recording.srt" \
        --audio "recording.mp3"

    python .agents/skills/srt-to-scenes/scripts/setup_scenes.py \
        output/20260417_my-video \
        --srt "recording.srt" \
        --target-duration 10 \
        --max-duration 14
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path


def parse_srt_time(time_str: str) -> float:
    """Convert SRT timestamp (HH:MM:SS,mmm) to seconds."""
    time_str = time_str.strip().replace(",", ".")
    parts = time_str.split(":")
    h = int(parts[0])
    m = int(parts[1])
    s = float(parts[2])
    return h * 3600 + m * 60 + s


def parse_srt(srt_path: Path):
    """Parse SRT file into list of (start_sec, end_sec, text) tuples."""
    content = srt_path.read_text(encoding="utf-8")
    blocks = re.split(r"\n\s*\n", content.strip())
    entries = []
    for block in blocks:
        lines = [line.strip() for line in block.strip().split("\n") if line.strip()]
        if len(lines) < 3:
            continue
        ts_line = None
        text_lines = []
        for i, line in enumerate(lines):
            if "-->" in line:
                ts_line = line
                text_lines = lines[i + 1:]
                break
        if not ts_line:
            continue
        start_str, end_str = ts_line.split("-->")
        start = parse_srt_time(start_str)
        end = parse_srt_time(end_str)
        raw_text = " ".join(text_lines)
        # Remove common transcription watermarks
        raw_text = re.sub(r"\(Transcribed by TurboScribe[^)]*\)\s*", "", raw_text)
        raw_text = re.sub(r"\[.*?transcribed.*?\]\s*", "", raw_text, flags=re.IGNORECASE)
        # Sanitize long dashes — caption rendering artifacts
        raw_text = raw_text.replace("\u2014", ",").replace("\u2013", "-")
        raw_text = raw_text.strip()
        if raw_text:
            entries.append((start, end, raw_text))
    return entries


def ends_sentence(text: str) -> bool:
    """Return True if text ends at a natural sentence boundary."""
    t = text.rstrip()
    return t.endswith((".", "?", "!", ":"))


def group_into_scenes(entries, target_dur: float = 13.0, max_dur: float = 15.0):
    """Group SRT entries into scenes.

    Rules:
    - Keep adding entries until target_dur is reached AND entry ends a sentence
    - Never exceed max_dur (force break regardless of sentence boundary)
    - Merge trailing scene into previous if it would be < 6s
    """
    scenes = []
    current = []

    for start, end, text in entries:
        if not current:
            current.append((start, end, text))
            continue

        scene_start = current[0][0]
        projected_dur = end - scene_start
        current_dur = current[-1][1] - scene_start

        if projected_dur > max_dur:
            # Force break: adding this entry would exceed hard max
            scenes.append(current)
            current = [(start, end, text)]
        elif current_dur >= target_dur and ends_sentence(current[-1][2]):
            # Natural break: sentence ended and target duration reached
            scenes.append(current)
            current = [(start, end, text)]
        else:
            current.append((start, end, text))

    if current:
        # Merge last scene into previous if too short (< 6s)
        if scenes and (current[-1][1] - current[0][0]) < 6:
            scenes[-1].extend(current)
        else:
            scenes.append(current)

    return scenes


def build_srt_block(entries, offset: float = 0.0) -> str:
    """Build SRT content from entries, time-offset to scene start."""
    def fmt(sec: float) -> str:
        sec = max(0.0, sec)
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s_int = int(sec % 60)
        ms = int(round((sec - int(sec)) * 1000))
        return f"{h:02d}:{m:02d}:{s_int:02d},{ms:03d}"

    lines = []
    for i, (start, end, text) in enumerate(entries, 1):
        lines.append(str(i))
        lines.append(f"{fmt(start - offset)} --> {fmt(end - offset)}")
        lines.append(text)
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Group an SRT transcript into scene folders for video production."
    )
    parser.add_argument("project_folder", help="Output project folder (created if absent)")
    parser.add_argument("--srt", required=True, help="Path to the SRT transcript file")
    parser.add_argument(
        "--audio", default=None,
        help="Path to the full audio file. Copied as audio_full.mp3 if provided."
    )
    parser.add_argument(
        "--target-duration", type=float, default=13.0,
        help="Target seconds per scene (default: 13)"
    )
    parser.add_argument(
        "--max-duration", type=float, default=15.0,
        help="Hard max seconds per scene (default: 15)"
    )
    args = parser.parse_args()

    project_dir = Path(args.project_folder)
    srt_file = Path(args.srt)
    audio_file = Path(args.audio) if args.audio else None

    if not srt_file.exists():
        print(f"[ERROR] SRT file not found: {srt_file}", file=sys.stderr)
        sys.exit(1)
    if audio_file and not audio_file.exists():
        print(f"[ERROR] Audio file not found: {audio_file}", file=sys.stderr)
        sys.exit(1)

    project_dir.mkdir(parents=True, exist_ok=True)

    # Copy full audio
    if audio_file:
        dst_audio = project_dir / "audio_full.mp3"
        if not dst_audio.exists():
            shutil.copy2(audio_file, dst_audio)
            print(f"[OK] Copied audio -> {dst_audio}")
        else:
            print(f"[SKIP] audio_full.mp3 already exists")

    # Parse SRT
    entries = parse_srt(srt_file)
    print(f"[OK] Parsed {len(entries)} SRT entries from {srt_file.name}")

    # Group into scenes
    scenes = group_into_scenes(
        entries,
        target_dur=args.target_duration,
        max_dur=args.max_duration,
    )
    print(f"[OK] Grouped into {len(scenes)} scenes "
          f"(target={args.target_duration}s, max={args.max_duration}s)")

    # Write scene_times.json — used by split_audio.py
    scene_times = []

    for i, scene_entries in enumerate(scenes, 1):
        scene_dir = project_dir / f"scene_{i}"
        scene_dir.mkdir(exist_ok=True)

        scene_start = scene_entries[0][0]
        scene_end = scene_entries[-1][1]
        duration = scene_end - scene_start
        scene_times.append([round(scene_start, 3), round(scene_end, 3)])

        # Concatenate text for subtitle file (sanitize long dashes)
        full_text = " ".join(e[2] for e in scene_entries)
        full_text = re.sub(r"\s+", " ", full_text).strip()

        subtitle_path = scene_dir / f"subtitles_{i}.txt"
        if not subtitle_path.exists():
            subtitle_path.write_text(full_text, encoding="utf-8")

        # Write per-scene SRT (time-offset so it starts at 0:00:00)
        srt_path = scene_dir / f"subtitle_{i}.srt"
        if not srt_path.exists():
            srt_content = build_srt_block(scene_entries, offset=scene_start)
            srt_path.write_text(srt_content, encoding="utf-8")

        print(f"  scene_{i:02d}: {scene_start:7.2f}s - {scene_end:7.2f}s "
              f"({duration:5.1f}s) | {full_text[:65]}")

    times_path = project_dir / "scene_times.json"
    times_path.write_text(json.dumps(scene_times, indent=2), encoding="utf-8")
    print(f"\n[OK] scene_times.json written ({len(scene_times)} scenes)")

    print(f"\n[DONE] Project folder: {project_dir}")
    print(f"       Total scenes  : {len(scenes)}")
    print(f"       Next step     : Run split_audio.py to cut audio per scene")
    print(f"                       (or generate TTS with edge-tts/generate_tts.py)")


if __name__ == "__main__":
    main()
