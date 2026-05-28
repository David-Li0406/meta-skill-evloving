---
id: openai-api-integration
name: "OpenAI API Integration"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# OpenAI API Integration

## Overview

OpenAI API provides access to GPT-4, GPT-4 Turbo, GPT-4o, and other models for text generation, embeddings, image generation, and more. This methodology covers authentication, model selection, request handling, and production-ready integration patterns.

## When to Use

- Building conversational AI applications
- Text generation, summarization, translation
- Code generation and analysis
- Content moderation and classification
- When you need state-of-the-art language capabilities
- Production applications requiring high reliability

## Key Concepts

### Models Hierarchy (2024-2025)

| Model | Context | Best For | Cost |
|-------|---------|----------|------|
| gpt-4o | 128K | Multimodal, general tasks | Medium |
| gpt-4o-mini | 128K | Fast, cost-effective | Low |
| gpt-4-turbo | 128K | Complex reasoning | High |
| gpt-4 | 8K/32K | Legacy support | High |
| gpt-3.5-turbo | 16K | Simple tasks, high volume | Very Low |

### API Structure

```
POST https://api.openai.com/v1/chat/completions
POST https://api.openai.com/v1/embeddings
POST https://api.openai.com/v1/images/generations
POST https://api.openai.com/v1/audio/transcriptions
```

## Implementation

### Basic Setup

```python
from openai import OpenAI
import os

# Initialize client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Simple completion
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing in simple terms."}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)
```

### Streaming Responses

```python
def stream_response(prompt: str) -> str:
    """Stream response for better UX in interactive applications."""
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    full_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            full_response += content

    return full_response
```

### Async Implementation

```python
import asyncio
from openai import AsyncOpenAI

async_client = AsyncOpenAI()

async def async_completion(prompt: str) -> str:
    """Async completion for concurrent requests."""
    response = await async_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

async def batch_completions(prompts: list[str]) -> list[str]:
    """Process multiple prompts concurrently."""
    tasks = [async_completion(p) for p in prompts]
    return await asyncio.gather(*tasks)
```

### Structured Output with JSON Mode

```python
from pydantic import BaseModel
from typing import List

class ProductReview(BaseModel):
    sentiment: str
    score: float
    key_points: List[str]
    summary: str

def analyze_review(review_text: str) -> ProductReview:
    """Extract structured data from review."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Analyze the review and return JSON with: sentiment, score (0-1), key_points, summary"
            },
            {"role": "user", "content": review_text}
        ],
        response_format={"type": "json_object"}
    )

    import json
    data = json.loads(response.choices[0].message.content)
    return ProductReview(**data)
```

### Error Handling and Retries

```python
from openai import OpenAI, APIError, RateLimitError, APIConnectionError
from tenacity import retry, stop_after_attempt, wait_exponential

client = OpenAI()

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=lambda e: isinstance(e, (RateLimitError, APIConnectionError))
)
def robust_completion(messages: list, model: str = "gpt-4o") -> str:
    """Completion with automatic retry on transient errors."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            timeout=30.0
        )
        return response.choices[0].message.content
    except APIError as e:
        if e.status_code == 429:
            raise RateLimitError(e.message)
        raise
```

### Token Counting

```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    """Count tokens for cost estimation."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def estimate_cost(input_tokens: int, output_tokens: int, model: str) -> float:
    """Estimate API cost in USD."""
    pricing = {
        "gpt-4o": {"input": 0.005, "output": 0.015},
        "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    }

    if model not in pricing:
        return 0.0

    p = pricing[model]
    return (input_tokens * p["input"] + output_tokens * p["output"]) / 1000
```

### Production Service Class

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import logging

@dataclass
class CompletionConfig:
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 1000
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0

class OpenAIService:
    """Production-ready OpenAI service wrapper."""

    def __init__(self, api_key: Optional[str] = None):
        self.client = OpenAI(api_key=api_key)
        self.logger = logging.getLogger(__name__)

    def complete(
        self,
        messages: List[Dict[str, str]],
        config: Optional[CompletionConfig] = None
    ) -> Dict[str, Any]:
        """Execute completion with full response metadata."""
        config = config or CompletionConfig()

        try:
            response = self.client.chat.completions.create(
                model=config.model,
                messages=messages,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                top_p=config.top_p,
                frequency_penalty=config.frequency_penalty,
                presence_penalty=config.presence_penalty
            )

            return {
                "content": response.choices[0].message.content,
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "finish_reason": response.choices[0].finish_reason
            }

        except Exception as e:
            self.logger.error(f"OpenAI API error: {e}")
            raise
```

## Best Practices

1. **API Key Management**
   - Never hardcode API keys
   - Use environment variables or secret managers
   - Rotate keys periodically

2. **Cost Control**
   - Set usage limits in OpenAI dashboard
   - Count tokens before sending large requests
   - Use appropriate model for task complexity

3. **Rate Limiting**
   - Implement exponential backoff
   - Use async for batch processing
   - Consider request queuing for high volume

4. **Prompt Engineering**
   - Use system messages for consistent behavior
   - Be specific about output format
   - Include examples for complex tasks

5. **Monitoring**
   - Log all API calls with token usage
   - Track latency and error rates
   - Set up alerts for unusual patterns

## Common Pitfalls

1. **Token Overflow** - Not checking if prompt + max_tokens exceeds context limit
2. **Ignoring Finish Reason** - Not handling "length" finish reason (truncated output)
3. **Blocking Calls** - Using sync API in async applications
4. **No Timeout** - Requests hanging indefinitely
5. **Hardcoded Prompts** - Difficulty updating prompts in production
6. **Missing Error Handling** - API errors crashing applications

## References

- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [OpenAI Cookbook](https://cookbook.openai.com/)
- [tiktoken Library](https://github.com/openai/tiktoken)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
