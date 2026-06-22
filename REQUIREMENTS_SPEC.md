# Requirement Specification
# SEO Keyword Research — Claude Code Skill
**Version:** 1.0.0  
**Status:** Draft  
**Tanggal:** 2026-06-22

---

## 1. Ringkasan Proyek

Sebuah **Claude Code Skill** berbasis agent untuk riset keyword SEO, dibangun sepenuhnya di atas tools free/open-source. Skill ini menggantikan dependensi pada API berbayar (SerpApi, DataForSEO) dengan SearXNG self-hosted sebagai backbone pencarian, diperkaya oleh PyTrends, Wikipedia API, dan NLP lokal.

Skill mengikuti pola arsitektur hybrid dari dua referensi:
- **`AgriciDaniel/claude-seo`** → 3-layer architecture, `agents/` folder, `references/` progressive disclosure
- **`secondsky/claude-skills`** → YAML frontmatter ketat, `plugin.json` per-skill, `model: inherit` untuk LLM-agnostic

---

## 2. Tujuan & Non-Tujuan

### Tujuan
- Menghasilkan daftar keyword yang sudah diklasifikasikan berdasarkan intent, diklustering secara semantik, dan dilengkapi data tren
- Berjalan 100% dengan tools free/OSS tanpa API key berbayar
- Kompatibel dengan semua LLM: Claude, Ollama, OpenAI-compatible, dsb.
- Dapat diinstal via Claude Code marketplace (`/plugin install`)
- Mendukung Bahasa Indonesia dan Inggris

### Non-Tujuan
- Bukan technical SEO auditor (tidak cek Core Web Vitals, schema, backlink)
- Bukan content writer / brief generator
- Tidak menggantikan Google Search Console (tidak ada data klik/impresi nyata)
- Tidak crawl website pengguna

---

## 3. Pengguna Target

| Segmen | Kebutuhan Utama |
|---|---|
| Blogger / content creator | Temukan keyword long-tail dengan cepat tanpa bayar tool SEO |
| SEO freelancer | Riset keyword klien tanpa bergantung Ahrefs/Semrush |
| Developer yang bangun produk | Validasi demand sebelum build fitur |
| Tim konten perusahaan | Riset keyword bahasa Indonesia yang relevan |

---

## 4. Arsitektur Sistem

### 4.1 Struktur Folder

```
seo-keyword-research/
├── .claude-plugin/
│   ├── plugin.json          # Marketplace manifest
│   └── marketplace.json     # Distribusi /plugin marketplace add
│
├── skills/
│   ├── seo-keyword/
│   │   ├── SKILL.md         # Orchestrator — routing + dispatch
│   │   └── references/
│   │       ├── intent-types.md       # Definisi 4 intent SEO
│   │       ├── scoring-formula.md    # Rumus Opportunity Score
│   │       └── output-formats.md     # Template laporan
│   ├── seo-cluster/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── clustering-methods.md
│   ├── seo-trends/
│   │   └── SKILL.md
│   └── seo-paa/
│       └── SKILL.md         # People Also Ask
│
├── agents/
│   ├── seo-searxng.md       # Agent: SearXNG self-hosted
│   ├── seo-autocomplete.md  # Agent: Google + DDG free endpoint
│   ├── seo-pytrends.md      # Agent: PyTrends (Google Trends)
│   ├── seo-wikipedia.md     # Agent: Wikipedia semantic enrichment
│   └── seo-nlp.md           # Agent: NLP clustering lokal
│
├── scripts/
│   ├── searxng_client.py    # Wrapper SearXNG JSON API
│   ├── autocomplete.py      # Google/DDG public endpoints
│   ├── trends.py            # PyTrends wrapper + normalisasi
│   ├── nlp_cluster.py       # spaCy + scikit-learn clustering
│   ├── wikipedia_enrich.py  # Wikipedia REST API
│   └── cache.py             # DiskCache + SQLite history
│
├── commands/
│   ├── keyword.md           # /keyword "topik"
│   └── cluster.md           # /cluster keywords.csv
│
├── templates/
│   ├── keyword-report.md    # Template output laporan
│   └── cluster-map.md       # Template peta cluster
│
├── SKILL.md                 # Entry point utama
├── CLAUDE.md                # Instruksi proyek untuk Claude Code
├── AGENTS.md                # Instruksi multi-platform (Cursor, Codex)
├── config.yaml              # SEARXNG_URL, lang, cache TTL
├── requirements.txt         # Python dependencies
├── install.sh               # Setup Unix/macOS/Linux
├── install.ps1              # Setup Windows
└── README.md
```

### 4.2 Layer Architecture

```
Layer 0 — Entry
  User: /keyword "machine learning untuk pemula"
          ↓
Layer 1 — Orchestrator (skills/seo-keyword/SKILL.md)
  - Deteksi bahasa dan intent awal
  - Dispatch parallel ke 2–5 agents sesuai kebutuhan
          ↓ (paralel)
Layer 2 — Sub-Agents (agents/*.md)
  seo-searxng     → SERP data + related searches
  seo-autocomplete → Suggestions Google/DDG
  seo-pytrends    → Tren 12 bulan + related queries
  seo-wikipedia   → Entitas semantik terkait
  seo-nlp         → Clustering + intent tagging
          ↓
Layer 3 — Scripts Python (scripts/*.py)
  Eksekutor — fetch, parse, cache, return JSON
          ↓
Layer 4 — Output
  Markdown report + JSON raw + CSV export + SQLite history
```

---

## 5. Fitur & Spesifikasi

### 5.1 Slash Commands

| Command | Deskripsi | Contoh |
|---|---|---|
| `/keyword <topik>` | Riset lengkap satu topik — autocomplete + tren + PAA + cluster | `/keyword "investasi saham pemula"` |
| `/keyword <topik> --depth 2` | Tambah kedalaman PAA (0–3) | `/keyword "cara diet" --depth 2` |
| `/keyword <topik> --lang id` | Paksa bahasa tertentu (id/en) | `/keyword "resep masakan" --lang id` |
| `/keyword <topik> --engines ac,rs` | Pilih engine: ac (autocomplete), rs (related searches), tr (trends), paa (people also ask) | `/keyword "laptop gaming" --engines ac,tr` |
| `/cluster keywords.csv` | Cluster daftar keyword dari file CSV | `/cluster my-keywords.csv` |
| `/cluster --topic <topik>` | Auto-generate seed keywords lalu cluster | `/cluster --topic "digital marketing"` |

### 5.2 Data Sources per Agent

| Agent | Source | Endpoint / Library | API Key? |
|---|---|---|---|
| `seo-searxng` | SearXNG self-hosted | `{SEARXNG_URL}/search?format=json` | Tidak |
| `seo-autocomplete` | Google Suggest | `suggestqueries.google.com/complete/search?client=firefox` | Tidak |
| `seo-autocomplete` | DuckDuckGo AC | `duckduckgo.com/ac/?q={q}&type=list` | Tidak |
| `seo-pytrends` | Google Trends | `pytrends` library (unofficial) | Tidak |
| `seo-wikipedia` | Wikipedia REST | `en.wikipedia.org/api/rest_v1/` + `id.wikipedia.org` | Tidak |
| `seo-nlp` | Lokal | `spaCy` + `scikit-learn` (on-device) | Tidak |

### 5.3 Pipeline Riset Keyword (8 Fase)

Setiap eksekusi `/keyword` menjalankan 8 fase, diumumkan ke user saat berjalan:

```
[Fase 1/8] Scope       — deteksi bahasa, intent awal, parameter pencarian
[Fase 2/8] Discover    — seed keywords dari autocomplete (Google + DDG)
[Fase 3/8] Expand      — SERP SearXNG → related searches + PAA
[Fase 4/8] Trends      — PyTrends → volume relatif, rising queries, 12-bulan tren
[Fase 5/8] Enrich      — Wikipedia API → entitas terkait, topik induk, sinonim
[Fase 6/8] Classify    — intent tagging: informational / navigational / commercial / transactional
[Fase 7/8] Cluster     — NLP grouping: pillar topics + cluster keywords
[Fase 8/8] Deliver     — output laporan prioritas + opportunity score
```

### 5.4 Skoring Keyword

Setiap keyword mendapat **Opportunity Score** berdasarkan data yang tersedia:

```
Opportunity Score = (Trend Score × Intent Value) / Estimated Difficulty

Trend Score    : 1–100 dari PyTrends interest over time (normalisasi)
Intent Value   : Informational=1, Navigational=1, Commercial=2, Transactional=3
Est. Difficulty: Estimasi dari jumlah hasil SERP + authority domain (1–100)
```

> Karena tidak ada data volume pencarian eksak (butuh Google Ads API), difficulty dan volume adalah estimasi relatif, bukan angka absolut. Ini ditampilkan transparan ke user.

### 5.5 Klasifikasi Intent

| Intent | Sinyal | Contoh |
|---|---|---|
| Informational | "apa", "cara", "bagaimana", "pengertian", "contoh" | "apa itu saham" |
| Navigational | nama brand/website spesifik | "tokopedia login" |
| Commercial | "terbaik", "review", "rekomendasi", "vs", "perbandingan" | "laptop gaming terbaik 2026" |
| Transactional | "beli", "harga", "diskon", "order", "daftar" | "beli laptop gaming murah" |

### 5.6 Output Format

Setiap `/keyword` menghasilkan:

**1. Tampilan terminal (Rich table):**
```
Keyword Research: "machine learning untuk pemula"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Keyword                          Intent    Trend  Score
 ─────────────────────────────────────────────────────
 machine learning untuk pemula    Info       87     261
 belajar machine learning gratis  Info       72     216
 kursus machine learning online   Commercial 65     390
 ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Topic Clusters: 3  |  Total Keywords: 42  |  Quick Wins: 8
```

**2. File output:**
- `KEYWORD-REPORT.md` — laporan lengkap dengan cluster map + rekomendasi
- `keywords-raw.json` — semua data mentah per keyword
- `keywords.csv` — tabel flat untuk spreadsheet

**3. SQLite history:**
- Setiap run disimpan di `~/.seo-keyword/history.db`
- Bisa diakses ulang, di-compare antar waktu

---

## 6. Konfigurasi (`config.yaml`)

```yaml
# Wajib diisi setelah install
searxng:
  url: "http://localhost:8080"   # URL SearXNG self-hosted
  timeout: 10                    # Detik
  max_results: 20                # Per query

search:
  default_lang: "id"             # id | en
  default_country: "ID"          # Kode negara ISO
  depth_limit: 1                 # PAA depth default (0–3)
  engines: ["ac", "rs", "tr", "paa"]  # Semua engine aktif by default

cache:
  enabled: true
  ttl_hours: 24                  # Cache valid 24 jam
  path: "~/.seo-keyword/cache"

output:
  dir: "./seo-output"            # Folder output laporan
  formats: ["md", "json", "csv"] # Format yang digenerate
```

---

## 7. Plugin Manifest (`.claude-plugin/plugin.json`)

```json
{
  "name": "seo-keyword-research",
  "version": "1.0.0",
  "description": "Free/OSS SEO keyword research skill. Autocomplete, trends, PAA, semantic clustering — via SearXNG self-hosted + PyTrends + spaCy. No paid API required.",
  "author": "your-github-username",
  "license": "MIT",
  "skills": ["seo-keyword", "seo-cluster", "seo-trends", "seo-paa"],
  "agents": ["seo-searxng", "seo-autocomplete", "seo-pytrends", "seo-wikipedia", "seo-nlp"],
  "commands": ["keyword", "cluster"],
  "requirements": {
    "python": ">=3.10",
    "setup": "bash install.sh"
  },
  "tags": ["seo", "keyword-research", "free", "open-source", "searxng", "nlp"]
}
```

---

## 8. SKILL.md Frontmatter (standar secondsky)

Setiap SKILL.md dimulai dengan YAML frontmatter agar Claude Code bisa auto-route:

```yaml
---
name: seo-keyword
description: >
  Riset keyword SEO lengkap dari satu topik seed. Jalankan saat user minta
  keyword research, keyword ideas, keyword suggestions, topik konten, atau
  analisis keyword. Menghasilkan daftar keyword terklasifikasi (intent),
  terklustering (semantik), dan dilengkapi data tren. Semua sumber data
  free/OSS: SearXNG self-hosted, PyTrends, Wikipedia API, spaCy.
tools: [Bash, Read, Write]
model: inherit
triggers:
  - "keyword research"
  - "riset keyword"
  - "keyword ideas"
  - "topik konten"
  - "cari keyword"
outputs:
  - KEYWORD-REPORT.md
  - keywords-raw.json
  - keywords.csv
---
```

---

## 9. Batasan & Transparansi ke User

Skill ini harus selalu jujur kepada user soal keterbatasan data:

| Keterbatasan | Cara Komunikasikan |
|---|---|
| Volume pencarian tidak akurat | Tampilkan "Trend Score (relatif)" bukan "Search Volume" |
| Difficulty adalah estimasi | Label jelas "Est. Difficulty — bukan data Ahrefs/Semrush" |
| PyTrends bisa rate-limit | Retry otomatis + pesan "Google Trends sedang throttle, coba lagi" |
| SearXNG perlu self-hosted | Setup wizard di `install.sh`, pesan error jelas jika URL tidak valid |
| spaCy model Indonesia terbatas | Fallback ke NLTK jika model `id_core_news_sm` tidak tersedia |

---

## 10. Instalasi

```bash
# Unix / macOS / Linux
git clone https://github.com/your-username/seo-keyword-research.git
bash seo-keyword-research/install.sh

# Windows
git clone https://github.com/your-username/seo-keyword-research.git
powershell -ExecutionPolicy Bypass -File seo-keyword-research\install.ps1

# Via Claude Code marketplace
/plugin marketplace add your-username/seo-keyword-research
/plugin install seo-keyword-research
```

`install.sh` otomatis:
1. Cek Python >= 3.10
2. `pip install -r requirements.txt`
3. Download spaCy model (`id_core_news_sm` + `en_core_web_sm`)
4. Buat `config.yaml` dari template + prompt isi `SEARXNG_URL`
5. Buat folder `~/.seo-keyword/` untuk cache dan history

---

## 11. Roadmap

| Fase | Fitur | Status |
|---|---|---|
| v1.0 | Core: autocomplete + SearXNG + tren + clustering + PAA | Planned |
| v1.1 | Integrasi Google Search Console (opsional, Tier 1) | Planned |
| v1.2 | Export ke Notion / Obsidian format | Planned |
| v2.0 | Competitor keyword gap analysis via SearXNG | Planned |
| v2.1 | GEO/AEO scoring — citability untuk AI search | Planned |

---

## 12. Referensi Inspirasi

| Proyek | Yang Diambil |
|---|---|
| `AgriciDaniel/claude-seo` | 3-layer architecture, agents/ folder, references/ progressive disclosure, scripts/ Python |
| `secondsky/claude-skills` | YAML frontmatter, plugin.json per-skill, model: inherit, marketplace pattern |
| `ccforseo/seo-claude-code-skills` | Skill murni SKILL.md tanpa dependency untuk tier dasar |
| `aaron-he-zhu/seo-geo-claude-skills` | 8-fase pipeline, skill contract pattern, handoff summary format |
| `chukhraiartur/seo-keyword-research-tool` | Referensi fitur: autocomplete, related searches, PAA depth |
