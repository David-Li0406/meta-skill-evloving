# Cerebras API Skill

> **Install:** `npx skills add diskd-ai/cerebras-api` | [skills.sh](https://skills.sh)

## Build with the Speed of Cerebras

> Experience real-time AI responses for code generation, summarization, and autonomous tasks with the world's fastest AI inference.

Get a free API key at the [Cerebras Cloud](https://cloud.cerebras.ai).

---

## Quickstart

**Python:**
```python
import os
from cerebras.cloud.sdk import Cerebras

client = Cerebras(
    api_key=os.environ.get("CEREBRAS_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Why is fast inference important?",
        }
    ],
    model="llama-3.3-70b",
)

print(chat_completion)
```

**Node.js:**
```javascript
import Cerebras from '@cerebras/cerebras_cloud_sdk';

const client = new Cerebras({
  apiKey: process.env['CEREBRAS_API_KEY'],
});

async function main() {
  const completionCreateResponse = await client.chat.completions.create({
    messages: [{ role: 'user', content: 'Why is fast inference important?' }],
    model: 'llama-3.3-70b',
  });

  console.log(completionCreateResponse);
}

main();
```

**cURL:**
```bash
curl --location 'https://api.cerebras.ai/v1/chat/completions' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer ${CEREBRAS_API_KEY}" \
--data '{
  "model": "llama-3.3-70b",
  "stream": false,
  "messages": [{"content": "why is fast inference important?", "role": "user"}],
  "temperature": 0,
  "max_tokens": -1,
  "seed": 0,
  "top_p": 1
}'
```

**OpenAI Compatibility:** The Cerebras API is compatible with OpenAI's client libraries. Use base URL: `https://api.cerebras.ai/v1`

---

## Scope & Purpose

This skill provides guidance and patterns for working with Cerebras's API, covering:

* Chat completions with world's fastest inference (2,000+ tokens/s)
* Streaming responses
* Tool use/function calling
* Structured outputs with JSON schema enforcement
* Reasoning models with thinking tokens

---

## When to Use This Skill

**Triggers:**
* Mentions of Cerebras, Cerebras Inference, or Cerebras Cloud
* Working with fast LLM inference needs
* Using Python SDK (`cerebras_cloud_sdk`) or TypeScript SDK (`@cerebras/cerebras_cloud_sdk`)
* Tasks involving Llama, Qwen, or GLM models on Cerebras

**Use cases:**
* Implementing chat completions with Llama 3.1/3.3, Qwen 3, GPT-OSS, or GLM models
* Building real-time chat applications requiring low latency
* Creating agents with tool use/function calling
* Generating structured JSON outputs with schema validation
* Using reasoning models with thinking tokens

---

## Quick Reference

### Installation

```bash
# Python
pip install cerebras_cloud_sdk

# TypeScript/JavaScript
npm install @cerebras/cerebras_cloud_sdk
```

### Environment

```bash
export CEREBRAS_API_KEY=<your-api-key>
```

### Basic Usage

**Python:**
```python
from cerebras.cloud.sdk import Cerebras

client = Cerebras()  # Uses CEREBRAS_API_KEY env var

response = client.chat.completions.create(
    model="llama-3.3-70b",
    messages=[{"role": "user", "content": "Hello"}]
)
```

**TypeScript:**
```typescript
import Cerebras from "@cerebras/cerebras_cloud_sdk";

const client = new Cerebras();

const response = await client.chat.completions.create({
    model: "llama-3.3-70b",
    messages: [{ role: "user", content: "Hello" }],
});
```

---

## Model Selection Guide

> **Deprecation Notice:** `qwen-3-32b` and `llama-3.3-70b` are scheduled for deprecation on February 16, 2026.

### Production Models

| Model | Model ID | Parameters | Speed | Use Case |
|-------|----------|------------|-------|----------|
| Llama 3.1 8B | `llama3.1-8b` | 8B | ~2200 tok/s | Real-time chat, interactive apps |
| Llama 3.3 70B | `llama-3.3-70b` | 70B | ~2100 tok/s | Chat, coding, math, reasoning |
| OpenAI GPT OSS | `gpt-oss-120b` | 120B | ~3000 tok/s | Reasoning with effort control |
| Qwen 3 32B | `qwen-3-32b` | 32B | ~2600 tok/s | Hybrid reasoning with `<think>` tags |

### Preview Models

| Model | Model ID | Parameters | Speed | Use Case |
|-------|----------|------------|-------|----------|
| Qwen 3 235B | `qwen-3-235b-a22b-instruct-2507` | 235B | ~1400 tok/s | Multilingual, instruction following |
| Z.ai GLM 4.7 | `zai-glm-4.7` | 355B | ~1000 tok/s | Superior tool use, #1 on BFCL |

---

## Skill Structure

```
cerebras-api/
  SKILL.md          # Full API reference and patterns
  README.md         # This file (overview)
  references/       # Supporting documentation
    python.md       # Python SDK reference
    typescript.md   # TypeScript SDK reference
```

---

## Key Patterns

### Streaming Responses

```python
stream = client.chat.completions.create(
    model="llama-3.3-70b",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### Structured Outputs

```python
from pydantic import BaseModel

class Movie(BaseModel):
    title: str
    director: str
    year: int

response = client.chat.completions.create(
    model="llama-3.3-70b",
    messages=[{"role": "user", "content": "Suggest a sci-fi movie"}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "movie",
            "strict": True,
            "schema": Movie.model_json_schema()
        }
    }
)
```

### Tool Calling

```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "strict": True,
        "description": "Get weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"}
            },
            "required": ["location"],
            "additionalProperties": False
        }
    }
}]

response = client.chat.completions.create(
    model="zai-glm-4.7",
    messages=[{"role": "user", "content": "Weather in Tokyo?"}],
    tools=tools
)
```

### Reasoning Models

```python
response = client.chat.completions.create(
    model="qwen-3-32b",
    messages=[{"role": "user", "content": "Solve: 15% of 240"}],
    reasoning_format="parsed"
)

print("Thinking:", response.choices[0].message.reasoning)
print("Answer:", response.choices[0].message.content)
```

---

## Error Handling

```python
import cerebras.cloud.sdk

try:
    response = client.chat.completions.create(
        model="llama-3.3-70b",
        messages=[{"role": "user", "content": "Hello"}]
    )
except cerebras.cloud.sdk.RateLimitError:
    # Wait and retry with exponential backoff
    pass
except cerebras.cloud.sdk.APIConnectionError:
    # Network issue
    pass
except cerebras.cloud.sdk.APIStatusError as e:
    # API error (check e.status_code)
    pass
```

---

## Resources

**Skill Files:**
* [SKILL.md](cerebras-api/SKILL.md) - Full API reference and patterns
* [references/python.md](cerebras-api/references/python.md) - Python SDK reference
* [references/typescript.md](cerebras-api/references/typescript.md) - TypeScript SDK reference

**Getting Started:**
* [API Playground](https://cloud.cerebras.ai) - Get API key and experiment
* [Live Chatbot Demo](https://inference.cerebras.ai) - Try the inference
* [Pricing](https://inference-docs.cerebras.ai/support/pricing) - View pricing details

**Documentation:**
* [Official Docs](https://inference-docs.cerebras.ai) - Full documentation
* [API Reference](https://inference-docs.cerebras.ai/api-reference/chat-completions) - API endpoints
* [Models Overview](https://inference-docs.cerebras.ai/models/overview) - Available models
* [OpenAI Compatibility](https://inference-docs.cerebras.ai/resources/openai) - Migration guide

**SDKs:**
* [Python SDK](https://github.com/Cerebras/cerebras-cloud-sdk-python)
* [TypeScript SDK](https://github.com/Cerebras/cerebras-cloud-sdk-node)

---

## License

MIT
