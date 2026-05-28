# BaseAgent Quick Implementation

Quick reference for implementing custom agents with Kaizen's BaseAgent architecture.

## Pattern: Extend BaseAgent (3 Steps)

```python
from kaizen.core.base_agent import BaseAgent
from kaizen.signatures import Signature, InputField, OutputField
from dataclasses import dataclass

# Step 1: Define Domain Configuration
@dataclass
class MyConfig:
    """Domain-specific configuration (NOT BaseAgentConfig)."""
    llm_provider: str = "openai"
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000
    # Add custom domain fields as needed

# Step 2: Define Signature (Type-Safe I/O)
class MySignature(Signature):
    """Define inputs and outputs with descriptions."""
    # Inputs
    question: str = InputField(description="User question")
    context: str = InputField(description="Additional context", default="")

    # Outputs
    answer: str = OutputField(description="Agent response")
    confidence: float = OutputField(description="Confidence score 0.0-1.0")
    reasoning: str = OutputField(description="Brief reasoning")

# Step 3: Extend BaseAgent
class MyAgent(BaseAgent):
    """Custom agent with domain-specific logic."""

    def __init__(self, config: MyConfig):
        # BaseAgent auto-converts domain config → BaseAgentConfig
        super().__init__(config=config, signature=MySignature())
        self.domain_config = config  # Keep reference if needed

    def process(self, question: str, context: str = "") -> dict:
        """
        Process user input and return structured result.

        BaseAgent.run() automatically provides:
        - Async execution (AsyncSingleShotStrategy)
        - Error handling and retries
        - Performance tracking
        - Memory management (if configured)
        - Logging
        """
        result = self.run(question=question, context=context)

        # Optional: Add domain-specific processing
        if result.get("confidence", 0) < 0.5:
            result["warning"] = "Low confidence response"

        return result
```

## What BaseAgent Provides Automatically

**Core Features:**
- ✅ Config auto-conversion (domain config → BaseAgentConfig)
- ✅ Async execution (2-3x faster than sync)
- ✅ Error handling with automatic retries
- ✅ Performance tracking (timing, tokens, cost)
- ✅ Structured logging with context
- ✅ Memory management (optional, via BufferMemory)
- ✅ A2A capability cards (`to_a2a_card()`)
- ✅ Workflow generation (`to_workflow()`)
- ✅ **Autonomous tool calling (v0.2.0)** - opt-in via `tool_registry`
- ✅ **Bidirectional communication (v0.2.0)** - opt-in via `control_protocol`

**Code Reduction:**
- Traditional agent: ~496 lines
- BaseAgent-based: ~65 lines
- **87% reduction** with more features

## Usage Example

```python
from dotenv import load_dotenv
load_dotenv()  # Load API keys from .env

# Create agent
config = MyConfig(llm_provider="openai", model="gpt-4")
agent = MyAgent(config)

# Execute
result = agent.process("What is quantum computing?")
print(result["answer"])
print(f"Confidence: {result['confidence']}")
print(f"Reasoning: {result['reasoning']}")
```

## With Memory Enabled

```python
@dataclass
class MyConfig:
    llm_provider: str = "openai"
    model: str = "gpt-4"
    max_turns: int = 10  # Enable BufferMemory

agent = MyAgent(config)

# Use session_id for memory continuity
result1 = agent.process("My name is Alice", session_id="user123")
result2 = agent.process("What's my name?", session_id="user123")
# Returns: "Your name is Alice"
```

## Multi-Agent with Shared Memory

```python
from kaizen.memory.shared_memory import SharedMemoryPool

shared_pool = SharedMemoryPool()

researcher = ResearcherAgent(config, shared_pool, agent_id="researcher")
analyst = AnalystAgent(config, shared_pool, agent_id="analyst")

# Agent 1: Research and write findings
findings = researcher.research("AI trends 2025")

# Agent 2: Read findings and analyze
insights = shared_pool.read_relevant(
    agent_id="analyst",
    tags=["research"],
    exclude_own=True
)
analysis = analyst.analyze(insights)
```

## Async Execution with run_async()

**For production FastAPI applications and high-throughput scenarios.**

### Configuration

```python
from kaizen.core.base_agent import BaseAgent
from dataclasses import dataclass

@dataclass
class AsyncConfig:
    llm_provider: str = "openai"
    model: str = "gpt-4"
    use_async_llm: bool = True  # ← Enable async mode

agent = MyAgent(AsyncConfig())
```

### Usage in FastAPI

```python
from fastapi import FastAPI
app = FastAPI()

@app.post("/api/chat")
async def chat(request: ChatRequest):
    result = await agent.run_async(question=request.message)
    return {"response": result["answer"]}
```

### Concurrent Execution

```python
# Execute 100 requests concurrently
tasks = [
    agent.run_async(question=f"Question {i}")
    for i in range(100)
]
results = await asyncio.gather(*tasks)  # All run in parallel
```

### Performance Comparison

| Scenario | run() (sync) | run_async() (async) |
|----------|--------------|---------------------|
| Single request | 500ms | 500ms (same) |
| 10 concurrent | 5000ms (queued) | 500ms (parallel) |
| 100 concurrent | 50000ms + timeouts | 500ms (parallel) |

### When to Use

**Use run_async():**
- FastAPI/async web apps
- High-throughput (10+ concurrent requests)
- Docker deployments with AsyncLocalRuntime

**Use run():**
- CLI scripts and tools
- Jupyter notebooks
- Simple sequential workflows

## v0.2.0: Autonomous Tool Calling (Opt-In)

```python
# Tools auto-configured via MCP

# Enable tool calling

# 12 builtin tools enabled via MCP

class FileAgent(BaseAgent):
    def __init__(self, config: MyConfig):
        super().__init__(
            config=config,
            signature=MySignature(),
            tools="all"  # Enable 12 builtin tools via MCP
        )

    async def process_file(self, path: str) -> dict:
        # Execute tool with automatic approval workflow
        result = await self.execute_tool(
            tool_name="read_file",
            params={"path": path},
            store_in_memory=True
        )
        return result

agent = FileAgent(config)
result = await agent.process_file("/tmp/data.txt")
```

**12 Builtin Tools**: File (5), HTTP (4), Bash (1), Web (2)
**Approval Workflows**: SAFE (auto-approved) → LOW → MEDIUM → HIGH → CRITICAL

## v0.2.0: Interactive Agents with Control Protocol (Opt-In)

```python
from kaizen.core.autonomy.control.protocol import ControlProtocol
from kaizen.core.autonomy.control.transports import CLITransport

# Enable bidirectional communication
transport = CLITransport()
await transport.connect()
protocol = ControlProtocol(transport)

class InteractiveAgent(BaseAgent):
    def __init__(self, config: MyConfig):
        super().__init__(
            config=config,
            signature=MySignature(),
            control_protocol=protocol  # Enable interaction
        )

    async def process_interactive(self, task: str) -> dict:
        # Ask user for clarification
        approach = await self.ask_user_question(
            question="Which approach to use?",
            options=["Fast", "Accurate", "Balanced"]
        )

        # Request approval for risky operation
        approved = await self.request_approval(
            action="delete_temp_files",
            details={"count": 150, "size_mb": 2.3}
        )

        # Report progress
        await self.report_progress(
            message="Processing...",
            percentage=50.0
        )

        return self.run(task=task, approach=approach)
```

**4 Transports**: CLI, HTTP/SSE, stdio, memory
**<20ms latency** for real-time interaction

## CRITICAL RULES

**ALWAYS:**
- ✅ Use domain configs (e.g., `MyConfig`), let BaseAgent auto-convert
- ✅ Call `self.run()`, not `strategy.execute()`
- ✅ Load `.env` with `load_dotenv()` before creating agents
- ✅ Let AsyncSingleShotStrategy be default (don't specify)

**NEVER:**
- ❌ Create BaseAgentConfig manually (use auto-conversion)
- ❌ Call `strategy.execute()` directly (use `self.run()`)
- ❌ Skip loading `.env` file

## Code Reduction Benefits

**Traditional Agent (496 lines):**
```python
class TraditionalAgent:
    def __init__(self, model, temperature, ...):
        self.model = model
        self.temperature = temperature
        self.memory = []  # Manual memory
        self.logger = logging.getLogger(...)  # Manual logging
        # ... 50+ lines of setup

    def process(self, input_data):
        # Manual prompt construction
        # Manual error handling
        # Manual retry logic
        # Manual performance tracking
        # Manual memory management
        # ... 100+ lines
```

**BaseAgent-Based (65 lines):**
```python
class MyAgent(BaseAgent):
    def __init__(self, config: MyConfig):
        super().__init__(config=config, signature=MySignature())

    def process(self, input_data):
        return self.run(input_field=input_data)
```

All features (logging, error handling, retries, performance tracking, memory) are automatically provided by BaseAgent.

## Related Skills

- **kaizen-signatures** - Deep dive into InputField/OutputField
- **kaizen-config-patterns** - Advanced configuration patterns
- **kaizen-ux-helpers** - extract_*(), write_to_memory()
- **kaizen-agent-execution** - Advanced execution patterns

## References

- **Source**: `apps/kailash-kaizen/src/kaizen/core/base_agent.py`
- **Examples**: `apps/kailash-kaizen/examples/1-single-agent/`
- **Tests**: `apps/kailash-kaizen/tests/unit/core/test_base_agent.py`
