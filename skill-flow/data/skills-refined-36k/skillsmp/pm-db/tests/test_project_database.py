#!/usr/bin/env python3
"""
Unit Tests for ProjectDatabase

Tests all core functionality of the ProjectDatabase class.

Usage:
    python3 skills/pm-db/tests/test_project_database.py
    python3 -m unittest skills/pm-db/tests/test_project_database.py
"""

import unittest
import tempfile
import sqlite3
import json
from pathlib import Path
from datetime import datetime
import sys

# Add lib to path
lib_path = Path(__file__).parent.parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

from project_database import ProjectDatabase


class TestProjectDatabase(unittest.TestCase):
    """Test ProjectDatabase class"""

    def setUp(self):
        """Set up test database before each test"""
        # Create temporary database
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()

        # Initialize database
        self.db = ProjectDatabase(db_path=self.db_path)

        # Run migrations
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                self.db.conn.executescript(f.read())

    def tearDown(self):
        """Clean up after each test"""
        self.db.close()
        Path(self.db_path).unlink(missing_ok=True)

    # ==================== PROJECT TESTS ====================

    def test_create_project(self):
        """Test creating a project"""
        project_id = self.db.create_project(
            name="test-project",
            description="Test description",
            filesystem_path="/tmp/test"
        )

        self.assertIsInstance(project_id, int)
        self.assertGreater(project_id, 0)

        # Verify project was created
        project = self.db.get_project(project_id)
        self.assertEqual(project['name'], "test-project")
        self.assertEqual(project['description'], "Test description")
        self.assertEqual(project['filesystem_path'], "/tmp/test")

    def test_create_project_duplicate_name(self):
        """Test creating project with duplicate name fails"""
        self.db.create_project("test", filesystem_path="/tmp/test")

        with self.assertRaises(sqlite3.IntegrityError):
            self.db.create_project("test", filesystem_path="/tmp/test2")

    def test_create_project_relative_path(self):
        """Test creating project with relative path fails"""
        with self.assertRaises(ValueError):
            self.db.create_project("test", filesystem_path="relative/path")

    def test_get_project(self):
        """Test getting a project by ID"""
        project_id = self.db.create_project("test", filesystem_path="/tmp/test")
        project = self.db.get_project(project_id)

        self.assertIsNotNone(project)
        self.assertEqual(project['id'], project_id)
        self.assertEqual(project['name'], "test")

    def test_get_project_nonexistent(self):
        """Test getting nonexistent project returns None"""
        project = self.db.get_project(999999)
        self.assertIsNone(project)

    def test_get_project_by_name(self):
        """Test getting project by name"""
        self.db.create_project("my-project", filesystem_path="/tmp/test")
        project = self.db.get_project_by_name("my-project")

        self.assertIsNotNone(project)
        self.assertEqual(project['name'], "my-project")

    def test_list_projects(self):
        """Test listing all projects"""
        self.db.create_project("project1", filesystem_path="/tmp/p1")
        self.db.create_project("project2", filesystem_path="/tmp/p2")

        projects = self.db.list_projects()
        self.assertEqual(len(projects), 2)
        # Projects are ordered by created_at DESC (most recent first)
        self.assertEqual(projects[0]['name'], "project2")
        self.assertEqual(projects[1]['name'], "project1")

    # ==================== SPEC TESTS ====================

    def test_create_spec(self):
        """Test creating a specification"""
        project_id = self.db.create_project("test", filesystem_path="/tmp/test")
        spec_id = self.db.create_spec(
            project_id=project_id,
            name="test-spec",
            frd_content="# FRD",
            frs_content="# FRS",
            gs_content="# GS",
            tr_content="# TR",
            task_list_content="# Tasks"
        )

        self.assertIsInstance(spec_id, int)
        self.assertGreater(spec_id, 0)

        # Verify spec
        spec = self.db.get_spec(spec_id)
        self.assertEqual(spec['name'], "test-spec")
        self.assertEqual(spec['frd_content'], "# FRD")

    def test_list_specs(self):
        """Test listing specs for a project"""
        project_id = self.db.create_project("test", filesystem_path="/tmp/test")
        self.db.create_spec(project_id, "spec1", frd_content="# FRD1")
        self.db.create_spec(project_id, "spec2", frd_content="# FRD2")

        specs = self.db.list_specs(project_id=project_id)
        self.assertEqual(len(specs), 2)

    # ==================== JOB TESTS ====================

    def test_create_job(self):
        """Test creating a job"""
        project_id = self.db.create_project("test", filesystem_path="/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")

        job_id = self.db.create_job(
            spec_id=spec_id,
            name="Test Job",
            priority="high",
            assigned_agent="test-agent"
        )

        self.assertIsInstance(job_id, int)

        # Verify job
        job = self.db.get_job(job_id)
        self.assertEqual(job['name'], "Test Job")
        self.assertEqual(job['priority'], "high")
        self.assertEqual(job['status'], "pending")

    def test_start_job(self):
        """Test starting a job"""
        project_id = self.db.create_project("test", filesystem_path="/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")
        job_id = self.db.create_job(spec_id, "Test Job")

        self.db.start_job(job_id)

        job = self.db.get_job(job_id)
        self.assertEqual(job['status'], 'in-progress')
        self.assertIsNotNone(job['started_at'])

    def test_complete_job(self):
        """Test completing a job"""
        project_id = self.db.create_project("test", filesystem_path="/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")
        job_id = self.db.create_job(spec_id, "Test Job")

        self.db.start_job(job_id)
        self.db.complete_job(job_id, exit_code=0)

        job = self.db.get_job(job_id)
        self.assertEqual(job['status'], 'completed')
        self.assertIsNotNone(job['completed_at'])
        self.assertIsNotNone(job['duration_seconds'])

    def test_fail_job(self):
        """Test failing a job"""
        project_id = self.db.create_project("test", filesystem_path="/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")
        job_id = self.db.create_job(spec_id, "Test Job")

        self.db.start_job(job_id)
        self.db.complete_job(job_id, exit_code=1)

        job = self.db.get_job(job_id)
        self.assertEqual(job['status'], 'failed')

    def test_list_jobs(self):
        """Test listing jobs with filters"""
        project_id = self.db.create_project("test", filesystem_path="/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")

        job1_id = self.db.create_job(spec_id, "Job 1")
        job2_id = self.db.create_job(spec_id, "Job 2")
        self.db.start_job(job2_id)

        # List pending jobs
        pending = self.db.list_jobs(status='pending')
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0]['id'], job1_id)

        # List in-progress jobs
        in_progress = self.db.list_jobs(status='in-progress')
        self.assertEqual(len(in_progress), 1)
        self.assertEqual(in_progress[0]['id'], job2_id)

    # ==================== TASK TESTS ====================

    def test_create_task(self):
        """Test creating a task"""
        project_id = self.db.create_project("test", filesystem_path="/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")
        job_id = self.db.create_job(spec_id, "Job")

        task_id = self.db.create_task(
            job_id=job_id,
            name="Test Task",
            order=1
        )

        self.assertIsInstance(task_id, int)

        # Verify task
        task = self.db.get_task(task_id)
        self.assertEqual(task['name'], "Test Task")
        self.assertEqual(task['order'], 1)
        self.assertEqual(task['status'], 'pending')

    def test_start_task(self):
        """Test starting a task"""
        project_id = self.db.create_project("test", filesystem_path="/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")
        job_id = self.db.create_job(spec_id, "Job")
        task_id = self.db.create_task(job_id, "Task", order=1)

        self.db.start_task(task_id)

        task = self.db.get_task(task_id)
        self.assertEqual(task['status'], 'in-progress')
        self.assertIsNotNone(task['started_at'])

    def test_complete_task(self):
        """Test completing a task"""
        project_id = self.db.create_project("test", filesystem_path="/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")
        job_id = self.db.create_job(spec_id, "Job")
        task_id = self.db.create_task(job_id, "Task", order=1)

        self.db.start_task(task_id)
        self.db.complete_task(task_id, exit_code=0)

        task = self.db.get_task(task_id)
        self.assertEqual(task['status'], 'completed')
        self.assertIsNotNone(task['completed_at'])

    def test_get_tasks(self):
        """Test getting tasks for a job"""
        project_id = self.db.create_project("test", filesystem_path="/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")
        job_id = self.db.create_job(spec_id, "Job")

        self.db.create_task(job_id, "Task 1", order=1)
        self.db.create_task(job_id, "Task 2", order=2)

        tasks = self.db.get_tasks(job_id)
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0]['order'], 1)

    # ==================== CODE REVIEW TESTS ====================

    def test_add_code_review(self):
        """Test adding a code review"""
        project_id = self.db.create_project("test", filesystem_path="/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")
        job_id = self.db.create_job(spec_id, "Job")

        review_id = self.db.add_code_review(
            job_id=job_id,
            task_id=None,
            reviewer="alice",
            summary="Good code",
            verdict="approved",
            issues_found=json.dumps([]),
            files_reviewed=json.dumps(["file.py"])
        )

        self.assertIsInstance(review_id, int)

        # Verify review
        reviews = self.db.get_code_reviews(job_id=job_id)
        self.assertEqual(len(reviews), 1)
        self.assertEqual(reviews[0]['verdict'], 'approved')

    def test_get_code_reviews(self):
        """Test getting code reviews"""
        project_id = self.db.create_project("test", filesystem_path="/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")
        job_id = self.db.create_job(spec_id, "Job")

        self.db.add_code_review(job_id, None, "alice", "Review 1", "approved")
        self.db.add_code_review(job_id, None, "bob", "Review 2", "changes-requested")

        reviews = self.db.get_code_reviews(job_id=job_id)
        self.assertEqual(len(reviews), 2)

    # ==================== EXECUTION LOG TESTS ====================

    def test_log_execution(self):
        """Test logging command execution"""
        project_id = self.db.create_project("test", filesystem_path="/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")
        job_id = self.db.create_job(spec_id, "Job")

        log_id = self.db.log_execution(
            job_id=job_id,
            task_id=None,
            command="pytest tests/",
            output="All tests passed",
            exit_code=0,
            duration_ms=1500
        )

        self.assertIsInstance(log_id, int)

        # Verify log
        logs = self.db.get_execution_logs(job_id=job_id)
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]['command'], "pytest tests/")

    def test_log_execution_output_truncation(self):
        """Test that large output is truncated"""
        project_id = self.db.create_project("test", filesystem_path="/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")
        job_id = self.db.create_job(spec_id, "Job")

        # Create output larger than 50KB
        large_output = "x" * 60000

        self.db.log_execution(
            job_id=job_id,
            task_id=None,
            command="test",
            output=large_output
        )

        logs = self.db.get_execution_logs(job_id=job_id)
        self.assertLess(len(logs[0]['output']), 51000)
        self.assertIn("(truncated)", logs[0]['output'])

    # ==================== AGENT ASSIGNMENT TESTS ====================

    def test_assign_agent(self):
        """Test assigning agent to job"""
        project_id = self.db.create_project("test", filesystem_path="/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")
        job_id = self.db.create_job(spec_id, "Job")

        assignment_id = self.db.assign_agent(
            agent_type="code-reviewer",
            job_id=job_id,
            task_id=None
        )

        self.assertIsInstance(assignment_id, int)

        # Verify assignment
        assignments = self.db.get_agent_assignments(job_id=job_id)
        self.assertEqual(len(assignments), 1)
        self.assertEqual(assignments[0]['agent_type'], 'code-reviewer')

    # ==================== REPORTING TESTS ====================

    def test_generate_dashboard(self):
        """Test dashboard generation"""
        project_id = self.db.create_project("test", filesystem_path="/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")

        # Create some jobs
        job1 = self.db.create_job(spec_id, "Job 1")
        job2 = self.db.create_job(spec_id, "Job 2")
        self.db.start_job(job2)

        dashboard = self.db.generate_dashboard()

        self.assertIn('active_jobs', dashboard)
        self.assertIn('pending_jobs', dashboard)
        self.assertIn('recent_completions', dashboard)
        self.assertIn('velocity', dashboard)

        self.assertEqual(len(dashboard['pending_jobs']), 1)
        self.assertEqual(len(dashboard['active_jobs']), 1)

    def test_get_job_timeline(self):
        """Test job timeline generation"""
        project_id = self.db.create_project("test", filesystem_path="/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")
        job_id = self.db.create_job(spec_id, "Job")
        self.db.start_job(job_id)

        timeline = self.db.get_job_timeline(job_id)

        self.assertIsInstance(timeline, list)
        self.assertGreater(len(timeline), 0)
        self.assertIn('type', timeline[0])
        self.assertIn('timestamp', timeline[0])

    def test_search_execution_logs(self):
        """Test execution log search"""
        project_id = self.db.create_project("test", filesystem_path="/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")
        job_id = self.db.create_job(spec_id, "Job")

        # Add some logs
        self.db.log_execution(job_id, None, "pytest", "pass", 0, 1000)
        self.db.log_execution(job_id, None, "npm build", "error", 1, 2000)

        # Search by exit code
        failed = self.db.search_execution_logs(exit_code=1)
        self.assertEqual(len(failed), 1)
        self.assertIn("npm", failed[0]['command'])

        # Search by command pattern
        pytest_logs = self.db.search_execution_logs(command_pattern="%pytest%")
        self.assertEqual(len(pytest_logs), 1)

    def test_get_code_review_metrics(self):
        """Test code review metrics aggregation"""
        project_id = self.db.create_project("test", filesystem_path="/tmp/test")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")
        job_id = self.db.create_job(spec_id, "Job")

        # Add reviews
        self.db.add_code_review(job_id, None, "alice", "Good", "approved")
        self.db.add_code_review(job_id, None, "bob", "Issues", "changes-requested",
                               issues_found=json.dumps(["Missing tests", "Type error"]))

        metrics = self.db.get_code_review_metrics(job_id=job_id)

        self.assertEqual(metrics['total_reviews'], 2)
        self.assertIn('approved', metrics['verdict_distribution'])
        self.assertGreater(metrics['avg_issues_per_review'], 0)
        self.assertEqual(len(metrics['reviewer_activity']), 2)

    # ==================== CONTEXT MANAGER TESTS ====================

    def test_context_manager(self):
        """Test using ProjectDatabase as context manager"""
        with ProjectDatabase(db_path=self.db_path) as db:
            project_id = db.create_project("test", filesystem_path="/tmp/test")
            self.assertIsInstance(project_id, int)

        # Connection should be closed
        # (Can't easily test without accessing private attributes)


class TestDatabaseMigrations(unittest.TestCase):
    """Test database migrations"""

    def test_migrations_exist(self):
        """Test that migration files exist"""
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        self.assertTrue(migrations_dir.exists())

        migration_files = list(migrations_dir.glob("*.sql"))
        self.assertGreaterEqual(len(migration_files), 3)

    def test_migration_order(self):
        """Test that migrations are numbered correctly"""
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        migration_files = sorted(migrations_dir.glob("*.sql"))

        for i, migration_file in enumerate(migration_files, start=1):
            self.assertTrue(migration_file.name.startswith(f"{i:03d}_"))


if __name__ == '__main__':
    unittest.main(verbosity=2)
