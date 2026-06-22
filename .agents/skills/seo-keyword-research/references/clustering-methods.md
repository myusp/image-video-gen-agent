# Clustering Methods Reference

## Metode Utama: TF-IDF + Cosine Similarity + Hierarchical Clustering

### Pipeline
1. **TF-IDF Vectorization** — representasi keyword sebagai vektor numerik
2. **Cosine Distance Matrix** — hitung jarak antar semua keyword
3. **Hierarchical Clustering** — agglomerative clustering dengan ward linkage
4. **Cluster Labeling** — extract top 3 term per cluster sebagai pillar topic

### Parameter Default
- ngram_range: (1, 2) — unigram + bigram
- max_features: 1000
- distance_threshold: 0.7 (auto-cut dendrogram)
- min_cluster_size: 2

### Bahasa
- **id:** spaCy `id_core_news_sm` untuk tokenization + stop words
- **en:** spaCy `en_core_web_sm`
- **Fallback:** scikit-learn `CountVectorizer` dengan stop_words jika spaCy model tidak tersedia

### Output
- Pillar topic per cluster (top keyword dengan score tertinggi)
- Keyword list per cluster
- Inter-cluster distance matrix (opsional)
