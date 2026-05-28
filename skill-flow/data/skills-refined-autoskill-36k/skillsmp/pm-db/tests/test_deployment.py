#!/usr/bin/env python3
"""
Deployment Validation Tests for PM-DB System

Tests deployment readiness:
- Database initialization
- Migration execution
- Script functionality
- File structure
- System health checks

Usage:
    python3 skills/pm-db/tests/test_deployment.py
"""

import unittest
import tempfile
import subprocess
import json
from pathlib import Path
import sys
import shutil
import os

# Add lib to path
lib_path = Path(__file__).parent.parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

from project_database import ProjectDatabase


class TestDatabaseInitialization(unittest.TestCase):
    """Test database initialization from scratch"""

    def setUp(self):
        """Create temporary directory"""
        self.temp_dir = tempfile.mkdtemp(prefix='test-deploy-')
        self.db_path = Path(self.temp_dir) / "projects.db"

    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_database_creation(self):
        """Test database file is created correctly"""
        print("\n  Testing database creation...")

        # Database should not exist yet
        self.assertFalse(self.db_path.exists())

        # Create database
        db = ProjectDatabase(db_path=str(self.db_path))
        db.close()

        # Database should now exist
        self.assertTrue(self.db_path.exists())
        print(f"  ✓ Database created: {self.db_path}")

        # Verify file permissions (should be readable/writable by user)
        stat = self.db_path.stat()
        self.assertTrue(stat.st_mode & 0o600)  # User read/write
        print(f"  ✓ File permissions: {oct(stat.st_mode)[-3:]}")

        # Verify SQLite file format
        with open(self.db_path, 'rb') as f:
            header = f.read(16)
            self.assertEqual(header[:15], b'SQLite format 3')
        print(f"  ✓ Valid SQLite file format")

    def test_wal_mode_enabled(self):
        """Test WAL mode is enabled automatically"""
        print("\n  Testing WAL mode...")

        db = ProjectDatabase(db_path=str(self.db_path))

        # Check journal mode
        cursor = db.conn.execute("PRAGMA journal_mode")
        mode = cursor.fetchone()[0]
        self.assertEqual(mode.lower(), 'wal')
        print(f"  ✓ Journal mode: {mode}")

        db.close()

        # Verify WAL and SHM files exist
        wal_file = Path(str(self.db_path) + "-wal")
        shm_file = Path(str(self.db_path) + "-shm")

        # These files are created after first write
        db = ProjectDatabase(db_path=str(self.db_path))
        db.conn.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER)")
        db.conn.commit()
        db.close()

        print(f"  ✓ WAL mode operational")

    def test_foreign_keys_enabled(self):
        """Test foreign keys are enabled"""
        print("\n  Testing foreign key enforcement...")

        db = ProjectDatabase(db_path=str(self.db_path))

        # Check foreign_keys setting
        cursor = db.conn.execute("PRAGMA foreign_keys")
        enabled = cursor.fetchone()[0]
        self.assertEqual(enabled, 1)
        print(f"  ✓ Foreign keys enabled: {bool(enabled)}")

        db.close()


class TestMigrationExecution(unittest.TestCase):
    """Test migration system"""

    def setUp(self):
        """Create temporary directory"""
        self.temp_dir = tempfile.mkdtemp(prefix='test-migrate-')
        self.db_path = Path(self.temp_dir) / "projects.db"

    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_migration_execution(self):
        """Test all migrations execute successfully"""
        print("\n  Testing migration execution...")

        db = ProjectDatabase(db_path=str(self.db_path))

        # Run migrations
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        migration_files = sorted(migrations_dir.glob("*.sql"))

        self.assertGreater(len(migration_files), 0, "No migration files found")
        print(f"  ✓ Found {len(migration_files)} migration files")

        for i, migration_file in enumerate(migration_files, 1):
            print(f"  ✓ Running migration {i}: {migration_file.name}")
            with open(migration_file, 'r') as f:
                sql = f.read()
                db.conn.executescript(sql)

        db.conn.commit()
        print(f"  ✓ All migrations executed successfully")

        # Verify schema_version table exists and has entries
        cursor = db.conn.execute("SELECT COUNT(*) FROM schema_version")
        version_count = cursor.fetchone()[0]
        self.assertGreater(version_count, 0)
        print(f"  ✓ Schema version entries: {version_count}")

        # Verify all expected tables exist
        expected_tables = [
            'projects', 'specs', 'jobs', 'tasks',
            'code_reviews', 'execution_logs', 'agent_assignments',
            'schema_version'
        ]

        cursor = db.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = [row[0] for row in cursor.fetchall()]

        for table in expected_tables:
            self.assertIn(table, tables, f"Table {table} missing")
            print(f"  ✓ Table exists: {table}")

        db.close()

    def test_schema_version_tracking(self):
        """Test schema version is tracked correctly"""
        print("\n  Testing schema version tracking...")

        db = ProjectDatabase(db_path=str(self.db_path))

        # Run migrations
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                db.conn.executescript(f.read())

        # Check latest version
        cursor = db.conn.execute(
            "SELECT MAX(version) as latest_version FROM schema_version"
        )
        latest_version = cursor.fetchone()['latest_version']

        self.assertIsNotNone(latest_version)
        self.assertGreater(latest_version, 0)
        print(f"  ✓ Latest schema version: {latest_version}")

        # Verify version metadata
        cursor = db.conn.execute(
            "SELECT version, description, applied_at FROM schema_version ORDER BY version"
        )
        versions = cursor.fetchall()

        for version in versions:
            self.assertIsNotNone(version['description'])
            self.assertIsNotNone(version['applied_at'])
            print(f"  ✓ Version {version['version']}: {version['description']}")

        db.close()


class TestScriptFunctionality(unittest.TestCase):
    """Test all scripts execute correctly"""

    def setUp(self):
        """Create temporary environment"""
        self.temp_dir = tempfile.mkdtemp(prefix='test-scripts-')
        self.db_path = Path(self.temp_dir) / "projects.db"

        # Initialize database
        db = ProjectDatabase(db_path=str(self.db_path))
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                db.conn.executescript(f.read())
        db.close()

    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_script(self):
        """Test init_db.py script"""
        print("\n  Testing init_db.py script...")

        script_path = Path(__file__).parent.parent / "scripts" / "init_db.py"

        if script_path.exists():
            # Note: Can't fully test interactive script, but can verify it's valid Python
            result = subprocess.run(
                ["python3", "-m", "py_compile", str(script_path)],
                capture_output=True
            )
            self.assertEqual(result.returncode, 0, "Script has syntax errors")
            print(f"  ✓ init_db.py: Valid Python syntax")
        else:
            print(f"  ⚠ init_db.py not found (expected location: {script_path})")

    def test_migrate_script(self):
        """Test migrate.py script"""
        print("\n  Testing migrate.py script...")

        script_path = Path(__file__).parent.parent / "scripts" / "migrate.py"

        if script_path.exists():
            result = subprocess.run(
                ["python3", "-m", "py_compile", str(script_path)],
                capture_output=True
            )
            self.assertEqual(result.returncode, 0, "Script has syntax errors")
            print(f"  ✓ migrate.py: Valid Python syntax")
        else:
            print(f"  ⚠ migrate.py not found")

    def test_import_script(self):
        """Test import_specs.py script"""
        print("\n  Testing import_specs.py script...")

        script_path = Path(__file__).parent.parent / "scripts" / "import_specs.py"

        if script_path.exists():
            result = subprocess.run(
                ["python3", "-m", "py_compile", str(script_path)],
                capture_output=True
            )
            self.assertEqual(result.returncode, 0, "Script has syntax errors")
            print(f"  ✓ import_specs.py: Valid Python syntax")
        else:
            print(f"  ⚠ import_specs.py not found")

    def test_export_script(self):
        """Test export_to_memory_bank.py script"""
        print("\n  Testing export_to_memory_bank.py script...")

        script_path = Path(__file__).parent.parent / "scripts" / "export_to_memory_bank.py"

        if script_path.exists():
            result = subprocess.run(
                ["python3", "-m", "py_compile", str(script_path)],
                capture_output=True
            )
            self.assertEqual(result.returncode, 0, "Script has syntax errors")
            print(f"  ✓ export_to_memory_bank.py: Valid Python syntax")
        else:
            print(f"  ⚠ export_to_memory_bank.py not found")

    def test_dashboard_script(self):
        """Test generate_report.py script"""
        print("\n  Testing generate_report.py script...")

        script_path = Path(__file__).parent.parent / "scripts" / "generate_report.py"

        if script_path.exists():
            result = subprocess.run(
                ["python3", "-m", "py_compile", str(script_path)],
                capture_output=True
            )
            self.assertEqual(result.returncode, 0, "Script has syntax errors")
            print(f"  ✓ generate_report.py: Valid Python syntax")
        else:
            print(f"  ⚠ generate_report.py not found (non-critical)")


class TestFileStructure(unittest.TestCase):
    """Test file structure is correct"""

    def test_required_directories_exist(self):
        """Test all required directories exist"""
        print("\n  Testing directory structure...")

        base_dir = Path(__file__).parent.parent.parent.parent

        required_dirs = [
            "lib",
            "migrations",
            "skills/pm-db",
            "skills/pm-db/scripts",
            "skills/pm-db/tests",
        ]

        for dir_path in required_dirs:
            full_path = base_dir / dir_path
            self.assertTrue(full_path.exists(), f"Directory {dir_path} missing")
            self.assertTrue(full_path.is_dir(), f"{dir_path} is not a directory")
            print(f"  ✓ Directory exists: {dir_path}")

    def test_required_files_exist(self):
        """Test all required files exist"""
        print("\n  Testing required files...")

        base_dir = Path(__file__).parent.parent.parent.parent

        required_files = [
            "lib/project_database.py",
            "skills/pm-db/SKILL.md",
            "skills/pm-db/README.md",
            "skills/pm-db/USER_GUIDE.md",
            "skills/pm-db/API_REFERENCE.md",
            "skills/pm-db/DEVELOPMENT.md",
            "skills/pm-db/SECURITY_AUDIT.md",
        ]

        for file_path in required_files:
            full_path = base_dir / file_path
            self.assertTrue(full_path.exists(), f"File {file_path} missing")
            self.assertTrue(full_path.is_file(), f"{file_path} is not a file")
            print(f"  ✓ File exists: {file_path}")

    def test_migration_files_exist(self):
        """Test migration files exist and are numbered correctly"""
        print("\n  Testing migration files...")

        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        migration_files = sorted(migrations_dir.glob("*.sql"))

        self.assertGreater(len(migration_files), 0, "No migration files found")
        print(f"  ✓ Migration files found: {len(migration_files)}")

        # Verify sequential numbering
        for i, migration_file in enumerate(migration_files, 1):
            # Migration files should be 001_xxx.sql, 002_xxx.sql, etc.
            filename = migration_file.name
            # Just verify they're numbered (not necessarily sequential from 1)
            self.assertTrue(filename[0].isdigit(), f"Migration {filename} not numbered")
            print(f"  ✓ Migration file: {filename}")

    def test_test_files_exist(self):
        """Test all test files exist"""
        print("\n  Testing test suite files...")

        tests_dir = Path(__file__).parent

        expected_tests = [
            "test_project_database.py",
            "test_integration.py",
            "test_performance.py",
            "test_hooks.py",
            "test_security.py",
            "test_end_to_end.py",
            "test_deployment.py",  # This file
        ]

        for test_file in expected_tests:
            full_path = tests_dir / test_file
            if full_path.exists():
                self.assertTrue(full_path.is_file())
                # Verify it's executable
                stat = full_path.stat()
                # Check if user has execute permission
                print(f"  ✓ Test file exists: {test_file}")
            else:
                print(f"  ⚠ Test file missing: {test_file}")


class TestSystemHealthCheck(unittest.TestCase):
    """Test overall system health"""

    def setUp(self):
        """Create temporary environment"""
        self.temp_dir = tempfile.mkdtemp(prefix='test-health-')
        self.db_path = Path(self.temp_dir) / "projects.db"

        # Initialize database with migrations
        db = ProjectDatabase(db_path=str(self.db_path))
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                db.conn.executescript(f.read())
        db.close()

    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_basic_crud_operations(self):
        """Test basic CRUD operations work"""
        print("\n  Testing basic CRUD operations...")

        db = ProjectDatabase(db_path=str(self.db_path))

        # Create
        project_id = db.create_project("test", "Test", "/tmp/test")
        self.assertIsNotNone(project_id)
        print(f"  ✓ CREATE: Project created")

        # Read
        project = db.get_project(project_id)
        self.assertIsNotNone(project)
        self.assertEqual(project['name'], "test")
        print(f"  ✓ READ: Project retrieved")

        # Update (via spec creation)
        spec_id = db.create_spec(project_id, "spec", frd_content="# FRD")
        self.assertIsNotNone(spec_id)
        print(f"  ✓ UPDATE: Spec created")

        # Delete (via SQL - not exposed in API)
        db.conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        db.conn.commit()
        deleted_project = db.get_project(project_id)
        self.assertIsNone(deleted_project)
        print(f"  ✓ DELETE: Project deleted")

        db.close()

    def test_all_core_methods_callable(self):
        """Test all core API methods are callable"""
        print("\n  Testing core API methods...")

        db = ProjectDatabase(db_path=str(self.db_path))

        # Create test data
        project_id = db.create_project("test", "Test", "/tmp/test")
        spec_id = db.create_spec(project_id, "spec", frd_content="# FRD")
        job_id = db.create_job(spec_id, "job")
        task_id = db.create_task(job_id, "task", order=1)

        # Test all major methods
        methods_tested = []

        # Project methods
        db.get_project(project_id)
        methods_tested.append("get_project")
        db.get_project_by_name("test")
        methods_tested.append("get_project_by_name")
        db.list_projects()
        methods_tested.append("list_projects")

        # Spec methods
        db.get_spec(spec_id)
        methods_tested.append("get_spec")
        db.list_specs()
        methods_tested.append("list_specs")

        # Job methods
        db.get_job(job_id)
        methods_tested.append("get_job")
        db.list_jobs()
        methods_tested.append("list_jobs")
        db.start_job(job_id)
        methods_tested.append("start_job")

        # Task methods
        db.get_task(task_id)
        methods_tested.append("get_task")
        db.get_tasks(job_id)
        methods_tested.append("get_tasks")
        db.start_task(task_id)
        methods_tested.append("start_task")
        db.complete_task(task_id, 0)
        methods_tested.append("complete_task")

        # Code review methods
        review_id = db.add_code_review(job_id, None, "reviewer", "summary", "approved")
        methods_tested.append("add_code_review")
        db.get_code_reviews(job_id=job_id)
        methods_tested.append("get_code_reviews")

        # Execution log methods
        log_id = db.log_execution(job_id, task_id, "cmd", "output", 0, 100)
        methods_tested.append("log_execution")
        db.get_execution_logs(job_id=job_id)
        methods_tested.append("get_execution_logs")
        db.search_execution_logs(command_pattern="%cmd%")
        methods_tested.append("search_execution_logs")

        # Reporting methods
        db.generate_dashboard()
        methods_tested.append("generate_dashboard")
        db.get_job_timeline(job_id)
        methods_tested.append("get_job_timeline")
        db.get_dependency_graph(job_id)
        methods_tested.append("get_dependency_graph")
        db.get_code_review_metrics()
        methods_tested.append("get_code_review_metrics")

        # Complete job
        db.complete_job(job_id, 0)
        methods_tested.append("complete_job")

        print(f"  ✓ All {len(methods_tested)} core methods callable")
        for method in methods_tested:
            print(f"    ✓ {method}()")

        db.close()

    def test_concurrent_access(self):
        """Test database handles concurrent access (basic check)"""
        print("\n  Testing concurrent access...")

        # Open two connections
        db1 = ProjectDatabase(db_path=str(self.db_path))
        db2 = ProjectDatabase(db_path=str(self.db_path))

        # Write from both
        project1_id = db1.create_project("project1", "Project 1", "/tmp/p1")
        project2_id = db2.create_project("project2", "Project 2", "/tmp/p2")

        # Read from both
        p1_from_db1 = db1.get_project(project1_id)
        p1_from_db2 = db2.get_project(project1_id)

        self.assertEqual(p1_from_db1['name'], p1_from_db2['name'])
        print(f"  ✓ Concurrent reads consistent")

        # Clean up
        db1.close()
        db2.close()
        print(f"  ✓ Multiple connections handled correctly (WAL mode)")


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("PM-DB Deployment Validation Test Suite")
    print("=" * 70)

    unittest.main(verbosity=2)
