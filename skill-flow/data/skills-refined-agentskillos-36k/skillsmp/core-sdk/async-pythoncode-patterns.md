---
name: async-pythoncode-patterns
description: "AsyncPythonCodeNode patterns and best practices including multi-output support (v0.9.30+), async I/O, concurrent processing, and full parity with PythonCodeNode. Use when asking 'AsyncPythonCodeNode', 'async Python', 'async code', 'concurrent processing', 'asyncio', 'async workflows', or 'async best practices'."
---

# AsyncPythonCodeNode Patterns

Comprehensive guide for AsyncPythonCodeNode with full PythonCodeNode feature parity (v0.9.30+).

> **Skill Metadata**
> Category: `core-sdk`
> Priority: `CRITICAL`
> SDK Version: `0.9.30+` (multi-output), `0.9.29+` (exceptions), `0.9.28+` (basic async)

## Quick Reference

- **Primary Use**: Async Python code execution with concurrent processing
- **Multi-Output**: ✅ FULLY SUPPORTED (v0.9.30+) - exports ALL variables like PythonCodeNode
- **Parity**: ✅ 100% feature parity with PythonCodeNode (v0.9.30+)
- **Use Cases**: Async I/O, database queries, HTTP requests, concurrent operations

## Feature Parity Status (v0.9.30+)

| Feature | PythonCodeNode | AsyncPythonCodeNode | Since |
|---------|----------------|---------------------|-------|
| Multi-output (export all variables) | ✅ | ✅ | v0.9.30 |
| Template resolution (nested params) | ✅ | ✅ | v0.9.30 |
| Exception handling (22 classes) | ✅ | ✅ | v0.9.29 |
| Module whitelists | ✅ | ✅ | v0.9.30 |
| Security sandbox | ✅ | ✅ | v0.9.28 |

**IMPORTANT**: Both nodes now behave identically. Choose based on async needs, not features!

## Multi-Output Pattern (v0.9.30+)

### Basic Multi-Output

```python
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()

# ✅ MODERN PATTERN: Export multiple variables
workflow.add_node("AsyncPythonCodeNode", "async_processor", {
    "code": """
import asyncio

# Async operation
async def process_data(items):
    await asyncio.sleep(0.1)
    return [item * 2 for item in items]

data = [1, 2, 3, 4, 5]
processed_data = await process_data(data)

# All variables automatically exported!
item_count = len(processed_data)
total_value = sum(processed_data)
processing_complete = True
average_value = total_value / item_count
    """
})

# Connect each output individually
workflow.add_connection("async_processor", "processed_data", "next_node", "data")
workflow.add_connection("async_processor", "item_count", "next_node", "count")
workflow.add_connection("async_processor", "total_value", "next_node", "total")
workflow.add_connection("async_processor", "processing_complete", "next_node", "status")
```

### Backward Compatibility

```python
# ✅ LEGACY PATTERN: Still works (single result)
workflow.add_node("AsyncPythonCodeNode", "legacy", {
    "code": """
async def process():
    await asyncio.sleep(0.1)
    return {"data": [1, 2, 3], "count": 3}

result = await process()
    """
})

# Access nested values with dot notation
workflow.add_connection("legacy", "result.data", "next", "input_data")
workflow.add_connection("legacy", "result.count", "next", "input_count")
```

## Concurrent Processing Patterns

### asyncio.gather - Parallel Execution

```python
workflow.add_node("AsyncPythonCodeNode", "parallel_fetch", {
    "code": """
import asyncio

async def fetch_item(id):
    await asyncio.sleep(0.1)  # Simulate I/O
    return {"id": id, "value": id * 10}

# Fetch multiple items concurrently
item_ids = [1, 2, 3, 4, 5]
tasks = [fetch_item(id) for id in item_ids]
results = await asyncio.gather(*tasks)

# Export results
fetched_items = results
success_count = len([r for r in results if r is not None])
fetch_complete = True
    """
})
```

### asyncio.create_task - Task Management

```python
workflow.add_node("AsyncPythonCodeNode", "task_manager", {
    "code": """
import asyncio

async def long_operation(data):
    await asyncio.sleep(1.0)
    return {"processed": data, "status": "complete"}

# Create task and continue
task = asyncio.create_task(long_operation(input_data))

# Do other work...
intermediate_result = "processing_started"

# Wait for task
final_result = await task

# Export multiple outputs
operation_result = final_result
operation_status = final_result["status"]
    """
})
```

## Async I/O Patterns

### HTTP Requests with aiohttp

```python
workflow.add_node("AsyncPythonCodeNode", "http_client", {
    "code": """
import aiohttp
import asyncio

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Fetch multiple APIs concurrently
api_urls = [
    "https://api.example.com/users",
    "https://api.example.com/products",
    "https://api.example.com/orders"
]

tasks = [fetch_url(url) for url in api_urls]
api_responses = await asyncio.gather(*tasks)

# Export results
users_data = api_responses[0]
products_data = api_responses[1]
orders_data = api_responses[2]
fetch_success = all(r is not None for r in api_responses)
    """
})
```

### Database Operations with asyncpg

```python
workflow.add_node("AsyncPythonCodeNode", "db_query", {
    "code": """
import asyncpg
import asyncio

# Connect to database
conn = await asyncpg.connect(database_url)

try:
    # Run multiple queries concurrently
    users_task = conn.fetch("SELECT * FROM users WHERE active = true")
    orders_task = conn.fetch("SELECT * FROM orders WHERE status = 'pending'")
    stats_task = conn.fetchrow("SELECT COUNT(*) as count FROM products")

    users, orders, stats = await asyncio.gather(users_task, orders_task, stats_task)

    # Export multiple results
    active_users = [dict(u) for u in users]
    pending_orders = [dict(o) for o in orders]
    product_count = stats['count']
    query_success = True
finally:
    await conn.close()
    """
})
```

### File Operations with aiofiles

```python
workflow.add_node("AsyncPythonCodeNode", "file_processor", {
    "code": """
import aiofiles
import asyncio

async def read_file(filepath):
    async with aiofiles.open(filepath, mode='r') as f:
        return await f.read()

async def write_file(filepath, content):
    async with aiofiles.open(filepath, mode='w') as f:
        await f.write(content)

# Read multiple files concurrently
file_paths = ["/data/file1.txt", "/data/file2.txt", "/data/file3.txt"]
read_tasks = [read_file(fp) for fp in file_paths]
file_contents = await asyncio.gather(*read_tasks)

# Process and write
combined_content = "\\n".join(file_contents)
await write_file("/output/combined.txt", combined_content)

# Export results
files_read = len(file_contents)
total_chars = sum(len(c) for c in file_contents)
processing_complete = True
    """
})
```

## DataFlow Integration (v0.9.30+)

### Dynamic DataFlow Updates with Async

```python
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()

# Async preparation with multi-output
workflow.add_node("AsyncPythonCodeNode", "async_prepare", {
    "code": """
import asyncio

# Simulate async data validation
async def validate_user(user_id):
    await asyncio.sleep(0.1)  # Simulate I/O
    return {"id": user_id, "verified": True, "premium": True}

user_data = await validate_user(current_user_id)

# Export multiple variables for DataFlow
filter_data = {"id": user_data["id"]}
verification_status = user_data["verified"]
premium_status = user_data["premium"]
updated_at = "2025-01-15T10:30:00Z"
    """
})

# Connect to DataFlow UpdateNode
workflow.add_node("UserUpdateNode", "update_user", {
    "db_instance": "my_db",
    "model_name": "User"
})

workflow.add_connection("async_prepare", "filter_data", "update_user", "filter")
workflow.add_connection("async_prepare", "verification_status", "update_user", "verified")
workflow.add_connection("async_prepare", "premium_status", "update_user", "premium")
workflow.add_connection("async_prepare", "updated_at", "update_user", "updated_at")
```

## When to Use AsyncPythonCodeNode

### ✅ USE AsyncPythonCodeNode FOR:

**Async I/O Operations:**
- Database queries (asyncpg, aiomysql, motor)
- HTTP requests (aiohttp, httpx)
- File operations (aiofiles)
- WebSocket connections
- Redis operations (redis.asyncio)

**Concurrent Processing:**
- Multiple API calls
- Batch database operations
- Parallel data fetching
- Multiple file operations

**Integration with Async Libraries:**
- FastAPI applications
- AsyncSQL operations
- Async message queues
- Async cache operations

### ❌ USE PythonCodeNode INSTEAD FOR:

**CPU-Bound Operations:**
- Data processing calculations
- pandas DataFrame operations
- numpy computations
- Statistical analysis

**Blocking I/O:**
- Visualization (matplotlib, seaborn, plotly)
- Synchronous libraries
- Simple calculations

**Simple Logic:**
- Basic conditionals
- Data transformations
- Simple mappings

## Exception Handling (v0.9.29+)

All exception classes are now available in AsyncPythonCodeNode:

```python
workflow.add_node("AsyncPythonCodeNode", "error_handler", {
    "code": """
import asyncio

try:
    # This will raise NameError if variable doesn't exist
    result = undefined_variable
except NameError as e:
    # ✅ NameError is now available (v0.9.29+)
    error_message = f"Variable not found: {e}"
    error_type = "NameError"
    has_error = True
except AttributeError as e:
    # ✅ AttributeError is now available
    error_message = f"Attribute error: {e}"
    error_type = "AttributeError"
    has_error = True
except ZeroDivisionError as e:
    # ✅ ZeroDivisionError is now available
    error_message = f"Division error: {e}"
    error_type = "ZeroDivisionError"
    has_error = True

# Export error info
error_occurred = has_error if 'has_error' in locals() else False
error_details = error_message if 'error_message' in locals() else None
    """
})
```

**Available Exceptions** (v0.9.29+):
- `NameError`, `AttributeError`, `ZeroDivisionError`
- `StopIteration`, `AssertionError`, `ImportError`
- `IOError`, `ArithmeticError`

## Template Resolution (v0.9.30+)

Template syntax `${param}` now works in nested parameters:

```python
workflow.add_node("AsyncPythonCodeNode", "templated", {
    "code": """
import asyncio

# Template resolution works in nested dicts/lists (v0.9.30+)
filter_config = {
    "id": user_id,  # From template resolution
    "status": status,  # From template resolution
    "metadata": {
        "source": source_system,  # Nested template resolution!
        "timestamp": timestamp
    }
}

# Use in async operation
async def query_data(config):
    await asyncio.sleep(0.1)
    return {"matched": 10, "config": config}

query_result = await query_data(filter_config)

# Export results
matched_count = query_result["matched"]
filter_used = query_result["config"]
    """
})
```

## Performance Best Practices

### Limit Concurrent Tasks

```python
workflow.add_node("AsyncPythonCodeNode", "controlled_concurrency", {
    "code": """
import asyncio

# Limit concurrent operations
semaphore = asyncio.Semaphore(5)  # Max 5 concurrent

async def limited_fetch(id):
    async with semaphore:
        await asyncio.sleep(0.1)
        return {"id": id, "data": f"result_{id}"}

# Process with concurrency limit
item_ids = range(100)
tasks = [limited_fetch(id) for id in item_ids]
results = await asyncio.gather(*tasks)

# Export results
processed_count = len(results)
processing_complete = True
    """
})
```

### Error Handling in Concurrent Operations

```python
workflow.add_node("AsyncPythonCodeNode", "error_resilient", {
    "code": """
import asyncio

async def safe_fetch(id):
    try:
        await asyncio.sleep(0.1)
        if id % 3 == 0:
            raise ValueError(f"Invalid ID: {id}")
        return {"id": id, "status": "success"}
    except Exception as e:
        return {"id": id, "status": "error", "error": str(e)}

# Gather with return_exceptions=False (default)
item_ids = range(10)
tasks = [safe_fetch(id) for id in item_ids]
results = await asyncio.gather(*tasks)

# Separate successes and errors
successful_items = [r for r in results if r["status"] == "success"]
failed_items = [r for r in results if r["status"] == "error"]

# Export results
success_count = len(successful_items)
error_count = len(failed_items)
processing_complete = True
    """
})
```

## Common Pitfalls

### ❌ WRONG: Blocking operations in async code

```python
# ❌ This blocks the event loop!
workflow.add_node("AsyncPythonCodeNode", "blocking", {
    "code": """
import time
await asyncio.sleep(0.1)
time.sleep(5)  # ❌ Blocks event loop!
result = "done"
    """
})
```

### ✅ CORRECT: Use async alternatives

```python
# ✅ This doesn't block
workflow.add_node("AsyncPythonCodeNode", "non_blocking", {
    "code": """
import asyncio
await asyncio.sleep(0.1)
await asyncio.sleep(5)  # ✅ Non-blocking
result = "done"
    """
})
```

## Related Skills

- **[pythoncode-best-practices](pythoncode-best-practices.md)** - PythonCodeNode patterns
- **[async-workflow-patterns](async-workflow-patterns.md)** - Async workflow design
- **[dataflow-dynamic-updates](../02-dataflow/dataflow-dynamic-updates.md)** - DataFlow with async
- **[runtime-execution](runtime-execution.md)** - Runtime patterns

## Version History

- **v0.9.30** (Oct 24, 2025): Multi-output support, template resolution, full parity
- **v0.9.29** (Oct 24, 2025): Exception handling (22 classes added)
- **v0.9.28** (Oct 24, 2025): Multi-output pattern introduced

## Keywords for Auto-Trigger

<!-- Trigger Keywords: AsyncPythonCodeNode, async Python, async code, concurrent processing, asyncio, async workflows, async best practices, async I/O, asyncpg, aiohttp, aiofiles -->
