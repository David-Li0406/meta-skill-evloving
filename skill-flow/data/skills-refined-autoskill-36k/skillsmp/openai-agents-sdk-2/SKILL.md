---
name: openai-agents-sdk
description: Expert assistance for OpenAI Agents SDK Python library including installation, configuration, multi-agent systems, debugging, and best practices. Proactively fetches the latest documentation to ensure accuracy. Use when setting up OpenAI Agents SDK with Python, configuring agents with OpenRouter or other non-OpenAI models, building multi-agent systems with handoffs and coordination, implementing function tools and tool usage, debugging agent behavior or configuration issues, learning best practices for agent orchestration, integrating with LiteLLM for multiple model providers, or setting up tracing, sessions, and observability.
---

# OpenAI Agents SDK Python

## Overview

Expert guidance for building multi-agent systems using the OpenAI Agents SDK Python library. This skill provides up-to-date documentation, code examples, and best practices for agent configuration, tool usage, model integration (including OpenRouter), and multi-agent orchestration.

## Quick Start

### Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install OpenAI Agents SDK with LiteLLM support for OpenRouter
pip install "openai-agents[litellm]"
```

### Basic Agent Configuration

Create a simple agent with function tools:

```python
from agents import Agent, Runner, function_tool
import asyncio

@function_tool
def get_weather(city: str) -> str:
    """Returns weather info for the specified city."""
    return f"The weather in {city} is sunny."

agent = Agent(
    name="Weather Assistant",
    instructions="You are a helpful weather assistant.",
    model="gpt-4o",
    tools=[get_weather],
)

async def main():
    result = await Runner.run(agent, "What's the weather in Tokyo?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

## Using OpenRouter Models

### Configuration with LiteLLM

OpenRouter models can be used through LiteLLM integration. First, ensure you have installed with LiteLLM support:

```bash
pip install "openai-agents[litellm]"
```

### Basic OpenRouter Setup

```python
from agents import Agent, Runner, function_tool
from agents.extensions.models.litellm_model import LitellmModel
import asyncio
import os

@function_tool
def get_weather(city: str) -> str:
    """Returns weather info for the specified city."""
    return f"The weather in {city} is sunny."

# Set your OpenRouter API key as environment variable
os.environ["OPENROUTER_API_KEY"] = "your-openrouter-api-key"

agent = Agent(
    name="OpenRouter Assistant",
    instructions="You are a helpful assistant using OpenRouter models.",
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

### Available OpenRouter Models

OpenRouter provides access to multiple model providers. Use the `openrouter/` prefix:

```python
# GPT models
model="openrouter/openai/gpt-4-turbo"
model="openrouter/openai/gpt-4o"

# Anthropic models
model="openrouter/anthropic/claude-3-5-sonnet"
model="openrouter/anthropic/claude-3-haiku"

# Google models
model="openrouter/google/gemini-2.0-flash-exp"
model="openrouter/google/gemini-2.0-pro-exp"

# Meta models
model="openrouter/meta-llama/llama-3.3-70b-instruct"
```

### Advanced Configuration with Environment Variables

```python
from agents import Agent, Runner, function_tool
from agents.extensions.models.litellm_model import LitellmModel
import asyncio
import os

# Configure OpenRouter settings
os.environ["OPENROUTER_API_KEY"] = "your-api-key"
os.environ["OPENROUTER_BASE_URL"] = "https://openrouter.ai/api/v1"

@function_tool
def calculator(a: float, b: float, operation: str) -> float:
    """Perform basic arithmetic operations."""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b if b != 0 else float('inf')
    else:
        raise ValueError(f"Unknown operation: {operation}")

agent = Agent(
    name="Math Assistant",
    instructions="You are a math tutor that helps with calculations.",
    model=LitellmModel(
        model="openrouter/openai/gpt-4o",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url=os.getenv("OPENROUTER_BASE_URL"),
        temperature=0.7,
        max_tokens=1000
    ),
    tools=[calculator],
)

async def main():
    result = await Runner.run(
        agent,
        "Calculate 15 multiplied by 23 using the calculator tool"
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

## Multi-Agent Systems

### Creating Multiple Coordinated Agents

```python
from agents import Agent, Runner, function_tool
from agents.extensions.models.litellm_model import LitellmModel
import asyncio

# Specialist agents
@function_tool
def research_topic(topic: str) -> str:
    """Research a topic and return information."""
    return f"Research on {topic}: This is sample research information."

@function_tool
def summarize_text(text: str) -> str:
    """Summarize the given text."""
    return f"Summary: {text[:100]}..."

researcher = Agent(
    name="Research Agent",
    instructions="You research topics thoroughly and provide detailed information.",
    model=LitellmModel(model="openrouter/openai/gpt-4-turbo"),
    tools=[research_topic],
)

summarizer = Agent(
    name="Summarization Agent",
    instructions="You summarize information concisely.",
    model=LitellmModel(model="openrouter/anthropic/claude-3-haiku"),
    tools=[summarize_text],
)

async def collaborative_workflow():
    # First agent researches
    research_result = await Runner.run(
        researcher,
        "Research quantum computing basics"
    )

    # Second agent summarizes
    summary_result = await Runner.run(
        summarizer,
        f"Summarize this: {research_result.final_output}"
    )

    print(f"Research: {research_result.final_output}")
    print(f"Summary: {summary_result.final_output}")

asyncio.run(collaborative_workflow())
```

### Agent Handoffs

```python
from agents import Agent, Runner, function_tool, handoff
from agents.extensions.models.litellm_model import LitellmModel
import asyncio

@function_tool
def get_stock_price(symbol: str) -> str:
    """Get current stock price for a symbol."""
    return f"Stock {symbol}: $150.25"

@function_tool
def analyze_trends(data: str) -> str:
    """Analyze stock trends based on data."""
    return f"Trend analysis: {data} shows bullish pattern."

financial_analyst = Agent(
    name="Financial Analyst",
    instructions="You analyze financial data and prices.",
    model=LitellmModel(model="openrouter/openai/gpt-4-turbo"),
    tools=[get_stock_price],
)

trend_analyst = Agent(
    name="Trend Analyst",
    instructions="You identify market trends and patterns.",
    model=LitellmModel(model="openrouter/anthropic/claude-3-haiku"),
    tools=[analyze_trends],
)

@handoff(from_agent=financial_analyst, to_agent=trend_analyst)
async def analyze_stock(symbol: str):
    """Handoff workflow: Get price → Analyze trends."""
    price = await get_stock_price(symbol)
    analysis = await analyze_trends(price)
    return analysis

async def main():
    result = await analyze_stock("AAPL")
    print(result)

asyncio.run(main())
```

## Advanced Features

### Structured Output with Pydantic

```python
from typing import Annotated
from pydantic import BaseModel, Field
from agents import Agent, Runner, function_tool
from agents.extensions.models.litellm_model import LitellmModel
import asyncio

class WeatherResponse(BaseModel):
    city: str = Field(description="The city name")
    temperature: str = Field(description="Temperature in Celsius")
    conditions: str = Field(description="Weather conditions")
    humidity: str = Field(description="Humidity percentage")

@function_tool
def get_weather(city: Annotated[str, "The city to get weather for"]) -> WeatherResponse:
    """Get current weather information with structured response."""
    return WeatherResponse(
        city=city,
        temperature="22°C",
        conditions="Partly cloudy",
        humidity="65%"
    )

agent = Agent(
    name="Structured Weather Agent",
    instructions="You provide structured weather information.",
    model=LitellmModel(model="openrouter/openai/gpt-4o"),
    tools=[get_weather],
)

async def main():
    result = await Runner.run(
        agent,
        "Get weather for London with structured data"
    )
    print(f"City: {result.final_output.city}")
    print(f"Temperature: {result.final_output.temperature}")
    print(f"Conditions: {result.final_output.conditions}")

asyncio.run(main())
```

### Error Handling and Validation

```python
from agents import Agent, Runner, function_tool
from agents.extensions.models.litellm_model import LitellmModel
import asyncio

@function_tool
def divide_numbers(a: float, b: float) -> float:
    """Divide two numbers with error handling."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

agent = Agent(
    name="Safe Calculator",
    instructions="You perform calculations safely with error handling.",
    model=LitellmModel(model="openrouter/openai/gpt-4-turbo"),
    tools=[divide_numbers],
    max_steps=10,  # Limit execution steps
    allow_delegation=False  # Disable delegation for safety
)

async def safe_calculation():
    try:
        result = await Runner.run(
            agent,
            "Divide 10 by 0"
        )
        print(f"Result: {result.final_output}")
    except Exception as e:
        print(f"Error occurred: {e}")

asyncio.run(safe_calculation())
```

## Troubleshooting Common Issues

### Model Not Found Errors
```python
# Incorrect: Missing provider prefix
# model="gpt-4o"  # This won't work with OpenRouter

# Correct: Use openrouter/ prefix
model="openrouter/openai/gpt-4o"
```

### API Key Configuration
```python
import os

# Set environment variable before creating agent
os.environ["OPENROUTER_API_KEY"] = "your-api-key"

# Or pass directly to LitellmModel
model=LitellmModel(
    model="openrouter/openai/gpt-4o",
    api_key="your-api-key"  # Or use os.getenv("OPENROUTER_API_KEY")
)
```

### Async/Await Pattern
```python
# Correct: Use async/await
async def main():
    result = await Runner.run(agent, "Hello")
    print(result.final_output)

# Run with asyncio
import asyncio
asyncio.run(main())
```

## Resources

This skill includes comprehensive reference materials for the OpenAI Agents SDK:

### references/
- **setup-guide.md**: Complete installation and setup instructions
- **openrouter-integration.md**: Detailed OpenRouter configuration guide
- **multi-agent-patterns.md**: Patterns for building multi-agent systems
- **tool-definition.md**: Advanced function tool patterns and best practices

### scripts/
- **basic_agent.py**: Template for basic agent setup
- **openrouter_config.py**: Configuration template for OpenRouter models
- **multi_agent_workflow.py**: Example of coordinated multi-agent system

### assets/
- **agent-templates/**: Starter templates for common agent patterns
- **example-configs/**: Configuration examples for different use cases

**Note:** For the most up-to-date documentation and API changes, always check [references/openrouter-integration.md](references/openrouter-integration.md) for OpenRouter-specific configuration and [references/setup-guide.md](references/setup-guide.md) for general SDK setup.

---

**Pro Tip:** Always fetch the latest documentation using Context7 MCP server when working with OpenAI Agents SDK to ensure you have the most current information about API changes, new features, and best practices.
