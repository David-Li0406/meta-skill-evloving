# Snapshot Testing & Visual Regression

## Contents
- [Snapshot Testing for Data Outputs](#snapshot-testing-for-data-outputs)
- [Automated Approval Workflows](#automated-approval-workflows)

---

## Snapshot Testing for Data Outputs

```python
# tests/snapshots/test_feature_snapshots.py
import pytest
import json
from pathlib import Path

class TestFeatureSnapshots:
    """Snapshot tests for feature engineering outputs."""

    @pytest.fixture
    def snapshot_dir(self):
        """Directory for storing snapshots."""
        path = Path("tests/snapshots/data")
        path.mkdir(parents=True, exist_ok=True)
        return path

    def test_user_features_snapshot(self, snapshot_dir, bq_client):
        """Snapshot test for user features output."""

        # Generate current output
        query = """
        SELECT user_id, total_events, total_spent
        FROM `project.recommendation.user_features`
        WHERE user_id IN ('user_1', 'user_2', 'user_3')
        ORDER BY user_id
        """

        current_output = [dict(row) for row in bq_client.query(query).result()]

        snapshot_file = snapshot_dir / "user_features.json"

        if snapshot_file.exists():
            # Compare with existing snapshot
            with open(snapshot_file) as f:
                expected_output = json.load(f)

            assert current_output == expected_output, \
                "Feature output changed! Review diff:\n" + \
                f"Expected: {expected_output}\nActual: {current_output}"
        else:
            # Create new snapshot
            with open(snapshot_file, 'w') as f:
                json.dump(current_output, f, indent=2, default=str)
            pytest.skip("Created new snapshot. Review and commit if correct.")

    def test_recommendation_output_snapshot(self, snapshot_dir):
        """Snapshot test for recommendation model output."""

        from src.recommendation.model import get_recommendations

        # Get recommendations for test users
        recommendations = get_recommendations(user_ids=["user_1", "user_2"])

        snapshot_file = snapshot_dir / "recommendations.json"

        if snapshot_file.exists():
            with open(snapshot_file) as f:
                expected = json.load(f)

            # Allow some variance in scores (within 5%)
            for i, (curr, exp) in enumerate(zip(recommendations, expected)):
                assert curr["user_id"] == exp["user_id"]
                assert curr["product_id"] == exp["product_id"]

                score_diff = abs(curr["score"] - exp["score"])
                tolerance = exp["score"] * 0.05  # 5% tolerance

                assert score_diff <= tolerance, \
                    f"Score changed by {score_diff:.3f} (>{tolerance:.3f}): {curr} vs {exp}"
        else:
            with open(snapshot_file, 'w') as f:
                json.dump(recommendations, f, indent=2, default=str)
            pytest.skip("Created new snapshot")
```

---

## Automated Approval Workflows

### Configuration

```python
# tests/snapshots/conftest.py
import pytest
import os

def pytest_configure(config):
    """Configure snapshot testing behavior."""
    config.addinivalue_line(
        "markers", "snapshot: mark test as snapshot test"
    )

@pytest.fixture
def snapshot_update_mode():
    """Control snapshot update behavior via environment variable."""
    return os.getenv("UPDATE_SNAPSHOTS", "false").lower() == "true"
```

### Approval Workflow Tests

```python
# tests/snapshots/test_with_approval.py
import pytest

@pytest.mark.snapshot
class TestWithApproval:
    """Snapshot tests with approval workflow."""

    def test_query_output_approval(self, snapshot_dir, snapshot_update_mode, bq_client):
        """Test query output with approval workflow."""

        query = "SELECT COUNT(*) as count FROM `project.recommendation.user_features`"
        result = list(bq_client.query(query).result())[0]
        current_count = result.count

        snapshot_file = snapshot_dir / "user_feature_count.txt"

        if snapshot_update_mode:
            # Update mode: always update snapshots
            with open(snapshot_file, 'w') as f:
                f.write(str(current_count))
            pytest.skip("Snapshot updated in UPDATE mode")

        elif snapshot_file.exists():
            # Comparison mode
            with open(snapshot_file) as f:
                expected_count = int(f.read().strip())

            # Allow 10% variance
            variance = abs(current_count - expected_count) / expected_count
            assert variance < 0.10, \
                f"Count variance {variance:.1%} exceeds 10%: {current_count} vs {expected_count}"
        else:
            # Create new snapshot (requires manual approval)
            with open(snapshot_file, 'w') as f:
                f.write(str(current_count))
            pytest.skip("New snapshot created. Run 'git add' to approve.")
```

### Usage Commands

```bash
# Normal test run (compares with snapshots)
pytest tests/snapshots/

# Update all snapshots
UPDATE_SNAPSHOTS=true pytest tests/snapshots/

# Review changes before committing
git diff tests/snapshots/data/
```

---

## Tolerance-Based Comparison

For numerical outputs that may have minor variations:

```python
def test_numerical_output_with_tolerance(self, snapshot_dir, bq_client):
    """Test numerical output with configurable tolerance."""

    query = """
    SELECT AVG(total_spent) as avg_spent, STDDEV(total_spent) as std_spent
    FROM `project.recommendation.user_features`
    """

    result = dict(list(bq_client.query(query).result())[0])
    snapshot_file = snapshot_dir / "spending_stats.json"

    if snapshot_file.exists():
        with open(snapshot_file) as f:
            expected = json.load(f)

        # Define tolerances for each metric
        tolerances = {
            'avg_spent': 0.05,  # 5% tolerance
            'std_spent': 0.10,  # 10% tolerance (more variance expected)
        }

        for key, tolerance in tolerances.items():
            actual = result[key]
            exp = expected[key]
            relative_diff = abs(actual - exp) / exp if exp != 0 else abs(actual)

            assert relative_diff <= tolerance, \
                f"{key} changed by {relative_diff:.1%} (tolerance: {tolerance:.0%})"
    else:
        with open(snapshot_file, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        pytest.skip("Created new snapshot")
```
