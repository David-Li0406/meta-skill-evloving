#!/usr/bin/env python3
"""
Update an existing BatDigest blog post inside data/blog.yaml with a minimal diff.

Dry-run by default; pass --write to apply changes.

Typical usage:
  python3 scripts/batdigest_blog_extract.py --slug my-post
  # edit /tmp/batdigest-blog-extract/my-post/content.html and meta.json
  python3 scripts/batdigest_blog_update.py --slug my-post --meta-json .../meta.json --content-file .../content.html --write
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_BLOG_YAML = Path("~/Coding_Projects/batdigest-flask/data/blog.yaml").expanduser()


def _yaml_value(value: str | None) -> str:
    if value is None:
        return "null"
    text = str(value).strip()
    if not text:
        return "null"
    return json.dumps(text, ensure_ascii=True)


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


def _find_entry_bounds(lines: list[str], slug: str) -> tuple[int, int]:
    slug_line_index = None
    for index, line in enumerate(lines):
        match = re.match(r"^\s{4}slug:\s*(.*)\s*$", line)
        if not match:
            continue
        parsed = _parse_scalar(match.group(1))
        if str(parsed) == slug:
            slug_line_index = index
            break

    if slug_line_index is None:
        raise SystemExit(f"Slug not found in blog.yaml: {slug}")

    start = None
    for index in range(slug_line_index, -1, -1):
        if lines[index].startswith("  -") and lines[index].strip() == "-":
            start = index
            break
    if start is None:
        raise SystemExit("Could not locate start of entry (expected a '  -' line).")

    end = len(lines)
    for index in range(slug_line_index + 1, len(lines)):
        if lines[index].startswith("  -") and lines[index].strip() == "-":
            end = index
            break

    return start, end


def _find_key_line(block: list[str], key: str) -> int | None:
    pattern = re.compile(rf"^\s{{4}}{re.escape(key)}:\s*.*$")
    for index, line in enumerate(block):
        if pattern.match(line):
            return index
    return None


def _insert_after_last_of(block: list[str], keys: list[str], new_lines: list[str]) -> None:
    last_index = None
    for key in keys:
        index = _find_key_line(block, key)
        if index is not None:
            last_index = max(last_index or index, index)
    insert_at = (last_index + 1) if last_index is not None else 1
    block[insert_at:insert_at] = new_lines


def _set_scalar(block: list[str], key: str, value: str | None) -> bool:
    new_line = f"    {key}: {_yaml_value(value)}\n"
    index = _find_key_line(block, key)
    if index is not None:
        if block[index] == new_line:
            return False
        block[index] = new_line
        return True

    # Insert in a stable-ish spot matching blog_yaml_add.py ordering.
    preferred_predecessors = {
        "title": ["slug"],
        "content": ["title", "slug"],
        "blog_sub_heading": ["content", "title", "slug"],
        "blog_summary": ["blog_sub_heading", "content", "title", "slug"],
        "category": ["key_takeaways", "blog_summary", "blog_sub_heading", "content"],
        "updated_at": ["created_at", "category"],
        "is_active": ["updated_at", "created_at", "category"],
        "feature_desktop_img": ["is_active", "updated_at"],
        "feature_mobile_img": ["feature_desktop_img"],
        "thumb_img": ["feature_mobile_img", "feature_desktop_img"],
        "published_date": ["thumb_img", "feature_mobile_img", "feature_desktop_img", "is_active"],
    }
    _insert_after_last_of(block, preferred_predecessors.get(key, ["slug"]), [new_line])
    return True


def _remove_key_takeaways(block: list[str]) -> bool:
    for index, line in enumerate(block):
        if re.match(r"^\s{4}(key_takeaways|key_takeaway):\s*$", line):
            end = index + 1
            while end < len(block) and re.match(r"^\s{6}-\s*", block[end]):
                end += 1
            del block[index:end]
            return True
    return False


def _existing_key_takeaways(block: list[str]) -> list[str]:
    for index, line in enumerate(block):
        if re.match(r"^\s{4}(key_takeaways|key_takeaway):\s*$", line):
            items: list[str] = []
            cursor = index + 1
            while cursor < len(block):
                match = re.match(r"^\s{6}-\s*(.*)$", block[cursor])
                if not match:
                    break
                parsed = _parse_scalar(match.group(1))
                if parsed is not None:
                    text = str(parsed).strip()
                    if text:
                        items.append(text)
                cursor += 1
            return items
    return []


def _set_key_takeaways(block: list[str], takeaways: list[str] | None) -> bool:
    cleaned = [t.strip() for t in (takeaways or []) if str(t).strip()]
    existing = _existing_key_takeaways(block)
    if cleaned == existing:
        return False

    changed = _remove_key_takeaways(block)
    if not cleaned:
        return changed

    insertion_anchor = None
    for key in ("blog_summary", "blog_sub_heading", "content", "title"):
        index = _find_key_line(block, key)
        if index is not None:
            insertion_anchor = index
            break

    insert_at = (insertion_anchor + 1) if insertion_anchor is not None else 1
    lines = ["    key_takeaways:\n"]
    lines.extend([f"      - {_yaml_value(item)}\n" for item in cleaned])
    block[insert_at:insert_at] = lines
    return True


def _load_meta(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("--meta-json must be a JSON object.")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Update a BatDigest blog post in data/blog.yaml (minimal diff).")
    parser.add_argument("--slug", required=True, help="Existing slug to update.")
    parser.add_argument("--blog-yaml", default=str(DEFAULT_BLOG_YAML), help="Path to batdigest-flask data/blog.yaml.")
    parser.add_argument("--meta-json", help="Optional meta.json (like output from batdigest_blog_extract.py).")
    parser.add_argument("--content-file", help="Path to HTML fragment file to set as post.content.")

    parser.add_argument("--title", help="Set title.")
    parser.add_argument("--sub-heading", dest="blog_sub_heading", help="Set blog_sub_heading.")
    parser.add_argument("--summary", dest="blog_summary", help="Set blog_summary.")
    parser.add_argument("--category", help="Set category.")
    parser.add_argument("--is-active", help="Set is_active (0 or 1).")
    parser.add_argument("--published-date", help="Set published_date (string).")
    parser.add_argument("--feature-desktop", dest="feature_desktop_img", help="Set feature_desktop_img filename.")
    parser.add_argument("--feature-mobile", dest="feature_mobile_img", help="Set feature_mobile_img filename.")
    parser.add_argument("--thumb", dest="thumb_img", help="Set thumb_img filename.")
    parser.add_argument("--key-takeaway", action="append", dest="key_takeaways", help="Repeatable key takeaway.")

    parser.add_argument("--no-touch-updated-at", action="store_true", help="Do not modify updated_at.")
    parser.add_argument("--write", action="store_true", help="Apply changes (default: dry-run).")
    parser.add_argument("--no-backup", action="store_true", help="Disable writing a .bak backup when --write is used.")

    args = parser.parse_args()

    slug = args.slug.strip()
    if not slug:
        raise SystemExit("--slug is empty.")

    blog_yaml = Path(args.blog_yaml).expanduser()
    if not blog_yaml.exists():
        raise SystemExit(f"blog.yaml not found: {blog_yaml}")

    meta = _load_meta(Path(args.meta_json).expanduser()) if args.meta_json else {}

    content = None
    if args.content_file:
        content_path = Path(args.content_file).expanduser()
        content = content_path.read_text(encoding="utf-8")
        if not content.strip():
            raise SystemExit("content-file is empty.")

    title = args.title if args.title is not None else meta.get("title")
    blog_sub_heading = args.blog_sub_heading if args.blog_sub_heading is not None else meta.get("blog_sub_heading")
    blog_summary = args.blog_summary if args.blog_summary is not None else meta.get("blog_summary")
    category = args.category if args.category is not None else meta.get("category")
    published_date = args.published_date if args.published_date is not None else meta.get("published_date")
    feature_desktop_img = args.feature_desktop_img if args.feature_desktop_img is not None else meta.get("feature_desktop_img")
    feature_mobile_img = args.feature_mobile_img if args.feature_mobile_img is not None else meta.get("feature_mobile_img")
    thumb_img = args.thumb_img if args.thumb_img is not None else meta.get("thumb_img")

    key_takeaways = args.key_takeaways if args.key_takeaways is not None else meta.get("key_takeaways")

    is_active = None
    if args.is_active is not None:
        try:
            is_active = int(args.is_active)
        except ValueError as exc:
            raise SystemExit("--is-active must be 0 or 1.") from exc
    elif "is_active" in meta and meta["is_active"] is not None:
        is_active = 1 if bool(meta["is_active"]) else 0

    text = blog_yaml.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines(keepends=True)
    start, end = _find_entry_bounds(lines, slug)

    block = lines[start:end]
    changed_fields: list[str] = []

    if content is not None:
        if _set_scalar(block, "content", content):
            changed_fields.append("content")
    if title is not None:
        if _set_scalar(block, "title", title):
            changed_fields.append("title")
    if blog_sub_heading is not None:
        if _set_scalar(block, "blog_sub_heading", blog_sub_heading):
            changed_fields.append("blog_sub_heading")
    if blog_summary is not None:
        if _set_scalar(block, "blog_summary", blog_summary):
            changed_fields.append("blog_summary")
    if key_takeaways is not None:
        if _set_key_takeaways(block, list(key_takeaways) if isinstance(key_takeaways, list) else [str(key_takeaways)]):
            changed_fields.append("key_takeaways")
    if category is not None:
        if _set_scalar(block, "category", category):
            changed_fields.append("category")
    if published_date is not None:
        if _set_scalar(block, "published_date", published_date):
            changed_fields.append("published_date")
    if is_active is not None:
        new_line = f"    is_active: {is_active}\n"
        index = _find_key_line(block, "is_active")
        if index is not None:
            if block[index] != new_line:
                block[index] = new_line
                changed_fields.append("is_active")
        else:
            _insert_after_last_of(block, ["updated_at", "created_at", "category"], [new_line])
            changed_fields.append("is_active")
    if feature_desktop_img is not None:
        if _set_scalar(block, "feature_desktop_img", feature_desktop_img):
            changed_fields.append("feature_desktop_img")
    if feature_mobile_img is not None:
        if _set_scalar(block, "feature_mobile_img", feature_mobile_img):
            changed_fields.append("feature_mobile_img")
    if thumb_img is not None:
        if _set_scalar(block, "thumb_img", thumb_img):
            changed_fields.append("thumb_img")

    if not args.no_touch_updated_at:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")
        if _set_scalar(block, "updated_at", now):
            changed_fields.append("updated_at")

    if not changed_fields:
        print("No changes requested (or everything already matched).")
        return

    lines[start:end] = block
    new_text = "".join(lines)

    print(f"blog.yaml: {blog_yaml}")
    print(f"slug: {slug}")
    print("planned updates: " + ", ".join(dict.fromkeys(changed_fields)))

    if not args.write:
        print("dry-run: pass --write to apply")
        return

    if not args.no_backup:
        backup_path = blog_yaml.with_suffix(blog_yaml.suffix + ".bak")
        backup_path.write_text(text, encoding="utf-8")
        print(f"backup: {backup_path}")

    blog_yaml.write_text(new_text, encoding="utf-8")
    print("applied")


if __name__ == "__main__":
    main()
