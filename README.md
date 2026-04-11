# image-video-gen-agent

> AI-powered short-form video production pipeline — generates YouTube Shorts & Instagram Reels from a title or script using autonomous agents, React/Remotion, and open AI APIs.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-green)](https://nodejs.org)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Remotion](https://img.shields.io/badge/Remotion-4.0-orange)](https://www.remotion.dev)

---

## What it does

Given a topic or full script, the pipeline automatically:

1. **Writes the script** — using personality-driven short-form writing styles (punchy, outscal, etc.)
2. **Generates scene images** — AI image generation via [Pollinations API](https://pollinations.ai) (Flux, nanobanana, DALL-E, etc.)
3. **Produces narration audio** — per-scene TTS with word-level SRT timing via [edge-tts](https://github.com/rany2/edge-tts)
4. **Downloads BGM / SFX** — royalty-free audio from Pixabay
5. **Compiles to MP4** — smooth Ken Burns motion + scene transitions + burned TikTok-style captions via [Remotion](https://www.remotion.dev)

**Output**: vertical MP4 (1080×1920, 30fps, H.264) ready for TikTok, YouTube Shorts, and Instagram Reels.

---

## Demo

| Scene 1 | Scene 4 | Scene 6 |
|---------|---------|---------|
| ![scene1](output/20260411_funfact-planet-mars/scene_1/prompt_1.txt) | … | … |

> Example output in [`output/20260411_funfact-planet-mars/`](output/20260411_funfact-planet-mars/)

---

## Architecture

```
.github/agents/          ← Agent orchestrators
  image-video-gen.agent.md      ← 7-phase: script → images → audio → metadata
  remotion-compilation.agent.md ← compile output folder → final MP4

.agents/skills/          ← Domain skill packages (reusable across agents)
  pollinations-python/   ← Image generation (Pollinations API + Python)
  edge-tts/              ← TTS narration + word-level SRT
  pixabay-audio/         ← BGM / SFX search & download
  ffmpeg/                ← Video/audio conversion helpers
  remotion-best-practices/  ← Remotion animation & timing rules
  shorts-script-personality/  ← Viral short-form script styles
  content-creation/      ← Marketing copy & angle research
  social-content/        ← Social media optimization
  youtube-scriptwriting/ ← Hook → body → payoff structure
  ai-image-prompts-skill/  ← Curated 10k+ image prompt library

src/                     ← Shared Remotion template (never modified per-video)
  Root.tsx               ← Loads scene-config.json dynamically
  Main.tsx               ← TransitionSeries + per-scene audio
  SceneImage.tsx         ← Animated image (zoom / pan / Ken Burns)
  CaptionOverlay.tsx     ← TikTok-style word-highlighted captions

output/{date}_{slug}/    ← Per-video assets (git-ignored)
  scene_N/               ← image, audio, prompt, SRT per scene
  scene-config.json      ← Motion + timing config (read at render time)
  subtitles.srt          ← Full-video merged captions
  metadata.json          ← Title, hashtags, thumbnail_prompt
```

**Shared template model**: `src/` is one shared Remotion project. Every video only needs its own `scene-config.json` + asset files in the output folder. `REMOTION_PUBLIC_DIR` switches which video is loaded at render time.

---

## Quick Start

### Prerequisites

- **Node.js 18+** and **npm**
- **Python 3.10+**
- **ffmpeg** in PATH (for audio concatenation)
- API keys: [Pollinations](https://pollinations.ai), [Pixabay](https://pixabay.com/api/docs/) (optional)

### 1. Clone & Install

```bash
git clone https://github.com/myusp/image-video-gen-agent.git
cd image-video-gen-agent

# Node deps (Remotion)
npm install

# Python deps
pip install edge-tts requests python-dotenv pillow openai
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```dotenv
POLLINATIONS_API_KEY="your-key-here"   # from https://pollinations.ai
PIXABAY_API_KEY="your-key-here"        # optional, for BGM/SFX
EDGE_TTS_NAME="id-ID-ArdiNeural"       # TTS voice (see edge-tts --list-voices)
OUTPUT="./output"
WORD_BREAK_SUBTITLE=4
```

### 3. Generate a video

The pipeline runs via **GitHub Copilot Agent Mode** (VS Code). Open the project in VS Code, then in a chat window:

```
@Image Video Generator Fun fact tentang Planet Mars
```

The agent will:
- Auto-generate a script (or accept your script)
- Generate scene images, TTS audio, BGM
- Save everything to `output/20260411_funfact-planet-mars/`

### 4. Compile to MP4

```
@Remotion Compilation Agent output/20260411_funfact-planet-mars
```

Or run directly from the terminal:

```bash
REMOTION_PUBLIC_DIR=./output/20260411_funfact-planet-mars \
  npm run render:captions \
  --output ./output/20260411_funfact-planet-mars/final_video.mp4
```

### 5. Preview in Remotion Studio

```bash
REMOTION_PUBLIC_DIR=./output/20260411_funfact-planet-mars npm run dev
```

---

## Motion Effects

| Effect | Description | Auto-selected when prompt contains |
|--------|-------------|-----------------------------------|
| `zoom_in` | Scale 1.0 → 1.5 | close-up, detail, macro, face |
| `zoom_out` | Scale 1.5 → 1.0 | wide shot, landscape, crowd |
| `pan_left_right` | ±10% X @ 1.5× scale | action, movement, chase, speed |
| `pan_right_left` | reverse X pan | same |
| `pan_up_down` | ±10% Y @ 1.5× scale | falling, rain, descending |
| `pan_down_up` | reverse Y pan | rising, flying, sky, hope |
| `ken_burns` | Scale 1.0 → 1.4 + drift | cinematic, dramatic, portrait, reveal |

---

## Caption Styles

Three Remotion compositions are registered:

| Composition ID | Caption Style | Use |
|----------------|--------------|-----|
| `main` | TikTok-style word highlight (yellow `#FFE600`) | Default for Shorts |
| `main-plain-captions` | Plain white text, no highlight | Clean look |
| `main-no-captions` | No captions | B-roll, manual sub overlay |

Captions include a **−150ms timing offset** to compensate for edge-tts word-boundary delay.

---

## Output Structure

```
output/
└── 20260411_funfact-planet-mars/
    ├── scene_1/
    │   ├── image_1.jpeg        ← AI-generated scene image
    │   ├── audio_1.mp3         ← TTS narration
    │   ├── prompt_1.txt        ← Image prompt (used for motion selection)
    │   ├── subtitles_1.txt     ← Scene text
    │   └── subtitle_1.srt      ← Word-level SRT
    ├── scene_2/ … scene_N/
    ├── audio/
    │   ├── bgm_cinematic.mp3   ← Background music (Pixabay)
    │   └── audio_manifest.json
    ├── scene-config.json       ← Motion + timing per scene
    ├── subtitles.srt           ← Full-video captions
    ├── subtitles.txt           ← Full narration text
    ├── audio_full.mp3          ← Concatenated narration
    └── metadata.json           ← Title, description, hashtags, thumbnail_prompt
```

---

## Skills

Skills are modular knowledge packages used by agents. Each skill under `.agents/skills/` contains:
- `SKILL.md` — Instructions and workflow
- `references/` — Domain reference docs
- `scripts/` — Ready-to-run Python scripts

See each skill's `SKILL.md` for usage details.

---

## Critical Constraints

| Constraint | Reason |
|------------|--------|
| No em dash `—` / en dash `–` in subtitles | Causes rendering artifacts in burned captions |
| Images must be `.jpeg` | Pollinations API returns JPEG binary; other formats break rendering |
| No symlinks in output folder | Remotion HTTP bundler can't resolve symlinks → 404 |
| Never edit `src/` per-video | Shared template; config goes only in `scene-config.json` |
| `REMOTION_PUBLIC_DIR` must be set | Without it, Remotion can't find `scene-config.json` |
| Pan translate `< (scale-1)/(2×scale)` | Exceeding this shows black edges at frame borders |

---

## Contributing

Contributions welcome! Please open an issue before submitting large PRs.

1. Fork the repo
2. Create a feature branch (`git checkout -b feat/my-feature`)
3. Commit your changes
4. Open a PR against `main`

---

## License

[MIT](LICENSE) © 2026 Mohamad Yusup
