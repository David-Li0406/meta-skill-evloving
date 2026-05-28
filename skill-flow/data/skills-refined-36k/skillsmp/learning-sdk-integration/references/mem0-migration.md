# Migrating from mem0 to Learning SDK

This guide shows how to replace mem0 with the Learning SDK for simpler, automatic memory management.

## Key Differences

| Aspect | mem0 | Learning SDK |
|--------|------|--------------|
| Memory capture | Manual `client.add()` | Automatic |
| Memory retrieval | Manual `client.search()` | Automatic |
| Context injection | Manual prompt building | Automatic |
| Code changes | Significant | 3 lines |

## Before: mem0

```python
from mem0 import MemoryClient
from openai import OpenAI

mem0 = MemoryClient(api_key="mem0-key")
openai = OpenAI()

def chat(user_id: str, message: str):
    # 1. Manually retrieve relevant memories
    memories = mem0.search(message, filters={"user_id": user_id})
    context = "\n".join([m["memory"] for m in memories.get("results", [])])
    
    # 2. Manually build messages with context
    messages = [{"role": "user", "content": message}]
    if context:
        messages.insert(0, {"role": "system", "content": f"User context:\n{context}"})
    
    # 3. Make LLM call
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    assistant_message = response.choices[0].message.content
    
    # 4. Manually save the conversation
    mem0.add([
        {"role": "user", "content": message},
        {"role": "assistant", "content": assistant_message}
    ], user_id=user_id)
    
    return assistant_message

# Usage
chat("user123", "I'm a vegetarian and allergic to nuts.")
chat("user123", "What should I eat for dinner?")
```

## After: Learning SDK

```python
from openai import OpenAI
from agentic_learning import learning

openai = OpenAI()

def chat(user_id: str, message: str):
    # Everything is automatic - just wrap your LLM call
    with learning(agent=user_id):
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message}]
        )
        return response.choices[0].message.content

# Usage - memory automatically captured and retrieved
chat("user123", "I'm a vegetarian and allergic to nuts.")
chat("user123", "What should I eat for dinner?")  # Remembers dietary restrictions
```

## Migration Steps

### 1. Install Learning SDK

```bash
pip uninstall mem0ai
pip install agentic-learning
```

### 2. Set Environment Variables

```bash
# Remove
# MEM0_API_KEY=...

# Add
export LETTA_API_KEY="your-letta-api-key"
```

### 3. Update Imports

```python
# Remove
from mem0 import MemoryClient

# Add
from agentic_learning import learning
```

### 4. Remove Manual Memory Code

Remove all:
- `client.add()` calls
- `client.search()` calls
- Manual context building
- Manual prompt injection

### 5. Wrap LLM Calls

```python
# Before
response = openai.chat.completions.create(...)

# After
with learning(agent="user-id"):
    response = openai.chat.completions.create(...)
```

## Feature Mapping

### User/Agent Identification

```python
# mem0
client.add(messages, user_id="user123")

# Learning SDK
with learning(agent="user123"):
    ...
```

### Capture Without Retrieval

```python
# mem0 - add without search
client.add(messages, user_id="user123")

# Learning SDK
with learning(agent="user123", capture_only=True):
    ...
```

### Custom Memory Structure

```python
# mem0 - categories/metadata
client.add(messages, user_id="user123", metadata={"category": "preferences"})

# Learning SDK - memory blocks
with learning(agent="user123", memory=[
    {"label": "preferences", "description": "User preferences"}
]):
    ...
```

## Provider Support

Both support multiple LLM providers:

| Provider | mem0 | Learning SDK |
|----------|------|--------------|
| OpenAI | ✅ | ✅ |
| Anthropic | ✅ | ✅ |
| Gemini | ✅ | ✅ |
| PydanticAI | ❌ | ✅ |

## Async Support

```python
# mem0 - separate async client
from mem0 import AsyncMemoryClient

# Learning SDK - same context manager works
with learning(agent="user123"):
    response = await openai.chat.completions.acreate(...)
```

## Benefits of Migration

1. **Less code**: Remove 10-20 lines of memory management per endpoint
2. **No manual sync**: Memory capture/retrieval is automatic
3. **Fewer bugs**: No risk of forgetting to save or retrieve
4. **Cleaner architecture**: Memory is transparent, not scattered through code
