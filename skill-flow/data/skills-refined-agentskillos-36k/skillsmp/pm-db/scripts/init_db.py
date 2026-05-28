#!/usr/bin/env python3
"""
Database Initialization Script for Project Management Database

Initializes the projects.db database and runs all migrations.

Usage:
    python3 skills/pm-db/scripts/init_db.py
    python3 skills/pm-db/scripts/init_db.py --reset

Features:
- Creates database at ~/.claude/projects.db
- Sets file permissions to 600 (user-only read/write)
- Runs all migrations via migrate.py
- Enables WAL mode for concurrency
- Optional reset (backup old database and create fresh one)
"""

import sqlite3
import sys
import os
import shutil
from pathlib import Path
from datetime import datetime

# Add lib and scripts to path
lib_path = Path(__file__).parent.parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

# Import migrate module
scripts_path = Path(__file__).parent
sys.path.insert(0, str(scripts_path))
import migrate


def backup_database(db_path: Path) -> Path:
    """
    Create backup of existing database.

    Args:
        db_path: Path to database file

    Returns:
        Path to backup file
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = db_path.with_suffix(f".backup-{timestamp}.db")

    print(f"  Creating backup: {backup_path}")
    shutil.copy2(db_path, backup_path)

    return backup_path


def set_file_permissions(db_path: Path):
    """
    Set database file permissions to 600 (user-only read/write).

    Args:
        db_path: Path to database file
    """
    os.chmod(db_path, 0o600)
    print(f"  ✅ File permissions set to 600 (user-only read/write)")


def enable_wal_mode(db_path: str):
    """
    Enable WAL mode for better concurrency.

    Args:
        db_path: Path to database file
    """
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        conn.commit()
        print("  ✅ WAL mode enabled")
        print("  ✅ Foreign keys enabled")
    finally:
        conn.close()


def verify_schema(db_path: str) -> bool:
    """
    Verify database schema is complete.

    Args:
        db_path: Path to database file

    Returns:
        True if schema is valid, False otherwise
    """
    conn = sqlite3.connect(db_path)

    try:
        # Check for required tables
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = [row[0] for row in cursor.fetchall()]

        required_tables = [
            'projects', 'specs', 'jobs', 'tasks',
            'code_reviews', 'execution_logs', 'agent_assignments',
            'schema_version'
        ]

        missing_tables = [t for t in required_tables if t not in tables]

        if missing_tables:
            print(f"  ❌ Missing tables: {missing_tables}")
            return False

        # Check schema version
        cursor = conn.execute("SELECT MAX(version) FROM schema_version")
        version = cursor.fetchone()[0]

        print(f"  ✅ Schema version: {version}")
        print(f"  ✅ All required tables present: {len(required_tables)}")

        return True

    except Exception as e:
        print(f"  ❌ Schema verification failed: {e}")
        return False

    finally:
        conn.close()


def get_database_stats(db_path: str):
    """
    Get database statistics.

    Args:
        db_path: Path to database file
    """
    db_path_obj = Path(db_path)

    if not db_path_obj.exists():
        print("  Database not yet created")
        return

    # File size
    size_bytes = db_path_obj.stat().st_size
    size_kb = size_bytes / 1024
    size_mb = size_kb / 1024

    if size_mb >= 1:
        size_str = f"{size_mb:.2f} MB"
    elif size_kb >= 1:
        size_str = f"{size_kb:.2f} KB"
    else:
        size_str = f"{size_bytes} bytes"

    print(f"  📊 Database size: {size_str}")

    # Record counts
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.execute("SELECT COUNT(*) FROM projects")
        projects = cursor.fetchone()[0]

        cursor = conn.execute("SELECT COUNT(*) FROM jobs")
        jobs = cursor.fetchone()[0]

        cursor = conn.execute("SELECT COUNT(*) FROM tasks")
        tasks = cursor.fetchone()[0]

        print(f"  📊 Projects: {projects}, Jobs: {jobs}, Tasks: {tasks}")

    except Exception as e:
        print(f"  📊 Unable to read stats: {e}")
    finally:
        conn.close()


def init_database(db_path: str, reset: bool = False) -> bool:
    """
    Initialize database.

    Args:
        db_path: Path to database file
        reset: If True, backup existing database and create fresh one

    Returns:
        True if successful, False if error
    """
    db_path_obj = Path(db_path)

    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📊 Database Initialization")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"\nDatabase path: {db_path}")

    # Check if database exists
    db_exists = db_path_obj.exists()

    if db_exists and not reset:
        print(f"\n⚠️  Database already exists!")
        get_database_stats(db_path)

        response = input("\nReset database? This will backup existing data. (y/N): ")
        if response.lower() != 'y':
            print("\nCancelled. Database unchanged.")
            return False

        reset = True

    # Backup existing database if resetting
    if db_exists and reset:
        print(f"\n📦 Backing up existing database...")
        backup_path = backup_database(db_path_obj)
        print(f"  ✅ Backup created: {backup_path}")

        # Remove old database
        db_path_obj.unlink()
        print(f"  ✅ Old database removed")

    # Create database file
    print(f"\n🔨 Creating new database...")

    # Ensure parent directory exists
    db_path_obj.parent.mkdir(parents=True, exist_ok=True)

    # Create empty database
    conn = sqlite3.connect(db_path)
    conn.close()
    print(f"  ✅ Database file created")

    # Set permissions
    set_file_permissions(db_path_obj)

    # Run migrations
    print(f"\n🔄 Running migrations...")
    success = migrate.run_migrations(db_path=db_path)

    if not success:
        print(f"\n❌ Migration failed!")
        return False

    # Enable WAL mode
    print(f"\n⚙️  Configuring database...")
    enable_wal_mode(db_path)

    # Verify schema
    print(f"\n✅ Verifying schema...")
    if not verify_schema(db_path):
        return False

    # Show stats
    print(f"\n📊 Database Statistics:")
    get_database_stats(db_path)

    # Success message
    print(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"✅ Database initialization complete!")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"\nDatabase ready at: {db_path}")
    print(f"\nYou can now:")
    print(f"  • Import specs: python3 skills/pm-db/scripts/import_specs.py")
    print(f"  • View dashboard: python3 skills/pm-db/scripts/generate_report.py")
    print(f"\n")

    return True


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Initialize project management database"
    )
    parser.add_argument(
        "--db-path",
        default=str(Path.home() / ".claude" / "projects.db"),
        help="Path to database file (default: ~/.claude/projects.db)"
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Backup existing database and create fresh one"
    )

    args = parser.parse_args()

    success = init_database(db_path=args.db_path, reset=args.reset)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
