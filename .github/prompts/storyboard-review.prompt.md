---
description: "Review storyboard scene prompts before image generation. Use when: review prompt_1.txt prompt_2.txt, preview image prompts before generating images, cek konsistensi storyboard, review continuity antar scene, audit prompt scene untuk video pendek"
name: "Storyboard Reviewer"
agent: "agent"
tools: [read, search]
argument-hint: "Path folder video output atau judul video yang ingin direview storyboard-nya"
---

Review the generated storyboard package before any image generation runs.

## Goal

Audit all scene prompt files in the target video folder and report whether the storyboard is ready for image generation.

## Target Resolution Rules

1. Accept either a direct path to a generated video folder or a video title.
2. Read `.env` to resolve `OUTPUT` if only the title is provided.
3. Inspect:
   - `subtitles.txt`
   - `subtitles.srt` if present
   - every `scene_{x}/subtitles_{x}.txt`
   - every `scene_{x}/prompt_{x}.txt`

## Review Criteria

Evaluate each scene prompt for:
- narrative alignment with its subtitle text
- visual clarity and shot specificity
- style consistency across all scenes
- character, object, and environment continuity
- pacing fit for an 8–12 second segment
- duplicate or near-duplicate imagery across adjacent scenes
- ambiguity that could make the image generator drift
- missing details needed for a strong single-frame illustration

## Output Format

Return exactly these sections:

### Ready Verdict

State one of:
- `READY`
- `READY WITH FIXES`
- `NOT READY`

### Storyboard Summary

Provide:
- video folder reviewed
- total scenes found
- how many prompts are strong as-is
- how many prompts need revision

### Scene Review Table

Use a compact table with columns:
- `Scene`
- `Status`
- `Subtitle Intent`
- `Prompt Risk`
- `Recommended Fix`

### Cross-Scene Issues

List continuity or style problems that affect multiple scenes.

### Suggested Rewrites

For every scene that needs work, provide a rewritten prompt block labeled by scene number.

## Constraints

- Do not edit files automatically
- Do not generate images
- Do not rewrite strong prompts just for style preference
- Prefer minimal, targeted fixes that preserve the original story structure