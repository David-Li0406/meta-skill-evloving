# Connection Manager Pattern

Centralized WebSocket connection state management.

## Why Centralized Management?

Connection state must live in ONE place because:
- Business logic must not handle socket tracking
- Broadcasting requires knowing all active connections
- Cleanup must be deterministic and complete
- Room membership needs a single source of truth

## Core Pattern

```python
from fastapi import WebSocket


class ConnectionManager:
    """Single source of truth for all WebSocket connections."""

    def __init__(self):
        self.active_connections: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        """Accept and track a new connection."""
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        """Remove connection from tracking."""
        self.active_connections.discard(websocket)

    async def broadcast(self, message: str) -> None:
        """Send message to all active connections."""
        for connection in self.active_connections.copy():
            try:
                await connection.send_text(message)
            except Exception:
                self.disconnect(connection)
```

## Key Design Decisions

### Use `set` Not `list`

```python
# Good - O(1) add/remove, no duplicates
self.active_connections: set[WebSocket] = set()

# Bad - O(n) remove, allows duplicates
self.active_connections: list[WebSocket] = []
```

### Use `discard` Not `remove`

```python
# Good - silent if not found
self.active_connections.discard(websocket)

# Bad - raises KeyError if not found
self.active_connections.remove(websocket)
```

### Copy Before Iteration

```python
# Good - safe if set modified during iteration
for connection in self.active_connections.copy():
    ...

# Bad - RuntimeError if set changes during iteration
for connection in self.active_connections:
    ...
```

## Singleton Instance

Create a single manager instance at module level:

```python
# app/websocket/manager.py

class ConnectionManager:
    ...

# Singleton - import this everywhere
manager = ConnectionManager()
```

Usage:

```python
# app/websocket/router.py
from app.websocket.manager import manager

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    ...
```

## Extended Manager with User Tracking

```python
from collections import defaultdict
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.connections: set[WebSocket] = set()
        self.user_connections: dict[str, set[WebSocket]] = defaultdict(set)
        self.connection_user: dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket, user_id: str) -> None:
        await websocket.accept()
        self.connections.add(websocket)
        self.user_connections[user_id].add(websocket)
        self.connection_user[websocket] = user_id

    def disconnect(self, websocket: WebSocket) -> None:
        self.connections.discard(websocket)
        user_id = self.connection_user.pop(websocket, None)
        if user_id:
            self.user_connections[user_id].discard(websocket)
            # Clean up empty user entry
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]

    async def send_to_user(self, user_id: str, message: str) -> None:
        """Send to all of a user's connections (multi-device support)."""
        for conn in self.user_connections[user_id].copy():
            try:
                await conn.send_text(message)
            except Exception:
                self.disconnect(conn)

    def is_online(self, user_id: str) -> bool:
        return bool(self.user_connections.get(user_id))
```

## Best Practices

1. **Never store manager in endpoint function** - Use module-level singleton
2. **Always cleanup in finally block** - Ensure disconnect on any exit
3. **Handle send failures** - Remove dead connections during broadcast
4. **Use defaultdict for mappings** - Avoids KeyError on first access
5. **Track bidirectional relationships** - connection→user AND user→connections

## Anti-Patterns

```python
# Bad: Creating manager per request
@router.websocket("/ws")
async def ws(websocket: WebSocket):
    manager = ConnectionManager()  # Wrong! State lost per request

# Bad: Passing manager as parameter
async def ws(websocket: WebSocket, manager: ConnectionManager = Depends(...)):
    # Creates new instance each time

# Bad: Storing connections in global list
connections = []  # Not thread-safe, allows duplicates
```
