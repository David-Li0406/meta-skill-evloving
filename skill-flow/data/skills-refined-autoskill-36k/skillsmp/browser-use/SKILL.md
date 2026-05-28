---
name: browser-use
description: "AI-powered browser automation for web scraping, form filling, data extraction, research, and any task requiring browser interaction. Executes natural language instructions as browser actions using vision and LLM reasoning in the cloud. Use when tasks require: (1) Navigating websites and extracting information, (2) Filling forms or interacting with web UIs, (3) Scraping data from multiple pages, (4) Automated web research, (5) Testing web applications, (6) Any task that would normally require manual browser use. Environment variable BROWSER_USE_API_KEY must be set."
license: Proprietary. LICENSE.txt has complete terms
---

# Browser Use Cloud Agent

## Overview

Browser Use provides AI-powered browser automation via cloud-managed browsers. The agent executes natural language instructions to navigate websites, interact with elements, extract data, and complete multi-step web tasks autonomously.

**Task flow**: Describe task in natural language -> Cloud agent executes browser actions -> Returns results/extracted data

## Quick Start

```python
from browser_use_sdk import BrowserUse

client = BrowserUse()  # Uses BROWSER_USE_API_KEY from environment

task = client.tasks.create_task(
    task="Find the top post on Hacker News and extract its title and URL",
    llm="browser-use-llm",
)
result = task.complete()
print(result.output)
```

Or use the provided script:

```bash
uv run skills/browser-use/scripts/execute_task.py "Find the top post on Hacker News" --json
```

**Note**: All tasks run on Browser Use Cloud which provides managed browsers. This requires `BROWSER_USE_API_KEY` to be set.

## Dispatching Browser Tasks

**Always dispatch an `external_ref` immediately after creating a browser task.** This enables the timeline to track the task and potentially display results later.

```python
from browser_use_sdk import BrowserUse
from fulcrum_sdk._internal.dispatch import get_dispatch_client

client = BrowserUse()
task = client.tasks.create_task(
    task="Find the top post on Hacker News and extract its title and URL",
    llm="browser-use-llm",
)

# Dispatch immediately after task creation (id is available on task object)
dispatch = get_dispatch_client()
dispatch.dispatch_external_ref(
    summary="Browser task created",
    provider="browser-use",
    ref_type="task",
    ref_id=task.id,  # Available immediately from create_task response
)

result = task.complete()
print(result.output)
```

**Key points:**
- Dispatch **immediately** after `create_task` (before calling `complete()`)
- Use `task.id` which is available right after task creation
- Provider is `"browser-use"`, ref_type is `"task"`
- Include a descriptive summary of what the task does

## LLM Selection

| Model | API String | Cost/Step | Best For |
|-------|------------|-----------|----------|
| Browser Use LLM | `browser-use-llm` | $0.002 | Default - fast, cheapest |
| Gemini 3 Pro Preview | `gemini-3-pro-preview` | $0.03 | Complex tasks |
| Claude Opus 4.5 | `claude-opus-4-5-20251101` | $0.10 | Hardest tasks, maximum quality |

**Recommendation**: Start with `browser-use-llm` (default). Upgrade to `gemini-3-pro-preview` for complex multi-step tasks. Use `claude-opus-4-5-20251101` only for the most challenging tasks requiring maximum reasoning.

## Core Patterns

### 1. Simple Task Execution

```python
from browser_use_sdk import BrowserUse

client = BrowserUse()
task = client.tasks.create_task(
    task="Search Google for 'Python web scraping' and list the top 5 results",
    llm="browser-use-llm",
)
result = task.complete()
print(result.output)
```

### 2. Structured Output

Extract typed data using Pydantic models:

```python
from browser_use_sdk import BrowserUse
from pydantic import BaseModel
from typing import List

class Article(BaseModel):
    title: str
    url: str
    points: int

class HNResults(BaseModel):
    articles: List[Article]

client = BrowserUse()
task = client.tasks.create_task(
    task="Get the top 10 articles from Hacker News with title, URL, and points",
    llm="browser-use-llm",
    schema=HNResults,
)
result = task.complete()
data = result.parsed_output  # HNResults instance
```

### 3. Domain-Restricted Tasks

Include domain restrictions in the task description:

```python
task = client.tasks.create_task(
    task="Find Python async examples. Only visit github.com and stackoverflow.com domains.",
    llm="browser-use-llm",
)
```

### 4. Form Filling

```python
task = client.tasks.create_task(
    task="""
    Go to example.com/contact and fill out the form:
    - Name: John Smith
    - Email: john@example.com
    - Message: Hello, I have a question about your services
    Then submit the form
    """,
    llm="browser-use-llm",
)
```

### 5. Handling Sensitive Data (Logins, Credentials)

Use the `secrets` parameter to securely pass credentials. The LLM sees only placeholders - actual values are injected by the browser agent at runtime.

```python
task = client.tasks.create_task(
    task="Go to example.com/login, enter {{username}} and {{password}}, then click Login",
    secrets={
        "username": "my_actual_username",
        "password": "my_actual_password",
    },
    llm="browser-use-llm",
)
```

Or via CLI:

```bash
uv run skills/browser-use/scripts/execute_task.py \
    "Log into example.com with {{username}} and {{password}}" \
    --secrets '{"username": "user", "password": "pass"}'
```

**Key points:**
- Use `{{key}}` placeholders in your task string
- Pass actual values via the `secrets` dict
- The LLM never sees the real credentials
- Values are injected when the browser fills form fields

### 6. Multi-Page Scraping

```python
from browser_use_sdk import AsyncBrowserUse
import asyncio

async def scrape_articles():
    client = AsyncBrowserUse()
    task = await client.tasks.create_task(
        task="""
        1. Go to news.ycombinator.com
        2. Open the top 5 articles in new tabs
        3. Extract the title and first paragraph from each
        4. Return the results as a list
        """,
        llm="browser-use-llm",
    )
    result = await task.complete()
    return result.output

asyncio.run(scrape_articles())
```

## Streaming Progress

Monitor task execution in real-time:

```python
from browser_use_sdk import AsyncBrowserUse
import asyncio

async def main():
    client = AsyncBrowserUse()
    task = await client.tasks.create_task(
        task="Research Python web frameworks and compare their features",
        llm="browser-use-llm",
    )

    # Stream progress updates
    async for step in task.stream():
        print(f"Step {step.number}: {step.url} - {step.next_goal}")

    result = await task.complete()
    print(result.output)

asyncio.run(main())
```

## Scripts

### execute_task.py

Complete browser task execution with progress streaming:

```bash
uv run skills/browser-use/scripts/execute_task.py "Find Python jobs on HN" \
    --timeout 30 \
    --json
```

| Option | Default | Description |
|--------|---------|-------------|
| `--output-schema` | None | JSON schema file for structured output |
| `--save-screenshots` | False | Save screenshots if available |
| `--output-dir` | output/ | Directory for output files |
| `--timeout` | 15 | Task timeout in minutes |
| `--llm` | browser-use-llm | LLM model to use |
| `--json` | False | Output as JSON |
| `--secrets` | None | JSON dict for credential injection (see section 5) |

## Use Cases

### Web Research

```bash
uv run skills/browser-use/scripts/execute_task.py \
    "Research the top 5 Python web frameworks in 2024, find their GitHub stars and latest version" \
    --json
```

### Price Monitoring

```bash
uv run skills/browser-use/scripts/execute_task.py \
    "Go to amazon.com and find the current price of 'Python Crash Course' book" \
    --json
```

### Form Automation

```bash
uv run skills/browser-use/scripts/execute_task.py \
    "Go to typeform.com/templates and sign up for their newsletter with test@example.com"
```

### Competitive Analysis

```bash
uv run skills/browser-use/scripts/execute_task.py \
    "Visit competitor.com and extract their pricing tiers, features, and target audience" \
    --json
```

## Data Extraction with Claude

For complex extraction from browser results, combine with the Claude skill:

```python
from browser_use_sdk import BrowserUse
from anthropic import Anthropic
import json

# Step 1: Browser extracts raw content
client = BrowserUse()
task = client.tasks.create_task(
    task="Go to techcrunch.com and extract all article headlines from the homepage",
    llm="browser-use-llm",
)
result = task.complete()
raw_content = result.output

# Step 2: Claude structures the data
claude = Anthropic()
message = claude.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=2048,
    temperature=0,
    system="""Extract article data and return JSON array:
    [{"title": string, "category": string, "is_featured": boolean}]""",
    messages=[{"role": "user", "content": raw_content}],
)
articles = json.loads(message.content[0].text)
```

## Error Handling

```python
from browser_use_sdk import BrowserUse

client = BrowserUse()

try:
    task = client.tasks.create_task(
        task="Extract data from website",
        llm="browser-use-llm",
    )
    result = task.complete()

    if result.output:
        print(result.output)
    else:
        print("No output received")

except Exception as e:
    print(f"Task failed: {e}")
```

### Common Issues

| Issue | Solution |
|-------|----------|
| API key missing | Set `BROWSER_USE_API_KEY` environment variable |
| Timeout | Increase `--timeout` or simplify task |
| No results | Make task more specific, use numbered steps |
| Captcha blocking | Cloud handles most captchas automatically |

## Best Practices

### Task Writing

1. **Be specific**: "Click the blue 'Sign Up' button" not "click sign up"
2. **Use numbered steps** for multi-step tasks
3. **Include fallbacks**: "If not found, try searching for..."
4. **Specify output format**: "Return results as a JSON array"

### Performance

1. Use appropriate timeout for complex tasks
2. Use structured output (Pydantic schemas) for typed results
3. Include domain restrictions in task when applicable

### Reliability

1. Add error handling around task execution
2. Use streaming to monitor progress
3. Save results to output directory for debugging

## References

For detailed API documentation, see [references/api_reference.md](references/api_reference.md).
