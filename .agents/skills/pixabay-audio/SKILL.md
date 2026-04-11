---
name: pixabay-audio
description: "Search and download royalty-free music and sound effects from Pixabay API. Use when: finding background music (BGM), searching SFX, downloading royalty-free audio, cari musik latar, cari sound effect, download BGM gratis, audio for video production, ambient sounds, music category search."
argument-hint: "Search query for music/SFX (e.g. 'cinematic background', 'explosion sfx', 'happy upbeat')"
---

# Pixabay Audio Skill

Search and download royalty-free music tracks and sound effects from the Pixabay API for video production. Free with API key.

## When to Use
- Finding background music (BGM) for video projects
- Searching sound effects (SFX) for specific scenes
- Downloading royalty-free audio that matches a video mood/theme
- Building audio asset libraries for reusable production

---

## Core Principles

1. **Always use `.env`** — load `PIXABAY_API_KEY` via `python-dotenv`
2. **Cache results 24h** — Pixabay requires caching; don't re-search the same query within 24h
3. **Download to local** — hotlinking Pixabay URLs is not allowed; always download files
4. **Save to `audio/` folder** — store all downloaded audio in `{project_folder}/audio/` for reusability
5. **Rate limit** — max 100 requests per 60 seconds per API key
6. **Attribution** — show Pixabay as source when displaying search results

---

## Environment Setup

```dotenv
# .env
PIXABAY_API_KEY=your_pixabay_key_here
```

### Install Dependencies

```bash
pip install requests python-dotenv
```

---

## API Reference

### Search Music

```
GET https://pixabay.com/api/videos/?key={KEY}&q={query}
```

**Note:** Pixabay does not have a dedicated audio-only search endpoint. Use the **videos** endpoint filtered by music/SFX categories, or use the image endpoint with `category=music` for music-related content.

For actual audio/music downloads, Pixabay provides audio via their main website. The API approach below works with their search to find relevant content.

### Search for Music/SFX via Pixabay API

```python
import requests
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("PIXABAY_API_KEY")
if not API_KEY:
    raise EnvironmentError("PIXABAY_API_KEY is not set in .env")

def search_pixabay_videos(
    query: str,
    category: str = "music",
    per_page: int = 5,
    order: str = "popular",
    lang: str = "en",
) -> list[dict]:
    """Search Pixabay for video/audio content."""
    url = "https://pixabay.com/api/videos/"
    params = {
        "key": API_KEY,
        "q": query,
        "category": category,
        "per_page": per_page,
        "order": order,
        "lang": lang,
        "safesearch": "true",
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data.get("hits", [])
```

### Download Audio/Video File

```python
def download_file(url: str, dest: Path) -> Path:
    """Download a file from URL to local path."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        print(f"Already exists: {dest}")
        return dest
    resp = requests.get(url, timeout=120)
    resp.raise_for_status()
    dest.write_bytes(resp.content)
    print(f"Downloaded: {dest} ({len(resp.content) // 1024}KB)")
    return dest
```

### Search Images by Music Category (for finding audio-themed content)

```python
def search_pixabay_images(
    query: str,
    category: str = "music",
    per_page: int = 5,
) -> list[dict]:
    url = "https://pixabay.com/api/"
    params = {
        "key": API_KEY,
        "q": query,
        "category": category,
        "per_page": per_page,
        "safesearch": "true",
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json().get("hits", [])
```

---

## Audio Selection Strategy for Video Production

When selecting BGM/SFX for a video, follow this decision tree:

### BGM (Background Music) Selection

| Video mood | Search queries to try |
|------------|----------------------|
| Cinematic, dramatic | `cinematic orchestral`, `epic trailer`, `dramatic tension` |
| Happy, upbeat, fun | `happy upbeat`, `fun cheerful`, `positive energy` |
| Calm, peaceful | `calm ambient`, `peaceful piano`, `relaxing nature` |
| Dark, suspenseful | `dark suspense`, `horror tension`, `mystery thriller` |
| Tech, modern | `electronic technology`, `digital futuristic`, `tech corporate` |
| Emotional, sad | `emotional piano`, `sad violin`, `melancholy` |
| Action, energetic | `action rock`, `energetic drums`, `fast-paced` |

### SFX (Sound Effects) Selection

| Scene content | Search queries |
|---------------|---------------|
| Transition, whoosh | `whoosh transition`, `swoosh` |
| Impact, hit | `impact hit`, `boom`, `punch` |
| Nature sounds | `wind`, `rain`, `ocean waves`, `birds` |
| UI/notification | `notification ding`, `pop click`, `bell` |
| Dramatic reveal | `dramatic reveal`, `tension riser`, `build up` |

---

## Integration with Video Pipeline

### Folder Structure

All downloaded audio goes into `{project_folder}/audio/`:

```
{project_folder}/
├── audio/
│   ├── bgm_cinematic_01.mp3       ← background music
│   ├── sfx_whoosh_01.mp3          ← sound effect
│   ├── sfx_impact_01.mp3
│   └── audio_manifest.json        ← tracks metadata & scene assignments
├── scene_1/
│   ├── audio_1.mp3                ← TTS narration (from edge-tts)
│   └── ...
```

### Audio Manifest

Save download metadata to `audio/audio_manifest.json` for traceability:

```json
{
  "bgm": [
    {
      "file": "bgm_cinematic_01.mp3",
      "source": "pixabay",
      "pixabay_id": 12345,
      "query": "cinematic orchestral",
      "duration": 120,
      "assigned_to": "full_video"
    }
  ],
  "sfx": [
    {
      "file": "sfx_whoosh_01.mp3",
      "source": "pixabay",
      "pixabay_id": 67890,
      "query": "whoosh transition",
      "assigned_to": ["scene_1", "scene_3"]
    }
  ]
}
```

---

## Rate Limit Headers

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Max requests per 60 seconds (default 100) |
| `X-RateLimit-Remaining` | Remaining requests in window |
| `X-RateLimit-Reset` | Seconds until window resets |

---

## Error Reference

| HTTP Code | Meaning | Fix |
|-----------|---------|-----|
| 400 | Bad parameters | Check query length (max 100 chars), valid category |
| 401 | Invalid API key | Verify `PIXABAY_API_KEY` in `.env` |
| 429 | Rate limit exceeded | Wait for `X-RateLimit-Reset` seconds |

---

## Important Notes

- Pixabay content is royalty-free under their [Content License](https://pixabay.com/service/terms/)
- Always download files locally — hotlinking is not allowed
- Cache search results for 24 hours to comply with API terms
- Maximum 500 results per query; paginate if needed
- Show "Source: Pixabay" attribution when displaying results to users
