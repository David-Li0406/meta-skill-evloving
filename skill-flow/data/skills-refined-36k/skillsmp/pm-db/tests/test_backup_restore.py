#!/usr/bin/env python3
"""
Backup and Restore Tests for PM-DB System

Tests backup and restore functionality:
- Backup creation
- Backup integrity verification
- Database restoration
- Safety backup creation
- Old backup cleanup

Usage:
    python3 skills/pm-db/tests/test_backup_restore.py
"""

import unittest
import tempfile
import subprocess
import json
from pathlib import Path
import sys
import shutil

# Add scripts to path
scripts_path = Path(__file__).parent.parent.parent.parent / "scripts"
sys.path.insert(0, str(scripts_path))

# Add lib to path
lib_path = Path(__file__).parent.parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

from project_database import ProjectDatabase


class TestBackupCreation(unittest.TestCase):
    """Test backup creation functionality"""

    def setUp(self):
        """Create temporary database and backup directory"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

        self.db_path = self.temp_path / "test.db"
        self.backup_dir = self.temp_path / "backups"

        # Create and populate database
        self.db = ProjectDatabase(db_path=str(self.db_path))

        # Run migrations
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                self.db.conn.executescript(f.read())

        # Add test data
        project_id = self.db.create_project("test-project", "Test", "/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")
        self.job_id = self.db.create_job(spec_id, "Test Job")

        self.db.close()

    def tearDown(self):
        """Clean up temporary files"""
        shutil.rmtree(self.temp_dir)

    def test_backup_script_exists(self):
        """Test backup script file exists and is executable"""
        script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "backup_db.py"
        self.assertTrue(script_path.exists())
        self.assertTrue(script_path.stat().st_mode & 0o111)  # Executable bit

    def test_backup_creation(self):
        """Test backup is created successfully"""
        script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "backup_db.py"

        result = subprocess.run(
            [
                sys.executable,
                str(script_path),
                "--db-path", str(self.db_path),
                "--backup-dir", str(self.backup_dir)
            ],
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0, f"Backup script failed: {result.stderr}")
        self.assertIn("Backup created successfully", result.stdout)

        # Verify backup file exists
        backups = list(self.backup_dir.glob("projects-backup-*.db"))
        self.assertEqual(len(backups), 1)

        # Verify backup has data
        backup_db = ProjectDatabase(db_path=str(backups[0]))
        jobs = backup_db.list_jobs()
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]['name'], "Test Job")
        backup_db.close()

    def test_backup_list(self):
        """Test backup listing functionality"""
        script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "backup_db.py"

        # Create a backup first
        subprocess.run(
            [
                sys.executable,
                str(script_path),
                "--db-path", str(self.db_path),
                "--backup-dir", str(self.backup_dir)
            ],
            capture_output=True
        )

        # List backups
        result = subprocess.run(
            [
                sys.executable,
                str(script_path),
                "--backup-dir", str(self.backup_dir),
                "--list"
            ],
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("Found 1 backups", result.stdout)
        self.assertIn("projects-backup-", result.stdout)

    def test_old_backup_cleanup(self):
        """Test old backup cleanup (keep only N recent)"""
        script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "backup_db.py"

        # Create 5 backups
        for i in range(5):
            subprocess.run(
                [
                    sys.executable,
                    str(script_path),
                    "--db-path", str(self.db_path),
                    "--backup-dir", str(self.backup_dir),
                    "--keep", "3"
                ],
                capture_output=True
            )

        # Verify only 3 backups remain
        backups = list(self.backup_dir.glob("projects-backup-*.db"))
        self.assertEqual(len(backups), 3)


class TestRestoreFunctionality(unittest.TestCase):
    """Test database restore functionality"""

    def setUp(self):
        """Create temporary database and backup"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

        self.original_db = self.temp_path / "original.db"
        self.backup_file = self.temp_path / "backup.db"
        self.restored_db = self.temp_path / "restored.db"

        # Create and populate original database
        db = ProjectDatabase(db_path=str(self.original_db))

        # Run migrations
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                db.conn.executescript(f.read())

        # Add test data
        project_id = db.create_project("original-project", "Original", "/tmp/original")
        spec_id = db.create_spec(project_id, "spec", frd_content="# Original FRD")
        self.job_id = db.create_job(spec_id, "Original Job")

        db.close()

        # Create backup
        shutil.copy2(self.original_db, self.backup_file)

    def tearDown(self):
        """Clean up temporary files"""
        shutil.rmtree(self.temp_dir)

    def test_restore_script_exists(self):
        """Test restore script file exists and is executable"""
        script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "restore_db.py"
        self.assertTrue(script_path.exists())
        self.assertTrue(script_path.stat().st_mode & 0o111)  # Executable bit

    def test_restore_to_new_location(self):
        """Test restoring backup to new location"""
        script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "restore_db.py"

        result = subprocess.run(
            [
                sys.executable,
                str(script_path),
                str(self.backup_file),
                "--db-path", str(self.restored_db),
                "--force"
            ],
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0, f"Restore script failed: {result.stderr}")
        self.assertIn("Restore complete", result.stdout)

        # Verify restored database has correct data
        db = ProjectDatabase(db_path=str(self.restored_db))
        jobs = db.list_jobs()
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]['name'], "Original Job")
        db.close()

    def test_restore_with_safety_backup(self):
        """Test restore creates safety backup of existing database"""
        script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "restore_db.py"

        # Create an existing database at target location
        existing_db = ProjectDatabase(db_path=str(self.restored_db))
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                existing_db.conn.executescript(f.read())

        project_id = existing_db.create_project("existing", "Existing", "/tmp/existing")
        existing_db.close()

        # Restore (should create safety backup)
        result = subprocess.run(
            [
                sys.executable,
                str(script_path),
                str(self.backup_file),
                "--db-path", str(self.restored_db),
                "--force"
            ],
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("Safety backup created", result.stdout)

        # Verify safety backup exists
        safety_backups = list(self.temp_path.glob("projects-pre-restore-*.db"))
        self.assertEqual(len(safety_backups), 1)

        # Verify safety backup contains old data
        safety_db = ProjectDatabase(db_path=str(safety_backups[0]))
        projects = safety_db.list_projects()
        self.assertEqual(projects[0]['name'], "existing")
        safety_db.close()

    def test_restore_invalid_backup(self):
        """Test restore rejects invalid backup file"""
        script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "restore_db.py"

        # Create invalid backup (empty file)
        invalid_backup = self.temp_path / "invalid.db"
        invalid_backup.write_text("not a database")

        result = subprocess.run(
            [
                sys.executable,
                str(script_path),
                str(invalid_backup),
                "--db-path", str(self.restored_db),
                "--force"
            ],
            capture_output=True,
            text=True
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("verification failed", result.stdout)


class TestBackupIntegrity(unittest.TestCase):
    """Test backup integrity and data consistency"""

    def setUp(self):
        """Create temporary database"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

        self.db_path = self.temp_path / "test.db"
        self.backup_dir = self.temp_path / "backups"

    def tearDown(self):
        """Clean up temporary files"""
        shutil.rmtree(self.temp_dir)

    def test_backup_preserves_all_data(self):
        """Test backup contains all data from original database"""
        # Create database with comprehensive data
        db = ProjectDatabase(db_path=str(self.db_path))

        # Run migrations
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                db.conn.executescript(f.read())

        # Add comprehensive test data
        project_id = db.create_project("backup-test", "Backup Test", "/tmp/backup-test")
        spec_id = db.create_spec(project_id, "spec", frd_content="# FRD Content")
        job_id = db.create_job(spec_id, "Test Job")
        task_id = db.create_task(job_id, "Test Task", order=1)

        db.log_execution(job_id, task_id, "test command", "test output", 0, 1000)
        db.add_code_review(job_id, None, "reviewer", "summary", "approved")

        original_projects = db.list_projects()
        original_jobs = db.list_jobs()
        original_logs = db.get_execution_logs()

        db.close()

        # Create backup
        script_path = Path(__file__).parent.parent.parent.parent / "scripts" / "backup_db.py"
        subprocess.run(
            [
                sys.executable,
                str(script_path),
                "--db-path", str(self.db_path),
                "--backup-dir", str(self.backup_dir)
            ],
            capture_output=True
        )

        # Verify backup
        backup_files = list(self.backup_dir.glob("projects-backup-*.db"))
        self.assertEqual(len(backup_files), 1)

        backup_db = ProjectDatabase(db_path=str(backup_files[0]))

        backup_projects = backup_db.list_projects()
        backup_jobs = backup_db.list_jobs()
        backup_logs = backup_db.get_execution_logs()

        # Verify all data preserved
        self.assertEqual(len(backup_projects), len(original_projects))
        self.assertEqual(len(backup_jobs), len(original_jobs))
        self.assertEqual(len(backup_logs), len(original_logs))

        self.assertEqual(backup_projects[0]['name'], original_projects[0]['name'])
        self.assertEqual(backup_jobs[0]['name'], original_jobs[0]['name'])

        backup_db.close()


if __name__ == '__main__':
    # Run with verbose output
    unittest.main(verbosity=2)
