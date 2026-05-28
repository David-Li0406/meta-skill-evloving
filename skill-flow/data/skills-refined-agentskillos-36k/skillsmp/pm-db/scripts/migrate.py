#!/usr/bin/env python3
"""
Migration Runner for Project Management Database

Applies database migrations in order with rollback capability.

Usage:
    python3 skills/pm-db/scripts/migrate.py
    python3 skills/pm-db/scripts/migrate.py --dry-run
    python3 skills/pm-db/scripts/migrate.py --target-version 2

Features:
- Auto-discovers migration files from migrations/ directory
- Tracks applied migrations in schema_version table
- Skips already-applied migrations
- Rolls back on error
- Dry-run mode for testing
"""

import sqlite3
import sys
from pathlib import Path
from typing import List, Tuple

# Add lib to path for ProjectDatabase import
lib_path = Path(__file__).parent.parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))


def get_migration_files(migrations_dir: Path) -> List[Tuple[int, Path]]:
    """
    Discover migration files and extract version numbers.

    Args:
        migrations_dir: Path to migrations directory

    Returns:
        List of (version, path) tuples sorted by version
    """
    migrations = []

    for sql_file in sorted(migrations_dir.glob("*.sql")):
        # Extract version from filename (e.g., "001_initial.sql" -> 1)
        try:
            version = int(sql_file.stem.split("_")[0])
            migrations.append((version, sql_file))
        except (ValueError, IndexError):
            print(f"Warning: Skipping invalid migration filename: {sql_file.name}")
            continue

    # Sort by version
    migrations.sort(key=lambda x: x[0])

    return migrations


def get_current_version(conn: sqlite3.Connection) -> int:
    """
    Get current schema version from database.

    Args:
        conn: SQLite connection

    Returns:
        Current schema version (0 if no schema_version table exists)
    """
    try:
        cursor = conn.execute(
            "SELECT MAX(version) FROM schema_version"
        )
        result = cursor.fetchone()
        return result[0] if result[0] is not None else 0
    except sqlite3.OperationalError:
        # schema_version table doesn't exist yet
        return 0


def apply_migration(
    conn: sqlite3.Connection,
    version: int,
    sql_file: Path,
    dry_run: bool = False
) -> bool:
    """
    Apply a single migration.

    Args:
        conn: SQLite connection
        version: Migration version number
        sql_file: Path to SQL file
        dry_run: If True, don't actually apply (just show what would happen)

    Returns:
        True if successful, False if error

    Raises:
        sqlite3.Error: If migration fails
    """
    print(f"  Applying migration {version}: {sql_file.name}")

    if dry_run:
        print(f"    [DRY RUN] Would execute SQL from {sql_file}")
        return True

    # Read SQL file
    with open(sql_file, 'r') as f:
        sql = f.read()

    # Execute migration (already wrapped in transaction in SQL file)
    try:
        conn.executescript(sql)
        print(f"    ✅ Migration {version} applied successfully")
        return True
    except sqlite3.Error as e:
        print(f"    ❌ Migration {version} failed: {e}")
        raise


def run_migrations(
    db_path: str,
    migrations_dir: str = "migrations",
    dry_run: bool = False,
    target_version: int = None
) -> bool:
    """
    Run all pending migrations.

    Args:
        db_path: Path to SQLite database
        migrations_dir: Path to migrations directory
        dry_run: If True, show what would happen without applying
        target_version: Optional version to migrate to (default: latest)

    Returns:
        True if all migrations successful, False if any failed
    """
    db_path_obj = Path(db_path)
    migrations_path = Path(migrations_dir)

    if not migrations_path.exists():
        print(f"Error: Migrations directory not found: {migrations_path}")
        return False

    # Discover migration files
    migrations = get_migration_files(migrations_path)

    if not migrations:
        print("No migration files found.")
        return True

    print(f"Found {len(migrations)} migration file(s)")

    # Connect to database
    conn = sqlite3.connect(db_path)

    try:
        # Get current version
        current_version = get_current_version(conn)
        print(f"Current schema version: {current_version}")

        # Determine target version
        if target_version is None:
            target_version = migrations[-1][0]  # Latest version

        print(f"Target schema version: {target_version}")

        # Filter migrations to apply
        pending_migrations = [
            (v, p) for v, p in migrations
            if v > current_version and v <= target_version
        ]

        if not pending_migrations:
            print("No pending migrations to apply.")
            return True

        print(f"\nApplying {len(pending_migrations)} pending migration(s):")

        # Apply each migration
        for version, sql_file in pending_migrations:
            if not apply_migration(conn, version, sql_file, dry_run=dry_run):
                return False

        if dry_run:
            print("\n[DRY RUN] No changes made to database.")
        else:
            print(f"\n✅ All migrations applied successfully!")
            print(f"Schema version: {current_version} → {target_version}")

        return True

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print("Rolling back changes...")
        conn.rollback()
        return False

    finally:
        conn.close()


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Apply database migrations"
    )
    parser.add_argument(
        "--db-path",
        default=str(Path.home() / ".claude" / "projects.db"),
        help="Path to database file (default: ~/.claude/projects.db)"
    )
    parser.add_argument(
        "--migrations-dir",
        default="migrations",
        help="Path to migrations directory (default: migrations)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without applying migrations"
    )
    parser.add_argument(
        "--target-version",
        type=int,
        help="Migrate to specific version (default: latest)"
    )

    args = parser.parse_args()

    success = run_migrations(
        db_path=args.db_path,
        migrations_dir=args.migrations_dir,
        dry_run=args.dry_run,
        target_version=args.target_version
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
