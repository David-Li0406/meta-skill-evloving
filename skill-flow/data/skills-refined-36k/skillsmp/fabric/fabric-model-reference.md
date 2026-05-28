# Fabric Model Reference - Thinking Levels, Speed & Cost

**Purpose**: Quick reference for selecting the right AI model in Fabric based on your use case, budget, and
performance requirements.

## Available API Keys

Based on `.config/fabric/.env`:

- ✅ **Anthropic** (Claude models)
- ✅ **Gemini** (Google models)
- ✅ **GrokAI** (xAI models)
- ✅ **OpenAI** (GPT models)

---

## Model Classification Framework

### Thinking Levels

- **L0 - No Extended Thinking**: Standard fast completion (most models)
- **L1 - Basic Reasoning**: Some chain-of-thought capabilities
- **L2 - Extended Thinking**: Models with explicit reasoning/thinking modes
- **L3 - Advanced Reasoning**: Deepest reasoning capabilities (o1, o3, etc.)

### Speed Categories

- **Ultra-Fast**: < 1s response time, real-time use
- **Fast**: 1-3s response time, interactive use
- **Standard**: 3-10s response time, general purpose
- **Slow**: 10-30s response time, complex tasks
- **Very Slow**: > 30s response time, reasoning-heavy tasks

### Cost Tiers

- **Free**: No cost (free tier models)
- **Ultra-Low**: < $0.50 per 1M input tokens
- **Low**: $0.50-$2 per 1M input tokens
- **Medium**: $2-$10 per 1M input tokens
- **High**: $10-$30 per 1M input tokens
- **Premium**: > $30 per 1M input tokens

---

## Anthropic Models (Claude)

### Recommended Models

| Model | Thinking | Speed | Cost | Best For |
 | ----- | -------- | ----- | ---- | -------- | 
| `claude-sonnet-4-5-20250929` | L1 | Fast | Medium | General purpose, best balance |
| `claude-3-5-haiku-20241022` | L0 | Ultra-Fast | Ultra-Low | Quick tasks, high volume |
| `claude-opus-4-20250514` | L1 | Standard | High | Complex analysis, quality critical |

### All Claude Models

**Sonnet Family** (Balanced):

- `claude-sonnet-4-5-20250929` - Latest Sonnet 4.5 (recommended)
- `claude-sonnet-4-5` - Sonnet 4.5 latest pointer
- `claude-sonnet-4-20250514` - Sonnet 4.0
- `claude-3-7-sonnet-20250219` - Sonnet 3.7
- `claude-3-7-sonnet-latest` - Pointer to latest 3.7

**Haiku Family** (Fast & Cheap):

- `claude-3-5-haiku-20241022` - Latest Haiku (recommended for speed)
- `claude-3-5-haiku-latest` - Pointer to latest Haiku
- `claude-3-haiku-20240307` - Original Haiku 3

**Opus Family** (Highest Quality):

- `claude-opus-4-20250514` - Latest Opus 4
- `claude-opus-4-1-20250805` - Opus 4.1
- `claude-3-opus-20240229` - Original Opus 3
- `claude-3-opus-latest` - Pointer to latest Opus 3

**Cost Estimates** (approximate):

- Haiku: $0.25/$1.25 per 1M tokens (input/output)
- Sonnet: $3/$15 per 1M tokens
- Opus: $15/$75 per 1M tokens

---

## Gemini Models (Google)

### Recommended Models

| Model | Thinking | Speed | Cost | Best For |
 | ----- | -------- | ----- | ---- | -------- | 
| `gemini-2.5-flash` | L0 | Ultra-Fast | Ultra-Low | High-volume, fast processing |
| `gemini-2.5-pro` | L1 | Fast | Low | Balanced quality/cost |
| `gemini-2.0-flash-thinking-exp` | L2 | Slow | Low | Reasoning tasks |

### Flash Models (Fast & Efficient)

**Gemini 2.5 Flash** (Latest):

- `gemini-2.5-flash` - Production-ready, fast (recommended)
- `gemini-2.5-flash-image` - With image generation
- `gemini-2.5-flash-lite` - Even faster, lower cost
- `gemini-2.5-flash-preview-09-2025` - Preview version
- `gemini-2.5-flash-preview-tts` - With text-to-speech

**Gemini 2.0 Flash**:

- `gemini-2.0-flash` - Stable 2.0
- `gemini-2.0-flash-exp` - Experimental features
- `gemini-2.0-flash-thinking-exp` - **Reasoning mode** (L2)
- `gemini-2.0-flash-thinking-exp-01-21` - Specific thinking version
- `gemini-2.0-flash-lite` - Ultra-fast variant
- `gemini-2.0-flash-lite-001` - Stable lite version

### Pro Models (Highest Quality)

**Gemini 2.5 Pro**:

- `gemini-2.5-pro` - Production-ready (recommended)
- `gemini-2.5-pro-preview-03-25` - Preview versions
- `gemini-2.5-pro-preview-05-06`
- `gemini-2.5-pro-preview-06-05`
- `gemini-2.5-pro-preview-tts` - With text-to-speech

**Gemini 2.0 Pro**:

- `gemini-2.0-pro-exp` - Experimental 2.0 Pro
- `gemini-2.0-pro-exp-02-05` - Specific version

### Specialized Models

- `gemini-exp-1206` - Experimental features
- `gemini-robotics-er-1.5-preview` - Robotics applications
- `learnlm-2.0-flash-experimental` - Learning/education focused
- `gemini-2.0-flash-exp-image-generation` - Image generation
- `imagen-4.0-generate-preview-06-06` - Advanced image generation
- `imagen-4.0-ultra-generate-preview-06-06` - Ultra-quality images

### Gemma Models (Open Source)

Small, efficient models that can run locally or in cloud:

- `gemma-3-27b-it` - Largest, best quality
- `gemma-3-12b-it` - Medium size
- `gemma-3-4b-it` - Small, fast
- `gemma-3-1b-it` - Tiny, ultra-fast
- `gemma-3n-e4b-it` - Nano variants
- `gemma-3n-e2b-it`

**Cost**: Gemini models are generally **free** for moderate usage (API key required)

---

## GrokAI Models (xAI)

### Recommended Models

| Model | Thinking | Speed | Cost | Best For |
 | ----- | -------- | ----- | ---- | -------- | 
| `grok-4-fast-non-reasoning` | L0 | Fast | Medium | General tasks, speed priority |
| `grok-4-fast-reasoning` | L2 | Slow | High | Complex reasoning |
| `grok-3` | L1 | Standard | Medium | Balanced performance |

### Grok 4 Family (Latest)

- `grok-4-0709` - Main Grok 4 model
- `grok-4-fast-non-reasoning` - Fast, no extended thinking (recommended for speed)
- `grok-4-fast-reasoning` - Fast with reasoning capabilities (L2)

### Grok 3 Family

- `grok-3` - Latest stable Grok 3 (recommended)
- `grok-3-mini` - Smaller, faster variant

### Grok 2 Family

- `grok-2-1212` - Text-only Grok 2
- `grok-2-vision-1212` - With vision capabilities
- `grok-2-image-1212` - Image generation

### Specialized

- `grok-code-fast-1` - Code-optimized model

**Cost**: Moderate pricing, similar to OpenAI GPT-4

---

## OpenAI Models (GPT)

### Recommended Models

| Model | Thinking | Speed | Cost | Best For |
 | ----- | -------- | ----- | ---- | -------- | 
| `gpt-4.1` | L1 | Standard | High | General high-quality tasks |
| `gpt-4.1-mini` | L1 | Fast | Medium | Balanced cost/quality |
| `gpt-4.1-nano` | L0 | Ultra-Fast | Low | Simple, fast tasks |
| `chatgpt-4o-latest` | L1 | Fast | Medium | Conversational, multimodal |

### GPT-4.1 Family (Latest)

- `gpt-4.1` - Latest flagship model
- `gpt-4.1-2025-04-14` - Specific version
- `gpt-4.1-mini` - Smaller, faster, cheaper
- `gpt-4.1-mini-2025-04-14`
- `gpt-4.1-nano` - Ultra-fast, ultra-cheap
- `gpt-4.1-nano-2025-04-14`

### GPT-4 Turbo Family

- `chatgpt-4o-latest` - ChatGPT-4o (multimodal, recommended)
- `gpt-4-turbo` - GPT-4 Turbo
- `gpt-4-turbo-2024-04-09` - Specific version
- `gpt-4-turbo-preview` - Preview version
- `gpt-4-1106-preview`
- `gpt-4-0125-preview`

### GPT-4 Original

- `gpt-4` - Original GPT-4
- `gpt-4-0613` - Specific version

### GPT-3.5 Family (Legacy, Cheap)

- `gpt-3.5-turbo` - Cheapest option
- `gpt-3.5-turbo-0125` - Specific versions
- `gpt-3.5-turbo-1106`
- `gpt-3.5-turbo-16k` - Extended context
- `gpt-3.5-turbo-instruct` - Instruction-following
- `gpt-3.5-turbo-instruct-0914`

### Legacy Models

- `davinci-002` - GPT-3 era
- `babbage-002` - GPT-3 era, very cheap

### Specialized

- `computer-use-preview` - Computer interaction
- `computer-use-preview-2025-03-11`
- `codex-mini-latest` - Code generation
- `dall-e-2` - Image generation (cheap)
- `dall-e-3` - Image generation (quality)

**Cost Estimates**:

- GPT-3.5: ~$0.50/$1.50 per 1M tokens
- GPT-4 Mini: ~$2.50/$10 per 1M tokens
- GPT-4 Turbo: ~$10/$30 per 1M tokens
- GPT-4: ~$30/$60 per 1M tokens

---

## Quick Selection Guide

### By Use Case

**High Volume / Cost Sensitive**:

1. `gemini-2.5-flash` (free, ultra-fast)
2. `claude-3-5-haiku-20241022` (ultra-low cost)
3. `gpt-4.1-nano` (cheap, fast)

**Balanced Quality/Speed**:

1. `claude-sonnet-4-5-20250929` (recommended)
2. `gemini-2.5-pro` (free)
3. `gpt-4.1-mini`

**Maximum Quality**:

1. `claude-opus-4-20250514` (best quality)
2. `gpt-4.1` (strong general purpose)
3. `grok-3` (alternative perspective)

**Reasoning/Thinking Tasks**:

1. `gemini-2.0-flash-thinking-exp` (free, L2 reasoning)
2. `grok-4-fast-reasoning` (L2 reasoning)
3. `claude-opus-4-20250514` (strong reasoning)

**Code Generation**:

1. `claude-sonnet-4-5-20250929` (excellent for code)
2. `grok-code-fast-1` (code-optimized)
3. `codex-mini-latest` (specialized)

**Creative Writing**:

1. `claude-opus-4-20250514` (best for prose)
2. `gpt-4.1` (strong creative capabilities)
3. `claude-sonnet-4-5-20250929`

---

## Model Selection Decision Tree

```text
START
  |
  ├─ Is cost a major concern?
  │   ├─ YES → Use Gemini (free) or Haiku (ultra-low cost)
  │   └─ NO → Continue
  |
  ├─ Need reasoning/thinking capabilities?
  │   ├─ YES → gemini-2.0-flash-thinking-exp or grok-4-fast-reasoning
  │   └─ NO → Continue
  |
  ├─ Need maximum quality?
  │   ├─ YES → claude-opus-4-20250514
  │   └─ NO → Continue
  |
  ├─ Need speed?
  │   ├─ YES → gemini-2.5-flash or claude-haiku
  │   └─ NO → Continue
  |
  └─ Default → claude-sonnet-4-5-20250929 (best general purpose)
```

---

## Testing Models

To test which model works best for your specific Fabric pattern:

```bash
# Test with different models
echo "test content" | fabric --pattern extract_wisdom --model gemini-2.5-flash
echo "test content" | fabric --pattern extract_wisdom --model claude-sonnet-4-5-20250929
echo "test content" | fabric --pattern extract_wisdom --model gpt-4.1-mini

# Check model list anytime
fabric --listmodels

# Set default model in Fabric config
fabric --changeDefaultModel
```

---

## Cost Optimization Strategies

### Strategy 1: Tiered Approach

- **Draft/Exploration**: Use Gemini Flash (free) or Haiku (cheap)
- **Refinement**: Use Sonnet (balanced)
- **Final/Critical**: Use Opus (quality)

### Strategy 2: Pattern-Specific

- **Simple patterns** (summarize, extract): Gemini Flash or Haiku
- **Analysis patterns** (analyze_claims, threat_model): Sonnet or Pro
- **Creative patterns** (create_prd, improve_writing): Opus or GPT-4.1

### Strategy 3: Batch Processing

- Use free Gemini models for bulk processing
- Use paid models only for critical outputs

---

## Performance Comparison (Subjective)

Based on community feedback and testing:

**Code Quality**: Claude Opus > Claude Sonnet > GPT-4.1 > Gemini Pro

**Creative Writing**: Claude Opus > GPT-4.1 > Claude Sonnet > Gemini Pro

**Reasoning**: Gemini Thinking > Grok Reasoning > Claude Opus > GPT-4.1

**Speed**: Gemini Flash > Claude Haiku > GPT-4.1-nano > Gemini Lite

**Cost Efficiency**: Gemini (free) > Claude Haiku > GPT-3.5

**Instruction Following**: Claude Sonnet > GPT-4.1 > Gemini Pro

---

## Updating This Reference

```bash
# Check for new models
fabric --listmodels

# Test new models
echo "test" | fabric --pattern summarize --model <new-model-name>
```

Last updated: 2025-11-14
