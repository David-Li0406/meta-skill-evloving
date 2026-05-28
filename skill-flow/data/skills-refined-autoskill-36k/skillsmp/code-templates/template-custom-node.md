---
name: template-custom-node
description: "Generate Kailash custom node template. Use when requesting 'custom node template', 'create custom node', 'extend node', 'node development', or 'custom node boilerplate'."
---

# Custom Node Template

Template for creating custom Kailash SDK nodes with proper parameter declaration and execution patterns.

> **Skill Metadata**
> Category: `cross-cutting` (code-generation)
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`
> Related Skills: [`workflow-quickstart`](../../01-core-sdk/workflow-quickstart.md)
> Related Subagents: `pattern-expert` (advanced node development)

## Basic Custom Node Template

```python
"""Custom Node Implementation"""

from kailash.nodes.base import Node, NodeParameter
from typing import Dict, Any, Optional

class CustomProcessingNode(Node):
    """Custom node for [specific purpose]."""

    def __init__(self, node_id: Optional[str] = None):
        """Initialize custom node."""
        super().__init__(node_id=node_id)

    def get_parameters(self) -> Dict[str, NodeParameter]:
        """Declare all expected parameters."""
        return {
            "input_data": NodeParameter(
                name="input_data",
                type=dict,
                required=True,
                description="Input data to process"
            ),
            "operation": NodeParameter(
                name="operation",
                type=str,
                required=False,
                default="transform",
                description="Operation to perform"
            ),
            "options": NodeParameter(
                name="options",
                type=dict,
                required=False,
                default={},
                description="Additional options"
            )
        }

    def run(self, **kwargs) -> Dict[str, Any]:
        """Execute node logic."""
        # Extract parameters (guaranteed by get_parameters())
        input_data = kwargs["input_data"]
        operation = kwargs.get("operation", "transform")
        options = kwargs.get("options", {})

        # Implement your custom logic
        if operation == "transform":
            result = self._transform_data(input_data, options)
        elif operation == "validate":
            result = self._validate_data(input_data, options)
        else:
            raise ValueError(f"Unknown operation: {operation}")

        return result

    def _transform_data(self, data: dict, options: dict) -> dict:
        """Transform data logic."""
        # Implement transformation
        transformed = {k.upper(): v for k, v in data.items()}
        return {
            "transformed": transformed,
            "status": "success",
            "operation": "transform"
        }

    def _validate_data(self, data: dict, options: dict) -> dict:
        """Validate data logic."""
        # Implement validation
        valid = all(k and v for k, v in data.items())
        return {
            "valid": valid,
            "status": "success",
            "operation": "validate"
        }
```

## Usage in Workflow

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import LocalRuntime

# Register custom node (if needed for discovery)
from kailash.nodes.registry import NodeRegistry
NodeRegistry.register("CustomProcessingNode", CustomProcessingNode)

# Use in workflow
workflow = WorkflowBuilder()

workflow.add_node("CustomProcessingNode", "custom", {
    "input_data": {"name": "test", "value": 123},
    "operation": "transform"
})

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())

print(results["custom"])  # Custom node output
```

## Advanced Template with Validation

```python
from kailash.nodes.base import Node, NodeParameter
from pydantic import BaseModel, Field
from typing import Dict, Any

class CustomNodeContract(BaseModel):
    """Parameter contract for validation."""
    input_data: dict = Field(description="Input data")
    threshold: float = Field(ge=0.0, le=1.0, default=0.5)
    operation: str = Field(pattern="^(filter|transform|aggregate)$")

class AdvancedCustomNode(Node):
    """Custom node with Pydantic validation."""

    def get_parameters(self) -> Dict[str, NodeParameter]:
        """Declare parameters matching contract."""
        return {
            "input_data": NodeParameter(type=dict, required=True),
            "threshold": NodeParameter(type=float, required=False, default=0.5),
            "operation": NodeParameter(type=str, required=False, default="filter")
        }

    def run(self, **kwargs) -> Dict[str, Any]:
        """Execute with validation."""
        # Validate with Pydantic
        validated = CustomNodeContract(**kwargs)

        # Execute logic
        if validated.operation == "filter":
            return self._filter(validated.input_data, validated.threshold)
        # ... more operations

    def _filter(self, data: dict, threshold: float) -> dict:
        """Filter implementation."""
        return {"filtered": data, "threshold": threshold}
```

## Related Patterns

- **Node development**: [`custom-node-guide`](../../06-cheatsheets/custom-node-guide.md)
- **Gold standard**: [`gold-custom-nodes`](../../17-gold-standards/gold-custom-nodes.md)

## When to Escalate

Use `pattern-expert` when:
- Complex custom node architecture
- Performance optimization
- Advanced parameter handling

## Documentation References

### Primary Sources
- **Custom Node Creation**: [`sdk-users/2-core-concepts/cheatsheet/011-custom-node-creation.md`](../../../../sdk-users/2-core-concepts/cheatsheet/011-custom-node-creation.md)
- **Gold Standard**: [`sdk-users/7-gold-standards/custom-node-development-guide.md`](../../../../sdk-users/7-gold-standards/custom-node-development-guide.md)
- **Custom Development**: [`sdk-users/3-development/05-custom-development.md`](../../../../sdk-users/3-development/05-custom-development.md)

## Quick Tips

- 💡 **Declare parameters**: Always implement `get_parameters()`
- 💡 **Type validation**: Use Pydantic for complex validation
- 💡 **Error handling**: Implement proper error handling
- 💡 **Documentation**: Add docstrings for all methods

<!-- Trigger Keywords: custom node template, create custom node, extend node, node development, custom node boilerplate, custom node example, develop node -->
