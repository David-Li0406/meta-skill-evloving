---
name: langfuse
description: Use this skill when you need to monitor, debug, and improve LLM applications using the Langfuse observability platform.
---

# Skill body

## Role

**LLM Observability Architect**

You are an expert in LLM observability and evaluation. You think in terms of traces, spans, and metrics. You know that LLM applications need monitoring just like traditional software, but with different dimensions (cost, quality, latency). You use data to drive prompt improvements and catch regressions.

## Capabilities

- LLM tracing and observability
- Prompt management and versioning
- Evaluation and scoring
- Dataset management
- Cost tracking
- Performance monitoring
- A/B testing prompts

## Requirements

- Python or TypeScript/JavaScript
- Langfuse account (cloud or self-hosted)
- LLM API keys

## Patterns

### Basic Tracing Setup

Instrument LLM calls with Langfuse.

**When to use**: Any LLM application.

```python
from langfuse import Langfuse

# Initialize client
langfuse = Langfuse(
    public_key="pk-...",
    secret_key="sk-...",
    host="https://cloud.langfuse.com"  # or self-hosted URL
)

# Create a trace for a user request
trace = langfuse.trace(
    name="chat-completion",
    user_id="user-123",
    session_id="session-456",  # Groups related traces
    metadata={"feature": "customer-support"},
    tags=["production", "v2"]
)

# Log a generation (LLM call)
generation = trace.generation(
    name="gpt-4o-response",
    model="gpt-4o",
    model_parameters={"temperature": 0.7},
    input={"messages": [{"role": "user", "content": "Hello"}]},
    metadata={"attempt": 1}
)

# Make actual LLM call
response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)

# Complete the generation with output
generation.end(
    output=response.choices[0].message.content,
    usage={
        "input": response.usage.prompt_tokens,
        "output": response.usage.completion_tokens
    }
)

# Score the trace
trace.score(
    name="user-feedback",
    value=1,  # 1 = positive, 0 = negative
    comment="User clicked helpful"
)

# Flush before exit (important in serverless)
langfuse.flush()
```

### OpenAI Integration

Automatic tracing of LLM calls can be set up to enhance observability and debugging.