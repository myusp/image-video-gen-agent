#!/usr/bin/env python3
"""Fetch autocomplete suggestions from Google Suggest + DuckDuckGo.

Usage:
    python autocomplete.py --query "investasi saham pemula" --lang id
    python autocomplete.py --query "machine learning" --lang en --engine google
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

# Add project root to path for cache import
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cache import CacheManager


def fetch_google(query: str, lang: str = "id") -> list[str]:
    """Fetch suggestions from Google Suggest API (free, no key)."""
    params = {
        "client": "firefox",
        "q": query,
        "hl": lang,
    }
    url = f"https://suggestqueries.google.com/complete/search?{urllib.parse.urlencode(params)}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data[1] if len(data) > 1 else []
    except Exception as e:
        print(f"[autocomplete] Google suggest error: {e}", file=sys.stderr)
        return []


def fetch_duckduckgo(query: str) -> list[str]:
    """Fetch suggestions from DuckDuckGo Suggest API (free, no key)."""
    url = f"https://duckduckgo.com/ac/?q={urllib.parse.quote(query)}&type=list"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return [item.get("phrase", "") for item in data if isinstance(item, dict)]
    except Exception as e:
        print(f"[autocomplete] DuckDuckGo error: {e}", file=sys.stderr)
        return []


def main():
    parser = argparse.ArgumentParser(description="Fetch autocomplete keyword suggestions")
    parser.add_argument("--query", required=True, help="Seed keyword")
    parser.add_argument("--lang", default="id", help="Language code (id/en)")
    parser.add_argument("--engine", choices=["google", "duckduckgo", "all"], default="all", help="Engine to use")
    parser.add_argument("--no-cache", action="store_true", help="Skip cache")
    args = parser.parse_args()

    cache = CacheManager("autocomplete", ttl_hours=24)
    cache_key = f"{args.query}:{args.lang}:{args.engine}"

    if not args.no_cache:
        cached = cache.get(cache_key)
        if cached is not None:
            print(json.dumps(cached, indent=2))
            return

    results = {}

    if args.engine in ("google", "all"):
        google_results = fetch_google(args.query, args.lang)
        results["google"] = google_results
        print(f"[autocomplete] Google: {len(google_results)} suggestions", file=sys.stderr)

    if args.engine in ("duckduckgo", "all"):
        ddg_results = fetch_duckduckgo(args.query)
        results["duckduckgo"] = ddg_results
        print(f"[autocomplete] DuckDuckGo: {len(ddg_results)} suggestions", file=sys.stderr)

    # Merge all suggestions, deduplicate
    all_suggestions = []
    seen = set()
    for engine_results in results.values():
        for suggestion in engine_results:
            lower = suggestion.lower().strip()
            if lower and lower not in seen:
                seen.add(lower)
                all_suggestions.append(suggestion)

    output = {
        "query": args.query,
        "lang": args.lang,
        "engine": args.engine,
        "suggestions": all_suggestions,
        "total": len(all_suggestions),
        "per_engine": results,
    }

    cache.set(cache_key, output)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
