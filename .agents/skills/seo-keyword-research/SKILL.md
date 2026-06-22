---
name: seo-keyword-research
description: "Riset keyword SEO gratis/OSS — autocomplete, tren, PAA, semantic clustering via SearXNG + PyTrends + spaCy. Use when: user minta keyword research, keyword ideas, riset keyword, topik konten, cari keyword, analisis keyword, SEO content planning, atau validasi ide topik. Tidak butuh API key berbayar. Mendukung Bahasa Indonesia dan Inggris."
argument-hint: "Slash command (/keyword <topik> atau /cluster <file.csv>), depth (0-3), bahasa (id/en), engine filter (ac/rs/tr/paa)"
---

# SEO Keyword Research Skill

**REQUIRED SUB-SKILL:** Use [searxng](../../searxng/SKILL.md) for SERP data (related searches, people-also-ask, organic results).

Riset keyword SEO gratis/OSS 8-fase pipeline — autocomplete, related searches, tren Google Trends, semantic clustering, intent classification. Semua sumber data free tanpa API key berbayar.

**8-Fase Pipeline (auto-run saat `/keyword`):**

```
[1/8] Scope      — deteksi bahasa, intent awal, parameter
[2/8] Discover   — seed keywords dari autocomplete Google + DDG
[3/8] Expand     — SERP SearXNG → related searches + PAA
[4/8] Trends     — PyTrends → volume relatif, rising queries, tren 12 bln
[5/8] Enrich     — Wikipedia API → entitas terkait, sinonim
[6/8] Classify   — intent tagging (info/nav/commercial/transactional)
[7/8] Cluster    — NLP grouping: pillar topic + cluster keywords
[8/8] Deliver    — output laporan prioritas + Opportunity Score
```

Setiap fase mengumumkan progres ke user. Fase 2-5 jalan paralel via subagents.

---

## Slash Commands

| Command | Deskripsi | Contoh |
|---------|-----------|--------|
| `/keyword <topik>` | Riset lengkap satu topik | `/keyword "investasi saham pemula"` |
| `/keyword <topik> --depth 2` | Kedalaman PAA (0-3) | `/keyword "cara diet" --depth 2` |
| `/keyword <topik> --lang id` | Paksa bahasa | `/keyword "resep masakan" --lang id` |
| `/keyword <topik> --engines ac,rs` | Filter engine (ac/rs/tr/paa) | `/keyword "laptop gaming" --engines ac,tr` |
| `/cluster keywords.csv` | Cluster dari file CSV | `/cluster my-keywords.csv` |
| `/cluster --topic <topik>` | Auto-generate seed lalu cluster | `/cluster --topic "digital marketing"` |

---

## Pipeline Detail

### Fase 1 — Scope

Deteksi bahasa (id/en), intent awal dari query, set parameter pencarian.

**Heuristik intent:**
- Informational: "apa", "cara", "bagaimana", "pengertian", "contoh", "what", "how", "why"
- Navigational: nama brand/website spesifik
- Commercial: "terbaik", "review", "rekomendasi", "vs", "perbandingan", "best", "vs"
- Transactional: "beli", "harga", "diskon", "order", "daftar", "buy", "price"

### Fase 2 — Discover (Autocomplete)

Jalankan script autocomplete untuk seed keywords dari Google Suggest + DuckDuckGo:

```bash
python .agents/skills/seo-keyword-research/scripts/autocomplete.py \
  --query "investasi saham pemula" \
  --lang id \
  --output .agents/skills/seo-keyword-research/scripts/ # cached di SQLite
```

### Fase 3 — Expand (SERP SearXNG)

Gunakan searxng skill untuk related searches dan PAA. Dispatche parallel:

```bash
python .agents/skills/searxng/scripts/search_searxng.py \
  --query "investasi saham pemula" \
  --limit 20
```

Parse hasil untuk `related_searches` dan people-also-ask dari JSON response.

**PAA Depth:** depth=0 (langsung), 1 (1 level follow-up), 2-3 (rekursif). Default 1.

### Fase 4 — Trends (PyTrends)

```bash
python .agents/skills/seo-keyword-research/scripts/trends.py \
  --keywords "investasi saham pemula,belajar saham,reksadana pemula" \
  --lang id
```

Output: interest over time (12 bln), rising queries, related queries.

### Fase 5 — Enrich (Wikipedia)

```bash
python .agents/skills/seo-keyword-research/scripts/wikipedia_enrich.py \
  --topic "investasi saham" \
  --lang id
```

Output: entitas terkait, topik induk, sinonim, kategori.

### Fase 6 — Classify (Intent Tagging)

Rule-based + NLP fallback. Lihat [references/intent-types.md](references/intent-types.md) untuk detail 4 intent dan sinyal.

### Fase 7 — Cluster (NLP)

Jalankan script clustering:

```bash
python .agents/skills/seo-keyword-research/scripts/nlp_cluster.py \
  --input keywords-raw.json \
  --lang id
```

Metode: TF-IDF + cosine distance + hierarchical clustering. Lihat [references/clustering-methods.md](references/clustering-methods.md).

### Fase 8 — Deliver (Output)

Generate 3 file + tampilkan ringkasan:

| File | Format | Isi |
|------|--------|-----|
| `KEYWORD-REPORT.md` | Markdown | Laporan lengkap + cluster map + rekomendasi |
| `keywords-raw.json` | JSON | Semua data mentah per keyword dengan skor |
| `keywords.csv` | CSV | Tabel flat untuk spreadsheet |

Lihat [references/output-formats.md](references/output-formats.md) untuk template detail.

---

## Opportunity Score

```
Opportunity Score = (Trend Score × Intent Value) / Est. Difficulty

Trend Score    : 1-100 dari PyTrends (normalisasi)
Intent Value   : Info=1, Nav=1, Commercial=2, Transactional=3
Est. Difficulty: 1-100 (estimasi dari jumlah SERP + authority)
```

**Transparansi:** Volume adalah estimasi relatif, bukan data Google Ads API. Label "Trend Score (relatif)" bukan "Search Volume".

---

## Resumability

Semua script cek cache sebelum fetch. Cache via SQLite di `~/.seo-keyword/cache/` (default TTL 24 jam). Riwayat semua run disimpan di `~/.seo-keyword/history.db`.

---

## Scripts

| Script | Fungsi | Dependency |
|--------|--------|------------|
| `scripts/autocomplete.py` | Google + DDG suggest | requests |
| `scripts/trends.py` | PyTrends wrapper | pytrends |
| `scripts/nlp_cluster.py` | spaCy + scikit-learn clustering | spacy, scikit-learn |
| `scripts/wikipedia_enrich.py` | Wikipedia REST API | requests |
| `scripts/cache.py` | DiskCache + SQLite | diskcache, sqlite3 |

---

## Dependencies

```bash
# Python
pip install requests pytrends spacy scikit-learn diskcache

# spaCy models
python -m spacy download id_core_news_sm   # Indonesian
python -m spacy download en_core_web_sm    # English
```

---

## Configuration (`config.yaml`)

Wajib diisi: `searxng.url` (URL instance SearXNG). Default di file `~/.seo-keyword/config.yaml`.

```yaml
searxng:
  url: "http://localhost:8888"
  timeout: 10
  max_results: 20

search:
  default_lang: "id"
  default_country: "ID"
  depth_limit: 1
  engines: ["ac", "rs", "tr", "paa"]

cache:
  enabled: true
  ttl_hours: 24
  path: "~/.seo-keyword/cache"

output:
  dir: "./seo-output"
  formats: ["md", "json", "csv"]
```

---

## Limitations (wajib transparan ke user)

| Keterbatasan | Cara Komunikasikan |
|---|---|
| Volume pencarian tidak akurat | Tampilkan "Trend Score (relatif)" bukan "Search Volume" |
| Difficulty adalah estimasi | Label jelas "Est. Difficulty — bukan data Ahrefs/Semrush" |
| PyTrends bisa rate-limit | Retry otomatis + pesan "Google Trends sedang throttle" |
| SearXNG perlu self-hosted | Pesan error jelas jika URL tidak valid di config |
| spaCy model Indonesia terbatas | Fallback ke NLTK jika model `id_core_news_sm` tidak tersedia |
