---
name: searxng
description: "Web search via self-hosted SearXNG instance (https://github.com/searxng/searxng). Use when: mencari informasi terbaru dari web, web research untuk konten video, fact-checking, mencari data/statistik terbaru, mencari referensi artikel/berita, mencari sumber untuk outline YouTube, mencari argumen pro/kontra suatu topik, mencari studi kasus nyata dari internet, riset online untuk skrip video."
argument-hint: "Query pencarian, jumlah hasil, kategori pencarian (general/news/science), URL instance SearXNG (default: localhost:8888)"
---

# SearXNG Search skill

Web search menggunakan self-hosted [SearXNG](https://github.com/searxng/searxng) — metasearch engine privat yang menggabungkan hasil dari Google, Bing, DuckDuckGo, Wikipedia, dan banyak engine lain.

## Kapan Menggunakan

- Riset web untuk konten YouTube, artikel, atau skrip
- Mencari data, statistik, atau informasi terkini dari internet
- Fact-checking dan verifikasi informasi
- Mencari studi kasus, berita, atau referensi untuk konten
- Menggali perspektif pro/kontra dari berbagai sumber
- Riset topik untuk outline video YouTube

## Prinsip

1. **Python script** — gunakan `scripts/search_searxng.py` untuk query dari command line
2. **URL instance bisa dikustom** — via argumen `--url` atau env var `SEARXNG_URL`
3. **API key opsional** — via argumen `--api-key` atau env var `SEARXNG_API_KEY`
4. **JSON output** — script return JSON yang bisa diparsing untuk konten
5. **Cross-platform** — pathlib, tidak ada dependency berat

---

## Instalasi

```bash
pip install requests
```

## Environment Config

```dotenv
# .env (opsional)
SEARXNG_URL=http://localhost:8888
SEARXNG_API_KEY=your_api_key_here   # jika SearXNG pakai auth
```

---

## CLI Usage

```bash
# Search default (localhost:8888)
python .agents/skills/searxng/scripts/search_searxng.py --query "inflasi indonesia 2026"

# Custom URL & limit hasil
python .agents/skills/searxng/scripts/search_searxng.py \
  --url "http://searxng.example.com" \
  --query "krisis energi eropa" \
  --limit 10

# Dengan API key
python .agents/skills/searxng/scripts/search_searxng.py \
  --query "AI regulation" \
  --api-key "sk-xxx" \
  --category "news"

# Kategori spesifik
python .agents/skills/searxng/scripts/search_searxng.py \
  --query "black hole discovery" \
  --category "science"
```

---

## Python API (import)

```python
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / ".agents/skills/searxng/scripts"))
from search_searxng import search_searxng

results = search_searxng(
    query="kenaikan harga beras 2026",
    searxng_url="http://localhost:8888",
    limit=5,
    category="general",
)
for r in results:
    print(f"{r['title']} — {r['url']}")
    print(r['content'][:200])
    print()
```

---

## Parameter

| Parameter | Default | Deskripsi |
|-----------|---------|-----------|
| `--url` | `http://localhost:8888` | URL instance SearXNG |
| `--query` | (required) | Query pencarian |
| `--limit` | `5` | Jumlah hasil maksimal |
| `--category` | `general` | Kategori: `general`, `news`, `science`, `images`, `videos`, `files`, `social media` |
| `--api-key` | — | API key (jika SearXNG pakai auth) |
| `--language` | — | Filter bahasa, misal `id`, `en`, `all` |

## Output Format

Script return list of dicts:

```python
[
    {
        "title": "Judul Hasil",
        "url": "https://...",
        "content": "Snippet/konten...",
        "engine": "google",
        "category": "general",
        "publishedDate": "2026-06-20",
    },
]
```

## Integrasi Riset untuk Outline YouTube

Saat membuat outline YouTube, gunakan SearXNG untuk riset data aktual sebelum menyusun segmen:

1. **Search data/statistik** — untuk memperkuat argumen dengan angka nyata
2. **Search berita terbaru** — untuk konteks "apa yang terjadi sekarang"
3. **Search studi kasus** — untuk contoh konkret di segmen studi kasus
4. **Search perspektif pro/kontra** — untuk segmen analisis mendalam
5. **Search konteks Indonesia** — untuk segmen Spotlight Indonesia

Format perintah di agent prompt:
```
Search web untuk data terkini: python .agents/skills/searxng/scripts/search_searxng.py --query "[query]" --limit 5 --category "[category]"
```
