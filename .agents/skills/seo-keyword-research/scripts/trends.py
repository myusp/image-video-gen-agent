#!/usr/bin/env python3
"""Fetch Google Trends data via PyTrends.

Usage:
    python trends.py --keywords "investasi saham pemula,belajar saham" --lang id
    python trends.py --keywords "machine learning" --lang en --geo US
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cache import CacheManager


def fetch_trends(keywords: list[str], lang: str = "id", geo: str = "ID", retries: int = 2) -> dict:
    """Fetch trends data using PyTrends."""
    try:
        from pytrends.request import TrendReq
    except ImportError:
        print("[trends] pytrends not installed. Run: pip install pytrends", file=sys.stderr)
        return {"error": "pytrends not installed"}

    for attempt in range(retries + 1):
        try:
            pytrends = TrendReq(hl=f"{lang}-{geo}" if lang == "id" else lang,
                                tz=480, timeout=10)
            pytrends.build_payload(keywords, cat=0, timeframe="today 12-m", geo=geo, gprop="")

            result = {}

            # Interest over time
            iot = pytrends.interest_over_time()
            if iot is not None and not iot.empty:
                # Drop the partial last week
                if "isPartial" in iot.columns:
                    iot = iot[iot["isPartial"] == False]  # noqa
                result["interest_over_time"] = {
                    str(idx.date()): {k: int(v) for k, v in row.items() if k != "isPartial"}
                    for idx, row in iot.iterrows()
                }
                # Normalized trend score (1-100)
                values = [v for row in result["interest_over_time"].values() for v in row.values()]
                result["trend_score"] = round(sum(values) / len(values)) if values else 50
            else:
                result["trend_score"] = 50

            # Related queries
            rq = pytrends.related_queries()
            if rq:
                related = {}
                for kw in keywords:
                    if kw in rq and rq[kw] is not None:
                        top = rq[kw].get("top")
                        rising = rq[kw].get("rising")
                        if top is not None and not top.empty:
                            related[kw] = {
                                "top": top.head(10).to_dict(orient="records"),
                                "rising": rising.head(10).to_dict(orient="records") if rising is not None and not rising.empty else [],
                            }
                result["related_queries"] = related

            return result

        except Exception as e:
            err_msg = str(e).lower()
            if "429" in err_msg or "too many" in err_msg:
                if attempt < retries:
                    import time
                    wait = (attempt + 1) * 5
                    print(f"[trends] Rate limited, retrying in {wait}s (attempt {attempt+1}/{retries})", file=sys.stderr)
                    time.sleep(wait)
                    continue
                return {"error": "Google Trends rate limited. Try again later."}
            return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Fetch Google Trends data")
    parser.add_argument("--keywords", required=True, help="Comma-separated keywords")
    parser.add_argument("--lang", default="id", help="Language code")
    parser.add_argument("--geo", default="ID", help="Geo code (ID/US)")
    parser.add_argument("--no-cache", action="store_true", help="Skip cache")
    args = parser.parse_args()

    keywords = [kw.strip() for kw in args.keywords.split(",")]
    cache = CacheManager("trends", ttl_hours=12)
    cache_key = f"{args.keywords}:{args.lang}:{args.geo}"

    if not args.no_cache:
        cached = cache.get(cache_key)
        if cached is not None:
            print(json.dumps(cached, indent=2))
            return

    print(f"[trends] Fetching trends for: {keywords}", file=sys.stderr)
    result = fetch_trends(keywords, args.lang, args.geo)

    result["query"] = args.keywords
    result["lang"] = args.lang
    result["geo"] = args.geo

    cache.set(cache_key, result)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
