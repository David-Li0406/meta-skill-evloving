---
name: kaizen
description: "Kailash Kaizen - production-ready AI agent framework with signature-based programming, multi-agent coordination, and enterprise features. Use when asking about 'AI agents', 'agent framework', 'BaseAgent', 'multi-agent systems', 'agent coordination', 'signatures', 'agent signatures', 'RAG agents', 'vision agents', 'audio agents', 'multimodal agents', 'agent prompts', 'prompt optimization', 'chain of thought', 'ReAct pattern', 'Planning agent', 'PEV agent', 'Tree-of-Thoughts', 'pipeline patterns', 'supervisor-worker', 'router pattern', 'ensemble pattern', 'blackboard pattern', 'parallel execution', 'agent-to-agent communication', 'A2A protocol', 'streaming agents', 'agent testing', 'agent memory', 'agentic workflows', 'AgentRegistry', 'OrchestrationRuntime', 'distributed agents', 'agent registry', '100+ agents', 'capability discovery', 'fault tolerance', 'health monitoring', 'trust protocol', 'EATP', 'TrustedAgent', 'trust chains', 'secure messaging', 'enterprise trust', 'credential rotation', 'trust verification', or 'cross-organization agents'."
---

# Kailash Kaizen - AI Agent Framework

Kaizen is a production-ready AI agent framework built on Kailash Core SDK that provides signature-based programming and multi-agent coordination.

## Features

Kaizen enables building sophisticated AI agents with:

- **Signature-Based Programming**: Type-safe agent interfaces with automatic validation and optimization
- **BaseAgent Architecture**: Production-ready agent foundation with error handling, audit trails, and cost tracking
- **Multi-Agent Coordination**: Supervisor-worker, agent-to-agent protocols, hierarchical structures
- **Orchestration Patterns**: 9 composable patterns (Ensemble, Blackboard, Router, Parallel, Sequential, Supervisor-Worker, Handoff, Consensus, Debate)
- **Multimodal Processing**: Vision, audio, and text processing capabilities
- **Autonomy Infrastructure**: 6 integrated subsystems (Hooks, Checkpoint, Interrupt, Memory, Planning, Meta-Controller)
- **Distributed Coordination**: AgentRegistry for 100+ agent systems with O(1) capability discovery
- **Enterprise Features**: Cost tracking, streaming responses, automatic optimization
- **Memory System**: 3-tier hierarchical storage (Hot/Warm/Cold) with DataFlow backend
- **Security**: RBAC, process isolation, compliance controls (SOC2, GDPR, HIPAA, PCI-DSS)
- **Enterprise Agent Trust Protocol (v0.8.0)**: Cryptographic trust chains, TrustedAgent, secure messaging, credential rotation

## Quick Start

### Basic Agent
```python
from kaizen.core.base_agent import BaseAgent
from kaizen.signatures import Signature, InputField, OutputField
from dataclasses import dataclass

# Define agent signature (type-safe interface)
class SummarizeSignature(Signature):
    text: str = InputField(description="Text to summarize")
    summary: str = OutputField(description="Generated summary")

# Define configuration
@dataclass
class SummaryConfig:
    llm_provider: str = "openai"
    model: str = "gpt-4"
    temperature: float = 0.7

# Create agent with signature
class SummaryAgent(BaseAgent):
    def __init__(self, config: SummaryConfig):
        super().__init__(
            config=config,
            signature=SummarizeSignature()
        )

# Execute
agent = SummaryAgent(SummaryConfig())
result = agent.run(text="Long text here...")
print(result['summary'])
```

### Pipeline Patterns (Orchestration)
```python
from kaizen.orchestration.pipeline import Pipeline

# Ensemble: Multi-perspective collaboration
pipeline = Pipeline.ensemble(
    agents=[code_expert, data_expert, writing_expert, research_expert],
    synthesizer=synthesis_agent,
    discovery_mode="a2a",  # A2A semantic matching
    top_k=3                # Select top 3 agents
)

# Execute - automatically selects best agents for task
result = pipeline.run(task="Analyze codebase", input="repo_path")

# Router: Intelligent task delegation
router = Pipeline.router(
    agents=[code_agent, data_agent, writing_agent],
    routing_strategy="semantic"  # A2A-based routing
)

# Blackboard: Iterative problem-solving
blackboard = Pipeline.blackboard(
    agents=[solver, analyzer, optimizer],
    controller=controller,
    max_iterations=10,
    discovery_mode="a2a"
)
```

## Reference Documentation

### Comprehensive Guides

For in-depth documentation, see `apps/kailash-kaizen/docs/`:

**Core Guides:**
- **[BaseAgent Architecture](../../../apps/kailash-kaizen/docs/guides/baseagent-architecture.md)** - Complete unified agent system guide
- **[Multi-Agent Coordination](../../../apps/kailash-kaizen/docs/guides/multi-agent-coordination.md)** - Google A2A protocol, 5 coordination patterns
- **[Signature Programming](../../../apps/kailash-kaizen/docs/guides/signature-programming.md)** - Complete signature system guide
- **[Hooks System Guide](../../../apps/kailash-kaizen/docs/guides/hooks-system-guide.md)** - Event-driven observability framework
- **[Integration Patterns](../../../apps/kailash-kaizen/docs/guides/integration-patterns.md)** - DataFlow, Nexus, MCP integration
- **[Meta-Controller Guide](../../../apps/kailash-kaizen/docs/guides/meta-controller-guide.md)** - Intelligent task delegation
- **[Planning System Guide](../../../apps/kailash-kaizen/docs/guides/planning-system-guide.md)** - Structured workflow orchestration

**Reference Documentation:**
- **[Example Gallery](../../../apps/kailash-kaizen/examples/autonomy/EXAMPLE_GALLERY.md)** - 15 production-ready autonomy examples with learning paths
- **[API Reference](../../../apps/kailash-kaizen/docs/reference/api-reference.md)** - Complete API documentation
- **[Checkpoint API](../../../apps/kailash-kaizen/docs/reference/checkpoint-api.md)** - State persistence API
- **[Coordination API](../../../apps/kailash-kaizen/docs/reference/coordination-api.md)** - Multi-agent coordination API
- **[Interrupts API](../../../apps/kailash-kaizen/docs/reference/interrupts-api.md)** - Graceful shutdown API
- **[Memory API](../../../apps/kailash-kaizen/docs/reference/memory-api.md)** - 3-tier memory system API
- **[Observability API](../../../apps/kailash-kaizen/docs/reference/observability-api.md)** - Hooks and monitoring API
- **[Planning Agents API](../../../apps/kailash-kaizen/docs/reference/planning-agents-api.md)** - Planning/PEV/ToT agents API
- **[Tools API](../../../apps/kailash-kaizen/docs/reference/tools-api.md)** - Tool calling and approval API
- **[Configuration Guide](../../../apps/kailash-kaizen/docs/reference/configuration.md)** - All configuration options
- **[Troubleshooting](../../../apps/kailash-kaizen/docs/reference/troubleshooting.md)** - Common issues and solutions

### Quick Start (Skills)
- **[kaizen-quickstart-template](kaizen-quickstart-template.md)** - Quick start guide with templates
- **[kaizen-baseagent-quick](kaizen-baseagent-quick.md)** - BaseAgent fundamentals
- **[kaizen-signatures](kaizen-signatures.md)** - Signature-based programming
- **[kaizen-agent-execution](kaizen-agent-execution.md)** - Agent execution patterns
- **[README](README.md)** - Framework overview

### Agent Patterns
- **[kaizen-agent-patterns](kaizen-agent-patterns.md)** - Common agent design patterns
- **[kaizen-chain-of-thought](kaizen-chain-of-thought.md)** - Chain of thought reasoning
- **[kaizen-react-pattern](kaizen-react-pattern.md)** - ReAct (Reason + Act) pattern
- **[kaizen-rag-agent](kaizen-rag-agent.md)** - Retrieval-Augmented Generation agents
- **[kaizen-config-patterns](kaizen-config-patterns.md)** - Agent configuration strategies

### Multi-Agent Systems & Orchestration
- **[kaizen-multi-agent-setup](kaizen-multi-agent-setup.md)** - Multi-agent system setup
- **[kaizen-supervisor-worker](kaizen-supervisor-worker.md)** - Supervisor-worker coordination
- **[kaizen-a2a-protocol](kaizen-a2a-protocol.md)** - Agent-to-agent communication
- **[kaizen-shared-memory](kaizen-shared-memory.md)** - Shared memory between agents
- **[kaizen-agent-registry](kaizen-agent-registry.md)** - Distributed agent coordination for 100+ agent systems

**Pipeline Patterns** (9 Composable Patterns):
- **Ensemble**: Multi-perspective collaboration with A2A discovery + synthesis
- **Blackboard**: Controller-driven iterative problem-solving
- **Router** (Meta-Controller): Intelligent task routing via A2A matching
- **Parallel**: Concurrent execution with aggregation
- **Sequential**: Linear agent chain
- **Supervisor-Worker**: Hierarchical coordination
- **Handoff**: Agent handoff with context transfer
- **Consensus**: Voting-based decision making
- **Debate**: Adversarial deliberation

### Multimodal Processing
- **[kaizen-multimodal-orchestration](kaizen-multimodal-orchestration.md)** - Multimodal coordination
- **[kaizen-vision-processing](kaizen-vision-processing.md)** - Vision and image processing
- **[kaizen-audio-processing](kaizen-audio-processing.md)** - Audio processing agents
- **[kaizen-multimodal-pitfalls](kaizen-multimodal-pitfalls.md)** - Common pitfalls and solutions

### Advanced Features
- **[kaizen-control-protocol](kaizen-control-protocol.md)** - Bidirectional agent ↔ client communication
- **[kaizen-tool-calling](kaizen-tool-calling.md)** - Autonomous tool execution with approval workflows
- **[kaizen-memory-system](kaizen-memory-system.md)** - Persistent memory, learning, FAQ detection
- **[kaizen-checkpoint-resume](kaizen-checkpoint-resume.md)** - Checkpoint & resume for long-running agents
- **[kaizen-interrupt-mechanism](kaizen-interrupt-mechanism.md)** - Graceful shutdown, Ctrl+C handling
- **[kaizen-persistent-memory](kaizen-persistent-memory.md)** - DataFlow-backed conversation persistence
- **[kaizen-streaming](kaizen-streaming.md)** - Streaming agent responses
- **[kaizen-cost-tracking](kaizen-cost-tracking.md)** - Cost monitoring and optimization
- **[kaizen-ux-helpers](kaizen-ux-helpers.md)** - UX enhancement utilities

### Observability & Monitoring
- **[kaizen-observability-hooks](kaizen-observability-hooks.md)** - Lifecycle event hooks, production security (RBAC)
- **[kaizen-observability-tracing](kaizen-observability-tracing.md)** - Distributed tracing with OpenTelemetry
- **[kaizen-observability-metrics](kaizen-observability-metrics.md)** - Prometheus metrics collection
- **[kaizen-observability-logging](kaizen-observability-logging.md)** - Structured JSON logging
- **[kaizen-observability-audit](kaizen-observability-audit.md)** - Compliance audit trails

### Enterprise Agent Trust Protocol (v0.8.0)
- **[kaizen-trust-eatp](kaizen-trust-eatp.md)** - Complete trust infrastructure for AI agents
  - Trust lineage chains with cryptographic verification
  - TrustedAgent and TrustedSupervisorAgent with built-in trust
  - Secure messaging with HMAC authentication and replay protection
  - Trust-aware orchestration with policy enforcement
  - Enterprise System Agent (ESA) for legacy system integration
  - A2A HTTP service for cross-organization trust operations
  - Credential rotation, rate limiting, and security audit logging

### Testing & Quality
- **[kaizen-testing-patterns](kaizen-testing-patterns.md)** - Testing AI agents
- **[Performance Benchmarks](../../../apps/kailash-kaizen/docs/benchmarks/BENCHMARK_GUIDE.md)** - Measure Kaizen performance

## Key Concepts

### Signature-Based Programming
Signatures define type-safe interfaces for agents:
- **Input**: Define expected inputs with descriptions
- **Output**: Specify output format and structure
- **Validation**: Automatic type checking and validation
- **Optimization**: Framework can optimize prompts automatically

### BaseAgent Architecture
Foundation for all Kaizen agents:
- **Error Handling**: Built-in retry logic and error recovery
- **Audit Trails**: Automatic logging of agent actions
- **Cost Tracking**: Monitor API usage and costs
- **Streaming**: Support for streaming responses
- **Memory**: State management across invocations
- **Hooks System**: Zero-code-change observability and lifecycle management

### Autonomy Infrastructure (6 Subsystems)

**1. Hooks System** - Event-driven observability framework
- Zero-code-change monitoring via lifecycle events (PRE/POST hooks)
- 6 builtin hooks: Logging, Metrics, Cost, Performance, Audit, Tracing
- Production security: RBAC, Ed25519 signatures, process isolation, rate limiting
- Performance: <0.01ms overhead (625x better than 10ms target)

**2. Checkpoint System** - Persistent state management
- Save/load/fork agent state for failure recovery
- 4 storage backends: Filesystem, Redis, PostgreSQL, S3
- Automatic compression and incremental checkpoints
- State manager with deduplication and versioning

**3. Interrupt Mechanism** - Graceful shutdown and execution control
- 3 interrupt sources: USER (Ctrl+C), SYSTEM (timeout/budget), PROGRAMMATIC (API)
- 2 shutdown modes: GRACEFUL (finish cycle + checkpoint) vs IMMEDIATE (stop now)
- Signal propagation across multi-agent hierarchies

**4. Memory System** - 3-tier hierarchical storage
- Hot tier: In-memory buffer (<1ms retrieval, last 100 messages)
- Warm tier: Database (10-50ms, agent-specific history with JSONL compression)
- Cold tier: Object storage (100ms+, long-term archival with S3/MinIO)
- DataFlow-backed with auto-persist and cross-session continuity

**5. Planning Agents** - Structured workflow orchestration
- PlanningAgent: Plan before you act (pre-execution validation)
- PEVAgent: Plan, Execute, Verify, Refine (iterative refinement)
- Tree-of-Thoughts: Explore multiple reasoning paths
- Multi-step decomposition, validation, and replanning

**6. Meta-Controller Routing** - Intelligent task delegation
- A2A-based semantic capability matching (no hardcoded if/else)
- Automatic agent discovery, ranking, and selection
- Fallback strategies and load balancing
- Integrated with Router, Ensemble, and Supervisor-Worker patterns

### AgentRegistry - Distributed Coordination
For 100+ agent distributed systems:
- O(1) capability-based discovery with semantic matching
- Event broadcasting (6 event types for cross-runtime coordination)
- Health monitoring with automatic deregistration
- Status management (ACTIVE, UNHEALTHY, DEGRADED, OFFLINE)
- Multi-runtime coordination across processes/machines

## When to Use This Skill

Use Kaizen when you need to:
- Build AI agents with type-safe interfaces
- Implement multi-agent systems with orchestration patterns
- Process multimodal inputs (vision, audio, text)
- Create RAG (Retrieval-Augmented Generation) systems
- Implement chain-of-thought reasoning
- Build supervisor-worker or ensemble architectures
- Track costs and performance of AI agents
- Add zero-code-change observability to agents
- Monitor, trace, and audit agent behavior in production
- Secure agent observability with RBAC and compliance controls
- Create production-ready agentic applications
- **Enterprise trust and accountability (v0.8.0)**:
  - Cryptographic trust chains for AI agents
  - Cross-organization agent coordination
  - Regulatory compliance with audit trails
  - Secure inter-agent communication

**Use Pipeline Patterns When:**
- **Ensemble**: Need diverse perspectives synthesized (code review, research)
- **Blackboard**: Iterative problem-solving (optimization, debugging)
- **Router**: Intelligent task delegation to specialists
- **Parallel**: Bulk processing or voting-based consensus
- **Sequential**: Linear workflows with dependency chains

## Integration Patterns

### With DataFlow (Data-Driven Agents)
```python
from kaizen.core.base_agent import BaseAgent
from dataflow import DataFlow

class DataAgent(BaseAgent):
    def __init__(self, config, db: DataFlow):
        self.db = db
        super().__init__(config=config, signature=MySignature())
```

### With Nexus (Multi-Channel Agents)
```python
from kaizen.core.base_agent import BaseAgent
from nexus import Nexus

# Deploy agents via API/CLI/MCP
agent_workflow = create_agent_workflow()
nexus = Nexus([agent_workflow])
nexus.run()  # Agents available via all channels
```

### With Core SDK (Custom Workflows)
```python
from kaizen.core.base_agent import BaseAgent
from kailash.workflow.builder import WorkflowBuilder

# Embed agents in workflows
workflow = WorkflowBuilder()
workflow.add_node("KaizenAgent", "agent1", {
    "agent": my_agent,
    "input": "..."
})
```

## Critical Rules

- ✅ Define signatures before implementing agents
- ✅ Extend BaseAgent for production agents
- ✅ Use type hints in signatures for validation
- ✅ Track costs in production environments
- ✅ Test agents with real infrastructure (NO MOCKING)
- ✅ Enable hooks for observability
- ✅ Use AgentRegistry for distributed coordination
- ❌ NEVER skip signature definitions
- ❌ NEVER ignore cost tracking in production
- ❌ NEVER mock LLM calls in integration tests

## Related Skills

- **[01-core-sdk](../../01-core-sdk/SKILL.md)** - Core workflow patterns
- **[02-dataflow](../dataflow/SKILL.md)** - Database integration
- **[03-nexus](../nexus/SKILL.md)** - Multi-channel deployment
- **[05-mcp](../mcp/SKILL.md)** - MCP server integration
- **[17-gold-standards](../../17-gold-standards/SKILL.md)** - Best practices

## Support

For Kaizen-specific questions, invoke:
- `kaizen-specialist` - Kaizen framework implementation
- `testing-specialist` - Agent testing strategies
- `framework-advisor` - When to use Kaizen vs other frameworks
