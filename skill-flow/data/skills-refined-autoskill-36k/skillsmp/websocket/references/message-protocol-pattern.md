# Message Protocol Pattern

Structured message contracts for reliable WebSocket communication.

## Why Message Discipline Matters

Without structure:
- No way to route messages to handlers
- No validation possible
- Protocol evolution breaks clients
- Debugging becomes guesswork

## Core Message Structure

Every message must have:
1. **Type** - Declares intent, routes to handler
2. **Payload** - Contains the actual data

```json
{
  "type": "chat_message",
  "payload": {
    "content": "Hello!",
    "room_id": "general"
  }
}
```

## Pydantic Models

```python
# app/websocket/models.py
from pydantic import BaseModel
from typing import Any


class WebSocketMessage(BaseModel):
    """Base message structure."""
    type: str
    payload: dict[str, Any] = {}


class ChatPayload(BaseModel):
    """Chat message payload."""
    content: str
    room_id: str | None = None


class JoinRoomPayload(BaseModel):
    """Room join payload."""
    room_id: str


class ErrorPayload(BaseModel):
    """Error response payload."""
    message: str
    code: str | None = None
```

## Type-Based Routing

```python
# app/websocket/handlers.py
from fastapi import WebSocket
from app.websocket.models import WebSocketMessage, ChatPayload, JoinRoomPayload


async def handle_chat(ws: WebSocket, payload: dict) -> None:
    chat = ChatPayload(**payload)
    # Process chat message...


async def handle_join_room(ws: WebSocket, payload: dict) -> None:
    join = JoinRoomPayload(**payload)
    # Join room logic...


async def handle_leave_room(ws: WebSocket, payload: dict) -> None:
    # Leave room logic...


# Message type → handler mapping
HANDLERS = {
    "chat": handle_chat,
    "join_room": handle_join_room,
    "leave_room": handle_leave_room,
}


async def dispatch(websocket: WebSocket, raw_data: str) -> None:
    """Parse and route message to handler."""
    try:
        message = WebSocketMessage.model_validate_json(raw_data)
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "payload": {"message": f"Invalid message format: {e}"}
        })
        return

    handler = HANDLERS.get(message.type)
    if handler:
        try:
            await handler(websocket, message.payload)
        except Exception as e:
            await websocket.send_json({
                "type": "error",
                "payload": {"message": f"Handler error: {e}"}
            })
    else:
        await websocket.send_json({
            "type": "error",
            "payload": {"message": f"Unknown message type: {message.type}"}
        })
```

## Server-to-Client Messages

Define clear message types for server responses:

```python
# System messages
{"type": "connected", "payload": {"user_id": "abc123"}}
{"type": "user_joined", "payload": {"user_id": "xyz", "room_id": "general"}}
{"type": "user_left", "payload": {"user_id": "xyz", "room_id": "general"}}

# Data messages
{"type": "chat", "payload": {"from": "user1", "content": "Hello"}}
{"type": "room_update", "payload": {"room_id": "general", "users": 5}}

# Error messages
{"type": "error", "payload": {"message": "Invalid room", "code": "ROOM_NOT_FOUND"}}

# Acknowledgments
{"type": "ack", "payload": {"ref": "msg_123", "status": "delivered"}}
```

## Message Acknowledgment Pattern

For reliable delivery:

```python
# Client sends with reference
{"type": "chat", "ref": "msg_001", "payload": {"content": "Hello"}}

# Server acknowledges
{"type": "ack", "payload": {"ref": "msg_001", "status": "delivered"}}
```

```python
class MessageWithRef(BaseModel):
    type: str
    ref: str | None = None  # Optional client reference
    payload: dict[str, Any] = {}


async def handle_with_ack(websocket: WebSocket, message: MessageWithRef) -> None:
    try:
        await process_message(message)
        if message.ref:
            await websocket.send_json({
                "type": "ack",
                "payload": {"ref": message.ref, "status": "ok"}
            })
    except Exception as e:
        if message.ref:
            await websocket.send_json({
                "type": "ack",
                "payload": {"ref": message.ref, "status": "error", "message": str(e)}
            })
```

## Versioning (Future-Proofing)

Include version for protocol evolution:

```python
class VersionedMessage(BaseModel):
    v: int = 1  # Protocol version
    type: str
    payload: dict[str, Any] = {}


async def dispatch(websocket: WebSocket, raw: str) -> None:
    msg = VersionedMessage.model_validate_json(raw)
    if msg.v == 1:
        await dispatch_v1(websocket, msg)
    elif msg.v == 2:
        await dispatch_v2(websocket, msg)
    else:
        await websocket.send_json({
            "type": "error",
            "payload": {"message": f"Unsupported protocol version: {msg.v}"}
        })
```

## Common Message Types

### Client → Server

| Type | Purpose | Payload |
|------|---------|---------|
| `ping` | Keep-alive | `{}` |
| `join_room` | Join a room | `{room_id}` |
| `leave_room` | Leave a room | `{room_id}` |
| `chat` | Send chat message | `{content, room_id?}` |
| `typing` | Typing indicator | `{room_id, is_typing}` |
| `subscribe` | Subscribe to updates | `{topic}` |
| `unsubscribe` | Unsubscribe | `{topic}` |

### Server → Client

| Type | Purpose | Payload |
|------|---------|---------|
| `pong` | Keep-alive response | `{}` |
| `connected` | Connection confirmed | `{user_id, session_id}` |
| `error` | Error occurred | `{message, code?}` |
| `chat` | Chat message | `{from, content, room_id}` |
| `user_joined` | User joined room | `{user_id, room_id}` |
| `user_left` | User left room | `{user_id, room_id}` |
| `ack` | Message acknowledged | `{ref, status}` |

## Best Practices

1. **Always validate** - Use Pydantic for all incoming messages
2. **Type field is required** - Reject messages without type
3. **Payload is always dict** - Never use primitives as payload
4. **Document your protocol** - List all message types
5. **Error responses are typed** - Use `{"type": "error", ...}`
6. **Keep payloads flat** - Avoid deep nesting

## Anti-Patterns

```python
# Bad: No type field
{"content": "Hello"}

# Bad: Primitive payload
{"type": "chat", "payload": "Hello"}

# Bad: Using type as payload
{"chat": {"content": "Hello"}}

# Bad: Inconsistent error handling
await websocket.send_text("Error occurred")  # Not JSON, no type
```
