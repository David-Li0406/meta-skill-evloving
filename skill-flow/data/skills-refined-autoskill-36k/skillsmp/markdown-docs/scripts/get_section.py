#!/usr/bin/env python3
"""Extract a section from a markdown document by heading anchor.

Usage:
    python get_section.py <file> <anchor>
    python get_section.py mddocs/prd.md user-authentication
    python get_section.py mddocs/prd.md user-authentication/requirements

Options:
    --shallow    Only get immediate content, exclude subsections
    --list       List all available sections in the document

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


@dataclass
class Heading:
  """Represents a heading in a markdown document."""

  level: int
  text: str
  slug: str
  line_start: int
  line_end: int | None = None  # Set after parsing all headings

  @property
  def line_count(self) -> int:
    if self.line_end is None:
      return 0
    return self.line_end - self.line_start


def strip_frontmatter(content: str) -> tuple[str, int]:
  """Strip YAML frontmatter from markdown content.

  Returns:
      Tuple of (content without frontmatter, number of lines stripped)
  """
  lines = content.split("\n")

  if not lines or lines[0].strip() != "---":
    return content, 0

  # Find closing ---
  for i, line in enumerate(lines[1:], start=1):
    if line.strip() == "---":
      # Return content after frontmatter
      remaining_lines = lines[i + 1 :]
      return "\n".join(remaining_lines), i + 1

  # No closing ---, return original
  return content, 0


def slugify(text: str) -> str:
  """Convert heading text to anchor slug (GitHub-Flavored Markdown style).

  Rules:
  1. Convert to lowercase
  2. Replace spaces with hyphens
  3. Remove punctuation (except hyphens)
  4. Collapse consecutive hyphens
  5. Strip leading/trailing hyphens
  """
  slug = text.lower()
  slug = re.sub(r"\s+", "-", slug)
  slug = re.sub(r"[^a-z0-9\-]", "", slug)
  slug = re.sub(r"-+", "-", slug)
  return slug.strip("-")


def parse_headings(content: str, frontmatter_lines: int = 0) -> list[Heading]:
  """Parse all headings from markdown content using markdown-it-py.

  This properly handles code blocks, so headings inside fenced code
  are not extracted.

  Args:
      content: Markdown content (with frontmatter already stripped)
      frontmatter_lines: Number of lines of frontmatter that were stripped
                        (used to adjust line numbers to match original file)
  """
  md = MarkdownIt()
  tokens = md.parse(content)
  lines = content.split("\n")

  headings: list[Heading] = []

  i = 0
  while i < len(tokens):
    token = tokens[i]

    if token.type == "heading_open":
      level = int(token.tag[1])  # h1 -> 1, h2 -> 2, etc.
      # Adjust line number to account for stripped frontmatter
      line_start = (token.map[0] if token.map else 0) + frontmatter_lines

      # Next token should be inline with the heading text
      if i + 1 < len(tokens) and tokens[i + 1].type == "inline":
        text = tokens[i + 1].content
      else:
        text = ""

      headings.append(
        Heading(
          level=level,
          text=text,
          slug=slugify(text),
          line_start=line_start,
        )
      )

    i += 1

  # Calculate line_end for each heading
  # Total lines = content lines + frontmatter lines
  total_lines = len(lines) + frontmatter_lines
  for i, heading in enumerate(headings):
    if i + 1 < len(headings):
      heading.line_end = headings[i + 1].line_start
    else:
      heading.line_end = total_lines

  return headings


def find_heading_by_path(headings: list[Heading], path: str) -> Heading | None:
  """Find a heading by anchor path.

  Supports both simple anchors (#user-auth) and hierarchical paths
  (#user-auth/requirements).

  For hierarchical paths, each segment must be a child (deeper level)
  of the previous segment.
  """
  path = path.lstrip("#")
  parts = path.split("/")

  if not parts:
    return None

  # For simple (non-hierarchical) anchors, just find the first match
  if len(parts) == 1:
    for h in headings:
      if h.slug == parts[0]:
        return h
    return None

  # For hierarchical paths, walk down the tree
  current_idx = 0
  current_level = 0
  result = None

  for part in parts:
    found = False

    for i in range(current_idx, len(headings)):
      h = headings[i]

      # Must be deeper than current level
      if h.level <= current_level:
        # We've exited the parent's scope without finding the child
        if result is not None:
          break
        continue

      if h.slug == part:
        result = h
        current_level = h.level
        current_idx = i + 1
        found = True
        break

    if not found:
      return None

  return result


def get_section_end_line(
  heading: Heading, headings: list[Heading], shallow: bool = False
) -> int:
  """Determine where a section ends.

  Args:
      heading: The heading whose section we're extracting
      headings: All headings in the document
      shallow: If True, stop at any next heading. If False, stop at
               same-or-higher level heading (include subsections).
  """
  heading_idx = headings.index(heading)

  for h in headings[heading_idx + 1 :]:
    if shallow:
      # Stop at any heading
      return h.line_start
    # Stop at same or higher level (lower number = higher level)
    if h.level <= heading.level:
      return h.line_start

  # No stopping point found, go to end of document
  return heading.line_end if heading.line_end else 0


def extract_section(
  content: str, heading: Heading, headings: list[Heading], shallow: bool = False
) -> str:
  """Extract the content for a section."""
  lines = content.split("\n")
  start = heading.line_start
  end = get_section_end_line(heading, headings, shallow)

  section_lines = lines[start:end]

  # Trim trailing blank lines
  while section_lines and not section_lines[-1].strip():
    section_lines.pop()

  return "\n".join(section_lines)


def build_heading_path(heading: Heading, headings: list[Heading]) -> str:
  """Build the full hierarchical path for a heading."""
  path_parts: list[str] = []
  heading_idx = headings.index(heading)

  # Walk backwards collecting ancestors
  current_level = heading.level
  for h in reversed(headings[: heading_idx + 1]):
    if h.level < current_level:
      path_parts.insert(0, h.slug)
      current_level = h.level
    elif h == heading:
      path_parts.append(h.slug)

  return "/".join(path_parts)


def list_sections(headings: list[Heading]) -> str:
  """Generate a tree view of available sections."""
  lines: list[str] = []

  # Track slug occurrences to identify ambiguous anchors
  slug_counts: dict[str, int] = {}
  for h in headings:
    slug_counts[h.slug] = slug_counts.get(h.slug, 0) + 1

  for h in headings:
    indent = "  " * (h.level - 1)
    anchor = f"#{h.slug}"

    # If slug is ambiguous, show the full path
    if slug_counts[h.slug] > 1:
      full_path = build_heading_path(h, headings)
      anchor = f"#{full_path}"

    lines.append(f"{indent}- {h.text} ({anchor})")

  return "\n".join(lines)


def main() -> None:
  parser = argparse.ArgumentParser(
    description="Extract sections from markdown documents",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
    # List all sections
    python get_section.py mddocs/prd.md --list

    # Get a section by simple anchor
    python get_section.py mddocs/prd.md user-authentication

    # Get a nested section by path
    python get_section.py mddocs/prd.md user-authentication/requirements

    # Get shallow content (no subsections)
    python get_section.py mddocs/prd.md overview --shallow
        """,
  )
  parser.add_argument("file", help="Markdown file path")
  parser.add_argument("anchor", nargs="?", help="Section anchor or path (without #)")
  parser.add_argument(
    "--shallow",
    action="store_true",
    help="Only get immediate content, exclude subsections",
  )
  parser.add_argument("--list", action="store_true", help="List all available sections")

  args = parser.parse_args()

  path = Path(args.file)
  if not path.exists():
    print(f"Error: File not found: {path}", file=sys.stderr)
    sys.exit(1)

  if path.suffix.lower() != ".md":
    print(f"Warning: File does not have .md extension: {path}", file=sys.stderr)

  raw_content = path.read_text(encoding="utf-8")
  content, frontmatter_lines = strip_frontmatter(raw_content)
  headings = parse_headings(content, frontmatter_lines)

  if not headings:
    print("No headings found in document", file=sys.stderr)
    sys.exit(1)

  if args.list:
    print(list_sections(headings))
    sys.exit(0)

  if not args.anchor:
    print("Error: Must provide an anchor or use --list", file=sys.stderr)
    parser.print_usage(sys.stderr)
    sys.exit(1)

  heading = find_heading_by_path(headings, args.anchor)

  if not heading:
    print(f"Error: Section '{args.anchor}' not found", file=sys.stderr)
    print("\nAvailable sections:", file=sys.stderr)
    print(list_sections(headings), file=sys.stderr)
    sys.exit(1)

  # Use raw_content for extraction since line numbers are relative to full file
  section = extract_section(raw_content, heading, headings, args.shallow)
  print(section)


if __name__ == "__main__":
  main()
