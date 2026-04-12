#!/usr/bin/env python3
"""Regenerate TTS SRT files using edge-tts 7.x SubMaker API (streaming).

Usage:
    python .agents/skills/edge-tts/scripts/regenerate_srt.py <project_dir> [num_scenes]

    project_dir  — path to the video output folder
    num_scenes   — number of scenes (optional, auto-detected from scene_* folders)

Environment (.env):
    EDGE_TTS_NAME         — voice name (default: id-ID-ArdiNeural)
    WORD_BREAK_SUBTITLE   — words per caption block (default: 4)
"""

import argparse
import asyncio
import os
import re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

try:
    import edge_tts
except ImportError:
    raise ImportError("Run: pip install edge-tts>=7.0")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Regenerate SRT from edge-tts SubMaker")
    parser.add_argument("project_dir", type=str, help="Path to the video output folder")
    parser.add_argument("num_scenes", type=int, nargs="?", default=0,
                        help="Number of scenes (auto-detected if omitted)")
    parser.add_argument("--voice", type=str, default=None, help="Override TTS voice name")
    return parser.parse_args()


def _detect_num_scenes(project_dir: Path) -> int:
    scene_dirs = sorted(project_dir.glob("scene_*"))
    return len(scene_dirs)


_args = _parse_args()
PROJECT_DIR = Path(_args.project_dir)
VOICE = _args.voice or os.getenv("EDGE_TTS_NAME", "id-ID-ArdiNeural").strip()
WORD_BREAK = int(os.getenv("WORD_BREAK_SUBTITLE", "4"))
NUM_SCENES = _args.num_scenes or _detect_num_scenes(PROJECT_DIR)

if not PROJECT_DIR.exists():
    raise FileNotFoundError(f"Project directory not found: {PROJECT_DIR}")
if NUM_SCENES == 0:
    raise ValueError(f"No scene_* folders found in {PROJECT_DIR}")


def parse_srt_time(t: str) -> float:
    h, m, rest = t.split(":")
    s, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def seconds_to_srt(sec: float) -> str:
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(round((sec - int(sec)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def group_srt_by_words(srt_content: str, words_per_block: int) -> str:
    """Post-process sentence-level SRT into N-word blocks."""
    pattern = re.compile(
        r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\n|\Z)",
        re.DOTALL,
    )
    entries = pattern.findall(srt_content)
    if not entries:
        return srt_content

    # Flatten all words with their sentence timing
    all_words = []
    for _, start, end, text in entries:
        words = text.strip().split()
        if not words:
            continue
        start_sec = parse_srt_time(start)
        end_sec = parse_srt_time(end)
        if len(words) == 1:
            all_words.append((start_sec, end_sec, words[0]))
        else:
            step = (end_sec - start_sec) / len(words)
            for i, word in enumerate(words):
                all_words.append((
                    start_sec + i * step,
                    start_sec + (i + 1) * step,
                    word
                ))

    grouped = []
    idx = 1
    for i in range(0, len(all_words), words_per_block):
        chunk = all_words[i: i + words_per_block]
        start = seconds_to_srt(chunk[0][0])
        end = seconds_to_srt(chunk[-1][1])
        text = " ".join(w[2] for w in chunk)
        grouped.append(f"{idx}\n{start} --> {end}\n{text}")
        idx += 1

    return "\n\n".join(grouped) + "\n"


async def regenerate_srt(scene_num: int) -> None:
    scene_dir = PROJECT_DIR / f"scene_{scene_num}"
    audio_path = scene_dir / f"audio_{scene_num}.mp3"
    srt_path = scene_dir / f"subtitle_{scene_num}.srt"
    text_path = scene_dir / f"subtitles_{scene_num}.txt"

    text = text_path.read_text(encoding="utf-8").strip()

    print(f"[TTS]  scene_{scene_num}: streaming + SubMaker ...")
    communicate = edge_tts.Communicate(text=text, voice=VOICE, rate="+0%")
    submaker = edge_tts.SubMaker()

    # Stream: collect audio + feed boundary events to SubMaker
    with open(audio_path, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                submaker.feed(chunk)

    raw_srt = submaker.get_srt()
    grouped = group_srt_by_words(raw_srt, WORD_BREAK)
    srt_path.write_text(grouped, encoding="utf-8")
    print(f"[OK]   subtitle_{scene_num}.srt ({len(grouped.splitlines())} lines)")


def offset_srt(srt_content: str, offset_sec: float, start_index: int) -> tuple[str, int]:
    pattern = re.compile(
        r"\d+\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\n|\Z)",
        re.DOTALL,
    )
    entries = pattern.findall(srt_content)
    result = []
    idx = start_index
    for start, end, text in entries:
        new_start = seconds_to_srt(parse_srt_time(start) + offset_sec)
        new_end = seconds_to_srt(parse_srt_time(end) + offset_sec)
        result.append(f"{idx}\n{new_start} --> {new_end}\n{text.strip()}")
        idx += 1
    return "\n\n".join(result) + "\n", idx


def get_audio_duration(audio_path: Path) -> float:
    import subprocess
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(audio_path)],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())


async def main():
    for i in range(1, NUM_SCENES + 1):
        await regenerate_srt(i)

    # Rebuild merged subtitles.srt
    merged_srt_path = PROJECT_DIR / "subtitles.srt"
    merged_blocks = []
    cumulative = 0.0
    idx = 1
    for i in range(1, NUM_SCENES + 1):
        dur = get_audio_duration(PROJECT_DIR / f"scene_{i}" / f"audio_{i}.mp3")
        srt_content = (PROJECT_DIR / f"scene_{i}" / f"subtitle_{i}.srt").read_text(encoding="utf-8")
        shifted, idx = offset_srt(srt_content, cumulative, idx)
        merged_blocks.append(shifted)
        cumulative += dur

    merged_srt_path.write_text("\n\n".join(merged_blocks), encoding="utf-8")
    print(f"\n[OK]  Merged subtitles.srt ({cumulative:.1f}s total)")


asyncio.run(main())
