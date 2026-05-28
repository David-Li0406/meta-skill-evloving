---
name: model-configuration
description: SDK/API patterns for configuring LLM models on Letta agents. Use when setting model handles, adjusting temperature/tokens, configuring provider-specific settings (reasoning, extended thinking), or setting up custom endpoints.
license: MIT
---

# Letta Model Configuration

Patterns for configuring LLM models on Letta agents via SDK/API. Covers model handles, settings, provider-specific configuration, and custom endpoints.

## When to Use This Skill

Use this skill when:
- Creating agents with specific model configurations
- Adjusting model settings (temperature, max tokens, context window)
- Configuring provider-specific features (OpenAI reasoning, Anthropic thinking)
- Setting up custom OpenAI-compatible endpoints
- Changing models on existing agents
- Configuring embedding models for self-hosted deployments

**Not covered here:** Model selection advice (which model to choose) - see `agent-development` skill's `references/model-recommendations.md`.

## Model Handles

Models use a `provider/model-name` format:

| Provider | Handle Prefix | Example |
|----------|---------------|---------|
| OpenAI | `openai/` | `openai/gpt-4o`, `openai/gpt-4o-mini` |
| Anthropic | `anthropic/` | `anthropic/claude-sonnet-4-5-20250929` |
| Google AI | `google_ai/` | `google_ai/gemini-2.0-flash` |
| Azure OpenAI | `azure/` | `azure/gpt-4o` |
| AWS Bedrock | `bedrock/` | `bedrock/anthropic.claude-3-5-sonnet` |
| Groq | `groq/` | `groq/llama-3.3-70b-versatile` |
| Together | `together/` | `together/meta-llama/Llama-3-70b` |
| OpenRouter | `openrouter/` | `openrouter/anthropic/claude-3.5-sonnet` |
| Ollama (local) | `ollama/` | `ollama/llama3.2` |

## Basic Model Configuration

### Python
```python
from letta_client import Letta

client = Letta(api_key="your-api-key")

agent = client.agents.create(
    model="openai/gpt-4o",
    model_settings={
        "provider_type": "openai",  # Required - must match model provider
        "temperature": 0.7,
        "max_output_tokens": 4096,
    },
    context_window_limit=128000
)
```

### TypeScript
```typescript
import Letta from "@letta-ai/letta-client";

const client = new Letta({ apiKey: "your-api-key" });

const agent = await client.agents.create({
  model: "openai/gpt-4o",
  model_settings: {
    provider_type: "openai",  // Required - must match model provider
    temperature: 0.7,
    max_output_tokens: 4096,
  },
  context_window_limit: 128000,
});
```

## Common Settings

| Setting | Type | Description |
|---------|------|-------------|
| `provider_type` | string | **Required.** Must match model provider (`openai`, `anthropic`, `google_ai`, etc.) |
| `temperature` | float | Controls randomness (0.0-2.0). Lower = more deterministic. |
| `max_output_tokens` | int | Maximum tokens in the response. |

## Context Window Limit

Set at agent level (not inside `model_settings`):

```python
agent = client.agents.create(
    model="anthropic/claude-sonnet-4-5-20250929",
    context_window_limit=200000  # Use 200K of Claude's context
)
```

**Important:**
- Must be <= model's maximum context size
- Default: 32,000 tokens if not specified
- Larger windows increase latency and may reduce reliability
- When context fills up, Letta automatically summarizes older messages

## Changing an Agent's Model

Update existing agents with `agents.update()`:

### Python
```python
# Change model only
client.agents.update(
    agent_id=agent.id,
    model="anthropic/claude-sonnet-4-5-20250929"
)

# Change model and settings
client.agents.update(
    agent_id=agent.id,
    model="openai/gpt-4o",
    model_settings={
        "provider_type": "openai",
        "temperature": 0.5
    },
    context_window_limit=64000
)
```

### TypeScript
```typescript
// Change model only
await client.agents.update(agent.id, {
  model: "anthropic/claude-sonnet-4-5-20250929",
});

// Change model and settings
await client.agents.update(agent.id, {
  model: "openai/gpt-4o",
  model_settings: {
    provider_type: "openai",
    temperature: 0.5,
  },
  context_window_limit: 64000,
});
```

**Note:** Agents retain memory and tools when changing models.

## Provider-Specific Settings

For OpenAI reasoning models and Anthropic extended thinking, see `references/provider-settings.md`.

## Custom Endpoints

For OpenAI-compatible endpoints (vLLM, LM Studio, LocalAI), see `references/custom-endpoints.md`.

## Embedding Models

Required for self-hosted deployments (Letta Cloud handles automatically):

```python
agent = client.agents.create(
    model="openai/gpt-4o",
    embedding="openai/text-embedding-3-small"
)
```

Common embedding models:
- `openai/text-embedding-3-small` (recommended)
- `openai/text-embedding-3-large`
- `openai/text-embedding-ada-002`

## Anti-Hallucination Checklist

Before configuring models, verify:

- [ ] Model handle uses correct `provider/model-name` format
- [ ] `model_settings` includes required `provider_type` field
- [ ] `context_window_limit` is set at agent level, not in `model_settings`
- [ ] Provider-specific settings use correct nested structure (see references)
- [ ] For self-hosted: embedding model is specified
- [ ] Temperature is within valid range (0.0-2.0)

## Example Scripts

See `scripts/` for runnable examples:
- `scripts/basic_config.py` - Basic model configuration
- `scripts/basic_config.ts` - TypeScript equivalent
- `scripts/change_model.py` - Changing models on existing agents
- `scripts/provider_specific.py` - OpenAI reasoning, Anthropic thinking
