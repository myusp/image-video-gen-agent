#!/usr/bin/env python3
"""Disk-based cache with SQLite for SEO keyword research scripts.

Backend: diskcache (DiskCache) with optional SQLite fallback.
Cache location: ~/.seo-keyword/cache/
"""

import json
import os
import time
from pathlib import Path


CACHE_DIR = Path.home() / ".seo-keyword" / "cache"


class CacheManager:
    """Simple TTL-based cache manager using diskcache when available, JSON files as fallback."""

    def __init__(self, namespace: str, ttl_hours: int = 24):
        self.namespace = namespace
        self.ttl_seconds = ttl_hours * 3600
        self.cache_path = CACHE_DIR / namespace
        self.cache_path.mkdir(parents=True, exist_ok=True)

        self._diskcache = None
        self._init_diskcache()

    def _init_diskcache(self):
        """Try to initialize diskcache."""
        try:
            import diskcache
            self._diskcache = diskcache.Cache(str(self.cache_path / "cache.db"))
        except ImportError:
            pass

    def get(self, key: str):
        """Get cached value. Returns None if expired or missing."""
        if self._diskcache:
            try:
                return self._diskcache.get(key, default=None)
            except Exception:
                return None

        # Fallback: file-based cache
        filepath = self.cache_path / _safe_filename(key)
        if filepath.exists():
            try:
                data = json.loads(filepath.read_text())
                if time.time() - data.get("_cached_at", 0) < self.ttl_seconds:
                    return data.get("value")
            except (json.JSONDecodeError, KeyError):
                pass
        return None

    def set(self, key: str, value):
        """Set cached value."""
        if self._diskcache:
            try:
                self._diskcache.set(key, value, expire=self.ttl_seconds)
                return
            except Exception:
                pass

        # Fallback: file-based cache
        filepath = self.cache_path / _safe_filename(key)
        data = {"_cached_at": time.time(), "value": value}
        filepath.write_text(json.dumps(data, default=str))

    def clear(self):
        """Clear all cached entries for this namespace."""
        if self._diskcache:
            try:
                self._diskcache.clear()
                return
            except Exception:
                pass
        import shutil
        for f in self.cache_path.iterdir():
            if f.is_dir():
                shutil.rmtree(f)
            else:
                f.unlink()


def _safe_filename(key: str) -> str:
    """Convert a key to a safe filename."""
    import hashlib
    return hashlib.md5(key.encode()).hexdigest() + ".json"
