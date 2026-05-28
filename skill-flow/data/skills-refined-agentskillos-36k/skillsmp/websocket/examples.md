# WebSocket Examples

Production-ready WebSocket examples for FastAPI/Starlette applications.

## Example 1: Basic WebSocket Endpoint

Minimal WebSocket endpoint with echo functionality.

```python
# app/websocket/router.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        pass  # Client disconnected - expected behavior
```

```python
# app/main.py
from fastapi import FastAPI
from app.websocket.router import router as ws_router

app = FastAPI()
app.include_router(ws_router, tags=["websocket"])
```

## Example 2: Connection Manager Pattern

Centralized connection tracking with broadcast capability.

```python
# app/websocket/manager.py
from fastapi import WebSocket


class ConnectionManager:
    """Centralized WebSocket connection management."""

    def __init__(self):
        self.active_connections: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        """Accept and track a new connection."""
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        """Remove a connection from tracking."""
        self.active_connections.discard(websocket)

    async def send_personal(self, message: str, websocket: WebSocket) -> None:
        """Send message to a specific connection."""
        await websocket.send_text(message)

    async def broadcast(self, message: str) -> None:
        """Send message to all active connections."""
        disconnected: set[WebSocket] = set()
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                disconnected.add(connection)
        # Clean up failed connections
        self.active_connections -= disconnected


# Singleton instance
manager = ConnectionManager()
```

```python
# app/websocket/router.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.manager import manager

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("A client disconnected")
```

## Example 3: Typed Message Handling

Structured message protocol with type-based routing.

```python
# app/websocket/models.py
from pydantic import BaseModel
from typing import Any


class WebSocketMessage(BaseModel):
    """Base message structure for WebSocket communication."""
    type: str
    payload: dict[str, Any] = {}


class ChatMessage(BaseModel):
    """Chat-specific payload."""
    content: str
    username: str


class TypingIndicator(BaseModel):
    """Typing indicator payload."""
    username: str
    is_typing: bool
```

```python
# app/websocket/handlers.py
from fastapi import WebSocket
from app.websocket.models import WebSocketMessage, ChatMessage
from app.websocket.manager import manager
import json


async def handle_chat(websocket: WebSocket, payload: dict) -> None:
    """Handle chat messages."""
    chat = ChatMessage(**payload)
    await manager.broadcast(json.dumps({
        "type": "chat",
        "payload": {"username": chat.username, "content": chat.content}
    }))


async def handle_typing(websocket: WebSocket, payload: dict) -> None:
    """Handle typing indicators."""
    await manager.broadcast(json.dumps({
        "type": "typing",
        "payload": payload
    }))


# Message type to handler mapping
MESSAGE_HANDLERS = {
    "chat": handle_chat,
    "typing": handle_typing,
}


async def dispatch_message(websocket: WebSocket, raw_data: str) -> None:
    """Parse and route message to appropriate handler."""
    try:
        message = WebSocketMessage.model_validate_json(raw_data)
        handler = MESSAGE_HANDLERS.get(message.type)
        if handler:
            await handler(websocket, message.payload)
        else:
            await websocket.send_json({
                "type": "error",
                "payload": {"message": f"Unknown message type: {message.type}"}
            })
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "payload": {"message": str(e)}
        })
```

```python
# app/websocket/router.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.manager import manager
from app.websocket.handlers import dispatch_message

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await dispatch_message(websocket, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

## Example 4: Room/Channel Implementation

Logical grouping for targeted broadcasts.

```python
# app/websocket/manager.py
from collections import defaultdict
from fastapi import WebSocket


class ConnectionManager:
    """Connection manager with room support."""

    def __init__(self):
        self.active_connections: set[WebSocket] = set()
        self.rooms: dict[str, set[WebSocket]] = defaultdict(set)
        self.connection_rooms: dict[WebSocket, set[str]] = defaultdict(set)

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        """Remove connection and clean up all room memberships."""
        self.active_connections.discard(websocket)
        # Remove from all rooms
        for room_id in self.connection_rooms.get(websocket, set()):
            self.rooms[room_id].discard(websocket)
        self.connection_rooms.pop(websocket, None)

    def join_room(self, websocket: WebSocket, room_id: str) -> None:
        """Add connection to a room."""
        self.rooms[room_id].add(websocket)
        self.connection_rooms[websocket].add(room_id)

    def leave_room(self, websocket: WebSocket, room_id: str) -> None:
        """Remove connection from a room."""
        self.rooms[room_id].discard(websocket)
        self.connection_rooms[websocket].discard(room_id)

    async def broadcast(self, message: str) -> None:
        """Broadcast to all connections."""
        for connection in self.active_connections.copy():
            try:
                await connection.send_text(message)
            except Exception:
                self.disconnect(connection)

    async def broadcast_to_room(
        self, room_id: str, message: str, exclude: WebSocket | None = None
    ) -> None:
        """Broadcast to all connections in a specific room."""
        for connection in self.rooms[room_id].copy():
            if connection != exclude:
                try:
                    await connection.send_text(message)
                except Exception:
                    self.disconnect(connection)

    def get_room_count(self, room_id: str) -> int:
        """Get number of connections in a room."""
        return len(self.rooms[room_id])


manager = ConnectionManager()
```

```python
# app/websocket/router.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.manager import manager
import json

router = APIRouter()

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await manager.connect(websocket)
    manager.join_room(websocket, room_id)

    # Announce join
    await manager.broadcast_to_room(
        room_id,
        json.dumps({"type": "system", "payload": {"message": "User joined"}}),
        exclude=websocket
    )

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast_to_room(room_id, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast_to_room(
            room_id,
            json.dumps({"type": "system", "payload": {"message": "User left"}})
        )
```

## Example 5: Broadcast with User Identification

Track connections by user ID for targeted messaging.

```python
# app/websocket/manager.py
from collections import defaultdict
from fastapi import WebSocket


class ConnectionManager:
    """Connection manager with user identification."""

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

    async def send_to_user(self, user_id: str, message: str) -> None:
        """Send message to all connections of a specific user."""
        for connection in self.user_connections[user_id].copy():
            try:
                await connection.send_text(message)
            except Exception:
                self.disconnect(connection)

    async def broadcast(self, message: str, exclude_user: str | None = None) -> None:
        """Broadcast to all except optionally excluded user."""
        for connection in self.connections.copy():
            user_id = self.connection_user.get(connection)
            if user_id != exclude_user:
                try:
                    await connection.send_text(message)
                except Exception:
                    self.disconnect(connection)

    def get_user_id(self, websocket: WebSocket) -> str | None:
        """Get user ID for a connection."""
        return self.connection_user.get(websocket)

    def is_user_online(self, user_id: str) -> bool:
        """Check if user has any active connections."""
        return bool(self.user_connections[user_id])


manager = ConnectionManager()
```

## Example 6: Error Handling and Graceful Cleanup

Defensive patterns for production reliability.

```python
# app/websocket/router.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
from app.websocket.manager import manager
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


async def safe_send(websocket: WebSocket, message: str) -> bool:
    """Safely send message, return False if connection is dead."""
    if websocket.client_state != WebSocketState.CONNECTED:
        return False
    try:
        await websocket.send_text(message)
        return True
    except Exception as e:
        logger.warning(f"Failed to send message: {e}")
        return False


async def safe_close(websocket: WebSocket, code: int = 1000) -> None:
    """Safely close connection."""
    if websocket.client_state == WebSocketState.CONNECTED:
        try:
            await websocket.close(code=code)
        except Exception:
            pass  # Connection already closed


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await manager.connect(websocket)
    except Exception as e:
        logger.error(f"Failed to accept connection: {e}")
        return

    try:
        while True:
            try:
                data = await websocket.receive_text()
            except WebSocketDisconnect:
                break  # Normal disconnection
            except Exception as e:
                logger.warning(f"Receive error: {e}")
                break

            # Process message
            try:
                await process_message(websocket, data)
            except Exception as e:
                logger.error(f"Message processing error: {e}")
                if not await safe_send(websocket, f'{{"type":"error","payload":{{"message":"Internal error"}}}}'):
                    break
    finally:
        manager.disconnect(websocket)
        await safe_close(websocket)
        logger.info("Connection cleaned up")


async def process_message(websocket: WebSocket, data: str) -> None:
    """Process incoming message with validation."""
    import json
    try:
        message = json.loads(data)
        if "type" not in message:
            raise ValueError("Missing message type")
        # Handle message...
        await manager.broadcast(data)
    except json.JSONDecodeError:
        await websocket.send_json({
            "type": "error",
            "payload": {"message": "Invalid JSON"}
        })
```

## Example 7: Complete FastAPI Integration

Full integration with FastAPI application structure.

```python
# app/websocket/__init__.py
from app.websocket.manager import manager
from app.websocket.router import router

__all__ = ["manager", "router"]
```

```python
# app/websocket/manager.py
from collections import defaultdict
from fastapi import WebSocket
import json


class ConnectionManager:
    def __init__(self):
        self.connections: set[WebSocket] = set()
        self.rooms: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections.add(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.connections.discard(websocket)
        for room in self.rooms.values():
            room.discard(websocket)

    def join_room(self, websocket: WebSocket, room_id: str) -> None:
        self.rooms[room_id].add(websocket)

    def leave_room(self, websocket: WebSocket, room_id: str) -> None:
        self.rooms[room_id].discard(websocket)

    async def send_json(self, websocket: WebSocket, data: dict) -> None:
        await websocket.send_text(json.dumps(data))

    async def broadcast_to_room(self, room_id: str, data: dict) -> None:
        message = json.dumps(data)
        dead: set[WebSocket] = set()
        for ws in self.rooms[room_id]:
            try:
                await ws.send_text(message)
            except Exception:
                dead.add(ws)
        for ws in dead:
            self.disconnect(ws)


manager = ConnectionManager()
```

```python
# app/websocket/router.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from app.websocket.manager import manager

router = APIRouter(prefix="/ws", tags=["websocket"])


@router.websocket("")
async def global_websocket(websocket: WebSocket):
    """Global WebSocket endpoint for all connections."""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")

            if msg_type == "join_room":
                room_id = data["payload"]["room_id"]
                manager.join_room(websocket, room_id)
                await manager.send_json(websocket, {
                    "type": "joined",
                    "payload": {"room_id": room_id}
                })

            elif msg_type == "leave_room":
                room_id = data["payload"]["room_id"]
                manager.leave_room(websocket, room_id)

            elif msg_type == "message":
                room_id = data["payload"].get("room_id")
                if room_id:
                    await manager.broadcast_to_room(room_id, data)

    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.websocket("/room/{room_id}")
async def room_websocket(websocket: WebSocket, room_id: str):
    """Room-specific WebSocket endpoint."""
    await manager.connect(websocket)
    manager.join_room(websocket, room_id)

    await manager.broadcast_to_room(room_id, {
        "type": "system",
        "payload": {"message": "User joined the room"}
    })

    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast_to_room(room_id, {
                "type": "message",
                "payload": data
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast_to_room(room_id, {
            "type": "system",
            "payload": {"message": "User left the room"}
        })
```

```python
# app/main.py
from fastapi import FastAPI
from app.websocket import router as ws_router

app = FastAPI(title="WebSocket Example")

# Include WebSocket router
app.include_router(ws_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
```

**Client usage (JavaScript):**

```javascript
// Connect to room
const ws = new WebSocket('ws://localhost:8000/ws/room/general');

ws.onopen = () => {
    console.log('Connected');
    ws.send(JSON.stringify({
        type: 'chat',
        content: 'Hello everyone!'
    }));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};

ws.onclose = () => {
    console.log('Disconnected');
};
```
