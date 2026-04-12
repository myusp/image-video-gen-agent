---
name: pollinations-python
description: "Python cross-platform scripts using Pollinations API (https://gen.pollinations.ai). Use when: generating images, generating video, generating audio/TTS, generating text, managing .env config for Pollinations API key, writing Python scripts for image gen, setting up python-dotenv, creating cross-OS compatible scripts, using OpenAI SDK with Pollinations base URL, uploading/downloading media from Pollinations, checking API balance or usage."
argument-hint: "What do you want to generate? (image/text/audio/video) and any special config"
---

# Pollinations Python Skill

Generate images, text, audio, and video using the [Pollinations API](https://gen.pollinations.ai) from Python — cross-platform (macOS, Linux, Windows) with `.env` for all config.

## When to Use
- Writing or reviewing Python scripts that call `https://gen.pollinations.ai`
- Setting up API key management via `.env` + `python-dotenv`
- Image generation (text-to-image, image-to-image, edits)
- Text generation via OpenAI-compatible SDK
- TTS / audio generation
- Video generation
- Checking pollen balance, usage, or key info

---

## Core Principles

1. **Always use `.env`** — never hardcode API keys; load with `python-dotenv`
2. **Cross-platform paths** — use `pathlib.Path` instead of string paths
3. **Single `requirements.txt`** — list all deps; pin where behaviour matters
4. **OpenAI SDK first** — prefer `openai` client with `base_url="https://gen.pollinations.ai"` over raw `requests` when the endpoint is OpenAI-compatible
5. **Fail loudly on missing env vars** — validate at startup, not at request time

---

## Environment Setup

### Required `.env` Keys

```dotenv
POLLINATIONS_API_KEY=sk_your_key_here

# Optional tuning
TARGET_VIDEO_DURATION=180
AUDIO_PROVIDER=edge-tts
EDGE_TTS_NAME=id-ID-ArdiNeural
```

### Install Dependencies

```bash
pip install openai python-dotenv requests pillow
```

Or add to `requirements.txt`:
```
openai>=1.0.0
python-dotenv>=1.0.0
requests>=2.31.0
pillow>=10.0.0
```

### Load `.env` in Every Script

```python
from dotenv import load_dotenv
import os

load_dotenv()  # reads .env in CWD or any parent

API_KEY = os.getenv("POLLINATIONS_API_KEY")
if not API_KEY:
    raise EnvironmentError("POLLINATIONS_API_KEY is not set in .env")
```

Run the environment checker any time setup is uncertain:
```bash
python .agents/skills/pollinations-python/scripts/check_env.py
```

---

## API Reference Docs

| Topic | File |
|-------|------|
| Image generation (text-to-image, edits, models) | [references/image-gen.md](./references/image-gen.md) |
| Environment & cross-platform setup | [references/env-setup.md](./references/env-setup.md) |

---

## Quick Patterns

### Text Generation (OpenAI SDK)

```python
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(
    base_url="https://gen.pollinations.ai",
    api_key=os.environ["POLLINATIONS_API_KEY"],
)

response = client.chat.completions.create(
    model="openai",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

### Image Generation (OpenAI SDK)

```python
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(
    base_url="https://gen.pollinations.ai/v1",
    api_key=os.environ["POLLINATIONS_API_KEY"],
)

response = client.images.generate(
    model="flux",
    prompt="a cat in space",
    size="1024x1024",
)
print(response.data[0].url)
```

### Save Image to Disk (Cross-Platform)

```python
import requests
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

def save_image(url: str, filename: str) -> Path:
    """Download image URL and save to output/ folder."""
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)  # works on all OS
    dest = output_dir / filename
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    dest.write_bytes(resp.content)
    return dest
```

### Audio / TTS

```python
import requests
from pathlib import Path
from dotenv import load_dotenv
import os
from urllib.parse import quote

load_dotenv()
API_KEY = os.environ["POLLINATIONS_API_KEY"]

def tts(text: str, voice: str = "nova", out: str = "speech.mp3") -> Path:
    url = f"https://gen.pollinations.ai/audio/{quote(text)}?voice={voice}"
    resp = requests.get(url, headers={"Authorization": f"Bearer {API_KEY}"}, timeout=120)
    resp.raise_for_status()
    dest = Path(out)
    dest.write_bytes(resp.content)
    return dest
```

### Check API Balance

```python
import requests
from dotenv import load_dotenv
import os

load_dotenv()
resp = requests.get(
    "https://gen.pollinations.ai/api/account/balance",
    headers={"Authorization": f"Bearer {os.environ['POLLINATIONS_API_KEY']}"},
)
print(resp.json())
```

---

## Cross-Platform Checklist

When writing or reviewing scripts, verify:

- [ ] All file paths use `pathlib.Path`, not string concatenation
- [ ] `.env` loaded with `python-dotenv` at the top of `main` / entry point
- [ ] No hardcoded API keys — all read from `os.getenv` or `os.environ`
- [ ] `requirements.txt` exists and lists all imports
- [ ] `mkdir` calls use `parents=True, exist_ok=True`
- [ ] Binary file writes use `.write_bytes()` not `open(..., 'w')` (important on Windows)
- [ ] Timeouts set on all `requests` calls
- [ ] `load_dotenv()` called before any `os.getenv` that reads API keys

---

## Error Codes Quick Reference

| HTTP | Meaning | Fix |
|------|---------|-----|
| 401 | Missing/invalid API key | Check `POLLINATIONS_API_KEY` in `.env` |
| 402 | Insufficient pollen balance | Top up at https://enter.pollinations.ai |
| 400 | Bad parameters | Check prompt, model name, size format |
| 500 | Server error | Retry with exponential backoff |

---

## Bundled Scripts

### `generate_images.py` — Batch scene image generation

Reads `prompt_N.txt` from each scene folder and calls the Pollinations image API to generate a JPEG. Defaults are tuned for the 9:16 short-form video pipeline (1080×1920 portrait).

**Install deps:**
```bash
pip install requests python-dotenv
```

**Configure `.env`:**
```
POLLINATIONS_API_KEY=your_key_here
```

**Run directly (no editing needed):**
```bash
# Portrait (default 1080×1920) — auto-detects scenes
python .agents/skills/pollinations-python/scripts/generate_images.py output/20260411_funfact-planet-mars

# Landscape (1920×1080)
python .agents/skills/pollinations-python/scripts/generate_images.py output/20260411_funfact-planet-mars --orientation landscape

# Custom model and dimensions
python .agents/skills/pollinations-python/scripts/generate_images.py output/20260411_funfact-planet-mars \
  --model nanobanana --width 1080 --height 1920
```

**CLI arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| `project_dir` | Yes | Path to the video output folder |
| `--model` | No | Image model (default: `flux`) |
| `--width` | No | Image width (default: auto from orientation) |
| `--height` | No | Image height (default: auto from orientation) |
| `--orientation` | No | `portrait` (1080×1920) or `landscape` (1920×1080) |

**Output per scene:** `scene_N/image_N.jpeg`

**Resumable:** Skips scenes where `image_N.jpeg` already exists.

> **Important:** Output must be `.jpeg` — Remotion's renderer requires JPEG format. Other formats will break rendering.
