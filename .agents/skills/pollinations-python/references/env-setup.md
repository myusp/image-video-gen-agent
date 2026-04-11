# Cross-Platform Python Environment Setup

## Project Structure Convention

```
project-root/
├── .env                  # secrets & config — never commit
├── .env.example          # committed template (no real values)
├── requirements.txt      # all pip dependencies
├── output/               # generated files (.gitignore this)
└── scripts/              # Python entrypoints
```

### `.env.example` template

```dotenv
POLLINATIONS_API_KEY=sk_your_key_here

# Image generation defaults
DEFAULT_IMAGE_MODEL=flux
DEFAULT_IMAGE_WIDTH=1024
DEFAULT_IMAGE_HEIGHT=1024

# Audio / TTS
AUDIO_PROVIDER=edge-tts
EDGE_TTS_NAME=id-ID-ArdiNeural
POLLINATION_TTS_NAME=

# Video
TARGET_VIDEO_DURATION=180
```

---

## Virtual Environment (cross-platform)

```bash
# Create venv (same command on all OS)
python -m venv .venv

# Activate — macOS/Linux
source .venv/bin/activate

# Activate — Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Activate — Windows (CMD)
.venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

---

## Loading `.env` Correctly

### Basic load (one-liner)

```python
from dotenv import load_dotenv
load_dotenv()  # searches CWD then parent dirs
```

### Explicit path (useful for scripts run from subfolders)

```python
from dotenv import load_dotenv
from pathlib import Path

# Always resolve relative to THIS script's location
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
```

### Strict validation helper

```python
import os

REQUIRED_VARS = ["POLLINATIONS_API_KEY"]

def validate_env(required: list[str] = REQUIRED_VARS) -> None:
    missing = [v for v in required if not os.getenv(v)]
    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}\n"
            "Copy .env.example to .env and fill in the values."
        )
```

---

## Path Handling (avoid Windows/macOS differences)

```python
from pathlib import Path

# GOOD — works everywhere
output_dir = Path("output") / "images"
output_dir.mkdir(parents=True, exist_ok=True)

# BAD — breaks on Windows
output_dir = "output/images"
os.makedirs(output_dir, exist_ok=True)  # technically ok but avoid mixing

# Reading files
data = Path("data/prompt.txt").read_text(encoding="utf-8")

# Writing binary files (images, audio, video)
Path("output/image.jpg").write_bytes(response.content)

# Writing text files
Path("output/result.txt").write_text(result, encoding="utf-8")
```

---

## `requirements.txt` Baseline

```
openai>=1.0.0
python-dotenv>=1.0.0
requests>=2.31.0
pillow>=10.0.0
```

Add as needed:
```
edge-tts>=6.1.0          # if AUDIO_PROVIDER=edge-tts
httpx>=0.25.0            # async HTTP client
aiofiles>=23.0.0         # async file I/O
tqdm>=4.65.0             # progress bars
```

---

## Environment Variable Patterns

| Pattern | Use Case |
|---------|---------|
| `os.environ["KEY"]` | Required — raises `KeyError` immediately if missing |
| `os.getenv("KEY")` | Optional — returns `None` if missing |
| `os.getenv("KEY", "default")` | Optional with fallback value |

```python
# Required
api_key = os.environ["POLLINATIONS_API_KEY"]

# Optional with default
model = os.getenv("DEFAULT_IMAGE_MODEL", "flux")
width = int(os.getenv("DEFAULT_IMAGE_WIDTH", "1024"))
```

---

## `.gitignore` Essentials

```gitignore
.env
.venv/
__pycache__/
*.pyc
output/
*.mp3
*.mp4
*.jpg
*.png
```
