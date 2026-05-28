# Unified Agent API - Implementation Blueprint

**Detailed Technical Specification for Developers**

---

## File Structure

```
apps/kailash-kaizen/
├── src/kaizen/
│   ├── __init__.py                    # Export Agent class
│   ├── core/
│   │   ├── agents.py                  # NEW: Unified Agent class (THIS FILE)
│   │   ├── base_agent.py              # KEEP: Foundation (used internally)
│   │   ├── config.py                  # KEEP: BaseAgentConfig
│   │   └── presets.py                 # NEW: Agent type and workflow presets
│   ├── agents/
│   │   ├── specialized/
│   │   │   ├── simple_qa.py           # REFACTOR: Thin wrapper over Agent
│   │   │   ├── react.py               # REFACTOR: Thin wrapper over Agent
│   │   │   ├── chain_of_thought.py    # REFACTOR: Thin wrapper over Agent
│   │   │   └── ...                    # All become thin wrappers
│   └── ...
├── tests/
│   ├── unit/
│   │   └── test_unified_agent.py      # NEW: 100+ unit tests
│   ├── integration/
│   │   └── test_unified_agent_integration.py  # NEW: 20+ integration tests
│   └── ...
├── examples/
│   └── unified_agent/                 # NEW: 20+ examples using Agent class
│       ├── 01_simple_qa.py
│       ├── 02_react_pattern.py
│       ├── 03_multi_modal.py
│       └── ...
└── docs/
    └── guides/
        ├── unified_agent.md           # NEW: Complete guide
        └── migration_guide.md         # NEW: Migration from specialized classes
```

---

## Part 1: Core Implementation (`src/kaizen/core/agents.py`)

### Agent Class Skeleton

```python
"""
Unified Agent API - Single entry point for all agent types.

This module implements the unified Agent class that replaces the need for
16 specialized agent classes through configuration-driven behavior.

Examples:
    # Zero-config (Layer 1)
    >>> agent = Agent(model="gpt-4")
    >>> result = agent.run("What is AI?")

    # Configured (Layer 2)
    >>> agent = Agent(model="gpt-4", agent_type="react", memory_turns=20)

    # Expert override (Layer 3)
    >>> agent = Agent(model="gpt-4", memory=CustomMemory())

Architecture:
    Agent wraps BaseAgent and provides:
    - Smart defaults for all infrastructure
    - Configuration-driven specialization
    - Progressive disclosure (3 layers)
    - 100% backward compatibility

Author: Kaizen Team
Created: 2025-10-26
"""

from typing import Literal, Optional, List, Dict, Any, Callable, Union
from dataclasses import dataclass
import logging
import uuid

# Kaizen imports
from kaizen.core.base_agent import BaseAgent
from kaizen.core.config import BaseAgentConfig
from kaizen.core.presets import AGENT_TYPE_PRESETS, WORKFLOW_PRESETS
from kaizen.signatures import Signature, InputField, OutputField
from kaizen.memory import (
    BaseMemory,
    BufferMemory,
    PersistentBufferMemory,
    SummaryMemory,
    VectorMemory,
    KnowledgeGraphMemory,
    SharedMemoryPool,
)
# Tools auto-configured via MCP, ToolExecutor

from kaizen.core.autonomy.hooks import HookManager
from kaizen.core.autonomy.state.manager import StateManager
from kaizen.core.autonomy.state.storage import FilesystemStorage
from kaizen.core.autonomy.control import ControlProtocol

logger = logging.getLogger(__name__)

__all__ = ["Agent", "AgentManager"]

class Agent:
    """
    Universal agent with everything enabled by default.

    Provides a unified entry point that replaces the need for specialized
    agent classes (SimpleQAAgent, ReActAgent, etc.) through configuration.

    Features enabled by default:
        - Memory: 10 turns, buffer backend
        - Tools: All 12 builtin tools
        - Observability: Tracing, metrics, logging
        - Checkpointing: Every 5 steps
        - Cost tracking: $1.00 USD budget limit
        - Rich UX: Startup banner, progress, metrics
        - Error handling: 3 automatic retries
        - Google A2A: Capability card generation

    Three usage layers:
        1. Zero-config: agent = Agent(model="gpt-4")
        2. Configuration: agent = Agent(model="gpt-4", agent_type="react")
        3. Expert override: agent = Agent(model="gpt-4", memory=CustomMemory())

    Examples:
        # Layer 1: Zero-config
        >>> agent = Agent(model="gpt-4")
        >>> result = agent.run("Explain quantum computing")

        # Layer 2: Configured
        >>> agent = Agent(
        ...     model="gpt-4",
        ...     agent_type="react",
        ...     memory_turns=20,
        ...     tools=["read_file", "http_get"],
        ...     budget_limit_usd=5.0
        ... )

        # Layer 3: Expert
        >>> agent = Agent(
        ...     model="gpt-4",
        ...     memory=RedisMemory(),
        ...     tools="all"  # Enable tools via MCP
        ...     hook_manager=DatadogHooks()
        ... )
    """

    def __init__(
        self,
        # ====================================
        # REQUIRED PARAMETERS
        # ====================================
        model: str,

        # ====================================
        # LAYER 1: SMART DEFAULTS
        # ====================================
        provider: str = "openai",
        agent_id: Optional[str] = None,

        # ====================================
        # LAYER 2: BEHAVIORAL CONFIGURATION
        # ====================================

        # Agent behavior
        agent_type: Literal[
            "simple",        # Simple Q&A, single inference
            "cot",           # Chain of thought reasoning
            "react",         # Reason + Act cycles
            "rag",           # Retrieval-augmented generation
            "autonomous",    # Long-running autonomous agent
            "reflection",    # Self-reflection and improvement
        ] = "simple",

        workflow: Optional[Literal[
            "supervisor_worker",  # Supervisor delegates to workers
            "consensus",          # Multi-agent consensus
            "debate",             # Adversarial debate
            "sequential",         # Sequential pipeline
            "handoff",            # Dynamic handoff
        ]] = None,

        multimodal: Optional[List[Literal["vision", "audio", "document"]]] = None,

        # Memory configuration
        memory_turns: int = 10,
        memory_type: Literal[
            "buffer",           # In-memory buffer
            "persistent",       # SQLite persistence
            "summary",          # LLM-generated summaries
            "vector",           # Semantic search
            "knowledge_graph",  # Entity relationships
        ] = "buffer",
        memory_backend: Literal["file", "sqlite", "postgresql"] = "file",
        shared_memory: Optional[SharedMemoryPool] = None,

        # Tool configuration
        tools: Union[
            Literal["all"],    # All builtin tools
            List[str],         # Subset of tools
            Literal[False]     # No tools
        ] = "all",
        auto_approve_safe: bool = True,
        require_approval: bool = False,

        # Execution configuration
        max_cycles: int = 10,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,

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
        show_cost: bool = True,

        # Workflow configuration (if workflow is set)
        workers: Optional[List['Agent']] = None,
        workflow_config: Optional[Dict[str, Any]] = None,

        # ====================================
        # LAYER 3: EXPERT OVERRIDES
        # ====================================
        signature: Optional[Signature] = None,
        memory: Optional[BaseMemory] = None,
        tool_registry: Optional[ToolRegistry] = None,
        hook_manager: Optional[HookManager] = None,
        state_manager: Optional[StateManager] = None,
        control_protocol: Optional[ControlProtocol] = None,
        mcp_client: Optional['MCPClient'] = None,
        approval_callback: Optional[Callable] = None,
        error_handler: Optional[Callable] = None,

        **kwargs
    ):
        """
        Initialize unified agent with smart defaults.

        See class docstring for parameter descriptions and examples.
        """
        # Store core parameters
        self.model = model
        self.provider = provider
        self.agent_id = agent_id or self._generate_agent_id()

        # Store configuration
        self._agent_type = agent_type
        self._workflow = workflow
        self._multimodal = multimodal or []

        # Store all config parameters for access
        self._config = {
            "memory_turns": memory_turns,
            "memory_type": memory_type,
            "memory_backend": memory_backend,
            "tools": tools,
            "max_cycles": max_cycles,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "budget_limit_usd": budget_limit_usd,
            "checkpoint_frequency": checkpoint_frequency,
            "checkpointing": checkpointing,
            "observability": observability,
            "tracing_only": tracing_only,
            "rich_output": rich_output,
            "verbosity": verbosity,
            "streaming": streaming,
            "progress_reporting": progress_reporting,
            "show_cost": show_cost,
            "auto_approve_safe": auto_approve_safe,
            "require_approval": require_approval,
        }

        # Initialize component configurations
        self._memory_config = {}
        self._tools_config = {}
        self._observability_config = {}
        self._checkpoint_config = {}
        self._budget_config = {}

        # Setup smart defaults
        self._setup_smart_defaults()

        # Apply agent type preset
        self._apply_agent_type(agent_type)

        # Apply multimodal configuration
        if multimodal:
            self._apply_multimodal(multimodal)

        # Apply workflow pattern
        if workflow:
            self._apply_workflow(workflow, workers, workflow_config)

        # Setup infrastructure (smart defaults or expert overrides)
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
            shared_memory=shared_memory,
            **kwargs
        )

        # Show startup banner (if enabled)
        if rich_output and verbosity != "quiet":
            self._show_startup_banner()

    # ====================================
    # SETUP METHODS (INTERNAL)
    # ====================================

    def _generate_agent_id(self) -> str:
        """Generate unique agent ID."""
        return f"agent_{uuid.uuid4().hex[:8]}"

    def _setup_smart_defaults(self):
        """Setup smart defaults for all components."""
        # Memory configuration
        self._memory_config = {
            "type": self._config["memory_type"],
            "turns": self._config["memory_turns"],
            "backend": self._config["memory_backend"],
            "enabled": self._config["memory_type"] != False,
        }

        # Tools configuration
        self._tools_config = {
            "enabled": self._config["tools"] != False,
            "tools": self._config["tools"],
            "auto_approve_safe": self._config["auto_approve_safe"],
            "require_approval": self._config["require_approval"],
        }

        # Observability configuration
        if self._config["tracing_only"]:
            self._observability_config = {
                "enabled": True,
                "tracing": True,
                "metrics": False,
                "logging": False,
            }
        else:
            self._observability_config = {
                "enabled": self._config["observability"],
                "tracing": self._config["observability"],
                "metrics": self._config["observability"],
                "logging": self._config["observability"],
            }

        # Checkpointing configuration
        self._checkpoint_config = {
            "enabled": self._config["checkpointing"],
            "frequency": self._config["checkpoint_frequency"],
            "storage": "filesystem",
            "compress": True,
        }

        # Budget configuration
        self._budget_config = {
            "limit_usd": self._config["budget_limit_usd"],
            "warn_at": 0.75,   # Warn at 75%
            "error_at": 1.0,   # Error at 100%
            "show_cost": self._config["show_cost"],
        }

    def _apply_agent_type(self, agent_type: str):
        """Apply agent type preset configuration."""
        preset = AGENT_TYPE_PRESETS.get(agent_type)
        if not preset:
            raise ValueError(
                f"Unknown agent_type: {agent_type}. "
                f"Valid options: {list(AGENT_TYPE_PRESETS.keys())}"
            )

        # Store preset for reference
        self._preset = preset

        # Apply execution strategy
        self._strategy = preset["strategy"]

        # Apply max cycles (preset can override user config)
        self._max_cycles = preset.get("max_cycles", self._config["max_cycles"])

        # Override tool configuration if preset disables tools
        if not preset.get("tools_enabled", True):
            self._tools_config["enabled"] = False

        # Apply preset-specific features
        if preset.get("reasoning_steps"):
            self._reasoning_enabled = True
            self._prompt_modifier = preset.get("prompt_modifier", "")

        if preset.get("convergence"):
            self._convergence_strategy = preset["convergence"]

        if preset.get("required_tools"):
            self._required_tools = preset["required_tools"]
            # Ensure required tools are enabled
            if not self._tools_config["enabled"]:
                raise ValueError(
                    f"Agent type '{agent_type}' requires tools, "
                    f"but tools are disabled"
                )

        if preset.get("checkpointing_required"):
            if not self._checkpoint_config["enabled"]:
                logger.warning(
                    f"Agent type '{agent_type}' works best with checkpointing. "
                    f"Enabling checkpointing automatically."
                )
                self._checkpoint_config["enabled"] = True

        if preset.get("reflection_enabled"):
            self._reflection_enabled = True

    def _apply_multimodal(self, modalities: List[str]):
        """Apply multimodal configuration."""
        self._vision_enabled = "vision" in modalities
        self._audio_enabled = "audio" in modalities
        self._document_enabled = "document" in modalities

        # Validate multimodal requirements
        if self._vision_enabled or self._audio_enabled or self._document_enabled:
            # Ensure provider supports multimodal
            if self.provider not in ["openai", "anthropic", "ollama"]:
                raise ValueError(
                    f"Provider '{self.provider}' does not support multimodal. "
                    f"Use 'openai', 'anthropic', or 'ollama'."
                )

    def _apply_workflow(
        self,
        workflow: str,
        workers: Optional[List['Agent']],
        config: Optional[Dict[str, Any]]
    ):
        """Apply workflow pattern configuration."""
        workflow_preset = WORKFLOW_PRESETS.get(workflow)
        if not workflow_preset:
            raise ValueError(
                f"Unknown workflow: {workflow}. "
                f"Valid options: {list(WORKFLOW_PRESETS.keys())}"
            )

        # Validate required parameters
        required_params = workflow_preset.get("required_params", [])
        if "workers" in required_params and not workers:
            raise ValueError(
                f"Workflow '{workflow}' requires 'workers' parameter"
            )

        # Store workflow configuration
        self._workflow_preset = workflow_preset
        self._workers = workers or []
        self._workflow_config = config or {}

        # Workflow will be instantiated in _create_base_agent()

    def _setup_infrastructure(
        self,
        memory=None,
        tools="all"  # Enable tools via MCP
        hook_manager=None,
        state_manager=None,
        control_protocol=None,
        mcp_client=None,
    ):
        """
        Setup infrastructure components.

        Uses expert overrides if provided, otherwise creates smart defaults.
        """
        # Memory system
        if memory:
            self._memory = memory  # Expert override
        elif self._memory_config["enabled"]:
            self._memory = self._create_default_memory()  # Smart default
        else:
            self._memory = None  # Disabled

        # Tool registry
        if tool_registry:
            self._tool_registry = tool_registry  # Expert override
        elif self._tools_config["enabled"]:
            self._tool_registry = self._create_default_tool_registry()  # Smart default
        else:
            self._tool_registry = None  # Disabled

        # Hook manager (observability)
        if hook_manager:
            self._hook_manager = hook_manager  # Expert override
        elif self._observability_config["enabled"]:
            self._hook_manager = self._create_default_hook_manager()  # Smart default
        else:
            self._hook_manager = None  # Disabled

        # State manager (checkpointing)
        if state_manager:
            self._state_manager = state_manager  # Expert override
        elif self._checkpoint_config["enabled"]:
            self._state_manager = self._create_default_state_manager()  # Smart default
        else:
            self._state_manager = None  # Disabled

        # Control protocol (opt-in)
        self._control_protocol = control_protocol

        # MCP client (opt-in)
        self._mcp_client = mcp_client

    def _create_default_memory(self) -> BaseMemory:
        """Create default memory based on configuration."""
        memory_type = self._memory_config["type"]
        turns = self._memory_config["turns"]
        backend = self._memory_config["backend"]

        if memory_type == "buffer":
            return BufferMemory(max_turns=turns)
        elif memory_type == "persistent":
            # File or SQLite backend
            if backend == "sqlite":
                return PersistentBufferMemory(
                    db_path=f".kaizen/memory/{self.agent_id}.db",
                    max_turns=turns
                )
            else:
                return PersistentBufferMemory(
                    file_path=f".kaizen/memory/{self.agent_id}.jsonl",
                    max_turns=turns
                )
        elif memory_type == "summary":
            return SummaryMemory(
                llm_provider=self.provider,
                model=self.model,
                max_turns=turns
            )
        elif memory_type == "vector":
            return VectorMemory(
                embedding_provider=self.provider,
                max_turns=turns
            )
        elif memory_type == "knowledge_graph":
            return KnowledgeGraphMemory(
                llm_provider=self.provider,
                model=self.model,
                max_turns=turns
            )
        else:
            raise ValueError(f"Unknown memory_type: {memory_type}")

    def _create_default_tool_registry(self) -> ToolRegistry:
        """Create default tool registry with builtin tools."""


        # Register builtin tools
        if self._tools_config["tools"] == "all":
            # Register all 12 builtin tools
            # 12 builtin tools enabled via MCP
        elif isinstance(self._tools_config["tools"], list):
            # Register subset of tools
            register_builtin_tools(
                registry,
                tool_names=self._tools_config["tools"]
            )

        return registry

    def _create_default_hook_manager(self) -> HookManager:
        """Create default hook manager with observability."""
        hook_manager = HookManager()

        # Register observability hooks based on configuration
        if self._observability_config["tracing"]:
            from kaizen.core.autonomy.observability import register_tracing_hooks
            register_tracing_hooks(hook_manager)

        if self._observability_config["metrics"]:
            from kaizen.core.autonomy.observability import register_metrics_hooks
            register_metrics_hooks(hook_manager)

        if self._observability_config["logging"]:
            from kaizen.core.autonomy.observability import register_logging_hooks
            register_logging_hooks(hook_manager)

        return hook_manager

    def _create_default_state_manager(self) -> StateManager:
        """Create default state manager for checkpointing."""
        storage = FilesystemStorage(
            base_dir=f".kaizen/checkpoints/{self.agent_id}",
            compress=self._checkpoint_config["compress"]
        )

        return StateManager(
            storage=storage,
            checkpoint_frequency=self._checkpoint_config["frequency"],
            retention_count=10  # Keep latest 10 checkpoints
        )

    def _create_base_agent(
        self,
        signature: Optional[Signature],
        approval_callback: Optional[Callable],
        error_handler: Optional[Callable],
        shared_memory: Optional[SharedMemoryPool],
        **kwargs
    ) -> BaseAgent:
        """Create underlying BaseAgent with all configuration applied."""
        # Create BaseAgentConfig
        base_config = BaseAgentConfig(
            llm_provider=self.provider,
            model=self.model,
            temperature=self._config["temperature"],
            max_tokens=self._config["max_tokens"],
            agent_id=self.agent_id,
            # Add more config as needed
        )

        # Create or use provided signature
        if signature is None:
            signature = self._create_default_signature()

        # Create BaseAgent
        agent = BaseAgent(
            config=base_config,
            signature=signature,
            memory=self._memory,
            tools="all"  # Enable tools via MCP
            hook_manager=self._hook_manager,
            state_manager=self._state_manager,
            control_protocol=self._control_protocol,
            mcp_client=self._mcp_client,
            approval_callback=approval_callback,
            error_handler=error_handler,
            shared_memory=shared_memory,
            **kwargs
        )

        # Apply workflow pattern if specified
        if self._workflow:
            agent = self._wrap_with_workflow(agent)

        return agent

    def _create_default_signature(self) -> Signature:
        """Create default signature based on agent type."""
        # Generic signature that works for most cases
        class DefaultSignature(Signature):
            input: str = InputField(description="User input")
            output: str = OutputField(description="Agent output")

        return DefaultSignature()

    def _wrap_with_workflow(self, agent: BaseAgent) -> BaseAgent:
        """Wrap agent in workflow pattern if specified."""
        # Import workflow pattern class
        pattern_module = self._workflow_preset["pattern_class"]
        # TODO: Dynamically import and instantiate pattern
        # This is where workflow integration happens
        return agent

    # ====================================
    # UX METHODS (INTERNAL)
    # ====================================

    def _show_startup_banner(self):
        """Display rich startup banner."""
        if self._config["verbosity"] == "quiet":
            return

        print("\n✨ Kaizen Agent Starting...")
        print(f"   Model: {self.model} ({self.provider})")
        print(f"   Type: {self._agent_type} - {self._preset['description']}")

        if self._memory and self._memory_config["enabled"]:
            print(
                f"   Memory: Enabled "
                f"({self._memory_config['turns']} turns, "
                f"{self._memory_config['type']})"
            )

        if self._tool_registry and self._tools_config["enabled"]:
            tool_count = len(self._tool_registry.list_tools())
            print(f"   Tools: Enabled ({tool_count} tools)")

        if self._hook_manager and self._observability_config["enabled"]:
            features = []
            if self._observability_config["tracing"]:
                features.append("tracing")
            if self._observability_config["metrics"]:
                features.append("metrics")
            if self._observability_config["logging"]:
                features.append("logging")
            print(f"   Observability: Enabled ({', '.join(features)})")

        if self._state_manager and self._checkpoint_config["enabled"]:
            print(
                f"   Checkpointing: Enabled "
                f"(every {self._checkpoint_config['frequency']} steps)"
            )

        if self._budget_config["limit_usd"] is not None:
            print(f"   Budget: ${self._budget_config['limit_usd']:.2f} USD limit")

        print()  # Blank line

    def _show_progress_start(self):
        """Show execution start progress."""
        if self._config["verbosity"] == "quiet":
            return
        print("⚙️  Executing...")

    def _show_completion(self, result: Dict[str, Any]):
        """Show execution completion with metrics."""
        if self._config["verbosity"] == "quiet":
            return

        # Extract metrics from result
        duration = result.get("execution_time", 0)
        tokens = result.get("total_tokens", 0)
        cost = result.get("cost_usd", 0)

        print(f"✅ Complete ({duration:.1f}s, {tokens} tokens, ${cost:.3f})")

    # ====================================
    # PUBLIC API
    # ====================================

    def run(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Execute agent with given inputs.

        Delegates to underlying BaseAgent.run() with additional features:
        - Progress reporting (if enabled)
        - Cost tracking and warnings
        - Performance metrics
        - Error handling with retries

        Args:
            *args: Positional arguments passed to BaseAgent
            **kwargs: Keyword arguments passed to BaseAgent

        Returns:
            Dict with execution results including:
                - answer/output: Main result
                - execution_time: Duration in seconds
                - total_tokens: Token usage
                - cost_usd: Estimated cost
                - trace_id: Trace ID (if observability enabled)
        """
        # Show progress start
        if self._config["progress_reporting"]:
            self._show_progress_start()

        try:
            # Execute via BaseAgent
            result = self._base_agent.run(*args, **kwargs)

            # Check budget
            if self._budget_config["limit_usd"] is not None:
                self._check_budget(result)

            # Show completion
            if self._config["rich_output"]:
                self._show_completion(result)

            return result

        except Exception as e:
            # Handle error (with retries if configured)
            return self._handle_execution_error(e, *args, **kwargs)

    async def run_async(self, *args, **kwargs) -> Dict[str, Any]:
        """Async version of run()."""
        # Similar implementation to run() but async
        if self._config["progress_reporting"]:
            self._show_progress_start()

        try:
            result = await self._base_agent.run_async(*args, **kwargs)

            if self._budget_config["limit_usd"] is not None:
                self._check_budget(result)

            if self._config["rich_output"]:
                self._show_completion(result)

            return result

        except Exception as e:
            return await self._handle_execution_error_async(e, *args, **kwargs)

    def _check_budget(self, result: Dict[str, Any]):
        """Check budget and warn if approaching limit."""
        if self._budget_config["limit_usd"] is None:
            return  # No budget limit

        cost = result.get("cost_usd", 0)
        limit = self._budget_config["limit_usd"]

        if cost >= limit * self._budget_config["error_at"]:
            raise RuntimeError(
                f"Budget limit exceeded: ${cost:.3f} >= ${limit:.2f}"
            )
        elif cost >= limit * self._budget_config["warn_at"]:
            logger.warning(
                f"Approaching budget limit: ${cost:.3f} / ${limit:.2f} "
                f"({cost/limit*100:.0f}%)"
            )

    def _handle_execution_error(self, error: Exception, *args, **kwargs):
        """Handle execution error with retry logic."""
        # TODO: Implement retry logic
        raise error

    async def _handle_execution_error_async(self, error: Exception, *args, **kwargs):
        """Async version of error handler."""
        # TODO: Implement async retry logic
        raise error

    # ====================================
    # HELPER METHODS (DELEGATED)
    # ====================================

    def extract_list(self, result: Dict, key: str, default: List = None) -> List:
        """Extract list from result (delegates to BaseAgent)."""
        return self._base_agent.extract_list(result, key, default)

    def extract_dict(self, result: Dict, key: str, default: Dict = None) -> Dict:
        """Extract dict from result (delegates to BaseAgent)."""
        return self._base_agent.extract_dict(result, key, default)

    def extract_float(self, result: Dict, key: str, default: float = 0.0) -> float:
        """Extract float from result (delegates to BaseAgent)."""
        return self._base_agent.extract_float(result, key, default)

    def extract_str(self, result: Dict, key: str, default: str = "") -> str:
        """Extract string from result (delegates to BaseAgent)."""
        return self._base_agent.extract_str(result, key, default)

    def write_to_memory(
        self,
        content: Any,
        tags: List[str] = None,
        importance: float = 0.5
    ):
        """Write to memory (delegates to BaseAgent)."""
        return self._base_agent.write_to_memory(content, tags, importance)

    # ====================================
    # METADATA & INTROSPECTION
    # ====================================

    def to_a2a_card(self):
        """Generate Google A2A capability card (delegates to BaseAgent)."""
        return self._base_agent.to_a2a_card()

    def get_config(self) -> Dict[str, Any]:
        """Get current agent configuration."""
        return {
            "model": self.model,
            "provider": self.provider,
            "agent_id": self.agent_id,
            "agent_type": self._agent_type,
            "workflow": self._workflow,
            "multimodal": self._multimodal,
            **self._config,
        }

    def get_features(self) -> Dict[str, bool]:
        """Get enabled features."""
        return {
            "memory": self._memory is not None,
            "tools": self._tool_registry is not None,
            "observability": self._hook_manager is not None,
            "checkpointing": self._state_manager is not None,
            "control_protocol": self._control_protocol is not None,
            "mcp": self._mcp_client is not None,
            "vision": self._vision_enabled if hasattr(self, "_vision_enabled") else False,
            "audio": self._audio_enabled if hasattr(self, "_audio_enabled") else False,
            "document": self._document_enabled if hasattr(self, "_document_enabled") else False,
        }

# ====================================
# AGENT MANAGER (Multi-agent orchestration)
# ====================================

class AgentManager:
    """
    Manage multiple agents with coordination.

    Provides utilities for:
    - Creating and managing agent pools
    - Shared memory coordination
    - Workflow orchestration
    """

    def __init__(self, shared_memory: Optional[SharedMemoryPool] = None):
        """
        Initialize agent manager.

        Args:
            shared_memory: Optional shared memory pool for agents
        """
        self.agents: Dict[str, Agent] = {}
        self.shared_memory = shared_memory or SharedMemoryPool()

    def create_agent(self, agent_id: str, **kwargs) -> Agent:
        """Create and register an agent."""
        agent = Agent(agent_id=agent_id, shared_memory=self.shared_memory, **kwargs)
        self.agents[agent_id] = agent
        return agent

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get agent by ID."""
        return self.agents.get(agent_id)

    def list_agents(self) -> List[str]:
        """List all agent IDs."""
        return list(self.agents.keys())

    # TODO: Add workflow orchestration methods
```

---

## Part 2: Presets Definition (`src/kaizen/core/presets.py`)

```python
"""
Agent type and workflow presets for unified Agent API.

This module defines configuration presets for different agent behaviors
and workflow patterns.
"""

from typing import Dict, Any

# ====================================
# AGENT TYPE PRESETS
# ====================================

AGENT_TYPE_PRESETS: Dict[str, Dict[str, Any]] = {
    "simple": {
        "description": "Simple Q&A, single inference",
        "strategy": "single_shot",
        "max_cycles": 1,
        "tools_enabled": False,
        "memory_type": "buffer",
        "use_case": "Basic Q&A, fact retrieval, simple transformations",
    },

    "cot": {
        "description": "Step-by-step reasoning (Chain of Thought)",
        "strategy": "single_shot",
        "max_cycles": 1,
        "tools_enabled": False,
        "memory_type": "buffer",
        "reasoning_steps": True,
        "prompt_modifier": "Think step by step:",
        "use_case": "Math problems, logic puzzles, complex reasoning",
    },

    "react": {
        "description": "Reason + Act cycles with tool calling",
        "strategy": "multi_cycle",
        "max_cycles": 10,
        "tools_enabled": True,
        "memory_type": "persistent",
        "convergence": "satisfaction",
        "use_case": "Research, data gathering, API interactions",
    },

    "rag": {
        "description": "Retrieval-augmented generation",
        "strategy": "single_shot",
        "max_cycles": 1,
        "tools_enabled": True,
        "required_tools": ["vector_search"],
        "memory_type": "vector",
        "use_case": "Document Q&A, knowledge base queries",
    },

    "autonomous": {
        "description": "Long-running autonomous agent",
        "strategy": "multi_cycle",
        "max_cycles": 100,
        "tools_enabled": True,
        "memory_type": "persistent",
        "checkpointing_required": True,
        "convergence": "goal_achieved",
        "use_case": "Complex tasks, multi-step workflows, extended operations",
    },

    "reflection": {
        "description": "Self-reflection and improvement",
        "strategy": "multi_cycle",
        "max_cycles": 5,
        "tools_enabled": False,
        "memory_type": "persistent",
        "reflection_enabled": True,
        "use_case": "Self-improvement, error correction, quality refinement",
    },
}

# ====================================
# WORKFLOW PRESETS
# ====================================

WORKFLOW_PRESETS: Dict[str, Dict[str, Any]] = {
    "supervisor_worker": {
        "description": "Supervisor delegates tasks to specialized workers",
        "required_params": ["workers"],
        "optional_params": ["selection_strategy", "parallel_execution"],
        "pattern_class": "SupervisorWorkerPattern",
        "use_case": "Complex tasks requiring specialization",
    },

    "consensus": {
        "description": "Multiple agents reach consensus on decision",
        "required_params": ["agents"],
        "optional_params": ["consensus_threshold", "max_rounds"],
        "pattern_class": "ConsensusPattern",
        "use_case": "Critical decisions requiring agreement",
    },

    "debate": {
        "description": "Adversarial agents debate to best solution",
        "required_params": ["agents"],
        "optional_params": ["max_rounds", "judge_agent"],
        "pattern_class": "DebatePattern",
        "use_case": "Exploring multiple perspectives",
    },

    "sequential": {
        "description": "Sequential pipeline of specialized agents",
        "required_params": ["agents"],
        "optional_params": ["allow_backtrack"],
        "pattern_class": "SequentialPattern",
        "use_case": "Multi-stage processing pipelines",
    },

    "handoff": {
        "description": "Dynamic handoff between agents",
        "required_params": ["agents"],
        "optional_params": ["handoff_criteria"],
        "pattern_class": "HandoffPattern",
        "use_case": "Adaptive task routing",
    },
}
```

---

## Part 3: Package Export (`src/kaizen/__init__.py`)

```python
# Add to existing exports

from kaizen.core.agents import Agent, AgentManager

__all__ = [
    # ... existing exports ...
    "Agent",
    "AgentManager",
]
```

---

## Part 4: Testing Strategy

### Unit Tests (`tests/unit/test_unified_agent.py`)

```python
"""
Unit tests for unified Agent class.

Tests all 3 layers:
1. Zero-config defaults
2. Configuration options
3. Expert overrides
"""

import pytest
from kaizen import Agent
from kaizen.memory import BufferMemory, PersistentBufferMemory
# Tools auto-configured via MCP

class TestLayer1ZeroConfig:
    """Test zero-config defaults (Layer 1)."""

    def test_agent_creation_minimal(self):
        """Test agent creation with minimal parameters."""
        agent = Agent(model="gpt-4")

        assert agent.model == "gpt-4"
        assert agent.provider == "openai"
        assert agent.agent_id is not None

    def test_default_features_enabled(self):
        """Test all default features are enabled."""
        agent = Agent(model="gpt-4")

        features = agent.get_features()

        assert features["memory"] is True
        assert features["tools"] is True
        assert features["observability"] is True
        assert features["checkpointing"] is True

    def test_run_method_exists(self):
        """Test run method is available."""
        agent = Agent(model="gpt-4")

        assert hasattr(agent, "run")
        assert callable(agent.run)

class TestLayer2Configuration:
    """Test configuration options (Layer 2)."""

    def test_agent_type_simple(self):
        """Test simple agent type configuration."""
        agent = Agent(model="gpt-4", agent_type="simple")

        assert agent._agent_type == "simple"
        assert agent._max_cycles == 1

    def test_agent_type_react(self):
        """Test ReAct agent type configuration."""
        agent = Agent(model="gpt-4", agent_type="react")

        assert agent._agent_type == "react"
        assert agent._tools_config["enabled"] is True
        assert agent._max_cycles == 10

    def test_memory_configuration(self):
        """Test memory configuration options."""
        agent = Agent(
            model="gpt-4",
            memory_turns=20,
            memory_type="persistent"
        )

        assert agent._memory_config["turns"] == 20
        assert agent._memory_config["type"] == "persistent"

    def test_tools_configuration(self):
        """Test tools configuration options."""
        agent = Agent(
            model="gpt-4",
            tools=["read_file", "http_get"]
        )

        assert agent._tools_config["enabled"] is True
        assert agent._tools_config["tools"] == ["read_file", "http_get"]

    def test_disable_features(self):
        """Test disabling features."""
        agent = Agent(
            model="gpt-4",
            memory=False,
            tools=False,
            observability=False,
            checkpointing=False
        )

        features = agent.get_features()

        assert features["memory"] is False
        assert features["tools"] is False
        assert features["observability"] is False
        assert features["checkpointing"] is False

class TestLayer3ExpertOverride:
    """Test expert override options (Layer 3)."""

    def test_custom_memory(self):
        """Test custom memory override."""
        custom_memory = BufferMemory(max_turns=50)
        agent = Agent(model="gpt-4", memory=custom_memory)

        assert agent._memory is custom_memory

    def test_custom_tool_registry(self):
        """Test custom tool registry override."""
        custom_
        agent = Agent(model="gpt-4", tools="all"  # Enable tools via MCP

        assert agent._tool_registry is custom_registry

# Add 100+ more unit tests...
```

---

This blueprint provides the detailed technical specification for implementing the unified Agent API. The full implementation would continue with integration tests, migration tools, documentation, and examples.

Would you like me to continue with additional sections (migration tools, documentation templates, etc.)?
