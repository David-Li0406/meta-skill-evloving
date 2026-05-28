#!/usr/bin/env python3
"""Generate or update table of contents in markdown documents.

Usage:
    # Update ToC in a single document
    python generate_toc.py <file>

    # Update ToC in all markdown files in a directory
    python generate_toc.py <directory>

    # Preview without writing (dry-run)
    python generate_toc.py <path> --dry-run

The ToC is placed under a standardized heading: ## Table of Contents
This heading has anchor: #table-of-contents

Requirements:
    pip install markdown-it-py
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
  from markdown_it import MarkdownIt
except ImportError:
  print(
    "Error: markdown-it-py is required. Install with: pip install markdown-it-py",
    file=sys.stderr,
  )
  sys.exit(1)


# Standard ToC heading - consistent across all documents
TOC_HEADING = "## Table of Contents"
TOC_ANCHOR = "table-of-contents"


@dataclass
class Heading:
  """Represents a heading in a markdown document."""

  level: int
  text: str
  slug: str
  line: int


def slugify(text: str) -> str:
  """Convert heading text to anchor slug (GitHub-Flavored Markdown style)."""
  slug = text.lower()
  slug = re.sub(r"\s+", "-", slug)
  slug = re.sub(r"[^a-z0-9\-]", "", slug)
  slug = re.sub(r"-+", "-", slug)
  return slug.strip("-")


def strip_frontmatter(content: str) -> tuple[str, int]:
  """Strip YAML frontmatter from markdown content.

  Returns:
      Tuple of (content without frontmatter, number of lines stripped)
  """
  lines = content.split("\n")

  if not lines or lines[0].strip() != "---":
    return content, 0

  for i, line in enumerate(lines[1:], start=1):
    if line.strip() == "---":
      remaining_lines = lines[i + 1 :]
      return "\n".join(remaining_lines), i + 1

  return content, 0


def parse_headings(content: str, frontmatter_lines: int = 0) -> list[Heading]:
  """Parse all headings from markdown content."""
  md = MarkdownIt()
  tokens = md.parse(content)

  headings: list[Heading] = []

  i = 0
  while i < len(tokens):
    token = tokens[i]

    if token.type == "heading_open":
      level = int(token.tag[1])
      line = (token.map[0] if token.map else 0) + frontmatter_lines

      if i + 1 < len(tokens) and tokens[i + 1].type == "inline":
        text = tokens[i + 1].content
      else:
        text = ""

      headings.append(
        Heading(
          level=level,
          text=text,
          slug=slugify(text),
          line=line,
        )
      )

    i += 1

  return headings


def build_heading_path(heading: Heading, headings: list[Heading]) -> str:
  """Build the full hierarchical path for a heading."""
  path_parts: list[str] = []
  heading_idx = headings.index(heading)

  current_level = heading.level
  for h in reversed(headings[: heading_idx + 1]):
    if h.level < current_level:
      path_parts.insert(0, h.slug)
      current_level = h.level
    elif h == heading:
      path_parts.append(h.slug)

  return "/".join(path_parts)


def generate_toc_content(headings: list[Heading], min_level: int = 2) -> str:
  """Generate the table of contents markdown.

  Args:
      headings: List of headings to include
      min_level: Minimum heading level to include (default: 2 = ##)

  Returns:
      Markdown formatted table of contents
  """
  # Filter out the ToC heading itself and headings above min_level
  filtered = [h for h in headings if h.level >= min_level and h.slug != TOC_ANCHOR]

  if not filtered:
    return ""

  # Track slug occurrences to identify ambiguous anchors
  slug_counts: dict[str, int] = {}
  for h in filtered:
    slug_counts[h.slug] = slug_counts.get(h.slug, 0) + 1

  lines: list[str] = []

  # Find the base level (usually 2 for ##)
  base_level = min(h.level for h in filtered)

  for h in filtered:
    # Calculate indent (0 spaces for base level, 2 for each level deeper)
    indent = "  " * (h.level - base_level)

    # Determine anchor - use full path if ambiguous
    anchor = build_heading_path(h, headings) if slug_counts[h.slug] > 1 else h.slug

    lines.append(f"{indent}- [{h.text}](#{anchor})")

  return "\n".join(lines)


def find_toc_section(
  lines: list[str], frontmatter_end: int = 0
) -> tuple[int, int] | None:
  """Find existing ToC section in the document.

  Returns:
      Tuple of (start_line, end_line) or None if not found.
      Lines are 0-indexed into the lines list.
  """
  toc_start = None

  for i, line in enumerate(lines):
    # Skip frontmatter
    if i < frontmatter_end:
      continue

    # Found ToC heading
    if line.strip() == TOC_HEADING:
      toc_start = i
      continue

    # If we're in ToC, look for the next heading to mark the end
    if toc_start is not None:
      # Next heading (any level) marks end of ToC content
      if line.strip().startswith("#"):
        return (toc_start, i)

  # ToC found but no heading after it (ToC at end of doc)
  if toc_start is not None:
    # Find last non-empty line after ToC
    end = len(lines)
    while end > toc_start and not lines[end - 1].strip():
      end -= 1
    return (toc_start, end)

  return None


def find_insertion_point(
  lines: list[str], headings: list[Heading], frontmatter_end: int = 0
) -> int:
  """Find the best place to insert a new ToC.

  Strategy:
  1. After frontmatter + title (h1) + Related Documents section, if present
  2. After frontmatter + title (h1), if present
  3. After frontmatter
  """
  # Start after frontmatter
  insert_at = frontmatter_end

  # Skip blank lines after frontmatter
  while insert_at < len(lines) and not lines[insert_at].strip():
    insert_at += 1

  # Look for h1 title
  h1_found = False
  for h in headings:
    if h.level == 1:
      # Find end of h1 line
      insert_at = h.line + 1
      h1_found = True
      break

  if not h1_found:
    return insert_at

  # Skip blank lines after h1
  while insert_at < len(lines) and not lines[insert_at].strip():
    insert_at += 1

  # Check if next section is "Related Documents" - if so, place ToC after it
  for h in headings:
    if h.slug == "related-documents" and h.line >= insert_at:
      # Find the end of the Related Documents section
      h_idx = headings.index(h)
      if h_idx + 1 < len(headings):
        # Next heading marks end of Related Documents
        insert_at = headings[h_idx + 1].line
      else:
        # Related Documents is last section - insert at end
        insert_at = len(lines)

      # Back up over trailing blank lines
      while insert_at > 0 and not lines[insert_at - 1].strip():
        insert_at -= 1
      break

  return insert_at


def update_toc(content: str, dry_run: bool = False) -> tuple[str, bool]:
  """Update or insert table of contents in a markdown document.

  Args:
      content: Full markdown content
      dry_run: If True, return what would be written without modifying

  Returns:
      Tuple of (updated_content, was_changed)
  """
  raw_content = content
  body, frontmatter_lines = strip_frontmatter(raw_content)
  headings = parse_headings(body, frontmatter_lines)

  # Generate new ToC content
  toc_content = generate_toc_content(headings)

  if not toc_content:
    # No headings to include in ToC
    return raw_content, False

  lines = raw_content.split("\n")

  # Build the full ToC section
  toc_section = f"{TOC_HEADING}\n\n{toc_content}"

  # Find existing ToC
  existing_toc = find_toc_section(lines, frontmatter_lines)

  if existing_toc:
    start, end = existing_toc

    # Extract current ToC to compare
    current_toc = "\n".join(lines[start:end]).strip()

    if current_toc == toc_section.strip():
      # No change needed
      return raw_content, False

    # Replace existing ToC
    new_lines = [*lines[:start], toc_section, "", *lines[end:]]
    return "\n".join(new_lines), True

  # Insert new ToC
  insert_at = find_insertion_point(lines, headings, frontmatter_lines)

  # Add blank line before and after ToC
  new_lines = [*lines[:insert_at], "", toc_section, "", *lines[insert_at:]]

  # Clean up excessive blank lines
  result = "\n".join(new_lines)
  result = re.sub(r"\n{4,}", "\n\n\n", result)

  return result, True


def process_file(path: Path, dry_run: bool = False) -> bool:
  """Process a single markdown file.

  Returns:
      True if file was (or would be) modified
  """
  content = path.read_text(encoding="utf-8")
  updated, changed = update_toc(content, dry_run)

  if changed:
    if dry_run:
      print(f"Would update: {path}")
    else:
      path.write_text(updated, encoding="utf-8")
      print(f"Updated: {path}")
    return True
  print(f"No changes: {path}")
  return False


def process_directory(directory: Path, dry_run: bool = False) -> tuple[int, int]:
  """Process all markdown files in a directory recursively.

  Returns:
      Tuple of (files_processed, files_modified)
  """
  processed = 0
  modified = 0

  for path in sorted(directory.rglob("*.md")):
    processed += 1
    if process_file(path, dry_run):
      modified += 1

  return processed, modified


def main() -> None:
  parser = argparse.ArgumentParser(
    description="Generate or update table of contents in markdown documents",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
    # Update ToC in a single file
    python generate_toc.py mddocs/prd.md

    # Update ToC in all files in mddocs/
    python generate_toc.py mddocs/

    # Preview changes without writing
    python generate_toc.py mddocs/ --dry-run
        """,
  )
  parser.add_argument("path", help="Markdown file or directory path")
  parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Preview changes without modifying files",
  )

  args = parser.parse_args()
  path = Path(args.path)

  if not path.exists():
    print(f"Error: Path not found: {path}", file=sys.stderr)
    sys.exit(1)

  if path.is_file():
    if path.suffix.lower() != ".md":
      print(f"Warning: File does not have .md extension: {path}", file=sys.stderr)
    process_file(path, args.dry_run)
  else:
    processed, modified = process_directory(path, args.dry_run)
    print(f"\nProcessed {processed} files, {modified} modified")


if __name__ == "__main__":
  main()
