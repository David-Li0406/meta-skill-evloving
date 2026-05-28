"""
Utilities to ensure SQLite + FTS5 availability with graceful fallbacks.

This helper attempts to load the standard library `sqlite3` module and verify
that it was compiled with FTS5 support. If FTS5 is unavailable, it tries to
import `pysqlite3` (which bundles a modern SQLite build with FTS5 enabled).
When all attempts fail, the helper degrades to fuzzy `LIKE` queries so that
callers can keep the feature usable, albeit with reduced ranking quality.
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Iterable, Protocol


class SQLiteModule(Protocol):
    def connect(self, *args: Any, **kwargs: Any) -> Any: ...


def _has_fts5(sqlite_mod: SQLiteModule) -> bool:
    """Return True if the sqlite module advertises FTS5 support."""
    try:
        conn = sqlite_mod.connect(":memory:")
        try:
            rows = conn.execute("PRAGMA compile_options;").fetchall()
            if any(
                "FTS5" in (row[0] if isinstance(row, Iterable) else "") for row in rows
            ):
                return True
            # Fallback: attempt to create a throwaway FTS5 table to confirm support
            conn.execute("CREATE VIRTUAL TABLE temp_fts_probe USING fts5(x);")
            conn.execute("DROP TABLE temp_fts_probe;")
            return True
        finally:
            conn.close()
    except Exception:
        return False


@dataclass(frozen=True)
class SQLiteSupport:
    """Bundle metadata about the loaded SQLite module."""

    sqlite: SQLiteModule
    has_fts5: bool
    fuzzy_mode: bool
    source: str


@lru_cache(maxsize=1)
def load_sqlite_with_fts() -> SQLiteSupport:
    """
    Load a sqlite module with FTS5 support if possible.

    Returns metadata about the loaded module and whether callers should degrade
    to fuzzy LIKE queries (when `fuzzy_mode` is True).
    """
    base_mod = importlib.import_module("sqlite3")
    if _has_fts5(base_mod):
        return SQLiteSupport(
            sqlite=base_mod, has_fts5=True, fuzzy_mode=False, source="stdlib"
        )

    # stdlib lacked FTS5; try bundled wheel
    try:
        bundled = importlib.import_module("pysqlite3")
        if _has_fts5(bundled):
            return SQLiteSupport(
                sqlite=bundled, has_fts5=True, fuzzy_mode=False, source="pysqlite3"
            )
    except ModuleNotFoundError:
        pass

    # Fall back to stdlib without FTS5; signal fuzzy mode
    return SQLiteSupport(
        sqlite=base_mod, has_fts5=False, fuzzy_mode=True, source="stdlib-no-fts"
    )
