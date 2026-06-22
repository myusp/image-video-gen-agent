# Opportunity Score Formula

## Formula

```
Opportunity Score = (Trend Score × Intent Value) / Est. Difficulty
```

## Components

### Trend Score (1-100)
- Dari PyTrends interest over time — normalisasi ke skala 1-100
- Jika PyTrends tidak tersedia (rate-limit): fallback ke jumlah related searches
- Jika data tren tidak ada sama sekali: default 50 (neutral)

### Intent Value
| Intent | Value |
|--------|-------|
| Informational | 1 |
| Navigational | 1 |
| Commercial | 2 |
| Transactional | 3 |

### Est. Difficulty (1-100)
- Estimasi dari jumlah hasil SERP: lebih banyak hasil = lebih kompetitif
- Semakin banyak domain authority tinggi di SERP = difficulty naik
- **Bukan data Ahrefs/Semrush** — ditampilkan sebagai estimasi

## Prioritas Sorting

1. Score tertinggi → prioritas utama
2. Jika score sama: utamakan Commercial/Transactional > Informational
3. Jika intent sama: utamakan Trend Score lebih tinggi

## Quick Wins

Keyword dengan kriteria:
- Opportunity Score >= 150
- Est. Difficulty < 30
- Trend Score >= 40

Label sebagai "Quick Win" di output.
