# Bridge Manifest Reference

Complete schema for bridge manifest YAML configuration.

## Location

Bridge manifests are stored in:
```
.scribe/config/bridges/<bridge_id>.yaml
```

Files starting with `_` (e.g., `_template.yaml`) are ignored during discovery.

## Required Fields

```yaml
bridge_id: string       # Unique identifier (alphanumeric, hyphens, underscores only)
name: string            # Human-readable name
version: string         # Semantic version (e.g., "1.0.0")
description: string     # Description of bridge purpose
author: string          # Author name or organization
```

### Validation Rules

- `bridge_id`: Must match pattern `^[a-zA-Z0-9_-]+$`
- `version`: Recommended semantic versioning
- All required fields must be non-empty

## Permissions

```yaml
permissions:
  - read:all_projects     # Read any project's logs
  - read:own_projects     # Read only bridge-owned projects
  - write:all_projects    # Write to any project (admin)
  - write:own_projects    # Write only to bridge-owned projects
  - create:projects       # Create new projects
```

### Permission Hierarchy

| Permission | Read Logs | Write Logs | Create Projects | Modify Any |
|------------|-----------|------------|-----------------|------------|
| `read:all_projects` | ✅ All | ❌ | ❌ | ❌ |
| `read:own_projects` | ✅ Own | ❌ | ❌ | ❌ |
| `write:all_projects` | ❌ | ✅ All | ❌ | ✅ |
| `write:own_projects` | ❌ | ✅ Own | ❌ | ❌ |
| `create:projects` | ❌ | ❌ | ✅ | ❌ |

## Project Configuration

```yaml
project_config:
  can_create_projects: boolean    # Allow project creation (default: false)
  project_prefix: string          # Prefix for created projects (e.g., "my_")
  auto_tag: list[string]          # Tags added to all created projects
  default_metadata: object        # Metadata injected into all projects
```

### Example

```yaml
project_config:
  can_create_projects: true
  project_prefix: "council_"
  auto_tag:
    - automated
    - council-managed
    - production
  default_metadata:
    source: council_mcp
    environment: production
```

### Project Naming

When a bridge creates a project named `my_project`:
- Final name: `{project_prefix}my_project` → `council_my_project`
- `original_name` preserved in metadata
- Tags: `auto_tag` + `["bridge:<bridge_id>"]`

## Hooks Configuration

```yaml
hooks:
  pre_append:
    callback_type: string    # sync|async|webhook (default: async)
    timeout_ms: integer      # Timeout in milliseconds (default: 5000)
    critical: boolean        # If true, failure aborts operation (default: false)

  post_append:
    callback_type: async
    timeout_ms: 5000
    critical: false

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
    critical: false

  post_project_create:
    callback_type: async
    timeout_ms: 5000
    critical: false
```

### Hook Types

| Hook | When Called | Can Modify | Failure Behavior |
|------|-------------|------------|------------------|
| `pre_append` | Before entry logged | Entry data | Aborts if critical |
| `post_append` | After entry logged | Nothing | Fire-and-forget |
| `pre_rotate` | Before log rotation | Nothing | Aborts if critical |
| `post_rotate` | After log rotation | Nothing | Fire-and-forget |
| `pre_project_create` | Before project created | Project config | Aborts if critical |
| `post_project_create` | After project created | Nothing | Fire-and-forget |

### Callback Types

- `sync`: Blocking execution (not recommended)
- `async`: Non-blocking async execution (default)
- `webhook`: HTTP POST to external URL (future)

## Validation Configuration

```yaml
validation:
  mode: string               # strict|lenient|custom (default: lenient)
  schema: object             # JSON Schema for custom validation
  custom_validator: string   # Path to custom validator (for mode: custom)
```

### Validation Modes

- `strict`: All fields validated, unknown fields rejected
- `lenient`: Required fields validated, unknown fields allowed (default)
- `custom`: Use provided schema or custom_validator

## Log Configuration (Optional)

```yaml
log_config:
  custom_audit:
    log_type: string              # Unique log type identifier
    path_template: string         # Path template with placeholders
    format: string                # markdown|jsonl (default: markdown)
    metadata_requirements: list   # Required metadata fields
    rotation_threshold: integer   # Entries before rotation (optional)
    description: string           # Human-readable description
```

### Path Template Placeholders

- `{docs_dir}`: Project docs directory
- `{project_slug}`: Project name slug
- `{progress_log}`: Path to progress log

### Example

```yaml
log_config:
  audit_log:
    log_type: audit_log
    path_template: "{docs_dir}/AUDIT_LOG.md"
    format: markdown
    metadata_requirements:
      - agent_id
      - action_type
    description: Audit trail for compliance
```

## Security

```yaml
api_key: string              # Environment variable reference: ${VAR_NAME}
```

### Environment Variable Expansion

```yaml
api_key: ${MY_BRIDGE_API_KEY}  # Expands from environment
```

If variable not found, `api_key` will be `null`.

## Version Compatibility

```yaml
min_scribe_version: string   # Minimum Scribe version required (default: "2.1.0")
max_scribe_version: string   # Maximum Scribe version supported (optional)
```

## Complete Example

```yaml
bridge_id: council_mcp
name: Council MCP Bridge
version: 1.0.0
description: Integration bridge for Council orchestration MCP
author: Scribe Team

permissions:
  - read:all_projects
  - write:own_projects
  - create:projects

project_config:
  can_create_projects: true
  project_prefix: "council_"
  auto_tag:
    - automated
    - council-managed
  default_metadata:
    source: council_mcp
    orchestration: true

hooks:
  pre_append:
    callback_type: async
    timeout_ms: 5000
    critical: false
  post_append:
    callback_type: async
    timeout_ms: 5000
    critical: false
  pre_rotate:
    callback_type: async
    timeout_ms: 10000
    critical: false
  post_rotate:
    callback_type: async
    timeout_ms: 10000
    critical: false

log_config:
  orchestration_log:
    log_type: orchestration
    path_template: "{docs_dir}/ORCHESTRATION_LOG.md"
    format: markdown
    metadata_requirements:
      - agent_id
      - task_id
    description: Council orchestration audit trail

validation:
  mode: lenient

api_key: ${COUNCIL_MCP_API_KEY}

min_scribe_version: "2.1.0"
```

## Programmatic Access

```python
from scribe_mcp.bridges import BridgeManifest

# From YAML
manifest = registry.load_manifest(Path("path/to/manifest.yaml"))

# From dict
manifest = BridgeManifest.from_dict({
    "bridge_id": "my_bridge",
    "name": "My Bridge",
    "version": "1.0.0",
    "description": "Test bridge",
    "author": "Test"
})

# Validate
errors = manifest.validate()
if errors:
    print(f"Validation errors: {errors}")

# Expand env vars
manifest.expand_env_vars()

# Serialize
json_str = manifest.to_json()
```
