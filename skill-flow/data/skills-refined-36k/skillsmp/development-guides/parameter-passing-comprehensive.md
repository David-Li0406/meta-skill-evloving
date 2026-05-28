# Parameter Passing Comprehensive

Enterprise parameter passing patterns for Kailash SDK with security and governance.

## Source Documentation
- `/Users/esperie/repos/dev/kailash_python_sdk/sdk-users/7-gold-standards/parameter_passing_comprehensive.md`

## Core Patterns

### 1. Three Ways to Pass Parameters

**1. Static Parameters (Node Configuration)**
```python
workflow.add_node("HTTPRequestNode", "api_call", {
    "url": "https://api.example.com",
    "method": "GET"
})
```

**2. Dynamic Parameters (Runtime)**
```python
runtime.execute(workflow.build(), parameters={
    "api_call": {"url": "https://different-api.com"}
})
```

**3. Connection-Based (Data Flow)**
```python
workflow.add_connection("source", "output_key", "target", "input_key")
```

### 2. Parameter Scoping (v0.9.31+)

**Node-specific parameters are unwrapped automatically:**

```python
# What you pass:
parameters = {
    "api_key": "global",     # Global param (all nodes)
    "node1": {"value": 10},  # Node-specific
    "node2": {"value": 20}   # Node-specific
}

# What node1 receives (unwrapped):
{
    "api_key": "global",  # Global param
    "value": 10           # Unwrapped from nested dict
}
# node1 does NOT receive node2's parameters (isolated)
```

**Scoping rules:**
- Parameters filtered by node ID
- Node-specific params unwrapped
- Global params (non-node-ID keys) included for all nodes
- Other nodes' params excluded (prevents leakage)

### 3. Parameter Priority
```
Connection-based > Runtime > Static
(Highest)                   (Lowest)
```

### 4. Complex Parameter Patterns
```python
workflow.add_node("PythonCodeNode", "complex", {
    "code": """
# Access parameters directly (automatically injected)
config = {
    'database': {
        'host': db_host,    # From parameter
        'port': db_port,    # From parameter
        'user': db_user     # From parameter
    }
}
result = {'config': config}
"""
})

# Provide via runtime
runtime.execute(workflow.build(), parameters={
    "complex": {
        "db_host": "localhost",
        "db_port": 5432,
        "db_user": "admin"
    }
})
```

### 5. Parameter Validation

```python
from kailash.nodes.base import Node, NodeParameter

class ValidatedNode(Node):
    def get_parameters(self):
        return {
            "api_url": NodeParameter(type=str, required=True),
            "timeout": NodeParameter(type=int, required=False, default=30)
        }

    def run(self, **kwargs):
        # Validate business logic
        api_url = kwargs["api_url"]
        if not api_url.startswith("https://"):
            raise ValueError("API URL must use HTTPS")

        timeout = kwargs.get("timeout", 30)
        if timeout < 1 or timeout > 300:
            raise ValueError("Timeout must be between 1-300 seconds")

        return {"result": "validated"}
```

### 6. Security Patterns

```python
# Parameter isolation prevents data leakage
parameters = {
    "tenant_a_processor": {"tenant_id": "tenant-a", "data": sensitive_a},
    "tenant_b_processor": {"tenant_id": "tenant-b", "data": sensitive_b}
}

# Each node only receives its own parameters
# No cross-tenant data leakage possible
```

### 7. Error Handling (v0.9.31+)

**Validation failures now raise ValueError:**

```python
try:
    runtime = LocalRuntime(connection_validation="invalid")
except ValueError as e:  # Changed from RuntimeExecutionError
    print(f"Configuration error: {e}")

try:
    workflow.build()
except ValueError as e:  # Parameter validation errors
    print(f"Missing parameters: {e}")
```

## When to Engage
- User asks about "enterprise parameters", "parameter governance", "parameter security"
- Complex parameter needs across multiple nodes
- Multi-tenant parameter isolation required
- Parameter validation patterns needed

## Integration with Other Skills
- Route to **param-passing-quick** for basic concepts
- Route to **workflow-quickstart** for workflow building
- Route to **gold-parameter-passing** for compliance patterns
