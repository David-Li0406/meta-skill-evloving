# Research Workflow

Step-by-step research processes for common scenarios.

**Principle:** Follow systematic methodology—don't skip steps.

---

## Workflow 1: Bug Persists After 2 Attempts

**Context:** You've tried 2 fixes, both failed. Time to research.

### Step 1: Collect Evidence (5 minutes)

```bash
# Create investigation directory
mkdir bug-investigation-$(date +%Y%m%d-%H%M%S)
cd bug-investigation-*

# Save error logs
aws logs filter-log-events \
  --log-group-name /aws/lambda/worker \
  --start-time $(($(date +%s) - 3600))000 \
  --filter-pattern "ERROR" > error-logs.json

# Save successful logs (for comparison)
aws logs filter-log-events \
  --log-group-name /aws/lambda/worker \
  --start-time $(($(date +%s) - 3600))000 \
  --filter-pattern "SUCCESS" > success-logs.json

# Get recent deployments
git log --oneline -10 > recent-commits.txt

# Save current code state
git diff HEAD~2 > changes-last-2-commits.diff
```

### Step 2: Formulate Hypotheses (10 minutes)

**Ask:**
1. What changed recently? (Check `changes-last-2-commits.diff`)
2. What's the exact error message? (Check `error-logs.json`)
3. Does it fail consistently or intermittently?
4. Does it fail for all inputs or specific ones?

**Example:**

```bash
# Analyze error logs
cat error-logs.json | jq -r '.events[].message' | grep -i "error"

# Output: "TypeError: not all arguments converted"

# Hypothesis 1: Type mismatch in database query parameters
# Hypothesis 2: JSON serialization issue
# Hypothesis 3: NumPy/Pandas type not converted
```

### Step 3: Read Primary Sources (15 minutes)

**For each hypothesis, read official documentation:**

```bash
# Hypothesis 1: PyMySQL parameter types
open https://pymysql.readthedocs.io/en/latest/modules/cursors.html

# Look for:
# - How to pass parameters?
# - What types are accepted?
# - Any special handling for JSON/dict?

# Take notes
cat > hypothesis1-notes.md << 'EOF'
PyMySQL Documentation Findings:
- execute() accepts parameters as tuple
- Dict types must be serialized to JSON string manually
- %s placeholder does NOT auto-convert dicts

Conclusion: Need json.dumps() for dict parameters
EOF
```

### Step 4: Reproduce Locally (20 minutes)

```python
# test_hypothesis.py
import pymysql
import json

def test_dict_parameter():
    """Test if PyMySQL accepts dict for JSON column"""

    conn = pymysql.connect(host='127.0.0.1', port=3307, user='admin', password='***', database='test')
    cursor = conn.cursor()

    # Create test table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_json (
            id INT PRIMARY KEY AUTO_INCREMENT,
            data JSON
        )
    """)

    test_data = {'key': 'value', 'nested': {'foo': 'bar'}}

    # Test 1: Raw dict (hypothesis: will fail)
    print("Test 1: Raw dict")
    try:
        cursor.execute("INSERT INTO test_json (data) VALUES (%s)", (test_data,))
        print("✅ Raw dict accepted")
    except TypeError as e:
        print(f"❌ Raw dict rejected: {e}")

    # Test 2: JSON string (hypothesis: will succeed)
    print("\nTest 2: JSON string")
    try:
        cursor.execute("INSERT INTO test_json (data) VALUES (%s)", (json.dumps(test_data),))
        print("✅ JSON string accepted")
        conn.commit()
    except Exception as e:
        print(f"❌ JSON string rejected: {e}")

    # Verify
    cursor.execute("SELECT data FROM test_json WHERE id = LAST_INSERT_ID()")
    result = cursor.fetchone()
    print(f"\nRetrieved: {result}")

    # Cleanup
    cursor.execute("DROP TABLE test_json")
    conn.close()

if __name__ == '__main__':
    test_hypothesis()
```

**Run test:**

```bash
python3 test_hypothesis.py

# Output:
# Test 1: Raw dict
# ❌ Raw dict rejected: not all arguments converted
#
# Test 2: JSON string
# ✅ JSON string accepted
# Retrieved: ('{"key": "value", "nested": {"foo": "bar"}}',)
```

**Conclusion:** Hypothesis 1 confirmed. Need `json.dumps()`.

### Step 5: Apply Fix with Confidence (5 minutes)

```python
# src/telegram/services/precompute_service.py

def store_report(self, symbol: str, report_json: dict) -> bool:
    """Store precomputed report to Aurora."""

    query = """
        INSERT INTO precomputed_reports (symbol, report_json, created_at)
        VALUES (%s, %s, NOW())
        ON DUPLICATE KEY UPDATE
            report_json = VALUES(report_json),
            updated_at = NOW()
    """

    # FIX: Convert dict to JSON string (researched and confirmed)
    result = self.db_client.execute(
        query,
        (symbol, json.dumps(report_json))  # ← Added json.dumps()
    )

    return result > 0  # Returns True if rows affected
```

### Step 6: Verify Fix (5 minutes)

```bash
# Run tests
pytest tests/telegram/services/test_precompute_service.py -v

# Deploy to dev
git add .
git commit -m "fix: Convert dict to JSON string for PyMySQL

Root cause: PyMySQL does not auto-serialize dicts for JSON columns.
Research: Confirmed via PyMySQL docs + local reproduction.
Fix: Use json.dumps() before passing to execute()."

git push origin dev

# Monitor for errors
aws logs tail /aws/lambda/worker-dev --follow --filter-pattern "ERROR"
```

**Total Time:** 60 minutes (vs 120+ minutes with blind iteration)

---

## Workflow 2: Unfamiliar Codebase

**Context:** Need to add feature to code you've never seen.

### Step 1: Find Entry Point (5 minutes)

```bash
# Search for likely entry points
rg "def lambda_handler" --type py
rg "def main" --type py
rg "@click.command" --type py
rg "app = FastAPI" --type py

# For Telegram API, found:
# src/telegram/api/app.py:8:app = FastAPI()
```

### Step 2: Trace Request Flow (15 minutes)

```bash
# Follow the flow from API → Service → Workflow → Data

# 1. Find route for feature
rg "\/api\/reports" src/telegram/api/

# Output: src/telegram/api/routes/reports.py:12:@router.post("/api/reports")

# 2. Read route
cat src/telegram/api/routes/reports.py | head -30

# Output shows: calls ReportService.generate_report()

# 3. Find service
rg "class ReportService" src/

# Output: src/telegram/services/report_service.py:15:class ReportService

# 4. Read service
cat src/telegram/services/report_service.py | head -50

# Output shows: calls workflow.run(state)

# 5. Find workflow
rg "class.*Workflow" src/workflow/

# Output: src/workflow/graph.py:20:class WorkflowGraph
```

**Draw flow diagram:**

```
User Request
    ↓
FastAPI Route (/api/reports)
    ↓
ReportService.generate_report()
    ↓
WorkflowGraph.run(AgentState)
    ↓
├─ fetch_ticker_data()
├─ analyze_technical()
├─ fetch_news()
├─ generate_report()
└─ score_report()
    ↓
Return report_json
```

### Step 3: Read Tests for Usage Examples (10 minutes)

```bash
# Tests show how to use the code
rg "test.*generate_report" tests/ --type py

# Read relevant test
cat tests/telegram/services/test_report_service.py

# Learn from test:
def test_generate_report_success(self, mock_workflow):
    """Shows how to call generate_report()"""

    # Input format
    ticker = "NVDA19"

    # Expected mocks
    mock_workflow.run.return_value = {
        'ticker': 'NVDA19',
        'report_text': 'Analysis...',
        'report_json': {...}
    }

    # How to call
    service = ReportService()
    result = service.generate_report(ticker)

    # Expected output
    assert result['ticker'] == 'NVDA19'
    assert 'report_text' in result
```

### Step 4: Check Git History (10 minutes)

```bash
# Why was this code written?
git log --oneline src/telegram/services/report_service.py | head -10

# Read relevant commits
git show abc123def
# Commit message: "feat: Add precompute service for caching reports"
# Shows: Original design intent

# Find related PRs
gh pr list --search "precompute" --state closed

# Read PR description
gh pr view 123
# Shows: Architecture decisions, trade-offs, alternatives considered
```

### Step 5: Identify Extension Point (5 minutes)

```bash
# Where to add new feature?

# Current flow:
# API → Service → Workflow → [Add feature here?]

# Check if similar feature exists
rg "user_facing_scores" src/

# Output shows: Already computed in workflow_nodes.py

# Read existing pattern
cat src/workflow/workflow_nodes.py | grep -A 20 "user_facing_scores"

# Pattern found:
def score_report(state: AgentState) -> AgentState:
    """Score report for user display"""

    # Extract data from state
    ticker_data = state['ticker_data']

    # Calculate scores
    scores = {
        'momentum_score': calculate_momentum(ticker_data),
        'value_score': calculate_value(ticker_data)
    }

    # Add to state
    state['user_facing_scores'] = scores
    return state
```

### Step 6: Implement Following Pattern (10 minutes)

```python
# src/workflow/workflow_nodes.py

def score_report(state: AgentState) -> AgentState:
    """Score report for user display"""

    # Existing code...

    # NEW FEATURE: Add sentiment score
    sentiment_score = calculate_sentiment(state.get('news_articles', []))

    scores = {
        'momentum_score': calculate_momentum(ticker_data),
        'value_score': calculate_value(ticker_data),
        'sentiment_score': sentiment_score  # ← New score
    }

    state['user_facing_scores'] = scores
    return state

def calculate_sentiment(articles: list) -> float:
    """Calculate sentiment score from news articles"""
    if not articles:
        return 0.0

    # Implementation...
    return sentiment_value
```

**Total Time:** 55 minutes (systematic exploration)

---

## Workflow 3: Technology Evaluation

**Context:** Choosing between alternatives (e.g., which database, which library).

### Step 1: Define Requirements (10 minutes)

```markdown
# requirements.md

## Use Case
Store and retrieve 365-day price history for 46 tickers.

## Functional Requirements
- Query by ticker symbol
- Sort by date
- Return as JSON

## Non-Functional Requirements
- Latency: < 100ms per query
- Cost: < $50/month
- Maintenance: Minimal ops overhead
- Scalability: Support 1000 req/min

## Nice to Have
- SQL interface (for ad-hoc queries)
- Automatic backups
- Regional availability (ap-southeast-1)
```

### Step 2: Research Alternatives (30 minutes)

**Option 1: Aurora Serverless MySQL**

```bash
# Read official docs
open https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.html

# Take notes:
# - Pros: SQL interface, automatic scaling, backups
# - Cons: $0.12/ACU-hour (min 0.5 ACU = ~$44/month)
# - Latency: ~10ms
# - Scalability: Up to 128 ACUs

# Check version compatibility
aws rds describe-db-engine-versions \
  --engine aurora-mysql \
  --query 'DBEngineVersions[].EngineVersion'
```

**Option 2: DynamoDB**

```bash
# Read official docs
open https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html

# Take notes:
# - Pros: Serverless, pay-per-request, single-digit ms latency
# - Cons: No SQL, requires partition key design
# - Latency: ~5ms
# - Scalability: Unlimited
# - Cost: $0.25/GB storage + $1.25/million requests
```

### Step 3: Prototype with Real Use Case (60 minutes)

**Aurora Prototype:**

```python
# test_aurora.py
import pymysql
import time

def test_aurora_performance():
    conn = pymysql.connect(host='aurora-endpoint', user='admin', password='***', database='test')
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
        CREATE TABLE price_history (
            ticker VARCHAR(10),
            date DATE,
            price DECIMAL(10,2),
            PRIMARY KEY (ticker, date)
        )
    """)

    # Insert 365 days * 46 tickers = 16,790 rows
    start = time.time()
    for ticker in TICKERS:
        for day in range(365):
            cursor.execute(
                "INSERT INTO price_history VALUES (%s, %s, %s)",
                (ticker, date_from_offset(day), random_price())
            )
    conn.commit()
    insert_time = time.time() - start

    # Query performance
    start = time.time()
    cursor.execute("SELECT * FROM price_history WHERE ticker = %s ORDER BY date", ('NVDA19',))
    result = cursor.fetchall()
    query_time = time.time() - start

    print(f"Insert time: {insert_time:.2f}s")
    print(f"Query time: {query_time * 1000:.2f}ms")

    cursor.execute("DROP TABLE price_history")
    conn.close()

# Results:
# Insert time: 12.3s
# Query time: 8.5ms
```

**DynamoDB Prototype:**

```python
# test_dynamodb.py
import boto3
import time

def test_dynamodb_performance():
    dynamodb = boto3.resource('dynamodb')

    # Create table
    table = dynamodb.create_table(
        TableName='price_history',
        KeySchema=[
            {'AttributeName': 'ticker', 'KeyType': 'HASH'},
            {'AttributeName': 'date', 'KeyType': 'RANGE'}
        ],
        BillingMode='PAY_PER_REQUEST'
    )

    # Insert data
    start = time.time()
    with table.batch_writer() as batch:
        for ticker in TICKERS:
            for day in range(365):
                batch.put_item(Item={
                    'ticker': ticker,
                    'date': date_from_offset(day),
                    'price': random_price()
                })
    insert_time = time.time() - start

    # Query performance
    start = time.time()
    response = table.query(
        KeyConditionExpression='ticker = :ticker',
        ExpressionAttributeValues={':ticker': 'NVDA19'}
    )
    query_time = time.time() - start

    print(f"Insert time: {insert_time:.2f}s")
    print(f"Query time: {query_time * 1000:.2f}ms")

    table.delete()

# Results:
# Insert time: 4.1s (faster!)
# Query time: 3.2ms (faster!)
```

### Step 4: Compare Trade-Offs (15 minutes)

| Criteria | Aurora | DynamoDB | Winner |
|----------|--------|----------|--------|
| **Latency** | 8.5ms | 3.2ms | DynamoDB |
| **Cost (monthly)** | ~$44 | ~$6 | DynamoDB |
| **SQL Support** | ✅ Yes | ❌ No | Aurora |
| **Ops Overhead** | Low | None | DynamoDB |
| **Scalability** | Up to 128 ACU | Unlimited | DynamoDB |
| **Flexibility** | SQL queries | Key-value only | Aurora |

**Decision Matrix:**

```
Priority 1: Latency (3.2ms vs 8.5ms) → DynamoDB wins
Priority 2: Cost ($6 vs $44) → DynamoDB wins
Priority 3: SQL flexibility → Aurora wins (but not essential)

WINNER: DynamoDB
```

### Step 5: Document Decision (10 minutes)

```markdown
# docs/adr/011-use-dynamodb-for-price-history.md

# ADR 011: Use DynamoDB for Price History Storage

## Context
Need to store and retrieve 365-day price history for 46 tickers with <100ms latency.

## Decision
Use DynamoDB with partition key `ticker` and sort key `date`.

## Consequences

**Positive:**
- ✅ 3.2ms latency (vs 8.5ms for Aurora)
- ✅ $6/month cost (vs $44 for Aurora)
- ✅ Zero ops overhead
- ✅ Unlimited scalability

**Negative:**
- ❌ No SQL interface (must use DynamoDB query API)
- ❌ Less flexible for ad-hoc analysis

**Mitigation:**
- Use PartiQL for SQL-like queries when needed
- Export to S3 for ad-hoc analysis

## Alternatives Considered
- Aurora Serverless v2: Higher latency, higher cost, but SQL support
```

**Total Time:** 125 minutes (thorough evaluation)

---

## Quick Reference

### Research Workflow Selection

| Scenario | Workflow | Time Budget |
|----------|----------|-------------|
| **Bug after 2 attempts** | Workflow 1 | 60 minutes |
| **Unfamiliar codebase** | Workflow 2 | 55 minutes |
| **Technology decision** | Workflow 3 | 125 minutes |
| **Production incident** | See INVESTIGATION-CHECKLIST.md | Variable |

---

## References

- [The Scientific Method of Troubleshooting](https://www.brendangregg.com/blog/2016-02-08/linux-load-averages.html)
- [Systems Performance Methodology](https://www.brendangregg.com/methodology.html)
- [Google SRE: Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/)
