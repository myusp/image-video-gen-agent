"""
check_env.py — Validate Pollinations API setup.
Run: python .agents/skills/pollinations-python/scripts/check_env.py
"""
import os
import sys
from pathlib import Path

# ── Load .env from project root (2 levels up from this script) ──────────────
try:
    from dotenv import load_dotenv
except ImportError:
    print("[FAIL] python-dotenv is not installed.")
    print("       Run: pip install python-dotenv")
    sys.exit(1)

env_path = Path(__file__).resolve().parents[3] / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print(f"[OK]   Loaded .env from {env_path}")
else:
    load_dotenv()
    print(f"[WARN] .env not found at {env_path}, tried CWD fallback")

# ── Check required variables ─────────────────────────────────────────────────
REQUIRED = ["POLLINATIONS_API_KEY"]
OPTIONAL = {
    "DEFAULT_IMAGE_MODEL": "flux",
    "DEFAULT_IMAGE_WIDTH": "1024",
    "DEFAULT_IMAGE_HEIGHT": "1024",
    "AUDIO_PROVIDER": "edge-tts",
    "EDGE_TTS_NAME": "id-ID-ArdiNeural",
    "TARGET_VIDEO_DURATION": "180",
}

all_ok = True
for var in REQUIRED:
    val = os.getenv(var)
    if val:
        # Mask key: show first 8 chars only
        masked = val[:8] + "..." if len(val) > 8 else val
        print(f"[OK]   {var} = {masked}")
    else:
        print(f"[FAIL] {var} is not set")
        all_ok = False

for var, default in OPTIONAL.items():
    val = os.getenv(var, default)
    print(f"[INFO] {var} = {val}")

# ── Test API connectivity ────────────────────────────────────────────────────
if all_ok:
    try:
        import requests
    except ImportError:
        print("[FAIL] requests is not installed. Run: pip install requests")
        sys.exit(1)

    api_key = os.environ["POLLINATIONS_API_KEY"]
    print("\n── Testing API key validity ───────────────────────────────────────")
    try:
        resp = requests.get(
            "https://gen.pollinations.ai/api/account/key",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10,
        )
        if resp.status_code == 200:
            data = resp.json()
            print(f"[OK]   Key valid — type: {data.get('type')}, name: {data.get('name')}")
            if data.get("pollenBudget") is not None:
                print(f"[INFO] Pollen budget: {data['pollenBudget']}")
        elif resp.status_code == 401:
            print("[FAIL] API key rejected (401 Unauthorized)")
            all_ok = False
        else:
            print(f"[WARN] Unexpected status {resp.status_code}: {resp.text[:120]}")
    except requests.exceptions.ConnectionError:
        print("[WARN] Could not reach gen.pollinations.ai — check internet connection")
    except requests.exceptions.Timeout:
        print("[WARN] Request timed out")

# ── Summary ──────────────────────────────────────────────────────────────────
print()
if all_ok:
    print("Setup looks good. You can start using Pollinations API.")
else:
    print("One or more checks failed. Fix the issues above before running scripts.")
    sys.exit(1)
