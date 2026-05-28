# Error Handling Pattern

Defensive patterns for production WebSocket reliability.

## Core Principle

> Disconnections are expected, not exceptional.
> One failure must not cascade to others.

## The Reality of WebSocket Connections

WebSocket connections fail constantly:
- Network interruptions
- Client closes browser tab
- Mobile device sleeps
- Server restarts
- Proxy timeouts

Your code must handle ALL of these gracefully.

## Essential Try/Finally Structure

```python
from fastapi import WebSocket, WebSocketDisconnect

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await process(data)
    except WebSocketDisconnect:
        pass  # Normal exit
    finally:
        manager.disconnect(websocket)  # ALWAYS cleanup
```

The `finally` block runs regardless of:
- Normal disconnect
- Exception
- Server shutdown

## Distinguishing Error Types

```python
import logging
from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            try:
                data = await websocket.receive_text()
            except WebSocketDisconnect:
                logger.debug("Client disconnected normally")
                break  # Exit loop
            except Exception as e:
                logger.warning(f"Receive error: {e}")
                break  # Exit loop

            try:
                await process_message(websocket, data)
            except ValueError as e:
                # Business logic error - inform client, continue
                await safe_send(websocket, f'{{"type":"error","payload":{{"message":"{e}"}}}}')
            except Exception as e:
                # Unexpected error - log and continue
                logger.error(f"Processing error: {e}")
    finally:
        manager.disconnect(websocket)
```

## Safe Send Helper

Writes can fail even when connection appears alive:

```python
from starlette.websockets import WebSocketState


async def safe_send(websocket: WebSocket, message: str) -> bool:
    """
    Safely send message to websocket.
    Returns True if successful, False if connection is dead.
    """
    if websocket.client_state != WebSocketState.CONNECTED:
        return False

    try:
        await websocket.send_text(message)
        return True
    except Exception:
        return False


async def safe_send_json(websocket: WebSocket, data: dict) -> bool:
    """Safely send JSON data."""
    if websocket.client_state != WebSocketState.CONNECTED:
        return False

    try:
        await websocket.send_json(data)
        return True
    except Exception:
        return False
```

Usage:

```python
if not await safe_send(websocket, message):
    manager.disconnect(websocket)
    return  # Exit handler
```

## Safe Close Helper

```python
async def safe_close(websocket: WebSocket, code: int = 1000) -> None:
    """Safely close WebSocket connection."""
    if websocket.client_state == WebSocketState.CONNECTED:
        try:
            await websocket.close(code=code)
        except Exception:
            pass  # Already closed or errored
```

## Broadcast with Cleanup

Handle failures during fan-out:

```python
async def broadcast(self, message: str) -> None:
    """Broadcast to all, cleaning up dead connections."""
    dead: set[WebSocket] = set()

    for connection in self.active_connections.copy():  # Copy to allow modification
        try:
            await connection.send_text(message)
        except Exception:
            dead.add(connection)

    # Remove dead connections after iteration
    for ws in dead:
        self.disconnect(ws)
```

## Connection Accept Failures

The `accept()` call can fail:

```python
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
    except Exception as e:
        logger.error(f"Failed to accept connection: {e}")
        return  # Cannot proceed

    # Now safe to use manager
    manager.add(websocket)
    try:
        ...
    finally:
        manager.disconnect(websocket)
```

## Timeout Handling

Detect stale connections:

```python
import asyncio

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            try:
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=120.0  # 2 minute timeout
                )
                await process(data)
            except asyncio.TimeoutError:
                # No message for 2 minutes - send ping
                if not await safe_send(websocket, '{"type":"ping"}'):
                    break  # Connection dead
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(websocket)
```

## Close Codes

Use appropriate WebSocket close codes:

```python
# Normal closure
await websocket.close(code=1000)

# Going away (server shutdown)
await websocket.close(code=1001)

# Protocol error
await websocket.close(code=1002)

# Invalid data
await websocket.close(code=1003)

# Policy violation
await websocket.close(code=1008)

# Message too big
await websocket.close(code=1009)

# Internal error
await websocket.close(code=1011)
```

## Complete Error-Resilient Endpoint

```python
import asyncio
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState

router = APIRouter()
logger = logging.getLogger(__name__)


async def safe_send(ws: WebSocket, msg: str) -> bool:
    if ws.client_state != WebSocketState.CONNECTED:
        return False
    try:
        await ws.send_text(msg)
        return True
    except Exception:
        return False


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Accept with error handling
    try:
        await manager.connect(websocket)
    except Exception as e:
        logger.error(f"Connection failed: {e}")
        return

    try:
        while True:
            # Receive with timeout
            try:
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=300.0
                )
            except asyncio.TimeoutError:
                if not await safe_send(websocket, '{"type":"ping"}'):
                    logger.info("Connection stale, closing")
                    break
                continue
            except WebSocketDisconnect:
                logger.debug("Client disconnected")
                break
            except Exception as e:
                logger.warning(f"Receive error: {e}")
                break

            # Process with error handling
            try:
                await process_message(websocket, data)
            except ValueError as e:
                await safe_send(websocket, f'{{"type":"error","payload":{{"message":"{e}"}}}}')
            except Exception as e:
                logger.error(f"Processing error: {e}", exc_info=True)

    finally:
        manager.disconnect(websocket)
        logger.debug("Connection cleaned up")
```

## Best Practices

1. **Always use try/finally** - Guarantee cleanup
2. **Distinguish WebSocketDisconnect** - Not an error
3. **Check connection state before send** - Avoid exceptions
4. **Copy collections before iterating** - Prevent modification during loop
5. **Log at appropriate levels** - Debug for normal, warning for unusual, error for problems
6. **Use timeouts** - Detect stale connections
7. **Clean up eagerly** - Don't wait for garbage collection

## Anti-Patterns

```python
# Bad: No cleanup
while True:
    data = await websocket.receive_text()  # Leaks on exception

# Bad: Treating disconnect as error
except Exception as e:
    logger.error(f"Error: {e}")  # Logs normal disconnects

# Bad: Not checking state before send
await websocket.send_text(msg)  # May raise if disconnected

# Bad: Not copying before iteration
for ws in self.connections:  # RuntimeError if modified
    await ws.send_text(msg)
```
