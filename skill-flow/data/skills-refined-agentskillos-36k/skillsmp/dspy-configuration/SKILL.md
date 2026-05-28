---
name: dspy-configuration
description: DSPy configuration, LM setup, caching, and version management. Use when configuring language models, enabling caching, managing dependencies, or setting up multi-provider configurations.
---

# DSPy Configuration

DSPy configuration, LM setup, caching, and version management.

## Quick Start

### Configure LM Globally
```python
import dspy

# Configure LM globally
dspy.configure(lm=dspy.LM('openai/gpt-4o-mini'))
response = qa(question="How many floors are in the castle?")
print('GPT-4o-mini:', response.answer)
```

### Switch LM Locally
```python
# Change LM within a context block
with dspy.context(lm=dspy.LM('openai/gpt-3.5-turbo')):
    response = qa(question="How many floors are in the castle?")
    print('GPT-3.5-turbo:', response.answer)
```

### Enable Caching
```python
# Configure caching
dspy.configure_cache(
    enable_disk_cache=True,
    enable_memory_cache=True,
)
```

### Configure Responses API
```python
dspy.configure(
    lm=dspy.LM(
        "openai/gpt-5-mini",
        model_type="responses",
        temperature=1.0,
        max_tokens=16000,
    ),
)
```

## When to Use This Skill

Use this skill when:
- Configuring language models for DSPy
- Setting up LM switching (global/local)
- Enabling and customizing caching
- Configuring multi-provider LMs
- Managing version compatibility
- Setting up Responses API for advanced models

## Core Concepts

### LM Configuration
Configure which language models to use and how to switch between them.

**Key features:**
- **Global configuration**: `dspy.configure(lm=...)` for entire session
- **Local overrides**: `dspy.context(lm=...)` for code blocks
- **Multi-provider**: Support for OpenAI, Anthropic, Together AI, and more
- **Responses API**: Enable advanced model features

**See:** [references/lm-config.md](references/lm-config.md) for:
- LM configuration patterns
- Multi-provider setup
- Responses API configuration
- Best practices

### Caching
Manage cache behavior to improve performance and control costs.

**Cache layers:**
- **In-memory cache**: Fast access using cachetools.LRUCache
- **On-disk cache**: Persistent storage using diskcache.FanoutCache
- **Server-side cache**: Managed by LLM provider (OpenAI, Anthropic)

**See:** [references/caching.md](references/caching.md) for:
- Cache architecture details
- Custom cache key implementation
- Cache debugging techniques
- Configuration options

### Version Management
Track and manage dependency versions to ensure compatibility.

**Key features:**
- **Automatic versioning**: `save()` captures dependency versions
- **Version checking**: Alerts on version mismatches
- **Compatibility**: Prevents issues from outdated dependencies

**See:** [references/versioning.md](references/versioning.md) for:
- Dependency versioning patterns
- Version mismatch detection
- Compatibility best practices

## Scripts

The `scripts/` directory provides reusable tools:

- **compile-dspy.py**: Compile DSPy modules with proper caching
- **clear-cache.py**: Clear DSPy cache safely

## Progressive Disclosure

This skill uses progressive disclosure:

1. **SKILL.md** (this file): Quick reference and navigation
2. **references/**: Detailed technical docs loaded as needed

Load reference files only when you need detailed information on a specific topic.

## Related Skills

- **dspy-basics**: Signature design, basic modules, program composition
- **dspy-optimization**: Teleprompters, metrics, optimization workflows
- **dspy-advanced**: ReAct agents, tool calling, output refinement
