---
name: claude-api-reference
description: "Claude API development reference guide. Use when developing Claude API applications for Messages API, Vision, PDF processing, Tool Use, Streaming, and more. Triggers: (1) Claude API integration development, (2) Image or PDF file processing, (3) Tool Use or Function Calling implementation, (4) Streaming or Batch processing setup, (5) Any Claude SDK development questions"
---

# Claude API Reference Skill

This skill provides essential knowledge and best practices for Claude API development.

## Quick Start

```python
from anthropic import Anthropic

client = Anthropic()  # Automatically reads ANTHROPIC_API_KEY from environment
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}]
)
print(message.content[0].text)
```

## Core API Endpoints

| Endpoint | Purpose |
|----------|---------|
| `POST /v1/messages` | Primary conversation API |
| `POST /v1/messages/batches` | Batch processing (50% discount) |
| `POST /v1/messages/count_tokens` | Token counting |
| `GET /v1/models` | List available models |
| `POST /v1/files` | File upload (Beta) |

## Required Headers

```
x-api-key: YOUR_API_KEY
anthropic-version: 2023-06-01
content-type: application/json
```

## Model Selection

| Model | ID | Features |
|-------|-----|----------|
| Claude Opus 4.5 | `claude-opus-4-5-20251101` | Highest intelligence |
| Claude Sonnet 4.5 | `claude-sonnet-4-5-20250929` | Balanced performance/cost |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | Fastest speed |

## File Handling

For detailed specifications, see:
- **PDF/Image processing**: `references/file_handling.md`
- **Tool Use**: `references/tool_use.md`
- **Advanced features**: `references/advanced_features.md`

### PDF Quick Example

```python
import base64

with open("document.pdf", "rb") as f:
    pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": pdf_data
                }
            },
            {"type": "text", "text": "Analyze the key points of this document"}
        ]
    }]
)
```

### Image Processing

```python
# Base64 method
{
    "type": "image",
    "source": {
        "type": "base64",
        "media_type": "image/png",  # image/jpeg, image/gif, image/webp
        "data": image_base64
    }
}

# URL method
{
    "type": "image",
    "source": {
        "type": "url",
        "url": "https://example.com/image.jpg"
    }
}
```

## Limits

| Limit Type | Value |
|------------|-------|
| Standard request size | 32 MB |
| Batch API | 256 MB |
| Files API | 500 MB |
| PDF pages | 100 pages |
| Single image | 8000x8000 px |
| Multi-image per image | 2000x2000 px |
| Max images per request | 20 images |
| Message limit | 100,000 per request |

## Official Resources

- Documentation: https://docs.claude.com
- Python SDK: https://github.com/anthropics/anthropic-sdk-python
- Cookbook: https://github.com/anthropics/anthropic-cookbook
- Quickstarts: https://github.com/anthropics/anthropic-quickstarts