# Test Patterns and Examples for Budget Buddy

Complete test patterns, examples, and advanced testing techniques.

## Test Categories

### 1. Unit Tests

Test individual functions in isolation.

```python
import pytest
from difflib import SequenceMatcher

def test_fuzzy_match_exact():
    """Test exact string match returns 1.0"""
    similarity = SequenceMatcher(None, "test", "test").ratio()
    assert similarity == 1.0

def test_fuzzy_match_similar():
    """Test similar strings above threshold"""
    similarity = SequenceMatcher(
        None,
        "CHECK #1234 - RENT",
        "CHECK #1235 - RENT"
    ).ratio()
    assert similarity >= 0.85

def test_fuzzy_match_different():
    """Test different strings below threshold"""
    similarity = SequenceMatcher(None, "STARBUCKS", "TARGET").ratio()
    assert similarity < 0.85
```

### 2. API Tests

Test API endpoints with HTTP requests.

```python
import pytest
import requests

BASE_URL = "http://127.0.0.1:8000/api/v2"

def test_get_transactions():
    """Test GET /transactions endpoint"""
    response = requests.get(f"{BASE_URL}/transactions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_diagnostics():
    """Test GET /diagnostics endpoint"""
    response = requests.get(f"{BASE_URL}/diagnostics")
    assert response.status_code == 200
    data = response.json()
    assert 'status' in data

def test_cors_headers():
    """Test CORS headers are present"""
    response = requests.options(
        f"{BASE_URL}/transactions",
        headers={
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'GET'
        }
    )
    assert response.headers.get('access-control-allow-origin') == 'http://localhost:3000'
```

### 3. Database Tests

```python
import pytest
from backend.database.session import get_session
from backend.database.models import Transaction

@pytest.fixture
def test_db():
    """Create test database session"""
    session = get_session()
    yield session
    session.close()

def test_create_transaction(test_db):
    """Test creating a new transaction"""
    tx = Transaction(
        description="TEST TRANSACTION",
        amount=-50.00,
        date="2026-01-01",
        merchant_name="Test Merchant"
    )
    test_db.add(tx)
    test_db.commit()

    # Verify
    saved_tx = test_db.query(Transaction).filter_by(
        description="TEST TRANSACTION"
    ).first()

    assert saved_tx is not None
    assert saved_tx.amount == -50.00

    # Cleanup
    test_db.delete(saved_tx)
    test_db.commit()
```

## Test Organization

### Directory Structure

```
backend/tests/
├── __init__.py
├── conftest.py                    # Shared fixtures
├── test_apply_planning.py         # Planning logic
├── test_api_endpoints.py          # API integration
├── test_database_operations.py    # Database tests
├── test_fuzzy_matching.py         # Classification
├── test_plaid_integration.py      # Bank integration
└── test_buddy_ai.py               # Buddy AI tests
```

### Fixtures (conftest.py)

```python
import pytest
from backend.database.session import get_session

@pytest.fixture(scope='session')
def test_db():
    """Database session for all tests"""
    session = get_session()
    yield session
    session.close()

@pytest.fixture
def sample_transaction():
    """Sample transaction for testing"""
    return {
        'id': 1,
        'description': 'STARBUCKS COFFEE #123',
        'merchant_name': 'Starbucks',
        'amount': -5.50,
        'date': '2026-01-01',
        'bb_category': 'Food & Dining',
        'bb_category_manual': False
    }

@pytest.fixture
def plaid_test_credentials():
    """Test Plaid credentials"""
    return {
        'client_id': os.getenv('PLAID_CLIENT_ID'),
        'secret': os.getenv('PLAID_SECRET_SANDBOX'),
        'env': 'sandbox'
    }
```

## Coverage Analysis

### Generate HTML Report

```bash
pytest backend/tests/ --cov=backend --cov-report=html
open htmlcov/index.html
```

### View in Terminal

```bash
pytest backend/tests/ --cov=backend --cov-report=term-missing
```

Output example:
```
Name                                    Stmts   Miss  Cover   Missing
---------------------------------------------------------------------
backend/api/main.py                       120      5    96%   45-49
backend/services/database_service.py      450     30    93%   234-245
backend/services/plaid_service.py         180     45    75%   90-102
---------------------------------------------------------------------
TOTAL                                    1500    120    92%
```

### Coverage Goals

- **Overall**: 80%+
- **Critical paths**: 95%+ (classification, budget calc, Plaid, DB ops)
- **UI components**: 70%+
- **Utilities**: 90%+

## Common Test Patterns

### Testing with Mock Data

```python
from unittest.mock import Mock, patch

def test_plaid_api_error_handling():
    """Test handling Plaid API errors"""
    with patch('plaid.ApiClient') as mock_client:
        # Simulate API error
        mock_client.transactions_get.side_effect = Exception("API Error")

        service = PlaidService()

        with pytest.raises(Exception) as exc:
            service.fetch_transactions("bad_token")

        assert "API Error" in str(exc.value)
```

### Testing Async Functions

```python
import pytest

@pytest.mark.asyncio
async def test_async_fetch():
    """Test async data fetching"""
    result = await fetch_data_async()
    assert result is not None
```

### Parametrized Tests

```python
@pytest.mark.parametrize("desc1,desc2,expected", [
    ("CHECK #80", "CHECK #81", 0.95),
    ("STARBUCKS", "TARGET", 0.20),
    ("RENT PAYMENT", "RENT PAYMENT", 1.0),
])
def test_similarity_scores(desc1, desc2, expected):
    """Test various similarity calculations"""
    from difflib import SequenceMatcher
    similarity = SequenceMatcher(None, desc1, desc2).ratio()
    assert abs(similarity - expected) < 0.05
```

## Debugging Tests

### Run Single Test Verbose

```bash
pytest backend/tests/test_file.py::test_function_name -vv
```

### Disable Capture (show prints)

```bash
pytest backend/tests/test_file.py -s
```

### Use Debugger

```bash
pytest backend/tests/test_file.py --pdb
```

In pdb:
```python
(Pdb) print(variable_name)
(Pdb) locals()
(Pdb) continue
```

### Full Traceback

```bash
pytest backend/tests/test_file.py --tb=long
```

## CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/test.yml
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11

    - name: Install dependencies
      run: |
        pip install -r backend/requirements.txt
        pip install pytest pytest-cov

    - name: Run tests
      run: |
        pytest backend/tests/ --cov=backend --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v2
      with:
        file: ./coverage.xml
```

## Test Data Management

### Create Test Database

```python
# backend/tests/conftest.py

import pytest
from backend.database.session import init_db

@pytest.fixture(scope='session', autouse=True)
def setup_test_db():
    """Create test database before all tests"""
    os.environ['DATABASE_URL'] = 'sqlite:///./test_budget_buddy.db'

    init_db()
    yield

    # Cleanup
    if os.path.exists('test_budget_buddy.db'):
        os.remove('test_budget_buddy.db')
```

### Seed Test Data

```python
@pytest.fixture
def seed_transactions(test_db):
    """Add sample transactions for testing"""
    transactions = [
        Transaction(description="STARBUCKS", amount=-5.50, date="2026-01-01"),
        Transaction(description="WHOLE FOODS", amount=-50.00, date="2026-01-02"),
        Transaction(description="TARGET", amount=-30.00, date="2026-01-03"),
    ]

    test_db.bulk_save_objects(transactions)
    test_db.commit()

    yield

    # Cleanup
    test_db.query(Transaction).delete()
    test_db.commit()
```

## Performance Testing

### Measure Test Duration

```bash
pytest backend/tests/ --durations=10
```

Shows 10 slowest tests.

### Test Query Performance

```python
import time

def test_query_performance():
    """Ensure queries complete within acceptable time"""
    start = time.time()

    results = db.query(Transaction).filter(
        Transaction.date >= "2026-01-01"
    ).all()

    elapsed = time.time() - start

    assert elapsed < 1.0  # Under 1 second
    assert len(results) > 0
```

## Full Test Suite Script

```bash
#!/bin/bash
# run_all_tests.sh

echo "Running all backend tests..."

# Unit tests
echo "1. Running unit tests..."
pytest backend/tests/test_*.py --ignore=backend/tests/test_api_*.py -v

# API tests (requires backend running)
echo "2. Starting backend for API tests..."
python -m uvicorn backend.api.main:app --reload --port 8000 &
BACKEND_PID=$!
sleep 5

echo "3. Running API tests..."
pytest backend/tests/test_api_*.py -v

echo "4. Stopping backend..."
kill $BACKEND_PID

# Coverage report
echo "5. Generating coverage report..."
pytest backend/tests/ --cov=backend --cov-report=html --cov-report=term

echo "Done! Coverage report: htmlcov/index.html"
```

## Continuous Integration Mode

```bash
# Fast mode for CI/CD
pytest backend/tests/ \
  --tb=short \
  --maxfail=1 \
  --cov=backend \
  --cov-report=term-missing \
  --cov-fail-under=70
```

Flags:
- `--tb=short` - Shorter tracebacks
- `--maxfail=1` - Stop after first failure
- `--cov-fail-under=70` - Fail if coverage < 70%
