# BridgePlugin API Reference

The `BridgePlugin` abstract base class defines the interface for all bridge implementations.

## Import

```python
from scribe_mcp.bridges import BridgePlugin, BridgeManifest, BridgeState
```

## Class Definition

```python
class BridgePlugin(ABC):
    """Base class for bridge plugins."""

    def __init__(self, manifest: BridgeManifest):
        self.manifest = manifest
        self.bridge_id = manifest.bridge_id
        self.state = BridgeState.REGISTERED
        self._api = None  # Set by registry
```

## Required Methods (Abstract)

### `on_activate()`

```python
@abstractmethod
async def on_activate(self) -> None:
    """Called when bridge transitions to ACTIVE state."""
    pass
```

**Purpose:**
- Establish external connections
- Initialize resources
- Register webhooks
- Start background tasks

**Called when:**
- `registry.activate_bridge(bridge_id)` is called
- Bridge recovers from ERROR state

**On failure:**
- Bridge state transitions to ERROR
- Exception is logged and re-raised

### `on_deactivate()`

```python
@abstractmethod
async def on_deactivate(self) -> None:
    """Called when bridge transitions to INACTIVE state."""
    pass
```

**Purpose:**
- Close external connections
- Clean up resources
- Unregister webhooks
- Stop background tasks

**Must be idempotent** - safe to call multiple times.

**Called when:**
- `registry.deactivate_bridge(bridge_id)` is called
- Before bridge is unregistered
- During graceful shutdown

### `health_check()`

```python
@abstractmethod
async def health_check(self) -> Dict[str, Any]:
    """Return health status for monitoring."""
    pass
```

**Must return dict with at least `{"healthy": bool}`.**

**Recommended fields:**
```python
{
    "healthy": True,
    "message": "All systems operational",
    "latency_ms": 42,
    "last_error": None,
    "uptime_seconds": 3600,
    "connections": {
        "database": "connected",
        "external_api": "connected"
    }
}
```

**Called by:**
- `BridgeHealthMonitor` (periodic checks)
- `registry.health_check_all()`
- Admin CLI health command

## Optional Hook Methods

### `pre_append()`

```python
async def pre_append(self, entry_data: Dict[str, Any]) -> Dict[str, Any]:
    """Called before entry is appended to log."""
    return entry_data
```

**Use cases:**
- Validate entry data
- Enrich with additional metadata
- Transform or normalize data
- Reject invalid entries (raise exception)

**Parameters:**
```python
entry_data = {
    "message": str,
    "status": str,
    "emoji": str,
    "agent": str,
    "meta": dict,
    "timestamp_utc": str
}
```

**Returns:** Modified entry data (or original if no changes)

**On exception:** Entry is rejected (if hook is critical)

### `post_append()`

```python
async def post_append(self, entry_data: Dict[str, Any]) -> None:
    """Called after entry is successfully appended."""
    pass
```

**Use cases:**
- Send notifications
- Update external systems
- Trigger workflows
- Collect analytics

**Fire-and-forget** - exceptions are logged but don't affect the append.

### `pre_rotate()`

```python
async def pre_rotate(self, log_type: str) -> None:
    """Called before log rotation begins."""
    pass
```

**Use cases:**
- Archive data to external storage
- Generate reports
- Send summaries

### `post_rotate()`

```python
async def post_rotate(self, log_type: str, archive_path: str) -> None:
    """Called after log rotation completes."""
    pass
```

**Parameters:**
- `log_type`: Type of log rotated (e.g., "progress")
- `archive_path`: Path to archived log file

### `pre_project_create()`

```python
async def pre_project_create(
    self,
    project_name: str,
    project_config: Dict[str, Any]
) -> Dict[str, Any]:
    """Called before project is created."""
    return project_config
```

**Use cases:**
- Validate project configuration
- Add default metadata
- Apply naming conventions

**Returns:** Modified project config (or original if no changes)

**On exception:** Project creation is rejected (if hook is critical)

### `post_project_create()`

```python
async def post_project_create(
    self,
    project_name: str,
    project_data: Dict[str, Any]
) -> None:
    """Called after project is created."""
    pass
```

**Use cases:**
- Send notifications
- Initialize external resources
- Log project creation

## API Access

### `set_api()`

```python
def set_api(self, api) -> None:
    """Set API instance. Called by registry during registration."""
    self._api = api
```

### `get_api()`

```python
def get_api(self):
    """Get Scribe API instance."""
    if self._api is None:
        raise RuntimeError(f"Bridge {self.bridge_id} API not initialized")
    return self._api
```

**Returns:** `BridgeToScribeAPI` instance

**Raises:** `RuntimeError` if bridge not properly registered

## State Management

### BridgeState Enum

```python
class BridgeState(Enum):
    REGISTERED = "registered"    # Initial state after registration
    ACTIVE = "active"            # Running and processing
    INACTIVE = "inactive"        # Stopped but registered
    ERROR = "error"              # Failed, needs recovery
    UNREGISTERED = "unregistered"  # Removed from registry
```

### State Transitions

```
┌──────────────────────────────────────────────────┐
│                                                  │
│   REGISTERED ──activate──▶ ACTIVE                │
│        │                      │                  │
│        │                      ▼                  │
│        │                   ERROR                 │
│        │                      │                  │
│        │        ◀──recover────┘                  │
│        │                      │                  │
│        ▼                      ▼                  │
│   UNREGISTERED ◀──────── INACTIVE                │
│                                                  │
└──────────────────────────────────────────────────┘
```

## Complete Implementation Example

```python
from scribe_mcp.bridges import BridgePlugin, BridgeManifest, BridgeState
from typing import Dict, Any
import asyncio
import logging

logger = logging.getLogger(__name__)

class CouncilBridgePlugin(BridgePlugin):
    """Council MCP integration bridge."""

    def __init__(self, manifest: BridgeManifest):
        super().__init__(manifest)
        self._background_task = None
        self._connected = False

    async def on_activate(self) -> None:
        """Initialize Council connection."""
        logger.info(f"Activating {self.bridge_id}")

        # Connect to Council
        self._connected = True

        # Start background sync task
        self._background_task = asyncio.create_task(self._sync_loop())

        logger.info(f"Bridge {self.bridge_id} activated successfully")

    async def on_deactivate(self) -> None:
        """Clean up Council connection."""
        logger.info(f"Deactivating {self.bridge_id}")

        # Stop background task
        if self._background_task:
            self._background_task.cancel()
            try:
                await self._background_task
            except asyncio.CancelledError:
                pass

        # Disconnect
        self._connected = False

        logger.info(f"Bridge {self.bridge_id} deactivated")

    async def health_check(self) -> Dict[str, Any]:
        """Check Council connection health."""
        return {
            "healthy": self._connected,
            "message": "Connected" if self._connected else "Disconnected",
            "latency_ms": 5 if self._connected else None
        }

    async def pre_append(self, entry_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich entries with Council metadata."""
        entry_data["meta"] = entry_data.get("meta", {})
        entry_data["meta"]["council_bridge_version"] = self.manifest.version
        entry_data["meta"]["orchestrated"] = True
        return entry_data

    async def post_append(self, entry_data: Dict[str, Any]) -> None:
        """Notify Council of new entry."""
        if self._connected:
            # Send to Council (fire-and-forget)
            logger.debug(f"Notified Council: {entry_data.get('message', '')[:50]}")

    async def pre_rotate(self, log_type: str) -> None:
        """Archive to Council before rotation."""
        logger.info(f"Pre-rotate: archiving {log_type} to Council")

    async def post_rotate(self, log_type: str, archive_path: str) -> None:
        """Record rotation in Council."""
        logger.info(f"Post-rotate: {log_type} archived to {archive_path}")

    async def _sync_loop(self) -> None:
        """Background sync with Council."""
        while True:
            try:
                await asyncio.sleep(60)  # Sync every minute
                logger.debug("Syncing with Council...")
            except asyncio.CancelledError:
                break
```

## Best Practices

1. **Always call `super().__init__(manifest)`** in constructor
2. **Make `on_deactivate()` idempotent** - safe to call multiple times
3. **Keep health checks fast** - should complete in < 1 second
4. **Use logging** - all significant events should be logged
5. **Handle exceptions gracefully** in hooks
6. **Don't block** in async methods - use `asyncio.create_task()` for long operations
7. **Clean up resources** in `on_deactivate()`
