---
name: testing-patterns
description: Guidelines for testing the application, including directory structure, coverage requirements, mocking external APIs, and validation tests.
version: 1.0.0
---

# Testing Patterns

## Test Directory Structure

```
tests/
├── conftest.py              # Shared fixtures
├── test_elo_ratings.py      # Elo implementation tests
├── test_kalshi_markets.py   # API integration tests
├── test_data_validation.py  # Data quality tests
├── test_dag_parsing.py      # Airflow DAG tests
└── test_{module}.py         # Module-specific tests
```

## Coverage Requirement

**Maintain 85%+ code coverage.**

```bash
# Run with coverage
pytest --cov=plugins --cov-report=term-missing

# Check specific module
pytest tests/test_nba_elo_rating.py --cov=plugins/nba_elo_rating.py
```

## Common Fixtures (conftest.py)

```python
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_db():
    """Mock database manager."""
    db = MagicMock()
    db.fetch_df.return_value = pd.DataFrame()
    return db

@pytest.fixture
def sample_games():
    """Sample game data for testing."""
    return [
        {"home_team": "Lakers", "away_team": "Celtics", "home_score": 110, "away_score": 105},
        {"home_team": "Warriors", "away_team": "Suns", "home_score": 120, "away_score": 115},
    ]
```

## Mocking External APIs

```python
from unittest.mock import patch, MagicMock

def test_fetch_markets():
    with patch('kalshi_markets.MarketsApi') as mock_api:
        mock_api.return_value.get_markets.return_value = MagicMock(
            to_dict=lambda: {"markets": [{"ticker": "NBAWIN-250115-LAKBOS"}]}
        )

        result = fetch_nba_markets()
        assert len(result) == 1
```

## Testing Elo Predictions

```python
def test_elo_prediction_bounds():
    elo = NBAEloRating()
    prob = elo.predict("Lakers", "Celtics")

    assert 0.0 <= prob <= 1.0
    assert prob != 0.5  # Should have home advantage

def test_elo_update_conservation():
    elo = NBAEloRating()
    initial_sum = sum(elo.ratings.values()) if elo.ratings else 0

    elo.update("Lakers", "Celtics", home_won=True)

    # Ratings should be zero-sum
    final_sum = sum(elo.ratings.values())
    assert abs(final_sum - initial_sum - 3000) < 0.01  # 2 new teams at 1500
```

## DAG Parsing Test

```python
def test_dag_imports():
    """Ensure DAG file parses without errors."""
    from dags.multi_sport_betting_workflow import dag

    assert dag is not None
    assert len(dag.tasks) > 0
```

## Data Validation Tests

```python
def test_game_data_completeness():
    from data_validation import validate_nba_data

    report = validate_nba_data()

    assert report.row_count > 1000
    assert report.null_percentage < 5.0
    assert len(report.missing_teams) == 0
```

## Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_nba_elo_rating.py -v

# With coverage
pytest --cov=plugins --cov-report=html

# Fast mode (stop on first failure)
pytest -x
```

## Files to Reference

- `tests/conftest.py` - Shared fixtures
- `tests/test_nba_elo_rating.py` - Elo test examples
- `tests/test_kalshi_markets.py` - API mocking examples
