# Rooms Pattern

Logical routing layer for targeted message delivery.

## What is a Room?

A room is NOT a WebSocket feature - it's a **logical grouping** you implement:
- A connection can be in 0 or more rooms
- A connection belongs to exactly 1 manager
- Leaving a room ≠ disconnecting
- Rooms enable subset broadcasting

## Core Data Structure

```python
from collections import defaultdict
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        # All active connections
        self.connections: set[WebSocket] = set()

        # Room → connections mapping
        self.rooms: dict[str, set[WebSocket]] = defaultdict(set)

        # Connection → rooms mapping (for cleanup)
        self.connection_rooms: dict[WebSocket, set[str]] = defaultdict(set)
```

## Implementation

```python
from collections import defaultdict
from fastapi import WebSocket
import json


class ConnectionManager:
    def __init__(self):
        self.connections: set[WebSocket] = set()
        self.rooms: dict[str, set[WebSocket]] = defaultdict(set)
        self.connection_rooms: dict[WebSocket, set[str]] = defaultdict(set)

    async def connect(self, websocket: WebSocket) -> None:
        """Accept and track connection."""
        await websocket.accept()
        self.connections.add(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        """Remove connection and clean up all room memberships."""
        self.connections.discard(websocket)

        # Remove from all rooms this connection was in
        for room_id in self.connection_rooms.pop(websocket, set()):
            self.rooms[room_id].discard(websocket)
            # Clean up empty rooms
            if not self.rooms[room_id]:
                del self.rooms[room_id]

    def join_room(self, websocket: WebSocket, room_id: str) -> None:
        """Add connection to a room."""
        self.rooms[room_id].add(websocket)
        self.connection_rooms[websocket].add(room_id)

    def leave_room(self, websocket: WebSocket, room_id: str) -> None:
        """Remove connection from a room (does NOT disconnect)."""
        self.rooms[room_id].discard(websocket)
        self.connection_rooms[websocket].discard(room_id)

        # Clean up empty room
        if not self.rooms[room_id]:
            del self.rooms[room_id]

    async def broadcast_to_room(
        self,
        room_id: str,
        message: str,
        exclude: WebSocket | None = None
    ) -> None:
        """Send message to all connections in a room."""
        if room_id not in self.rooms:
            return

        dead: set[WebSocket] = set()
        for ws in self.rooms[room_id]:
            if ws != exclude:
                try:
                    await ws.send_text(message)
                except Exception:
                    dead.add(ws)

        # Clean up dead connections
        for ws in dead:
            self.disconnect(ws)

    def get_room_members(self, room_id: str) -> set[WebSocket]:
        """Get all connections in a room."""
        return self.rooms.get(room_id, set()).copy()

    def get_room_count(self, room_id: str) -> int:
        """Get number of connections in a room."""
        return len(self.rooms.get(room_id, set()))

    def get_user_rooms(self, websocket: WebSocket) -> set[str]:
        """Get all rooms a connection is in."""
        return self.connection_rooms.get(websocket, set()).copy()


manager = ConnectionManager()
```

## Usage Example

```python
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.manager import manager
import json

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")

            if msg_type == "join":
                room_id = data["payload"]["room_id"]
                manager.join_room(websocket, room_id)

                # Notify room
                await manager.broadcast_to_room(
                    room_id,
                    json.dumps({
                        "type": "user_joined",
                        "payload": {"room_id": room_id}
                    }),
                    exclude=websocket
                )

                # Confirm to user
                await websocket.send_json({
                    "type": "joined",
                    "payload": {
                        "room_id": room_id,
                        "member_count": manager.get_room_count(room_id)
                    }
                })

            elif msg_type == "leave":
                room_id = data["payload"]["room_id"]
                manager.leave_room(websocket, room_id)

                await manager.broadcast_to_room(
                    room_id,
                    json.dumps({
                        "type": "user_left",
                        "payload": {"room_id": room_id}
                    })
                )

            elif msg_type == "message":
                room_id = data["payload"]["room_id"]
                await manager.broadcast_to_room(room_id, json.dumps(data))

    except WebSocketDisconnect:
        # Get rooms before cleanup
        user_rooms = manager.get_user_rooms(websocket)
        manager.disconnect(websocket)

        # Notify all rooms user was in
        for room_id in user_rooms:
            await manager.broadcast_to_room(
                room_id,
                json.dumps({
                    "type": "user_left",
                    "payload": {"room_id": room_id}
                })
            )
```

## Room-Specific Endpoint

Alternative: URL-based room assignment.

```python
@router.websocket("/ws/room/{room_id}")
async def room_websocket(websocket: WebSocket, room_id: str):
    await manager.connect(websocket)
    manager.join_room(websocket, room_id)

    # Announce arrival
    await manager.broadcast_to_room(
        room_id,
        json.dumps({"type": "user_joined", "payload": {}}),
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
            json.dumps({"type": "user_left", "payload": {}})
        )
```

## Rooms with Metadata

Track additional room information:

```python
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Room:
    id: str
    name: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    connections: set[WebSocket] = field(default_factory=set)
    metadata: dict = field(default_factory=dict)


class ConnectionManager:
    def __init__(self):
        self.connections: set[WebSocket] = set()
        self.rooms: dict[str, Room] = {}

    def create_room(self, room_id: str, name: str, **metadata) -> Room:
        room = Room(id=room_id, name=name, metadata=metadata)
        self.rooms[room_id] = room
        return room

    def get_room(self, room_id: str) -> Room | None:
        return self.rooms.get(room_id)

    def list_rooms(self) -> list[dict]:
        return [
            {
                "id": room.id,
                "name": room.name,
                "member_count": len(room.connections),
                **room.metadata
            }
            for room in self.rooms.values()
        ]
```

## Key Insights

1. **Bidirectional tracking is required**
   - `rooms[room_id]` → connections in room
   - `connection_rooms[ws]` → rooms for connection
   - Both needed for efficient cleanup

2. **Cleanup on disconnect is critical**
   - Must remove from ALL rooms
   - Must clean up empty rooms
   - One disconnect() call handles everything

3. **Leave ≠ Disconnect**
   - `leave_room()` - Connection stays alive, exits one room
   - `disconnect()` - Connection closes, exits all rooms

4. **Exclude sender on broadcast**
   - Don't echo back to sender unless intentional
   - Use `exclude` parameter

## Best Practices

1. **Auto-cleanup empty rooms** - Don't let them accumulate
2. **Track both directions** - Room→connections AND connection→rooms
3. **Use `defaultdict(set)`** - Avoids KeyError on first access
4. **Copy before iteration** - Prevents modification during loop
5. **Notify on join/leave** - Other room members should know
