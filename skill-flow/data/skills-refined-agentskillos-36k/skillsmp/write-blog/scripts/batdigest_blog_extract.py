#!/usr/bin/env python3
"""
Extract a single BatDigest blog post from data/blog.yaml into editable files.

Writes:
  - content.html (decoded HTML)
  - meta.json (title/summary/takeaways/etc.)
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


DEFAULT_BLOG_YAML = Path("~/Coding_Projects/batdigest-flask/data/blog.yaml").expanduser()
DEFAULT_OUT_ROOT = Path("/tmp/batdigest-blog-extract")


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


def _sanitize_dirname(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip())
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-")
    return cleaned or "blog-post"


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract one blog post from batdigest-flask data/blog.yaml.")
    parser.add_argument("--slug", required=True, help="Blog slug to extract.")
    parser.add_argument("--blog-yaml", default=str(DEFAULT_BLOG_YAML), help="Path to data/blog.yaml.")
    parser.add_argument(
        "--out-dir",
        help="Output directory (default: /tmp/batdigest-blog-extract/<slug>).",
    )
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files.")

    args = parser.parse_args()
    target_slug = args.slug.strip()
    if not target_slug:
        raise SystemExit("--slug is empty.")

    blog_yaml = Path(args.blog_yaml).expanduser()
    if not blog_yaml.exists():
        raise SystemExit(f"blog.yaml not found: {blog_yaml}")

    out_dir = Path(args.out_dir).expanduser() if args.out_dir else (DEFAULT_OUT_ROOT / _sanitize_dirname(target_slug))
    out_dir.mkdir(parents=True, exist_ok=True)

    content_path = out_dir / "content.html"
    meta_path = out_dir / "meta.json"
    if not args.overwrite and (content_path.exists() or meta_path.exists()):
        raise SystemExit(f"Output exists: {out_dir} (use --overwrite)")

    in_posts = False
    current = None
    list_key = None
    is_target = False

    def flush_current():
        nonlocal current, is_target
        if current is None:
            return None
        if not is_target:
            return None
        return current

    found = None

    with blog_yaml.open("r", encoding="utf-8", errors="replace") as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\n")
            stripped = line.strip()

            if stripped == "blog_posts:":
                in_posts = True
                continue
            if not in_posts:
                continue

            if line.startswith("  -") and stripped == "-":
                maybe = flush_current()
                if maybe is not None:
                    found = maybe
                    break
                current = {}
                list_key = None
                is_target = False
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
                    if is_target and key in ("key_takeaways", "key_takeaway"):
                        current["key_takeaways"] = []
                    continue

                parsed = _parse_scalar(raw_value)

                if key == "slug":
                    slug_value = str(parsed) if parsed is not None else ""
                    if slug_value == target_slug:
                        is_target = True
                        current["slug"] = slug_value
                    continue

                if not is_target:
                    continue

                if key == "is_active":
                    current[key] = _coerce_bool(parsed)
                elif key in ("created_at", "updated_at"):
                    current[key] = _parse_datetime(parsed)
                elif key == "published_date":
                    current[key] = str(parsed).strip() if parsed is not None else None
                else:
                    current[key] = parsed

                continue

            if is_target and list_key in ("key_takeaways", "key_takeaway"):
                list_item = re.match(r"^\s{6}-\s*(.*)$", line)
                if list_item:
                    item = _parse_scalar(list_item.group(1))
                    if item is not None:
                        current.setdefault("key_takeaways", []).append(str(item))

    if found is None:
        found = flush_current()

    if found is None:
        raise SystemExit(f"Slug not found: {target_slug}")

    content = found.get("content")
    if not isinstance(content, str) or not content.strip():
        raise SystemExit("Found post but content is empty.")

    content_path.write_text(content, encoding="utf-8")

    meta = {
        "slug": found.get("slug"),
        "title": found.get("title"),
        "blog_sub_heading": found.get("blog_sub_heading"),
        "blog_summary": found.get("blog_summary"),
        "key_takeaways": found.get("key_takeaways") or [],
        "category": found.get("category"),
        "is_active": found.get("is_active"),
        "feature_desktop_img": found.get("feature_desktop_img"),
        "feature_mobile_img": found.get("feature_mobile_img"),
        "thumb_img": found.get("thumb_img"),
        "created_at": found.get("created_at").isoformat() if found.get("created_at") else None,
        "updated_at": found.get("updated_at").isoformat() if found.get("updated_at") else None,
        "published_date": found.get("published_date"),
    }
    meta_path.write_text(json.dumps(meta, indent=2, sort_keys=True), encoding="utf-8")

    print(f"Wrote: {content_path}")
    print(f"Wrote: {meta_path}")


if __name__ == "__main__":
    main()
