#!/usr/bin/env python3
"""Generate scene images for funfact-planet-mars using Pollinations API."""

import os
import requests
from pathlib import Path
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("POLLINATIONS_API_KEY") or os.getenv("POLLINATION_API_KEY")
if not API_KEY:
    raise EnvironmentError("POLLINATIONS_API_KEY is not set in .env")

PROJECT_DIR = Path("output/20260411_funfact-planet-mars")
MODEL = "flux"
WIDTH = 1080
HEIGHT = 1920

scenes = list(range(1, 7))

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
