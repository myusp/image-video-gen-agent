# Project Guidelines

## Overview

AI-powered short-form video production pipeline: `script → scene images → TTS audio → Remotion MP4`. Generates YouTube Shorts / Instagram Reels (1080×1920, 30fps) using autonomous agents and a shared Remotion template.

## Architecture

```
.github/agents/          ← Agent orchestrators (image-video-gen, remotion-compilation)
.agents/skills/          ← Skill packages with reference docs + bundled scripts
src/                     ← Shared Remotion template (Root, Main, SceneImage, CaptionOverlay)
output/{date}_{slug}/    ← Per-video assets + scene-config.json (loaded at render time)
```

**Shared template model**: `src/` is never modified per-video. All video-specific config goes in `output/{folder}/scene-config.json`. Remotion reads it dynamically via `calculateMetadata` + `REMOTION_PUBLIC_DIR` env var.

**Two agents, one pipeline**:
1. **Image Video Generator** — 7-phase orchestrator: script → segment → prompts → images → TTS → BGM → metadata
2. **Remotion Compilation** — Takes output folder → renders final MP4 with motion effects + transitions + burned captions

## Build & Run

```bash
npm install                       # Install Remotion + React deps
npm run dev                       # Remotion Studio (preview)
npm run lint                      # ESLint + TypeScript check

# Render specific video:
REMOTION_PUBLIC_DIR=./output/{video_folder} npm run render:captions \
  --output ./output/{video_folder}/remotion_compiled.mp4
```

Python scripts live in `.agents/skills/*/scripts/`. Install deps: `pip install edge-tts requests python-dotenv pillow openai`

## Critical Constraints

- **No long dashes in subtitles** — em dash `—` and en dash `–` cause caption rendering artifacts. Replace with commas, periods, or ASCII hyphen `-`
- **JPEG only** — Scene images must be `.jpeg` (Pollinations API output). Other formats break rendering
- **No symlinks in output** — Remotion serves via HTTP; symlinks → 404. Always copy real files
- **Never modify `src/` per-video** — Shared template; per-video config goes only in `scene-config.json`
- **Pan safety** — For pan effects, max translate must be `< (scale-1)/(2*scale) * 100%`. Current: scale 1.5, translate ±10% (safe limit ±16.67%)
- **Caption offset** — `-150ms` compensates for edge-tts word-boundary timing delay; changing TTS providers requires re-tuning
- **`prompt_N.txt` is required** — The compilation agent reads it to auto-select motion effects per scene

## Conventions

- **Output folders**: `{yyyymmdd}_{title-slug}/` (e.g., `20260411_funfact-planet-mars/`)
- **Scene files**: `scene_N/image_N.jpeg`, `scene_N/audio_N.mp3`, `scene_N/prompt_N.txt`, `scene_N/subtitle_N.srt`, `scene_N/subtitles_N.txt`
- **Compositions**: `main` (TikTok captions), `main-plain-captions` (white text), `main-no-captions` (clean)
- **Motion effects**: `zoom_in`, `zoom_out`, `pan_left_right`, `pan_right_left`, `pan_up_down`, `pan_down_up`, `ken_burns` — auto-selected from prompt keywords
- **Resumability**: All agent phases check for existing files before regenerating. Partial runs can be continued

## Environment Variables

See [.env.example](.env.example) for the full list. Required:
- `POLLINATIONS_API_KEY` — Image generation
- `EDGE_TTS_NAME` — TTS voice (e.g., `id-ID-ArdiNeural`)
- `OUTPUT` — Base output dir (default `./output`)

Optional: `PIXABAY_API_KEY` (BGM/SFX), `WORD_BREAK_SUBTITLE` (words per caption block, default `4`)

## Common Pitfalls

- `REMOTION_PUBLIC_DIR` must be set per render — without it, Remotion can't find `scene-config.json`
- Scene duration in `scene-config.json` must match actual MP3 duration — mismatch causes audio desync
- `TransitionSeries` children must be `TransitionSeries.Sequence` or `TransitionSeries.Transition` — **never** React Fragments
- `tsconfig.json` uses `"lib": ["es2015"]` (no `"dom"`) — this is intentional for Remotion's bundler; `fetch`/`console` warnings in IDE are expected
