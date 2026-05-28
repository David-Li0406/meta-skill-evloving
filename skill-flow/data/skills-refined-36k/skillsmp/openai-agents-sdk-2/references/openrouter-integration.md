# OpenRouter Integration Guide

## Overview

OpenRouter provides access to multiple AI models through a unified API. This guide covers how to configure and use OpenRouter models with the OpenAI Agents SDK.

## Supported Models

OpenRouter supports models from various providers:

| Provider | Example Model Names |
|----------|---------------------|
| OpenAI | `openrouter/openai/gpt-4o`, `openrouter/openai/gpt-4-turbo` |
| Anthropic | `openrouter/anthropic/claude-3-5-sonnet`, `openrouter/anthropic/claude-3-haiku` |
| Google | `openrouter/google/gemini-2.0-flash-exp`, `openrouter/google/gemini-2.0-pro-exp` |
| Meta | `openrouter/meta-llama/llama-3.3-70b-instruct` |
| Mistral | `openrouter/mistralai/mistral-7b-instruct` |

## Getting Started

### 1. Get OpenRouter API Key

1. Sign up at [OpenRouter.ai](https://openrouter.ai)
2. Get your API key from the dashboard
3. Add funds to your account for API usage

### 2. Install LiteLLM Integration

```bash
pip install "openai-agents[litellm]"
```

### 3. Basic Configuration

```python
import os
from agents import Agent, Runner, function_tool
from agents.extensions.models.litellm_model import LitellmModel
import asyncio

# Set API key
os.environ["OPENROUTER_API_KEY"] = "your-api-key-here"

@function_tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"The weather in {city} is sunny."

# Create agent with OpenRouter model
agent = Agent(
    name="OpenRouter Assistant",
    instructions="You are a helpful assistant using OpenRouter.",
    model=LitellmModel(
        model="openrouter/openai/gpt-4-turbo",
        api_key=os.getenv("OPENROUTER_API_KEY")
    ),
    tools=[get_weather],
)

async def main():
    result = await Runner.run(agent, "What's the weather in Tokyo?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

## Advanced Configuration

### Custom Base URL

```python
agent = Agent(
    name="Custom OpenRouter Agent",
    instructions="Custom configured agent.",
    model=LitellmModel(
        model="openrouter/openai/gpt-4o",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",  # Custom base URL
        temperature=0.7,
        max_tokens=1000,
        top_p=0.9,
        frequency_penalty=0.0,
        presence_penalty=0.0
    ),
    tools=[get_weather],
)
```

### Multiple Model Configuration

```python
from typing import Dict

# Model configurations for different use cases
MODEL_CONFIGS: Dict[str, dict] = {
    "fast": {
        "model": "openrouter/anthropic/claude-3-haiku",
        "temperature": 0.3,
        "max_tokens": 500
    },
    "balanced": {
        "model": "openrouter/openai/gpt-4-turbo",
        "temperature": 0.7,
        "max_tokens": 1000
    },
    "creative": {
        "model": "openrouter/google/gemini-2.0-pro-exp",
        "temperature": 0.9,
        "max_tokens": 1500
    }
}

def create_agent_with_config(config_name: str, tools=None):
    """Create agent with predefined configuration."""
    config = MODEL_CONFIGS[config_name]

    return Agent(
        name=f"{config_name.capitalize()} Agent",
        instructions="You are a helpful assistant.",
        model=LitellmModel(
            model=config["model"],
            api_key=os.getenv("OPENROUTER_API_KEY"),
            temperature=config["temperature"],
            max_tokens=config["max_tokens"]
        ),
        tools=tools or []
    )

# Usage
fast_agent = create_agent_with_config("fast", [get_weather])
creative_agent = create_agent_with_config("creative", [get_weather])
```

## Cost Optimization

### Using Different Models for Different Tasks

```python
from agents import Agent, Runner, function_tool
from agents.extensions.models.litellm_model import LitellmModel
import asyncio

@function_tool
def simple_task(query: str) -> str:
    """Simple task suitable for cheaper models."""
    return f"Processed: {query}"

@function_tool
def complex_task(query: str) -> str:
    """Complex task requiring more capable models."""
    return f"Complex analysis of: {query}"

# Use cheaper model for simple tasks
simple_agent = Agent(
    name="Simple Task Agent",
    instructions="Handle simple tasks efficiently.",
    model=LitellmModel(
        model="openrouter/anthropic/claude-3-haiku",  # Cheaper option
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0.3,
        max_tokens=300
    ),
    tools=[simple_task],
)

# Use more capable model for complex tasks
complex_agent = Agent(
    name="Complex Task Agent",
    instructions="Handle complex analysis tasks.",
    model=LitellmModel(
        model="openrouter/openai/gpt-4o",  # More capable option
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0.7,
        max_tokens=2000
    ),
    tools=[complex_task],
)
```

### Budget Monitoring

```python
import os
import time
from typing import Optional

class OpenRouterBudgetMonitor:
    """Monitor OpenRouter API usage and costs."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.usage = {
            "requests": 0,
            "tokens": 0,
            "estimated_cost": 0.0
        }

    def track_request(self, model: str, tokens_used: int):
        """Track API request usage."""
        self.usage["requests"] += 1
        self.usage["tokens"] += tokens_used

        # Estimate cost (simplified - check OpenRouter pricing for accurate rates)
        cost_per_token = self._get_cost_per_token(model)
        self.usage["estimated_cost"] += tokens_used * cost_per_token

    def _get_cost_per_token(self, model: str) -> float:
        """Get approximate cost per token for a model."""
        # These are example rates - check OpenRouter documentation for current rates
        rates = {
            "openrouter/openai/gpt-4o": 0.00001,
            "openrouter/openai/gpt-4-turbo": 0.00003,
            "openrouter/anthropic/claude-3-5-sonnet": 0.000015,
            "openrouter/anthropic/claude-3-haiku": 0.000001,
            "openrouter/google/gemini-2.0-flash-exp": 0.0000005,
        }
        return rates.get(model, 0.00001)  # Default rate

    def get_usage_summary(self) -> dict:
        """Get current usage summary."""
        return {
            **self.usage,
            "average_tokens_per_request": self.usage["tokens"] / max(self.usage["requests"], 1)
        }
```

## Error Handling

### API Errors

```python
import asyncio
from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel
from openai import APIError, RateLimitError

async def safe_agent_run(agent, prompt: str, max_retries: int = 3):
    """Run agent with error handling and retries."""
    for attempt in range(max_retries):
        try:
            result = await Runner.run(agent, prompt)
            return result.final_output

        except RateLimitError:
            wait_time = (attempt + 1) * 5  # Exponential backoff
            print(f"Rate limit hit, waiting {wait_time}s...")
            await asyncio.sleep(wait_time)

        except APIError as e:
            print(f"API error on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2)

    raise Exception("Max retries exceeded")

# Usage
async def main():
    agent = Agent(
        name="Error Handling Agent",
        instructions="You are a helpful assistant.",
        model=LitellmModel(
            model="openrouter/openai/gpt-4-turbo",
            api_key=os.getenv("OPENROUTER_API_KEY")
        )
    )

    try:
        response = await safe_agent_run(
            agent,
            "Tell me about AI safety",
            max_retries=3
        )
        print(f"Response: {response}")
    except Exception as e:
        print(f"Failed after retries: {e}")
```

### Model-Specific Configuration

```python
def create_model_specific_agent(model_name: str):
    """Create agent with model-specific configuration."""
    model_configs = {
        "openrouter/openai/gpt-4o": {
            "temperature": 0.7,
            "max_tokens": 2000,
            "top_p": 0.9,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        },
        "openrouter/anthropic/claude-3-haiku": {
            "temperature": 0.3,
            "max_tokens": 1000,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        },
        "openrouter/google/gemini-2.0-flash-exp": {
            "temperature": 0.2,
            "max_tokens": 2048,
            "top_p": 0.95,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        }
    }

    config = model_configs.get(model_name, model_configs["openrouter/openai/gpt-4o"])

    return Agent(
        name=f"{model_name.split('/')[-1]} Agent",
        instructions="You are a helpful assistant.",
        model=LitellmModel(
            model=model_name,
            api_key=os.getenv("OPENROUTER_API_KEY"),
            **config
        )
    )
```

## Best Practices

### 1. Environment Variables
```python
# Store API keys securely
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in environment variables")
```

### 2. Model Selection
- Use cheaper models (`claude-3-haiku`, `gemini-2.0-flash`) for simple tasks
- Use more capable models (`gpt-4o`, `claude-3-5-sonnet`) for complex reasoning
- Match model capabilities to task requirements

### 3. Rate Limiting
```python
import asyncio
import time

class RateLimiter:
    def __init__(self, requests_per_minute: int):
        self.requests_per_minute = requests_per_minute
        self.requests = []

    async def wait_if_needed(self):
        """Wait if rate limit would be exceeded."""
        now = time.time()
        # Remove requests older than 1 minute
        self.requests = [req_time for req_time in self.requests
                        if now - req_time < 60]

        if len(self.requests) >= self.requests_per_minute:
            sleep_time = 60 - (now - self.requests[0])
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)

        self.requests.append(now)
```

### 4. Logging and Monitoring

```python
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenRouterLogger:
    def __init__(self):
        self.request_log = []

    def log_request(self, model: str, prompt: str, response: str, tokens: int):
        """Log API request details."""
        entry = {
            "timestamp": time.time(),
            "model": model,
            "prompt_length": len(prompt),
            "response_length": len(response),
            "tokens": tokens
        }
        self.request_log.append(entry)
        logger.info(f"OpenRouter request: {model}, tokens: {tokens}")

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics."""
        if not self.request_log:
            return {"total_requests": 0, "total_tokens": 0}

        total_requests = len(self.request_log)
        total_tokens = sum(entry["tokens"] for entry in self.request_log)

        return {
            "total_requests": total_requests,
            "total_tokens": total_tokens,
            "average_tokens_per_request": total_tokens / total_requests
        }
```

## Troubleshooting

### Common Issues

#### 1. Model Not Found
```python
# Error: Model not found
# Solution: Use correct OpenRouter model format
agent = Agent(
    model=LitellmModel(
        model="openrouter/openai/gpt-4o",  # Correct format
        # NOT: "gpt-4o" or "openai/gpt-4o"
        api_key=api_key
    )
)
```

#### 2. API Key Issues
```python
# Check if API key is properly set
import os
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    print("Error: OPENROUTER_API_KEY environment variable not set")
    print("Set it with: export OPENROUTER_API_KEY='your-key'")
```

#### 3. Async/Await Pattern
```python
# Always use async/await pattern
async def run_agent():
    result = await Runner.run(agent, "Your prompt")
    return result

# Run with asyncio
import asyncio
asyncio.run(run_agent())
```

## Example Scripts

See `scripts/` directory for complete working examples:
- `scripts/openrouter_config.py` - Complete OpenRouter configuration
- `scripts/multi_model_agent.py` - Using multiple OpenRouter models
- `scripts/budget_monitor.py` - Cost tracking and budget management