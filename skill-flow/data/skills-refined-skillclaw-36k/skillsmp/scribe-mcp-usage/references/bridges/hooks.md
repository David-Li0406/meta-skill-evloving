# Bridge Hooks Reference

Hooks enable bridges to intercept and modify Scribe operations.

## Hook Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                     append_entry()                          │
│                           │                                 │
│                           ▼                                 │
│   ┌───────────────────────────────────────────────────┐    │
│   │  BridgeHookManager.execute_pre_append(entry_data) │    │
│   │    ├── Bridge A: pre_append() → modified data     │    │
│   │    ├── Bridge B: pre_append() → modified data     │    │
│   │    └── Bridge C: pre_append() → modified data     │    │
│   └───────────────────────────────────────────────────┘    │
│                           │                                 │
│                           ▼                                 │
│            [ Entry written to log file ]                    │
│                           │                                 │
│                           ▼                                 │
│   ┌───────────────────────────────────────────────────┐    │
│   │  BridgeHookManager.execute_post_append(entry_data)│    │
│   │    ├── Bridge A: post_append() → fire-and-forget  │    │
│   │    ├── Bridge B: post_append() → fire-and-forget  │    │
│   │    └── Bridge C: post_append() → fire-and-forget  │    │
│   └───────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## BridgeHookManager

### Import

```python
from scribe_mcp.bridges import BridgeHookManager, get_hook_manager
```

### Global Singleton

```python
# Get the global hook manager instance
manager = get_hook_manager()
```

### Methods

#### `register_bridge()`

```python
def register_bridge(self, bridge: BridgePlugin) -> None:
    """Register a bridge for hook execution."""
```

#### `unregister_bridge()`

```python
def unregister_bridge(self, bridge_id: str) -> None:
    """Remove a bridge from hook execution."""
```

#### `execute_pre_append()`

```python
async def execute_pre_append(self, entry_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute pre_append hooks on all active bridges."""
```

**Behavior:**
- Only ACTIVE bridges are called
- Hooks execute sequentially
- Each hook receives output of previous hook
- Respects timeout from manifest
- Critical hooks abort on failure
- Returns final modified entry data

#### `execute_post_append()`

```python
async def execute_post_append(self, entry_data: Dict[str, Any]) -> None:
    """Execute post_append hooks on all active bridges."""
```

**Behavior:**
- Only ACTIVE bridges are called
- Hooks execute concurrently (fire-and-forget)
- Exceptions are logged but don't abort
- No return value

#### `execute_pre_rotate()`

```python
async def execute_pre_rotate(self, log_type: str) -> None:
    """Execute pre_rotate hooks on all active bridges."""
```

#### `execute_post_rotate()`

```python
async def execute_post_rotate(self, log_type: str, archive_path: str) -> None:
    """Execute post_rotate hooks on all active bridges."""
```

## Hook Configuration

In manifest YAML:

```yaml
hooks:
  pre_append:
    callback_type: async     # sync|async|webhook
    timeout_ms: 5000         # Timeout in milliseconds
    critical: false          # Abort on failure?

  post_append:
    callback_type: async
    timeout_ms: 5000
    critical: false          # Ignored for post hooks

  pre_rotate:
    callback_type: async
    timeout_ms: 10000
    critical: false

  post_rotate:
    callback_type: async
    timeout_ms: 10000
    critical: false

  pre_project_create:
    callback_type: async
    timeout_ms: 5000
    critical: true           # Project creation aborts on failure

  post_project_create:
    callback_type: async
    timeout_ms: 5000
    critical: false
```

## Hook Parameters

### `callback_type`

| Value | Behavior |
|-------|----------|
| `sync` | Blocking execution (not recommended) |
| `async` | Non-blocking async execution (default) |
| `webhook` | HTTP POST to external URL (future) |

### `timeout_ms`

Maximum execution time in milliseconds. Default: 5000.

If hook exceeds timeout:
- `asyncio.TimeoutError` raised
- Hook logged as failed
- If critical: operation aborts
- If not critical: operation continues

### `critical`

If `true` and hook fails:
- Pre-hooks: Operation is aborted
- Post-hooks: Ignored (fire-and-forget)

## Error Handling

### Timeout Example

```python
hooks:
  pre_append:
    timeout_ms: 1000  # 1 second
    critical: true
```

```python
async def pre_append(self, entry_data):
    await asyncio.sleep(2)  # Takes 2 seconds
    return entry_data

# Result: TimeoutError, entry not logged (critical=true)
```

### Exception Example

```python
async def pre_append(self, entry_data):
    raise ValueError("Invalid entry")

# If critical=true: Entry not logged
# If critical=false: Entry logged anyway (default behavior)
```

### Isolation

Bridges are isolated from each other:
- One bridge's failure doesn't affect others
- Hooks execute in order but failures don't cascade
- Post-hooks are fire-and-forget

## Integration with Scribe Tools

### append_entry Integration

```python
# In tools/append_entry.py (simplified)
from bridges.hooks import get_hook_manager

async def append_entry(...):
    hook_manager = get_hook_manager()

    # Pre-hooks can modify entry
    entry_data = await hook_manager.execute_pre_append(entry_data)

    # Write to log
    await storage.insert_entry(...)

    # Post-hooks for notifications
    await hook_manager.execute_post_append(entry_data)
```

### rotate_log Integration

```python
# In tools/rotate_log.py (simplified)
async def rotate_log(...):
    hook_manager = get_hook_manager()

    # Pre-rotate for archival
    await hook_manager.execute_pre_rotate(log_type)

    # Perform rotation
    archive_path = await do_rotation(...)

    # Post-rotate for notifications
    await hook_manager.execute_post_rotate(log_type, archive_path)
```

## Best Practices

### 1. Keep Hooks Fast

```python
# Good: Quick metadata injection
async def pre_append(self, entry_data):
    entry_data["meta"]["timestamp"] = time.time()
    return entry_data

# Bad: Long-running operation
async def pre_append(self, entry_data):
    await self.sync_to_external_db()  # Could timeout
    return entry_data
```

### 2. Use Post-Hooks for Side Effects

```python
# Good: Fire-and-forget notification
async def post_append(self, entry_data):
    asyncio.create_task(self.notify_external_system(entry_data))

# Bad: Critical logic in post-hook
async def post_append(self, entry_data):
    if not await self.update_database():
        raise Exception("Failed!")  # Ignored anyway
```

### 3. Make Pre-Hooks Idempotent

```python
# Good: Safe to run multiple times
async def pre_append(self, entry_data):
    if "bridge_id" not in entry_data.get("meta", {}):
        entry_data["meta"]["bridge_id"] = self.bridge_id
    return entry_data

# Bad: Accumulates on retry
async def pre_append(self, entry_data):
    entry_data["meta"]["call_count"] = entry_data.get("meta", {}).get("call_count", 0) + 1
    return entry_data
```

### 4. Handle Missing Hook Config

```python
# Hook only runs if configured in manifest
hooks:
  pre_append:
    timeout_ms: 5000
  # post_append not configured - won't run
```

### 5. Log Hook Activity

```python
async def pre_append(self, entry_data):
    logger.debug(f"Bridge {self.bridge_id} processing entry")
    # ...
    return entry_data
```

## Security Considerations

### BridgeSecurityManager

```python
from scribe_mcp.bridges import BridgeSecurityManager

# Execute with timeout
result = await BridgeSecurityManager.execute_with_timeout(
    func, timeout_ms=1000
)

# Isolate errors (returns None on failure)
@BridgeSecurityManager.isolate_errors
async def risky_operation():
    ...

# Safe execute with default
result = await BridgeSecurityManager.safe_execute(
    func, timeout_ms=1000, default="fallback"
)
```

### Timeout Enforcement

All hooks are wrapped with timeout enforcement:
- `asyncio.wait_for()` with configured timeout
- Timeout errors logged and handled
- Critical hooks abort, non-critical continue

### Error Isolation

Bridge failures never crash Scribe core:
- All exceptions caught and logged
- Operations continue despite failures
- Health checks can detect issues
