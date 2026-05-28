#!/usr/bin/env python3
"""
Convert markdown artifact to YAML+Markdown hybrid format.

This script parses existing markdown files, extracts metadata from headers and tables,
generates YAML frontmatter based on schemas, preserves markdown body, validates against
schema, and writes the hybrid format file.

Usage:
    python convert_to_hybrid.py input.md output.md [--artifact-type progress]
    python convert_to_hybrid.py input.md --in-place
    python convert_to_hybrid.py input.md --dry-run
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import yaml

from validate_artifact import validate_artifact_file


def extract_metadata_from_markdown(content: str, artifact_type: str) -> Dict[str, Any]:
    """
    Extract metadata from markdown content based on artifact type.

    Args:
        content: Markdown content to parse
        artifact_type: Type of artifact (progress, context, bug-fix, observation)

    Returns:
        Dictionary of extracted metadata
    """
    metadata: Dict[str, Any] = {"type": artifact_type}

    if artifact_type == "progress":
        metadata.update(_extract_progress_metadata(content))
    elif artifact_type == "context":
        metadata.update(_extract_context_metadata(content))
    elif artifact_type == "bug-fix":
        metadata.update(_extract_bug_fix_metadata(content))
    elif artifact_type == "observation":
        metadata.update(_extract_observation_metadata(content))
    else:
        raise ValueError(f"Unknown artifact type: {artifact_type}")

    return metadata


def _extract_progress_metadata(content: str) -> Dict[str, Any]:
    """Extract metadata specific to progress tracking artifacts."""
    metadata: Dict[str, Any] = {}

    # Extract title from first h1 header
    title_match = re.search(r'^#\s+(.+?)(?:\s*-\s*Phase\s*\d+)?$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
        # Remove PRD prefix if present
        title = re.sub(r'^[a-z0-9-]+\s*-\s*', '', title, flags=re.IGNORECASE)
        metadata["title"] = title

    # Extract PRD from filename or header
    prd_match = re.search(r'(?:PRD|prd):\s*([a-z0-9-]+)', content, re.IGNORECASE)
    if prd_match:
        metadata["prd"] = prd_match.group(1).lower()

    # Extract phase number
    phase_match = re.search(r'(?:Phase|phase):\s*(\d+)', content, re.IGNORECASE)
    if phase_match:
        metadata["phase"] = int(phase_match.group(1))

    # Extract status
    status_match = re.search(r'(?:Status|status):\s*(?:\S+\s+)?(\w+(?:-\w+)?)', content, re.IGNORECASE)
    if status_match:
        status = status_match.group(1).lower()
        # Map common status values
        status_map = {
            "planning": "planning",
            "in-progress": "in-progress",
            "in_progress": "in-progress",
            "review": "review",
            "complete": "complete",
            "completed": "complete",
            "blocked": "blocked",
        }
        metadata["status"] = status_map.get(status, "in-progress")

    # Extract dates
    started_match = re.search(r'(?:Started|started):\s*(\d{4}-\d{2}-\d{2})', content)
    if started_match:
        metadata["started"] = started_match.group(1)
    else:
        # Use today's date as fallback
        metadata["started"] = datetime.now().strftime("%Y-%m-%d")

    completed_match = re.search(r'(?:Completed|completed):\s*(\d{4}-\d{2}-\d{2})', content)
    if completed_match:
        metadata["completed"] = completed_match.group(1)
    else:
        metadata["completed"] = None

    # Extract progress percentage
    progress_match = re.search(r'(\d+)%\s*(?:complete|progress)', content, re.IGNORECASE)
    if progress_match:
        metadata["overall_progress"] = int(progress_match.group(1))
    else:
        metadata["overall_progress"] = 0

    # Extract task counts from tables
    task_counts = _extract_task_counts_from_table(content)
    metadata.update(task_counts)

    # Extract owners and contributors
    owner_match = re.search(r'(?:Owner|owner)s?:\s*([^\n]+)', content)
    if owner_match:
        owners = [o.strip() for o in owner_match.group(1).split(',')]
        metadata["owners"] = [o.lower().replace(' ', '-') for o in owners if o]

    contributor_match = re.search(r'(?:Contributor|contributor)s?:\s*([^\n]+)', content)
    if contributor_match:
        contributors = [c.strip() for c in contributor_match.group(1).split(',')]
        metadata["contributors"] = [c.lower().replace(' ', '-') for c in contributors if c]

    # Set defaults if not found
    metadata.setdefault("title", "Untitled Phase")
    metadata.setdefault("prd", "unknown-prd")
    metadata.setdefault("phase", 1)
    metadata.setdefault("status", "in-progress")
    metadata.setdefault("overall_progress", 0)
    metadata.setdefault("completion_estimate", "on-track")
    metadata.setdefault("owners", [])
    metadata.setdefault("contributors", [])
    metadata.setdefault("blockers", [])
    metadata.setdefault("success_criteria", [])

    return metadata


def _extract_context_metadata(content: str) -> Dict[str, Any]:
    """Extract metadata specific to context notes artifacts."""
    metadata: Dict[str, Any] = {}

    # Extract title
    title_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
    if title_match:
        metadata["title"] = title_match.group(1).strip()

    # Extract PRD
    prd_match = re.search(r'(?:PRD|prd):\s*([a-z0-9-]+)', content, re.IGNORECASE)
    if prd_match:
        metadata["prd"] = prd_match.group(1).lower()

    # Extract phase (optional for context)
    phase_match = re.search(r'(?:Phase|phase):\s*(\d+)', content, re.IGNORECASE)
    if phase_match:
        metadata["phase"] = int(phase_match.group(1))
    else:
        metadata["phase"] = None

    # Extract status
    status_match = re.search(r'(?:Status|status):\s*(\w+(?:-\w+)?)', content, re.IGNORECASE)
    if status_match:
        status = status_match.group(1).lower()
        status_map = {
            "complete": "complete",
            "completed": "complete",
            "in-progress": "in-progress",
            "in_progress": "in-progress",
            "blocked": "blocked",
        }
        metadata["status"] = status_map.get(status, "in-progress")

    # Set defaults
    metadata.setdefault("title", "Untitled Context")
    metadata.setdefault("prd", "unknown-prd")
    metadata.setdefault("status", "in-progress")
    metadata.setdefault("phase_status", [])
    metadata.setdefault("blockers", [])
    metadata.setdefault("decisions", [])
    metadata.setdefault("integrations", [])
    metadata.setdefault("gotchas", [])
    metadata.setdefault("modified_files", [])
    metadata["updated"] = datetime.now().isoformat()

    return metadata


def _extract_bug_fix_metadata(content: str) -> Dict[str, Any]:
    """Extract metadata specific to bug fix tracking artifacts."""
    metadata: Dict[str, Any] = {}

    # Extract month from filename or content
    month_match = re.search(r'(\d{2})-(\d{2})', content)
    if month_match:
        metadata["month"] = f"{month_match.group(1)}-{month_match.group(2)}"
    else:
        now = datetime.now()
        metadata["month"] = now.strftime("%m-%y")

    # Extract fixes from content
    # This is a simplified extraction - actual implementation would parse fix entries
    metadata["total_fixes"] = 0
    metadata["fixes"] = []

    return metadata


def _extract_observation_metadata(content: str) -> Dict[str, Any]:
    """Extract metadata specific to observation log artifacts."""
    metadata: Dict[str, Any] = {}

    # Extract month from filename or content
    month_match = re.search(r'(\d{2})-(\d{2})', content)
    if month_match:
        metadata["month"] = f"{month_match.group(1)}-{month_match.group(2)}"
    else:
        now = datetime.now()
        metadata["month"] = now.strftime("%m-%y")

    # Extract observations from content
    metadata["total_observations"] = 0
    metadata["observations"] = []

    return metadata


def _extract_task_counts_from_table(content: str) -> Dict[str, int]:
    """Extract task counts from markdown task tables."""
    counts = {
        "total_tasks": 0,
        "completed_tasks": 0,
        "in_progress_tasks": 0,
        "blocked_tasks": 0,
    }

    # Look for task table
    task_table_match = re.search(r'\|\s*ID\s*\|.*?Status.*?\|.*?\n\|[-\s|]+\n((?:\|.*?\n)+)', content, re.MULTILINE)
    if task_table_match:
        task_rows = task_table_match.group(1).strip().split('\n')

        for row in task_rows:
            if not row.strip().startswith('|'):
                continue

            counts["total_tasks"] += 1

            # Check status symbols
            if '✓' in row or 'Complete' in row or 'Done' in row:
                counts["completed_tasks"] += 1
            elif '🔄' in row or 'In Progress' in row or 'In-Progress' in row:
                counts["in_progress_tasks"] += 1
            elif '🚫' in row or 'Blocked' in row:
                counts["blocked_tasks"] += 1

    return counts


def split_frontmatter_and_body(content: str) -> Tuple[Optional[str], str]:
    """
    Split content into YAML frontmatter and markdown body.

    Args:
        content: Full content with or without frontmatter

    Returns:
        Tuple of (frontmatter_string, body_content)
    """
    # Check if content starts with frontmatter delimiter
    if content.strip().startswith('---'):
        # Find the closing delimiter
        match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
        if match:
            return match.group(1), match.group(2)

    # No frontmatter found
    return None, content


def generate_hybrid_format(metadata: Dict[str, Any], body: str) -> str:
    """
    Generate hybrid YAML+Markdown format.

    Args:
        metadata: Metadata dictionary
        body: Markdown body content

    Returns:
        Complete hybrid format string
    """
    # Generate YAML frontmatter
    yaml_content = yaml.dump(
        metadata,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        width=80,
    )

    # Combine frontmatter and body
    hybrid_content = f"---\n{yaml_content}---\n\n{body.strip()}\n"

    return hybrid_content


def detect_artifact_type(filepath: Path, content: str) -> str:
    """
    Auto-detect artifact type from filepath and content.

    Args:
        filepath: Path to the file
        content: File content

    Returns:
        Artifact type string
    """
    filename = filepath.name.lower()

    # Check filename patterns
    if 'progress' in filename:
        return 'progress'
    elif 'context' in filename:
        return 'context'
    elif 'bug-fix' in filename or 'bug_fix' in filename:
        return 'bug-fix'
    elif 'observation' in filename:
        return 'observation'

    # Check content patterns
    if re.search(r'(?:Phase|phase):\s*\d+', content):
        return 'progress'
    elif re.search(r'(?:Decision|DECISION)-\d+', content):
        return 'context'
    elif re.search(r'(?:Fix|fix)(?:es)?:', content):
        return 'bug-fix'
    elif re.search(r'(?:Observation|observation)s?:', content):
        return 'observation'

    # Default to progress
    return 'progress'


def convert_file(
    input_path: Path,
    output_path: Optional[Path] = None,
    artifact_type: Optional[str] = None,
    dry_run: bool = False,
) -> bool:
    """
    Convert a markdown file to hybrid YAML+Markdown format.

    Args:
        input_path: Path to input markdown file
        output_path: Path to output file (None for in-place)
        artifact_type: Type of artifact (auto-detect if None)
        dry_run: If True, don't write output, just validate

    Returns:
        True if conversion succeeded, False otherwise
    """
    try:
        # Read input file
        if not input_path.exists():
            print(f"Error: Input file not found: {input_path}", file=sys.stderr)
            return False

        content = input_path.read_text(encoding='utf-8')

        # Auto-detect artifact type if not provided
        if artifact_type is None:
            artifact_type = detect_artifact_type(input_path, content)
            print(f"Auto-detected artifact type: {artifact_type}")

        # Split existing frontmatter and body
        existing_frontmatter, body = split_frontmatter_and_body(content)

        # Extract metadata from body
        metadata = extract_metadata_from_markdown(body, artifact_type)

        # Merge with existing frontmatter if present
        if existing_frontmatter:
            try:
                existing_meta = yaml.safe_load(existing_frontmatter)
                if existing_meta and isinstance(existing_meta, dict):
                    # Existing frontmatter takes precedence
                    metadata = {**metadata, **existing_meta}
            except yaml.YAMLError as e:
                print(f"Warning: Could not parse existing frontmatter: {e}", file=sys.stderr)

        # Generate hybrid format
        hybrid_content = generate_hybrid_format(metadata, body)

        # Determine output path
        if output_path is None:
            output_path = input_path

        if dry_run:
            print(f"\n--- DRY RUN: Would write to {output_path} ---")
            print(hybrid_content[:500] + "..." if len(hybrid_content) > 500 else hybrid_content)
            print(f"--- END DRY RUN ---\n")

            # Validate without writing
            from io import StringIO
            temp_file = StringIO(hybrid_content)
            is_valid = validate_artifact_file(temp_file, artifact_type, verbose=True)
            return is_valid

        # Write output file
        output_path.write_text(hybrid_content, encoding='utf-8')
        print(f"Successfully converted: {input_path} -> {output_path}")

        # Validate the output
        is_valid = validate_artifact_file(output_path, artifact_type, verbose=True)

        if not is_valid:
            print(f"Warning: Output file did not pass validation", file=sys.stderr)
            return False

        return True

    except Exception as e:
        print(f"Error converting {input_path}: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point for convert_to_hybrid script."""
    parser = argparse.ArgumentParser(
        description="Convert markdown artifact to YAML+Markdown hybrid format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert with auto-detected type
  python convert_to_hybrid.py input.md output.md

  # Convert with explicit type
  python convert_to_hybrid.py input.md output.md --artifact-type progress

  # Convert in-place
  python convert_to_hybrid.py input.md --in-place

  # Dry run to preview changes
  python convert_to_hybrid.py input.md --dry-run
        """
    )

    parser.add_argument(
        'input',
        type=Path,
        help='Input markdown file path'
    )

    parser.add_argument(
        'output',
        type=Path,
        nargs='?',
        help='Output file path (optional if using --in-place)'
    )

    parser.add_argument(
        '--artifact-type',
        '-t',
        choices=['progress', 'context', 'bug-fix', 'observation'],
        help='Type of artifact (auto-detected if not specified)'
    )

    parser.add_argument(
        '--in-place',
        '-i',
        action='store_true',
        help='Modify input file in-place'
    )

    parser.add_argument(
        '--dry-run',
        '-n',
        action='store_true',
        help='Preview changes without writing'
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.in_place and not args.output and not args.dry_run:
        parser.error("Either provide an output file, use --in-place, or use --dry-run")

    output_path = None if args.in_place else args.output

    # Convert file
    success = convert_file(
        args.input,
        output_path,
        args.artifact_type,
        args.dry_run
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
