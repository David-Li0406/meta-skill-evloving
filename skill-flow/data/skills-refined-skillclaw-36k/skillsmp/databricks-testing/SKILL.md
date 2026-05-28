---
name: databricks-testing
description: Execute code on Databricks clusters using MCP Command Execution API. Supports stateless quick validation and stateful iterative development. Use when testing Python/SQL code on clusters, debugging pipelines, or validating transformations.
allowed-tools:
  - Read
  - Grep
model: claude-sonnet-4-5-20250929
user-invocable: true
---

# Databricks Code Testing via MCP

Execute and test code directly on Databricks clusters using the Model Context Protocol (MCP) Command Execution API. This skill handles both quick validations and interactive development sessions.

## When to Use This Skill

- Testing notebook code before packaging in DABs
- Debugging data transformations on actual cluster
- Validating SQL queries against real data
- Iterative development with immediate feedback
- Verifying cluster has required libraries
- Quick proof-of-concept validation

## Core Concepts

### Stateless vs Stateful Execution

**Stateless** (`databricks_command` MCP tool):
- Single operation, automatic cleanup
- No state persistence between calls
- Best for: One-off SQL queries, simple validations
- Context created and destroyed automatically

**Stateful** (context-based execution):
- Multiple operations in same session
- Variables and imports persist across calls
- Best for: Multi-step workflows, iterative debugging
- Requires explicit context management

## Execution Workflows

### Workflow 1: Stateless Testing (Quick Validation)

Use when you need to run a single operation without maintaining state.

**Pattern:**
1. User provides code snippet and cluster_id
2. Use `databricks_command` MCP tool with:
   - `cluster_id`: Target Databricks cluster
   - `language`: "python" or "sql"
   - `code`: The code to execute
3. MCP automatically creates context, runs code, returns output
4. Context cleaned up automatically

**Example:**
```python
# User request: "Test this SQL query on my cluster"

# Code to execute:
SELECT COUNT(*) as total_records
FROM my_catalog.my_schema.transactions
WHERE date >= current_date() - INTERVAL 7 DAY
```

Claude calls `databricks_command` MCP tool → Executes on cluster → Returns result count.

### Workflow 2: Stateful Testing (Iterative Development)

Use when you need multiple operations that build on each other.

**Pattern:**
1. User provides code and cluster_id
2. Call `create_context` MCP tool:
   - `cluster_id`: Target cluster
   - `language`: "python" (default)
   - Returns: `context_id`
3. Call `execute_command_with_context` for each code block:
   - `cluster_id`: Same cluster
   - `context_id`: From step 2
   - `code`: Code to execute
   - Variables persist between calls
4. When done, call `destroy_context`:
   - `cluster_id`: Same cluster
   - `context_id`: To clean up

**Example:**
```python
# User request: "Test this multi-step data transformation"

# Step 1: Create context
context_id = create_context(cluster_id="0123-456789-abc123", language="python")

# Step 2: Load data (context persists)
execute_command_with_context(
    cluster_id="0123-456789-abc123",
    context_id=context_id,
    code="""
from pyspark.sql import functions as F

df = spark.table("my_catalog.my_schema.raw_data")
print(f"Loaded {df.count()} records")
"""
)

# Step 3: Transform (uses df from step 2)
execute_command_with_context(
    cluster_id="0123-456789-abc123",
    context_id=context_id,
    code="""
clean_df = df.filter(F.col("id").isNotNull()).dropDuplicates(["id"])
print(f"Clean records: {clean_df.count()}")
clean_df.show(5)
"""
)

# Step 4: Cleanup
destroy_context(cluster_id="0123-456789-abc123", context_id=context_id)
```

### Workflow 3: Debugging Pattern

Use for fixing code based on cluster errors.

**Pattern:**
1. Run code via MCP (stateless or stateful)
2. If error occurs, show full error message to user
3. Suggest fix based on error type
4. Re-run with fix
5. Iterate until successful

**Common Errors and Fixes:**

| Error Type | Cause | Solution |
|------------|-------|----------|
| `NameError` | Variable not defined | Check if using stateful context, ensure variable defined in prior call |
| `AnalysisException` | Table/column not found | Verify full table name (catalog.schema.table), check column spelling |
| `Py4JJavaError` | Spark operation failed | Check data types, null handling, add filters to reduce data |
| `Timeout (120s)` | Code took too long | Break into smaller chunks, add limits, optimize query |

## Best Practices

### 1. Always Return Complete Output
- Never summarize or truncate cluster output
- Users need full error messages for debugging
- Show complete stack traces
- Include all print statements and display() results

### 2. Test Incrementally
- Break large notebooks into smaller test blocks
- Validate each transformation step
- Don't submit entire notebooks at once
- Test with data limits first (e.g., `LIMIT 100`)

### 3. Use Stateful for Debugging
- When iterating on code, use stateful context
- Avoid reloading large datasets on each iteration
- Keep context alive during debugging session
- Clean up context when switching tasks

### 4. Clean Up Contexts
- Always destroy contexts when done
- Don't leave contexts hanging
- One context per debugging session
- If unsure, create fresh context

### 5. Add Print Statements
- Use `print()` liberally for debugging
- Show row counts after each transformation
- Display sample data with `.show(5)`
- Log progress in multi-step operations

## Execution Rules (from CLAUDE.md)

**Critical Rules:**
- MCP commands **run automatically** (no confirmation needed)
- **Never simulate** execution locally
- **Always use real cluster** for testing
- Return **complete output** to user
- **Iterate until working** based on real errors

## Integration with Other Skills

### Called By
- `databricks-ml-pipeline` - Tests ML training code
- `databricks-data-engineering` - Tests ETL transformations

### Leads To
- `databricks-bundle-deploy` - Once code works, package as DAB

### Works With
- `databricks-unity-catalog` - Tests against UC tables

## Code Examples

### Example 1: Quick SQL Validation

```python
# User: "Validate this aggregation query"

# Stateless execution via databricks_command
databricks_command(
    cluster_id="0123-456789-abc123",
    language="sql",
    code="""
    SELECT
        customer_id,
        COUNT(*) as order_count,
        SUM(amount) as total_spent
    FROM my_catalog.sales.orders
    WHERE order_date >= '2024-01-01'
    GROUP BY customer_id
    HAVING COUNT(*) > 5
    LIMIT 10
    """
)

# Returns: Query results with top 10 customers
```

### Example 2: Test Python Transformation

```python
# User: "Test this data cleaning code"

# Stateless execution
databricks_command(
    cluster_id="0123-456789-abc123",
    language="python",
    code="""
from pyspark.sql import functions as F

# Load sample
df = spark.table("my_catalog.bronze.raw_events").limit(1000)

# Clean
clean_df = (
    df
    .filter(F.col("event_id").isNotNull())
    .filter(F.col("timestamp").isNotNull())
    .withColumn("amount", F.col("amount").cast("double"))
)

print(f"Original: {df.count()} rows")
print(f"Clean: {clean_df.count()} rows")
print(f"Removed: {df.count() - clean_df.count()} rows")

clean_df.show(5)
"""
)

# Returns: Row counts and sample data
```

### Example 3: Iterative Feature Engineering

```python
# User: "Help me build features for ML model"

# Create stateful context
context_id = create_context(
    cluster_id="0123-456789-abc123",
    language="python"
)

# Step 1: Load and explore
execute_command_with_context(
    cluster_id="0123-456789-abc123",
    context_id=context_id,
    code="""
df = spark.table("my_catalog.ml.customer_data")
print(f"Total customers: {df.count()}")
print(f"Columns: {df.columns}")
df.describe().show()
"""
)

# Step 2: Create features (df persists from step 1)
execute_command_with_context(
    cluster_id="0123-456789-abc123",
    context_id=context_id,
    code="""
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Time-based features
w = Window.partitionBy("customer_id").orderBy("transaction_date")

features_df = (
    df
    .withColumn("days_since_last",
        F.datediff(F.current_date(), F.col("transaction_date")))
    .withColumn("transaction_count",
        F.count("*").over(w))
    .withColumn("avg_amount",
        F.avg("amount").over(w))
)

print("Features created:")
features_df.select("customer_id", "days_since_last", "transaction_count", "avg_amount").show(10)
"""
)

# Step 3: Validate features
execute_command_with_context(
    cluster_id="0123-456789-abc123",
    context_id=context_id,
    code="""
# Check for nulls
null_counts = features_df.select([
    F.sum(F.when(F.col(c).isNull(), 1).otherwise(0)).alias(c)
    for c in features_df.columns
])
print("Null counts by column:")
null_counts.show()

# Validate ranges
print("\\nFeature statistics:")
features_df.select("days_since_last", "transaction_count", "avg_amount").describe().show()
"""
)

# Cleanup
destroy_context(
    cluster_id="0123-456789-abc123",
    context_id=context_id
)
```

### Example 4: Library Validation

```python
# User: "Check if cluster has required libraries"

databricks_command(
    cluster_id="0123-456789-abc123",
    language="python",
    code="""
# Test imports
try:
    import pandas as pd
    import numpy as np
    import mlflow
    import sklearn
    print("✓ All required libraries available")
    print(f"  pandas: {pd.__version__}")
    print(f"  numpy: {np.__version__}")
    print(f"  mlflow: {mlflow.__version__}")
    print(f"  sklearn: {sklearn.__version__}")
except ImportError as e:
    print(f"✗ Missing library: {e}")
    print("  Use: %pip install <library>")

# Check Spark version
print(f"\\n✓ Spark version: {spark.version}")
"""
)

# Returns: Library versions or installation instructions
```

## Troubleshooting

### Issue: Context Not Found
**Error:** "Context with id X does not exist"

**Causes:**
- Context was already destroyed
- Context timed out (idle > 1 hour)
- Wrong cluster_id used

**Solution:**
- Create new context
- Use same cluster_id across all calls
- Don't reuse old context_ids

### Issue: Timeout (120 seconds)
**Error:** "Command timed out after 120 seconds"

**Causes:**
- Query too complex/slow
- Large dataset without limits
- Cluster cold start

**Solution:**
- Add `LIMIT` to queries during testing
- Break into smaller operations
- Use stateful context to avoid repeated loading
- Optimize query (filters, partitions)

### Issue: Variable Not Defined
**Error:** `NameError: name 'df' is not defined`

**Causes:**
- Using stateless when need stateful
- Variable defined in previous destroyed context
- Typo in variable name

**Solution:**
- Use stateful context for multi-step workflows
- Re-run code that defines variable
- Check variable spelling

## Security Reminders

- Never print or log access tokens
- Use environment variables for credentials
- Don't embed secrets in test code
- Use widget parameters, not hard-coded values

## Summary

This skill enables rapid testing and iteration on Databricks clusters via MCP:
- **Stateless** for quick validations
- **Stateful** for iterative development
- **Automatic** execution (no confirmation)
- **Complete** output (no summaries)
- **Real cluster** testing (never simulate)

Use this skill to validate code before packaging with `databricks-bundle-deploy`.
