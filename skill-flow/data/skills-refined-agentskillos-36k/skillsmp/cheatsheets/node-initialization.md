---
name: node-initialization
description: "Node initialization patterns and parameter handling. Use when asking 'node initialization', 'node parameters', 'initialize nodes', 'node setup', or 'parameter patterns'."
---

# Node Initialization

Node Initialization guide with patterns, examples, and best practices.

> **Skill Metadata**
> Category: `advanced`
> Priority: `HIGH`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Node Initialization
- **Category**: advanced
- **Priority**: HIGH
- **Trigger Keywords**: node initialization, node parameters, initialize nodes, node setup

## Core Pattern

```python
from kailash.nodes.base import Node, NodeParameter
from typing import Dict, Any

class MyNode(Node):
    def __init__(self, name, **kwargs):
        # CRITICAL: Set ALL attributes BEFORE super().__init__()
        # Kailash validates during __init__(), attributes must exist first
        self.my_param = kwargs.get("my_param", "default")
        self.threshold = kwargs.get("threshold", 0.75)

        # NOW call parent init - validation will find attributes
        super().__init__(name=name)

    def get_parameters(self) -> Dict[str, NodeParameter]:
        """Return NodeParameter objects, NOT raw values"""
        return {
            "my_param": NodeParameter(
                name="my_param",
                type=str,
                required=False,
                default=self.my_param,
                description="Custom parameter"
            ),
            "threshold": NodeParameter(
                name="threshold",
                type=float,
                required=False,
                default=0.75,
                description="Processing threshold"
            )
        }

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Required by Kailash - main execution entry point"""
        return {"result": f"Processed with {self.my_param}"}
```

## Common Use Cases

- **Custom Node Development**: Building specialized nodes with proper parameter validation and initialization order
- **LLM/Embedding Integration**: Correctly handling provider-specific formats and required parameters (provider, model, messages)
- **Fixing AttributeError Bugs**: Resolving "object has no attribute" errors by setting attributes before super().__init__()
- **Parameter Type Validation**: Using NodeParameter for proper type checking instead of returning raw values
- **Provider-Specific Formats**: Handling different response formats from Ollama, OpenAI, etc. (embeddings as dicts vs lists)

## Related Patterns

- **For fundamentals**: See [`workflow-quickstart`](#)
- **For patterns**: See [`workflow-patterns-library`](#)
- **For parameters**: See [`param-passing-quick`](#)

## When to Escalate to Subagent

Use specialized subagents when:
- **pattern-expert**: Complex patterns, multi-node workflows
- **sdk-navigator**: Error resolution, parameter issues
- **testing-specialist**: Comprehensive testing strategies

## Documentation References

### Primary Sources
- [`sdk-users/2-core-concepts/cheatsheet/`](../../../sdk-users/2-core-concepts/cheatsheet/)

## Quick Tips

- 💡 **Attributes Before super().__init__()**: Most common error - ALWAYS set all self.attributes BEFORE calling super().__init__() or Kailash validation will fail
- 💡 **Return NodeParameter Objects**: get_parameters() must return Dict[str, NodeParameter], not raw values like int/str/float
- 💡 **Implement Required Methods**: All custom nodes need get_parameters() and run() methods - missing either causes "Can't instantiate abstract class" error
- 💡 **Provider Parameter Required**: LLMAgentNode and embedding nodes require provider="ollama" (or "openai" etc.) parameter in execute() calls
- 💡 **Check Provider Response Format**: Ollama embeddings return dicts with "embedding" key, not lists - use embedding_dict["embedding"] to extract vector
- 💡 **Use .run() Not .process()**: Call node.run() for execution, not .process() or .execute() directly
- 💡 **Test with Real Providers**: Mock data hides provider-specific format issues - always test with actual Ollama/OpenAI/etc.

## Keywords for Auto-Trigger

<!-- Trigger Keywords: node initialization, node parameters, initialize nodes, node setup -->
