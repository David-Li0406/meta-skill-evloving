---
name: claude
description: "AI-powered natural language processing, text generation, JSON extraction from unstructured data, and image analysis using the Anthropic Claude API. Use when tasks require: (1) Writing or processing natural language text, (2) Extracting structured JSON from unstructured content, (3) Analyzing or describing images, (4) Generating human-readable content, (5) Summarizing or transforming text, (6) Any task requiring LLM intelligence. Environment variable ANTHROPIC_API_KEY must be set."
license: "© 2025 Daisyloop Technologies Inc. See LICENSE.txt"
---

# Claude API Integration

## Overview

This skill provides integration with Anthropic's Claude API for natural language processing, text generation, structured data extraction, and image analysis. Use the provided scripts or write custom implementations following the patterns below.

## Quick Start

```python
from anthropic import Anthropic

client = Anthropic()  # Uses ANTHROPIC_API_KEY from environment

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}]
)
print(message.content[0].text)
```

## Model Selection

Choose the appropriate model based on task complexity and cost considerations:

| Model | Use Case | Cost | Speed |
|-------|----------|------|-------|
| `claude-3-5-haiku-20241022` | Simple tasks, high volume, low latency | Lowest | Fastest |
| `claude-sonnet-4-5-20250929` | Balanced performance, coding, general tasks | Medium | Medium |
| `claude-opus-4-5-20251101` | Complex reasoning, nuanced analysis, maximum quality | Highest | Slowest |

**Selection guidelines:**
- **Haiku**: Data extraction, simple Q&A, classification, formatting, high-throughput processing
- **Sonnet**: Code generation, multi-step reasoning, document analysis, general-purpose tasks
- **Opus**: Complex analysis, creative writing, nuanced judgment, tasks requiring maximum intelligence

## Core Capabilities

### 1. Text Generation

Generate natural language text with optional system prompts:

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=2048,
    system="You are an expert technical writer. Write clear, concise documentation.",
    messages=[
        {"role": "user", "content": "Write a user guide for the export feature."}
    ]
)
```

### 2. JSON Extraction

Extract structured data from unstructured text. Use explicit JSON formatting instructions:

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system="""Extract information and return ONLY valid JSON. No markdown, no explanation.
Output schema: {"name": string, "email": string, "company": string, "role": string}""",
    messages=[
        {"role": "user", "content": "John Smith from Acme Corp reached out. He's their CTO and can be reached at john@acme.com"}
    ]
)
# Parse the response
import json
data = json.loads(message.content[0].text)
```

For complex extraction, provide example input/output pairs in the system prompt.

### 3. Image Analysis

Analyze images using base64 encoding or URLs:

```python
import base64

# From file
with open("image.png", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": image_data
                }
            },
            {"type": "text", "text": "Describe this image in detail."}
        ]
    }]
)
```

**From URL:**
```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "url",
                    "url": "https://example.com/image.jpg"
                }
            },
            {"type": "text", "text": "What's in this image?"}
        ]
    }]
)
```

**Image limits:**
- Supported formats: JPEG, PNG, GIF, WebP
- Max size: 5MB per image (API), 10MB (claude.ai)
- Max dimensions: 8000x8000 px
- Up to 100 images per API request

### 4. Extended Thinking

For complex reasoning tasks, enable extended thinking:

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000  # Allocate tokens for reasoning
    },
    messages=[
        {"role": "user", "content": "Analyze this complex business problem..."}
    ]
)

# Access thinking and response
for block in message.content:
    if block.type == "thinking":
        print(f"Reasoning: {block.thinking}")
    elif block.type == "text":
        print(f"Answer: {block.text}")
```

Use extended thinking when:
- Task requires multi-step reasoning
- Mathematical or logical analysis
- Complex code generation
- Nuanced decision-making

## API Parameters

### Core Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `model` | Yes | Model identifier (see Model Selection) |
| `max_tokens` | Yes | Maximum tokens to generate |
| `messages` | Yes | Array of message objects |
| `system` | No | System prompt for context/instructions |
| `temperature` | No | Randomness (0.0-1.0, default 1.0) |

### Temperature Guidelines

- `0.0`: Deterministic, analytical tasks (data extraction, factual answers)
- `0.3-0.5`: Balanced (documentation, explanations)
- `0.7-1.0`: Creative tasks (writing, brainstorming)

## Best Practices

### Prompt Engineering

1. **Be specific**: Clear instructions produce better results
2. **Use system prompts**: Set context, role, and constraints
3. **Provide examples**: Show desired input/output format for complex tasks
4. **Structure output**: Request specific formats (JSON, markdown, lists)

### Performance Optimization

1. **Batch operations**: Process multiple items in a single request when possible
2. **Right-size models**: Use Haiku for simple tasks, reserve Opus for complex ones
3. **Stream responses**: Use streaming for long outputs to reduce perceived latency
4. **Cache prompts**: Reuse system prompts across similar requests

### Error Handling

```python
from anthropic import APIError, RateLimitError

try:
    message = client.messages.create(...)
except RateLimitError:
    # Back off and retry
    time.sleep(60)
except APIError as e:
    print(f"API error: {e.status_code} - {e.message}")
```

### Streaming

For long responses, use streaming to reduce time-to-first-token:

```python
with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    messages=[{"role": "user", "content": "Write a detailed report..."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

## Scripts

This skill includes ready-to-use scripts:

- `scripts/generate_text.py` - Text generation with configurable parameters
- `scripts/extract_json.py` - JSON extraction from unstructured text
- `scripts/analyze_image.py` - Image analysis and description

Run scripts directly or import functions into custom implementations.

## References

For detailed guidance on specific use cases, see:

- `references/model_selection.md` - Comprehensive model comparison and selection criteria
