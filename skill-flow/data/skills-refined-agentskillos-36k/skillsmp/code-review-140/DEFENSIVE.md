# Defensive Programming Review

Review patterns for error handling, validation, and failure detection.

**Principle:** Fail fast and visibly when something is wrong. Silent failures hide bugs.

---

## Critical Defensive Patterns

### 1. Validation Gates Before Execution

**Pattern:** Before executing a workflow node, validate that all prerequisite data exists and is non-empty.

```python
# ❌ REJECT: Assumes upstream succeeded
def analyze_technical(state: AgentState) -> AgentState:
    result = analyzer.calculate_indicators(state['ticker_data'])
    state['indicators'] = result  # Might be {} if ticker_data was empty!
    return state

# ✅ APPROVE: Validates prerequisites
def analyze_technical(state: AgentState) -> AgentState:
    # VALIDATION GATE
    if not state.get('ticker_data') or len(state['ticker_data']) == 0:
        logger.error(f"Cannot analyze: ticker_data is empty for {state['ticker']}")
        state['error'] = "Missing ticker data"
        return state

    # Safe to proceed
    result = analyzer.calculate_indicators(state['ticker_data'])
    state['indicators'] = result
    return state
```

**Review Questions:**
- [ ] Does this function validate inputs before processing?
- [ ] Does it check that prerequisite data exists AND is non-empty?
- [ ] Does it fail explicitly if prerequisites are missing?

---

### 2. No Silent None Propagation

**Pattern:** Functions that return `None` on failure create cascading silent failures.

```python
# ❌ REJECT: Returns None hides failures
def fetch_ticker_data(ticker: str):
    hist = yf.download(ticker, period='1y')
    if hist is None or hist.empty:
        logger.warning(f"No data for {ticker}")
        return None  # ✗ Caller doesn't know WHY it failed

# ✅ APPROVE: Raises explicit exception
def fetch_ticker_data(ticker: str):
    hist = yf.download(ticker, period='1y')
    if hist is None or hist.empty:
        error_msg = f"No historical data for {ticker}"
        logger.error(error_msg)
        raise ValueError(error_msg)  # ✓ Explicit failure
```

**Review Questions:**
- [ ] Does this function return None on error?
- [ ] Would an exception be more appropriate?
- [ ] Does the caller know HOW to handle None?

---

### 3. Explicit Failure Detection

**Pattern:** Check operation outcomes (rowcount, status codes), not just absence of exceptions.

```python
# ❌ REJECT: Only checks for exceptions
def store_report(symbol: str, data: dict) -> bool:
    try:
        db.execute(insert_query, params)
        return True  # Always returns True if no exception!
    except Exception as e:
        logger.warning(f"DB error: {e}")
        return True  # ❌ Still returns True!

# ✅ APPROVE: Checks actual outcome
def store_report(symbol: str, data: dict) -> bool:
    rowcount = db.execute(insert_query, params)
    if rowcount == 0:
        logger.error(f"INSERT affected 0 rows for {symbol}")
        return False  # Explicit failure
    return True
```

**Common Silent Failures:**

| Failure Mode | Raises Exception? | How to Detect |
|--------------|-------------------|---------------|
| FK constraint (MySQL) | Sometimes | Check rowcount |
| ENUM value mismatch | No | Check rowcount |
| Duplicate key (IGNORE) | No | Check rowcount |
| Write to wrong table | No | Round-trip test |

**Review Questions:**
- [ ] Does this function check operation outcomes (not just exceptions)?
- [ ] Are errors logged at ERROR level (not WARNING)?
- [ ] Does the function return explicit success/failure indicators?

---

## Boundary Validation Patterns

### 1. Type Compatibility at System Boundaries

**Pattern:** When crossing boundaries (API ↔ Database, Service ↔ External API), verify data type compatibility explicitly.

```python
# ❌ REJECT: Assumes type compatibility
def store_to_db(report: dict):
    # Python dict → MySQL JSON column
    db.execute("INSERT INTO reports (data) VALUES (%s)", (report,))
    # ✗ May fail silently if driver expects string

# ✅ APPROVE: Explicit conversion at boundary
import json

def store_to_db(report: dict):
    # Convert dict → JSON string at boundary
    json_string = json.dumps(report)
    db.execute("INSERT INTO reports (data) VALUES (%s)", (json_string,))
    # ✓ Guaranteed type compatibility
```

**Review Questions:**
- [ ] Does data cross system boundaries (DB, API, message queue)?
- [ ] Are types explicitly converted at boundaries?
- [ ] Is there a round-trip test (write then read)?

---

### 2. JSON Serialization Validation

**Pattern:** NumPy/Pandas types must be converted before JSON encoding.

```python
# ❌ REJECT: NumPy types not serializable
import numpy as np

def lambda_handler(event, context):
    result = {
        'price': np.float64(123.45),  # TypeError: not serializable
        'volume': np.int64(1000)
    }
    return result  # ✗ Lambda fails to return

# ✅ APPROVE: Convert to native types
def lambda_handler(event, context):
    result = {
        'price': float(np.float64(123.45)),  # Native Python float
        'volume': int(np.int64(1000))         # Native Python int
    }
    return result  # ✓ JSON-serializable
```

**Review Questions:**
- [ ] Does this code use NumPy/Pandas types?
- [ ] Are types converted before JSON encoding?
- [ ] Is there explicit serialization testing?

---

### 3. Database ENUM Validation

**Pattern:** MySQL ENUMs fail silently on mismatch (no exception, data just doesn't persist).

```python
# ❌ REJECT: No ENUM validation
def store_job(ticker: str, status: str):
    # If status not in ENUM values, INSERT affects 0 rows
    rowcount = db.execute(
        "INSERT INTO jobs (ticker, status) VALUES (%s, %s)",
        (ticker, status)
    )
    # ✗ Doesn't check rowcount

# ✅ APPROVE: Validates ENUM + checks outcome
VALID_STATUSES = {'pending', 'completed', 'failed'}

def store_job(ticker: str, status: str):
    # Validate ENUM before DB call
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}. Must be one of {VALID_STATUSES}")

    # Check operation outcome
    rowcount = db.execute(
        "INSERT INTO jobs (ticker, status) VALUES (%s, %s)",
        (ticker, status)
    )

    if rowcount == 0:
        logger.error(f"INSERT failed for {ticker} with status {status}")
        return False

    return True
```

**Review Questions:**
- [ ] Does schema use MySQL ENUMs?
- [ ] Are ENUM values validated before DB calls?
- [ ] Is rowcount checked after INSERT/UPDATE?

---

## Configuration Validation Patterns

### 1. Startup Validation vs Runtime Validation

**Pattern:** Validate configuration at startup, not on first use.

```python
# ❌ REJECT: Validates on first use
def populate_cache():
    # Assumes AURORA_HOST exists - may fail deep in execution
    lambda_client.invoke(FunctionName=SCHEDULER_LAMBDA, Payload={...})

# ✅ APPROVE: Validates at startup
import os

# Module-level validation (runs at import time)
REQUIRED_ENV_VARS = ['AURORA_HOST', 'AURORA_PASSWORD', 'OPENROUTER_API_KEY']

def validate_config():
    """Run at startup - fails fast if config missing"""
    missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing:
        raise ValueError(f"Missing required env vars: {missing}")

validate_config()  # Fails immediately if config wrong

def populate_cache():
    # Now safe - config validated at startup
    lambda_client.invoke(FunctionName=SCHEDULER_LAMBDA, Payload={...})
```

**Review Questions:**
- [ ] Is configuration validated at startup?
- [ ] Does validation fail fast (before any operations)?
- [ ] Are all required env vars checked?

---

### 2. Data Existence Validation

**Pattern:** Never assume data exists without validating first.

```python
# ❌ REJECT: Assumes cache is populated
def trigger_ui_refresh():
    # Assumes 46 tickers in cache - may fail silently
    invalidate_cloudfront()

# ✅ APPROVE: Validates data exists first
def trigger_ui_refresh():
    cache_count = check_cache_population()
    if cache_count == 0:
        raise ValueError("Cache is empty - populate before refreshing UI")

    if cache_count < 46:
        logger.warning(f"Cache only has {cache_count}/46 tickers - may be incomplete")

    invalidate_cloudfront()
```

**Review Questions:**
- [ ] Does this operation assume data exists?
- [ ] Is data existence validated before operations?
- [ ] Does code fail explicitly if data is missing?

---

## Error Propagation Patterns

### 1. Workflow vs Utility Error Handling

**Pattern:** Workflow nodes use state-based error propagation. Utility functions raise exceptions.

```python
# ✅ WORKFLOW NODE: State-based error propagation
def analyze_technical(state: AgentState) -> AgentState:
    """Workflow node - never raises exceptions"""
    try:
        result = analyzer.calculate_indicators(state['ticker_data'])
        state['indicators'] = result
    except Exception as e:
        logger.error(f"Technical analysis failed: {e}")
        state['error'] = str(e)  # Propagate via state

    return state  # Always returns state

# ✅ UTILITY FUNCTION: Raises exceptions
def calculate_rsi(prices: list) -> float:
    """Utility function - raises on invalid input"""
    if not prices or len(prices) < 14:
        raise ValueError("Need at least 14 prices for RSI")

    # Calculate RSI
    return rsi_value
```

**Review Questions:**
- [ ] Is this a workflow node or utility function?
- [ ] Does workflow node propagate errors via state (not exceptions)?
- [ ] Does utility function raise descriptive exceptions?

---

### 2. The Truthy Trap

**Pattern:** Empty dict is truthy but has no content.

```python
# ❌ REJECT: Empty dict passes truthy check
result = {'indicators': {}, 'ticker_data': {}, 'percentiles': {}}
if result['indicators']:  # ✓ Passes (dict exists)
    process(result)       # ✗ Fails (dict is empty)

# ✅ APPROVE: Check for actual content
if result.get('indicators') and len(result['indicators']) > 0:
    process(result)
else:
    logger.warning(f"Indicators dict is empty: {result.get('indicators')}")
    raise ValueError("indicators must contain data")
```

**Review Questions:**
- [ ] Does code check dict truthiness without checking length?
- [ ] Are empty dicts considered valid data?
- [ ] Does code validate actual content (not just existence)?

---

## Multi-Layer Verification Patterns

### 1. AWS Service Success ≠ No Errors

**Pattern:** AWS services returning successful HTTP status codes (200, 202) doesn't guarantee error-free execution.

```python
# ❌ REJECT: Only checks status code
response = lambda_client.invoke(FunctionName='worker', Payload='{}')
assert response['StatusCode'] == 200  # ✗ Weak validation

# ✅ APPROVE: Multi-layer verification
import boto3
from datetime import datetime, timedelta

response = lambda_client.invoke(FunctionName='worker', Payload='{}')

# Layer 1: Status code
assert response['StatusCode'] == 200

# Layer 2: Response payload
payload = json.loads(response['Payload'].read())
assert 'errorMessage' not in payload, f"Lambda error: {payload.get('errorMessage')}"

# Layer 3: CloudWatch logs
logs_client = boto3.client('logs')
log_events = logs_client.filter_log_events(
    logGroupName='/aws/lambda/worker',
    startTime=int((datetime.now() - timedelta(minutes=1)).timestamp() * 1000),
    filterPattern='ERROR'
)

assert len(log_events['events']) == 0, \
    f"Found {len(log_events['events'])} errors in logs"
```

**Verification Layers:**

| Layer | What It Checks | Strength |
|-------|----------------|----------|
| **Status Code** | Did process complete? | Weakest |
| **Response Payload** | What was returned? | Medium |
| **CloudWatch Logs** | Were errors logged? | Strongest |

**Review Questions:**
- [ ] Does code only check status codes?
- [ ] Is response payload validated?
- [ ] Are CloudWatch logs checked for errors?

---

### 2. Code Execution ≠ Correct Output

**Pattern:** A function returning without raising an exception doesn't mean it produced expected data.

```python
# ❌ REJECT: Assumes workflow produces expected data
def store_user_scores(agent_result):
    # Code exists to populate user_facing_scores, so we assume it worked
    precompute_service.store_report(
        report_json=agent_result  # Might be empty dict!
    )

# ✅ APPROVE: Validates actual output content
def store_user_scores(agent_result):
    # Verify output content, not just execution
    if 'user_facing_scores' not in agent_result:
        logger.error("Agent workflow did not produce user_facing_scores")
        raise ValueError("Missing required field: user_facing_scores")

    if not agent_result['user_facing_scores']:
        logger.error(f"user_facing_scores is empty: {agent_result['user_facing_scores']}")
        raise ValueError("user_facing_scores must not be empty")

    # Now safe - we know the data exists and is non-empty
    precompute_service.store_report(report_json=agent_result)
```

**Review Questions:**
- [ ] Does code assume output without verification?
- [ ] Is actual output content validated?
- [ ] Does code distinguish execution success from data correctness?

---

## Quick Reference

### Defensive Review Checklist

**Before Execution:**
- [ ] Are all prerequisites validated?
- [ ] Is configuration checked at startup?
- [ ] Are inputs validated (type, format, range)?

**During Execution:**
- [ ] Are operation outcomes checked (not just exceptions)?
- [ ] Are types converted at system boundaries?
- [ ] Is error propagation appropriate (state vs exceptions)?

**After Execution:**
- [ ] Is actual output validated (not just absence of errors)?
- [ ] Are CloudWatch logs checked (not just status codes)?
- [ ] Is data persistence verified (round-trip test)?

### Common Validation Patterns

| Validation Type | Pattern | Detection |
|-----------------|---------|-----------|
| **Prerequisites** | `if not data or len(data) == 0: raise` | Check before processing |
| **Configuration** | Module-level `validate_config()` | Fail at startup |
| **Type Boundary** | `json.dumps(data)` at boundary | Explicit conversion |
| **Operation Outcome** | `if rowcount == 0: return False` | Check actual result |
| **Output Content** | `if not result.get('key'): raise` | Validate data exists |

---

## Testing Defensive Code

### Pattern: Sabotage Testing

After writing defensive code, verify it can detect failures:

```python
# Step 1: Write defensive code
def store_report(symbol: str, data: dict) -> bool:
    if not symbol or not data:
        raise ValueError("symbol and data required")

    rowcount = db.execute(query, params)
    if rowcount == 0:
        return False

    return True

# Step 2: Test validation catches failures
def test_store_report_rejects_empty_symbol(self):
    with pytest.raises(ValueError, match="symbol and data required"):
        store_report('', {'key': 'value'})

def test_store_report_detects_db_failure(self):
    mock_db.execute.return_value = 0  # Simulate failure
    result = store_report('NVDA19', {'key': 'value'})
    assert result is False

# Step 3: Sabotage - temporarily break defensive code
def store_report(symbol: str, data: dict) -> bool:
    # BUG: Removed validation
    rowcount = db.execute(query, params)
    return True  # BUG: Always returns True

# Step 4: Verify tests FAIL with sabotaged code
# If tests still pass, the tests are weak (The Liar pattern)
```

---

## References

- [Defensive Programming (NASA)](https://swehb.nasa.gov/display/7150/SWE-134+-+Defensive+Programming)
- [Fail Fast Principle](https://www.martinfowler.com/ieeeSoftware/failFast.pdf)
- [Type Safety at Boundaries](https://www.infoq.com/articles/contracts-at-boundaries/)
