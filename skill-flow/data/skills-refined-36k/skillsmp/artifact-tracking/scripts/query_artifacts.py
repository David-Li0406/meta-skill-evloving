#!/usr/bin/env python3
"""
Query helper functions for artifact tracking.

This script provides efficient querying of artifact metadata without loading full bodies,
filtering by field values (status, agent, phase, tags), aggregation across multiple files,
and structured results.

Usage:
    python query_artifacts.py --directory .claude/progress --status in-progress
    python query_artifacts.py --directory .claude/progress --prd advanced-editing-v2
    python query_artifacts.py --directory .claude/progress --owner frontend-developer
    python query_artifacts.py --directory .claude/worknotes --type context --status blocked
    python query_artifacts.py --directory .claude/progress --aggregate --format json
"""

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


@dataclass
class ArtifactMetadata:
    """Lightweight artifact metadata for queries."""
    filepath: str
    type: str
    title: str
    status: str
    prd: Optional[str] = None
    phase: Optional[int] = None
    overall_progress: Optional[int] = None
    owners: Optional[List[str]] = None
    contributors: Optional[List[str]] = None
    started: Optional[str] = None
    completed: Optional[str] = None
    blockers_count: int = 0
    total_tasks: Optional[int] = None
    completed_tasks: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


def extract_frontmatter_only(filepath: Path) -> Optional[Dict[str, Any]]:
    """
    Extract only YAML frontmatter without reading full body (efficient).

    Args:
        filepath: Path to artifact file

    Returns:
        Parsed frontmatter dictionary or None if not found
    """
    import re

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # Read only first few KB to get frontmatter
            content = f.read(8192)  # 8KB should be enough for frontmatter

            # Check if content starts with frontmatter delimiter
            if not content.strip().startswith('---'):
                return None

            # Find the closing delimiter
            match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if not match:
                return None

            frontmatter_str = match.group(1)
            return yaml.safe_load(frontmatter_str)

    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)
        return None


def load_artifact_metadata(filepath: Path) -> Optional[ArtifactMetadata]:
    """
    Load lightweight metadata from artifact file.

    Args:
        filepath: Path to artifact file

    Returns:
        ArtifactMetadata object or None if loading failed
    """
    frontmatter = extract_frontmatter_only(filepath)
    if frontmatter is None:
        return None

    try:
        metadata = ArtifactMetadata(
            filepath=str(filepath),
            type=frontmatter.get('type', 'unknown'),
            title=frontmatter.get('title', filepath.name),
            status=frontmatter.get('status', 'unknown'),
            prd=frontmatter.get('prd'),
            phase=frontmatter.get('phase'),
            overall_progress=frontmatter.get('overall_progress'),
            owners=frontmatter.get('owners', []),
            contributors=frontmatter.get('contributors', []),
            started=frontmatter.get('started'),
            completed=frontmatter.get('completed'),
            blockers_count=len(frontmatter.get('blockers', [])),
            total_tasks=frontmatter.get('total_tasks'),
            completed_tasks=frontmatter.get('completed_tasks'),
        )
        return metadata

    except Exception as e:
        print(f"Warning: Could not parse metadata from {filepath}: {e}", file=sys.stderr)
        return None


def find_artifacts(directory: Path, pattern: str = "*.md") -> List[Path]:
    """
    Find all artifact files in directory.

    Args:
        directory: Directory to search
        pattern: Glob pattern for files (default: *.md)

    Returns:
        List of file paths
    """
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    # Recursively find all markdown files
    return sorted(directory.rglob(pattern))


def filter_artifacts(
    artifacts: List[ArtifactMetadata],
    artifact_type: Optional[str] = None,
    status: Optional[str] = None,
    prd: Optional[str] = None,
    phase: Optional[int] = None,
    owner: Optional[str] = None,
    contributor: Optional[str] = None,
    has_blockers: Optional[bool] = None,
) -> List[ArtifactMetadata]:
    """
    Filter artifacts by criteria.

    Args:
        artifacts: List of artifact metadata
        artifact_type: Filter by type (progress, context, etc.)
        status: Filter by status
        prd: Filter by PRD identifier
        phase: Filter by phase number
        owner: Filter by owner
        contributor: Filter by contributor
        has_blockers: Filter by blocker presence

    Returns:
        Filtered list of artifacts
    """
    filtered = artifacts

    if artifact_type:
        filtered = [a for a in filtered if a.type == artifact_type]

    if status:
        filtered = [a for a in filtered if a.status == status]

    if prd:
        filtered = [a for a in filtered if a.prd == prd]

    if phase is not None:
        filtered = [a for a in filtered if a.phase == phase]

    if owner:
        filtered = [a for a in filtered if a.owners and owner in a.owners]

    if contributor:
        filtered = [a for a in filtered if a.contributors and contributor in a.contributors]

    if has_blockers is not None:
        if has_blockers:
            filtered = [a for a in filtered if a.blockers_count > 0]
        else:
            filtered = [a for a in filtered if a.blockers_count == 0]

    return filtered


def aggregate_metrics(artifacts: List[ArtifactMetadata]) -> Dict[str, Any]:
    """
    Aggregate metrics across artifacts.

    Args:
        artifacts: List of artifact metadata

    Returns:
        Dictionary of aggregated metrics
    """
    if not artifacts:
        return {
            "total_artifacts": 0,
            "by_type": {},
            "by_status": {},
            "by_prd": {},
            "total_blockers": 0,
            "average_progress": 0,
        }

    # Count by type
    by_type: Dict[str, int] = {}
    for artifact in artifacts:
        by_type[artifact.type] = by_type.get(artifact.type, 0) + 1

    # Count by status
    by_status: Dict[str, int] = {}
    for artifact in artifacts:
        by_status[artifact.status] = by_status.get(artifact.status, 0) + 1

    # Count by PRD
    by_prd: Dict[str, int] = {}
    for artifact in artifacts:
        if artifact.prd:
            by_prd[artifact.prd] = by_prd.get(artifact.prd, 0) + 1

    # Total blockers
    total_blockers = sum(a.blockers_count for a in artifacts)

    # Average progress (only for artifacts with progress)
    progress_values = [a.overall_progress for a in artifacts if a.overall_progress is not None]
    average_progress = sum(progress_values) / len(progress_values) if progress_values else 0

    # Task metrics (only for progress artifacts)
    progress_artifacts = [a for a in artifacts if a.type == 'progress' and a.total_tasks is not None]
    total_tasks_sum = sum(a.total_tasks or 0 for a in progress_artifacts)
    completed_tasks_sum = sum(a.completed_tasks or 0 for a in progress_artifacts)

    return {
        "total_artifacts": len(artifacts),
        "by_type": by_type,
        "by_status": by_status,
        "by_prd": by_prd,
        "total_blockers": total_blockers,
        "average_progress": round(average_progress, 1),
        "total_tasks": total_tasks_sum,
        "completed_tasks": completed_tasks_sum,
        "task_completion_rate": round((completed_tasks_sum / total_tasks_sum * 100), 1) if total_tasks_sum > 0 else 0,
    }


def format_table_output(artifacts: List[ArtifactMetadata]) -> str:
    """
    Format artifacts as ASCII table.

    Args:
        artifacts: List of artifact metadata

    Returns:
        Formatted table string
    """
    if not artifacts:
        return "No artifacts found."

    lines = []

    # Header
    lines.append("=" * 100)
    lines.append(f"Found {len(artifacts)} artifact(s)")
    lines.append("=" * 100)

    # Table header
    lines.append(f"{'Type':<12} {'Status':<15} {'PRD':<20} {'Phase':<6} {'Progress':<10} {'Title':<30}")
    lines.append("-" * 100)

    # Table rows
    for artifact in artifacts:
        type_str = artifact.type[:11]
        status_str = artifact.status[:14]
        prd_str = (artifact.prd or 'N/A')[:19]
        phase_str = str(artifact.phase) if artifact.phase else 'N/A'
        progress_str = f"{artifact.overall_progress}%" if artifact.overall_progress is not None else 'N/A'
        title_str = artifact.title[:29]

        lines.append(f"{type_str:<12} {status_str:<15} {prd_str:<20} {phase_str:<6} {progress_str:<10} {title_str:<30}")

    lines.append("=" * 100)

    return "\n".join(lines)


def format_json_output(artifacts: List[ArtifactMetadata]) -> str:
    """
    Format artifacts as JSON.

    Args:
        artifacts: List of artifact metadata

    Returns:
        JSON string
    """
    data = [artifact.to_dict() for artifact in artifacts]
    return json.dumps(data, indent=2, default=str)


def format_summary_output(artifacts: List[ArtifactMetadata]) -> str:
    """
    Format artifacts as summary with aggregated metrics.

    Args:
        artifacts: List of artifact metadata

    Returns:
        Formatted summary string
    """
    metrics = aggregate_metrics(artifacts)

    lines = []
    lines.append("=" * 70)
    lines.append("Artifact Query Summary")
    lines.append("=" * 70)
    lines.append(f"Total Artifacts: {metrics['total_artifacts']}")
    lines.append("")

    lines.append("By Type:")
    for artifact_type, count in sorted(metrics['by_type'].items()):
        lines.append(f"  {artifact_type}: {count}")
    lines.append("")

    lines.append("By Status:")
    for status, count in sorted(metrics['by_status'].items()):
        lines.append(f"  {status}: {count}")
    lines.append("")

    if metrics['by_prd']:
        lines.append("By PRD:")
        for prd, count in sorted(metrics['by_prd'].items()):
            lines.append(f"  {prd}: {count}")
        lines.append("")

    lines.append(f"Total Blockers: {metrics['total_blockers']}")
    lines.append(f"Average Progress: {metrics['average_progress']}%")
    lines.append(f"Total Tasks: {metrics['total_tasks']}")
    lines.append(f"Completed Tasks: {metrics['completed_tasks']}")
    lines.append(f"Task Completion Rate: {metrics['task_completion_rate']}%")
    lines.append("=" * 70)

    return "\n".join(lines)


def query_artifacts(
    directory: Path,
    artifact_type: Optional[str] = None,
    status: Optional[str] = None,
    prd: Optional[str] = None,
    phase: Optional[int] = None,
    owner: Optional[str] = None,
    contributor: Optional[str] = None,
    has_blockers: Optional[bool] = None,
    output_format: str = 'table',
    aggregate: bool = False,
) -> str:
    """
    Query artifacts and return formatted results.

    Args:
        directory: Directory to search
        artifact_type: Filter by type
        status: Filter by status
        prd: Filter by PRD
        phase: Filter by phase
        owner: Filter by owner
        contributor: Filter by contributor
        has_blockers: Filter by blocker presence
        output_format: Output format (table, json, summary)
        aggregate: Show aggregated metrics

    Returns:
        Formatted query results
    """
    # Find all artifact files
    filepaths = find_artifacts(directory)

    # Load metadata (efficiently - only frontmatter)
    artifacts = []
    for filepath in filepaths:
        metadata = load_artifact_metadata(filepath)
        if metadata:
            artifacts.append(metadata)

    # Filter artifacts
    filtered = filter_artifacts(
        artifacts,
        artifact_type=artifact_type,
        status=status,
        prd=prd,
        phase=phase,
        owner=owner,
        contributor=contributor,
        has_blockers=has_blockers,
    )

    # Format output
    if aggregate or output_format == 'summary':
        return format_summary_output(filtered)
    elif output_format == 'json':
        return format_json_output(filtered)
    else:  # table
        return format_table_output(filtered)


def main():
    """Main entry point for query_artifacts script."""
    parser = argparse.ArgumentParser(
        description="Query artifact tracking files efficiently",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Find all in-progress artifacts
  python query_artifacts.py --directory .claude/progress --status in-progress

  # Find artifacts for specific PRD
  python query_artifacts.py --directory .claude/progress --prd advanced-editing-v2

  # Find artifacts owned by specific agent
  python query_artifacts.py --directory .claude/progress --owner frontend-developer

  # Find blocked context artifacts
  python query_artifacts.py --directory .claude/worknotes --type context --status blocked

  # Show aggregated metrics
  python query_artifacts.py --directory .claude/progress --aggregate

  # Output as JSON
  python query_artifacts.py --directory .claude/progress --format json
        """
    )

    parser.add_argument(
        '--directory',
        '-d',
        type=Path,
        required=True,
        help='Directory to search for artifacts'
    )

    parser.add_argument(
        '--type',
        '-t',
        choices=['progress', 'context', 'bug-fix', 'observation'],
        help='Filter by artifact type'
    )

    parser.add_argument(
        '--status',
        '-s',
        help='Filter by status (e.g., in-progress, complete, blocked)'
    )

    parser.add_argument(
        '--prd',
        '-p',
        help='Filter by PRD identifier'
    )

    parser.add_argument(
        '--phase',
        type=int,
        help='Filter by phase number'
    )

    parser.add_argument(
        '--owner',
        '-o',
        help='Filter by owner agent'
    )

    parser.add_argument(
        '--contributor',
        '-c',
        help='Filter by contributor agent'
    )

    parser.add_argument(
        '--has-blockers',
        action='store_true',
        help='Filter to only artifacts with blockers'
    )

    parser.add_argument(
        '--no-blockers',
        action='store_true',
        help='Filter to only artifacts without blockers'
    )

    parser.add_argument(
        '--format',
        '-f',
        choices=['table', 'json', 'summary'],
        default='table',
        help='Output format (default: table)'
    )

    parser.add_argument(
        '--aggregate',
        '-a',
        action='store_true',
        help='Show aggregated metrics across all artifacts'
    )

    args = parser.parse_args()

    # Determine has_blockers value
    has_blockers = None
    if args.has_blockers:
        has_blockers = True
    elif args.no_blockers:
        has_blockers = False

    try:
        # Query artifacts
        result = query_artifacts(
            args.directory,
            artifact_type=args.type,
            status=args.status,
            prd=args.prd,
            phase=args.phase,
            owner=args.owner,
            contributor=args.contributor,
            has_blockers=has_blockers,
            output_format=args.format,
            aggregate=args.aggregate,
        )

        print(result)
        sys.exit(0)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
