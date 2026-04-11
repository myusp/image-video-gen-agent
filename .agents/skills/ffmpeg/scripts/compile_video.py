#!/usr/bin/env python3
"""
FFmpeg Compilation Agent
Compiles scene images + TTS audio into compiled.mp4 and compiled_with_burn_subtitle.mp4
Ken Burns motion is selected per scene based on prompt framing hints.
"""

import subprocess
import json
from pathlib import Path

PROJECT_DIR = Path("output/20260411_funfact-planet-mars")
W, H = 1080, 1920
FPS = 25

# --- Motion config per scene (derived from prompt framing hints) ---
# zoompan: z=zoom expr, x_expr/y_expr = pan offset
MOTIONS = {
    1: {
        "desc": "slow zoom in from center (extreme close-up)",
        "z": "min(1+on/%d*0.25,1.25)",
        "x": "iw/2-(iw/zoom/2)",
        "y": "ih/2-(ih/zoom/2)",
    },
    2: {
        "desc": "gentle pan right (illustration layout)",
        "z": "1.2",
        "x": "on/%d*(iw-iw/1.2)",
        "y": "ih/2-(ih/1.2/2)",
    },
    3: {
        "desc": "slow zoom out — wide establishing shot",
        "z": "max(1.3-on/%d*0.3,1.0)",
        "x": "iw/2-(iw/zoom/2)",
        "y": "ih/2-(ih/zoom/2)",
    },
    4: {
        "desc": "pan left — storm rolling across landscape",
        "z": "1.2",
        "x": "iw-iw/1.2-on/%d*(iw-iw/1.2)",
        "y": "ih/2-(ih/1.2/2)",
    },
    5: {
        "desc": "slow zoom in on Phobos — night sky",
        "z": "min(1+on/%d*0.3,1.3)",
        "x": "iw/2-(iw/zoom/2)",
        "y": "ih*0.3-(ih/zoom*0.3)",
    },
    6: {
        "desc": "slow zoom out — epic space wide shot",
        "z": "max(1.35-on/%d*0.35,1.0)",
        "x": "iw/2-(iw/zoom/2)",
        "y": "ih/2-(ih/zoom/2)",
    },
}


def get_duration(audio_path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(audio_path)],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())


def build_scene_clip(scene_num: int) -> Path:
    scene_dir = PROJECT_DIR / f"scene_{scene_num}"
    image = scene_dir / f"image_{scene_num}.jpeg"
    audio = scene_dir / f"audio_{scene_num}.mp3"
    output = scene_dir / f"clip_{scene_num}.mp4"

    if output.exists():
        print(f"[SKIP] clip_{scene_num}.mp4 already exists")
        return output

    dur = get_duration(audio)
    frames = int(dur * FPS) + 1
    m = MOTIONS[scene_num]

    z_expr = m["z"] % frames if "%d" in m["z"] else m["z"]
    x_expr = m["x"] % frames if "%d" in m["x"] else m["x"]
    y_expr = m["y"] % frames if "%d" in m["y"] else m["y"]

    zoompan = (
        f"zoompan=z='{z_expr}':x='{x_expr}':y='{y_expr}'"
        f":d={frames}:s={W}x{H}:fps={FPS}"
    )
    vf = f"{zoompan},format=yuv420p"

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(image),
        "-i", str(audio),
        "-vf", vf,
        "-c:v", "libx264", "-preset", "fast", "-crf", "22",
        "-c:a", "aac", "-b:a", "128k",
        "-t", str(dur),
        "-movflags", "+faststart",
        str(output),
    ]

    print(f"[CLIP] scene_{scene_num}: {m['desc']} ({dur:.2f}s, {frames}fr)")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERR]  scene_{scene_num}:\n{result.stderr[-500:]}")
        raise RuntimeError(f"ffmpeg failed for scene {scene_num}")
    print(f"[OK]   clip_{scene_num}.mp4")
    return output


def concatenate_clips(clips: list[Path], output: Path) -> None:
    if output.exists():
        print(f"[SKIP] {output.name} already exists")
        return

    concat_file = PROJECT_DIR / "_concat_clips.txt"
    # Use absolute paths so ffmpeg can find files regardless of cwd
    concat_file.write_text(
        "\n".join(f"file '{c.resolve()}'" for c in clips)
    )

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_file.resolve()),
        "-c", "copy",
        "-movflags", "+faststart",
        str(output.resolve()),
    ]
    print(f"\n[CONCAT] → {output.name}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    concat_file.unlink(missing_ok=True)
    if result.returncode != 0:
        print(f"[ERR]  concat:\n{result.stderr[-500:]}")
        raise RuntimeError("ffmpeg concat failed")
    size_mb = output.stat().st_size / 1024 / 1024
    print(f"[OK]   {output.name} ({size_mb:.1f}MB)")


def burn_subtitles(input_video: Path, srt: Path, output: Path) -> None:
    if output.exists():
        print(f"[SKIP] {output.name} already exists")
        return

    # Style: white bold text, black outline, bottom-center, good for vertical video
    style = (
        "FontName=Arial,FontSize=22,Bold=1,Alignment=2,"
        "MarginV=120,PrimaryColour=&H00FFFFFF,"
        "OutlineColour=&H00000000,Outline=2,Shadow=1"
    )
    # Absolute path, escape colons for ffmpeg filter syntax (macOS paths with no spaces)
    srt_abs = str(srt.resolve()).replace("\\", "/").replace(":", "\\:")
    vf = f"subtitles='{srt_abs}':force_style='{style}'"

    cmd = [
        "ffmpeg", "-y",
        "-i", str(input_video),
        "-vf", vf,
        "-c:v", "libx264", "-preset", "fast", "-crf", "22",
        "-c:a", "copy",
        "-movflags", "+faststart",
        str(output),
    ]
    print(f"\n[BURN]  → {output.name}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERR]  burn subtitles:\n{result.stderr[-800:]}")
        raise RuntimeError("subtitle burn failed")
    size_mb = output.stat().st_size / 1024 / 1024
    print(f"[OK]   {output.name} ({size_mb:.1f}MB)")


def main():
    print(f"=== FFmpeg Compilation — funfact-planet-mars ===\n")

    # Step 1: Build per-scene clips
    clips = []
    for i in range(1, 7):
        clip = build_scene_clip(i)
        clips.append(clip)

    # Step 2: Concatenate
    compiled = PROJECT_DIR / "compiled.mp4"
    concatenate_clips(clips, compiled)

    # Step 3: Burn subtitles
    srt = PROJECT_DIR / "subtitles.srt"
    compiled_sub = PROJECT_DIR / "compiled_with_burn_subtitle.mp4"
    burn_subtitles(compiled, srt, compiled_sub)

    # Summary
    print("\n=== Done ===")
    for f in [compiled, compiled_sub]:
        sz = f.stat().st_size / 1024 / 1024
        print(f"  {f.name}: {sz:.1f}MB")

    dur_total = sum(get_duration(PROJECT_DIR / f"scene_{i}" / f"audio_{i}.mp3") for i in range(1, 7))
    print(f"  Total duration: {dur_total:.1f}s")


if __name__ == "__main__":
    main()
