#!/usr/bin/env python3
"""
Integration Tests for PM-DB System

Tests end-to-end workflows including hooks, scripts, and database interactions.

Usage:
    python3 skills/pm-db/tests/test_integration.py
"""

import unittest
import tempfile
import json
import subprocess
from pathlib import Path
import sys
import shutil

# Add lib to path
lib_path = Path(__file__).parent.parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

from project_database import ProjectDatabase


class TestHookIntegration(unittest.TestCase):
    """Test hook execution and database integration"""

    def setUp(self):
        """Set up test environment"""
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

        # Create test project
        self.project_id = self.db.create_project(
            "test-integration",
            "Integration test project",
            "/tmp/test-integration"
        )
        self.spec_id = self.db.create_spec(
            self.project_id,
            "test-spec",
            frd_content="# Test FRD"
        )

    def tearDown(self):
        """Clean up"""
        self.db.close()
        Path(self.db_path).unlink(missing_ok=True)

    def test_on_job_start_hook(self):
        """Test on-job-start hook creates and starts job"""
        hook_path = Path(__file__).parent.parent.parent / "hooks/pm-db/on-job-start.py"

        if not hook_path.exists():
            self.skipTest("Hook not found")

        # Prepare hook input
        hook_input = {
            "spec_id": self.spec_id,
            "job_name": "Integration Test Job",
            "priority": "high",
            "assigned_agent": "test-agent",
            "session_id": "test-session"
        }

        # Set environment variable for database path
        env = {"CLAUDE_DB_PATH": self.db_path}

        # Run hook
        result = subprocess.run(
            ["python3", str(hook_path)],
            input=json.dumps(hook_input),
            capture_output=True,
            text=True,
            env={**dict(subprocess.os.environ), **env}
        )

        # Check hook succeeded
        self.assertEqual(result.returncode, 0, f"Hook failed: {result.stderr}")

        # Parse output
        output = json.loads(result.stdout)
        self.assertEqual(output['status'], 'created')
        self.assertIn('job_id', output)

        # Verify job in database
        job = self.db.get_job(output['job_id'])
        self.assertIsNotNone(job)
        self.assertEqual(job['name'], "Integration Test Job")
        self.assertEqual(job['status'], 'in-progress')

    def test_on_task_start_hook(self):
        """Test on-task-start hook creates and starts task"""
        # Create a job first
        job_id = self.db.create_job(self.spec_id, "Test Job")

        hook_path = Path(__file__).parent.parent.parent / "hooks/pm-db/on-task-start.py"

        if not hook_path.exists():
            self.skipTest("Hook not found")

        # Prepare hook input
        hook_input = {
            "job_id": job_id,
            "task_name": "Integration Test Task",
            "order": 1
        }

        # Run hook
        result = subprocess.run(
            ["python3", str(hook_path)],
            input=json.dumps(hook_input),
            capture_output=True,
            text=True,
            env={"CLAUDE_DB_PATH": self.db_path}
        )

        self.assertEqual(result.returncode, 0)

        # Parse output
        output = json.loads(result.stdout)
        self.assertEqual(output['status'], 'created')

        # Verify task
        tasks = self.db.get_tasks(job_id)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['name'], "Integration Test Task")
        self.assertEqual(tasks[0]['status'], 'in-progress')

    def test_on_tool_use_hook(self):
        """Test on-tool-use hook logs execution"""
        # Create job first
        job_id = self.db.create_job(self.spec_id, "Test Job")

        hook_path = Path(__file__).parent.parent.parent / "hooks/pm-db/on-tool-use.py"

        if not hook_path.exists():
            self.skipTest("Hook not found")

        # Prepare hook input
        hook_input = {
            "job_id": job_id,
            "command": "pytest tests/",
            "output": "All tests passed",
            "exit_code": 0,
            "duration_ms": 1500
        }

        # Run hook
        result = subprocess.run(
            ["python3", str(hook_path)],
            input=json.dumps(hook_input),
            capture_output=True,
            text=True,
            env={"CLAUDE_DB_PATH": self.db_path}
        )

        self.assertEqual(result.returncode, 0)

        # Verify log
        logs = self.db.get_execution_logs(job_id=job_id)
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]['command'], "pytest tests/")


class TestDatabaseOperations(unittest.TestCase):
    """Test database operations and data integrity"""

    def setUp(self):
        """Set up test environment"""
        # Create temporary database
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()

        # Initialize database manually
        db = ProjectDatabase(db_path=self.db_path)
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                db.conn.executescript(f.read())
        db.close()

    def tearDown(self):
        """Clean up"""
        Path(self.db_path).unlink(missing_ok=True)

    def test_dashboard_data_integrity(self):
        """Test dashboard generation with real data"""
        with ProjectDatabase(db_path=self.db_path) as db:
            # Create test data
            project_id = db.create_project("test", "Test", "/tmp/test")
            spec_id = db.create_spec(project_id, "spec", frd_content="# FRD")

            job1_id = db.create_job(spec_id, "Active Job", priority="high")
            db.start_job(job1_id)

            job2_id = db.create_job(spec_id, "Completed Job", priority="normal")
            db.start_job(job2_id)
            db.complete_job(job2_id, exit_code=0)

            # Generate dashboard
            dashboard = db.generate_dashboard()

            # Verify structure
            self.assertIn('active_jobs', dashboard)
            self.assertIn('pending_jobs', dashboard)
            self.assertIn('recent_completions', dashboard)
            self.assertIn('velocity', dashboard)

            # Verify data
            self.assertEqual(len(dashboard['active_jobs']), 1)
            self.assertEqual(len(dashboard['recent_completions']), 1)
            self.assertEqual(dashboard['velocity']['this_week'], 1)

    def test_execution_log_search_integration(self):
        """Test execution log search with various filters"""
        with ProjectDatabase(db_path=self.db_path) as db:
            project_id = db.create_project("test", "Test", "/tmp/test")
            spec_id = db.create_spec(project_id, "spec", frd_content="# FRD")
            job_id = db.create_job(spec_id, "Test Job")

            # Add varied execution logs
            db.log_execution(job_id, None, "pytest tests/", "All passed", 0, 1000)
            db.log_execution(job_id, None, "npm run build", "Build error", 1, 2000)
            db.log_execution(job_id, None, "git status", "clean", 0, 100)

            # Test command pattern search
            pytest_logs = db.search_execution_logs(command_pattern="%pytest%")
            self.assertEqual(len(pytest_logs), 1)
            self.assertIn("pytest", pytest_logs[0]['command'])

            # Test output pattern search
            error_logs = db.search_execution_logs(output_pattern="%error%")
            self.assertEqual(len(error_logs), 1)

            # Test exit code filter
            failed = db.search_execution_logs(exit_code=1)
            self.assertEqual(len(failed), 1)
            self.assertEqual(failed[0]['exit_code'], 1)

    def test_code_review_metrics_integration(self):
        """Test code review metrics with real data"""
        with ProjectDatabase(db_path=self.db_path) as db:
            project_id = db.create_project("test", "Test", "/tmp/test")
            spec_id = db.create_spec(project_id, "spec", frd_content="# FRD")
            job_id = db.create_job(spec_id, "Test Job")

            # Add multiple reviews
            db.add_code_review(job_id, None, "alice", "Good", "approved")
            db.add_code_review(job_id, None, "bob", "Issues", "changes-requested",
                              issues_found=json.dumps(["Missing tests", "Type error"]))
            db.add_code_review(job_id, None, "alice", "Better", "approved")

            # Get metrics
            metrics = db.get_code_review_metrics(job_id=job_id)

            # Verify aggregations
            self.assertEqual(metrics['total_reviews'], 3)
            self.assertEqual(metrics['verdict_distribution']['approved'], 2)
            self.assertEqual(metrics['verdict_distribution']['changes-requested'], 1)

            # Verify reviewer activity
            self.assertEqual(len(metrics['reviewer_activity']), 2)
            alice_activity = next(r for r in metrics['reviewer_activity'] if r['reviewer'] == 'alice')
            self.assertEqual(alice_activity['review_count'], 2)


class TestEndToEndWorkflow(unittest.TestCase):
    """Test complete end-to-end workflows"""

    def setUp(self):
        """Set up test environment"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()

        # Initialize database manually
        db = ProjectDatabase(db_path=self.db_path)
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                db.conn.executescript(f.read())
        db.close()

    def tearDown(self):
        """Clean up"""
        Path(self.db_path).unlink(missing_ok=True)

    def test_complete_job_lifecycle(self):
        """Test full job lifecycle with hooks"""
        with ProjectDatabase(db_path=self.db_path) as db:
            # Create project and spec
            project_id = db.create_project("test", "Test", "/tmp/test")
            spec_id = db.create_spec(project_id, "spec", frd_content="# FRD")

            # Create job
            job_id = db.create_job(spec_id, "Full Lifecycle Job")
            self.assertEqual(db.get_job(job_id)['status'], 'pending')

            # Start job
            db.start_job(job_id)
            job = db.get_job(job_id)
            self.assertEqual(job['status'], 'in-progress')
            self.assertIsNotNone(job['started_at'])

            # Create tasks
            task1_id = db.create_task(job_id, "Task 1", order=1)
            task2_id = db.create_task(job_id, "Task 2", order=2)

            # Execute tasks
            db.start_task(task1_id)
            db.log_execution(job_id, task1_id, "command1", "output1", 0, 100)
            db.complete_task(task1_id, exit_code=0)

            db.start_task(task2_id)
            db.log_execution(job_id, task2_id, "command2", "output2", 0, 200)
            db.complete_task(task2_id, exit_code=0)

            # Add code review
            db.add_code_review(
                job_id, None, "reviewer", "Looks good", "approved",
                issues_found=json.dumps([]),
                files_reviewed=json.dumps(["file.py"])
            )

            # Complete job
            db.complete_job(job_id, exit_code=0)
            job = db.get_job(job_id)
            self.assertEqual(job['status'], 'completed')
            self.assertIsNotNone(job['completed_at'])
            # Duration may be 0 if completed immediately
            self.assertGreaterEqual(job['duration_seconds'], 0)

            # Verify timeline
            timeline = db.get_job_timeline(job_id)
            event_types = [e['type'] for e in timeline]
            self.assertIn('job_created', event_types)
            self.assertIn('job_started', event_types)
            self.assertIn('job_completed', event_types)
            self.assertIn('task_created', event_types)
            self.assertIn('code_review', event_types)

            # Verify metrics
            metrics = db.get_code_review_metrics(job_id=job_id)
            self.assertEqual(metrics['total_reviews'], 1)
            self.assertEqual(metrics['verdict_distribution']['approved'], 1)

            # Verify logs
            logs = db.get_execution_logs(job_id=job_id)
            self.assertEqual(len(logs), 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
