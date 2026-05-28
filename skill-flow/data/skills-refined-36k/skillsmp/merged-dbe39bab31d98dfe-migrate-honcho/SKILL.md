---
name: migrate-honcho
description: Use this skill to migrate Honcho SDK code (Python and TypeScript) from v1.6.0 to v2.0.0, addressing breaking changes and updates in the API.
---

# Honcho SDK Migration (v1.6.0 → v2.0.0)

## Overview

This skill migrates code from both the `honcho` Python SDK and the `@honcho-ai/sdk` TypeScript SDK v1.6.0 to v2.0.0, which is required for Honcho 3.0.0. 

**Key breaking changes:**

- `AsyncHoncho`/`AsyncPeer`/`AsyncSession` removed in Python; use `.aio` accessor.
- `@honcho-ai/core` dependency removed in TypeScript.
- "Observation" terminology changed to "Conclusion".
- `getConfig`/`setConfig` methods renamed to `getConfiguration`/`setConfiguration`.
- Streaming via `chatStream()` instead of `chat(stream=True)` in Python and `chat({ stream: true })` in TypeScript.
- `Representation` class removed; it now returns a string.
- `snake_case` properties converted to `camelCase` in TypeScript.

## Quick Migration Steps

### 1. Update async architecture (Python)

```python
# Before
from honcho import AsyncHoncho

async_client = AsyncHoncho()
response = await async_client.peer("user-123").chat("query")

# After
from honcho import Honcho

client = Honcho()
response = await client.aio.peer("user-123").aio.chat("query")
```

### 2. Update dependencies (TypeScript)

Remove `@honcho-ai/core` from `package.json`.

### 3. Rename configuration methods

**Python:**
```python
config = peer.get_config()
peer.set_config({"observe_me": False})

# After
config = peer.get_configuration()
peer.set_configuration(PeerConfig(observe_me=False))
```

**TypeScript:**
```typescript
await honcho.getConfig();
await honcho.setConfig({ key: 'value' });

// After
await honcho.getConfiguration();
await honcho.setConfiguration({ reasoning: { enabled: true } });
```

### 4. Update representation handling

**Python:**
```python
rep: Representation = peer.working_rep()

# After
rep: str = peer.representation()
```

**TypeScript:**
```typescript
const rep = await peer.workingRep(session, target, options);

// After
const rep = await peer.representation({ session, target, ...options });
```

### 5. Update streaming methods

**Python:**
```python
response = peer.chat("query", stream=True)

# After
stream = peer.chat_stream("query")
```

**TypeScript:**
```typescript
const stream = await peer.chat('Hello', { stream: true });

// After
const stream = await peer.chatStream('Hello');
```

### 6. Update observations to conclusions

**Python:**
```python
scope = peer.observations

# After
scope = peer.conclusions
```

**TypeScript:**
```typescript
peer.observationsOf('bob');

// After
peer.conclusionsOf('bob');
```

### 7. Update queue status methods

**Python:**
```python
status = client.get_deriver_status()

# After
status = client.queue_status()
```

**TypeScript:**
```typescript
await honcho.getDeriverStatus({ observer: peer });

// After
await honcho.queueStatus({ observer: peer });
```

### 8. Convert snake_case to camelCase (TypeScript)

```typescript
// Before
message.peer_id;

// After
message.peerId;
```

### 9. Move updateMessage to session

**Python:**
```python
updated = client.update_message(message=msg, session="sess-id")

# After
updated = session.update_message(message=msg)
```

**TypeScript:**
```typescript
await honcho.updateMessage(message, metadata, session);

// After
await session.updateMessage(message, metadata);
```

## Quick Reference Table

| v1.6.0 | v2.0.0 |
|--------|--------|
| `AsyncHoncho()` | `Honcho()` + `.aio` accessor |
| `getConfig()` | `getConfiguration()` |
| `setConfig()` | `setConfiguration()` |
| `getPeers()` | `peers()` |
| `getSessions()` | `sessions()` |
| `getDeriverStatus()` | `queueStatus()` |
| `chat(stream=True)` | `chat_stream()` |
| `working_rep()` | `representation()` |
| `observations` | `conclusions` |

## Detailed Reference

For comprehensive details on each change, see:

- [DETAILED-CHANGES.md](DETAILED-CHANGES.md) - Full API change documentation
- [MIGRATION-CHECKLIST.md](MIGRATION-CHECKLIST.md) - Step-by-step checklist

## New Exception Types

**Python:**
```python
from honcho import HonchoError, APIError, ...
```

**TypeScript:**
```typescript
import { HonchoError, AuthenticationError, ... } from '@honcho-ai/sdk';
```

## New Configuration Types (TypeScript)

Configurations are now strongly typed:

```typescript
await honcho.setConfiguration({
  reasoning: { enabled: true },
  peerCard: { use: true, create: true },
});
```