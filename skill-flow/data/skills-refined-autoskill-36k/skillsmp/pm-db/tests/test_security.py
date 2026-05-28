#!/usr/bin/env python3
"""
Security Tests for PM-DB System

Tests security controls identified in SECURITY_AUDIT.md:
- SQL injection prevention
- Path traversal prevention
- Command injection prevention
- Input validation
- Output sanitization

Usage:
    python3 skills/pm-db/tests/test_security.py
"""

import unittest
import tempfile
import json
from pathlib import Path
import sys

# Add lib to path
lib_path = Path(__file__).parent.parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

from project_database import ProjectDatabase


class TestSQLInjectionPrevention(unittest.TestCase):
    """Test SQL injection attack prevention"""

    def setUp(self):
        """Create temporary database"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()

        self.db = ProjectDatabase(db_path=self.db_path)

        # Run migrations
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                self.db.conn.executescript(f.read())

    def tearDown(self):
        """Clean up"""
        self.db.close()
        Path(self.db_path).unlink(missing_ok=True)

    def test_sql_injection_in_project_name(self):
        """Test SQL injection via project name is prevented"""
        malicious_names = [
            "'; DROP TABLE projects; --",
            "' OR '1'='1",
            "admin'--",
            "' UNION SELECT * FROM projects--",
        ]

        for i, malicious_name in enumerate(malicious_names):
            # Should create project with literal name, not execute SQL
            project_id = self.db.create_project(malicious_name, "Test", f"/tmp/test{i}")
            self.assertIsNotNone(project_id)

            # Verify project was created with literal name
            project = self.db.get_project(project_id)
            self.assertEqual(project['name'], malicious_name)

        # Verify projects table still exists (wasn't dropped)
        projects = self.db.list_projects()
        self.assertEqual(len(projects), len(malicious_names))

    def test_sql_injection_in_job_name(self):
        """Test SQL injection via job name is prevented"""
        project_id = self.db.create_project("test", "Test", "/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")

        malicious_name = "'; DELETE FROM jobs; --"

        job_id = self.db.create_job(spec_id, malicious_name)
        job = self.db.get_job(job_id)

        # Verify job was created with literal name
        self.assertEqual(job['name'], malicious_name)

        # Verify jobs table still has data
        jobs = self.db.list_jobs()
        self.assertEqual(len(jobs), 1)

    def test_sql_injection_in_search_pattern(self):
        """Test SQL injection via search patterns is prevented"""
        project_id = self.db.create_project("test", "Test", "/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")
        job_id = self.db.create_job(spec_id, "Test Job")

        # Log some executions
        self.db.log_execution(job_id, None, "pytest tests/", "All passed", 0, 100)

        # Try SQL injection via search pattern
        malicious_patterns = [
            "%'; DROP TABLE execution_logs; --",
            "' OR 1=1; --",
        ]

        for pattern in malicious_patterns:
            # Should treat as literal search pattern
            results = self.db.search_execution_logs(command_pattern=pattern)
            # Should find nothing (no matching command)
            self.assertEqual(len(results), 0)

        # Verify execution_logs table still exists
        all_logs = self.db.get_execution_logs()
        self.assertEqual(len(all_logs), 1)


class TestPathTraversalPrevention(unittest.TestCase):
    """Test path traversal attack prevention"""

    def setUp(self):
        """Create temporary database"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()

        self.db = ProjectDatabase(db_path=self.db_path)

        # Run migrations
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                self.db.conn.executescript(f.read())

    def tearDown(self):
        """Clean up"""
        self.db.close()
        Path(self.db_path).unlink(missing_ok=True)

    def test_relative_path_rejected(self):
        """Test relative paths are rejected"""
        malicious_paths = [
            "../../../etc/passwd",
            "../../.ssh/authorized_keys",
            "./local/path",
            "relative/path",
        ]

        for path in malicious_paths:
            with self.assertRaises(ValueError) as cm:
                self.db.create_project("test", "Test", path)

            self.assertIn("absolute path", str(cm.exception))

    def test_absolute_path_accepted(self):
        """Test absolute paths are accepted"""
        valid_paths = [
            "/home/user/project",
            "/tmp/test-project",
            str(Path.home() / "applications" / "my-app"),
        ]

        for i, path in enumerate(valid_paths):
            project_id = self.db.create_project(f"test{i}", "Test", path)
            project = self.db.get_project(project_id)
            self.assertEqual(project['filesystem_path'], path)

    def test_empty_path_rejected(self):
        """Test empty/None filesystem_path is rejected (NOT NULL constraint)"""
        # filesystem_path is required for per-project Memory Bank exports
        import sqlite3

        with self.assertRaises(sqlite3.IntegrityError):
            self.db.create_project("test", "Test", None)


class TestInputValidation(unittest.TestCase):
    """Test input validation on all user inputs"""

    def setUp(self):
        """Create temporary database"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()

        self.db = ProjectDatabase(db_path=self.db_path)

        # Run migrations
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                self.db.conn.executescript(f.read())

    def tearDown(self):
        """Clean up"""
        self.db.close()
        Path(self.db_path).unlink(missing_ok=True)

    def test_empty_project_name_rejected(self):
        """Test empty project name is rejected"""
        invalid_names = ["", "   ", "\t", "\n"]

        for name in invalid_names:
            with self.assertRaises(ValueError) as cm:
                self.db.create_project(name)

            self.assertIn("cannot be empty", str(cm.exception))

    def test_invalid_status_rejected(self):
        """Test invalid status enum is rejected"""
        project_id = self.db.create_project("test", "Test", "/tmp/test")

        invalid_statuses = ["invalid", "random", "DRAFT", "Draft"]

        for status in invalid_statuses:
            with self.assertRaises(ValueError) as cm:
                self.db.create_spec(project_id, "spec", status=status)

            self.assertIn("must be one of", str(cm.exception))

    def test_invalid_priority_rejected(self):
        """Test invalid priority enum is rejected"""
        project_id = self.db.create_project("test", "Test", "/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")

        invalid_priorities = ["urgent", "CRITICAL", "p1", "1"]

        for priority in invalid_priorities:
            with self.assertRaises(ValueError) as cm:
                self.db.create_job(spec_id, "Test Job", priority=priority)

            self.assertIn("must be one of", str(cm.exception))

    def test_invalid_verdict_rejected(self):
        """Test invalid code review verdict is rejected"""
        project_id = self.db.create_project("test", "Test", "/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")
        job_id = self.db.create_job(spec_id, "Test Job")

        invalid_verdicts = ["accepted", "APPROVED", "rejected_lowercase"]

        for verdict in invalid_verdicts:
            with self.assertRaises(ValueError) as cm:
                self.db.add_code_review(
                    job_id, None, "reviewer", "summary", verdict
                )

            self.assertIn("must be one of", str(cm.exception))

    def test_empty_command_rejected(self):
        """Test empty command in log_execution is rejected"""
        project_id = self.db.create_project("test", "Test", "/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")
        job_id = self.db.create_job(spec_id, "Test Job")

        invalid_commands = ["", "   ", "\t"]

        for command in invalid_commands:
            with self.assertRaises(ValueError) as cm:
                self.db.log_execution(job_id, None, command)

            self.assertIn("cannot be empty", str(cm.exception))

    def test_whitespace_trimmed(self):
        """Test whitespace is trimmed from inputs"""
        # Project name with whitespace
        project_id = self.db.create_project("  test  ", "Test", "/tmp/test")
        project = self.db.get_project(project_id)
        self.assertEqual(project['name'], "test")

        # Job name with whitespace
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")
        job_id = self.db.create_job(spec_id, "  Test Job  ")
        job = self.db.get_job(job_id)
        self.assertEqual(job['name'], "Test Job")


class TestOutputSanitization(unittest.TestCase):
    """Test output sanitization and truncation"""

    def setUp(self):
        """Create temporary database"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()

        self.db = ProjectDatabase(db_path=self.db_path)

        # Run migrations
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                self.db.conn.executescript(f.read())

        # Create test data
        self.project_id = self.db.create_project("test", "Test", "/tmp/test")
        self.spec_id = self.db.create_spec(self.project_id, "spec", frd_content="# FRD")
        self.job_id = self.db.create_job(self.spec_id, "Test Job")

    def tearDown(self):
        """Clean up"""
        self.db.close()
        Path(self.db_path).unlink(missing_ok=True)

    def test_large_output_truncated(self):
        """Test output larger than 50KB is truncated"""
        # Create output larger than 50KB
        large_output = "x" * 60000  # 60KB

        log_id = self.db.log_execution(
            self.job_id, None, "test command", large_output
        )

        # Verify output was truncated
        logs = self.db.get_execution_logs(job_id=self.job_id)
        stored_output = logs[0]['output']

        self.assertLess(len(stored_output), len(large_output))
        self.assertIn("truncated", stored_output)
        self.assertEqual(len(stored_output), 50000 + len("\n... (truncated)"))

    def test_normal_output_not_truncated(self):
        """Test output under 50KB is not truncated"""
        normal_output = "Test output\nLine 2\nLine 3"

        log_id = self.db.log_execution(
            self.job_id, None, "test command", normal_output
        )

        logs = self.db.get_execution_logs(job_id=self.job_id)
        stored_output = logs[0]['output']

        self.assertEqual(stored_output, normal_output)
        self.assertNotIn("truncated", stored_output)


class TestDatabaseConstraints(unittest.TestCase):
    """Test database-level security constraints"""

    def setUp(self):
        """Create temporary database"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()

        self.db = ProjectDatabase(db_path=self.db_path)

        # Run migrations
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                self.db.conn.executescript(f.read())

    def tearDown(self):
        """Clean up"""
        self.db.close()
        Path(self.db_path).unlink(missing_ok=True)

    def test_unique_project_name_enforced(self):
        """Test UNIQUE constraint on project name"""
        import sqlite3

        # Create first project
        self.db.create_project("test", "Test", "/tmp/test")

        # Try to create duplicate
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.create_project("test", "Test 2", "/tmp/test2")

    def test_foreign_key_constraint_enforced(self):
        """Test foreign key constraints are enforced"""
        import sqlite3

        # Try to create spec with non-existent project_id
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.create_spec(
                project_id=99999,
                name="spec",
                frd_content="# FRD"
            )

        # Try to create job with non-existent spec_id
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.create_job(
                spec_id=99999,
                name="job"
            )

    def test_cascade_delete_works(self):
        """Test CASCADE DELETE behavior for specs, SET NULL for jobs"""
        project_id = self.db.create_project("test", "Test", "/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")
        job_id = self.db.create_job(spec_id, "job")

        # Verify job and spec exist
        self.assertIsNotNone(self.db.get_job(job_id))
        self.assertIsNotNone(self.db.get_spec(spec_id))

        # Delete project (should cascade to spec, SET NULL for job.spec_id)
        self.db.conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        self.db.conn.commit()

        # Verify spec was deleted (CASCADE)
        self.assertIsNone(self.db.get_spec(spec_id))

        # Verify job still exists but spec_id is NULL (SET NULL)
        job = self.db.get_job(job_id)
        self.assertIsNotNone(job)
        self.assertIsNone(job['spec_id'])  # Foreign key SET NULL


class TestErrorHandling(unittest.TestCase):
    """Test error handling doesn't leak sensitive information"""

    def setUp(self):
        """Create temporary database"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()

        self.db = ProjectDatabase(db_path=self.db_path)

        # Run migrations
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                self.db.conn.executescript(f.read())

    def tearDown(self):
        """Clean up"""
        self.db.close()
        Path(self.db_path).unlink(missing_ok=True)

    def test_error_messages_not_verbose(self):
        """Test error messages don't reveal internal details"""
        # Empty name error
        try:
            self.db.create_project("")
        except ValueError as e:
            error_msg = str(e)
            # Should not contain SQL, internal paths, etc.
            self.assertNotIn("SELECT", error_msg)
            self.assertNotIn("INSERT", error_msg)
            self.assertNotIn(self.db_path, error_msg)

        # Invalid path error
        try:
            self.db.create_project("test", "Test", "./relative")
        except ValueError as e:
            error_msg = str(e)
            # Should be descriptive but not reveal internals
            self.assertIn("absolute path", error_msg)
            self.assertNotIn("Path(", error_msg)


if __name__ == '__main__':
    # Run with verbose output
    unittest.main(verbosity=2)
