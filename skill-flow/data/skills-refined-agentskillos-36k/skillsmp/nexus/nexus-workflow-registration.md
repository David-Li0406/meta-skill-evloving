---
skill: nexus-workflow-registration
description: Master workflow registration patterns including manual registration, auto-discovery, versioning, and lifecycle management
priority: HIGH
tags: [nexus, workflow, registration, auto-discovery, versioning]
---

# Nexus Workflow Registration

Master workflow registration patterns from basic to advanced.

## Basic Registration (v1.1.0)

```python
from nexus import Nexus
from kailash.workflow.builder import WorkflowBuilder

app = Nexus()

# Create workflow
workflow = WorkflowBuilder()
workflow.add_node("HTTPRequestNode", "fetch", {
    "url": "https://api.example.com/data",
    "method": "GET"
})

# Register with name - single call exposes on ALL channels
app.register("data-fetcher", workflow.build())

# What happens internally (v1.1.0):
# 1. Nexus stores workflow: self._workflows[name] = workflow
# 2. Gateway registration: self._gateway.register_workflow(name, workflow)
#    → API endpoint: POST /workflows/data-fetcher/execute
#    → CLI command: nexus execute data-fetcher
# 3. MCP registration: self._mcp_channel.register_workflow(name, workflow)
#    → MCP tool: workflow_data-fetcher

# No ChannelManager - Nexus handles everything directly
```

## Critical Rules

### Always Call .build()
```python
# CORRECT
app.register("workflow-name", workflow.build())

# WRONG - Will fail
app.register("workflow-name", workflow)
```

### Correct Parameter Order
```python
# CORRECT - name first, workflow second
app.register(name, workflow.build())

# WRONG - reversed parameters
app.register(workflow.build(), name)
```

## Enhanced Registration with Metadata (v1.1.0)

**NOTE**: Metadata is currently NOT supported in v1.1.0's `register()` method signature.
The method only accepts `(name, workflow)` - no metadata parameter.

```python
# v1.1.0 Reality: No metadata parameter
app.register("data-fetcher", workflow.build())

# Planned for future version:
# app.register("data-fetcher", workflow.build(), metadata={
#     "version": "1.0.0",
#     "description": "Fetches data from external API",
#     "tags": ["data", "api"]
# })

# Current workaround: Store metadata separately
app._workflow_metadata = getattr(app, '_workflow_metadata', {})
app._workflow_metadata["data-fetcher"] = {
    "version": "1.0.0",
    "description": "Fetches data from external API",
    "author": "Development Team",
    "tags": ["data", "api", "production"]
}
```

**What Changed:**
- ❌ `register(name, workflow, metadata)` not supported in v1.1.0
- ✅ Only `register(name, workflow)` signature available
- 🔜 Metadata support planned for future version

## Auto-Discovery

Nexus automatically discovers workflows in these patterns:

### File Patterns
- `workflows/*.py`
- `*.workflow.py`
- `workflow_*.py`
- `*_workflow.py`

### Example Workflow File
```python
# my_workflow.py
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()
workflow.add_node("HTTPRequestNode", "fetch", {
    "url": "https://httpbin.org/json",
    "method": "GET"
})
```

### Enable/Disable Auto-Discovery
```python
# Enable (default)
app = Nexus(auto_discovery=True)

# Disable (recommended with DataFlow)
app = Nexus(auto_discovery=False)
```

## Dynamic Registration

### Runtime Workflow Discovery
```python
from nexus import Nexus
import os
import importlib.util

app = Nexus()

def discover_and_register(directory="./workflows"):
    for filename in os.listdir(directory):
        if filename.endswith("_workflow.py"):
            name = filename[:-12]  # Remove '_workflow.py'

            # Load module
            spec = importlib.util.spec_from_file_location(
                name,
                os.path.join(directory, filename)
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Register workflow
            if hasattr(module, 'workflow'):
                app.register(name, module.workflow.build())
                print(f"Registered: {name}")

discover_and_register()
```

### Configuration-Driven Registration
```python
import yaml

def register_from_config(app, config_file="workflows.yaml"):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    for wf_config in config['workflows']:
        workflow = WorkflowBuilder()

        # Build from config
        for node in wf_config['nodes']:
            workflow.add_node(
                node['type'],
                node['id'],
                node['parameters']
            )

        # Add connections
        for conn in wf_config.get('connections', []):
            workflow.add_connection(
                conn['from_node'], "result",
                conn['to_node'], "input"
            )

        app.register(
            wf_config['name'],
            workflow.build(),
            metadata=wf_config.get('metadata', {})
        )
```

## Workflow Versioning

### Version Management
```python
class WorkflowVersionManager:
    def __init__(self, nexus_app):
        self.app = nexus_app
        self.versions = {}

    def register_version(self, name, workflow, version, metadata=None):
        versioned_name = f"{name}:v{version}"

        # Enhanced metadata
        version_metadata = {
            "version": version,
            "workflow_name": name,
            "registered_at": datetime.now().isoformat(),
            **(metadata or {})
        }

        self.app.register(versioned_name, workflow.build(), metadata=version_metadata)

        # Track versions
        if name not in self.versions:
            self.versions[name] = []
        self.versions[name].append(version)

        # Register as latest
        latest = max(self.versions[name])
        if version == latest:
            self.app.register(f"{name}:latest", workflow.build(), metadata=version_metadata)
            self.app.register(name, workflow.build(), metadata=version_metadata)

    def rollback(self, name, target_version):
        versioned_workflow = self.app.workflows.get(f"{name}:v{target_version}")
        if versioned_workflow:
            self.app.register(name, versioned_workflow.workflow)
            return True
        return False

# Usage
version_mgr = WorkflowVersionManager(app)
version_mgr.register_version("data-api", workflow, "1.0.0")
version_mgr.register_version("data-api", workflow_v2, "2.0.0")
version_mgr.rollback("data-api", "1.0.0")
```

### Blue-Green Deployment
```python
class BlueGreenDeployment:
    def __init__(self, nexus_app):
        self.app = nexus_app
        self.deployments = {}

    def deploy_blue(self, name, workflow, metadata=None):
        blue_name = f"{name}-blue"
        self.app.register(blue_name, workflow.build(), metadata=metadata)
        print(f"Blue deployed: {blue_name}")
        return blue_name

    def deploy_green(self, name, workflow, metadata=None):
        green_name = f"{name}-green"
        self.app.register(green_name, workflow.build(), metadata=metadata)
        print(f"Green deployed: {green_name}")
        return green_name

    def switch_traffic(self, name, target_environment):
        """Switch traffic to blue or green"""
        target_name = f"{name}-{target_environment}"

        if target_name in self.app.workflows:
            target_workflow = self.app.workflows[target_name]
            self.app.register(name, target_workflow.workflow, metadata=target_workflow.metadata)
            print(f"Traffic switched to {target_environment}")
            return True
        return False

# Usage
bg = BlueGreenDeployment(app)

# Deploy production to blue
bg.deploy_blue("data-service", prod_workflow)
bg.switch_traffic("data-service", "blue")

# Deploy new version to green
bg.deploy_green("data-service", new_workflow)

# Test green, then switch
bg.switch_traffic("data-service", "green")
```

## Lifecycle Management

### Lifecycle Hooks
```python
class WorkflowLifecycleManager:
    def __init__(self, nexus_app):
        self.app = nexus_app
        self.hooks = {
            "pre_register": [],
            "post_register": [],
            "pre_execute": [],
            "post_execute": []
        }

    def add_hook(self, event, hook_function):
        self.hooks[event].append(hook_function)

    def trigger_hooks(self, event, context):
        for hook in self.hooks.get(event, []):
            try:
                hook(context)
            except Exception as e:
                print(f"Hook error: {e}")

    def register_with_lifecycle(self, name, workflow, metadata=None):
        context = {
            "name": name,
            "workflow": workflow,
            "metadata": metadata,
            "timestamp": time.time()
        }

        # Pre-registration hooks
        self.trigger_hooks("pre_register", context)

        # Register
        self.app.register(name, workflow.build(), metadata=metadata)

        # Post-registration hooks
        context["registered"] = True
        self.trigger_hooks("post_register", context)

# Define hooks
def validate_workflow(context):
    if not context['workflow'].nodes:
        raise ValueError("Workflow has no nodes")
    print(f"Validated: {context['name']}")

def log_registration(context):
    print(f"Logged: {context['name']} at {context['timestamp']}")

# Use lifecycle management
lifecycle = WorkflowLifecycleManager(app)
lifecycle.add_hook("pre_register", validate_workflow)
lifecycle.add_hook("pre_register", log_registration)
lifecycle.register_with_lifecycle("my-workflow", workflow)
```

## Conditional Registration

```python
def conditional_register(app, name, workflow_factory, condition_func, metadata=None):
    """Register only if condition is met"""
    if condition_func():
        workflow = workflow_factory()
        app.register(name, workflow.build(), metadata=metadata)
        print(f"Registered: {name}")
        return True
    else:
        print(f"Skipped: {name}")
        return False

# Condition functions
def is_production():
    return os.getenv("ENVIRONMENT") == "production"

def has_database_access():
    return check_database_connection()

# Conditional registration
conditional_register(
    app,
    "production-api",
    create_production_workflow,
    is_production,
    metadata={"environment": "production"}
)
```

## Workflow Validation

```python
class WorkflowValidator:
    @staticmethod
    def validate_workflow(workflow, name):
        errors = []
        warnings = []

        # Check structure
        if not workflow.nodes:
            errors.append("No nodes")

        if len(workflow.nodes) == 1:
            warnings.append("Only one node")

        # Check connections
        if len(workflow.nodes) > 1 and not workflow.connections:
            warnings.append("No connections")

        return {"errors": errors, "warnings": warnings}

    @staticmethod
    def safe_register(app, name, workflow, metadata=None, strict=False):
        """Register with validation"""
        result = WorkflowValidator.validate_workflow(workflow, name)

        # Print warnings
        for warning in result["warnings"]:
            print(f"Warning: {warning}")

        # Check errors
        if result["errors"]:
            for error in result["errors"]:
                print(f"Error: {error}")

            if strict:
                raise ValueError(f"Validation failed: {name}")
            return False

        # Register if valid
        app.register(name, workflow.build(), metadata=metadata)
        print(f"Validated and registered: {name}")
        return True

# Usage
validator = WorkflowValidator()
validator.safe_register(app, "my-workflow", workflow)
```

## Best Practices

1. **Always call .build()** before registration
2. **Use descriptive names** for workflows
3. **Add metadata** for documentation and discovery
4. **Validate workflows** before registration
5. **Use versioning** for production deployments
6. **Implement lifecycle hooks** for monitoring
7. **Test registration** in development environment

## Common Issues

### Workflow Not Found
```python
# Ensure .build() is called
app.register("workflow", workflow.build())  # Correct
```

### Auto-Discovery Blocking
```python
# Disable when using DataFlow
app = Nexus(auto_discovery=False)
```

### Registration Order
```python
# Name first, workflow second
app.register(name, workflow.build())  # Correct
```

## Key Takeaways (v1.1.0)

**Registration Flow:**
- ✅ Single `app.register(name, workflow.build())` call
- ✅ Automatically exposes on API, CLI, and MCP channels
- ✅ No ChannelManager - Nexus handles everything directly
- ✅ Enterprise gateway provides multi-channel support

**Current Limitations:**
- ❌ No metadata parameter (use workaround with `_workflow_metadata`)
- ❌ Auto-discovery can block with DataFlow (use `auto_discovery=False`)
- ✅ Versioning and lifecycle management require custom implementation

**Always Remember:**
1. Call `.build()` before registration
2. Use `auto_discovery=False` when integrating with DataFlow
3. Single registration → multi-channel exposure
4. No need to manage channels manually

## Related Skills

- [nexus-quickstart](#) - Basic registration
- [nexus-dataflow-integration](#) - DataFlow workflow registration
- [nexus-production-deployment](#) - Production patterns
- [nexus-troubleshooting](#) - Fix registration issues
