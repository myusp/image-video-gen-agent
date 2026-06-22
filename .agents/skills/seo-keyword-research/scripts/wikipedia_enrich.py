#!/usr/bin/env python3
"""Enrich keyword research with Wikipedia entities, categories, and synonyms.

Usage:
    python wikipedia_enrich.py --topic "investasi saham" --lang id
    python wikipedia_enrich.py --topic "machine learning" --lang en
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cache import CacheManager


WIKIPEDIA_API = {
    "id": "https://id.wikipedia.org/w/api.php",
    "en": "https://en.wikipedia.org/w/api.php",
}


def search_wikipedia(query: str, lang: str = "id", limit: int = 5) -> dict:
    """Search Wikipedia for entities related to the query."""
    api_url = WIKIPEDIA_API.get(lang, WIKIPEDIA_API["en"])

    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "srlimit": limit,
        "srprop": "snippet|titlesnippet",
    }

    url = f"{api_url}?{urllib.parse.urlencode(params)}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "SEOKeywordSkill/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data
    except Exception as e:
        return {"error": str(e)}


def get_page_categories(page_id: int, lang: str = "id") -> list[str]:
    """Get categories for a Wikipedia page."""
    api_url = WIKIPEDIA_API.get(lang, WIKIPEDIA_API["en"])
    params = {
        "action": "query",
        "format": "json",
        "pageids": page_id,
        "prop": "categories",
        "cllimit": 20,
    }

    url = f"{api_url}?{urllib.parse.urlencode(params)}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "SEOKeywordSkill/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            if str(page_id) in pages:
                cats = pages[str(page_id)].get("categories", [])
                return [
                    cat["title"].replace("Kategori:", "").replace("Category:", "")
                    for cat in cats
                ]
    except Exception:
        pass
    return []


def extract_related_terms(query: str, lang: str = "id") -> dict:
    """Extract related terms, categories, and synonyms from Wikipedia."""
    result = {
        "query": query,
        "lang": lang,
        "articles": [],
        "categories": [],
        "super_categories": [],
        "related_topics": [],
    }

    search_data = search_wikipedia(query, lang)
    if "error" in search_data:
        result["error"] = search_data["error"]
        return result

    search_results = search_data.get("query", {}).get("search", [])
    for item in search_results[:5]:
        article = {
            "title": item.get("title", ""),
            "page_id": item.get("pageid", 0),
            "snippet": item.get("snippet", "").replace("<span class=\"searchmatch\">", "").replace("</span>", ""),
        }
        result["articles"].append(article)

        # Get categories
        if article["page_id"]:
            cats = get_page_categories(article["page_id"], lang)
            article["categories"] = cats
            result["categories"].extend(cats)

    # Deduplicate categories
    result["categories"] = list(set(result["categories"]))

    # Extract super-categories (concept-level)
    super_cats = [c for c in result["categories"] if " " not in c and len(c) > 3]
    result["super_categories"] = super_cats[:10]

    # Extract related topics from search titles
    all_titles = [a["title"] for a in result["articles"]]
    result["related_topics"] = all_titles

    return result


def main():
    parser = argparse.ArgumentParser(description="Enrich keywords with Wikipedia data")
    parser.add_argument("--topic", required=True, help="Topic to enrich")
    parser.add_argument("--lang", default="id", help="Language (id/en)")
    parser.add_argument("--no-cache", action="store_true", help="Skip cache")
    args = parser.parse_args()

    cache = CacheManager("wikipedia", ttl_hours=48)
    cache_key = f"{args.topic}:{args.lang}"

    if not args.no_cache:
        cached = cache.get(cache_key)
        if cached is not None:
            print(json.dumps(cached, indent=2))
            return

    print(f"[wikipedia] Enriching topic: {args.topic} ({args.lang})", file=sys.stderr)
    result = extract_related_terms(args.topic, args.lang)

    cache.set(cache_key, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
