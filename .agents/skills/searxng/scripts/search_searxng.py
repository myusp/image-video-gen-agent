#!/usr/bin/env python3
"""Search the web using a self-hosted SearXNG instance.

Usage:
    python .agents/skills/searxng/scripts/search_searxng.py --query "my search" [options]

Options:
    --url URL         SearXNG instance URL (default: http://localhost:8888)
    --query TEXT      Search query (required)
    --limit N         Max results (default: 5)
    --category CAT    Search category: general, news, science, images, videos, files, social media
    --api-key KEY     API key if SearXNG uses authentication
    --lang CODE       Language filter: id, en, all (default: all)

Environment (.env):
    SEARXNG_URL       Default SearXNG instance URL
    SEARXNG_API_KEY   Default API key
"""

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlencode, urljoin

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def search_searxng(
    query: str,
    searxng_url: str = "http://localhost:8888",
    limit: int = 5,
    category: str = "general",
    api_key: str | None = None,
    language: str | None = None,
) -> list[dict]:
    """Search via SearXNG and return structured results.

    Args:
        query: Search query string
        searxng_url: Base URL of SearXNG instance
        limit: Maximum number of results to return
        category: Search category (general, news, science, etc.)
        api_key: Optional API key for authentication
        language: Language filter code (id, en, all)

    Returns:
        List of dicts with keys: title, url, content, engine, category, publishedDate
    """
    headers = {
        "Accept": "application/json",
        "User-Agent": "SearXNG-Skill/1.0",
    }

    if api_key:
        headers["X-API-Key"] = api_key

    params = {
        "q": query,
        "format": "json",
        "categories": category,
        "pageno": 1,
    }

    if language and language != "all":
        params["language"] = language

    search_url = urljoin(searxng_url.rstrip("/") + "/", "search")

    try:
        resp = requests.get(
            search_url,
            params=params,
            headers=headers,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.ConnectionError:
        print(
            f"ERROR: Cannot connect to SearXNG at {searxng_url}. "
            "Is the server running?",
            file=sys.stderr,
        )
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("ERROR: SearXNG request timed out after 30s", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"ERROR: SearXNG request failed: {e}", file=sys.stderr)
        if hasattr(e, "response") and e.response is not None:
            print(f"Status: {e.response.status_code}", file=sys.stderr)
            print(f"Body: {e.response.text[:500]}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print("ERROR: Invalid JSON response from SearXNG", file=sys.stderr)
        sys.exit(1)

    results = data.get("results", [])
    formatted = []

    for r in results[:limit]:
        formatted.append({
            "title": r.get("title", "").strip(),
            "url": r.get("url", ""),
            "content": r.get("content", "").strip(),
            "engine": r.get("engine", ""),
            "category": r.get("category", category),
            "publishedDate": r.get("publishedDate", ""),
        })

    return formatted


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search the web using self-hosted SearXNG",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s --query \"inflasi indonesia 2026\"\n"
            "  %(prog)s --query \"AI news\" --category news --limit 10\n"
            "  %(prog)s --query \"studi kasus\" --url http://192.168.1.5:8888\n"
        ),
    )
    parser.add_argument(
        "--url",
        default=os.getenv("SEARXNG_URL", "http://localhost:8888"),
        help="SearXNG instance URL (default: http://localhost:8888, or $SEARXNG_URL)",
    )
    parser.add_argument(
        "--query",
        required=True,
        help="Search query",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Max results (default: 5)",
    )
    parser.add_argument(
        "--category",
        default="general",
        choices=["general", "news", "science", "images", "videos", "files", "social media"],
        help="Search category (default: general)",
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("SEARXNG_API_KEY"),
        help="API key for SearXNG auth (or $SEARXNG_API_KEY)",
    )
    parser.add_argument(
        "--lang",
        default="all",
        help="Language filter: id, en, all (default: all)",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    results = search_searxng(
        query=args.query,
        searxng_url=args.url,
        limit=args.limit,
        category=args.category,
        api_key=args.api_key,
        language=args.lang,
    )

    if not results:
        print(json.dumps({"query": args.query, "results": [], "count": 0}, indent=2))
        return

    print(json.dumps({
        "query": args.query,
        "results": results,
        "count": len(results),
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
