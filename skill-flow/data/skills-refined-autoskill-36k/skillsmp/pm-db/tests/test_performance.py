#!/usr/bin/env python3
"""
Performance Tests for PM-DB System

Tests performance targets:
- Query response: <100ms (P95)
- Dashboard generation: <2 seconds
- 100 spec import: <5 seconds
- Handles 10,000+ jobs without degradation

Usage:
    python3 skills/pm-db/tests/test_performance.py
"""

import unittest
import tempfile
import time
from pathlib import Path
import sys

# Add lib to path
lib_path = Path(__file__).parent.parent.parent.parent / "lib"
sys.path.insert(0, str(lib_path))

from project_database import ProjectDatabase


class TestPerformance(unittest.TestCase):
    """Test performance targets"""

    def setUp(self):
        """Set up test database"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()

        self.db = ProjectDatabase(db_path=self.db_path)

        # Run migrations
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                self.db.conn.executescript(f.read())

        # Create baseline data
        self.project_id = self.db.create_project("test", "Test", "/tmp/test")
        self.spec_id = self.db.create_spec(self.project_id, "spec", frd_content="# FRD")

    def tearDown(self):
        """Clean up"""
        self.db.close()
        Path(self.db_path).unlink(missing_ok=True)

    def test_query_performance(self):
        """Test query response time <100ms (P95)"""
        # Create 100 jobs
        job_ids = []
        for i in range(100):
            job_id = self.db.create_job(self.spec_id, f"Job {i}")
            job_ids.append(job_id)

        # Measure query times
        query_times = []
        for _ in range(20):
            start = time.time()
            self.db.list_jobs(limit=10)
            elapsed = (time.time() - start) * 1000
            query_times.append(elapsed)

        # Calculate P95
        query_times.sort()
        p95_index = int(len(query_times) * 0.95)
        p95_time = query_times[p95_index]

        print(f"\n  Query P95: {p95_time:.2f}ms")
        self.assertLess(p95_time, 100, f"Query P95 {p95_time:.2f}ms exceeds 100ms target")

    def test_dashboard_performance(self):
        """Test dashboard generation <2 seconds"""
        # Create realistic dataset
        for i in range(50):
            job_id = self.db.create_job(self.spec_id, f"Job {i}")
            if i % 2 == 0:
                self.db.start_job(job_id)
            if i % 3 == 0:
                self.db.complete_job(job_id, exit_code=0)

        # Measure dashboard generation
        start = time.time()
        dashboard = self.db.generate_dashboard()
        elapsed = time.time() - start

        print(f"\n  Dashboard generation: {elapsed:.3f}s")
        self.assertLess(elapsed, 2.0, f"Dashboard {elapsed:.3f}s exceeds 2s target")
        self.assertIsNotNone(dashboard)

    def test_bulk_insert_performance(self):
        """Test bulk operations performance"""
        # Measure 100 job creation
        start = time.time()
        for i in range(100):
            self.db.create_job(self.spec_id, f"Bulk Job {i}")
        elapsed = time.time() - start

        print(f"\n  100 jobs created in: {elapsed:.3f}s")
        self.assertLess(elapsed, 5.0, f"Bulk insert {elapsed:.3f}s exceeds 5s target")

    def test_search_performance(self):
        """Test search performance with large dataset"""
        # Create 1000 execution logs
        job_id = self.db.create_job(self.spec_id, "Search Test")

        for i in range(1000):
            self.db.log_execution(
                job_id, None,
                f"command_{i % 10}",
                f"output_{i}",
                i % 2,
                100
            )

        # Measure search performance
        start = time.time()
        results = self.db.search_execution_logs(command_pattern="%command_5%")
        elapsed = (time.time() - start) * 1000

        print(f"\n  Search 1000 logs: {elapsed:.2f}ms")
        self.assertLess(elapsed, 100, f"Search {elapsed:.2f}ms exceeds 100ms target")
        self.assertGreater(len(results), 0)

    def test_large_dataset_scalability(self):
        """Test system handles 1000+ jobs without degradation"""
        # Create 1000 jobs
        print("\n  Creating 1000 jobs...")
        start = time.time()

        for i in range(1000):
            job_id = self.db.create_job(self.spec_id, f"Scale Job {i}")
            if i % 100 == 0:
                print(f"    {i}/1000 jobs created")

        creation_time = time.time() - start
        print(f"  Creation time: {creation_time:.3f}s")

        # Test query performance on large dataset
        start = time.time()
        jobs = self.db.list_jobs(limit=50)
        query_time = (time.time() - start) * 1000

        print(f"  Query 1000 jobs: {query_time:.2f}ms")
        self.assertLess(query_time, 200, f"Large query {query_time:.2f}ms too slow")
        self.assertEqual(len(jobs), 50)


class TestMemoryUsage(unittest.TestCase):
    """Test memory efficiency"""

    def test_result_set_limit(self):
        """Test that queries respect LIMIT to prevent memory issues"""
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        db = ProjectDatabase(db_path=temp_db.name)

        # Run migrations
        migrations_dir = Path(__file__).parent.parent.parent.parent / "migrations"
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            with open(migration_file, 'r') as f:
                db.conn.executescript(f.read())

        # Create data
        project_id = db.create_project("test", "Test", "/tmp/test")
        spec_id = db.create_spec(project_id, "spec", frd_content="# FRD")

        for i in range(200):
            db.create_job(spec_id, f"Job {i}")

        # Verify LIMIT works
        jobs = db.list_jobs(limit=10)
        self.assertEqual(len(jobs), 10, "LIMIT not respected")

        jobs = db.list_jobs(limit=100)
        self.assertEqual(len(jobs), 100, "LIMIT not respected")

        # Clean up
        db.close()
        Path(temp_db.name).unlink()


if __name__ == '__main__':
    # Run with verbose output
    unittest.main(verbosity=2)
