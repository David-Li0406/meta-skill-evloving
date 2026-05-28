#!/usr/bin/env python3
"""
Scan Miwu blog posts and summarize existing tags and categories.
"""

import argparse
import os
from collections import Counter

FRONTMATTER_DELIM = "---"


def find_frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_DELIM:
        return []
    for i in range(1, len(lines)):
        if lines[i].strip() == FRONTMATTER_DELIM:
            return lines[1:i]
    return []


def strip_quotes(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
        return value[1:-1]
    return value


def parse_tags(value):
    value = value.strip()
    if value in ("", "[]"):
        return []
    if not value.startswith("[") or not value.endswith("]"):
        return []
    inner = value[1:-1].strip()
    if not inner:
        return []
    parts = [p.strip() for p in inner.split(",")]
    tags = []
    for part in parts:
        if not part:
            continue
        tags.append(strip_quotes(part))
    return [t for t in tags if t]


def parse_frontmatter(lines):
    tags = []
    category = ""
    title = ""
    for line in lines:
        if line.startswith("title:"):
            title = strip_quotes(line.split(":", 1)[1])
        elif line.startswith("tags:"):
            tags = parse_tags(line.split(":", 1)[1])
        elif line.startswith("category:"):
            category = strip_quotes(line.split(":", 1)[1])
    return title, tags, category


def iter_post_files(posts_dir):
    for root, _dirs, files in os.walk(posts_dir):
        for name in files:
            if name == "index.md":
                yield os.path.join(root, name)


def summarize(posts_dir):
    tag_counts = Counter()
    category_counts = Counter()
    titles = []

    for path in iter_post_files(posts_dir):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        fm = find_frontmatter(text)
        if not fm:
            continue
        title, tags, category = parse_frontmatter(fm)
        if title:
            titles.append(title)
        for tag in tags:
            tag_counts[tag] += 1
        if category and category not in ("''", '""'):
            category_counts[category] += 1

    return titles, tag_counts, category_counts


def format_counts(counter):
    items = sorted(counter.items(), key=lambda x: (-x[1], x[0]))
    return items


def main():
    parser = argparse.ArgumentParser(description="Summarize tags and categories.")
    parser.add_argument(
        "--posts-dir",
        default="src/content/posts",
        help="Path to posts directory (default: src/content/posts)",
    )
    args = parser.parse_args()

    titles, tag_counts, category_counts = summarize(args.posts_dir)

    print("Existing categories:")
    for name, count in format_counts(category_counts):
        print(f"- {name} ({count})")

    print("\nExisting tags:")
    for name, count in format_counts(tag_counts):
        print(f"- {name} ({count})")

    if titles:
        print("\nRecent titles:")
        for title in titles:
            print(f"- {title}")


if __name__ == "__main__":
    main()
