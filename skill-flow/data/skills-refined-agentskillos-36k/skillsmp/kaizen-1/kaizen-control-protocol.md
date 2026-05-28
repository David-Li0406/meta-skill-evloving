# Kaizen Control Protocol (v0.2.0+)

Bidirectional agent ↔ client communication for interactive AI agents.

## Overview

Control Protocol enables agents to interact with users during execution:
- **Ask questions** - Get user input mid-execution
- **Request approval** - Confirm dangerous operations
- **Report progress** - Real-time status updates

**Version:** Kaizen v0.2.0+

---

## Quick Start

```python
from kaizen.core.autonomy.control import ControlProtocol
from kaizen.core.autonomy.control.transports import CLITransport

# 1. Create transport
transport = CLITransport()

# 2. Create protocol
protocol = ControlProtocol(transport)
await protocol.start()

# 3. Enable for agent
agent = MyAgent(config, control_protocol=protocol)
```

---

## Core Methods

### ask_user_question()

Ask user to choose from options:

```python
class InteractiveAgent(BaseAgent):
    async def process(self):
        answer = await self.ask_user_question(
            question="Which approach?",
            options=["Fast", "Accurate", "Balanced"],
            default="Balanced"  # Optional
        )
        # Returns: "Fast" | "Accurate" | "Balanced"
```

### request_approval()

Request permission for dangerous operations:

```python
class SafeAgent(BaseAgent):
    async def cleanup(self):
        approved = await self.request_approval(
            action="Delete 100 temp files",
            details={"count": 100, "total_size": "5GB"}
        )

        if approved:
            # Proceed with deletion
            pass
```

### report_progress()

Report execution progress:

```python
class LongRunningAgent(BaseAgent):
    async def process_batch(self, items):
        for i, item in enumerate(items):
            await self.report_progress(
                message=f"Processing {item}",
                percentage=(i / len(items)) * 100
            )
            # Process item...
```

---

## Transports

### CLITransport (Terminal)

For command-line applications:

```python
from kaizen.core.autonomy.control.transports import CLITransport

transport = CLITransport(
    use_rich=True,  # Rich formatting
    use_color=True  # Colored output
)
```

**Use When:**
- CLI tools
- Local development
- Terminal-based agents

### HTTPTransport (Web)

For web applications with SSE:

```python
from kaizen.core.autonomy.control.transports import HTTPTransport

transport = HTTPTransport(
    host="0.0.0.0",
    port=8000
)
await transport.start_server()
```

**Use When:**
- Web UIs
- Real-time dashboards
- Browser-based agents

### StdioTransport (MCP)

For MCP integration:

```python
from kaizen.core.autonomy.control.transports import StdioTransport

transport = StdioTransport()
```

**Use When:**
- MCP servers
- Piped processes
- Inter-process communication

### MemoryTransport (Testing)

For testing without I/O:

```python
from kaizen.core.autonomy.control.transports import MemoryTransport

transport = MemoryTransport()
transport.queue_response("user_answer")  # Preload answers
```

**Use When:**
- Unit tests
- Integration tests
- Automated testing

---

## Complete Example

```python
from kaizen.core.base_agent import BaseAgent
from kaizen.signatures import Signature, InputField, OutputField
from kaizen.core.autonomy.control import ControlProtocol
from kaizen.core.autonomy.control.transports import CLITransport
from dataclasses import dataclass

class InteractiveSignature(Signature):
    task: str = InputField(description="Task description")
    result: str = OutputField(description="Task result")

@dataclass
class InteractiveConfig:
    llm_provider: str = "openai"
    model: str = "gpt-4"

class InteractiveAgent(BaseAgent):
    def __init__(self, config: InteractiveConfig, protocol: ControlProtocol):
        super().__init__(
            config=config,
            signature=InteractiveSignature(),
            control_protocol=protocol
        )

    async def execute_task(self, task: str) -> dict:
        # 1. Ask user for approach
        approach = await self.ask_user_question(
            question="Which approach should I use?",
            options=["Fast", "Thorough", "Balanced"]
        )

        # 2. Process task
        await self.report_progress("Analyzing task", 25.0)
        result = self.run(task=task, approach=approach)

        # 3. Request approval if needed
        if "delete" in task.lower():
            approved = await self.request_approval(
                action="Confirm deletion",
                details={"task": task}
            )
            if not approved:
                return {"result": "Cancelled by user"}

        await self.report_progress("Complete", 100.0)
        return result

# Usage
async def main():
    # Setup
    transport = CLITransport()
    protocol = ControlProtocol(transport)
    await protocol.start()

    # Create agent
    agent = InteractiveAgent(InteractiveConfig(), protocol)

    # Execute
    result = await agent.execute_task("Clean up temp files")
    print(result)
```

---

## Best Practices

### 1. Use Appropriate Transport

```python
# ✅ GOOD - CLI for terminal apps
transport = CLITransport()

# ✅ GOOD - HTTP for web apps
transport = HTTPTransport(host="0.0.0.0", port=8000)

# ✅ GOOD - Memory for tests
transport = MemoryTransport()
```

### 2. Provide Clear Options

```python
# ✅ GOOD - Clear, specific options
options = ["Delete all", "Delete old only", "Cancel"]

# ❌ BAD - Vague options
options = ["Yes", "No", "Maybe"]
```

### 3. Include Defaults

```python
# ✅ GOOD - Sensible default
answer = await self.ask_user_question(
    question="Confirm action?",
    options=["Yes", "No"],
    default="No"  # Safe default
)
```

### 4. Detailed Approval Requests

```python
# ✅ GOOD - Detailed context
approved = await self.request_approval(
    action="Delete files",
    details={
        "count": 100,
        "size": "5GB",
        "location": "/tmp/cache"
    }
)

# ❌ BAD - Vague request
approved = await self.request_approval("Delete stuff")
```

---

## Error Handling

```python
from kaizen.core.autonomy.control.protocol import TimeoutError

try:
    answer = await self.ask_user_question(
        question="Choose option",
        options=["A", "B"],
        timeout=30.0  # 30 seconds
    )
except TimeoutError:
    # Use default or cancel
    answer = "A"
```

---

## Performance

| Transport | Latency (p50) | Latency (p95) | Use Case |
|-----------|---------------|---------------|----------|
| Memory | <1ms | <1ms | Testing |
| CLI | ~50ms | ~100ms | Terminal |
| Stdio | ~20ms | ~50ms | MCP |
| HTTP | ~100ms | ~300ms | Web |

---

## Testing

```python
import pytest
from kaizen.core.autonomy.control.transports import MemoryTransport

@pytest.mark.asyncio
async def test_interactive_agent():
    # Setup memory transport with preloaded answers
    transport = MemoryTransport()
    transport.queue_response("Fast")  # Answer to question
    transport.queue_response(True)    # Approval response

    protocol = ControlProtocol(transport)
    await protocol.start()

    # Create and test agent
    agent = InteractiveAgent(InteractiveConfig(), protocol)
    result = await agent.execute_task("test task")

    assert result["status"] == "completed"
```

---

## Integration

### With Tool Calling

```python
class ToolAwareAgent(BaseAgent):
    async def process_file(self, path: str):
        # Request approval before dangerous tool
        approved = await self.request_approval(
            action="Delete file",
            details={"path": path}
        )

        if approved:
            await self.execute_tool("delete_file", {"path": path})
```

### With Multi-Agent

```python
from kaizen.agents.coordination.supervisor_worker import SupervisorWorkerPattern

# Supervisor can ask questions
class InteractiveSupervisor(BaseAgent):
    async def route_task(self, task):
        # Ask user which worker to use
        worker_choice = await self.ask_user_question(
            question="Which specialist?",
            options=["Data", "Code", "Research"]
        )
        return worker_map[worker_choice]
```

---

## Migration from Custom Solutions

**Before** (Custom prompts):
```python
# Prompt includes: "Choose: Fast, Accurate, or Balanced"
result = agent.run(task=task)
# Parse LLM output to extract choice
```

**After** (Control Protocol):
```python
# Direct user interaction
choice = await agent.ask_user_question(
    question="Choose approach",
    options=["Fast", "Accurate", "Balanced"]
)
result = agent.run(task=task, approach=choice)
```

**Benefits:**
- ✅ No prompt pollution
- ✅ Guaranteed valid input
- ✅ Better UX
- ✅ Cleaner code

---

## Common Patterns

### Progressive Disclosure

```python
# Start with high-level question
approach = await self.ask_user_question("Quick or thorough?", ["Quick", "Thorough"])

if approach == "Thorough":
    # Ask follow-up if needed
    detail_level = await self.ask_user_question(
        "Detail level?",
        ["Normal", "Verbose"]
    )
```

### Approval Chains

```python
# Multiple approval steps
step1_ok = await self.request_approval("Step 1: Backup data")
if not step1_ok:
    return {"status": "cancelled"}

step2_ok = await self.request_approval("Step 2: Delete data")
if not step2_ok:
    return {"status": "cancelled"}
```

### Progress Tracking

```python
steps = ["Load data", "Process", "Validate", "Save"]
for i, step in enumerate(steps):
    await self.report_progress(step, (i / len(steps)) * 100)
    # Execute step...
```

---

## Troubleshooting

**Issue:** `RuntimeError: No control protocol configured`

**Fix:** Pass `control_protocol` to BaseAgent init:
```python
agent = MyAgent(config, control_protocol=protocol)
```

**Issue:** Agent hangs on question

**Fix:** Add timeout:
```python
answer = await self.ask_user_question(
    question="...",
    options=["A", "B"],
    timeout=30.0
)
```

---

## Related

- **[kaizen-tool-calling.md](kaizen-tool-calling.md)** - Autonomous tool execution
- **[kaizen-baseagent-quick.md](kaizen-baseagent-quick.md)** - BaseAgent fundamentals
- **[Control Protocol API Reference](../../../sdk-users/apps/kaizen/docs/reference/control-protocol-api.md)** - Complete API (497 lines)
- **[Control Protocol Tutorial](../../../sdk-users/apps/kaizen/docs/guides/control-protocol-tutorial.md)** - Step-by-step guide (13KB)

---

**Version:** Kaizen v0.2.0+
**Status:** Production-ready ✅
