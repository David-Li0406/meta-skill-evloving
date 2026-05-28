# Kaizen Agent Execution

Complete guide to agent.run(), result handling, async execution, and execution strategies in Kaizen.

## Core Execution Pattern

**Key Method**: `agent.run()` - Sync interface to async execution

```python
from kaizen.core.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def process(self, input_data: str) -> dict:
        # agent.run() handles everything:
        # - Strategy execution (AsyncSingleShotStrategy default)
        # - Error handling and retries
        # - Performance tracking
        # - Memory management
        # - Logging
        result = self.run(input_field=input_data)

        return result
```

## What agent.run() Does

**Automatic Features:**
1. ✅ **Async Execution** - Uses AsyncSingleShotStrategy (2-3x faster)
2. ✅ **Signature Validation** - Validates inputs/outputs against signature
3. ✅ **Error Handling** - Catches and handles LLM errors gracefully
4. ✅ **Retry Logic** - Automatic retries on transient failures
5. ✅ **Performance Tracking** - Measures timing, tokens, cost
6. ✅ **Memory Management** - Updates BufferMemory if enabled
7. ✅ **Structured Logging** - Logs execution context
8. ✅ **Result Parsing** - Parses LLM JSON responses to dicts

## Execution Signatures

### Basic Execution

```python
class QASignature(Signature):
    question: str = InputField(description="User question")
    answer: str = OutputField(description="Answer")

class QAAgent(BaseAgent):
    def ask(self, question: str) -> dict:
        # Pass inputs matching signature InputFields
        result = self.run(question=question)

        # result contains OutputFields from signature
        assert "answer" in result
        return result
```

### Multiple Inputs

```python
class AnalysisSignature(Signature):
    text: str = InputField(description="Text to analyze")
    context: str = InputField(description="Context", default="")
    mode: str = InputField(description="Analysis mode", default="standard")

    analysis: str = OutputField(description="Analysis result")

class AnalysisAgent(BaseAgent):
    def analyze(self, text: str, context: str = "", mode: str = "standard") -> dict:
        # Pass all inputs
        result = self.run(text=text, context=context, mode=mode)
        return result
```

### Optional Inputs

```python
class SearchSignature(Signature):
    query: str = InputField(description="Search query")
    filters: dict = InputField(description="Optional filters", default=None)

class SearchAgent(BaseAgent):
    def search(self, query: str, filters: dict = None) -> dict:
        # Optional inputs can be omitted
        if filters:
            result = self.run(query=query, filters=filters)
        else:
            result = self.run(query=query)

        return result
```

## Result Handling

### Accessing Results

```python
def process(self, question: str) -> dict:
    result = self.run(question=question)

    # Direct access (assumes key exists)
    answer = result["answer"]

    # Safe access with get()
    confidence = result.get("confidence", 0.0)

    # Using extract helpers (recommended)
    keywords = self.extract_list(result, "keywords", default=[])

    return {"answer": answer, "confidence": confidence, "keywords": keywords}
```

### Result Structure

```python
result = agent.run(question="What is AI?")

# Standard fields (from signature OutputFields)
result["answer"]       # Main output
result["confidence"]   # If defined in signature

# Performance metadata (added automatically)
result["_timing"]      # Execution time in ms
result["_tokens"]      # Token usage
result["_cost"]        # Estimated cost

# Memory metadata (if memory enabled)
result["_session_id"]  # Session identifier
```

### Error Handling

```python
def process_with_errors(self, data: str) -> dict:
    try:
        result = self.run(data=data)
        return result
    except ValueError as e:
        # Input validation errors
        return {"error": "Invalid input", "details": str(e)}
    except TimeoutError as e:
        # Request timeout
        return {"error": "Request timeout", "details": str(e)}
    except Exception as e:
        # Other errors
        return {"error": "Execution failed", "details": str(e)}
```

## Execution with Memory

### Session-Based Memory

```python
@dataclass
class MemoryConfig:
    llm_provider: str = "openai"
    model: str = "gpt-4"
    max_turns: int = 10  # Enable BufferMemory

class ChatAgent(BaseAgent):
    def chat(self, message: str, session_id: str) -> dict:
        # Memory automatically loaded/saved with session_id
        result = self.run(
            message=message,
            session_id=session_id  # Memory continuity
        )

        return result

# Usage
agent = ChatAgent(MemoryConfig())

result1 = agent.chat("My name is Alice", session_id="user123")
result2 = agent.chat("What's my name?", session_id="user123")
# Returns: "Your name is Alice"
```

### Multi-Turn Conversations

```python
def conversation(self, messages: List[str], session_id: str) -> List[dict]:
    results = []

    for message in messages:
        result = self.run(
            message=message,
            session_id=session_id  # Accumulates context
        )
        results.append(result)

    return results
```

## Async Execution

### AsyncSingleShotStrategy (Default)

```python
# Default strategy (no configuration needed)
class MyAgent(BaseAgent):
    def __init__(self, config):
        # AsyncSingleShotStrategy used automatically
        super().__init__(config=config, signature=MySignature())

    def process(self, data: str) -> dict:
        # run() is sync interface to async execution
        result = self.run(data=data)
        return result
```

**Benefits:**
- ✅ 2-3x faster than sync execution
- ✅ Non-blocking I/O
- ✅ Better resource utilization
- ✅ Same sync API (no async/await in agent code)

### Custom Strategy

```python
from kaizen.strategies.base import Strategy

class CustomStrategy(Strategy):
    """Custom execution strategy."""

    async def execute(self, signature, inputs, config):
        # Pre-processing
        processed_inputs = self.preprocess(inputs)

        # LLM call
        result = await self.llm_call(signature, processed_inputs, config)

        # Post-processing
        return self.postprocess(result)

class MyAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(
            config=config,
            signature=MySignature(),
            strategy=CustomStrategy()  # Use custom strategy
        )
```

## Batch Execution

### Process Multiple Inputs

```python
def batch_process(self, items: List[str]) -> List[dict]:
    results = []

    for item in items:
        result = self.run(item=item)
        results.append(result)

    return results
```

### Parallel Execution

```python
import asyncio
from typing import List

class BatchAgent(BaseAgent):
    async def batch_process_async(self, items: List[str]) -> List[dict]:
        """Process items in parallel."""
        tasks = [
            self._process_one_async(item)
            for item in items
        ]

        results = await asyncio.gather(*tasks)
        return results

    async def _process_one_async(self, item: str) -> dict:
        # Direct async execution (bypass run())
        return await self.strategy.execute(
            self.signature,
            {"item": item},
            self.config
        )
```

## Performance Tracking

### Built-in Metrics

```python
def process_with_metrics(self, data: str) -> dict:
    result = self.run(data=data)

    # Access performance metrics
    timing_ms = result.get("_timing", 0)
    tokens_used = result.get("_tokens", {})
    estimated_cost = result.get("_cost", 0.0)

    print(f"Execution time: {timing_ms}ms")
    print(f"Tokens: {tokens_used}")
    print(f"Cost: ${estimated_cost:.4f}")

    return result
```

### Custom Tracking

```python
import time

def process_with_custom_tracking(self, data: str) -> dict:
    start_time = time.time()

    result = self.run(data=data)

    duration = (time.time() - start_time) * 1000
    result["custom_duration_ms"] = duration

    # Log to monitoring system
    self._log_metrics({
        "duration_ms": duration,
        "success": True,
        "data_size": len(data)
    })

    return result
```

## Integration with Core SDK

### Convert to Workflow

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Create agent
agent = MyAgent(config)

# Convert to workflow
workflow = agent.to_workflow()

# Execute via Core SDK
runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

### Embed in Workflows

```python
def create_workflow_with_agent(agent: BaseAgent) -> WorkflowBuilder:
    workflow = WorkflowBuilder()

    # Add preprocessing
    workflow.add_node("PreprocessNode", "preprocess", {
        "input": "{{inputs.data}}"
    })

    # Add agent as workflow node
    agent_workflow = agent.to_workflow()
    workflow.add_subworkflow("agent", agent_workflow.build())

    # Add postprocessing
    workflow.add_node("PostprocessNode", "postprocess", {
        "input": "{{agent.output}}"
    })

    return workflow
```

## CRITICAL RULES

**ALWAYS:**
- ✅ Call `self.run()`, not `strategy.execute()`
- ✅ Pass inputs matching signature InputFields
- ✅ Handle result errors gracefully
- ✅ Use session_id for memory continuity
- ✅ Let AsyncSingleShotStrategy be default

**NEVER:**
- ❌ Call `strategy.execute()` directly (use `self.run()`)
- ❌ Assume OutputFields exist without checking
- ❌ Skip error handling for production code
- ❌ Manually manage async/await (use `self.run()`)

## Common Patterns

### Retry on Failure

```python
def process_with_retry(self, data: str, max_retries: int = 3) -> dict:
    for attempt in range(max_retries):
        try:
            result = self.run(data=data)
            return result
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2 ** attempt)  # Exponential backoff
```

### Timeout Protection

```python
import signal
from contextlib import contextmanager

@contextmanager
def timeout(seconds):
    def handler(signum, frame):
        raise TimeoutError()
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

def process_with_timeout(self, data: str, timeout_sec: int = 30) -> dict:
    with timeout(timeout_sec):
        result = self.run(data=data)
    return result
```

### Validation Wrapper

```python
def process_with_validation(self, data: str) -> dict:
    # Pre-validation
    if not data or len(data) < 10:
        raise ValueError("Input too short")

    # Execute
    result = self.run(data=data)

    # Post-validation
    if result.get("confidence", 0) < 0.5:
        result["warning"] = "Low confidence result"

    return result
```

## Related Skills

- **kaizen-baseagent-quick** - BaseAgent basics
- **kaizen-signatures** - Defining I/O with signatures
- **kaizen-ux-helpers** - Result extraction helpers
- **kaizen-shared-memory** - Memory management

## References

- **Source**: `apps/kailash-kaizen/src/kaizen/core/base_agent.py`
- **Strategy**: `apps/kailash-kaizen/src/kaizen/strategies/async_single_shot.py`
- **Specialist**: `.claude/agents/frameworks/kaizen-specialist.md` lines 49-93
