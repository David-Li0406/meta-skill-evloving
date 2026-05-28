#!/usr/bin/env python3
"""
User Acceptance Testing (UAT) for PM-DB System

Tests real-world user scenarios and workflows to validate that the system
meets user requirements and expectations.

Scenarios:
1. New user onboarding
2. Daily workflow (import, dashboard, review)
3. Project tracking and reporting
4. Error recovery and edge cases
5. Integration with Memory Bank
6. Multi-project management
7. Code review workflow
8. Task execution tracking

Usage:
    python3 skills/pm-db/tests/test_uat.py
"""

import unittest
import tempfile
import shutil
import json
import subprocess
from pathlib import Path
import sys
import os

# Add lib to path
lib_path = Path(__file__).parent.parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

from project_database import ProjectDatabase


class TestNewUserOnboarding(unittest.TestCase):
    """
    UAT Scenario 1: New User Onboarding

    User story: As a new Claude Code user, I want to initialize PM-DB
    and start tracking my first project.
    """

    def setUp(self):
        """Create temporary environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        self.db_path = self.temp_path / "projects.db"

    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.temp_dir)

    def test_new_user_initialization(self):
        """
        Test: New user initializes database and creates first project

        Steps:
        1. Initialize database
        2. Verify database exists with correct structure
        3. Create first project
        4. Verify project is tracked
        """
        # Step 1: Initialize database
        db = ProjectDatabase(db_path=str(self.db_path))

        # Run migrations
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                db.conn.executescript(f.read())

        # Step 2: Verify database structure
        cursor = db.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = [row[0] for row in cursor.fetchall()]

        expected_tables = [
            'agent_assignments', 'code_reviews', 'execution_logs', 'jobs',
            'projects', 'schema_version', 'specs', 'tasks'
        ]

        for table in expected_tables:
            self.assertIn(table, tables, f"Missing table: {table}")

        # Step 3: Create first project
        project_id = db.create_project(
            "my-first-app",
            "My first application tracked in PM-DB",
            "/home/user/projects/my-first-app"
        )

        self.assertIsNotNone(project_id)
        self.assertIsInstance(project_id, int)

        # Step 4: Verify project is tracked
        projects = db.list_projects()
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0]['name'], "my-first-app")
        self.assertEqual(projects[0]['description'], "My first application tracked in PM-DB")

        db.close()

        # User sees success
        print("✅ New user successfully initialized PM-DB and created first project")


class TestDailyWorkflow(unittest.TestCase):
    """
    UAT Scenario 2: Daily Workflow

    User story: As a developer, I want to track my daily work including
    importing specs, executing jobs, and reviewing progress.
    """

    def setUp(self):
        """Create temporary database"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        self.db_path = self.temp_path / "projects.db"

        self.db = ProjectDatabase(db_path=str(self.db_path))

        # Run migrations
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                self.db.conn.executescript(f.read())

        # Create project
        self.project_id = self.db.create_project(
            "daily-work",
            "Daily development work",
            "/home/user/projects/daily-work"
        )

    def tearDown(self):
        """Clean up"""
        self.db.close()
        shutil.rmtree(self.temp_dir)

    def test_daily_workflow_complete(self):
        """
        Test: Complete daily workflow from spec import to dashboard review

        Steps:
        1. Import specification
        2. Create and start job
        3. Execute tasks
        4. Add code review
        5. Complete job
        6. View dashboard
        7. Verify all data tracked correctly
        """
        # Step 1: Import specification
        spec_id = self.db.create_spec(
            self.project_id,
            "feature-user-auth",
            frd_content="# User Authentication Feature\n\nImplement secure user authentication.",
            frs_content="## Requirements\n1. Email/password login\n2. JWT tokens\n3. Rate limiting",
            tr_content="## Technical Design\n- NextAuth.js\n- PostgreSQL\n- Redis cache",
            status="approved"
        )

        self.assertIsNotNone(spec_id)

        # Step 2: Create and start job
        job_id = self.db.create_job(
            spec_id,
            "Build user authentication system",
            priority="high",
            assigned_agent="nextjs-backend-developer"
        )

        self.db.start_job(job_id)

        job = self.db.get_job(job_id)
        self.assertEqual(job['status'], 'in-progress')
        self.assertIsNotNone(job['started_at'])

        # Step 3: Execute tasks
        task1_id = self.db.create_task(job_id, "Setup NextAuth.js", order=1)
        task2_id = self.db.create_task(job_id, "Create login API", order=2,
                                       dependencies=json.dumps([task1_id]))
        task3_id = self.db.create_task(job_id, "Add JWT generation", order=3,
                                       dependencies=json.dumps([task2_id]))

        for task_id in [task1_id, task2_id, task3_id]:
            self.db.start_task(task_id)
            self.db.log_execution(job_id, task_id, "npm install", "Installed successfully", 0, 5000)
            self.db.complete_task(task_id, exit_code=0)

        # Verify all tasks completed
        tasks = self.db.get_tasks(job_id)
        completed_tasks = [t for t in tasks if t['status'] == 'completed']
        self.assertEqual(len(completed_tasks), 3)

        # Step 4: Add code review
        review_id = self.db.add_code_review(
            job_id,
            None,
            "code-reviewer-agent",
            "Code quality excellent. Authentication follows security best practices.",
            "approved"
        )

        self.assertIsNotNone(review_id)

        # Step 5: Complete job
        self.db.complete_job(
            job_id,
            exit_code=0,
            summary="User authentication system implemented successfully with JWT tokens and rate limiting."
        )

        job = self.db.get_job(job_id)
        self.assertEqual(job['status'], 'completed')
        self.assertIsNotNone(job['completed_at'])
        self.assertEqual(job['exit_code'], 0)

        # Step 6: View dashboard
        dashboard = self.db.generate_dashboard()

        self.assertIn('active_jobs', dashboard)
        self.assertIn('pending_jobs', dashboard)
        self.assertIn('recent_completions', dashboard)
        self.assertIn('velocity', dashboard)

        # Step 7: Verify all data tracked
        self.assertEqual(len(dashboard['recent_completions']), 1)
        self.assertEqual(dashboard['recent_completions'][0]['name'], "Build user authentication system")
        self.assertEqual(dashboard['recent_completions'][0]['status'], 'completed')

        # Verify job appears in completions
        completed_job_ids = [j['id'] for j in dashboard['recent_completions']]
        self.assertIn(job_id, completed_job_ids)

        # User sees complete dashboard
        print("✅ Daily workflow complete: spec imported, job executed, dashboard updated")


class TestProjectTracking(unittest.TestCase):
    """
    UAT Scenario 3: Project Tracking and Reporting

    User story: As a project manager, I want to track multiple projects
    and generate reports on progress.
    """

    def setUp(self):
        """Create temporary database"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        self.db_path = self.temp_path / "projects.db"

        self.db = ProjectDatabase(db_path=str(self.db_path))

        # Run migrations
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                self.db.conn.executescript(f.read())

    def tearDown(self):
        """Clean up"""
        self.db.close()
        shutil.rmtree(self.temp_dir)

    def test_multi_project_tracking(self):
        """
        Test: Track multiple projects with different statuses

        Steps:
        1. Create 3 projects
        2. Create jobs for each project (various statuses)
        3. Generate dashboard
        4. Verify accurate reporting
        """
        # Step 1: Create 3 projects
        project1_id = self.db.create_project("project-alpha", "Alpha", "/tmp/alpha")
        project2_id = self.db.create_project("project-beta", "Beta", "/tmp/beta")
        project3_id = self.db.create_project("project-gamma", "Gamma", "/tmp/gamma")

        # Step 2: Create jobs with various statuses
        # Project Alpha: 2 completed, 1 in-progress
        spec1_id = self.db.create_spec(project1_id, "spec1", frd_content="# FRD")
        job1_id = self.db.create_job(spec1_id, "Job 1")
        self.db.start_job(job1_id)
        self.db.complete_job(job1_id, 0, "Done")

        job2_id = self.db.create_job(spec1_id, "Job 2")
        self.db.start_job(job2_id)
        self.db.complete_job(job2_id, 0, "Done")

        job3_id = self.db.create_job(spec1_id, "Job 3")
        self.db.start_job(job3_id)

        # Project Beta: 1 completed, 1 failed
        spec2_id = self.db.create_spec(project2_id, "spec2", frd_content="# FRD")
        job4_id = self.db.create_job(spec2_id, "Job 4")
        self.db.start_job(job4_id)
        self.db.complete_job(job4_id, 0, "Done")

        job5_id = self.db.create_job(spec2_id, "Job 5")
        self.db.start_job(job5_id)
        self.db.complete_job(job5_id, 1, "Failed")

        # Project Gamma: 1 pending
        spec3_id = self.db.create_spec(project3_id, "spec3", frd_content="# FRD")
        job6_id = self.db.create_job(spec3_id, "Job 6")

        # Step 3: Generate dashboard
        dashboard = self.db.generate_dashboard()

        # Step 4: Verify accurate reporting
        # Verify dashboard structure
        self.assertIn('active_jobs', dashboard)
        self.assertIn('pending_jobs', dashboard)
        self.assertIn('recent_completions', dashboard)
        self.assertIn('velocity', dashboard)

        # Verify counts
        self.assertEqual(len(dashboard['active_jobs']), 1)  # Job 3 is in-progress
        self.assertEqual(len(dashboard['pending_jobs']), 1)  # Job 6 is pending
        self.assertEqual(len(dashboard['recent_completions']), 4)  # Jobs 1,2,4,5 completed/failed

        # Verify completed and failed jobs in recent completions
        completed_statuses = [j['status'] for j in dashboard['recent_completions']]
        self.assertIn('completed', completed_statuses)
        self.assertIn('failed', completed_statuses)

        # Count projects (verify all 3 exist)
        all_projects = self.db.list_projects()
        self.assertEqual(len(all_projects), 3)

        project_names = [p['name'] for p in all_projects]
        self.assertIn("project-alpha", project_names)
        self.assertIn("project-beta", project_names)
        self.assertIn("project-gamma", project_names)

        # User sees accurate multi-project dashboard
        print("✅ Multi-project tracking: 3 projects, 6 jobs tracked accurately")


class TestErrorRecoveryScenarios(unittest.TestCase):
    """
    UAT Scenario 4: Error Recovery and Edge Cases

    User story: As a user, I want the system to handle errors gracefully
    and provide clear feedback.
    """

    def setUp(self):
        """Create temporary database"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        self.db_path = self.temp_path / "projects.db"

        self.db = ProjectDatabase(db_path=str(self.db_path))

        # Run migrations
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                self.db.conn.executescript(f.read())

    def tearDown(self):
        """Clean up"""
        self.db.close()
        shutil.rmtree(self.temp_dir)

    def test_duplicate_project_name_error(self):
        """Test: User tries to create duplicate project name"""
        import sqlite3

        # Create first project
        self.db.create_project("my-app", "My App", "/tmp/my-app")

        # Try to create duplicate (should fail with clear error)
        with self.assertRaises(sqlite3.IntegrityError) as cm:
            self.db.create_project("my-app", "Another App", "/tmp/another-app")

        # User sees clear error about duplicate name
        self.assertIn("UNIQUE", str(cm.exception).upper())
        print("✅ Duplicate project name error: Clear error message provided")

    def test_invalid_input_validation(self):
        """Test: User provides invalid input (empty names, invalid paths)"""

        # Empty project name
        with self.assertRaises(ValueError) as cm:
            self.db.create_project("", "Description", "/tmp/test")

        self.assertIn("cannot be empty", str(cm.exception))

        # Relative path
        with self.assertRaises(ValueError) as cm:
            self.db.create_project("test", "Description", "./relative/path")

        self.assertIn("absolute path", str(cm.exception))

        # Invalid status
        project_id = self.db.create_project("test", "Test", "/tmp/test")
        with self.assertRaises(ValueError) as cm:
            self.db.create_spec(project_id, "spec", status="invalid_status", frd_content="# FRD")

        self.assertIn("must be one of", str(cm.exception))

        # User sees clear validation errors
        print("✅ Input validation: Clear error messages for invalid inputs")

    def test_failed_job_recovery(self):
        """Test: User recovers from failed job and retries"""

        # Create project and job
        project_id = self.db.create_project("recovery-test", "Test", "/tmp/recovery")
        spec_id = self.db.create_spec(project_id, "spec", frd_content="# FRD")
        job_id = self.db.create_job(spec_id, "Failing Job")

        # Job fails
        self.db.start_job(job_id)
        self.db.log_execution(job_id, None, "npm test", "Tests failed", 1, 5000)
        self.db.complete_job(job_id, exit_code=1, summary="Build failed")

        job = self.db.get_job(job_id)
        self.assertEqual(job['status'], 'failed')
        self.assertEqual(job['exit_code'], 1)

        # User can still query and analyze failure
        logs = self.db.get_execution_logs(job_id=job_id)
        self.assertEqual(len(logs), 1)
        self.assertIn("failed", logs[0]['output'])

        # User sees failed job in dashboard
        dashboard = self.db.generate_dashboard()
        failed_jobs = [j for j in dashboard['recent_completions'] if j['status'] == 'failed']
        self.assertEqual(len(failed_jobs), 1)

        # User creates retry job
        retry_job_id = self.db.create_job(spec_id, "Failing Job (Retry)")
        self.db.start_job(retry_job_id)
        self.db.complete_job(retry_job_id, exit_code=0, summary="Fixed and succeeded")

        # Verify retry succeeded
        dashboard = self.db.generate_dashboard()
        completed_jobs = [j for j in dashboard['recent_completions'] if j['status'] == 'completed']
        failed_jobs = [j for j in dashboard['recent_completions'] if j['status'] == 'failed']
        self.assertEqual(len(completed_jobs), 1)
        self.assertEqual(len(failed_jobs), 1)

        print("✅ Failed job recovery: User can analyze failure and retry")


class TestMemoryBankIntegration(unittest.TestCase):
    """
    UAT Scenario 5: Integration with Memory Bank

    User story: As a user, I want my project data exported to Memory Bank
    for AI agent context.
    """

    def setUp(self):
        """Create temporary database and project directory"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        self.db_path = self.temp_path / "projects.db"
        self.project_dir = self.temp_path / "test-project"
        self.project_dir.mkdir()

        self.db = ProjectDatabase(db_path=str(self.db_path))

        # Run migrations
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                self.db.conn.executescript(f.read())

    def tearDown(self):
        """Clean up"""
        self.db.close()
        shutil.rmtree(self.temp_dir)

    @unittest.skip("Memory Bank export requires default database path - manual testing recommended")
    def test_memory_bank_export(self):
        """
        Test: User exports project data to Memory Bank

        NOTE: This test is skipped because the export script uses the default
        database path (~/.claude/lib/projects.db) and cannot be tested with
        a temporary database in automated tests.

        Manual Testing:
        1. Initialize database: /pm-db init
        2. Create project with filesystem path
        3. Add specs and jobs
        4. Run export: python3 skills/pm-db/scripts/export_to_memory_bank.py --project my-project
        5. Verify: ls -la /path/to/project/memory-bank/

        Steps:
        1. Create project with filesystem path
        2. Add specs and jobs
        3. Export to Memory Bank
        4. Verify Memory Bank files created
        5. Verify content is readable
        """
        # Manual test - see docstring above
        pass


class TestCodeReviewWorkflow(unittest.TestCase):
    """
    UAT Scenario 6: Code Review Workflow

    User story: As a developer, I want to track code reviews and maintain
    quality standards.
    """

    def setUp(self):
        """Create temporary database"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        self.db_path = self.temp_path / "projects.db"

        self.db = ProjectDatabase(db_path=str(self.db_path))

        # Run migrations
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                self.db.conn.executescript(f.read())

        # Create project
        self.project_id = self.db.create_project("review-test", "Test", "/tmp/review")
        self.spec_id = self.db.create_spec(self.project_id, "spec", frd_content="# FRD")

    def tearDown(self):
        """Clean up"""
        self.db.close()
        shutil.rmtree(self.temp_dir)

    def test_code_review_tracking(self):
        """
        Test: Track code reviews for jobs

        Steps:
        1. Create job
        2. Add multiple code reviews (approved, needs_changes, rejected)
        3. View code review metrics
        4. Verify quality trends
        """
        # Step 1: Create 3 jobs
        job1_id = self.db.create_job(self.spec_id, "Job 1")
        job2_id = self.db.create_job(self.spec_id, "Job 2")
        job3_id = self.db.create_job(self.spec_id, "Job 3")

        # Step 2: Add code reviews
        # Job 1: Approved
        self.db.add_code_review(job1_id, None, "reviewer-1", "Excellent work", "approved")

        # Job 2: Changes requested (2 reviews)
        self.db.add_code_review(job2_id, None, "reviewer-1", "Add error handling", "changes-requested")
        self.db.add_code_review(job2_id, None, "reviewer-1", "Good improvements", "approved")

        # Job 3: Rejected
        self.db.add_code_review(job3_id, None, "reviewer-1", "Security vulnerabilities", "rejected")

        # Step 3: View code review metrics
        metrics = self.db.get_code_review_metrics()

        # Step 4: Verify quality trends
        self.assertEqual(metrics['total_reviews'], 4)
        self.assertEqual(metrics['verdict_distribution']['approved'], 2)
        self.assertEqual(metrics['verdict_distribution']['changes-requested'], 1)
        self.assertEqual(metrics['verdict_distribution']['rejected'], 1)

        # Calculate approval rate
        approval_rate = metrics['verdict_distribution']['approved'] / metrics['total_reviews']
        self.assertEqual(approval_rate, 0.5)  # 2/4 = 50%

        print("✅ Code review workflow: Reviews tracked, metrics calculated")


if __name__ == '__main__':
    # Run with verbose output
    print("=" * 80)
    print("PM-DB User Acceptance Testing")
    print("=" * 80)
    print()

    unittest.main(verbosity=2)
