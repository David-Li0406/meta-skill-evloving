---
name: migrate-honcho
description: Use this skill when migrating Honcho SDK code from v1.6.0 to v2.0.0 for either Python or TypeScript, addressing breaking changes and API updates.
---

# Honcho SDK Migration (v1.6.0 → v2.0.0)

## Overview

This skill migrates code from the Honcho SDK (both Python and TypeScript) v1.6.0 to v2.0.0, which is required for Honcho 3.0.0. It addresses key breaking changes and API updates.

**Key breaking changes:**

- `AsyncHoncho`/`AsyncPeer`/`AsyncSession` removed in Python → use `.aio` accessor
- `@honcho-ai/core` dependency removed in TypeScript
- "Observation" terminology changed to "Conclusion"
- `Representation` class removed (now returns a string)
- Configuration methods renamed: `getConfig`/`setConfig` → `getConfiguration`/`setConfiguration`
- Streaming methods updated: Python uses `chat_stream()` instead of `chat(stream=True)`, TypeScript uses `chatStream()`
- `poll_deriver_status()` removed in TypeScript

## Quick Migration

### 1. Update async architecture (Python)

```python
# Before
from honcho import AsyncHoncho, AsyncPeer, AsyncSession

async_client = AsyncHoncho()
peer = await async_client.peer("user-123")
response = await peer.chat("query")

# After
from honcho import Honcho

client = Honcho()
peer = await client.aio.peer("user-123")
response = await peer.aio.chat("query")
```

### 2. Update dependencies (TypeScript)

Remove `@honcho-ai/core` from package.json. The SDK now has its own HTTP client.

### 3. Replace observations with conclusions

#### Python

```python
# Before
from honcho import Observation

scope = peer.observations
scope = peer.observations_of("other-peer")
rep = scope.get_representation()

# After
from honcho import Conclusion

scope = peer.conclusions
scope = peer.conclusions_of("other-peer")
rep = scope.representation()  # Returns str
```

#### TypeScript

```typescript
// Before
peer.observations
peer.observationsOf('bob')

// After
peer.conclusions
peer.conclusionsOf('bob')
```

### 4. Update representation handling

#### Python

```python
# Before
from honcho import Representation

rep: Representation = peer.working_rep()
print(rep.explicit)
print(rep.deductive)

# After
rep: str = peer.representation()
print(rep)  # Just a string now
```

### 5. Rename configuration methods

#### Python

```python
# Before
config = peer.get_config()

# After
config = peer.get_configuration()
```

#### TypeScript

```typescript
// Before
await honcho.getConfig()

// After
await honcho.getConfiguration()
```

### 6. Update streaming methods

#### Python

```python
# Before
response = await peer.chat("query", stream=True)

# After
response = await peer.chat_stream("query")
```

#### TypeScript

```typescript
// Before
const stream = await peer.chat('Hello', { stream: true })

// After
const stream = await peer.chatStream('Hello')
```

### 7. Update queue status methods (TypeScript)

```typescript
// Before
await honcho.getDeriverStatus({ observer: peer })

// After
// Removed - see documentation for new methods
```