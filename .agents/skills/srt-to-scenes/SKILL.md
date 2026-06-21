---
name: srt-to-scenes
description: "Segment an existing SRT transcript + audio into per-scene folders ready for image generation and Remotion rendering. Use when: video dari rekaman audio, transcript SRT sudah ada, audio sudah ada, split audio per scene, convert SRT to scenes, scene setup dari transkrip, setup project folder dari SRT, build scene-config.json, generate remotion config, generate audio_durations.json."
argument-hint: "Path ke project folder, path ke file SRT, path ke audio (opsional), orientation landscape/portrait"
---

# SRT-to-Scenes Skill

Convert an existing SRT transcript and audio file into a structured scene-based project folder ready for image generation and Remotion video compilation. Replaces the need to write per-project Python scripts.

## When to Use
- User provides an existing SRT transcript (e.g. from a recording, podcast, or auto-transcription)
- User has a full audio file and wants to split it into per-scene clips
- Setting up a project folder without TTS generation (audio already exists)
- Building `scene-config.json` for Remotion after images are generated
- Any workflow where narration is pre-recorded rather than synthesized

---

## Scripts Overview

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| `setup_scenes.py` | Parse SRT → scene folders | SRT file, optional audio | `scene_N/`, `scene_times.json` |
| `split_audio.py` | Split full audio per scene | `scene_times.json`, `audio_full.mp3` | `scene_N/audio_N.mp3`, `audio_durations.json` |
| `build_config.py` | Build Remotion config | scene assets + `audio_durations.json` | `scene-config.json`, `remotion_motions.txt` |

---

## Step-by-Step Usage

### Step 1 — Setup scene folders from SRT

Two modes are supported. **Agent-driven mode is preferred** for highest content quality.

#### Mode A — Agent-Driven (recommended)

The agent reads the full SRT transcript, analyzes narrative context and visual representability, then
decides scene boundaries. Scene count is unrestricted — each scene = one coherent visual concept.

```bash
python .agents/skills/srt-to-scenes/scripts/setup_scenes.py \
  output/{yyyymmdd}_{title_slug} \
  --srt "path/to/transcript.srt" \
  --audio "path/to/audio.mp3" \
  --scene-breaks '[[0.0, 22.5], [22.5, 45.1], [45.1, 71.0]]'
```

`--scene-breaks` is a JSON array of `[start_sec, end_sec]` pairs — one per scene. The agent
reads the SRT timestamps and outputs this array after analyzing the narrative.

#### Mode B — Duration-Based (legacy fallback)

Groups SRT entries at sentence boundaries, targeting a fixed seconds-per-scene. Use when
agent-driven analysis is not available.

```bash
python .agents/skills/srt-to-scenes/scripts/setup_scenes.py \
  output/{yyyymmdd}_{title_slug} \
  --srt "path/to/transcript.srt" \
  --audio "path/to/audio.mp3" \
  [--target-duration 13] \
  [--max-duration 15]
```

**What it does (both modes):**
- Parses SRT into entries → groups by agent-specified breaks or duration rules
- Creates `scene_N/` folders (resumable: skips existing)
- Writes `scene_N/subtitles_N.txt` (concatenated narration text)
- Writes `scene_N/subtitle_N.srt` (per-scene SRT, time-offset to 0)
- Copies audio → `audio_full.mp3` (if `--audio` provided)
- Writes `scene_times.json` → `[[start, end], ...]` for `split_audio.py`
- Sanitizes em/en dashes in subtitle text (prevents caption rendering artifacts)

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `--srt` | *(required)* | Path to the SRT transcript file |
| `--audio` | none | Path to the full audio file. Copied as `audio_full.mp3`. |
| `--scene-breaks` | none | Agent-specified scene boundaries as JSON `[[start, end], ...]`. Overrides duration-based grouping. |
| `--target-duration` | `13` | (Legacy) Target seconds per scene when not using `--scene-breaks` |
| `--max-duration` | `15` | (Legacy) Hard max seconds per scene when not using `--scene-breaks` |

---

### Step 2 — Split audio per scene

```bash
python .agents/skills/srt-to-scenes/scripts/split_audio.py \
  output/{yyyymmdd}_{title_slug}
```

**What it does:**
- Reads `scene_times.json` from the project folder
- Splits `audio_full.mp3` into `scene_N/audio_N.mp3` via FFmpeg (resumable)
- Measures actual MP3 durations via ffprobe
- Writes `audio_durations.json` → `{"1": 13.91, "2": 12.83, ...}`

**Prerequisites:** `ffmpeg` and `ffprobe` must be installed and on PATH.

---

### Step 3 — Generate image prompts (per scene)

After scene folders exist, generate `scene_N/prompt_N.txt` for each scene. The agent uses the `ai-image-prompts-skill` to write visually specific prompts based on the scene narration text (`subtitles_N.txt`).

---

### Step 4 — Generate images

```bash
python .agents/skills/pollinations-python/scripts/generate_images.py \
  output/{yyyymmdd}_{title_slug} \
  --model flux \
  --orientation landscape
```

---

### Step 5 — Build Remotion scene config

```bash
python .agents/skills/srt-to-scenes/scripts/build_config.py \
  output/{yyyymmdd}_{title_slug} \
  --orientation landscape
```

**What it does:**
- Reads `audio_durations.json` for scene durations
- Reads `prompt_N.txt` to auto-select motion effect per scene
- Skips scenes missing `image_N.jpeg` or `audio_N.mp3` (with a warning)
- Writes `scene-config.json` (Remotion template reads this via `REMOTION_PUBLIC_DIR`)
- Writes `remotion_motions.txt` (human-readable motion log)

**Options:**

| Flag | Default | Description |
|------|---------|-------------|
| `--orientation` | `landscape` | `landscape` (1920×1080) or `portrait` (1080×1920) |

---

## Motion Effect Auto-Selection

`build_config.py` selects the Remotion motion effect from keywords in `prompt_N.txt`:

| Keywords in prompt | Motion effect |
|-------------------|---------------|
| action, movement, running, chase, dynamic, flow | `pan_left_right` |
| close-up, detail, macro, face, eyes, portrait | `zoom_in` |
| wide, establishing, landscape, panoramic, aerial | `zoom_out` |
| reveal, introduction, hero, character, emerge | `ken_burns` |
| falling, descending, underwater, rain, pouring | `pan_up_down` |
| rising, flying, sky, ascending, hope, rocket, growth | `pan_down_up` |
| dramatic, emotional, cinematic, reflection | `ken_burns` |
| *(no match)* | `zoom_in` (default) |

---

## Output Files

After running all three scripts and image generation:

```
output/{yyyymmdd}_{title_slug}/
├── scene_1/
│   ├── subtitles_1.txt    ← scene narration text
│   ├── subtitle_1.srt     ← per-scene SRT (offset to 0)
│   ├── prompt_1.txt       ← image generation prompt (write manually or via agent)
│   ├── image_1.jpeg       ← generated image (JPEG)
│   └── audio_1.mp3        ← audio clip from full recording
├── scene_2/ ...
├── audio_full.mp3         ← copy of original full audio
├── scene_times.json       ← [[start, end], ...] per scene
├── audio_durations.json   ← {"1": 13.91, "2": 12.83, ...}
├── scene-config.json      ← Remotion scene configuration
└── remotion_motions.txt   ← human-readable motion log
```

---

## Full End-to-End Command Sequence

```bash
# 1. Agent reads the SRT, analyzes narrative, decides scene breaks, then:
python .agents/skills/srt-to-scenes/scripts/setup_scenes.py \
  output/20260417_my-video \
  --srt "recording.srt" \
  --audio "recording.mp3" \
  --scene-breaks '[[0.0, 22.5], [22.5, 48.3], [48.3, 71.0]]'

# 2. Split audio per scene
python .agents/skills/srt-to-scenes/scripts/split_audio.py \
  output/20260417_my-video

# 3. Generate image prompts (agent writes prompt_N.txt per scene using ai-image-prompts-skill)
# ... (handled by Image Video Generator agent)

# 4. Generate images
python .agents/skills/pollinations-python/scripts/generate_images.py \
  output/20260417_my-video --model flux --orientation landscape

# 5. Build Remotion config
python .agents/skills/srt-to-scenes/scripts/build_config.py \
  output/20260417_my-video --orientation landscape

# 6. Render with Remotion
REMOTION_PUBLIC_DIR=./output/20260417_my-video \
  npm run render:captions \
  --output ./output/20260417_my-video/remotion_compiled.mp4
```

---

## Resumability

All three scripts are resumable — they skip existing output files:

| File exists | Script behaviour |
|-------------|-----------------|
| `audio_full.mp3` | `setup_scenes.py` skips copying audio |
| `scene_N/subtitles_N.txt` | `setup_scenes.py` skips writing that scene's text |
| `scene_N/audio_N.mp3` | `split_audio.py` skips splitting that scene |
| `audio_durations.json` | Can skip `split_audio.py` entirely if already written |
| `scene-config.json` | Re-run `build_config.py` any time to regenerate |

---

## Dependencies

```bash
pip install  # no Python deps beyond stdlib
# Requires: ffmpeg, ffprobe (system install)
brew install ffmpeg   # macOS
apt install ffmpeg    # Ubuntu/Debian
```
