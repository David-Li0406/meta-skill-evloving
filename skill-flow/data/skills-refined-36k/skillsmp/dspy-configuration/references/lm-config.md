# DSPy Language Model Configuration

Configure which language models to use and how to switch between them. This guide covers LM setup, multi-provider configuration, and local overrides.

## Table of Contents

- [LM Configuration Overview](#lm-configuration-overview)
- [Basic LM Configuration](#basic-lm-configuration)
- [Multi-Provider Setup](#multi-provider-setup)
- [Local LM Overrides](#local-lm-overrides)
- [Responses API](#responses-api)
- [Best Practices](#best-practices)

## LM Configuration Overview

### What is LM Configuration?

DSPy uses the `dspy.LM` class to specify which language model to use for program execution. The `dspy.configure()` method sets this language model globally across all DSPy program invocations.

### Why Configure LMs?

- **Flexibility**: Easily switch between different models
- **Cost control**: Use cheaper models for simple tasks
- **Quality**: Use better models for complex reasoning
- **Multi-provider**: Access LLMs from multiple providers

## Basic LM Configuration

### Configure OpenAI LM

```python
import dspy

# Configure OpenAI LM
lm = dspy.LM('openai/gpt-4o-mini')
dspy.configure(lm=lm)
```

### Configure with API Key

```python
# Configure with API key directly
lm = dspy.LM('openai/gpt-4o-mini', api_key='YOUR_OPENAI_API_KEY')
dspy.configure(lm=lm)
```

### Configure with Temperature

```python
# Configure with temperature
lm = dspy.LM('openai/gpt-4o-mini', temperature=0.7)
dspy.configure(lm=lm)
```

### Configure with Max Tokens

```python
# Configure with max tokens
lm = dspy.LM('openai/gpt-4o-mini', max_tokens=1000)
dspy.configure(lm=lm)
```

## Multi-Provider Setup

### Anthropic LM

```python
# Configure Anthropic LM
lm = dspy.LM("anthropic/claude-3-opus-20240229")
dspy.configure(lm=lm)
```

### Together AI LM

```python
# Configure Together AI LM
lm = dspy.LM("together_ai/meta-llama/Llama-2-70b-chat-hf")
dspy.configure(lm=lm)
```

### General Provider Configuration

```python
# Configure with general provider (via LiteLLM)
lm = dspy.LM(
    "openai/your-model-name",
    api_key="PROVIDER_API_KEY",
    api_base="YOUR_PROVIDER_URL"
)
dspy.configure(lm=lm)
```

### Multiple Providers Example

```python
# OpenAI
openai_lm = dspy.LM('openai/gpt-4o-mini')

# Anthropic
anthropic_lm = dspy.LM("anthropic/claude-3-opus-20240229")

# Use different providers for different tasks
fast_lm = openai_lm
quality_lm = anthropic_lm

# Switch between them (see Local LM Overrides section)
```

## Local LM Overrides

### Global Configuration

Configure LM globally for entire session:

```python
import dspy

# Configure LM globally
dspy.configure(lm=dspy.LM('openai/gpt-4o-mini'))

# All programs use this LM
response = qa(question="Test question")
print('GPT-4o-mini:', response.answer)
```

### Local Context Override

Switch LM within a specific code block:

```python
import dspy

# Configure LM globally
dspy.configure(lm=dspy.LM('openai/gpt-4o-mini'))

# Use global LM
response = qa(question="Test question")
print('GPT-4o-mini:', response.answer)

# Change LM within a context block
with dspy.context(lm=dspy.LM('openai/gpt-3.5-turbo')):
    response = qa(question="Test question")
    print('GPT-3.5-turbo:', response.answer)

# Back to global LM
response = qa(question="Test question")
print('GPT-4o-mini:', response.answer)
```

### Task-Specific LM Configuration

```python
# Fast LM for simple tasks
fast_lm = dspy.LM('openai/gpt-3.5-turbo')

# Quality LM for complex tasks
quality_lm = dspy.LM('openai/gpt-4o')

# Use fast LM for classification
with dspy.context(lm=fast_lm):
    result = classify(text="This is a test")

# Use quality LM for reasoning
with dspy.context(lm=quality_lm):
    result = reason(task="Solve this complex problem")
```

### Thread-Safe Configuration

Both `dspy.configure()` and `dspy.context()` are thread-safe:

```python
import threading
import dspy

def worker(thread_id):
    # Each thread can have its own LM context
    with dspy.context(lm=dspy.LM('openai/gpt-3.5-turbo')):
        result = qa(question=f"Question from thread {thread_id}")
        print(f"Thread {thread_id}: {result.answer}")

# Create multiple threads
threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]

# Start all threads
for thread in threads:
    thread.start()

# Wait for all threads
for thread in threads:
    thread.join()
```

## Responses API

### Enable Responses API

Configure DSPy to use the Responses API for advanced models:

```python
import dspy

# Configure DSPy to use the Responses API
dspy.configure(
    lm=dspy.LM(
        "openai/gpt-5-mini",
        model_type="responses",
        temperature=1.0,
        max_tokens=16000,
    ),
)
```

### When to Use Responses API

- **Advanced reasoning models**: Models with enhanced reasoning capabilities
- **Better features**: Access to advanced model features
- **Improved quality**: Potential for higher quality outputs

### Note

Not all models or providers support the Responses API. Check LiteLLM's documentation to verify compatibility with your chosen model.

## Best Practices

### 1. Use Environment Variables for API Keys

```python
import os
import dspy

# Good: Use environment variables
api_key = os.getenv('OPENAI_API_KEY')
lm = dspy.LM('openai/gpt-4o-mini', api_key=api_key)
dspy.configure(lm=lm)

# Bad: Hardcode API keys
lm = dspy.LM('openai/gpt-4o-mini', api_key='sk-...')
dspy.configure(lm=lm)
```

### 2. Configure Default LM at Startup

```python
# Good: Configure LM once at startup
import dspy

def setup_dspy():
    """Configure DSPy with default LM."""
    lm = dspy.LM(
        'openai/gpt-4o-mini',
        temperature=0.7,
        max_tokens=1000
    )
    dspy.configure(lm=lm)

# Call at application startup
setup_dspy()
```

### 3. Use Context Manager for Task-Specific LMs

```python
# Good: Use context managers for task-specific LMs
with dspy.context(lm=fast_lm):
    result = classify(text="Test")

with dspy.context(lm=quality_lm):
    result = reason(task="Test")

# Bad: Don't reconfigure globally for task-specific LMs
dspy.configure(lm=fast_lm)
result = classify(text="Test")
dspy.configure(lm=quality_lm)
result = reason(task="Test")
```

### 4. Document LM Configuration

```python
"""
DSPy Configuration Documentation

Default LM: openai/gpt-4o-mini
- Temperature: 0.7
- Max Tokens: 1000

Task-Specific LMs:
- Fast LM: openai/gpt-3.5-turbo (for simple classification)
- Quality LM: openai/gpt-4o (for complex reasoning)
"""
```

### 5. Test LM Configuration

```python
# Good: Test LM configuration before use
import dspy

def test_lm():
    """Test if LM is configured correctly."""
    try:
        result = qa(question="Test question")
        return hasattr(result, 'answer')
    except Exception as e:
        print(f"LM configuration failed: {e}")
        return False

# Test before using in production
assert test_lm(), "LM configuration is invalid"
```

## Common Issues and Solutions

### Issue: LM Not Recognized

**Problem**: DSPy doesn't recognize the model name

**Solution**:
1. Check model name format: "provider/model"
2. Verify provider is supported by LiteLLM
3. Check model name is correct for provider
4. Try simpler model name (e.g., "openai/gpt-4")

### Issue: API Key Not Found

**Problem**: DSPy can't find API key

**Solution**:
1. Set environment variable: `OPENAI_API_KEY=your_key`
2. Pass API key directly: `dspy.LM('openai/gpt-4', api_key='your_key')`
3. Check API key is valid and not expired
4. Verify environment variable is set correctly

### Issue: Local Override Not Working

**Problem**: `dspy.context()` not changing LM

**Solution**:
1. Verify LM object is valid
2. Check indentation of context block
3. Ensure `with dspy.context(lm=...)` syntax is correct
4. Use thread-safe configuration if needed

### Issue: Responses API Not Available

**Problem**: Can't enable Responses API for model

**Solution**:
1. Check if model supports Responses API
2. Verify provider supports Responses API
3. Check LiteLLM documentation for compatibility
4. Use standard configuration if Responses API not available
