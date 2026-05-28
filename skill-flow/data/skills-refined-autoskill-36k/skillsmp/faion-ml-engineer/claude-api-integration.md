---
id: claude-api-integration
name: "Claude API Integration"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Claude API Integration

## Overview

Anthropic's Claude API provides access to Claude 3.5 Sonnet, Claude 3 Opus, and Claude 3 Haiku models. Claude excels at nuanced understanding, following complex instructions, coding, and maintaining helpful, harmless, and honest responses.

## When to Use

- Complex reasoning and analysis tasks
- Long document processing (200K context)
- Code generation and review
- Tasks requiring careful instruction following
- When safety and helpfulness are priorities
- Multi-turn conversations with context retention

## Key Concepts

### Model Hierarchy

| Model | Context | Strengths | Cost |
|-------|---------|-----------|------|
| claude-3-5-sonnet-20241022 | 200K | Best balance of speed/quality | Medium |
| claude-3-opus-20240229 | 200K | Most capable, complex reasoning | High |
| claude-3-sonnet-20240229 | 200K | Good balance | Medium |
| claude-3-haiku-20240307 | 200K | Fastest, most cost-effective | Low |

### Key Differentiators

- **System Prompts**: First-class support for defining Claude's behavior
- **Extended Thinking**: Chain-of-thought reasoning for complex problems
- **Tool Use**: Native function calling support
- **Vision**: Image understanding across all Claude 3 models
- **200K Context**: Process entire codebases or long documents

## Implementation

### Basic Setup

```python
from anthropic import Anthropic
import os

# Initialize client
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Simple completion
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system="You are a senior software architect specializing in Python.",
    messages=[
        {"role": "user", "content": "Review this code for security issues:\n```python\nimport pickle\ndata = pickle.loads(user_input)\n```"}
    ]
)

print(message.content[0].text)
```

### Streaming Responses

```python
def stream_claude(prompt: str, system: str = "") -> str:
    """Stream Claude response for real-time output."""
    full_response = ""

    with client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full_response += text

    return full_response
```

### Async Implementation

```python
import asyncio
from anthropic import AsyncAnthropic

async_client = AsyncAnthropic()

async def async_claude(prompt: str) -> str:
    """Async completion for concurrent requests."""
    message = await async_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

async def batch_process(prompts: list[str]) -> list[str]:
    """Process multiple prompts concurrently."""
    tasks = [async_claude(p) for p in prompts]
    return await asyncio.gather(*tasks)
```

### Tool Use / Function Calling

```python
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country, e.g., 'London, UK'"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit"
                }
            },
            "required": ["location"]
        }
    }
]

def chat_with_tools(user_message: str):
    """Claude with tool use capability."""
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=tools,
        messages=[{"role": "user", "content": user_message}]
    )

    # Check if Claude wants to use a tool
    for block in response.content:
        if block.type == "tool_use":
            tool_name = block.name
            tool_input = block.input
            tool_use_id = block.id

            # Execute the tool (your implementation)
            result = execute_tool(tool_name, tool_input)

            # Send result back to Claude
            follow_up = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                tools=tools,
                messages=[
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": response.content},
                    {
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": result
                        }]
                    }
                ]
            )
            return follow_up

    return response
```

### Vision (Image Analysis)

```python
import base64
import httpx

def analyze_image(image_url: str, question: str) -> str:
    """Analyze image with Claude Vision."""
    # For URL
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "url",
                            "url": image_url
                        }
                    },
                    {
                        "type": "text",
                        "text": question
                    }
                ]
            }
        ]
    )
    return message.content[0].text

def analyze_local_image(image_path: str, question: str) -> str:
    """Analyze local image file."""
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    # Determine media type
    media_type = "image/jpeg"
    if image_path.endswith(".png"):
        media_type = "image/png"
    elif image_path.endswith(".webp"):
        media_type = "image/webp"

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data
                        }
                    },
                    {"type": "text", "text": question}
                ]
            }
        ]
    )
    return message.content[0].text
```

### Extended Thinking (Claude 3.5 Sonnet)

```python
def complex_reasoning(problem: str) -> dict:
    """Use extended thinking for complex problems."""
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=16000,
        thinking={
            "type": "enabled",
            "budget_tokens": 10000  # Allow up to 10K tokens for thinking
        },
        messages=[{"role": "user", "content": problem}]
    )

    result = {"thinking": "", "response": ""}

    for block in response.content:
        if block.type == "thinking":
            result["thinking"] = block.thinking
        elif block.type == "text":
            result["response"] = block.text

    return result
```

### Production Service Class

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import logging

@dataclass
class ClaudeConfig:
    model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 1024
    temperature: float = 1.0
    system: str = ""

class ClaudeService:
    """Production-ready Claude service wrapper."""

    def __init__(self, api_key: Optional[str] = None):
        self.client = Anthropic(api_key=api_key)
        self.logger = logging.getLogger(__name__)

    def complete(
        self,
        messages: List[Dict[str, Any]],
        config: Optional[ClaudeConfig] = None
    ) -> Dict[str, Any]:
        """Execute completion with full response metadata."""
        config = config or ClaudeConfig()

        try:
            response = self.client.messages.create(
                model=config.model,
                max_tokens=config.max_tokens,
                temperature=config.temperature,
                system=config.system,
                messages=messages
            )

            return {
                "content": response.content[0].text,
                "model": response.model,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                },
                "stop_reason": response.stop_reason
            }

        except Exception as e:
            self.logger.error(f"Claude API error: {e}")
            raise

    def count_tokens(self, text: str) -> int:
        """Count tokens using Claude's tokenizer."""
        return self.client.count_tokens(text)
```

### Error Handling

```python
from anthropic import (
    Anthropic,
    APIError,
    RateLimitError,
    APIConnectionError,
    AuthenticationError
)
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=lambda e: isinstance(e, (RateLimitError, APIConnectionError))
)
def robust_claude(messages: list, system: str = "") -> str:
    """Claude call with automatic retry on transient errors."""
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system,
            messages=messages,
            timeout=60.0
        )
        return response.content[0].text
    except AuthenticationError:
        raise ValueError("Invalid API key")
    except RateLimitError:
        raise  # Will be retried
    except APIError as e:
        if e.status_code >= 500:
            raise APIConnectionError("Server error")
        raise
```

## Best Practices

1. **System Prompts**
   - Use system prompts to define Claude's persona and constraints
   - Be specific about output format requirements
   - Include domain context for specialized tasks

2. **Token Management**
   - Claude's 200K context is powerful but expensive
   - Summarize or chunk long documents when possible
   - Use `count_tokens()` before large requests

3. **Model Selection**
   - Sonnet: Default choice for most tasks
   - Opus: Complex reasoning, nuanced analysis
   - Haiku: High volume, simple tasks

4. **Temperature Settings**
   - 0.0-0.3: Factual, consistent outputs
   - 0.5-0.7: Balanced creativity
   - 0.8-1.0: Creative writing, brainstorming

5. **Tool Use**
   - Define clear, specific tool descriptions
   - Handle tool errors gracefully
   - Validate tool inputs before execution

## Common Pitfalls

1. **Ignoring Stop Reason** - Not handling "max_tokens" stop reason
2. **Large Images** - Sending unnecessarily high-resolution images
3. **Missing System Prompt** - Inconsistent behavior without clear instructions
4. **Sync in Async Context** - Blocking event loop with sync client
5. **No Token Counting** - Unexpected costs with large contexts
6. **Tool Loop** - Not setting max iterations for tool use

## References

- [Anthropic API Documentation](https://docs.anthropic.com/en/api)
- [Claude Prompt Engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)
