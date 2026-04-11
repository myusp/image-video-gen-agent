#!/usr/bin/env python3
"""Generate TTS audio + SRT for all scenes, then concatenate full audio and merge SRT."""

import asyncio
import os
import re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

try:
    import edge_tts
except ImportError:
    raise ImportError("Run: pip install edge-tts")

PROJECT_DIR = Path("output/20260411_funfact-planet-mars")
VOICE = os.getenv("EDGE_TTS_NAME", "id-ID-ArdiNeural").strip()
WORD_BREAK = int(os.getenv("WORD_BREAK_SUBTITLE", "4"))
NUM_SCENES = 6


def parse_srt_time(t: str) -> float:
    """Convert SRT timestamp to seconds."""
    h, m, rest = t.split(":")
    s, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def seconds_to_srt(sec: float) -> str:
    """Convert seconds back to SRT timestamp."""
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(round((sec - int(sec)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def group_srt_words(raw_srt: str, words_per_block: int) -> str:
    """Group word-level SRT into blocks of N words."""
    pattern = re.compile(
        r"\d+\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\n|\Z)",
        re.DOTALL,
    )
    entries = pattern.findall(raw_srt)
    if not entries:
        return raw_srt

    grouped = []
    idx = 1
    i = 0
    while i < len(entries):
        chunk = entries[i : i + words_per_block]
        start = chunk[0][0]
        end = chunk[-1][1]
        text = " ".join(e[2].strip() for e in chunk)
        grouped.append(f"{idx}\n{start} --> {end}\n{text}")
        idx += 1
        i += words_per_block

    return "\n\n".join(grouped) + "\n"


async def generate_scene_tts(scene_num: int) -> float:
    """Generate audio + grouped SRT for one scene. Returns audio duration in seconds."""
    scene_dir = PROJECT_DIR / f"scene_{scene_num}"
    audio_path = scene_dir / f"audio_{scene_num}.mp3"
    srt_path = scene_dir / f"subtitle_{scene_num}.srt"
    text_path = scene_dir / f"subtitles_{scene_num}.txt"

    text = text_path.read_text(encoding="utf-8").strip()

    if audio_path.exists() and srt_path.exists():
        print(f"[SKIP] scene_{scene_num} TTS already exists")
    else:
        print(f"[TTS]  scene_{scene_num}: {text[:60]}...")
        comm = edge_tts.Communicate(text=text, voice=VOICE, rate="+0%")
        raw_srt_path = scene_dir / f"_raw_subtitle_{scene_num}.srt"
        await comm.save(str(audio_path), str(raw_srt_path))

        raw_srt = raw_srt_path.read_text(encoding="utf-8")
        grouped = group_srt_words(raw_srt, WORD_BREAK)
        srt_path.write_text(grouped, encoding="utf-8")
        raw_srt_path.unlink(missing_ok=True)
        print(f"[OK]   audio saved: {audio_path}")

    # Measure audio duration via SRT last timestamp
    srt_content = srt_path.read_text(encoding="utf-8")
    ends = re.findall(r"\d{2}:\d{2}:\d{2},\d{3} --> (\d{2}:\d{2}:\d{2},\d{3})", srt_content)
    duration = parse_srt_time(ends[-1]) if ends else 10.0
    return duration


def offset_srt(srt_content: str, offset_sec: float, start_index: int) -> tuple[str, int]:
    """Shift all timestamps in SRT by offset_sec and renumber from start_index."""
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


async def main():
    durations = []
    for i in range(1, NUM_SCENES + 1):
        dur = await generate_scene_tts(i)
        durations.append(dur)
        print(f"      duration: {dur:.2f}s")

    # Concatenate all audio with ffmpeg
    full_audio = PROJECT_DIR / "audio_full.mp3"
    if not full_audio.exists():
        concat_list = PROJECT_DIR / "_concat_list.txt"
        lines = [f"file '{Path('scene_' + str(i)) / ('audio_' + str(i) + '.mp3')}'" for i in range(1, NUM_SCENES + 1)]
        concat_list.write_text("\n".join(lines), encoding="utf-8")

        import subprocess
        result = subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-c", "copy", str(full_audio)],
            cwd=str(PROJECT_DIR),
            capture_output=True,
            text=True,
        )
        concat_list.unlink(missing_ok=True)
        if result.returncode == 0:
            print(f"[OK]  Merged audio: {full_audio}")
        else:
            print(f"[WARN] ffmpeg concat failed: {result.stderr[:200]}")
    else:
        print(f"[SKIP] audio_full.mp3 already exists")

    # Merge all SRTs into one
    merged_srt_path = PROJECT_DIR / "subtitles.srt"
    merged_blocks = []
    cumulative = 0.0
    idx = 1
    for i, dur in enumerate(durations, start=1):
        srt_path = PROJECT_DIR / f"scene_{i}" / f"subtitle_{i}.srt"
        srt_content = srt_path.read_text(encoding="utf-8")
        shifted, idx = offset_srt(srt_content, cumulative, idx)
        merged_blocks.append(shifted)
        cumulative += dur

    merged_srt_path.write_text("\n\n".join(merged_blocks), encoding="utf-8")
    print(f"[OK]  Merged SRT: {merged_srt_path}")
    print(f"\nTotal estimated duration: {cumulative:.1f}s")


asyncio.run(main())
