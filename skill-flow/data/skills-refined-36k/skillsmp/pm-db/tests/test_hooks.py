#!/usr/bin/env python3
"""
Hook Tests for PM-DB System

Tests individual hook functionality in isolation.

Usage:
    python3 skills/pm-db/tests/test_hooks.py
"""

import unittest
import json
import subprocess
from pathlib import Path
import tempfile
import sys

# Add lib to path
lib_path = Path(__file__).parent.parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

from project_database import ProjectDatabase


class TestHooks(unittest.TestCase):
    """Test hook behavior"""

    def setUp(self):
        """Set up test environment"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()

        # Initialize database
        self.db = ProjectDatabase(db_path=self.db_path)
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                self.db.conn.executescript(f.read())

        # Create test data
        self.project_id = self.db.create_project("test", "Test", "/tmp/test")
        self.spec_id = self.db.create_spec(self.project_id, "spec", frd_content="# FRD")

    def tearDown(self):
        """Clean up"""
        self.db.close()
        Path(self.db_path).unlink(missing_ok=True)

    def run_hook(self, hook_name: str, input_data: dict) -> dict:
        """Run a hook and return parsed output"""
        hook_path = Path(__file__).parent.parent.parent / f"hooks/pm-db/{hook_name}.py"

        if not hook_path.exists():
            self.skipTest(f"Hook {hook_name} not found")

        result = subprocess.run(
            ["python3", str(hook_path)],
            input=json.dumps(input_data),
            capture_output=True,
            text=True,
            env={"CLAUDE_DB_PATH": self.db_path}
        )

        self.assertEqual(result.returncode, 0, f"Hook failed: {result.stderr}")
        return json.loads(result.stdout)

    def test_on_job_start_hook_minimal(self):
        """Test on-job-start with minimal input"""
        output = self.run_hook("on-job-start", {
            "spec_id": self.spec_id,
            "job_name": "Test Job"
        })

        self.assertEqual(output['status'], 'created')
        self.assertIn('job_id', output)

        # Verify in database
        job = self.db.get_job(output['job_id'])
        self.assertEqual(job['status'], 'in-progress')

    def test_on_task_start_hook(self):
        """Test on-task-start hook"""
        job_id = self.db.create_job(self.spec_id, "Test Job")

        output = self.run_hook("on-task-start", {
            "job_id": job_id,
            "task_name": "Test Task",
            "order": 1
        })

        self.assertEqual(output['status'], 'created')

        tasks = self.db.get_tasks(job_id)
        self.assertEqual(len(tasks), 1)

    def test_on_task_complete_hook(self):
        """Test on-task-complete hook"""
        job_id = self.db.create_job(self.spec_id, "Test Job")
        task_id = self.db.create_task(job_id, "Test Task", order=1)
        self.db.start_task(task_id)

        output = self.run_hook("on-task-complete", {
            "job_id": job_id,
            "task_name": "Test Task",
            "exit_code": 0
        })

        self.assertEqual(output['status'], 'completed')

        task = self.db.get_task(task_id)
        self.assertEqual(task['status'], 'completed')

    def test_on_code_review_hook(self):
        """Test on-code-review hook"""
        job_id = self.db.create_job(self.spec_id, "Test Job")

        output = self.run_hook("on-code-review", {
            "job_id": job_id,
            "reviewer": "test-reviewer",
            "summary": "Test review",
            "verdict": "approved",
            "issues_found": [],
            "files_reviewed": ["test.py"]
        })

        self.assertEqual(output['status'], 'stored')

        reviews = self.db.get_code_reviews(job_id=job_id)
        self.assertEqual(len(reviews), 1)

    def test_on_agent_assign_hook(self):
        """Test on-agent-assign hook"""
        job_id = self.db.create_job(self.spec_id, "Test Job")

        output = self.run_hook("on-agent-assign", {
            "agent_type": "test-agent",
            "job_id": job_id
        })

        self.assertEqual(output['status'], 'assigned')

        assignments = self.db.get_agent_assignments(job_id=job_id)
        self.assertEqual(len(assignments), 1)

    def test_hook_error_handling(self):
        """Test hooks handle invalid input gracefully"""
        # Test missing required field
        output = self.run_hook("on-job-start", {})
        self.assertEqual(output['status'], 'failed')
        self.assertIn('error', output)


if __name__ == '__main__':
    unittest.main(verbosity=2)
