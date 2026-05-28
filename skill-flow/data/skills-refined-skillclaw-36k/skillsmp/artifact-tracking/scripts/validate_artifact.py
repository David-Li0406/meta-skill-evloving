#!/usr/bin/env python3
"""
Validate artifact against JSON Schema.

This script loads schemas, parses YAML frontmatter, validates against the schema using
jsonschema library, reports errors with helpful messages, and returns pass/fail status.

Usage:
    python validate_artifact.py artifact.md
    python validate_artifact.py artifact.md --artifact-type progress
    python validate_artifact.py artifact.md --verbose
    python validate_artifact.py artifact.md --schema-dir ../schemas
"""

import argparse
import sys
from io import StringIO
from pathlib import Path
from typing import Any, Dict, Optional, Union

import jsonschema
import yaml


def load_schema(artifact_type: str, schema_dir: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load JSON Schema for artifact type.

    Args:
        artifact_type: Type of artifact (progress, context, bug-fix, observation)
        schema_dir: Directory containing schema files (default: ../schemas)

    Returns:
        Schema dictionary

    Raises:
        FileNotFoundError: If schema file doesn't exist
        yaml.YAMLError: If schema file is invalid
    """
    if schema_dir is None:
        # Default to ../schemas relative to this script
        script_dir = Path(__file__).parent
        schema_dir = script_dir.parent / 'schemas'

    schema_filename = f"{artifact_type}.schema.yaml"
    schema_path = schema_dir / schema_filename

    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")

    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = yaml.safe_load(f)

    return schema


def extract_frontmatter(file_content: str) -> Optional[str]:
    """
    Extract YAML frontmatter from file content.

    Args:
        file_content: Full file content

    Returns:
        YAML frontmatter string (without delimiters) or None if not found
    """
    import re

    # Check if content starts with frontmatter delimiter
    if not file_content.strip().startswith('---'):
        return None

    # Find the closing delimiter
    match = re.match(r'^---\n(.*?)\n---', file_content, re.DOTALL)
    if match:
        return match.group(1)

    return None


def parse_frontmatter(frontmatter_str: str) -> Dict[str, Any]:
    """
    Parse YAML frontmatter string.

    Args:
        frontmatter_str: YAML string to parse

    Returns:
        Parsed metadata dictionary

    Raises:
        yaml.YAMLError: If YAML is invalid
    """
    return yaml.safe_load(frontmatter_str)


def validate_metadata(metadata: Dict[str, Any], schema: Dict[str, Any]) -> tuple[bool, list[str]]:
    """
    Validate metadata against schema.

    Args:
        metadata: Metadata to validate
        schema: JSON Schema

    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []

    try:
        # Create validator
        validator = jsonschema.Draft7Validator(schema)

        # Validate and collect errors
        validation_errors = list(validator.iter_errors(metadata))

        if not validation_errors:
            return True, []

        # Format error messages
        for error in validation_errors:
            path = ".".join(str(p) for p in error.path) if error.path else "root"
            errors.append(f"  [{path}] {error.message}")

        return False, errors

    except Exception as e:
        errors.append(f"Validation error: {e}")
        return False, errors


def format_validation_report(
    filepath: Union[Path, str],
    artifact_type: str,
    is_valid: bool,
    errors: list[str],
    metadata: Optional[Dict[str, Any]] = None,
    verbose: bool = False
) -> str:
    """
    Format a human-readable validation report.

    Args:
        filepath: Path to the artifact file
        artifact_type: Type of artifact
        is_valid: Whether validation passed
        errors: List of error messages
        metadata: Metadata dictionary (optional, for verbose output)
        verbose: Include detailed metadata in report

    Returns:
        Formatted report string
    """
    lines = []

    # Header
    lines.append("=" * 70)
    lines.append(f"Artifact Validation Report")
    lines.append("=" * 70)
    lines.append(f"File: {filepath}")
    lines.append(f"Type: {artifact_type}")
    lines.append(f"Status: {'✓ VALID' if is_valid else '✗ INVALID'}")
    lines.append("=" * 70)

    if is_valid:
        lines.append("\n✓ All validations passed!")

        if verbose and metadata:
            lines.append("\nMetadata Summary:")
            lines.append(f"  Title: {metadata.get('title', 'N/A')}")
            lines.append(f"  PRD: {metadata.get('prd', 'N/A')}")

            if 'phase' in metadata:
                lines.append(f"  Phase: {metadata.get('phase', 'N/A')}")

            lines.append(f"  Status: {metadata.get('status', 'N/A')}")

            if artifact_type == 'progress':
                lines.append(f"  Progress: {metadata.get('overall_progress', 0)}%")
                lines.append(f"  Tasks: {metadata.get('total_tasks', 0)} total, "
                           f"{metadata.get('completed_tasks', 0)} completed")

    else:
        lines.append(f"\n✗ Validation failed with {len(errors)} error(s):")
        lines.append("")
        for error in errors:
            lines.append(error)

        lines.append("\nSuggestions:")
        if any("required" in err.lower() for err in errors):
            lines.append("  • Check that all required fields are present")
        if any("type" in err.lower() for err in errors):
            lines.append("  • Verify that field types match the schema")
        if any("pattern" in err.lower() for err in errors):
            lines.append("  • Check field formats (e.g., dates, IDs, kebab-case)")
        if any("enum" in err.lower() for err in errors):
            lines.append("  • Ensure enum values match allowed options")

        lines.append("\nTo fix errors:")
        lines.append("  1. Review the schema file for field requirements")
        lines.append("  2. Update the YAML frontmatter to match the schema")
        lines.append("  3. Re-run validation to verify fixes")

    lines.append("")
    lines.append("=" * 70)

    return "\n".join(lines)


def validate_artifact_file(
    filepath: Union[Path, str, StringIO],
    artifact_type: Optional[str] = None,
    schema_dir: Optional[Path] = None,
    verbose: bool = False
) -> bool:
    """
    Validate an artifact file against its schema.

    Args:
        filepath: Path to artifact file or StringIO object
        artifact_type: Type of artifact (auto-detected if None)
        schema_dir: Directory containing schema files
        verbose: Print detailed validation report

    Returns:
        True if validation passed, False otherwise
    """
    try:
        # Read file content
        if isinstance(filepath, StringIO):
            content = filepath.getvalue()
            filepath_display = "<StringIO>"
        else:
            filepath = Path(filepath)
            if not filepath.exists():
                print(f"Error: File not found: {filepath}", file=sys.stderr)
                return False
            content = filepath.read_text(encoding='utf-8')
            filepath_display = str(filepath)

        # Extract frontmatter
        frontmatter_str = extract_frontmatter(content)
        if frontmatter_str is None:
            print(f"Error: No YAML frontmatter found in {filepath_display}", file=sys.stderr)
            print("Expected frontmatter format:", file=sys.stderr)
            print("---", file=sys.stderr)
            print("field: value", file=sys.stderr)
            print("---", file=sys.stderr)
            return False

        # Parse frontmatter
        try:
            metadata = parse_frontmatter(frontmatter_str)
        except yaml.YAMLError as e:
            print(f"Error: Invalid YAML frontmatter in {filepath_display}", file=sys.stderr)
            print(f"YAML error: {e}", file=sys.stderr)
            return False

        # Auto-detect artifact type if not provided
        if artifact_type is None:
            artifact_type = metadata.get('type')
            if artifact_type is None:
                print(f"Error: No 'type' field in frontmatter and no --artifact-type specified",
                      file=sys.stderr)
                return False

        # Load schema
        try:
            schema = load_schema(artifact_type, schema_dir)
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            return False
        except yaml.YAMLError as e:
            print(f"Error: Invalid schema file: {e}", file=sys.stderr)
            return False

        # Validate metadata
        is_valid, errors = validate_metadata(metadata, schema)

        # Print report if verbose or if validation failed
        if verbose or not is_valid:
            report = format_validation_report(
                filepath_display,
                artifact_type,
                is_valid,
                errors,
                metadata,
                verbose
            )
            print(report)

        return is_valid

    except Exception as e:
        print(f"Error validating {filepath}: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point for validate_artifact script."""
    parser = argparse.ArgumentParser(
        description="Validate artifact against JSON Schema",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate with auto-detected type
  python validate_artifact.py phase-1-progress.md

  # Validate with explicit type
  python validate_artifact.py phase-1-progress.md --artifact-type progress

  # Verbose output
  python validate_artifact.py phase-1-progress.md --verbose

  # Custom schema directory
  python validate_artifact.py artifact.md --schema-dir /path/to/schemas
        """
    )

    parser.add_argument(
        'artifact',
        type=Path,
        help='Path to artifact file to validate'
    )

    parser.add_argument(
        '--artifact-type',
        '-t',
        choices=['progress', 'context', 'bug-fix', 'observation'],
        help='Type of artifact (auto-detected from frontmatter if not specified)'
    )

    parser.add_argument(
        '--schema-dir',
        '-s',
        type=Path,
        help='Directory containing schema files (default: ../schemas)'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Print detailed validation report'
    )

    args = parser.parse_args()

    # Validate artifact
    is_valid = validate_artifact_file(
        args.artifact,
        args.artifact_type,
        args.schema_dir,
        args.verbose
    )

    sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()
