# Pollinations Image Generation Reference

Base URL: `https://gen.pollinations.ai`

---

## Endpoints

### POST /v1/images/generations (OpenAI-compatible)

```python
from openai import OpenAI
import os

client = OpenAI(
    base_url="https://gen.pollinations.ai/v1",
    api_key=os.environ["POLLINATIONS_API_KEY"],
)

response = client.images.generate(
    model="flux",          # see model table below
    prompt="prompt text",
    size="1024x1024",      # WIDTHxHEIGHT
    # extra_body supports seed, enhance, safe, nologo, negative_prompt
    extra_body={"seed": 42, "enhance": False},
)
# response.data[0].url  — when response_format="url" (default server behavior)
# response.data[0].b64_json — when response_format="b64_json"
print(response.data[0].url)
```

### GET /image/{prompt} (simple URL)

```
https://gen.pollinations.ai/image/a%20cat%20in%20space?model=flux&seed=42&width=1024&height=1024
```

Download directly:
```python
import requests
from urllib.parse import quote
from pathlib import Path
import os

def generate_image_url(prompt: str, model: str = "flux", width: int = 1024, height: int = 1024, seed: int = 0) -> Path:
    encoded = quote(prompt)
    url = f"https://gen.pollinations.ai/image/{encoded}?model={model}&width={width}&height={height}&seed={seed}"
    resp = requests.get(url, headers={"Authorization": f"Bearer {os.environ['POLLINATIONS_API_KEY']}"}, timeout=120)
    resp.raise_for_status()
    dest = Path("output") / f"{model}_{seed}.jpeg"  # API returns JPEG binary
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(resp.content)
    return dest
```

### POST /v1/images/edits (image-to-image)

```python
response = client.images.edit(
    model="kontext",
    prompt="make the sky purple",
    image=open("input.jpg", "rb"),   # or pass URL via extra_body={"image": "https://..."}
)
print(response.data[0].url)
```

---

## Image Models

| Model | Notes |
|-------|-------|
| `flux` | Flux Schnell — fast, high quality |
| `zimage` | Z-Image Turbo — fast with 2x upscaling |
| `kontext` | FLUX.1 Kontext — in-context editing (requires image input) |
| `klein` | FLUX.2 Klein 4B — fast, supports image input |
| `gptimage` | GPT Image 1 Mini (paid) |
| `gptimage-large` | GPT Image 1.5 (paid) |
| `wan-image` | Wan 2.7 — up to 2K, supports image editing (paid) |
| `nanobanana` | Gemini 2.5 Flash Image (paid, image input) |
| `seedream5` | Seedream 5.0 Lite (paid) |
| `nova-canvas` | Amazon Nova Canvas (paid) |

### List models at runtime

```python
import requests
models = requests.get("https://gen.pollinations.ai/image/models").json()
for m in models:
    print(m["id"], "-", m.get("description", ""))
```

---

## Common Parameters

| Param | Type | Default | Notes |
|-------|------|---------|-------|
| `model` | string | `zimage` | See model table |
| `width` | int | 1024 | Pixel width |
| `height` | int | 1024 | Pixel height |
| `seed` | int | 0 | Use `-1` for random; `0` = fixed |
| `enhance` | bool | false | AI prompt enhancement |
| `negative_prompt` | string | — | flux, zimage only |
| `safe` | bool | false | Safety filter |
| `quality` | string | medium | `low/medium/high/hd` — gptimage only |
| `transparent` | bool | false | gptimage only |
| `image` | string | — | Reference image URL(s) separated by `\|` or `,` |

---

## Batch Image Generation

```python
from pathlib import Path
import os, requests
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor

def generate_one(args):
    prompt, seed, model, out_dir = args
    url = f"https://gen.pollinations.ai/image/{quote(prompt)}?model={model}&seed={seed}"
    resp = requests.get(url, headers={"Authorization": f"Bearer {os.environ['POLLINATIONS_API_KEY']}"}, timeout=120)
    resp.raise_for_status()
    dest = Path(out_dir) / f"seed_{seed}.jpeg"  # API returns JPEG binary
    dest.write_bytes(resp.content)
    return str(dest)

def batch_generate(prompt: str, seeds: list[int], model: str = "flux", out_dir: str = "output"):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    tasks = [(prompt, s, model, out_dir) for s in seeds]
    with ThreadPoolExecutor(max_workers=4) as ex:
        return list(ex.map(generate_one, tasks))
```

---

## Save as Base64 (for embedding in JSON/HTML)

```python
import base64, requests

def image_to_base64(url: str, api_key: str) -> str:
    resp = requests.get(url, headers={"Authorization": f"Bearer {api_key}"}, timeout=60)
    resp.raise_for_status()
    return base64.b64encode(resp.content).decode()
```
