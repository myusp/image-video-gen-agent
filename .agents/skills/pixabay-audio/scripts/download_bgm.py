#!/usr/bin/env python3
"""Search and download BGM from Pixabay for the Mars funfact video."""

import json
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PIXABAY_API_KEY")
if not API_KEY:
    raise EnvironmentError("PIXABAY_API_KEY is not set in .env")

PROJECT_DIR = Path("output/20260411_funfact-planet-mars")
AUDIO_DIR = PROJECT_DIR / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

MANIFEST_PATH = AUDIO_DIR / "audio_manifest.json"

# Video mood: documentary science, space = cinematic orchestral + epic
BGM_QUERIES = ["cinematic space documentary", "epic orchestral dramatic", "science documentary ambient"]


def search_pixabay_audio(query: str, per_page: int = 5) -> list[dict]:
    """Search Pixabay audio endpoint."""
    url = "https://pixabay.com/api/"
    params = {
        "key": API_KEY,
        "q": query,
        "category": "music",
        "per_page": per_page,
        "order": "popular",
        "safesearch": "true",
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json().get("hits", [])


def download_file(url: str, dest: Path) -> bool:
    if dest.exists():
        print(f"[SKIP] Already exists: {dest}")
        return True
    resp = requests.get(url, timeout=120)
    if resp.status_code != 200:
        print(f"[FAIL] Could not download {url}: HTTP {resp.status_code}")
        return False
    dest.write_bytes(resp.content)
    print(f"[OK]   Downloaded {dest.name} ({len(resp.content) // 1024}KB)")
    return True


bgm_manifest = []

for query in BGM_QUERIES:
    print(f"\n[SEARCH] BGM: '{query}'")
    hits = search_pixabay_audio(query)
    if not hits:
        print("  No results.")
        continue

    for hit in hits[:3]:
        # Pixabay image/music hits may have audio via pageURL or largeImageURL
        audio_url = hit.get("audio", hit.get("webformatURL", ""))
        page_url = hit.get("pageURL", "")
        duration = hit.get("duration", 0)
        tags = hit.get("tags", "")
        pixabay_id = hit.get("id", 0)

        print(f"  ID:{pixabay_id} tags:{tags[:50]} dur:{duration}s url:{audio_url[:60]}")

    # Use first result with a downloadable URL
    for hit in hits:
        # Try to get direct audio URL from various fields
        audio_url = (
            hit.get("audio")
            or hit.get("audioURL")
            or hit.get("webformatURL")
            or ""
        )

        if not audio_url or not audio_url.startswith("http"):
            continue

        # Only download music files
        if not any(ext in audio_url for ext in [".mp3", ".ogg", ".wav", "audio"]):
            # For image category hits, skip non-audio
            tags = hit.get("tags", "").lower()
            if "music" not in tags and "audio" not in tags:
                continue

        slug = query.replace(" ", "_")[:30]
        dest = AUDIO_DIR / f"bgm_{slug}_{hit['id']}.mp3"

        if download_file(audio_url, dest):
            bgm_manifest.append({
                "file": dest.name,
                "source": "pixabay",
                "pixabay_id": hit["id"],
                "query": query,
                "duration": hit.get("duration", 0),
                "page_url": hit.get("pageURL", ""),
                "assigned_to": "full_video",
            })
            break

# Save manifest
manifest = {"bgm": bgm_manifest, "sfx": []}
if MANIFEST_PATH.exists():
    existing = json.loads(MANIFEST_PATH.read_text())
    existing.setdefault("bgm", []).extend(bgm_manifest)
    manifest = existing

MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
print(f"\n[OK]  Manifest saved: {MANIFEST_PATH}")

if not bgm_manifest:
    print("\n[INFO] No BGM file downloaded (Pixabay image API doesn't serve audio directly).")
    print("       Create an empty manifest anyway for pipeline compatibility.")
    manifest = {"bgm": [], "sfx": [], "note": "Pixabay image API used — audio URLs not available. Use Pixabay website to manually download BGM."}
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
