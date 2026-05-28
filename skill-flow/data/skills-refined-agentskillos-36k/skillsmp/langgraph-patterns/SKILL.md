---
name: langgraph-patterns
description: Advanced LangGraph patterns for production applications. Use when implementing streaming (tokens, updates, custom data), parallel node execution, subgraphs for modular workflows, error handling and retries, or Command-based control flow. Covers stream modes, fan-out/fan-in, nested graphs, and production best practices.
---

# LangGraph Patterns

Advanced patterns for production LangGraph applications.

## Streaming

### Stream Modes

| Mode | Output | Use Case |
|------|--------|----------|
| `"values"` | Full state after each step | Debugging |
| `"updates"` | Partial updates per node | Progress tracking |
| `"messages"` | LLM tokens as generated | Chat UX |
| `"custom"` | User-defined data | Custom progress |

### Basic Streaming

```python
# Updates mode (most common)
for event in app.stream(inputs, stream_mode="updates"):
    for node_name, output in event.items():
        print(f"{node_name}: {output}")

# Async streaming
async for event in app.astream(inputs, stream_mode="updates"):
    print(event)
```

### Token Streaming

Stream LLM tokens as they generate:

```python
for msg, metadata in app.stream(inputs, stream_mode="messages"):
    if msg.content:
        print(msg.content, end="", flush=True)
```

Filter by node:

```python
for msg, metadata in app.stream(inputs, stream_mode="messages"):
    if metadata["langgraph_node"] == "agent":
        print(msg.content, end="")
```

### Custom Streaming

Send custom data from within nodes:

```python
from langgraph.config import get_stream_writer

def my_node(state: State) -> dict:
    writer = get_stream_writer()
    writer({"progress": "Starting analysis..."})
    # ... do work ...
    writer({"progress": "50% complete"})
    return {"result": "done"}

# Receive custom data
for event in app.stream(inputs, stream_mode=["updates", "custom"]):
    print(event)
```

### Multiple Stream Modes

```python
for event in app.stream(inputs, stream_mode=["updates", "messages"]):
    # event contains both update and message data
    pass
```

## Parallel Execution

### Fan-Out / Fan-In

Multiple nodes execute in parallel, then merge:

```python
from typing import Annotated
import operator

class State(TypedDict):
    input: str
    results: Annotated[list, operator.add]

def task_a(state: State) -> dict:
    return {"results": [f"A: {state['input']}"]}

def task_b(state: State) -> dict:
    return {"results": [f"B: {state['input']}"]}

def merge(state: State) -> dict:
    return {"final": " + ".join(state["results"])}

graph = StateGraph(State)
graph.add_node("task_a", task_a)
graph.add_node("task_b", task_b)
graph.add_node("merge", merge)

graph.add_edge(START, "task_a")
graph.add_edge(START, "task_b")
graph.add_edge(["task_a", "task_b"], "merge")  # Wait for both
graph.add_edge("merge", END)
```

### Async Parallel Within Node

```python
import asyncio

async def parallel_node(state: State) -> dict:
    tasks = [
        fetch_data_a(state["query"]),
        fetch_data_b(state["query"]),
        fetch_data_c(state["query"]),
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Handle failures
    successful = [r for r in results if not isinstance(r, Exception)]
    return {"data": successful}
```

## Subgraphs

Compose graphs for modularity:

```python
# Define subgraph
class SubState(TypedDict):
    query: str
    result: str

sub_builder = StateGraph(SubState)
sub_builder.add_node("process", process_node)
sub_builder.add_edge(START, "process")
sub_builder.add_edge("process", END)
subgraph = sub_builder.compile()

# Use in parent graph
class ParentState(TypedDict):
    query: str
    result: str
    other_data: str

parent = StateGraph(ParentState)
parent.add_node("subgraph", subgraph)  # Add compiled graph as node
parent.add_node("finalize", finalize_node)
parent.add_edge(START, "subgraph")
parent.add_edge("subgraph", "finalize")
parent.add_edge("finalize", END)
```

State mapping (when schemas differ):

```python
def call_subgraph(state: ParentState) -> dict:
    # Map parent state to subgraph input
    sub_input = {"query": state["query"]}
    result = subgraph.invoke(sub_input)
    # Map subgraph output to parent state
    return {"result": result["result"]}

parent.add_node("subgraph", call_subgraph)
```

## Command-Based Control Flow

Use `Command` for complex routing:

```python
from langgraph.types import Command
from typing import Literal

def router_node(state: State) -> Command[Literal["path_a", "path_b", "__end__"]]:
    if state["condition_a"]:
        return Command(
            update={"route": "a"},
            goto="path_a"
        )
    elif state["condition_b"]:
        return Command(
            update={"route": "b"},
            goto="path_b"
        )
    return Command(goto="__end__")
```

### Jump to Parent Graph

From subgraph, return control to parent:

```python
def subgraph_node(state: State) -> Command:
    return Command(
        update={"result": "done"},
        goto="parent_node",
        graph=Command.PARENT
    )
```

## Error Handling

### Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10)
)
async def resilient_node(state: State) -> dict:
    result = await flaky_api_call()
    return {"data": result}
```

### Graceful Degradation

```python
def safe_node(state: State) -> dict:
    try:
        result = risky_operation(state["input"])
        return {"result": result, "error": None}
    except Exception as e:
        return {"result": None, "error": str(e)}

def error_handler(state: State) -> str:
    if state["error"]:
        return "fallback"
    return "continue"

graph.add_conditional_edges("safe_node", error_handler)
```

### Checkpoint Recovery

With checkpointing, resume from last successful step:

```python
try:
    result = app.invoke(inputs, config)
except Exception:
    # Get last successful state
    snapshot = app.get_state(config)
    # Resume or handle error
    result = app.invoke(None, config)  # Retry from checkpoint
```

## Production Patterns

### Rate Limiting

```python
from asyncio import Semaphore

semaphore = Semaphore(5)  # Max 5 concurrent

async def rate_limited_node(state: State) -> dict:
    async with semaphore:
        result = await api_call()
    return {"result": result}
```

### Timeout

```python
import asyncio

async def timed_node(state: State) -> dict:
    try:
        result = await asyncio.wait_for(
            slow_operation(),
            timeout=30.0
        )
        return {"result": result}
    except asyncio.TimeoutError:
        return {"result": None, "error": "timeout"}
```

### Logging and Observability

```python
import logging
from langchain.callbacks import tracing_v2_enabled

logger = logging.getLogger(__name__)

def logged_node(state: State) -> dict:
    logger.info(f"Processing: {state['input'][:50]}...")
    result = process(state)
    logger.info(f"Completed with {len(result)} items")
    return {"result": result}

# With LangSmith tracing
with tracing_v2_enabled(project_name="my-project"):
    result = app.invoke(inputs)
```

## Key Points

- Use `stream_mode="updates"` for progress, `"messages"` for chat
- Fan-in with `add_edge([nodes], target)` waits for all
- Subgraphs enable modular, reusable workflows
- `Command` provides explicit routing control
- Always handle errors gracefully in production
- Use checkpointing for fault-tolerance
