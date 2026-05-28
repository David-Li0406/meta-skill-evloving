# Bridge Permissions Reference

The permission system controls what bridges can do with Scribe resources.

## Permission Types

### Read Permissions

| Permission | Scope | Description |
|------------|-------|-------------|
| `read:all_projects` | Global | Read logs from any project |
| `read:own_projects` | Bridge-owned | Read logs only from bridge-created projects |

### Write Permissions

| Permission | Scope | Description |
|------------|-------|-------------|
| `write:all_projects` | Global | Write to any project (admin level) |
| `write:own_projects` | Bridge-owned | Write only to bridge-created projects |

### Create Permissions

| Permission | Scope | Description |
|------------|-------|-------------|
| `create:projects` | Global | Create new projects |

## Manifest Configuration

```yaml
permissions:
  - read:all_projects
  - write:own_projects
  - create:projects
```

## BridgePolicyPlugin

### Import

```python
from scribe_mcp.bridges import BridgePolicyPlugin
```

### Constructor

```python
policy = BridgePolicyPlugin(manifest, storage_backend=None)
```

**Parameters:**
- `manifest`: `BridgeManifest` instance
- `storage_backend`: Optional storage for ownership lookups

### Methods

#### `can_read_entries()`

```python
def can_read_entries(self, project_name: str) -> bool:
    """Check if bridge can read from project."""
```

Returns `True` if bridge has `read:all_projects` permission.

#### `can_append_entry()`

```python
def can_append_entry(self, project_name: str, log_type: str = "progress") -> bool:
    """Check basic write permission (sync check)."""
```

Returns `True` if:
- Bridge has `write:all_projects`, OR
- Bridge has `write:own_projects`

Note: Does not check ownership (sync method).

#### `can_create_projects()`

```python
def can_create_projects(self) -> bool:
    """Check if bridge can create projects."""
```

Returns `True` if:
- `create:projects` permission present, AND
- `project_config.can_create_projects` is `True`

#### `can_modify_project()` (async)

```python
async def can_modify_project(self, project_name: str) -> bool:
    """Check if bridge can modify project (includes ownership check)."""
```

Returns `True` if:
- Bridge has `write:all_projects` (admin), OR
- Project is not bridge-managed (regular project), OR
- Project is owned by this bridge

#### `can_append_to_project()` (async)

```python
async def can_append_to_project(self, project_name: str, log_type: str) -> bool:
    """Combined log type validation and ownership check."""
```

Returns `True` if:
- Log type is valid, AND
- Bridge can modify project (ownership check)

## Project Ownership

### Bridge-Managed Projects

When a bridge creates a project:

```python
result = await api.create_project("my_project", description="Test")
# Result:
# {
#     "project_name": "bridge_my_project",  # Prefixed
#     "bridge_id": "my_bridge",
#     "bridge_managed": True,
#     ...
# }
```

Database columns:
- `bridge_id`: ID of owning bridge
- `bridge_managed`: Boolean flag (1 = bridge-managed)

### Ownership Rules

```
┌─────────────────────────────────────────────────────────────┐
│                    Project Types                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Bridge-Managed Projects (bridge_managed = True)            │
│  ├── Owner bridge: Full access                              │
│  ├── Other bridges: Denied (unless write:all_projects)      │
│  └── Scribe core: Full access                               │
│                                                             │
│  Regular Projects (bridge_managed = False)                  │
│  ├── All bridges with write:own_projects: Full access       │
│  └── Scribe core: Full access                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Access Decision Flow

```python
async def can_modify_project(project_name: str) -> bool:
    # 1. Admin permission bypasses all checks
    if "write:all_projects" in self.permissions:
        return True

    # 2. Non-bridge-managed projects accessible to all
    project = await storage.fetch_project(project_name)
    if not project or not project.bridge_managed:
        return True

    # 3. Bridge-managed: check ownership
    return project.bridge_id == self.bridge_id
```

## Log Type Validation

### Valid Log Types

Default valid log types:
- `progress`
- `doc_updates`
- `security`
- `bugs`

Custom log types defined in manifest `log_config` are also valid.

### Validation

```python
def _can_use_log_type(self, log_type: str) -> bool:
    """Check if log type is valid."""
    default_types = {"progress", "doc_updates", "security", "bugs"}
    custom_types = set(self.manifest.log_config.keys())
    return log_type in (default_types | custom_types)
```

## Integration with BridgeToScribeAPI

### API Permission Enforcement

```python
from scribe_mcp.bridges import BridgeToScribeAPI, BridgePolicyPlugin

# Create policy and API
policy = BridgePolicyPlugin(manifest, storage)
api = BridgeToScribeAPI(bridge_id, manifest, storage, policy)

# API methods check permissions internally
result = await api.create_project("test")
# Raises PermissionError if not allowed

result = await api.append_entry(project_name, message, ...)
# Raises PermissionError if not allowed
```

### append_entry Permission Check

```python
async def append_entry(self, project_name, message, ...):
    # Check permission
    if not await self._policy.can_append_to_project(project_name, log_type):
        raise PermissionError(
            f"Bridge {self.bridge_id} cannot append to {project_name}"
        )
    # Proceed with append
    ...
```

### create_project Permission Check

```python
async def create_project(self, name, ...):
    # Check permission
    if not self._policy.can_create_projects():
        raise PermissionError(
            f"Bridge {self.bridge_id} cannot create projects"
        )
    # Proceed with creation
    ...
```

## Common Permission Patterns

### Read-Only Bridge

```yaml
permissions:
  - read:all_projects

project_config:
  can_create_projects: false
```

Use case: Monitoring, analytics, reporting

### Standard Integration Bridge

```yaml
permissions:
  - read:all_projects
  - write:own_projects
  - create:projects

project_config:
  can_create_projects: true
  project_prefix: "mybridge_"
```

Use case: External MCP integration

### Admin Bridge

```yaml
permissions:
  - read:all_projects
  - write:all_projects
  - create:projects

project_config:
  can_create_projects: true
```

Use case: Orchestration, cross-project management

### Minimal Bridge

```yaml
permissions:
  - write:own_projects

project_config:
  can_create_projects: false
```

Use case: Write to pre-existing owned projects only

## Security Best Practices

### 1. Principle of Least Privilege

```yaml
# Good: Only what's needed
permissions:
  - read:all_projects
  - write:own_projects

# Bad: Overly permissive
permissions:
  - write:all_projects  # Rarely needed
```

### 2. Use Project Prefixes

```yaml
project_config:
  project_prefix: "mybridge_"  # Clear ownership
```

### 3. Validate in Hooks

```python
async def pre_append(self, entry_data):
    # Additional validation beyond permissions
    if not self._validate_entry(entry_data):
        raise ValueError("Invalid entry data")
    return entry_data
```

### 4. Log Permission Decisions

```python
async def can_modify_project(self, project_name: str) -> bool:
    result = await self._check_permission(project_name)
    logger.debug(
        f"Bridge {self.bridge_id} modify {project_name}: {result}"
    )
    return result
```

### 5. Handle Denials Gracefully

```python
try:
    await api.append_entry(project_name, message)
except PermissionError as e:
    logger.warning(f"Permission denied: {e}")
    # Handle gracefully
```
