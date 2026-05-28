# FastAPI WebSockets Reference

## Basic WebSocket

```python
from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
```

## WebSocket Methods

```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Receive data
    text = await websocket.receive_text()
    data = await websocket.receive_bytes()
    json_data = await websocket.receive_json()

    # Send data
    await websocket.send_text("Hello")
    await websocket.send_bytes(b"bytes")
    await websocket.send_json({"message": "hello"})

    # Close connection
    await websocket.close(code=1000)
```

## WebSocket with Parameters

```python
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: int,
    q: str | None = None,
    token: str = Depends(get_token)
):
    await websocket.accept()
    await websocket.send_text(f"Client {client_id} connected")
```

## Connection Manager Pattern

```python
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left")
```

## WebSocket with Authentication

```python
from fastapi import WebSocket, Query, status

async def get_cookie_or_token(
    websocket: WebSocket,
    session: str | None = Cookie(default=None),
    token: str | None = Query(default=None)
):
    if session or token:
        return session or token
    await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    cookie_or_token: str = Depends(get_cookie_or_token)
):
    await websocket.accept()
    await websocket.send_text(f"Session: {cookie_or_token}")
```
