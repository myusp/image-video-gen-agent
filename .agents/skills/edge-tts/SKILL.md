---
name: edge-tts
description: "Text-to-speech using Microsoft Edge TTS (edge-tts Python package). Use when: generating voice narration, TTS per scene, creating audio from text, converting script to speech, generating mp3 from subtitle text, voice synthesis for video narration, edge-tts voice list, changing TTS voice/rate/pitch/volume."
argument-hint: "Text to speak, voice name (optional), output path, rate/pitch/volume adjustments"
---

# Edge TTS Skill

Generate high-quality text-to-speech audio using Microsoft Edge's online TTS service via the `edge-tts` Python package. Free, no API key required.

## When to Use
- Converting script/subtitle text into spoken audio (MP3)
- Generating per-scene narration audio for video production
- Listing available voices and selecting by language/gender
- Adjusting speech rate, volume, or pitch
- Generating word-level SRT subtitles alongside audio

---

## Core Principles

1. **Use the Python module** — prefer `edge_tts.Communicate` over CLI for integration
2. **Always generate SRT alongside audio** — `communicate.save()` handles both, or use `--write-subtitles` in CLI
3. **Read voice config from `.env`** — use `EDGE_TTS_NAME` env var, fallback to `en-US-AriaNeural`
4. **Cross-platform paths** — use `pathlib.Path`
5. **Async by default** — `edge_tts` is async; use `asyncio.run()` at entry points

---

## Installation

```bash
pip install edge-tts
```

Add to `requirements.txt`:
```
edge-tts>=7.0.0
```

---

## Environment Config

```dotenv
# .env
EDGE_TTS_NAME=id-ID-ArdiNeural    # Voice name (see voice list below)
```

---

## Quick Patterns

### Generate Audio + SRT (Python — recommended)

```python
import asyncio
import edge_tts
from pathlib import Path

async def generate_tts(
    text: str,
    output_audio: Path,
    output_srt: Path,
    voice: str = "id-ID-ArdiNeural",
    rate: str = "+0%",
    volume: str = "+0%",
    pitch: str = "+0Hz",
) -> None:
    """Generate MP3 audio and word-level SRT from text."""
    output_audio.parent.mkdir(parents=True, exist_ok=True)
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        volume=volume,
        pitch=pitch,
    )
    await communicate.save(str(output_audio), str(output_srt))

# Usage
asyncio.run(generate_tts(
    text="Tahukah kamu bahwa Titanic punya kolam renang?",
    output_audio=Path("output/scene_1/audio_1.mp3"),
    output_srt=Path("output/scene_1/subtitle_1.srt"),
))
```

### Generate Audio Only (no SRT)

```python
import asyncio
import edge_tts
from pathlib import Path

async def tts_audio_only(text: str, output: Path, voice: str = "id-ID-ArdiNeural") -> None:
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(str(output))

asyncio.run(tts_audio_only("Hello world", Path("hello.mp3")))
```

### CLI Usage

```bash
# Basic generation with subtitles
edge-tts --text "Hello, world!" --write-media hello.mp3 --write-subtitles hello.srt

# With voice selection
edge-tts --voice id-ID-ArdiNeural --text "Halo dunia!" --write-media hello_id.mp3

# Adjust rate, volume, pitch
edge-tts --rate=-20% --volume=+10% --pitch=-10Hz --text "Slower and deeper" --write-media adjusted.mp3

# List all available voices
edge-tts --list-voices
```

### List Voices Programmatically

```python
import asyncio
import edge_tts

async def list_voices(language_prefix: str = "id-ID") -> list[dict]:
    voices = await edge_tts.list_voices()
    return [v for v in voices if v["ShortName"].startswith(language_prefix)]

voices = asyncio.run(list_voices("id-ID"))
for v in voices:
    print(f"{v['ShortName']:30s} {v['Gender']:8s} {v.get('Locale', '')}")
```

### Batch TTS for Multiple Scenes

```python
import asyncio
import edge_tts
from pathlib import Path

async def batch_tts(
    scenes: list[dict],  # [{"text": "...", "audio": Path, "srt": Path}, ...]
    voice: str = "id-ID-ArdiNeural",
    rate: str = "+0%",
) -> None:
    for scene in scenes:
        print(f"Generating TTS: {scene['audio']}")
        comm = edge_tts.Communicate(text=scene["text"], voice=voice, rate=rate)
        await comm.save(str(scene["audio"]), str(scene["srt"]))

# Example
scenes = [
    {
        "text": "Scene satu narasi...",
        "audio": Path("output/scene_1/audio_1.mp3"),
        "srt": Path("output/scene_1/subtitle_1.srt"),
    },
    {
        "text": "Scene dua narasi...",
        "audio": Path("output/scene_2/audio_2.mp3"),
        "srt": Path("output/scene_2/subtitle_2.srt"),
    },
]
asyncio.run(batch_tts(scenes))
```

---

## Popular Indonesian Voices

| Voice Name | Gender | Notes |
|------------|--------|-------|
| `id-ID-ArdiNeural` | Male | Clear, natural male voice |
| `id-ID-GadisNeural` | Female | Clear, natural female voice |

## Popular English Voices

| Voice Name | Gender | Notes |
|------------|--------|-------|
| `en-US-AriaNeural` | Female | Natural, expressive |
| `en-US-GuyNeural` | Male | Clear, professional |
| `en-US-JennyNeural` | Female | Friendly, warm |
| `en-GB-SoniaNeural` | Female | British English |
| `en-GB-RyanNeural` | Male | British English |

---

## Rate / Volume / Pitch Reference

| Parameter | Format | Examples |
|-----------|--------|----------|
| `rate` | `±N%` | `+20%`, `-30%`, `+0%` |
| `volume` | `±N%` | `+10%`, `-50%`, `+0%` |
| `pitch` | `±NHz` | `+50Hz`, `-20Hz`, `+0Hz` |

---

## SRT Output Format

Edge TTS generates word-level SRT timing. Example output:

```srt
1
00:00:00,000 --> 00:00:00,450
Tahukah

2
00:00:00,450 --> 00:00:00,800
kamu

3
00:00:00,800 --> 00:00:01,100
bahwa
```

This word-level timing can be used as-is for karaoke-style subtitles, or post-processed to group words using `WORD_BREAK_SUBTITLE` config (e.g., group every 4 words into one subtitle block).

---

## Error Reference

| Issue | Fix |
|-------|-----|
| `NoAudioReceived` | Check internet connection; Edge TTS requires online access |
| Voice not found | Run `edge-tts --list-voices` to verify voice name spelling |
| Garbled audio | Ensure text is in the same language as the selected voice |
| Timeout | Large text blocks may timeout; split into segments < 5000 chars |

---

## Bundled Scripts

Two ready-to-run scripts are in `.agents/skills/edge-tts/scripts/`:

### `generate_tts.py` — Full TTS + SRT pipeline

Generates per-scene TTS audio (`audio_N.mp3`) and word-level SRT captions (`subtitle_N.srt`), then concatenates all scenes into `audio_full.mp3` + merged `subtitles.srt`.

**Install deps:**
```bash
pip install edge-tts python-dotenv pydub
```

**Configure `.env`:**
```
EDGE_TTS_NAME=id-ID-ArdiNeural
WORD_BREAK_SUBTITLE=4   # words per caption block (default: 4)
```

**Run directly (no editing needed):**
```bash
# Auto-detects scene count from scene_* folders
python .agents/skills/edge-tts/scripts/generate_tts.py output/20260411_funfact-planet-mars

# Explicit scene count + voice override
python .agents/skills/edge-tts/scripts/generate_tts.py output/20260411_funfact-planet-mars 6 --voice en-US-AriaNeural

# With custom speech rate
python .agents/skills/edge-tts/scripts/generate_tts.py output/20260411_funfact-planet-mars --rate "+10%"
```

**CLI arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| `project_dir` | Yes | Path to the video output folder |
| `num_scenes` | No | Number of scenes (auto-detected from `scene_*` folders) |
| `--voice` | No | Override TTS voice (defaults to `EDGE_TTS_NAME` from `.env`) |
| `--rate` | No | Speech rate adjustment (default: `+0%`) |

**Per-scene outputs:**
- `scene_N/audio_N.mp3` — TTS audio clip
- `scene_N/subtitle_N.srt` — word-grouped SRT captions
- `scene_N/subtitles_N.txt` — plain-text captions

**Merged outputs:**
- `audio/audio_full.mp3` — all scenes concatenated
- `subtitles.srt` / `subtitles.txt` — merged caption file with per-scene time offsets

**Resumable:** Skips any scene where `audio_N.mp3` already exists.

---

### `regenerate_srt.py` — SRT-only regeneration (no audio re-synthesis)

Uses the `edge-tts >= 7.0` SubMaker streaming API to rebuild SRT files without re-generating audio. Use when caption grouping (`WORD_BREAK_SUBTITLE`) or timing needs adjustment but audio is already correct.

**Requires edge-tts 7.x:**
```bash
pip install "edge-tts>=7.0"
```

**Run directly (no editing needed):**
```bash
# Auto-detects scene count
python .agents/skills/edge-tts/scripts/regenerate_srt.py output/20260411_funfact-planet-mars

# Explicit scene count + voice override
python .agents/skills/edge-tts/scripts/regenerate_srt.py output/20260411_funfact-planet-mars 6 --voice en-US-AriaNeural
```

Uses the same `.env` variables as `generate_tts.py`.

**Outputs:** Overwrites `subtitle_N.srt`, `subtitles_N.txt`, and the merged `subtitles.srt` / `subtitles.txt`.
