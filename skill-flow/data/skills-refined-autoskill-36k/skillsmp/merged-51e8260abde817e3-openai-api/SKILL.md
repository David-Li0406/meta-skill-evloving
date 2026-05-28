---
name: openai-api
description: Use this skill when integrating OpenAI APIs, including GPT models, chat completions, embeddings, vision, and assistants into applications.
---

# OpenAI API Skill

Comprehensive assistance with OpenAI API development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Working with OpenAI API
- Asking about OpenAI API features or APIs
- Implementing OpenAI API solutions
- Debugging OpenAI API code
- Learning OpenAI API best practices

## Quick Reference

### Common Patterns

**Pattern 1:** Introduction
This API reference describes the RESTful, streaming, and realtime APIs you can use to interact with the OpenAI platform. REST APIs are usable via HTTP in any environment that supports HTTP requests. Language-specific SDKs are listed on the libraries page.

**Authentication**
The OpenAI API uses API keys for authentication. Create, manage, and learn more about API keys in your organization settings. Remember that your API key is a secret! Do not share it with others or expose it in any client-side code (browsers, apps). API keys should be securely loaded from an environment variable or key management service on the server.

**Example:**
```bash
curl https://api.openai.com/v1/models \
-H "Authorization: Bearer $OPENAI_API_KEY"
```

### Installation

```bash
# Python
pip install openai

# Node.js / TypeScript
npm install openai
```

### Client Setup

**Python:**
```python
from openai import OpenAI

# Uses OPENAI_API_KEY env var by default
client = OpenAI()
```

**TypeScript:**
```typescript
import OpenAI from "openai";

const openai = new OpenAI(); // Uses OPENAI_API_KEY env var
```

### Chat Completions

**Basic Chat Example:**

**Python:**
```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain async/await in Python"}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)
```

**TypeScript:**
```typescript
const response = await openai.chat.completions.create({
  model: "gpt-4o",
  messages: [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "Explain async/await in TypeScript" },
  ],
  temperature: 0.7,
  max_tokens: 500,
});

console.log(response.choices[0].message.content);
```

### Function Calling

**Define Tools Example:**
```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and state, e.g., San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "default": "fahrenheit"
                    }
                },
                "required": ["location"]
            }
        }
    }
]
```

### Error Handling & Retries

**Retry with Exponential Backoff:**
```python
import time
from openai import RateLimitError, APITimeoutError, APIConnectionError

def chat_with_retry(messages: list, model: str = "gpt-4o", max_retries: int = 3, base_delay: float = 1.0) -> str:
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(model=model, messages=messages)
            return response.choices[0].message.content
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            print(f"Rate limited. Retrying in {delay}s...")
            time.sleep(delay)
```

### Best Practices

- **System Prompt Design:** Clearly define the assistant's role and guidelines.
- **Prompt Templates:** Use templates for consistent prompt structures.
- **Production Checklist:** Ensure security, rate limits, costs, latency, reliability, logging, and testing.

### Resources

- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [OpenAI Cookbook](https://cookbook.openai.com/)
- [Pricing](https://openai.com/pricing)
- [Rate Limits](https://platform.openai.com/docs/guides/rate-limits)

## Notes

- This skill was automatically generated from official documentation.
- Reference files preserve the structure and examples from source docs.
- Code examples include language detection for better syntax highlighting.
- Quick reference patterns are extracted from common usage examples in the docs.

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration.
2. The skill will be rebuilt with the latest information.