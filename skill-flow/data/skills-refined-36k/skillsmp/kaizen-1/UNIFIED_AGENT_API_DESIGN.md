# Unified Agent API Design - From First Principles

**Strategic Rethinking**: ONE entry point, configuration-driven behavior, progressive disclosure

**Version**: 1.0
**Date**: 2025-10-26
**Status**: DESIGN PROPOSAL

---

## Executive Summary

### The Problem

Current Kaizen architecture suffers from **decision paralysis**:

```python
# Which one do I use?!
from kaizen.agents import (
    SimpleQAAgent,           # For Q&A?
    ChainOfThoughtAgent,     # For reasoning?
    ReActAgent,              # For tool calling?
    RAGResearchAgent,        # For RAG?
    MemoryAgent,             # For memory?
    CodeGenerationAgent,     # For code?
    VisionAgent,             # For vision?
    TranscriptionAgent,      # For audio?
    MultiModalAgent,         # For everything?
    BatchProcessingAgent,    # For batch?
    HumanApprovalAgent,      # For approval?
    ResilientAgent,          # For resilience?
    StreamingChatAgent,      # For streaming?
    SelfReflectionAgent,     # For reflection?
)

# 14 agent classes! Which one do I pick?
```

### The Vision

**ONE entry point** with configuration-driven specialization:

```python
from kaizen import Agent

# Dead simple (everything just works)
agent = Agent(model="gpt-4")
result = agent.run("What is AI?")

# Specialized behavior through configuration
agent = Agent(model="gpt-4", agent_type="react")
agent = Agent(model="gpt-4", agent_type="rag")
agent = Agent(model="gpt-4", workflow="supervisor_worker")
```

### Key Principles

1. **ONE CLASS** - `Agent` is the only entry point users need
2. **CONFIGURATION-DRIVEN** - Behavior through parameters, not class hierarchy
3. **EVERYTHING ENABLED** - Memory, tools, observability work by default
4. **PROGRESSIVE DISCLOSURE** - Simple → Config → Expert
5. **100% BACKWARD COMPATIBLE** - Existing code still works

---

## Part 1: Feature Categorization Matrix

### A. Agent Feature Set (Core Behavior)

| Feature | Current Implementation | Unified Approach | Priority |
|---------|----------------------|------------------|----------|
| **Base Execution** | BaseAgent | `Agent(model="gpt-4")` | CRITICAL |
| **Simple Q&A** | SimpleQAAgent | `agent_type="simple"` | CRITICAL |
| **Chain of Thought** | ChainOfThoughtAgent | `agent_type="cot"` | HIGH |
| **ReAct (Reason+Act)** | ReActAgent | `agent_type="react"` | HIGH |
| **RAG Research** | RAGResearchAgent | `agent_type="rag"` | HIGH |
| **Autonomous** | BaseAutonomousAgent | `agent_type="autonomous"` | HIGH |
| **Vision Processing** | VisionAgent | `multimodal=["vision"]` | HIGH |
| **Audio Processing** | TranscriptionAgent | `multimodal=["audio"]` | HIGH |
| **Multi-Modal** | MultiModalAgent | `multimodal=["vision", "audio"]` | HIGH |
| **Code Generation** | CodeGenerationAgent | `agent_type="cot"` + tools | MEDIUM |
| **Memory-Enabled** | MemoryAgent | Enabled by default | MEDIUM |
| **Streaming Chat** | StreamingChatAgent | `streaming=True` | MEDIUM |
| **Batch Processing** | BatchProcessingAgent | `batch_mode=True` | LOW |
| **Human Approval** | HumanApprovalAgent | `require_approval=True` | LOW |
| **Resilient** | ResilientAgent | Enabled by default | LOW |
| **Self-Reflection** | SelfReflectionAgent | `agent_type="reflection"` | LOW |

**Analysis**: 16 agent types → 1 unified `Agent` class with configuration parameters

**Consolidation Strategy**:
- **agent_type**: Controls execution pattern (simple, cot, react, rag, autonomous, reflection)
- **multimodal**: List of modalities (vision, audio, document)
- **streaming**: Boolean for streaming mode
- **batch_mode**: Boolean for batch processing
- **require_approval**: Boolean for human-in-loop

---

### B. Tooling Feature Set (Infrastructure)

| Feature | Components | Default State | User Control | Expert Override |
|---------|-----------|--------------|--------------|-----------------|
| **Memory System** | BufferMemory, PersistentBufferMemory, SummaryMemory, VectorMemory, KnowledgeGraphMemory, SharedMemoryPool | ✅ Enabled (BufferMemory, 10 turns) | `memory_turns=20`<br>`memory_type="persistent"` | `memory=CustomMemory()` |
| **Tool Calling** | ToolRegistry, ToolExecutor, 12 builtin tools | ✅ Enabled (all builtin) | `tools=["read_file", "http_get"]`<br>`tools=False` | `tools="all"  # Enable tools via MCP
| **Observability** | HookManager, Tracing, Metrics, Logging, Audit | ✅ Enabled (auto-start) | `observability=False`<br>`tracing_only=True` | `hook_manager=CustomHooks()` |
| **Checkpointing** | StateManager, FilesystemStorage | ✅ Enabled (every 5 steps) | `checkpoint_frequency=10`<br>`checkpointing=False` | `state_manager=CustomStateManager()` |
| **Cost Tracking** | Budget monitoring, warnings | ✅ Enabled ($1.00 limit) | `budget_limit_usd=5.0`<br>`budget_limit_usd=None` | Always enabled (safety) |
| **Permission System** | ExecutionContext, approval workflows | ✅ Enabled (danger-level based) | `auto_approve_safe=True`<br>`require_approval=True` | `approval_callback=custom_func` |
| **Control Protocol** | CLITransport, WebSocketTransport | ⚠️ Opt-in | `interactive=True` | `control_protocol=CustomProtocol()` |
| **MCP Integration** | MCPClient, tool discovery | ⚠️ Opt-in | `mcp_servers=["server1"]` | `mcp_client=CustomClient()` |
| **Google A2A** | Capability cards, semantic matching | ✅ Auto-generated | N/A (always on) | N/A |

**Analysis**: 9 infrastructure features

**Default Philosophy**:
- **Everything production-ready is ON by default** (memory, tools, observability, checkpointing, cost tracking)
- **Experimental features are OPT-IN** (control protocol, MCP)
- **Users disable what they don't need**, not enable what they do

---

### C. UX Feature Set (Developer Experience)

| Feature | Implementation | Default State | User Control |
|---------|---------------|--------------|--------------|
| **Rich Console Output** | Startup banner, progress bars, feature summary | ✅ Enabled | `rich_output=False`<br>`verbosity="quiet"` |
| **Streaming Responses** | Token-by-token output | ⚠️ Opt-in | `streaming=True` |
| **Cost Warnings** | Budget alerts at 75%, 90%, 100% | ✅ Enabled | `budget_warnings=False` |
| **Error Handling** | Automatic retries, fallback strategies | ✅ Enabled | `retry_count=3`<br>`fallback_strategy="none"` |
| **Result Extraction** | `extract_list()`, `extract_dict()`, `extract_float()`, `extract_str()` | ✅ Enabled | N/A (always available) |
| **Memory Helpers** | `write_to_memory()` | ✅ Enabled | N/A (always available) |
| **Config Auto-Conversion** | Domain config → BaseAgentConfig | ✅ Enabled | N/A (transparent) |
| **Performance Metrics** | Execution time, token usage, cost | ✅ Enabled | `metrics=False` |
| **Progress Reporting** | Step-by-step updates | ✅ Enabled (verbose) | `progress_reporting=False` |

**Analysis**: 9 UX features

**Philosophy**:
- **Make the right thing easy** - Rich output and helpful defaults
- **Don't clutter code** - Auto-conversion, extraction helpers
- **Safety by default** - Cost warnings, error handling

---

## Part 2: Layered API Design

### Layer 1: Zero-Config Defaults (99% of users)

**Mental Model**: "Just create an agent and go"

```python
from kaizen import Agent

# DEAD SIMPLE - Everything just works
agent = Agent(model="gpt-4")
result = agent.run("Explain quantum computing")

print(result['answer'])
```

**What happens automatically**:

```
✨ Kaizen Agent Starting...
   Model: gpt-4 (openai)
   Memory: Enabled (10 turns, buffer)
   Tools: Enabled (12 builtin tools)
   Observability: Enabled (tracing, metrics, logging)
   Checkpointing: Enabled (every 5 steps)
   Budget: $1.00 USD limit

⚙️  Executing...
✅ Complete (2.3s, 450 tokens, $0.008)
```

**Features enabled by default**:
- ✅ Memory: 10 turns, buffer backend
- ✅ Tools: All 12 builtin tools registered
- ✅ Observability: Jaeger tracing, Prometheus metrics, structured logging
- ✅ Checkpointing: Every 5 steps, filesystem storage
- ✅ Cost tracking: $1.00 budget limit with warnings
- ✅ Rich output: Startup banner, progress updates, performance metrics
- ✅ Error handling: 3 automatic retries with exponential backoff
- ✅ Google A2A: Automatic capability card generation

---

### Layer 2: Configuration Layer (Power Users)

**Mental Model**: "Configure behavior through parameters"

```python
from kaizen import Agent

# CONFIGURE BEHAVIOR
agent = Agent(
    model="gpt-4",
    agent_type="react",           # ReAct pattern (reasoning + acting)

    # Memory settings
    memory_turns=20,              # 20 conversation turns
    memory_type="persistent",     # SQLite persistence

    # Tool settings
    tools=["read_file", "http_get", "bash_command"],  # Subset

    # Budget & cost
    budget_limit_usd=5.0,         # $5 budget

    # UX settings
    rich_output=True,             # Fancy console output
    verbosity="verbose",          # Show everything

    # Execution settings
    max_cycles=10,                # Max 10 reasoning cycles
    temperature=0.7,              # Creativity level
)

result = agent.run("Research AI trends and create a report")
```

**Configuration Categories**:

#### Agent Behavior
- `agent_type`: "simple" | "cot" | "react" | "rag" | "autonomous" | "reflection"
- `workflow`: "supervisor_worker" | "consensus" | "debate" | "sequential" | "handoff"
- `multimodal`: ["vision"] | ["audio"] | ["vision", "audio", "document"]
- `max_cycles`: int (for iterative agents)
- `temperature`: float (LLM creativity)

#### Memory Configuration
- `memory_turns`: int (conversation history length)
- `memory_type`: "buffer" | "persistent" | "summary" | "vector" | "knowledge_graph"
- `memory_backend`: "file" | "sqlite" | "postgresql"
- `shared_memory`: SharedMemoryPool (for multi-agent)

#### Tool Configuration
- `tools`: "all" | List[str] | False
- `auto_approve_safe`: bool (auto-approve SAFE tools)
- `require_approval`: bool (approve all tools)

#### Infrastructure
- `budget_limit_usd`: float | None
- `checkpoint_frequency`: int (steps between checkpoints)
- `observability`: bool (enable/disable all)
- `tracing_only`: bool (only tracing, no metrics/logs)

#### UX Settings
- `rich_output`: bool
- `verbosity`: "quiet" | "normal" | "verbose"
- `streaming`: bool
- `progress_reporting`: bool

---

### Layer 3: Expert Override (1% of users)

**Mental Model**: "Replace components with custom implementations"

```python
from kaizen import Agent
from my_custom import (
    CustomMemorySystem,
    CustomToolRegistry,
    CustomHookManager,
    CustomStateManager,
)

# EXPERT CUSTOMIZATION
agent = Agent(
    model="gpt-4",
    agent_type="react",

    # Custom memory implementation
    memory=CustomMemorySystem(
        backend="redis",
        cluster_nodes=["node1", "node2", "node3"],
        replication_factor=3
    ),

    # Custom tool registry
    tools="all"  # Enable tools via MCP
        discovery_service="consul",
        dynamic_loading=True
    ),

    # Custom observability
    hook_manager=CustomHookManager(
        exporters=["datadog", "newrelic"],
        sampling_rate=0.1
    ),

    # Custom checkpointing
    state_manager=CustomStateManager(
        storage_backend="s3",
        bucket="agent-checkpoints",
        compression="lz4"
    ),

    # Custom control protocol
    control_protocol=CustomControlProtocol(
        transport="grpc",
        auth="oauth2"
    ),
)
```

**Expert Override Points**:
- `memory`: BaseMemory → Custom memory implementation
- `tool_registry`: ToolRegistry → Custom tool system
- `hook_manager`: HookManager → Custom observability
- `state_manager`: StateManager → Custom checkpointing
- `control_protocol`: ControlProtocol → Custom interaction
- `mcp_client`: MCPClient → Custom MCP integration
- `approval_callback`: Callable → Custom approval logic
- `error_handler`: Callable → Custom error handling

---

## Part 3: Agent Type System (Configuration Presets)

### Agent Type Mapping

Instead of 16 agent classes, ONE `Agent` with type parameter:

```python
AGENT_TYPE_PRESETS = {
    "simple": {
        "description": "Simple Q&A, single inference",
        "strategy": "single_shot",
        "max_cycles": 1,
        "tools_enabled": False,
        "memory_type": "buffer",
        "use_case": "Basic Q&A, fact retrieval, simple transformations"
    },

    "cot": {
        "description": "Step-by-step reasoning (Chain of Thought)",
        "strategy": "single_shot",
        "max_cycles": 1,
        "tools_enabled": False,
        "memory_type": "buffer",
        "reasoning_steps": True,
        "prompt_modifier": "Think step by step:",
        "use_case": "Math problems, logic puzzles, complex reasoning"
    },

    "react": {
        "description": "Reason + Act cycles with tool calling",
        "strategy": "multi_cycle",
        "max_cycles": 10,
        "tools_enabled": True,
        "memory_type": "persistent",
        "convergence": "satisfaction",
        "use_case": "Research, data gathering, API interactions"
    },

    "rag": {
        "description": "Retrieval-augmented generation",
        "strategy": "single_shot",
        "max_cycles": 1,
        "tools_enabled": True,
        "required_tools": ["vector_search"],
        "memory_type": "vector",
        "use_case": "Document Q&A, knowledge base queries"
    },

    "autonomous": {
        "description": "Long-running autonomous agent",
        "strategy": "multi_cycle",
        "max_cycles": 100,
        "tools_enabled": True,
        "memory_type": "persistent",
        "checkpointing_required": True,
        "convergence": "goal_achieved",
        "use_case": "Complex tasks, multi-step workflows, extended operations"
    },

    "reflection": {
        "description": "Self-reflection and improvement",
        "strategy": "multi_cycle",
        "max_cycles": 5,
        "tools_enabled": False,
        "memory_type": "persistent",
        "reflection_enabled": True,
        "use_case": "Self-improvement, error correction, quality refinement"
    },
}
```

### Usage Examples

```python
# Simple Q&A (single inference)
agent = Agent(model="gpt-4", agent_type="simple")
result = agent.run("What is the capital of France?")

# Chain of Thought (step-by-step reasoning)
agent = Agent(model="gpt-4", agent_type="cot")
result = agent.run("Solve: If a train leaves at 2pm going 60mph...")

# ReAct (reasoning + action with tools)
agent = Agent(model="gpt-4", agent_type="react")
result = agent.run("Research latest AI papers and summarize findings")

# RAG (retrieval-augmented generation)
agent = Agent(model="gpt-4", agent_type="rag")
result = agent.run("What does our documentation say about error handling?")

# Autonomous (long-running with checkpoints)
agent = Agent(model="gpt-4", agent_type="autonomous", max_cycles=50)
result = agent.run("Build a complete data pipeline from API to dashboard")

# Self-Reflection (iterative improvement)
agent = Agent(model="gpt-4", agent_type="reflection")
result = agent.run("Write a blog post and improve it 3 times")
```

---

## Part 4: Workflow Integration (Agentic Patterns)

### Current State (BAD)

```python
# Separate classes for workflows
from kaizen.agents.coordination import (
    SupervisorWorkerPattern,
    ConsensusPattern,
    DebatePattern,
    SequentialPattern,
    HandoffPattern,
)

# Complex setup
pattern = SupervisorWorkerPattern(
    supervisor=supervisor_agent,
    workers=[worker1, worker2, worker3],
    coordinator=coordinator,
    shared_pool=pool
)
```

### Proposed State (GOOD)

```python
# Workflow as configuration
from kaizen import Agent

# Create workers
researcher = Agent(model="gpt-4", agent_type="react", agent_id="researcher")
analyst = Agent(model="gpt-4", agent_type="cot", agent_id="analyst")
writer = Agent(model="gpt-4", agent_type="simple", agent_id="writer")

# Create supervisor with workflow
supervisor = Agent(
    model="gpt-4",
    agent_type="react",
    workflow="supervisor_worker",
    workers=[researcher, analyst, writer],
    workflow_config={
        "selection_strategy": "semantic",  # Google A2A semantic matching
        "parallel_execution": True,
        "require_consensus": False
    }
)

# Execute workflow
result = supervisor.run("Research AI trends, analyze data, write report")
```

### Workflow Types

```python
WORKFLOW_PRESETS = {
    "supervisor_worker": {
        "description": "Supervisor delegates tasks to specialized workers",
        "required_params": ["workers"],
        "optional_params": ["selection_strategy", "parallel_execution"],
        "pattern_class": "SupervisorWorkerPattern",
        "use_case": "Complex tasks requiring specialization"
    },

    "consensus": {
        "description": "Multiple agents reach consensus on decision",
        "required_params": ["agents"],
        "optional_params": ["consensus_threshold", "max_rounds"],
        "pattern_class": "ConsensusPattern",
        "use_case": "Critical decisions requiring agreement"
    },

    "debate": {
        "description": "Adversarial agents debate to best solution",
        "required_params": ["agents"],
        "optional_params": ["max_rounds", "judge_agent"],
        "pattern_class": "DebatePattern",
        "use_case": "Exploring multiple perspectives"
    },

    "sequential": {
        "description": "Sequential pipeline of specialized agents",
        "required_params": ["agents"],
        "optional_params": ["allow_backtrack"],
        "pattern_class": "SequentialPattern",
        "use_case": "Multi-stage processing pipelines"
    },

    "handoff": {
        "description": "Dynamic handoff between agents",
        "required_params": ["agents"],
        "optional_params": ["handoff_criteria"],
        "pattern_class": "HandoffPattern",
        "use_case": "Adaptive task routing"
    },
}
```

---

## Part 5: Smart Defaults Matrix

### Decision Framework: What's ON by default?

| Category | Feature | Default State | Reasoning |
|----------|---------|--------------|-----------|
| **SAFETY** | Cost tracking ($1 limit) | ✅ ON | Prevent accidental overspending |
| **SAFETY** | Error handling (3 retries) | ✅ ON | Resilience against transient failures |
| **SAFETY** | Tool approval (danger-level) | ✅ ON | Prevent destructive operations |
| **PRODUCTIVITY** | Memory (10 turns, buffer) | ✅ ON | Conversations require context |
| **PRODUCTIVITY** | Tools (12 builtin) | ✅ ON | Agents need capabilities |
| **PRODUCTIVITY** | Result extraction helpers | ✅ ON | Defensive parsing prevents errors |
| **OBSERVABILITY** | Tracing | ✅ ON | Debug issues in production |
| **OBSERVABILITY** | Metrics | ✅ ON | Monitor performance |
| **OBSERVABILITY** | Logging | ✅ ON | Audit trails |
| **RESILIENCE** | Checkpointing (every 5 steps) | ✅ ON | Resume from failures |
| **RESILIENCE** | State persistence | ✅ ON | Long-running agents |
| **UX** | Rich console output | ✅ ON | Better developer experience |
| **UX** | Progress reporting | ✅ ON | Visibility into execution |
| **UX** | Cost warnings (75%, 90%) | ✅ ON | Early alerts |
| **INTEGRATION** | Google A2A capability cards | ✅ ON | Multi-agent coordination |
| **EXPERIMENTAL** | Control protocol | ⚠️ OFF | Opt-in for interactive |
| **EXPERIMENTAL** | MCP integration | ⚠️ OFF | Opt-in for MCP servers |
| **EXPERIMENTAL** | Streaming | ⚠️ OFF | Opt-in for real-time |
| **OPTIONAL** | Batch mode | ⚠️ OFF | Specialized use case |
| **OPTIONAL** | Human approval (all tools) | ⚠️ OFF | Too restrictive for default |

### Philosophy

1. **ON by default** if it provides:
   - Safety (cost limits, error handling)
   - Productivity (memory, tools, helpers)
   - Observability (debugging, monitoring)
   - Resilience (checkpoints, retries)
   - Better UX (rich output, progress)

2. **OFF by default** if it:
   - Is experimental (control protocol, MCP)
   - Changes behavior significantly (streaming)
   - Is a specialized mode (batch, approval-all)
   - Requires external setup (MCP servers)

3. **User can disable** anything:
   ```python
   # Minimal agent (disable everything optional)
   agent = Agent(
       model="gpt-4",
       memory=False,
       tools=False,
       observability=False,
       checkpointing=False,
       rich_output=False,
       budget_limit_usd=None  # No budget limit
   )
   ```

---

## Part 6: Implementation Architecture

### Agent Class Design

```python
from typing import Literal, Optional, List, Dict, Any, Callable, Union
from dataclasses import dataclass
from kaizen.core.base_agent import BaseAgent
from kaizen.signatures import Signature
from kaizen.memory import BaseMemory, BufferMemory
# Tools auto-configured via MCP
from kaizen.core.autonomy.hooks import HookManager
from kaizen.core.autonomy.state.manager import StateManager

class Agent:
    """
    Universal agent with everything enabled by default.

    Replaces:
    - BaseAgent (low-level foundation - still used internally)
    - SimpleQAAgent, ReActAgent, ChainOfThoughtAgent, etc. (specialized classes)

    One entry point, configuration-driven behavior.

    Examples:
        # Dead simple
        >>> agent = Agent(model="gpt-4")
        >>> result = agent.run("What is AI?")

        # Configured behavior
        >>> agent = Agent(model="gpt-4", agent_type="react", memory_turns=20)

        # Expert customization
        >>> agent = Agent(model="gpt-4", memory=CustomMemory())
    """

    def __init__(
        self,
        # REQUIRED
        model: str,

        # Layer 1: Smart Defaults (most users stop here)
        provider: str = "openai",
        agent_id: Optional[str] = None,

        # Layer 2: Behavioral Configuration
        agent_type: Literal["simple", "cot", "react", "rag", "autonomous", "reflection"] = "simple",
        workflow: Optional[Literal["supervisor_worker", "consensus", "debate", "sequential", "handoff"]] = None,
        multimodal: Optional[List[Literal["vision", "audio", "document"]]] = None,

        # Memory configuration
        memory_turns: int = 10,
        memory_type: Literal["buffer", "persistent", "summary", "vector", "knowledge_graph"] = "buffer",
        memory_backend: Literal["file", "sqlite", "postgresql"] = "file",
        shared_memory: Optional['SharedMemoryPool'] = None,

        # Tool configuration
        tools: Union[Literal["all"], List[str], Literal[False]] = "all",
        auto_approve_safe: bool = True,
        require_approval: bool = False,

        # Execution configuration
        max_cycles: int = 10,
        temperature: float = 0.7,

        # Infrastructure settings
        budget_limit_usd: Optional[float] = 1.0,
        checkpoint_frequency: int = 5,
        checkpointing: bool = True,
        observability: bool = True,
        tracing_only: bool = False,

        # UX settings
        rich_output: bool = True,
        verbosity: Literal["quiet", "normal", "verbose"] = "normal",
        streaming: bool = False,
        progress_reporting: bool = True,

        # Workflow configuration (if workflow is set)
        workers: Optional[List['Agent']] = None,
        workflow_config: Optional[Dict[str, Any]] = None,

        # Layer 3: Expert Overrides (optional)
        signature: Optional[Signature] = None,
        memory: Optional[BaseMemory] = None,
        tool_registry: Optional[ToolRegistry] = None,
        hook_manager: Optional[HookManager] = None,
        state_manager: Optional[StateManager] = None,
        control_protocol: Optional['ControlProtocol'] = None,
        mcp_client: Optional['MCPClient'] = None,
        approval_callback: Optional[Callable] = None,
        error_handler: Optional[Callable] = None,

        **kwargs
    ):
        """
        Initialize Agent with smart defaults and optional customization.

        Args:
            model: LLM model name (e.g., "gpt-4", "gpt-3.5-turbo")
            provider: LLM provider ("openai", "anthropic", "ollama")
            agent_id: Unique identifier (auto-generated if not provided)

            agent_type: Execution pattern preset
            workflow: Multi-agent coordination pattern
            multimodal: List of modalities to enable

            memory_turns: Conversation history length
            memory_type: Memory implementation type
            memory_backend: Storage backend
            shared_memory: Shared memory pool for multi-agent

            tools: Tool configuration (all, subset, or disabled)
            auto_approve_safe: Auto-approve SAFE danger level tools
            require_approval: Require approval for all tools

            max_cycles: Maximum reasoning/action cycles
            temperature: LLM temperature (0.0-1.0)

            budget_limit_usd: Cost budget limit (None = unlimited)
            checkpoint_frequency: Steps between checkpoints
            checkpointing: Enable automatic checkpointing
            observability: Enable tracing/metrics/logging
            tracing_only: Only enable tracing (not metrics/logging)

            rich_output: Enable rich console output
            verbosity: Output verbosity level
            streaming: Enable token-by-token streaming
            progress_reporting: Show progress updates

            workers: Worker agents for workflow patterns
            workflow_config: Workflow-specific configuration

            signature: Custom signature (expert override)
            memory: Custom memory implementation (expert override)
            tool_registry: Custom tool registry (expert override)
            hook_manager: Custom observability (expert override)
            state_manager: Custom checkpointing (expert override)
            control_protocol: Custom interaction protocol (expert override)
            mcp_client: Custom MCP client (expert override)
            approval_callback: Custom approval logic (expert override)
            error_handler: Custom error handling (expert override)
        """
        self.model = model
        self.provider = provider
        self.agent_id = agent_id or self._generate_agent_id()

        # Store configuration
        self._agent_type = agent_type
        self._workflow = workflow
        self._multimodal = multimodal or []
        self._config_params = {
            "memory_turns": memory_turns,
            "memory_type": memory_type,
            "memory_backend": memory_backend,
            "tools": tools,
            "max_cycles": max_cycles,
            "temperature": temperature,
            "budget_limit_usd": budget_limit_usd,
            "checkpoint_frequency": checkpoint_frequency,
            "checkpointing": checkpointing,
            "observability": observability,
            "rich_output": rich_output,
            "verbosity": verbosity,
            "streaming": streaming,
        }

        # Initialize with smart defaults
        self._setup_smart_defaults()

        # Apply agent type behavior
        self._apply_agent_type(agent_type)

        # Apply multimodal configuration
        if multimodal:
            self._apply_multimodal(multimodal)

        # Apply workflow pattern
        if workflow:
            self._apply_workflow(workflow, workers, workflow_config)

        # Setup infrastructure (or use expert overrides)
        self._setup_infrastructure(
            memory=memory,
            tools="all"  # Enable tools via MCP
            hook_manager=hook_manager,
            state_manager=state_manager,
            control_protocol=control_protocol,
            mcp_client=mcp_client,
        )

        # Create underlying BaseAgent
        self._base_agent = self._create_base_agent(
            signature=signature,
            approval_callback=approval_callback,
            error_handler=error_handler,
            **kwargs
        )

        # Show rich startup banner (if enabled)
        if rich_output and verbosity != "quiet":
            self._show_startup_banner()

    def _setup_smart_defaults(self):
        """Setup smart defaults for all components."""
        # Memory: 10 turns, buffer, file backend
        self._memory_config = {
            "type": self._config_params["memory_type"],
            "turns": self._config_params["memory_turns"],
            "backend": self._config_params["memory_backend"],
        }

        # Tools: All 12 builtin tools
        self._tools_config = {
            "enabled": self._config_params["tools"] != False,
            "tools": self._config_params["tools"],
            "auto_approve_safe": True,
        }

        # Observability: Tracing, metrics, logging
        self._observability_config = {
            "enabled": self._config_params["observability"],
            "tracing": True,
            "metrics": True,
            "logging": True,
        }

        # Checkpointing: Every 5 steps, filesystem
        self._checkpoint_config = {
            "enabled": self._config_params["checkpointing"],
            "frequency": self._config_params["checkpoint_frequency"],
            "storage": "filesystem",
        }

        # Cost tracking: $1.00 limit
        self._budget_config = {
            "limit_usd": self._config_params["budget_limit_usd"],
            "warn_at": 0.75,  # Warn at 75%
            "error_at": 1.0,  # Error at 100%
        }

    def _apply_agent_type(self, agent_type: str):
        """Apply agent type preset configuration."""
        preset = AGENT_TYPE_PRESETS.get(agent_type)
        if not preset:
            raise ValueError(f"Unknown agent_type: {agent_type}")

        # Apply preset to configuration
        self._strategy = preset["strategy"]
        self._max_cycles = preset.get("max_cycles", self._config_params["max_cycles"])

        # Override tool configuration if preset disables tools
        if not preset.get("tools_enabled", True):
            self._tools_config["enabled"] = False

        # Apply preset-specific settings
        if preset.get("reasoning_steps"):
            self._reasoning_enabled = True

        if preset.get("convergence"):
            self._convergence_strategy = preset["convergence"]

        if preset.get("required_tools"):
            self._required_tools = preset["required_tools"]

    def _apply_multimodal(self, modalities: List[str]):
        """Apply multimodal configuration."""
        for modality in modalities:
            if modality == "vision":
                self._vision_enabled = True
            elif modality == "audio":
                self._audio_enabled = True
            elif modality == "document":
                self._document_enabled = True

    def _apply_workflow(self, workflow: str, workers: List['Agent'], config: Dict):
        """Apply workflow pattern configuration."""
        workflow_preset = WORKFLOW_PRESETS.get(workflow)
        if not workflow_preset:
            raise ValueError(f"Unknown workflow: {workflow}")

        # Validate required parameters
        if "workers" in workflow_preset["required_params"] and not workers:
            raise ValueError(f"Workflow '{workflow}' requires 'workers' parameter")

        # Create workflow pattern instance
        self._workflow_pattern = self._create_workflow_pattern(
            workflow, workers, config
        )

    def _setup_infrastructure(
        self,
        memory=None,
        tools="all"  # Enable tools via MCP
        hook_manager=None,
        state_manager=None,
        control_protocol=None,
        mcp_client=None,
    ):
        """Setup infrastructure components (smart defaults or expert overrides)."""
        # Memory
        if memory:
            self._memory = memory  # Expert override
        else:
            self._memory = self._create_default_memory()  # Smart default

        # Tools
        if tool_registry:
            self._tool_registry = tool_registry  # Expert override
        else:
            self._tool_registry = self._create_default_tool_registry()  # Smart default

        # Observability
        if hook_manager:
            self._hook_manager = hook_manager  # Expert override
        else:
            self._hook_manager = self._create_default_hook_manager()  # Smart default

        # Checkpointing
        if state_manager:
            self._state_manager = state_manager  # Expert override
        else:
            self._state_manager = self._create_default_state_manager()  # Smart default

        # Control protocol (opt-in)
        self._control_protocol = control_protocol

        # MCP client (opt-in)
        self._mcp_client = mcp_client

    def run(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Execute agent with given inputs.

        Delegates to underlying BaseAgent.run() but adds:
        - Rich progress reporting (if enabled)
        - Cost tracking and warnings
        - Performance metrics
        - Error handling with retries

        Returns:
            Dict with execution results
        """
        # Show progress (if enabled)
        if self._config_params["progress_reporting"]:
            self._show_progress_start()

        # Execute with error handling
        try:
            result = self._base_agent.run(*args, **kwargs)

            # Check budget
            if self._budget_config["limit_usd"]:
                self._check_budget(result)

            # Show completion (if rich output)
            if self._config_params["rich_output"]:
                self._show_completion(result)

            return result

        except Exception as e:
            # Handle error with retries
            return self._handle_execution_error(e, *args, **kwargs)

    async def run_async(self, *args, **kwargs) -> Dict[str, Any]:
        """Async version of run()."""
        # Similar to run() but async
        pass

    # ... additional helper methods ...

    def _show_startup_banner(self):
        """Show rich startup banner."""
        print("✨ Kaizen Agent Starting...")
        print(f"   Model: {self.model} ({self.provider})")
        print(f"   Type: {self._agent_type}")

        if self._memory_config["type"] != False:
            print(f"   Memory: Enabled ({self._memory_config['turns']} turns, {self._memory_config['type']})")

        if self._tools_config["enabled"]:
            tool_count = len(self._tool_registry.list_tools()) if self._tool_registry else 12
            print(f"   Tools: Enabled ({tool_count} tools)")

        if self._observability_config["enabled"]:
            features = []
            if self._observability_config["tracing"]:
                features.append("tracing")
            if self._observability_config["metrics"]:
                features.append("metrics")
            if self._observability_config["logging"]:
                features.append("logging")
            print(f"   Observability: Enabled ({', '.join(features)})")

        if self._checkpoint_config["enabled"]:
            print(f"   Checkpointing: Enabled (every {self._checkpoint_config['frequency']} steps)")

        if self._budget_config["limit_usd"]:
            print(f"   Budget: ${self._budget_config['limit_usd']:.2f} USD limit")

        print()  # Blank line

# Agent type presets (defined earlier)
AGENT_TYPE_PRESETS = {
    # ... (from Part 3)
}

# Workflow presets (defined earlier)
WORKFLOW_PRESETS = {
    # ... (from Part 4)
}
```

---

## Part 7: Migration Strategy

### Backward Compatibility Plan

**CRITICAL**: Existing code must continue to work

```python
# EXISTING CODE (still works)
from kaizen.agents import SimpleQAAgent, ReActAgent

agent = SimpleQAAgent(llm_provider="openai", model="gpt-4")
result = agent.ask("What is AI?")  # ✅ Still works

# NEW CODE (recommended)
from kaizen import Agent

agent = Agent(model="gpt-4", agent_type="simple")
result = agent.run("What is AI?")  # ✅ New way
```

### Implementation Phases

#### Phase 1: Agent Class Creation (Week 1-2)
- Implement `Agent` class with smart defaults
- Add agent_type presets
- Add workflow integration
- Add infrastructure setup
- 100% test coverage

**Deliverable**: Working `Agent` class, all tests passing

#### Phase 2: Documentation & Examples (Week 3)
- Update documentation to showcase `Agent` class
- Create migration guide (before/after examples)
- Add 20+ examples using `Agent` class
- Update quickstart to use `Agent`

**Deliverable**: Complete documentation, all examples work

#### Phase 3: Soft Deprecation (Week 4)
- Mark specialized classes as "legacy" in docs
- Add deprecation warnings (but keep working)
- Steer new users to `Agent` class
- Provide migration script

**Deliverable**: Migration path documented, warnings in place

#### Phase 4: Long-Term Support (Months 2-6)
- Maintain both APIs in parallel
- Specialized classes call `Agent` internally (refactor)
- Reduce duplication progressively
- Monitor adoption metrics

**Deliverable**: Dual API support, reduced maintenance burden

#### Phase 5: Full Migration (Month 7+)
- Optional: Remove specialized classes (breaking change)
- Or: Keep as thin wrappers forever (no breaking change)
- Decision based on user feedback

**Recommendation**: Keep specialized classes as thin wrappers indefinitely (no breaking changes)

---

## Part 8: Code Examples (Before/After)

### Example 1: Simple Q&A

**BEFORE (Current)**:
```python
from kaizen.agents import SimpleQAAgent
from dataclasses import dataclass

@dataclass
class QAConfig:
    llm_provider: str = "openai"
    model: str = "gpt-4"
    temperature: float = 0.7

config = QAConfig()
agent = SimpleQAAgent(
    llm_provider=config.llm_provider,
    model=config.model,
    temperature=config.temperature
)

result = agent.ask("What is AI?")
answer = result.get("answer", "No answer")
print(answer)
```

**AFTER (Unified)**:
```python
from kaizen import Agent

# Dead simple
agent = Agent(model="gpt-4")
result = agent.run("What is AI?")
print(result['answer'])

# Or with configuration
agent = Agent(model="gpt-4", temperature=0.7)
```

**Lines of code**: 18 → 4 (78% reduction)

---

### Example 2: ReAct with Tools

**BEFORE (Current)**:
```python
from kaizen.agents import ReActAgent
# Tools auto-configured via MCP

from dataclasses import dataclass

@dataclass
class ReActConfig:
    llm_provider: str = "openai"
    model: str = "gpt-4"
    max_cycles: int = 10
    temperature: float = 0.7

# Setup tools

# 12 builtin tools enabled via MCP

# Create agent
config = ReActConfig()
agent = ReActAgent(
    llm_provider=config.llm_provider,
    model=config.model,
    max_cycles=config.max_cycles,
    temperature=config.temperature,
    tools="all"  # Enable 12 builtin tools via MCP
)

# Execute
result = agent.execute("Research AI trends and create report")
answer = result.get("answer", "")
print(answer)
```

**AFTER (Unified)**:
```python
from kaizen import Agent

# Everything enabled by default
agent = Agent(model="gpt-4", agent_type="react")
result = agent.run("Research AI trends and create report")
print(result['answer'])
```

**Lines of code**: 30 → 4 (87% reduction)

---

### Example 3: Multi-Agent Workflow

**BEFORE (Current)**:
```python
from kaizen.agents import SimpleQAAgent
from kaizen.agents.coordination import SupervisorWorkerPattern
from kaizen.memory import SharedMemoryPool

# Create shared memory
pool = SharedMemoryPool()

# Create workers
researcher = SimpleQAAgent(
    llm_provider="openai",
    model="gpt-4",
    shared_memory=pool,
    agent_id="researcher"
)

analyst = SimpleQAAgent(
    llm_provider="openai",
    model="gpt-4",
    shared_memory=pool,
    agent_id="analyst"
)

writer = SimpleQAAgent(
    llm_provider="openai",
    model="gpt-4",
    shared_memory=pool,
    agent_id="writer"
)

# Create supervisor
supervisor = SimpleQAAgent(
    llm_provider="openai",
    model="gpt-4",
    agent_id="supervisor"
)

# Create pattern
pattern = SupervisorWorkerPattern(
    supervisor=supervisor,
    workers=[researcher, analyst, writer],
    coordinator=None,
    shared_pool=pool
)

# Execute
result = pattern.execute("Research, analyze, and write report on AI")
```

**AFTER (Unified)**:
```python
from kaizen import Agent

# Create workers
researcher = Agent(model="gpt-4", agent_type="react", agent_id="researcher")
analyst = Agent(model="gpt-4", agent_type="cot", agent_id="analyst")
writer = Agent(model="gpt-4", agent_type="simple", agent_id="writer")

# Create supervisor with workflow
supervisor = Agent(
    model="gpt-4",
    workflow="supervisor_worker",
    workers=[researcher, analyst, writer]
)

# Execute
result = supervisor.run("Research, analyze, and write report on AI")
```

**Lines of code**: 47 → 11 (77% reduction)

---

### Example 4: Vision + Audio Multi-Modal

**BEFORE (Current)**:
```python
from kaizen.agents import VisionAgent, TranscriptionAgent, MultiModalAgent
from kaizen.agents.multi_modal import VisionAgentConfig, TranscriptionAgentConfig

# Create vision agent
vision_config = VisionAgentConfig(
    llm_provider="openai",
    model="gpt-4-vision",
    vision_provider="openai_vision"
)
vision_agent = VisionAgent(config=vision_config)

# Create audio agent
audio_config = TranscriptionAgentConfig(
    llm_provider="openai",
    audio_provider="whisper"
)
audio_agent = TranscriptionAgent(config=audio_config)

# Create multi-modal orchestrator
multi_modal = MultiModalAgent(
    vision_agent=vision_agent,
    transcription_agent=audio_agent,
    llm_provider="openai",
    model="gpt-4"
)

# Process
result = multi_modal.process(
    image_path="video_frame.png",
    audio_path="audio.mp3",
    question="What is happening in this video?"
)
```

**AFTER (Unified)**:
```python
from kaizen import Agent

# Single agent with multimodal capabilities
agent = Agent(
    model="gpt-4",
    multimodal=["vision", "audio"]
)

# Process
result = agent.run(
    image="video_frame.png",
    audio="audio.mp3",
    question="What is happening in this video?"
)
```

**Lines of code**: 33 → 9 (73% reduction)

---

### Example 5: All 3 Layers Demonstrated

```python
from kaizen import Agent

# ====================================
# LAYER 1: Zero-Config (Dead Simple)
# ====================================

agent = Agent(model="gpt-4")
result = agent.run("What is machine learning?")

# What you get automatically:
# - Memory: 10 turns, buffer
# - Tools: 12 builtin tools
# - Observability: Tracing, metrics, logging
# - Checkpointing: Every 5 steps
# - Cost tracking: $1.00 limit
# - Rich output: Startup banner, progress, metrics

# ====================================
# LAYER 2: Configuration (Power User)
# ====================================

agent = Agent(
    model="gpt-4",
    agent_type="react",           # ReAct pattern
    memory_turns=20,              # 20 conversation turns
    memory_type="persistent",     # SQLite persistence
    tools=["read_file", "http_get"],  # Subset of tools
    budget_limit_usd=5.0,         # $5 budget
    max_cycles=15,                # 15 reasoning cycles
    rich_output=True,             # Fancy output
    verbosity="verbose"           # Show everything
)

result = agent.run("Research latest AI papers and summarize")

# ====================================
# LAYER 3: Expert Override
# ====================================

from my_custom import (
    RedisMemorySystem,
    ConsulToolRegistry,
    DatadogHookManager,
    S3StateManager
)

agent = Agent(
    model="gpt-4",
    agent_type="autonomous",

    # Expert overrides
    memory=RedisMemorySystem(
        cluster=["node1", "node2"],
        replication_factor=3
    ),

    tools="all"  # Enable tools via MCP
        service_discovery="consul.internal",
        dynamic_loading=True
    ),

    hook_manager=DatadogHookManager(
        api_key=os.getenv("DD_API_KEY"),
        sampling_rate=0.1
    ),

    state_manager=S3StateManager(
        bucket="agent-checkpoints",
        region="us-west-2",
        compression="lz4"
    )
)

result = agent.run("Build complete data pipeline")
```

---

## Part 9: Implementation Roadmap

### Week 1-2: Core Implementation

**Tasks**:
1. Create `Agent` class in `src/kaizen/core/agents.py`
2. Implement smart defaults system
3. Implement agent_type preset application
4. Implement workflow integration
5. Implement multimodal configuration
6. Write 100+ unit tests (Tier 1)
7. Write 20+ integration tests (Tier 2)

**Deliverables**:
- Working `Agent` class
- 100% test coverage
- All presets working

### Week 3: Documentation

**Tasks**:
1. Update README with `Agent` class
2. Create migration guide (before/after)
3. Update all quickstart docs
4. Create 20+ examples using `Agent`
5. Update API reference
6. Create decision tree (when to use what)

**Deliverables**:
- Complete documentation
- Migration guide
- 20+ working examples

### Week 4: Integration

**Tasks**:
1. Export `Agent` from `kaizen/__init__.py`
2. Add deprecation warnings to specialized classes
3. Update specialized classes to call `Agent` internally
4. Create migration script (automated refactoring)
5. Update all internal examples
6. Performance testing and optimization

**Deliverables**:
- `Agent` exported and available
- Deprecation warnings in place
- Migration tooling ready

### Month 2-6: Adoption

**Tasks**:
1. Monitor user adoption
2. Collect feedback
3. Iterate on API based on feedback
4. Progressive documentation updates
5. Community support and examples
6. Performance optimization

**Deliverables**:
- High adoption rate
- Positive feedback
- Optimized performance

---

## Part 10: Success Criteria

### Quantitative Metrics

1. **Code Reduction**: 70%+ less boilerplate in common use cases
2. **Import Simplification**: 1 import vs 5-10 imports
3. **Time to First Agent**: <2 minutes (vs 10+ minutes)
4. **Test Coverage**: 100% for `Agent` class
5. **Performance**: <100ms initialization overhead
6. **Adoption**: 80%+ of new examples use `Agent`

### Qualitative Metrics

1. **Developer Feedback**: "This is the simplest AI framework I've used"
2. **Documentation Clarity**: "I understood immediately how to use it"
3. **Decision Speed**: "I didn't have to think about which class to use"
4. **Feature Discovery**: "I discovered features I didn't know existed"
5. **Migration Experience**: "Migration was painless"

### User Testimonials (Target)

> "Before: Spent 30 minutes figuring out which agent class to use. After: 2 lines of code and it just worked." - New User

> "I love that everything is enabled by default. I can disable what I don't need instead of hunting for what to enable." - Power User

> "The 3-layer API is brilliant. I started with zero config, added configuration as I learned, and now I'm using expert overrides. Smooth progression." - Expert User

> "Migration took 10 minutes with the automated script. All my agents now have observability and checkpointing for free!" - Existing User

---

## Conclusion

### What We're Building

A **unified Agent API** that makes Kaizen the **simplest AI agent framework** while maintaining **full enterprise power**:

1. **ONE entry point**: `from kaizen import Agent`
2. **THREE layers**: Simple → Config → Expert
3. **EVERYTHING enabled**: Memory, tools, observability, checkpointing by default
4. **CONFIGURATION-driven**: Behavior through parameters, not class hierarchy
5. **100% backward compatible**: Existing code still works

### Why This Matters

**Current Reality**:
- 16 agent classes to choose from
- 30+ features scattered across modules
- Decision paralysis for new users
- Duplicated code across examples
- Hidden capabilities (users don't know what's available)

**Future State**:
- 1 agent class with smart defaults
- All features available out-of-the-box
- Clear mental model (3 layers)
- Minimal code duplication
- Feature discovery through documentation and startup banner

### Next Steps

1. **Review this design** with team
2. **Prototype Agent class** (Week 1)
3. **Test with real examples** (Week 2)
4. **Iterate based on feedback** (Week 3)
5. **Launch with documentation** (Week 4)

---

**Document Prepared By**: Claude (Deep Analysis)
**Date**: 2025-10-26
**Status**: READY FOR REVIEW

**Files Referenced**:
- `/Users/esperie/repos/dev/kailash_kaizen/apps/kailash-kaizen/src/kaizen/__init__.py`
- `/Users/esperie/repos/dev/kailash_kaizen/apps/kailash-kaizen/src/kaizen/core/base_agent.py`
- `/Users/esperie/repos/dev/kailash_kaizen/apps/kailash-kaizen/src/kaizen/agents/__init__.py`
- `/Users/esperie/repos/dev/kailash_kaizen/apps/kailash-kaizen/src/kaizen/strategies/__init__.py`
- `/Users/esperie/repos/dev/kailash_kaizen/apps/kailash-kaizen/src/kaizen/tools/__init__.py`
- `/Users/esperie/repos/dev/kailash_kaizen/apps/kailash-kaizen/src/kaizen/memory/__init__.py`
- `/Users/esperie/repos/dev/kailash_kaizen/.claude/skills/04-kaizen/README.md`
- All 30+ skill files in `.claude/skills/04-kaizen/`
