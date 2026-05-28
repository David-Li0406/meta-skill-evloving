"""Create a permanent note Markdown file under an Obsidian vault.

This script is designed to be called by an AI agent. It:
- Builds YAML frontmatter (summary/created/updated/status/tags/related/aliases)
- Selects a destination folder under permanent
- Writes a new .md file using a safe filename (no overwrite by default)

It does not attempt to update backlinks or modify other notes.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


KIND_CHOICES = {"hub", "leaf", "howto", "principle", "decision", "glossary"}
STATUS_CHOICES = {"seed", "draft", "evergreen", "deprecated"}
FOLDER_CHOICES = {"00_inbox", "10_hub", "20_leaf", "30_glossary", "90_meta"}
DOMAIN_CHOICES = {"work", "learning"}


@dataclass(frozen=True)
class NoteSpec:
    title: str
    summary: str
    domain: str
    kind: str
    status: str
    topics: list[str]
    related: list[str]
    aliases: list[str]
    content: str
    target_folder: str | None


def slugify_filename(title: str, max_len: int = 120) -> str:
    text = title.strip()
    text = re.sub(r"\s+", " ", text)
    text = text.replace("/", "-")
    text = text.replace("\\", "-")

    # Windows forbidden: <>:"/\|?* and control chars
    text = re.sub(r"[<>:\"/\\|?*]", "", text)
    text = "".join(ch for ch in text if ord(ch) >= 32)

    text = text.strip().strip(".")
    if not text:
        text = "untitled"

    text = text.replace(" ", "-")
    text = re.sub(r"-+", "-", text)

    if len(text) > max_len:
        text = text[:max_len].rstrip("-")

    return f"{text}.md"


def is_simple_yaml_token(value: str) -> bool:
    return re.fullmatch(r"[A-Za-z0-9/_-]+", value) is not None


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def yaml_list(values: list[str]) -> str:
    items: list[str] = []
    for v in values:
        v = v.strip()
        if not v:
            continue
        items.append(v if is_simple_yaml_token(v) else yaml_quote(v))
    return "[" + ", ".join(items) + "]"


def build_tags(domain: str, kind: str, status: str, topics: list[str]) -> list[str]:
    tags: list[str] = []
    tags.append(f"d/{domain}")
    for t in topics:
        t = t.strip()
        if not t:
            continue
        tags.append(f"t/{t}")
    tags.append(f"k/{kind}")
    tags.append(f"s/{status}")

    # de-dup while preserving order
    seen: set[str] = set()
    out: list[str] = []
    for tag in tags:
        if tag in seen:
            continue
        seen.add(tag)
        out.append(tag)
    return out


def choose_folder(spec: NoteSpec) -> str:
    if spec.target_folder:
        return spec.target_folder

    # If summary is missing, treat as inbox material.
    if not spec.summary.strip():
        return "00_inbox"

    if spec.kind == "hub":
        return "10_hub"
    if spec.kind == "glossary":
        return "30_glossary"
    return "20_leaf"


def render_body(spec: NoteSpec) -> str:
    title_line = f"# {spec.title}\n"

    content = spec.content.strip()
    content_block = ("\n" + content + "\n") if content else ""

    if spec.kind == "hub":
        return (
            title_line
            + "\n## TL;DR\n\n"
            + content_block
            + "\n## Key Takeaways\n\n"
            + "\n## Body\n\n"
            + "\n## Leaf Links\n\n"
            + "\n## References\n"
        )

    if spec.kind == "howto":
        return (
            title_line
            + "\n## Goal\n\n"
            + content_block
            + "\n## Steps\n\n"
            + "\n## Verification\n\n"
            + "\n## Troubleshooting\n\n"
            + "\n## Related\n"
        )

    if spec.kind == "principle":
        return (
            title_line
            + "\n## Principle\n\n"
            + content_block
            + "\n## When to Apply\n\n"
            + "\n## Trade-offs\n\n"
            + "\n## Examples\n\n"
            + "\n## Related\n"
        )

    if spec.kind == "decision":
        return (
            title_line
            + "\n## Context\n\n"
            + content_block
            + "\n## Decision\n\n"
            + "\n## Consequences\n\n"
            + "\n## Alternatives Considered\n\n"
            + "\n## Related\n"
        )

    if spec.kind == "glossary":
        return (
            title_line
            + "\n## Definition\n\n"
            + content_block
            + "\n## Notes\n\n"
            + "\n## Related\n"
        )

    # leaf (default)
    return (
        title_line
        + "\n## What\n\n"
        + content_block
        + "\n## When\n\n"
        + "\n## How\n\n"
        + "\n## Pitfalls\n\n"
        + "\n## Examples\n\n"
        + "\n## Related\n"
    )


def build_frontmatter(spec: NoteSpec) -> str:
    today = date.today().isoformat()
    tags = build_tags(spec.domain, spec.kind, spec.status, spec.topics)

    lines: list[str] = []
    lines.append("---")
    lines.append(f"summary: {yaml_quote(spec.summary.strip()) if spec.summary.strip() else yaml_quote('')}")
    lines.append(f"created: {today}")
    lines.append(f"updated: {today}")
    lines.append(f"status: {spec.status}")
    lines.append(f"tags: {yaml_list(tags)}")
    lines.append(f"related: {yaml_list(spec.related)}")

    if spec.aliases:
        lines.append(f"aliases: {yaml_list(spec.aliases)}")

    lines.append("---")
    return "\n".join(lines) + "\n"


def unique_path(dir_path: Path, filename: str) -> Path:
    candidate = dir_path / filename
    if not candidate.exists():
        return candidate

    stem = Path(filename).stem
    suffix = Path(filename).suffix
    for i in range(2, 1000):
        cand = dir_path / f"{stem}-{i}{suffix}"
        if not cand.exists():
            return cand
    raise RuntimeError("Could not find an available filename")


def parse_list(value: str) -> list[str]:
    if not value.strip():
        return []
    parts = re.split(r"\s*,\s*", value.strip())
    return [p for p in parts if p]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault-root", default=str(Path.cwd()), help="Vault root directory")
    parser.add_argument("--permanent-folder", default="permanent", help="Permanent folder name")

    parser.add_argument("--title", required=True)
    parser.add_argument("--summary", default="")
    parser.add_argument("--domain", required=True, choices=sorted(DOMAIN_CHOICES))
    parser.add_argument("--kind", required=True, choices=sorted(KIND_CHOICES))
    parser.add_argument("--status", default="seed", choices=sorted(STATUS_CHOICES))

    parser.add_argument("--topics", default="", help="Comma-separated topics (<=3 recommended)")
    parser.add_argument("--related", default="", help="Comma-separated wiki links like [[X]]")
    parser.add_argument("--aliases", default="", help="Comma-separated aliases")

    parser.add_argument("--content", default="", help="Body content snippet")
    parser.add_argument("--content-file", default="", help="Path to a file whose contents become body content")

    parser.add_argument("--target-folder", default="", choices=[""] + sorted(FOLDER_CHOICES))
    parser.add_argument("--overwrite", action="store_true", help="Overwrite if the target path exists")

    args = parser.parse_args()

    spec = NoteSpec(
        title=args.title.strip(),
        summary=args.summary,
        domain=args.domain,
        kind=args.kind,
        status=args.status,
        topics=parse_list(args.topics)[:3],
        related=parse_list(args.related),
        aliases=parse_list(args.aliases),
        content="",
        target_folder=args.target_folder or None,
    )

    content = args.content
    if args.content_file:
        content_path = Path(args.content_file).expanduser()
        content = content_path.read_text(encoding="utf-8", errors="replace")

    spec = NoteSpec(
        title=spec.title,
        summary=spec.summary,
        domain=spec.domain,
        kind=spec.kind,
        status=spec.status,
        topics=spec.topics,
        related=spec.related,
        aliases=spec.aliases,
        content=content,
        target_folder=spec.target_folder,
    )

    vault_root = Path(args.vault_root).expanduser().resolve()
    permanent_root = (vault_root / args.permanent_folder).resolve()
    if not permanent_root.exists():
        raise SystemExit(f"Permanent folder not found: {permanent_root}")

    folder = choose_folder(spec)
    destination_dir = permanent_root / folder
    destination_dir.mkdir(parents=True, exist_ok=True)

    filename = slugify_filename(spec.title)
    target = destination_dir / filename

    if target.exists() and not args.overwrite:
        target = unique_path(destination_dir, filename)

    frontmatter = build_frontmatter(spec)
    body = render_body(spec)
    output = frontmatter + "\n" + body

    if target.exists() and args.overwrite:
        target.write_text(output, encoding="utf-8")
    else:
        target.write_text(output, encoding="utf-8")

    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
