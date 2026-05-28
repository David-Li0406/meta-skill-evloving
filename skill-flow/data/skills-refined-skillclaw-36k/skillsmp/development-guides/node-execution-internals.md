# Node Execution Internals

You are an expert in Kailash SDK node execution internals. Guide users through how nodes work internally, execution lifecycle, and debugging.

## Source Documentation
- `/Users/esperie/repos/dev/kailash_python_sdk/sdk-users/3-development/node-execution-pattern.md`

## Core Responsibilities

### 1. Node Execution Lifecycle
1. **Initialization**: Node created with parameters
2. **Validation**: Parameters validated against schema
3. **Input Reception**: Inputs received from connections
4. **Execution**: `execute()` method called
5. **Output Generation**: Results returned
6. **Connection Propagation**: Outputs passed to connected nodes

### 2. Understanding Node Execution
```python
class CustomNode(Node):
    def __init__(self, node_id: str, parameters: Dict[str, Any]):
        # 1. Initialize base node
        super().__init__(node_id, parameters)

        # 2. Define parameters (validation happens here)
        self.add_parameter(NodeParameter(
            name="input",
            param_type="string",
            required=True
        ))

    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        # 3. Get validated parameters
        input_value = self.get_parameter("input", inputs)

        # 4. Execute logic
        result = process(input_value)

        # 5. Return outputs (keys must match connection targets)
        return {
            "result": result,
            "status": "success"
        }
```

### 3. Debugging Node Execution
```python
import logging

logger = logging.getLogger(__name__)

class DebugNode(Node):
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Node {self.node_id} starting execution")
        logger.debug(f"Inputs: {inputs}")

        try:
            result = self.process_data(inputs)
            logger.info(f"Node {self.node_id} completed successfully")
            return result
        except Exception as e:
            logger.error(f"Node {self.node_id} failed: {e}", exc_info=True)
            raise
```

## When to Engage
- User asks about "node execution", "how nodes work", "node internals"
- User needs to debug node execution
- User wants to understand execution flow

## Integration with Other Skills
- Route to **custom-development** for creating nodes
- Route to **sdk-fundamentals** for basic concepts
