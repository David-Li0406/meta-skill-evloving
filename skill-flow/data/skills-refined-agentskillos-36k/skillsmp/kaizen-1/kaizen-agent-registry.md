# AgentRegistry - Distributed Agent Coordination

**v0.6.4+**: Centralized agent lifecycle management for distributed multi-runtime coordination (100+ agent systems).

## Overview

AgentRegistry provides centralized coordination for distributed multi-agent systems with:

- **Multi-Runtime Coordination**: Track agents across distributed processes/machines
- **O(1) Capability Discovery**: Fast semantic agent lookup via capability indexing
- **Event Broadcasting**: Cross-runtime coordination with 6 event types
- **Health Monitoring**: Heartbeat-based detection with automatic deregistration
- **Status Management**: ACTIVE, UNHEALTHY, DEGRADED, OFFLINE agent states
- **Automatic Failover**: Health-based agent filtering for production routing

**Location**: `kaizen.orchestration.registry`
**Examples**: `examples/orchestration/agent-registry-patterns/` (3 patterns)
**Tests**: 27 unit + 12 integration + 6 E2E tests (100% coverage)

## Quick Start

### Basic Distributed Coordination

```python
from kaizen.orchestration import (
    AgentRegistry,
    AgentRegistryConfig,
    RegistryEventType,
    AgentStatus,
)

# Configure registry for distributed coordination
config = AgentRegistryConfig(
    enable_heartbeat_monitoring=True,
    heartbeat_timeout=30.0,              # Heartbeat timeout (seconds)
    auto_deregister_timeout=60.0,        # Auto-deregister timeout (seconds)
    enable_event_broadcasting=True,      # Enable event broadcasting
    event_queue_size=100,                # Event queue capacity
)

# Create and start registry
registry = AgentRegistry(config=config)
await registry.start()

# Register agents from different runtimes
agent_id = await registry.register_agent(my_agent, runtime_id="runtime_1")

# O(1) capability-based discovery with semantic matching
agents = await registry.find_agents_by_capability(
    "code generation",
    status_filter=AgentStatus.ACTIVE  # Only healthy agents
)

# Event-driven coordination
async def event_callback(event: RegistryEvent):
    print(f"Event: {event.event_type} for agent {event.agent_id}")

registry.subscribe(RegistryEventType.AGENT_STATUS_CHANGED, event_callback)

# Update agent health
await registry.update_agent_heartbeat(agent_id)
await registry.update_agent_status(agent_id, AgentStatus.UNHEALTHY)

# Deregister agent
await registry.deregister_agent(agent_id, runtime_id="runtime_1")

# Shutdown registry
await registry.shutdown()
```

## Core Concepts

### AgentRegistryConfig

Configuration for distributed agent coordination:

```python
from kaizen.orchestration import AgentRegistryConfig

config = AgentRegistryConfig(
    enable_heartbeat_monitoring=True,    # Enable heartbeat monitoring
    heartbeat_timeout=30.0,               # Heartbeat timeout (seconds)
    auto_deregister_timeout=60.0,         # Auto-deregister after timeout
    enable_event_broadcasting=True,       # Enable event broadcasting
    event_queue_size=100,                 # Event queue capacity
)
```

**Parameters**:
- `enable_heartbeat_monitoring`: Enable/disable heartbeat monitoring
- `heartbeat_timeout`: Max time between heartbeats before UNHEALTHY status
- `auto_deregister_timeout`: Max time before automatic deregistration
- `enable_event_broadcasting`: Enable/disable event broadcasting
- `event_queue_size`: Maximum number of events in queue

### Runtime Tracking

AgentRegistry tracks agents across distributed runtimes:

```python
# Register agents from different runtimes
agent_id_1 = await registry.register_agent(agent1, runtime_id="runtime_1")
agent_id_2 = await registry.register_agent(agent2, runtime_id="runtime_1")
agent_id_3 = await registry.register_agent(agent3, runtime_id="runtime_2")

# Query agents by runtime
runtime_1_agents = registry.runtime_agents["runtime_1"]  # {agent_id_1, agent_id_2}
runtime_2_agents = registry.runtime_agents["runtime_2"]  # {agent_id_3}

# Total agents across all runtimes
total_agents = len(registry.agents)  # 3
```

**Runtime Association**:
- Each agent associated with a `runtime_id`
- Registry tracks which agents belong to which runtimes
- RUNTIME_JOINED event when first agent from runtime registers
- RUNTIME_LEFT event when last agent from runtime deregisters

### Capability-Based Discovery

O(1) semantic agent lookup via capability indexing:

```python
# Semantic substring matching (case-insensitive)
code_agents = await registry.find_agents_by_capability("code generation")
data_agents = await registry.find_agents_by_capability("data")
python_agents = await registry.find_agents_by_capability("python")

# Status filtering (production routing)
healthy_agents = await registry.find_agents_by_capability(
    "code generation",
    status_filter=AgentStatus.ACTIVE  # Only healthy agents
)

unhealthy_agents = await registry.find_agents_by_capability(
    "code generation",
    status_filter=AgentStatus.UNHEALTHY  # Only failed agents
)

all_agents = await registry.find_agents_by_capability(
    "code generation",
    status_filter=None  # All agents regardless of status
)
```

**How It Works**:
1. Registry maintains O(1) capability index mapping capabilities to agents
2. Semantic substring matching (e.g., "python" matches "Python code generation")
3. Case-insensitive search
4. Status filtering excludes unhealthy agents automatically
5. Returns `List[AgentMetadata]` with full agent information

**AgentMetadata Structure**:
```python
# find_agents_by_capability returns List[AgentMetadata]
for metadata in agents:
    agent_id = metadata.agent_id          # Unique agent ID
    agent = metadata.agent                 # BaseAgent instance
    a2a_card = metadata.agent._a2a_card   # A2A capability card
    status = metadata.status               # AgentStatus (ACTIVE/UNHEALTHY/etc.)
    last_heartbeat = metadata.last_heartbeat  # datetime of last heartbeat
```

### Event Broadcasting

6 event types for cross-runtime coordination:

```python
from kaizen.orchestration import RegistryEventType, RegistryEvent

# Define event callback
async def event_handler(event: RegistryEvent):
    print(f"Event: {event.event_type}")
    print(f"Agent ID: {event.agent_id}")
    print(f"Runtime ID: {event.runtime_id}")
    print(f"Metadata: {event.metadata}")

# Subscribe to specific events
registry.subscribe(RegistryEventType.AGENT_REGISTERED, event_handler)
registry.subscribe(RegistryEventType.AGENT_DEREGISTERED, event_handler)
registry.subscribe(RegistryEventType.AGENT_STATUS_CHANGED, event_handler)
registry.subscribe(RegistryEventType.AGENT_HEARTBEAT, event_handler)
registry.subscribe(RegistryEventType.RUNTIME_JOINED, event_handler)
registry.subscribe(RegistryEventType.RUNTIME_LEFT, event_handler)

# Perform operations - events broadcast automatically
agent_id = await registry.register_agent(agent, runtime_id="runtime_1")
# → AGENT_REGISTERED event broadcast
# → RUNTIME_JOINED event broadcast (if first agent from runtime)

await registry.update_agent_status(agent_id, AgentStatus.UNHEALTHY)
# → AGENT_STATUS_CHANGED event broadcast

await registry.update_agent_heartbeat(agent_id)
# → AGENT_HEARTBEAT event broadcast

await registry.deregister_agent(agent_id, runtime_id="runtime_1")
# → AGENT_DEREGISTERED event broadcast
# → RUNTIME_LEFT event broadcast (if last agent from runtime)
```

**Event Types**:
- **AGENT_REGISTERED**: Agent added to registry
- **AGENT_DEREGISTERED**: Agent removed from registry
- **AGENT_STATUS_CHANGED**: Agent status updated
- **AGENT_HEARTBEAT**: Agent sent heartbeat
- **RUNTIME_JOINED**: First agent from runtime registered
- **RUNTIME_LEFT**: Last agent from runtime deregistered

### Health Monitoring

Heartbeat-based health monitoring with automatic deregistration:

```python
# Send heartbeats to keep agents healthy
await registry.update_agent_heartbeat(agent_id)

# Update agent status manually
await registry.update_agent_status(agent_id, AgentStatus.ACTIVE)
await registry.update_agent_status(agent_id, AgentStatus.UNHEALTHY)
await registry.update_agent_status(agent_id, AgentStatus.DEGRADED)
await registry.update_agent_status(agent_id, AgentStatus.OFFLINE)

# Check agent health
metadata = registry.agents[agent_id]
status = metadata.status                 # AgentStatus
last_heartbeat = metadata.last_heartbeat  # datetime
```

**Health States**:
- **ACTIVE**: Agent is healthy and available
- **UNHEALTHY**: Agent failed health checks
- **DEGRADED**: Agent has partial functionality
- **OFFLINE**: Agent is disconnected

**Automatic Deregistration**:
1. Registry monitors agent heartbeats at configured intervals
2. Agents must send heartbeats within timeout window (30s default)
3. Missed heartbeats trigger status change to UNHEALTHY
4. Auto-deregistration occurs after extended timeout (60s default)
5. Unhealthy agents excluded from capability discovery (ACTIVE filter)
6. Recovery possible by updating status back to ACTIVE

## Production Patterns

### Pattern 1: Basic Distributed Coordination

Register agents from multiple runtimes and discover across distributed systems:

```python
# Register agents from runtime_1
code_id = await registry.register_agent(code_agent, runtime_id="runtime_1")
data_id = await registry.register_agent(data_agent, runtime_id="runtime_1")

# Register agent from runtime_2
writing_id = await registry.register_agent(writing_agent, runtime_id="runtime_2")

# Discover agents across all runtimes
code_agents = await registry.find_agents_by_capability("code generation")
# Returns agents from any runtime with matching capability

# Verify runtime distribution
assert len(registry.runtime_agents["runtime_1"]) == 2
assert len(registry.runtime_agents["runtime_2"]) == 1
```

**Use Case**: Distributed multi-agent systems spanning multiple processes or machines

**Cost**: $0 (uses Ollama llama3.2:1b)

**Example**: `examples/orchestration/agent-registry-patterns/1_basic_distributed_coordination.py`

### Pattern 2: Capability Discovery with Event Monitoring

Intelligent agent discovery using O(1) capability indexing with event-driven coordination:

```python
# Track events
events_received = []

async def event_monitor(event: RegistryEvent):
    events_received.append(event)
    print(f"[EVENT] {event.event_type.value}: {event.agent_id or event.runtime_id}")

# Subscribe to all events
registry.subscribe(RegistryEventType.AGENT_REGISTERED, event_monitor)
registry.subscribe(RegistryEventType.RUNTIME_JOINED, event_monitor)
registry.subscribe(RegistryEventType.AGENT_STATUS_CHANGED, event_monitor)

# Register specialized agents
python_id = await registry.register_agent(python_expert, runtime_id="dev_runtime_1")
js_id = await registry.register_agent(js_expert, runtime_id="dev_runtime_1")
data_id = await registry.register_agent(data_scientist, runtime_id="analytics_runtime_2")

# O(1) capability-based discovery
python_agents = await registry.find_agents_by_capability("python")
js_agents = await registry.find_agents_by_capability("javascript")
data_agents = await registry.find_agents_by_capability("data")

# Status-based filtering
active_python = await registry.find_agents_by_capability(
    "python",
    status_filter=AgentStatus.ACTIVE
)
```

**Use Case**: Large-scale multi-agent systems requiring intelligent agent selection

**Cost**: $0 (uses Ollama llama3.2:1b)

**Example**: `examples/orchestration/agent-registry-patterns/2_capability_discovery.py`

### Pattern 3: Fault Tolerance and Health Monitoring

Production-grade fault tolerance with health monitoring and recovery:

```python
# Configure aggressive health monitoring
config = AgentRegistryConfig(
    enable_heartbeat_monitoring=True,
    heartbeat_timeout=10.0,  # 10 seconds (aggressive)
    auto_deregister_timeout=20.0,  # 20 seconds
)

registry = AgentRegistry(config=config)
await registry.start()

# Register production agents
primary_id = await registry.register_agent(primary_agent, runtime_id="prod_runtime_1")
backup_id = await registry.register_agent(backup_agent, runtime_id="prod_runtime_2")

# Send heartbeats
await registry.update_agent_heartbeat(primary_id)
await registry.update_agent_heartbeat(backup_id)

# Simulate primary agent failure
await registry.update_agent_status(primary_id, AgentStatus.UNHEALTHY)

# Failover to healthy agents
healthy_agents = await registry.find_agents_by_capability(
    "task processing",
    status_filter=AgentStatus.ACTIVE  # Only backup_agent
)

# Route task to healthy agent
selected_agent = healthy_agents[0]
result = selected_agent.agent.run(task="Process critical task")

# Recover failed agent
await registry.update_agent_status(primary_id, AgentStatus.ACTIVE)

# Now both agents available
all_healthy = await registry.find_agents_by_capability(
    "task processing",
    status_filter=AgentStatus.ACTIVE  # Both agents
)
```

**Use Case**: Production multi-agent systems requiring high reliability

**Cost**: ~$0.01 (uses OpenAI gpt-5-nano-2025-08-07)

**Example**: `examples/orchestration/agent-registry-patterns/3_fault_tolerance.py`

## Best Practices

### Heartbeat Intervals

Choose appropriate heartbeat intervals based on workload:

- **Fast (10-30s)**: Critical systems requiring quick failure detection
- **Normal (30-60s)**: Standard production workloads
- **Slow (60-300s)**: Long-running agents with infrequent tasks

**Rule**: Set `auto_deregister_timeout` to 2-3x `heartbeat_timeout` to allow missed heartbeats before deregistration.

### Event Broadcasting

Enable event broadcasting for observability:

```python
config = AgentRegistryConfig(
    enable_event_broadcasting=True,
    event_queue_size=200,  # Increase for high-traffic systems
)
```

**Benefits**:
- Monitor agent health in real-time
- Track runtime joins/leaves
- Audit agent lifecycle events
- Debug distributed coordination issues

### Status-Based Routing

Always filter by ACTIVE status for production routing:

```python
# ✅ CORRECT - Only route to healthy agents
agents = await registry.find_agents_by_capability(
    "code generation",
    status_filter=AgentStatus.ACTIVE
)

# ❌ WRONG - May include unhealthy agents
agents = await registry.find_agents_by_capability(
    "code generation",
    status_filter=None
)
```

### Graceful Recovery

Implement graceful recovery patterns for failed agents:

```python
# Detect failures via events
async def health_monitor(event: RegistryEvent):
    if event.event_type == RegistryEventType.AGENT_STATUS_CHANGED:
        new_status = event.metadata.get("new_status")
        if new_status == AgentStatus.UNHEALTHY:
            # Route to healthy agents
            healthy = await registry.find_agents_by_capability(
                capability,
                status_filter=AgentStatus.ACTIVE
            )
            # Process with healthy agents

# Restore failed agents when recovered
await registry.update_agent_status(agent_id, AgentStatus.ACTIVE)
```

## Scaling Considerations

- **10-100 agents**: Single OrchestrationRuntime per process
- **100-1000 agents**: Single AgentRegistry across multiple runtimes
- **1000+ agents**: Multiple AgentRegistry instances with sharding

## Comparison with OrchestrationRuntime

### OrchestrationRuntime (10-100 agents)

**Scope**: Single-process multi-agent orchestration

**Features**:
- Semantic, round-robin, random task routing
- Agent-level health checks with real LLM inference
- Per-agent and runtime-wide budget tracking
- Task distribution within a single runtime

**Use Case**: Task distribution within a single runtime

### AgentRegistry (100+ agents)

**Scope**: Distributed multi-runtime coordination

**Features**:
- O(1) capability-based agent discovery
- Heartbeat monitoring with automatic deregistration
- Cross-runtime event broadcasting
- Centralized coordination across distributed systems

**Use Case**: Centralized coordination across distributed systems

### Integration

Use both together for distributed orchestration:

```python
# Create runtime for local orchestration
runtime = OrchestrationRuntime(config=runtime_config)

# Create registry for global coordination
registry = AgentRegistry(config=registry_config)

# Register agents in both
agent_id = await runtime.register_agent(agent)  # Runtime tracking
await registry.register_agent(agent, runtime_id="runtime_1")  # Global discovery

# Route tasks locally via runtime
selected_agent = await runtime.route_task(task, strategy=RoutingStrategy.SEMANTIC)

# Discover agents globally via registry
all_agents = await registry.find_agents_by_capability("code generation")
```

## When to Use AgentRegistry

Use AgentRegistry when you need:

- **100+ agent systems** requiring centralized coordination
- **Distributed deployments** across multiple processes/machines
- **Production fault tolerance** with health monitoring
- **Large-scale discovery** and dynamic task routing
- **Cross-runtime coordination** with event broadcasting

Don't use AgentRegistry when:

- **10-100 agents** in single process (use OrchestrationRuntime)
- **Simple workflows** without distribution (use Pipeline patterns)
- **No health monitoring** needed (use direct agent communication)

## Related Skills

- **[kaizen-supervisor-worker](kaizen-supervisor-worker.md)** - Supervisor-worker coordination
- **[kaizen-multi-agent-setup](kaizen-multi-agent-setup.md)** - Multi-agent system setup
- **[kaizen-a2a-protocol](kaizen-a2a-protocol.md)** - Agent-to-agent communication
- **[kaizen-observability-hooks](kaizen-observability-hooks.md)** - Event-driven observability

## Support

- **Examples**: `examples/orchestration/agent-registry-patterns/`
- **Tests**: `tests/e2e/orchestration/test_agent_registry_e2e.py`
- **Docs**: `docs/features/agent-registry.md` (TODO)
- **Source**: `src/kaizen/orchestration/registry.py`
