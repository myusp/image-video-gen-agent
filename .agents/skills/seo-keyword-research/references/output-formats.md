# Output Format Templates

## Terminal Summary Table

```
Keyword Research: "machine learning untuk pemula"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Keyword                          Intent    Trend  Score  ▼
 ─────────────────────────────────────────────────────
 machine learning untuk pemula    Info       87     261
 belajar machine learning gratis  Info       72     216
 kursus machine learning online   Commercial 65     390
 ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Topic Clusters: 3  |  Total Keywords: 42  |  Quick Wins: 8
```

## KEYWORD-REPORT.md Template

```markdown
# Keyword Research: "{topic}"

**Generated:** {date}
**Language:** {lang}
**Total Keywords:** {count}
**Topic Clusters:** {cluster_count}
**Quick Wins:** {quick_wins}

---

## Top Keywords by Opportunity Score

| Keyword | Intent | Trend | Difficulty | Score | Quick Win |
|---------|--------|-------|------------|-------|-----------|
| {kw} | {intent} | {trend} | {diff} | {score} | ✅ |

---

## Topic Clusters

### Cluster 1: {pillar_topic}
- {keyword} ({intent})
- {keyword} ({intent})

### Cluster 2: {pillar_topic}
- ...

---

## Recommendations

1. **Target quick wins first** — {quick_win_count} keyword dengan difficulty rendah
2. **Pillar topic**: {pillar_topic} — buat content pillar
3. **Opportunity**: {commercial_count} keyword commercial siap dikonversi

---

## Data Sources
- Autocomplete: Google Suggest, DuckDuckGo
- SERP: SearXNG self-hosted
- Trends: PyTrends (Google Trends unofficial)
- Enrichment: Wikipedia API
- Clustering: spaCy + scikit-learn

**Disclaimer:** Trend Score adalah estimasi relatif. Bukan data Search Volume eksak dari Google Ads API.
```

## keywords-raw.json Template

```json
[
  {
    "keyword": "machine learning untuk pemula",
    "intent": "informational",
    "trend_score": 87,
    "estimated_difficulty": 33,
    "opportunity_score": 261,
    "cluster": "basic learning",
    "is_quick_win": false,
    "sources": {
      "autocomplete": true,
      "related_search": true,
      "trends": true,
      "wikipedia": false
    }
  }
]
```

## keywords.csv Template

```csv
keyword,intent,trend_score,estimated_difficulty,opportunity_score,cluster,is_quick_win
"machine learning untuk pemula",informational,87,33,261,"basic learning",false
```

## History DB Schema

SQLite di `~/.seo-keyword/history.db`:

```sql
CREATE TABLE runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT,
    lang TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_keywords INTEGER,
    clusters INTEGER,
    quick_wins INTEGER,
    engines_used TEXT
);

CREATE TABLE keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER REFERENCES runs(id),
    keyword TEXT,
    intent TEXT,
    trend_score REAL,
    difficulty REAL,
    opportunity_score REAL,
    cluster TEXT,
    is_quick_win BOOLEAN
);
```
