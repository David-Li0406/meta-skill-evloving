#!/usr/bin/env python3
"""
Bulk migration script for artifact tracking.

This script finds all markdown files in a directory, backs up originals, converts each using
convert_to_hybrid.py, validates all conversions, generates a migration report, and supports
dry-run mode.

Usage:
    python migrate_all.py --directory .claude/progress
    python migrate_all.py --directory .claude/progress --backup
    python migrate_all.py --directory .claude/progress --dry-run
    python migrate_all.py --directory .claude/progress --backup-dir .backups
    python migrate_all.py --directory .claude/worknotes --artifact-type context
"""

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from convert_to_hybrid import convert_file, detect_artifact_type
from validate_artifact import validate_artifact_file


class MigrationStats:
    """Track migration statistics."""

    def __init__(self):
        self.total_files: int = 0
        self.converted: int = 0
        self.failed: int = 0
        self.skipped: int = 0
        self.validated: int = 0
        self.validation_failed: int = 0
        self.errors: List[str] = []

    def add_error(self, filepath: Path, error: str):
        """Add an error message."""
        self.errors.append(f"{filepath}: {error}")

    def format_report(self) -> str:
        """Format a migration report."""
        lines = []
        lines.append("=" * 70)
        lines.append("Artifact Migration Report")
        lines.append("=" * 70)
        lines.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append(f"Total Files: {self.total_files}")
        lines.append(f"Converted: {self.converted}")
        lines.append(f"Failed: {self.failed}")
        lines.append(f"Skipped: {self.skipped}")
        lines.append(f"Validated: {self.validated}")
        lines.append(f"Validation Failed: {self.validation_failed}")
        lines.append("")

        if self.errors:
            lines.append(f"Errors ({len(self.errors)}):")
            for error in self.errors:
                lines.append(f"  • {error}")
            lines.append("")

        success_rate = (self.converted / self.total_files * 100) if self.total_files > 0 else 0
        lines.append(f"Success Rate: {success_rate:.1f}%")
        lines.append("=" * 70)

        return "\n".join(lines)


def find_markdown_files(directory: Path, recursive: bool = True) -> List[Path]:
    """
    Find all markdown files in directory.

    Args:
        directory: Directory to search
        recursive: Search recursively

    Returns:
        List of markdown file paths
    """
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    if recursive:
        return sorted(directory.rglob("*.md"))
    else:
        return sorted(directory.glob("*.md"))


def backup_file(filepath: Path, backup_dir: Optional[Path] = None) -> Path:
    """
    Create a backup of a file.

    Args:
        filepath: File to backup
        backup_dir: Backup directory (default: .backups next to file)

    Returns:
        Path to backup file
    """
    if backup_dir is None:
        backup_dir = filepath.parent / '.backups'

    backup_dir.mkdir(parents=True, exist_ok=True)

    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"{filepath.stem}.{timestamp}{filepath.suffix}"
    backup_path = backup_dir / backup_name

    # Copy file to backup
    shutil.copy2(filepath, backup_path)

    return backup_path


def should_skip_file(filepath: Path) -> bool:
    """
    Determine if a file should be skipped during migration.

    Args:
        filepath: File to check

    Returns:
        True if file should be skipped
    """
    # Skip backup directories
    if '.backups' in filepath.parts or '.backup' in filepath.parts:
        return True

    # Skip hidden files
    if filepath.name.startswith('.'):
        return True

    # Skip README files
    if filepath.name.upper() == 'README.MD':
        return True

    # Skip template files
    if 'template' in filepath.name.lower():
        return True

    return False


def migrate_directory(
    directory: Path,
    artifact_type: Optional[str] = None,
    backup: bool = False,
    backup_dir: Optional[Path] = None,
    dry_run: bool = False,
    recursive: bool = True,
    verbose: bool = False,
) -> MigrationStats:
    """
    Migrate all artifacts in a directory.

    Args:
        directory: Directory to migrate
        artifact_type: Type of artifacts (auto-detect if None)
        backup: Create backups before converting
        backup_dir: Custom backup directory
        dry_run: Preview changes without modifying files
        recursive: Search recursively
        verbose: Print detailed progress

    Returns:
        MigrationStats object
    """
    stats = MigrationStats()

    # Find all markdown files
    try:
        files = find_markdown_files(directory, recursive)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return stats

    stats.total_files = len(files)

    if stats.total_files == 0:
        print(f"No markdown files found in {directory}")
        return stats

    print(f"Found {stats.total_files} markdown file(s) in {directory}")
    if dry_run:
        print("DRY RUN MODE: No files will be modified")
    print("")

    # Process each file
    for filepath in files:
        # Check if file should be skipped
        if should_skip_file(filepath):
            stats.skipped += 1
            if verbose:
                print(f"⊘ Skipping: {filepath.name}")
            continue

        if verbose:
            print(f"Processing: {filepath}")

        # Backup file if requested
        if backup and not dry_run:
            try:
                backup_path = backup_file(filepath, backup_dir)
                if verbose:
                    print(f"  Backed up to: {backup_path}")
            except Exception as e:
                error_msg = f"Backup failed: {e}"
                stats.add_error(filepath, error_msg)
                if verbose:
                    print(f"  ✗ {error_msg}")
                stats.failed += 1
                continue

        # Detect artifact type if not provided
        file_artifact_type = artifact_type
        if file_artifact_type is None:
            try:
                content = filepath.read_text(encoding='utf-8')
                file_artifact_type = detect_artifact_type(filepath, content)
                if verbose:
                    print(f"  Detected type: {file_artifact_type}")
            except Exception as e:
                error_msg = f"Could not detect artifact type: {e}"
                stats.add_error(filepath, error_msg)
                if verbose:
                    print(f"  ✗ {error_msg}")
                stats.failed += 1
                continue

        # Convert file
        try:
            success = convert_file(
                filepath,
                output_path=filepath,  # In-place conversion
                artifact_type=file_artifact_type,
                dry_run=dry_run
            )

            if success:
                stats.converted += 1
                if verbose:
                    print(f"  ✓ Converted successfully")

                # Validate if not dry run
                if not dry_run:
                    try:
                        is_valid = validate_artifact_file(
                            filepath,
                            file_artifact_type,
                            verbose=False
                        )

                        if is_valid:
                            stats.validated += 1
                            if verbose:
                                print(f"  ✓ Validation passed")
                        else:
                            stats.validation_failed += 1
                            error_msg = "Validation failed"
                            stats.add_error(filepath, error_msg)
                            if verbose:
                                print(f"  ✗ {error_msg}")

                    except Exception as e:
                        error_msg = f"Validation error: {e}"
                        stats.add_error(filepath, error_msg)
                        stats.validation_failed += 1
                        if verbose:
                            print(f"  ✗ {error_msg}")

            else:
                stats.failed += 1
                error_msg = "Conversion failed"
                stats.add_error(filepath, error_msg)
                if verbose:
                    print(f"  ✗ {error_msg}")

        except Exception as e:
            error_msg = f"Conversion error: {e}"
            stats.add_error(filepath, error_msg)
            stats.failed += 1
            if verbose:
                print(f"  ✗ {error_msg}")

        if verbose:
            print("")

    return stats


def save_migration_report(stats: MigrationStats, output_path: Optional[Path] = None):
    """
    Save migration report to file.

    Args:
        stats: Migration statistics
        output_path: Output file path (default: migration-report-TIMESTAMP.txt)
    """
    if output_path is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = Path(f"migration-report-{timestamp}.txt")

    report = stats.format_report()
    output_path.write_text(report, encoding='utf-8')
    print(f"\nMigration report saved to: {output_path}")


def main():
    """Main entry point for migrate_all script."""
    parser = argparse.ArgumentParser(
        description="Bulk migration of artifact tracking files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Migrate all files in directory
  python migrate_all.py --directory .claude/progress

  # Migrate with backups
  python migrate_all.py --directory .claude/progress --backup

  # Dry run to preview changes
  python migrate_all.py --directory .claude/progress --dry-run

  # Custom backup directory
  python migrate_all.py --directory .claude/progress --backup --backup-dir .backups

  # Migrate specific artifact type
  python migrate_all.py --directory .claude/worknotes --artifact-type context

  # Verbose output
  python migrate_all.py --directory .claude/progress --verbose

  # Save migration report
  python migrate_all.py --directory .claude/progress --report migration-report.txt
        """
    )

    parser.add_argument(
        '--directory',
        '-d',
        type=Path,
        required=True,
        help='Directory to migrate'
    )

    parser.add_argument(
        '--artifact-type',
        '-t',
        choices=['progress', 'context', 'bug-fix', 'observation'],
        help='Type of artifacts (auto-detected if not specified)'
    )

    parser.add_argument(
        '--backup',
        '-b',
        action='store_true',
        help='Create backups before converting'
    )

    parser.add_argument(
        '--backup-dir',
        type=Path,
        help='Custom backup directory (default: .backups)'
    )

    parser.add_argument(
        '--dry-run',
        '-n',
        action='store_true',
        help='Preview changes without modifying files'
    )

    parser.add_argument(
        '--no-recursive',
        action='store_true',
        help='Do not search recursively (only top-level files)'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Print detailed progress'
    )

    parser.add_argument(
        '--report',
        '-r',
        type=Path,
        help='Save migration report to file'
    )

    args = parser.parse_args()

    # Migrate directory
    stats = migrate_directory(
        args.directory,
        artifact_type=args.artifact_type,
        backup=args.backup,
        backup_dir=args.backup_dir,
        dry_run=args.dry_run,
        recursive=not args.no_recursive,
        verbose=args.verbose,
    )

    # Print report
    report = stats.format_report()
    print("\n" + report)

    # Save report to file if requested
    if args.report:
        save_migration_report(stats, args.report)

    # Exit with appropriate code
    if stats.failed > 0 or stats.validation_failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
