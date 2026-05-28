# Resource Registry

You are an expert in resource registry patterns for sharing resources across workflows in Kailash SDK.

## Source Documentation
- `/Users/esperie/repos/dev/kailash_python_sdk/sdk-users/3-development/08-resource-registry-guide.md`

## Core Responsibilities

### 1. Resource Registry Pattern
```python
from kailash.core.resource_registry import ResourceRegistry

# Global resource registry
registry = ResourceRegistry()

# Register shared database connection
registry.register("db_connection", database_connection)

# Register shared cache
registry.register("cache", redis_client)

# Use in workflow
workflow.add_node("PythonCodeNode", "use_resource", {
    "code": """
# Access shared resource
db = registry.get("db_connection")
cache = registry.get("cache")

# Use resources
data = db.query("SELECT * FROM users")
cache.set("users", data)

result = {'users': data}
"""
})
```

### 2. Resource Lifecycle Management
```python
class ManagedResource:
    def __enter__(self):
        # Acquire resource
        return self.resource

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Release resource
        self.cleanup()

# Register managed resource
registry.register("managed_db", ManagedResource())
```

## When to Engage
- User asks about "resource registry", "shared resources", "registry pattern"
- User needs to share resources
- User wants resource management

## Integration with Other Skills
- Route to **production-deployment-guide** for deployment
- Route to **advanced-features** for advanced patterns
