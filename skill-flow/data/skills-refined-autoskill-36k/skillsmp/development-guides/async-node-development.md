# Async Node Development

You are an expert in developing asynchronous nodes with Kailash SDK. Guide users through AsyncNode patterns, async/await usage, and async workflow integration.

## Source Documentation
- `/Users/esperie/repos/dev/kailash_python_sdk/sdk-users/3-development/async-node-guide.md`

## Core Responsibilities

### 1. AsyncNode Pattern
```python
from kailash.nodes.base import AsyncNode, NodeParameter
from typing import Dict, Any
import aiohttp
import asyncio

class MyAsyncNode(AsyncNode):
    """Async node for non-blocking operations."""

    def __init__(self, node_id: str, parameters: Dict[str, Any]):
        super().__init__(node_id, parameters)

        self.add_parameter(NodeParameter(
            name="url",
            param_type="string",
            required=True,
            description="URL to fetch"
        ))

    async def execute_async(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute async operation."""
        url = self.get_parameter("url", inputs)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

                return {
                    "data": data,
                    "status": response.status
                }
```

### 2. Using AsyncLocalRuntime
```python
from kailash.runtime import AsyncLocalRuntime
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()
workflow.add_node("MyAsyncNode", "fetcher", {
    "url": "https://api.example.com/data"
})

# Use AsyncLocalRuntime for async execution
runtime = AsyncLocalRuntime()
results = await runtime.execute_workflow_async(workflow.build(), inputs={})
```

## When to Engage
- User asks about "async nodes", "AsyncNode", "asynchronous development"
- User needs non-blocking operations
- User wants concurrent execution

## Integration with Other Skills
- Route to **custom-development** for node basics
- Route to **production-deployment-guide** for async deployment
