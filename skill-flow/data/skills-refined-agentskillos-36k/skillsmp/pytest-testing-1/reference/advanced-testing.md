# Advanced Testing Patterns

## Contents
- [Property-Based Testing with Hypothesis](#property-based-testing-with-hypothesis)
- [Performance & Load Testing](#performance--load-testing)
- [Contract Testing](#contract-testing)

---

## Property-Based Testing with Hypothesis

```python
# tests/unit/test_feature_engineering.py
import pytest
from hypothesis import given, strategies as st, assume
from src.feature_engineering import calculate_interaction_score, aggregate_user_features

@given(
    views=st.integers(min_value=0, max_value=1000),
    cart_adds=st.integers(min_value=0, max_value=100),
    purchases=st.integers(min_value=0, max_value=10)
)
def test_interaction_score_properties(views, cart_adds, purchases):
    """Test interaction score calculation properties."""
    score = calculate_interaction_score(views, cart_adds, purchases)

    # Score should always be non-negative
    assert score >= 0

    # Purchases should contribute more than cart adds
    if purchases > 0:
        score_with_purchase = calculate_interaction_score(0, 0, purchases)
        score_with_cart = calculate_interaction_score(0, cart_adds, 0)
        assert score_with_purchase > score_with_cart or cart_adds == 0

    # Score should be monotonic
    score_double_views = calculate_interaction_score(views * 2, cart_adds, purchases)
    assert score_double_views >= score

@given(
    user_events=st.lists(
        st.fixed_dictionaries({
            'user_id': st.text(min_size=1, max_size=36),
            'event_type': st.sampled_from(['view', 'add_to_cart', 'purchase']),
            'product_id': st.text(min_size=1, max_size=10),
            'timestamp': st.datetimes(),
        }),
        min_size=1,
        max_size=100
    )
)
def test_user_aggregation_properties(user_events):
    """Test user feature aggregation properties."""
    result = aggregate_user_features(user_events)

    # Each user should appear once
    user_ids = [r['user_id'] for r in result]
    assert len(user_ids) == len(set(user_ids))

    # Event counts should match
    for user_result in result:
        user_id = user_result['user_id']
        expected_events = sum(1 for e in user_events if e['user_id'] == user_id)
        assert user_result['total_events'] == expected_events
```

---

## Performance & Load Testing

### Benchmarking with pytest-benchmark

```python
# tests/performance/test_query_performance.py
import pytest
from google.cloud import bigquery

@pytest.mark.performance
class TestQueryPerformance:
    """Performance tests for BigQuery queries."""

    @pytest.fixture
    def bq_client(self):
        return bigquery.Client()

    def test_user_features_query_performance(self, bq_client, benchmark):
        """Benchmark user features query."""

        def run_query():
            query = """
            SELECT user_id, COUNT(*) as events
            FROM `project.raw.user_events`
            WHERE DATE(event_timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
            GROUP BY user_id
            LIMIT 1000
            """
            return list(bq_client.query(query).result())

        # Benchmark the query
        result = benchmark(run_query)

        # Assert performance requirements
        assert benchmark.stats.stats.mean < 5.0  # Should complete in <5 seconds
        assert len(result) > 0

    @pytest.mark.slow
    def test_query_cost_regression(self, bq_client):
        """Test query doesn't exceed cost budget."""
        query = """
        SELECT * FROM `project.recommendation.user_features`
        WHERE DATE(created_at) = CURRENT_DATE()
        """

        # Dry run to estimate cost
        job_config = bigquery.QueryJobConfig(dry_run=True)
        query_job = bq_client.query(query, job_config=job_config)

        bytes_processed = query_job.total_bytes_processed
        estimated_cost_usd = (bytes_processed / 1e12) * 5  # $5 per TB

        assert estimated_cost_usd < 0.10, f"Query too expensive: ${estimated_cost_usd:.4f}"
```

---

## Contract Testing

### Schema Validation with Pydantic

```python
# tests/integration/test_data_contracts.py
import pytest
from google.cloud import bigquery
from pydantic import BaseModel, Field, validator
from datetime import datetime

class UserFeatureSchema(BaseModel):
    """Contract for user_features table."""
    user_id: str = Field(..., min_length=1, max_length=36)
    total_events: int = Field(..., ge=0)
    total_spent: float = Field(..., ge=0)
    days_since_last_visit: int = Field(..., ge=0, le=365)
    created_at: datetime

    @validator('total_spent')
    def spent_reasonable(cls, v):
        if v > 1000000:
            raise ValueError('Unreasonably high spend')
        return v

@pytest.mark.integration
class TestDataContracts:
    """Test data conforms to expected schemas."""

    def test_user_features_schema(self, bq_client):
        """Validate user_features table schema."""
        query = """
        SELECT * FROM `project.recommendation.user_features`
        LIMIT 100
        """
        results = bq_client.query(query).result()

        errors = []
        for row in results:
            try:
                UserFeatureSchema(**dict(row))
            except Exception as e:
                errors.append(f"Row validation failed: {e}")

        assert len(errors) == 0, f"Schema violations: {errors}"

    def test_schema_backward_compatibility(self, bq_client):
        """Test new schema is backward compatible."""
        table = bq_client.get_table("project.recommendation.user_features")
        current_fields = {field.name for field in table.schema}

        # Required fields that must exist
        required_fields = {'user_id', 'total_events', 'created_at'}

        assert required_fields.issubset(current_fields), \
            f"Missing required fields: {required_fields - current_fields}"
```

### JSON Schema Validation for API Contracts

```python
# tests/contracts/test_api_contracts.py
import pytest
import jsonschema
from jsonschema import validate

# Define API response schema
RECOMMENDATION_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "user_id": {"type": "string"},
        "recommendations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "string"},
                    "score": {"type": "number", "minimum": 0, "maximum": 1},
                    "reason": {"type": "string"}
                },
                "required": ["product_id", "score"]
            },
            "minItems": 1,
            "maxItems": 10
        },
        "metadata": {
            "type": "object",
            "properties": {
                "model_version": {"type": "string"},
                "timestamp": {"type": "string", "format": "date-time"}
            }
        }
    },
    "required": ["user_id", "recommendations"]
}

@pytest.mark.api
class TestAPIContracts:
    """Test API responses conform to contracts."""

    def test_recommendation_response_schema(self):
        """Validate recommendation API response schema."""
        response = {
            "user_id": "user_123",
            "recommendations": [
                {"product_id": "prod_456", "score": 0.95, "reason": "Previously purchased"},
                {"product_id": "prod_789", "score": 0.82}
            ],
            "metadata": {
                "model_version": "v1.2.3",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }

        try:
            validate(instance=response, schema=RECOMMENDATION_RESPONSE_SCHEMA)
        except jsonschema.exceptions.ValidationError as e:
            pytest.fail(f"Schema validation failed: {e.message}")
```

### Cross-Team Data Contract Enforcement

```python
# tests/contracts/test_cross_team_contracts.py
import pytest
from google.cloud import bigquery
import yaml

@pytest.fixture
def contract_spec():
    """Load contract specification from YAML."""
    with open("contracts/user_features_contract.yaml") as f:
        return yaml.safe_load(f)

class TestCrossTeamContracts:
    """Ensure data contracts are maintained across teams."""

    def test_upstream_team_contract(self, bq_client, contract_spec):
        """Validate upstream team's data meets our contract."""

        # Check table exists
        table_ref = contract_spec["table_ref"]
        table = bq_client.get_table(table_ref)
        assert table is not None, f"Table {table_ref} not found"

        # Validate schema matches contract
        expected_fields = {field["name"]: field["type"] for field in contract_spec["schema"]}
        actual_fields = {field.name: field.field_type for field in table.schema}

        for field_name, expected_type in expected_fields.items():
            assert field_name in actual_fields, f"Missing field: {field_name}"
            assert actual_fields[field_name] == expected_type, \
                f"Type mismatch for {field_name}: expected {expected_type}, got {actual_fields[field_name]}"

    def test_data_quality_contract(self, bq_client, contract_spec):
        """Validate data quality meets contract SLAs."""

        query = f"""
        SELECT
            COUNTIF(user_id IS NULL) as null_user_ids,
            COUNTIF(total_events < 0) as negative_events,
            COUNT(*) as total_rows
        FROM `{contract_spec["table_ref"]}`
        WHERE DATE(created_at) = CURRENT_DATE()
        """

        result = list(bq_client.query(query).result())[0]

        # Contract: <1% null user_ids
        null_rate = result.null_user_ids / result.total_rows
        assert null_rate < 0.01, f"Null rate {null_rate:.2%} exceeds 1% threshold"

        # Contract: zero negative events
        assert result.negative_events == 0, f"Found {result.negative_events} negative events"
```

---

## Edge Case Testing

```python
# tests/unit/test_edge_cases.py
import pytest
import numpy as np
import pandas as pd
from src.feature_engineering import calculate_rfm_features

class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_dataframe(self):
        """Test handling of empty input."""
        df = pd.DataFrame(columns=['user_id', 'event_type', 'timestamp'])
        result = calculate_rfm_features(df)
        assert len(result) == 0

    def test_single_event(self):
        """Test with single event."""
        df = pd.DataFrame([{
            'user_id': 'user1',
            'event_type': 'purchase',
            'timestamp': pd.Timestamp('2024-01-01'),
            'amount': 100.0
        }])
        result = calculate_rfm_features(df)
        assert len(result) == 1
        assert result.iloc[0]['recency_days'] >= 0

    def test_null_values(self):
        """Test handling of null values."""
        df = pd.DataFrame([
            {'user_id': 'user1', 'amount': None},
            {'user_id': 'user2', 'amount': 100.0},
        ])
        result = calculate_rfm_features(df)
        assert not result['total_spent'].isna().any()

    def test_extreme_values(self):
        """Test with extreme input values."""
        df = pd.DataFrame([
            {'user_id': 'user1', 'amount': 1e10},  # Very large
            {'user_id': 'user2', 'amount': 0.01},  # Very small
        ])
        result = calculate_rfm_features(df)
        assert all(np.isfinite(result['total_spent']))

    @pytest.mark.parametrize("event_type,expected_score", [
        ('view', 1),
        ('add_to_cart', 3),
        ('purchase', 5),
        ('unknown', 0),
    ])
    def test_event_type_scores(self, event_type, expected_score):
        """Test scoring for different event types."""
        score = calculate_interaction_score(event_type)
        assert score == expected_score
```

---

## Test Data Management

### Test Data Factories

```python
# tests/factories.py
import factory
from factory import fuzzy

class UserEventFactory(factory.Factory):
    """Factory for generating test user events."""

    class Meta:
        model = dict

    user_id = factory.Faker('uuid4')
    product_id = factory.LazyAttribute(lambda o: f"prod_{fuzzy.FuzzyInteger(1, 1000).fuzz()}")
    event_type = fuzzy.FuzzyChoice(['view', 'add_to_cart', 'purchase'])
    event_timestamp = factory.Faker('date_time_between', start_date='-30d', end_date='now')
    session_id = factory.Faker('uuid4')

    @factory.lazy_attribute
    def purchase_amount(self):
        if self.event_type == 'purchase':
            return fuzzy.FuzzyFloat(10.0, 1000.0).fuzz()
        return None

class UserFeatureFactory(factory.Factory):
    """Factory for user features."""

    class Meta:
        model = dict

    user_id = factory.Faker('uuid4')
    total_events = fuzzy.FuzzyInteger(1, 1000)
    total_spent = fuzzy.FuzzyFloat(0, 10000)
    days_since_last_visit = fuzzy.FuzzyInteger(0, 90)

# Usage in tests
def test_with_factory_data():
    """Test using factory-generated data."""
    events = UserEventFactory.create_batch(100)
    user_features = UserFeatureFactory.create_batch(50)
    result = process_user_data(events, user_features)
    assert len(result) > 0
```

### Synthetic Data Generation

```python
# tests/utils/synthetic_data.py
import pandas as pd
from faker import Faker
import random

def generate_realistic_user_events(n_users: int = 100, n_events: int = 1000) -> pd.DataFrame:
    """Generate realistic user event data for testing."""
    fake = Faker()

    users = [fake.uuid4() for _ in range(n_users)]
    products = [f"prod_{i}" for i in range(1, 201)]

    events = []
    for _ in range(n_events):
        user_id = random.choice(users)
        product_id = random.choice(products)
        event_type = random.choices(
            ['view', 'add_to_cart', 'purchase'],
            weights=[70, 20, 10]  # Realistic conversion funnel
        )[0]

        events.append({
            'user_id': user_id,
            'product_id': product_id,
            'event_type': event_type,
            'event_timestamp': fake.date_time_between(start_date='-30d'),
            'session_id': fake.uuid4(),
            'purchase_amount': fake.random_int(10, 1000) if event_type == 'purchase' else None,
        })

    return pd.DataFrame(events)
```
