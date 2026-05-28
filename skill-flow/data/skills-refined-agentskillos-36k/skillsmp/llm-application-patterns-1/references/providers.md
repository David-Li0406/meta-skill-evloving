# Provider Configuration

Configure LLM providers for your application. Each provider has different capabilities, pricing, and configuration options.

## Provider Overview

| Provider | Best For | Pricing | Latency |
|----------|----------|---------|---------|
| **OpenAI** | General use, best structured output | $$ | Fast |
| **Anthropic** | Complex reasoning, long context | $$$ | Medium |
| **Google Gemini** | Multimodal, long context | $$ | Fast |
| **Ollama** | Local development, privacy | Free | Varies |
| **OpenRouter** | Model switching, fallbacks | Varies | Varies |

## Configuration Patterns

### Environment-Based Config

```
# Development
provider: "ollama/llama3.1"
# Free, local, fast iteration

# Testing
provider: "openai/gpt-4o-mini"
temperature: 0.0
# Cheap, deterministic for tests

# Production
provider: "openai/gpt-4o"
# Or "anthropic/claude-3-5-sonnet"
# Best quality for user-facing features
```

### Multi-Provider Setup

```
Config:
  default_provider: "openai/gpt-4o-mini"

  providers:
    simple_tasks:
      provider: "openai/gpt-4o-mini"
      temperature: 0.3

    complex_reasoning:
      provider: "anthropic/claude-3-5-sonnet"
      temperature: 0.5

    code_generation:
      provider: "anthropic/claude-3-5-sonnet"
      temperature: 0.2

    local_dev:
      provider: "ollama/codellama"
      temperature: 0.7
```

## Provider-Specific Configuration

### OpenAI

```
provider: "openai/gpt-4o"
api_key: ENV["OPENAI_API_KEY"]
options:
  temperature: 0.7        # 0.0-2.0, creativity
  max_tokens: 4096        # Output limit
  top_p: 1.0              # Nucleus sampling
  frequency_penalty: 0.0  # Reduce repetition
  presence_penalty: 0.0   # Encourage new topics
```

**Models:**
- `gpt-4o` - Best quality, multimodal
- `gpt-4o-mini` - Fast, cheap, good quality
- `gpt-4-turbo` - Previous gen, still capable
- `o1-preview` - Reasoning model (beta)

### Anthropic

```
provider: "anthropic/claude-3-5-sonnet-20241022"
api_key: ENV["ANTHROPIC_API_KEY"]
options:
  temperature: 0.7
  max_tokens: 4096
```

**Models:**
- `claude-3-5-sonnet` - Best balance of speed/quality
- `claude-3-opus` - Highest capability
- `claude-3-haiku` - Fastest, cheapest

### Google Gemini

```
provider: "gemini/gemini-1.5-pro"
api_key: ENV["GOOGLE_API_KEY"]
options:
  temperature: 0.7
  max_output_tokens: 4096
```

**Models:**
- `gemini-1.5-pro` - Best quality, long context
- `gemini-1.5-flash` - Fast, efficient
- `gemini-pro` - Previous gen

### Ollama (Local)

```
provider: "ollama/llama3.1"
base_url: "http://localhost:11434"  # Default
options:
  temperature: 0.7
  num_ctx: 4096  # Context window
```

**Models:**
- `llama3.1` - General purpose
- `codellama` - Code tasks
- `mistral` - Fast, capable
- `mixtral` - MoE, good quality

## Feature Compatibility

### Structured Output Support

| Provider | JSON Mode | Function Calling | Schema Validation |
|----------|-----------|------------------|-------------------|
| OpenAI | Yes | Yes | Yes |
| Anthropic | Yes | Yes | Yes |
| Gemini | Yes | Yes | Yes |
| Ollama | Partial | Partial | No |

### Vision/Multimodal

| Provider | Image Input | Image URLs | Video |
|----------|-------------|------------|-------|
| OpenAI | Yes | Yes | No |
| Anthropic | Yes | No (base64 only) | No |
| Gemini | Yes | No (base64 only) | Yes |
| Ollama | Limited | No | No |

### Context Windows

| Provider | Model | Max Context |
|----------|-------|-------------|
| OpenAI | gpt-4o | 128K |
| Anthropic | claude-3-5-sonnet | 200K |
| Gemini | gemini-1.5-pro | 1M |
| Ollama | llama3.1 | 128K |

## Cost Optimization

### Token Pricing (approximate, per 1M tokens)

| Provider | Model | Input | Output |
|----------|-------|-------|--------|
| OpenAI | gpt-4o | $2.50 | $10.00 |
| OpenAI | gpt-4o-mini | $0.15 | $0.60 |
| Anthropic | claude-3-5-sonnet | $3.00 | $15.00 |
| Anthropic | claude-3-haiku | $0.25 | $1.25 |
| Gemini | gemini-1.5-pro | $1.25 | $5.00 |
| Gemini | gemini-1.5-flash | $0.075 | $0.30 |

### Cost Reduction Strategies

1. **Use smaller models for simple tasks**
   ```
   classification → gpt-4o-mini
   summarization → gemini-flash
   complex analysis → claude-3-5-sonnet
   ```

2. **Cache responses**
   ```
   if cached_response exists:
     return cached_response
   else:
     response = llm.predict(...)
     cache.set(input_hash, response)
     return response
   ```

3. **Batch requests when possible**
   ```
   # Instead of 10 separate calls
   results = llm.batch_predict([input1, input2, ...])
   ```

4. **Reduce token usage**
   - Shorter prompts
   - Limit output length
   - Use structured output (less verbose)

## Fallback Strategies

### Provider Fallback

```
try:
  return openai.predict(input)
catch RateLimitError:
  return anthropic.predict(input)
catch ServiceUnavailable:
  return gemini.predict(input)
```

### Model Fallback

```
try:
  return gpt4o.predict(input)
catch TokenLimitExceeded:
  # Fall back to model with larger context
  return claude_sonnet.predict(input)
```

### Graceful Degradation

```
try:
  return complex_analysis(input)
catch Timeout:
  # Return simpler analysis
  return basic_analysis(input)
```

## Rate Limiting

### Respect Provider Limits

| Provider | Requests/min | Tokens/min |
|----------|-------------|------------|
| OpenAI | Varies by tier | Varies |
| Anthropic | 60 | 100K |
| Gemini | 60 | 120K |

### Implementation

```
RateLimiter:
  tokens_per_minute: 100000
  requests_per_minute: 60

  before_request():
    wait_if_needed()
    track_request()

  track_tokens(count):
    update_token_count(count)
```

## Observability

### Logging

```
log:
  provider: "openai/gpt-4o-mini"
  input_tokens: 150
  output_tokens: 89
  duration_ms: 450
  cost: $0.00015
  success: true
```

### Metrics to Track

- Request count by provider/model
- Token usage (input/output)
- Latency percentiles (p50, p95, p99)
- Error rate by type
- Cost per request/day/feature

### Tracing

Integrate with observability platforms:
- OpenTelemetry
- Langfuse
- LangSmith
- Helicone
