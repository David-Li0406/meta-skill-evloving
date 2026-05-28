# Workflows API Reference

Workflows provide graph-based orchestration for multi-step and multi-agent processes.

## Installation

```bash
# Python
pip install agent-framework --pre
# Includes agent-framework-workflows

# .NET
dotnet add package Microsoft.Agents.AI --prerelease
```

---

## Core Concepts

- **Executor**: A unit of work (agent, function, or sub-workflow)
- **Edge**: Defines data flow between executors
- **Workflow**: Graph connecting executors via edges
- **Checkpoint**: Saved state for recovery/resumption

---

## Executor (Python)

Base class for workflow steps. Use `@Executor.register` decorator.

```python
from agent_framework.workflows import Executor
from pydantic import BaseModel

# Define typed input/output
class StepInput(BaseModel):
    query: str
    
class StepOutput(BaseModel):
    result: str
    confidence: float

# Create executor
@Executor.register
class ProcessStep(Executor[StepInput, StepOutput]):
    async def execute(self, input: StepInput, context) -> StepOutput:
        # Your logic here
        return StepOutput(
            result=f"Processed: {input.query}",
            confidence=0.95
        )
```

---

## AgentExecutor

Wrap a ChatAgent as an executor:

```python
from agent_framework import ChatAgent
from agent_framework.workflows import AgentExecutor

agent = ChatAgent(
    chat_client=client,
    instructions="You analyze data."
)

executor = AgentExecutor(
    agent=agent,
    name="analyzer",
    # Optional: transform input/output
    input_transformer=lambda x: x.query,
    output_transformer=lambda result: {"analysis": result.text}
)
```

---

## FunctionExecutor

Wrap a function as an executor:

```python
from agent_framework.workflows import FunctionExecutor

async def process_data(input_data: dict) -> dict:
    return {"processed": input_data["raw"]}

executor = FunctionExecutor(
    func=process_data,
    name="processor"
)
```

---

## Edge

Defines connections between executors:

```python
from agent_framework.workflows import Edge

# Basic edge
Edge(source="executor_a", target="executor_b")

# Edge from start
Edge(source="start", target="first_executor")

# Edge to end
Edge(source="last_executor", target="end")

# Conditional edge
Edge(
    source="router",
    target="handler_a",
    condition=lambda output: output.route == "A"
)
```

---

## Workflow

Combines executors and edges:

```python
from agent_framework.workflows import Workflow, Edge

workflow = Workflow(
    executors=[
        ProcessStep(),
        AgentExecutor(agent=agent, name="analyzer"),
        FunctionExecutor(func=format_output, name="formatter")
    ],
    edges=[
        Edge(source="start", target=ProcessStep),
        Edge(source=ProcessStep, target="analyzer"),
        Edge(source="analyzer", target="formatter"),
        Edge(source="formatter", target="end")
    ]
)
```

### Running a Workflow

```python
# Direct execution
result = await workflow.run({"query": "analyze this"})

# As an agent
workflow_agent = workflow.as_agent(name="analysis-workflow")
result = await workflow_agent.run("analyze this")

# Streaming
async for update in workflow_agent.run_streaming("analyze this"):
    print(update)
```

---

## Built-in Orchestration Patterns

### SequentialOrchestration

Agents run one after another:

```python
from agent_framework.workflows.orchestrations import SequentialOrchestration

orchestration = SequentialOrchestration(
    agents=[researcher, writer, editor],
    name="content-pipeline"
)

result = await orchestration.run("Write about AI agents")
```

### ConcurrentOrchestration (Fan-out/Fan-in)

Agents run in parallel, results aggregated:

```python
from agent_framework.workflows.orchestrations import ConcurrentOrchestration

orchestration = ConcurrentOrchestration(
    agents=[analyst1, analyst2, analyst3],
    aggregator=summarizer,  # Combines all results
    name="parallel-analysis"
)
```

### HandoffOrchestration

Route to specialized agents:

```python
from agent_framework.workflows.orchestrations import HandoffOrchestration

orchestration = HandoffOrchestration(
    router=classifier_agent,  # Decides which specialist
    specialists={
        "billing": billing_agent,
        "technical": tech_support_agent,
        "general": general_agent
    },
    name="support-router"
)
```

### MagenticOrchestration

Complex multi-agent collaboration:

```python
from agent_framework.workflows.orchestrations import MagenticOrchestration

orchestration = MagenticOrchestration(
    planner=planner_agent,
    specialists=[researcher, coder, writer, reviewer],
    name="complex-task"
)
```

### ReflectionOrchestration

Self-improvement through iteration:

```python
from agent_framework.workflows.orchestrations import ReflectionOrchestration

orchestration = ReflectionOrchestration(
    actor=writer_agent,
    critic=reviewer_agent,
    max_iterations=3,  # Stop after 3 refinements
    name="iterative-writer"
)
```

---

## Checkpointing

Save and resume workflow state:

```python
from agent_framework.workflows import Workflow
from agent_framework.workflows.checkpoints import (
    InMemoryCheckpointStore,
    CosmosCheckpointStore
)

# Development: In-memory
checkpoint_store = InMemoryCheckpointStore()

# Production: Cosmos DB
checkpoint_store = CosmosCheckpointStore(
    connection_string="...",
    database_name="workflows",
    container_name="checkpoints"
)

workflow = Workflow(
    executors=[...],
    edges=[...],
    checkpoint_store=checkpoint_store
)

# Run with checkpointing
result = await workflow.run(
    input={"task": "long running task"},
    checkpoint_id="run-123"  # Identifier for this run
)

# Resume from checkpoint (e.g., after crash)
result = await workflow.run(
    input={"task": "continue"},
    checkpoint_id="run-123"  # Same ID to resume
)
```

---

## Human-in-the-Loop

Pause workflow for human input:

```python
from agent_framework.workflows import RequestResponseExecutor
from pydantic import BaseModel

class ApprovalRequest(BaseModel):
    action: str
    risk_level: str
    details: str

class ApprovalResponse(BaseModel):
    approved: bool
    reason: str
    approver: str

@Executor.register
class HumanApproval(RequestResponseExecutor[ApprovalRequest, ApprovalResponse]):
    """Workflow pauses here until response received."""
    pass

# In workflow
workflow = Workflow(
    executors=[
        analyzer,
        HumanApproval(),
        executor_after_approval
    ],
    edges=[
        Edge(source="start", target="analyzer"),
        Edge(source="analyzer", target=HumanApproval),
        Edge(source=HumanApproval, target="executor_after_approval"),
    ]
)

# Workflow pauses at HumanApproval
# Later, provide response:
await workflow.respond(
    executor_name="HumanApproval",
    response=ApprovalResponse(
        approved=True,
        reason="Risk acceptable",
        approver="admin@company.com"
    )
)
```

---

## Workflow Context

Share state between executors:

```python
@Executor.register
class MyExecutor(Executor[Input, Output]):
    async def execute(self, input: Input, context) -> Output:
        # Read shared state
        previous = context.get("previous_result")
        
        # Write shared state
        context.set("my_key", my_value)
        
        # Access workflow metadata
        run_id = context.run_id
        
        return Output(...)
```

---

## Type Safety

Workflows validate type compatibility:

```python
class OutputA(BaseModel):
    value: int

class InputB(BaseModel):
    value: str  # Type mismatch!

# This will raise ValidationError at construction time
workflow = Workflow(
    executors=[ExecutorA(), ExecutorB()],  # OutputA -> InputB fails
    edges=[Edge(source=ExecutorA, target=ExecutorB)]
)
```

---

## Best Practices

1. **New instance per request**: Don't share workflow instances across concurrent requests
2. **Use checkpoints for long-running**: Enable recovery from failures
3. **Type your data models**: Use Pydantic for validation
4. **Keep executors focused**: Single responsibility per executor
5. **Test with InMemoryCheckpointStore**: Before production deployment
6. **Handle errors at executor level**: Return error states, don't throw
