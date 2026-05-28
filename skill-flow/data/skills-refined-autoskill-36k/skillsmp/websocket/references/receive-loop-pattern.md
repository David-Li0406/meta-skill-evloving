# Receive Loop Pattern

The receive loop is the heart of WebSocket handling - it defines connection lifetime and message entry.

## Why the Loop is Unavoidable

A WebSocket is a **long-lived connection**:
- HTTP: Request → Response → Done (stateless)
- WebSocket: Connect → [Messages...] → Disconnect (stateful)

Something must continuously listen for incoming messages. That "something" is the receive loop.

## Core Pattern

```python
from fastapi import WebSocket, WebSocketDisconnect

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:  # THE RECEIVE LOOP
            data = await websocket.receive_text()
            # Process message...
    except WebSocketDisconnect:
        pass  # Normal exit - client disconnected
    finally:
        # Cleanup always runs
        manager.disconnect(websocket)
```

## Loop Structure Explained

```python
while True:                              # 1. Infinite loop = connection lifetime
    data = await websocket.receive_text()  # 2. Blocks until message or disconnect
    await process(data)                    # 3. Handle the message
```

1. **Infinite loop** - Runs as long as connection is alive
2. **Await receive** - Blocks (yields to event loop) until:
   - A message arrives → returns data
   - Client disconnects → raises `WebSocketDisconnect`
   - Error occurs → raises exception
3. **Process message** - Your business logic

## Exception Handling

```python
try:
    while True:
        data = await websocket.receive_text()
        await process(data)
except WebSocketDisconnect:
    # Normal disconnection - NOT an error
    pass
except Exception as e:
    # Unexpected error - log it
    logger.error(f"WebSocket error: {e}")
finally:
    # ALWAYS runs - guaranteed cleanup
    manager.disconnect(websocket)
```

### Why `WebSocketDisconnect` is Not an Error

```python
# Bad - treating disconnect as error
except Exception as e:
    logger.error(f"Error: {e}")  # Logs normal disconnects as errors

# Good - distinguish normal from abnormal
except WebSocketDisconnect:
    logger.info("Client disconnected")  # Expected behavior
except Exception as e:
    logger.error(f"Unexpected error: {e}")  # Actual problems
```

## Loop Lifetime = Connection Lifetime

```
websocket.accept()
         ↓
    ┌────────────┐
    │            │←──── while True:
    │   LOOP     │        await receive()
    │            │        process()
    └────────────┘
         ↓
    WebSocketDisconnect
         ↓
    manager.disconnect()
```

When the loop exits (for any reason), the connection is done.

## Different Receive Methods

```python
# Text data
data = await websocket.receive_text()

# Binary data
data = await websocket.receive_bytes()

# JSON (automatically parsed)
data = await websocket.receive_json()

# Raw message (includes type info)
message = await websocket.receive()
# message = {"type": "websocket.receive", "text": "..."}
# message = {"type": "websocket.disconnect"}
```

## Loop with Timeout

For connections that should timeout without activity:

```python
import asyncio

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            try:
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=60.0  # 60 second timeout
                )
                await process(data)
            except asyncio.TimeoutError:
                # No message for 60 seconds
                await websocket.send_text('{"type":"ping"}')
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket)
```

## Loop with Background Tasks

Handle messages while running background work:

```python
import asyncio

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    async def receive_messages():
        try:
            while True:
                data = await websocket.receive_text()
                await process(data)
        except WebSocketDisconnect:
            pass

    async def send_updates():
        while True:
            await asyncio.sleep(5)
            await websocket.send_text('{"type":"heartbeat"}')

    try:
        # Run both concurrently
        receive_task = asyncio.create_task(receive_messages())
        send_task = asyncio.create_task(send_updates())

        # Wait for receive to complete (disconnect)
        await receive_task
        send_task.cancel()
    finally:
        manager.disconnect(websocket)
```

## Anti-Patterns

```python
# Bad: No loop - only handles one message
@router.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_text()  # Only one message!
    await websocket.send_text(f"Got: {data}")
    # Connection closes after first message

# Bad: Breaking on valid messages
while True:
    data = await websocket.receive_text()
    if data == "quit":
        break  # Should use close() instead

# Bad: Ignoring cleanup
while True:
    data = await websocket.receive_text()
    # No try/finally - connections leak on error
```

## Best Practices

1. **Always use try/finally** - Ensure cleanup runs
2. **Distinguish disconnect from error** - Don't log normal disconnects as errors
3. **Keep loop body fast** - Offload heavy work to background tasks
4. **Handle all exit paths** - Exceptions, disconnects, and errors
5. **Use appropriate receive method** - `receive_json()` for structured data
