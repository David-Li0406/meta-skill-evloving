#!/usr/bin/env python3
"""
List/sort BatDigest blog posts from data/blog.yaml to help pick refresh candidates.

Default blog.yaml location:
  ~/Coding_Projects/batdigest-flask/data/blog.yaml
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_BLOG_YAML = Path("~/Coding_Projects/batdigest-flask/data/blog.yaml").expanduser()


@dataclass(frozen=True)
class BlogMeta:
    slug: str
    title: str | None
    category: str | None
    created_at: datetime | None
    updated_at: datetime | None
    published_date: datetime | None
    is_active: bool | None
    blog_summary: str | None
    takeaways_count: int
    feature_desktop_img: str | None


def _parse_scalar(raw: str):
    value = raw.strip()
    if value in ("", "null", "None"):
        return None

    if value.startswith('"') and value.endswith('"'):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value[1:-1]

    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]

    lowered = value.lower()
    if lowered in ("true", "false"):
        return lowered == "true"

    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def _coerce_bool(value) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(int(value))
    text = str(value).strip().lower()
    if text in ("1", "true", "yes", "y"):
        return True
    if text in ("0", "false", "no", "n"):
        return False
    return None


def _parse_datetime(value) -> datetime | None:
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    text = str(value).strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1]
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def _iter_blog_meta(path: Path):
    if not path.exists():
        raise SystemExit(f"blog.yaml not found: {path}")

    in_posts = False
    current = None
    current_slug = None
    list_key = None

    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\n")
            stripped = line.strip()

            if stripped == "blog_posts:":
                in_posts = True
                continue
            if not in_posts:
                continue

            if line.startswith("  -") and stripped == "-":
                if current is not None and current_slug:
                    yield current
                current = {
                    "slug": None,
                    "title": None,
                    "category": None,
                    "created_at": None,
                    "updated_at": None,
                    "published_date": None,
                    "is_active": None,
                    "blog_summary": None,
                    "takeaways_count": 0,
                    "feature_desktop_img": None,
                }
                current_slug = None
                list_key = None
                continue

            if current is None:
                continue

            key_match = re.match(r"^\s{4}([A-Za-z0-9_]+):\s*(.*)$", line)
            if key_match:
                key = key_match.group(1)
                raw_value = key_match.group(2).strip()
                list_key = None

                if raw_value == "":
                    list_key = key
                    continue

                parsed = _parse_scalar(raw_value)

                if key == "slug":
                    current_slug = str(parsed) if parsed is not None else None
                    current["slug"] = current_slug
                elif key in current:
                    current[key] = parsed

                continue

            if list_key in ("key_takeaways", "key_takeaway"):
                list_item = re.match(r"^\s{6}-\s*(.*)$", line)
                if list_item:
                    current["takeaways_count"] += 1

    if current is not None and current_slug:
        yield current


def _to_meta(payload) -> BlogMeta:
    return BlogMeta(
        slug=payload["slug"],
        title=payload.get("title"),
        category=payload.get("category"),
        created_at=_parse_datetime(payload.get("created_at")),
        updated_at=_parse_datetime(payload.get("updated_at")),
        published_date=_parse_datetime(payload.get("published_date")),
        is_active=_coerce_bool(payload.get("is_active")),
        blog_summary=payload.get("blog_summary"),
        takeaways_count=int(payload.get("takeaways_count") or 0),
        feature_desktop_img=payload.get("feature_desktop_img"),
    )


def _pick_sort_dt(meta: BlogMeta, sort_key: str) -> datetime | None:
    if sort_key == "updated_at":
        return meta.updated_at or meta.created_at or meta.published_date
    if sort_key == "created_at":
        return meta.created_at or meta.updated_at or meta.published_date
    if sort_key == "published_date":
        return meta.published_date or meta.updated_at or meta.created_at
    raise ValueError(f"Unknown sort key: {sort_key}")


def main() -> None:
    parser = argparse.ArgumentParser(description="List/sort BatDigest blog posts for refresh candidates.")
    parser.add_argument("--blog-yaml", default=str(DEFAULT_BLOG_YAML), help="Path to batdigest-flask data/blog.yaml.")
    parser.add_argument("--top", type=int, default=25, help="How many rows to print (default: 25).")
    parser.add_argument(
        "--sort",
        choices=("updated_at", "created_at", "published_date"),
        default="updated_at",
        help="Sort by date field (default: updated_at).",
    )
    parser.add_argument("--include-drafts", action="store_true", help="Include is_active=0 posts.")
    parser.add_argument("--missing-summary", action="store_true", help="Only posts missing blog_summary.")
    parser.add_argument("--missing-takeaways", action="store_true", help="Only posts missing key_takeaways.")
    parser.add_argument("--missing-images", action="store_true", help="Only posts missing feature_desktop_img.")
    parser.add_argument("--contains", help="Filter where slug or title contains this text (case-insensitive).")

    args = parser.parse_args()

    path = Path(args.blog_yaml).expanduser()
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    metas = [_to_meta(payload) for payload in _iter_blog_meta(path)]

    if not args.include_drafts:
        metas = [meta for meta in metas if meta.is_active is not False]

    if args.missing_summary:
        metas = [meta for meta in metas if not (meta.blog_summary or "").strip()]
    if args.missing_takeaways:
        metas = [meta for meta in metas if meta.takeaways_count == 0]
    if args.missing_images:
        metas = [meta for meta in metas if not (meta.feature_desktop_img or "").strip() or meta.feature_desktop_img in ("None", "null")]

    if args.contains:
        needle = args.contains.strip().lower()
        metas = [
            meta
            for meta in metas
            if needle in meta.slug.lower()
            or needle in (meta.title or "").lower()
        ]

    def sort_key(meta: BlogMeta):
        dt = _pick_sort_dt(meta, args.sort)
        if not dt:
            return (1, 0)  # unknown date => oldest first
        age_days = int((now - dt).total_seconds() // 86400)
        return (0, -age_days)

    metas.sort(key=sort_key)

    rows = metas[: max(0, args.top)]
    if not rows:
        print("No posts matched.")
        return

    print(f"blog.yaml: {path}")
    print(f"Showing {len(rows)} of {len(metas)} (sorted by {args.sort}, oldest first)")
    print("")

    for meta in rows:
        dt = _pick_sort_dt(meta, args.sort)
        age = "?"
        dt_text = "unknown"
        if dt:
            age = str(int((now - dt).total_seconds() // 86400))
            dt_text = dt.isoformat(sep=" ", timespec="seconds")
        active = "live" if meta.is_active else "draft"
        category = meta.category or "-"
        title = (meta.title or "").strip() or "-"
        print(f"{age:>4}d  {dt_text:<19}  {active:<5}  {category:<12}  {meta.slug}  {title}")


if __name__ == "__main__":
    main()

