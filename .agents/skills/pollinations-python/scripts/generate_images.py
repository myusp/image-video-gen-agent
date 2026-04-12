#!/usr/bin/env python3
"""Generate scene images using Pollinations API.

Usage:
    python .agents/skills/pollinations-python/scripts/generate_images.py <project_dir> [options]

    project_dir  — path to the video output folder

Options:
    --model MODEL    — image generation model (default: flux)
    --width WIDTH    — image width (default: 1080)
    --height HEIGHT  — image height (default: 1920)
    --orientation    — portrait or landscape (overrides width/height defaults)

Environment (.env):
    POLLINATIONS_API_KEY  — API key (required)
"""

import argparse
import os
import requests
from pathlib import Path
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("POLLINATIONS_API_KEY") or os.getenv("POLLINATION_API_KEY")
if not API_KEY:
    raise EnvironmentError("POLLINATIONS_API_KEY is not set in .env")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate scene images via Pollinations API")
    parser.add_argument("project_dir", type=str, help="Path to the video output folder")
    parser.add_argument("--model", type=str, default="flux", help="Image model (default: flux)")
    parser.add_argument("--width", type=int, default=None, help="Image width (default: 1080 portrait, 1920 landscape)")
    parser.add_argument("--height", type=int, default=None, help="Image height (default: 1920 portrait, 1080 landscape)")
    parser.add_argument("--orientation", type=str, choices=["portrait", "landscape"], default="portrait",
                        help="Video orientation (default: portrait)")
    return parser.parse_args()


_args = _parse_args()
PROJECT_DIR = Path(_args.project_dir)
MODEL = _args.model

# Determine dimensions based on orientation
if _args.width and _args.height:
    WIDTH = _args.width
    HEIGHT = _args.height
elif _args.orientation == "landscape":
    WIDTH = 1920
    HEIGHT = 1080
else:
    WIDTH = 1080
    HEIGHT = 1920

if not PROJECT_DIR.exists():
    raise FileNotFoundError(f"Project directory not found: {PROJECT_DIR}")

# Auto-detect scenes from scene_* folders
scenes = sorted(
    [int(d.name.split("_")[1]) for d in PROJECT_DIR.iterdir()
     if d.is_dir() and d.name.startswith("scene_")],
)
if not scenes:
    raise ValueError(f"No scene_* folders found in {PROJECT_DIR}")

for scene_num in scenes:
    scene_dir = PROJECT_DIR / f"scene_{scene_num}"
    image_path = scene_dir / f"image_{scene_num}.jpeg"

    if image_path.exists():
        print(f"[SKIP] scene_{scene_num} already exists")
        continue

    prompt_path = scene_dir / f"prompt_{scene_num}.txt"
    prompt = prompt_path.read_text(encoding="utf-8").strip()
    seed = scene_num * 42

    encoded = quote(prompt)
    url = (
        f"https://gen.pollinations.ai/image/{encoded}"
        f"?model={MODEL}&width={WIDTH}&height={HEIGHT}&seed={seed}&nologo=true"
    )

    print(f"[GEN] scene_{scene_num} seed={seed} ...")
    resp = requests.get(
        url,
        headers={"Authorization": f"Bearer {API_KEY}"},
        timeout=120,
    )
    resp.raise_for_status()

    image_path.write_bytes(resp.content)
    print(f"[OK]  Saved {image_path} ({len(resp.content) // 1024}KB)")

print("\nAll images done!")
