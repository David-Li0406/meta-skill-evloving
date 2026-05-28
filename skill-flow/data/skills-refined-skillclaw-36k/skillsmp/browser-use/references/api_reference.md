# Browser Use Cloud SDK Reference

## Table of Contents

1. [Client Initialization](#client-initialization)
2. [Task Creation](#task-creation)
3. [Task Execution](#task-execution)
4. [Result Object](#result-object)
5. [Streaming](#streaming)
6. [Structured Output](#structured-output)
7. [Error Handling](#error-handling)

---

## Client Initialization

### Synchronous Client

```python
from browser_use_sdk import BrowserUse

client = BrowserUse()  # Uses BROWSER_USE_API_KEY from environment
# or
client = BrowserUse(api_key="bu_...")
```

### Asynchronous Client

```python
from browser_use_sdk import AsyncBrowserUse

client = AsyncBrowserUse()  # Uses BROWSER_USE_API_KEY from environment
# or
client = AsyncBrowserUse(api_key="bu_...")
```

---

## Task Creation

### create_task Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `task` | `str` | Yes | Natural language task description |
| `llm` | `str` | No | LLM model (default: "browser-use-llm") |
| `schema` | `BaseModel` | No | Pydantic model for structured output |
| `secrets` | `Dict[str, str]` | No | Secrets for credential injection. Use `{{key}}` placeholders in task. |

### Available LLM Models

| Model | API String | Cost/Step | Best For |
|-------|------------|-----------|----------|
| Browser Use LLM | `browser-use-llm` | $0.002 | Default - fast, cheapest |
| Gemini 2.5 Flash | `gemini-2.5-flash` | $0.0075 | Fast, good value |
| GPT-4.1 | `gpt-4.1` | $0.025 | Good balance |
| Gemini 3 Pro Preview | `gemini-3-pro-preview` | $0.03 | Complex tasks |
| Claude Sonnet 4.5 | `claude-sonnet-4-5-20250929` | $0.05 | Nuanced understanding |
| Claude Opus 4.5 | `claude-opus-4-5-20251101` | $0.10 | Hardest tasks, maximum quality |

### Sync Example

```python
task = client.tasks.create_task(
    task="Find the top article on Hacker News",
    llm="browser-use-llm",
)
```

### Async Example

```python
task = await client.tasks.create_task(
    task="Find the top article on Hacker News",
    llm="browser-use-llm",
)
```

---

## Task Execution

### complete()

Waits for task completion and returns the result.

**Sync:**
```python
result = task.complete()
```

**Async:**
```python
result = await task.complete()
```

---

## Result Object

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | `str` | Task ID |
| `output` | `str` | Text output from task |
| `parsed_output` | `BaseModel\|None` | Structured output if schema provided |

### Usage

```python
result = task.complete()

print(result.id)        # Task identifier
print(result.output)    # Text result

if result.parsed_output:
    data = result.parsed_output.model_dump()  # Dict from Pydantic model
```

---

## Streaming

Monitor task progress in real-time with async streaming.

### stream()

Returns an async iterator yielding step updates.

```python
async for step in task.stream():
    print(f"Step {step.number}: {step.next_goal}")
```

### Step Properties

| Property | Type | Description |
|----------|------|-------------|
| `number` | `int` | Step number |
| `url` | `str\|None` | Current page URL |
| `next_goal` | `str\|None` | What the agent is doing next |

### Full Example

```python
from browser_use_sdk import AsyncBrowserUse
import asyncio

async def main():
    client = AsyncBrowserUse()
    task = await client.tasks.create_task(
        task="Research Python frameworks",
        llm="browser-use-llm",
    )

    # Stream progress
    async for step in task.stream():
        print(f"Step {step.number}: {step.url} - {step.next_goal}")

    # Get final result
    result = await task.complete()
    print(result.output)

asyncio.run(main())
```

---

## Structured Output

Use Pydantic models to get typed, validated responses.

### Defining a Schema

```python
from pydantic import BaseModel
from typing import List

class Article(BaseModel):
    title: str
    url: str
    points: int

class SearchResults(BaseModel):
    articles: List[Article]
```

### Using the Schema

```python
task = client.tasks.create_task(
    task="Get top 5 Hacker News articles with title, URL, and points",
    schema=SearchResults,
    llm="browser-use-llm",
)

result = task.complete()
data = result.parsed_output  # SearchResults instance

for article in data.articles:
    print(f"{article.title}: {article.url} ({article.points} points)")
```

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Missing API key | `BROWSER_USE_API_KEY` not set | Set environment variable |
| Rate limit | Too many requests | Wait and retry |
| Timeout | Task took too long | Simplify task or increase timeout |
| Invalid task | Malformed request | Check task description |

### Error Handling Pattern

```python
from browser_use_sdk import BrowserUse
import os

# Check API key first
if not os.environ.get("BROWSER_USE_API_KEY"):
    raise ValueError("BROWSER_USE_API_KEY must be set")

client = BrowserUse()

try:
    task = client.tasks.create_task(
        task="Extract data from website",
        llm="browser-use-llm",
    )
    result = task.complete()
    print(result.output)

except Exception as e:
    print(f"Task failed: {e}")
```

### Webhook Verification

For webhook integrations, verify signatures:

```python
from browser_use_sdk import verify_webhook_event_signature

verified = verify_webhook_event_signature(
    body=request_body,
    timestamp=timestamp_header,
    secret=webhook_secret,
    expected_signature=signature_header,
)
```
