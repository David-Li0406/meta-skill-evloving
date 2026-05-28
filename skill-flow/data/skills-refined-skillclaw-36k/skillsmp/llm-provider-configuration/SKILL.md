---
name: llm-provider-configuration
description: Skill for configuring OpenAI Agents SDK to work with alternative LLM providers using base URL and API key
---

# LLM Provider Configuration Skill

This skill provides guidance for configuring the OpenAI Agents SDK to work with alternative LLM providers (like Google Gemini, Anthropic Claude, etc.) using a custom base URL and API key.

## Key Concepts

The OpenAI Agents SDK can work with alternative LLM providers that support the OpenAI API format by configuring a custom base URL and API key. This is done through one of three levels:

1. Agent Level (recommended)
2. Run Level
3. Global Level

## Agent Level Configuration (Recommended)

For per-agent configuration, use the OpenAIChatCompletionsModel with a custom client:

```python
import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled

# Initialize client with custom base URL and API key
client = AsyncOpenAI(
    api_key=your_api_key,
    base_url="https://your-provider-base-url/",
)

set_tracing_disabled(disabled=True)

# Create agent with custom model configuration
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model=OpenAIChatCompletionsModel(model="model-name", openai_client=client),
)
```

## Required Parameters

1. **Base URL**: The API endpoint for the LLM provider (e.g., "https://generativelanguage.googleapis.com/v1beta/openai/" for Gemini)
2. **API Key**: The authentication key for the LLM provider
3. **Model Name**: The specific model identifier (e.g., "gemini-2.0-flash")

## Gemini-Specific Configuration

For Google Gemini integration:

- Base URL: `https://generativelanguage.googleapis.com/v1beta/openai/`
- API Key: Google API key with Gemini access
- Model: `gemini-2.0-flash`, `gemini-2.5-flash`, etc.

## Common Provider URLs

- Google Gemini: `https://generativelanguage.googleapis.com/v1beta/openai/`
- Anthropic Claude (if OpenAI compatible): `https://api.anthropic.com/v1/`
- Other providers: Check documentation for OpenAI-compatible endpoints