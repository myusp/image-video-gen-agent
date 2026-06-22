#!/usr/bin/env python3
"""Cluster keywords using TF-IDF + hierarchical clustering.

Usage:
    python nlp_cluster.py --input keywords-raw.json --lang id
    python nlp_cluster.py --keywords "machine learning,deep learning,neural network" --lang en
"""

import argparse
import json
import sys
from pathlib import Path


def cluster_keywords(keywords: list[str], lang: str = "id") -> dict:
    """Cluster keywords using TF-IDF + hierarchical clustering."""
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.cluster import AgglomerativeClustering
        from sklearn.metrics.pairwise import cosine_distances
    except ImportError:
        return {"error": "scikit-learn not installed. Run: pip install scikit-learn"}

    if len(keywords) < 2:
        return {
            "clusters": [{"pillar": keywords[0] if keywords else "", "keywords": keywords}],
            "total_clusters": 1,
            "method": "single_keyword",
        }

    # Try loading spaCy stop words
    stop_words = None
    try:
        import spacy
        model = "id_core_news_sm" if lang == "id" else "en_core_web_sm"
        try:
            nlp = spacy.load(model)
            stop_words = list(nlp.Defaults.stop_words)
        except OSError:
            print(f"[nlp_cluster] spaCy model '{model}' not found. Using sklearn defaults.", file=sys.stderr)
    except ImportError:
        print("[nlp_cluster] spaCy not installed. Using sklearn defaults.", file=sys.stderr)

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=1000,
        stop_words=stop_words or "english" if lang == "en" else None,
        analyzer="char_wb",
    )

    try:
        X = vectorizer.fit_transform(keywords)
    except ValueError:
        # Fallback: all keywords identical or empty
        return {
            "clusters": [{"pillar": keywords[0], "keywords": keywords}],
            "total_clusters": 1,
            "method": "fallback_identical",
        }

    n_clusters = min(len(keywords) - 1, max(2, len(keywords) // 3))

    if n_clusters < 2:
        return {
            "clusters": [{"pillar": keywords[0], "keywords": keywords}],
            "total_clusters": 1,
            "method": "too_few",
        }

    # Agglomerative clustering
    cluster = AgglomerativeClustering(
        n_clusters=n_clusters,
        metric="cosine",
        linkage="average",
    )
    labels = cluster.fit_predict(X.toarray() if hasattr(X, "toarray") else X)

    # Build cluster output
    clusters_dict: dict[int, list[str]] = {}
    for kw, label in zip(keywords, labels):
        label = int(label)
        if label not in clusters_dict:
            clusters_dict[label] = []
        clusters_dict[label].append(kw)

    # Compute centroid for each cluster to find pillar topic
    dist_matrix = cosine_distances(X)
    result_clusters = []
    for label, cluster_kws in clusters_dict.items():
        indices = [i for i, kw in enumerate(keywords) if kw in cluster_kws]
        if not indices:
            continue
        # Find keyword closest to centroid
        cluster_distances = dist_matrix[indices][:, indices].mean(axis=1)
        centroid_idx = indices[cluster_distances.argmin()]
        pillar = keywords[centroid_idx]

        result_clusters.append({
            "pillar": pillar,
            "keyword_count": len(cluster_kws),
            "keywords": cluster_kws,
        })

    # Sort by cluster size descending
    result_clusters.sort(key=lambda c: c["keyword_count"], reverse=True)

    return {
        "clusters": result_clusters,
        "total_clusters": len(result_clusters),
        "total_keywords": len(keywords),
        "method": "tfidf_hierarchical",
        "n_clusters_requested": n_clusters,
    }


def main():
    parser = argparse.ArgumentParser(description="Cluster keywords using NLP")
    parser.add_argument("--input", help="Path to keywords-raw.json")
    parser.add_argument("--keywords", help="Comma-separated keywords (alternative to --input)")
    parser.add_argument("--lang", default="id", help="Language (id/en)")
    args = parser.parse_args()

    keywords = []

    if args.input:
        with open(args.input) as f:
            data = json.load(f)
        if isinstance(data, list):
            keywords = [item.get("keyword", "") if isinstance(item, dict) else str(item) for item in data]
        elif isinstance(data, dict):
            keywords = data.get("keywords", [])
    elif args.keywords:
        keywords = [kw.strip() for kw in args.keywords.split(",")]
    else:
        print("[nlp_cluster] Provide --input or --keywords", file=sys.stderr)
        sys.exit(1)

    keywords = [kw for kw in keywords if kw.strip()]
    print(f"[nlp_cluster] Clustering {len(keywords)} keywords (lang={args.lang})", file=sys.stderr)

    result = cluster_keywords(keywords, args.lang)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
