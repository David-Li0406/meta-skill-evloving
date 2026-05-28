---
name: pytest-testing
description: Pytest testing patterns for data pipelines, Airflow DAGs, and BigQuery queries. Use when writing unit tests for DAG tasks, integration tests with BigQuery, property-based tests with Hypothesis, data contract validation with Pydantic/JSON schemas, performance tests with pytest-benchmark, or snapshot/visual regression tests for data outputs.
---

# Pytest Testing Skill

Write effective tests for data pipelines following best practices.

## Project Setup

### pytest.ini
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = -v --tb=short --strict-markers
markers =
    unit: Unit tests
    integration: Integration tests (require GCP credentials)
    slow: Slow tests
filterwarnings =
    ignore::DeprecationWarning
```

### conftest.py
```python
# tests/conftest.py
import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch
from airflow.models import DAG, Connection
from airflow.utils.state import State

@pytest.fixture
def mock_dag():
    """Create a mock DAG for testing."""
    return DAG(
        dag_id="test_dag",
        start_date=datetime(2024, 1, 1),
        schedule=None,
        catchup=False,
    )

@pytest.fixture
def mock_task_instance(mock_dag):
    """Create a mock TaskInstance."""
    from airflow.models import TaskInstance
    from airflow.operators.empty import EmptyOperator

    task = EmptyOperator(task_id="test_task", dag=mock_dag)
    ti = TaskInstance(task=task, run_id="test_run")
    ti.state = State.RUNNING
    return ti

@pytest.fixture
def mock_context(mock_dag, mock_task_instance):
    """Create a mock Airflow context."""
    return {
        "dag": mock_dag,
        "task_instance": mock_task_instance,
        "ds": "2024-01-01",
        "ds_nodash": "20240101",
        "execution_date": datetime(2024, 1, 1),
        "params": {},
    }

@pytest.fixture
def mock_bigquery_client():
    """Mock BigQuery client."""
    with patch("google.cloud.bigquery.Client") as mock:
        client = MagicMock()
        mock.return_value = client
        yield client

@pytest.fixture
def mock_gcs_client():
    """Mock GCS client."""
    with patch("google.cloud.storage.Client") as mock:
        client = MagicMock()
        mock.return_value = client
        yield client
```

## DAG Testing

### Test DAG Structure
```python
# tests/unit/dags/test_recommendation_dag.py
import pytest
from airflow.models import DagBag

class TestRecommendationDAG:
    """Tests for recommendation DAG."""

    @pytest.fixture
    def dag_bag(self):
        return DagBag(dag_folder="src/dags", include_examples=False)

    def test_dag_loaded(self, dag_bag):
        """Test DAG loads without errors."""
        assert "recommendation_train_daily" in dag_bag.dags
        assert len(dag_bag.import_errors) == 0

    def test_dag_tags(self, dag_bag):
        """Test DAG has required tags."""
        dag = dag_bag.get_dag("recommendation_train_daily")
        assert "recommendation" in dag.tags
        assert "daily" in dag.tags

    def test_dag_schedule(self, dag_bag):
        """Test DAG schedule is correct."""
        dag = dag_bag.get_dag("recommendation_train_daily")
        assert dag.schedule_interval == "0 2 * * *"

    def test_dag_catchup_disabled(self, dag_bag):
        """Test catchup is disabled."""
        dag = dag_bag.get_dag("recommendation_train_daily")
        assert dag.catchup is False

    def test_dag_default_args(self, dag_bag):
        """Test default args are properly set."""
        dag = dag_bag.get_dag("recommendation_train_daily")
        assert dag.default_args["retries"] >= 1
        assert dag.default_args["owner"] != "airflow"

    def test_task_dependencies(self, dag_bag):
        """Test task dependencies are correct."""
        dag = dag_bag.get_dag("recommendation_train_daily")

        extract_task = dag.get_task("extract_user_events")
        transform_task = dag.get_task("transform_features")
        load_task = dag.get_task("load_to_bigquery")

        # Check upstream dependencies
        assert extract_task in transform_task.upstream_list
        assert transform_task in load_task.upstream_list
```

### Test DAG Tasks
```python
# tests/unit/dags/test_dag_tasks.py
import pytest
from unittest.mock import patch, MagicMock
from src.dags.recommendation.tasks import (
    extract_user_events,
    transform_features,
    calculate_recommendations,
)

class TestRecommendationTasks:
    """Tests for recommendation DAG tasks."""

    def test_extract_user_events_success(self, mock_context, mock_bigquery_client):
        """Test extract_user_events returns expected data."""
        mock_bigquery_client.query.return_value.to_dataframe.return_value = MagicMock(
            empty=False,
            shape=(1000, 5)
        )

        result = extract_user_events(**mock_context)

        assert result is not None
        mock_bigquery_client.query.assert_called_once()

    def test_extract_user_events_empty_result(self, mock_context, mock_bigquery_client):
        """Test extract_user_events handles empty result."""
        mock_bigquery_client.query.return_value.to_dataframe.return_value = MagicMock(
            empty=True
        )

        with pytest.raises(ValueError, match="No data found"):
            extract_user_events(**mock_context)

    def test_transform_features(self, mock_context):
        """Test feature transformation logic."""
        input_data = [
            {"user_id": "u1", "product_id": "p1", "event_type": "view"},
            {"user_id": "u1", "product_id": "p1", "event_type": "purchase"},
        ]

        result = transform_features(input_data, **mock_context)

        assert len(result) == 1  # Aggregated by user-product
        assert result[0]["interaction_score"] == 6  # 1 view + 5 purchase
```

## BigQuery Query Testing

```python
# tests/unit/sql/test_feature_queries.py
import pytest
from pathlib import Path

class TestFeatureQueries:
    """Tests for BigQuery feature engineering queries."""

    @pytest.fixture
    def sql_content(self):
        sql_file = Path("src/sql/features/user_features.sql")
        return sql_file.read_text()

    def test_query_has_partition_filter(self, sql_content):
        """Ensure query includes partition filter for cost optimization."""
        assert "WHERE" in sql_content.upper()
        assert any(
            pattern in sql_content.lower()
            for pattern in ["date(", "timestamp_", "_partitiontime"]
        )

    def test_query_no_select_star(self, sql_content):
        """Ensure query doesn't use SELECT *."""
        lines = sql_content.split("\n")
        for line in lines:
            if not line.strip().startswith("--"):  # Skip comments
                assert "SELECT *" not in line.upper(), \
                    "Query should specify columns instead of SELECT *"

    def test_query_uses_safe_divide(self, sql_content):
        """Ensure division uses SAFE_DIVIDE."""
        if "/" in sql_content:
            assert "SAFE_DIVIDE" in sql_content or \
                   all("--" in line for line in sql_content.split("\n") if "/" in line)
```

## Data Validation Tests

```python
# tests/integration/test_data_quality.py
import pytest
from google.cloud import bigquery

@pytest.mark.integration
class TestDataQuality:
    """Integration tests for data quality validation."""

    @pytest.fixture
    def bq_client(self):
        return bigquery.Client()

    def test_user_features_not_null(self, bq_client):
        """Test critical columns are not null."""
        query = """
        SELECT COUNT(*) as null_count
        FROM `project.recommendation.user_features`
        WHERE user_id IS NULL OR total_events IS NULL
        """
        result = list(bq_client.query(query).result())[0]
        assert result.null_count == 0, "Found null values in critical columns"

    def test_interaction_scores_valid(self, bq_client):
        """Test interaction scores are within valid range."""
        query = """
        SELECT
            MIN(interaction_score) as min_score,
            MAX(interaction_score) as max_score
        FROM `project.recommendation.user_product_interactions`
        """
        result = list(bq_client.query(query).result())[0]
        assert result.min_score > 0, "Interaction scores must be positive"
        assert result.max_score < 1000, "Abnormally high interaction score"

    def test_no_duplicate_user_products(self, bq_client):
        """Test no duplicate user-product pairs."""
        query = """
        SELECT user_id, product_id, COUNT(*) as cnt
        FROM `project.recommendation.user_product_interactions`
        GROUP BY user_id, product_id
        HAVING cnt > 1
        """
        result = list(bq_client.query(query).result())
        assert len(result) == 0, f"Found {len(result)} duplicate user-product pairs"
```

## Advanced Fixtures

### Enhanced conftest.py
```python
# tests/conftest.py (additional fixtures)
import pytest
from faker import Faker
import pandas as pd

@pytest.fixture
def fake():
    """Faker instance for generating test data."""
    return Faker()

@pytest.fixture
def sample_user_events_df(fake) -> pd.DataFrame:
    """Generate realistic sample user events DataFrame."""
    n_rows = 100
    return pd.DataFrame({
        'user_id': [fake.uuid4() for _ in range(n_rows)],
        'product_id': [f'prod_{fake.random_int(1, 100)}' for _ in range(n_rows)],
        'event_type': [fake.random_element(['view', 'add_to_cart', 'purchase'])
                       for _ in range(n_rows)],
        'event_timestamp': [fake.date_time_between(start_date='-30d', end_date='now')
                           for _ in range(n_rows)],
        'session_id': [fake.uuid4() for _ in range(n_rows)],
    })

@pytest.fixture
def airflow_test_env(monkeypatch):
    """Set up Airflow test environment variables."""
    test_vars = {
        'AIRFLOW__CORE__DAGS_FOLDER': '/tmp/test_dags',
        'AIRFLOW__CORE__LOAD_EXAMPLES': 'False',
        'AIRFLOW__CORE__UNIT_TEST_MODE': 'True',
        'AIRFLOW_VAR_GCP_PROJECT': 'test-project',
    }
    for key, value in test_vars.items():
        monkeypatch.setenv(key, value)
```

### Parametrized Fixtures
```python
@pytest.fixture(params=['view', 'add_to_cart', 'purchase'])
def event_type(request):
    """Parametrized event type fixture."""
    return request.param

@pytest.fixture(params=[10, 100, 1000])
def batch_size(request):
    """Parametrized batch size for testing scalability."""
    return request.param

def test_process_events_all_types(event_type, sample_user_events_df):
    """Test processing works for all event types."""
    df = sample_user_events_df[sample_user_events_df['event_type'] == event_type]
    result = process_events(df)
    assert result is not None
```

## Best Practices

- Separate unit and integration tests with markers
- Use fixtures for common mocks (BigQuery, GCS clients)
- Test DAG structure, not just task logic
- Validate SQL queries for common issues (SELECT *, partitioning)
- Include data quality tests in CI pipeline
- Mock external services in unit tests
- Parametrize tests for multiple scenarios
- Test edge cases: empty data, nulls, extreme values
- Track test coverage and aim for >80% for critical paths

## Advanced Topics

For detailed guidance on specialized testing patterns:

- **Property-Based Testing**: See [reference/advanced-testing.md](reference/advanced-testing.md) for Hypothesis patterns
- **Performance Testing**: See [reference/advanced-testing.md](reference/advanced-testing.md) for pytest-benchmark usage
- **Contract Testing**: See [reference/advanced-testing.md](reference/advanced-testing.md) for Pydantic/JSON schema validation
- **Snapshot Testing**: See [reference/snapshot-testing.md](reference/snapshot-testing.md) for visual regression and approval workflows
