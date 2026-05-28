---
skill: nexus-architecture
description: How Nexus works internally - architecture overview, design principles, and implementation details
priority: MEDIUM
tags: [nexus, architecture, design, internal, overview]
---

# Nexus Architecture

Understanding how Nexus works internally.

## High-Level Architecture

```
┌─────────────────────────────────────────────────┐
│                  Nexus Platform                  │
│                                                  │
│  ┌──────────────────────────────────────────┐  │
│  │         Multi-Channel Layer              │  │
│  │  ┌──────┐  ┌──────┐  ┌──────┐          │  │
│  │  │ API  │  │ CLI  │  │ MCP  │          │  │
│  │  └──┬───┘  └──┬───┘  └──┬───┘          │  │
│  └─────┼─────────┼─────────┼──────────────┘  │
│        └─────────┴─────────┘                   │
│                  │                              │
│  ┌───────────────┴──────────────────────────┐  │
│  │        Session Manager & Router          │  │
│  │  - Unified sessions across channels      │  │
│  │  - Request routing and validation        │  │
│  │  - Event broadcasting                    │  │
│  └───────────────┬──────────────────────────┘  │
│                  │                              │
│  ┌───────────────┴──────────────────────────┐  │
│  │         Enterprise Gateway               │  │
│  │  - Authentication & Authorization        │  │
│  │  - Rate Limiting & Circuit Breaker       │  │
│  │  - Caching & Monitoring                  │  │
│  └───────────────┬──────────────────────────┘  │
│                  │                              │
├──────────────────┴──────────────────────────────┤
│              Kailash SDK Core                   │
│  - WorkflowBuilder & Runtime                    │
│  - 110+ Nodes                                   │
│  - Execution Engine                             │
└─────────────────────────────────────────────────┘
```

## Core Components

### 1. Multi-Channel Layer

**Purpose**: Expose workflows via API, CLI, and MCP

**Components**:
- **API Channel**: FastAPI-based REST server (via enterprise gateway)
- **CLI Channel**: Command-line interface (via enterprise gateway)
- **MCP Channel**: Model Context Protocol server (separate initialization)

**Key Features**:
- Single workflow registration via `Nexus.register()`
- Automatic endpoint generation through enterprise gateway
- Unified parameter handling

**v1.1.0 Implementation:**
```python
# Actual v1.1.0 architecture - NO ChannelManager class
class Nexus:
    def __init__(self):
        # Channels initialized by Nexus directly:
        self._initialize_gateway()        # API + CLI channels
        self._initialize_mcp_server()     # MCP channel

    def register(self, name, workflow):
        # Single registration → Multi-channel exposure
        self._gateway.register_workflow(name, workflow)  # API + CLI
        self._mcp_channel.register_workflow(name, workflow)  # MCP

        # All three channels now have the workflow
```

**What Changed from Stubs:**
- ❌ **REMOVED**: `ChannelManager.initialize_channels()` (was stub returning success)
- ❌ **REMOVED**: `ChannelManager.register_workflow_on_channels()` (was stub logging success)
- ✅ **REALITY**: Nexus handles initialization and registration directly

### 2. Session Manager

**Purpose**: Unified session management across channels

**Features**:
- Cross-channel session persistence
- State synchronization
- Session lifecycle management

```python
class SessionManager:
    def __init__(self, backend="redis"):
        self.backend = backend
        self.sessions = {}

    def create_session(self, channel, metadata):
        session_id = generate_id()
        self.sessions[session_id] = {
            "channel": channel,
            "metadata": metadata,
            "created_at": time.time(),
            "state": {}
        }
        return session_id

    def sync_session(self, session_id, target_channel):
        # Sync session state across channels
        session = self.sessions.get(session_id)
        if session:
            session["channel"] = target_channel
            return session
```

### 3. Enterprise Gateway

**Purpose**: Production-grade features

**Components**:
- **Authentication**: OAuth2, JWT, API keys
- **Authorization**: RBAC, permissions
- **Rate Limiting**: Per-user, per-endpoint
- **Circuit Breaker**: Failure handling
- **Caching**: Response caching
- **Monitoring**: Metrics and tracing

```python
class EnterpriseGateway:
    def __init__(self):
        self.auth = AuthenticationManager()
        self.rate_limiter = RateLimiter()
        self.circuit_breaker = CircuitBreaker()
        self.cache = CacheManager()
        self.monitor = MonitoringManager()

    def process_request(self, request):
        # Authentication
        user = self.auth.authenticate(request)

        # Authorization
        if not self.auth.authorize(user, request.workflow):
            raise UnauthorizedError()

        # Rate limiting
        if not self.rate_limiter.check(user):
            raise RateLimitError()

        # Circuit breaker
        if self.circuit_breaker.is_open(request.workflow):
            raise ServiceUnavailableError()

        # Check cache
        cached = self.cache.get(request)
        if cached:
            return cached

        # Execute workflow
        result = self.execute_workflow(request)

        # Cache result
        self.cache.set(request, result)

        # Monitor
        self.monitor.record_request(request, result)

        return result
```

### 4. Workflow Registry

**Purpose**: Manage registered workflows

```python
class WorkflowRegistry:
    def __init__(self):
        self.workflows = {}
        self.metadata = {}

    def register(self, name, workflow, metadata=None):
        self.workflows[name] = workflow
        self.metadata[name] = metadata or {}

    def get(self, name):
        return self.workflows.get(name)

    def list(self):
        return list(self.workflows.keys())

    def get_metadata(self, name):
        return self.metadata.get(name, {})
```

## Design Principles

### 1. Zero Configuration

**Goal**: Work out-of-the-box with no config

```python
# Just works
app = Nexus()
app.start()
```

**Implementation**:
- Smart defaults for all settings
- Auto-detection of environment
- Graceful fallbacks

### 2. Progressive Enhancement

**Goal**: Start simple, add features as needed

```python
# Start simple
app = Nexus()

# Add features progressively
app.enable_auth = True
app.enable_monitoring = True
app.rate_limit = 1000
```

**Implementation**:
- Feature flags for all components
- Lazy initialization
- Optional dependencies

### 3. Multi-Channel Orchestration

**Goal**: Single source, multiple interfaces

**Implementation**:
- Abstract workflow execution layer
- Channel-agnostic request handling
- Unified response formatting

### 4. Built on Core SDK

**Goal**: Leverage existing Kailash SDK

**Benefits**:
- No SDK modification needed
- All 110+ nodes available
- Proven execution engine

```python
# Nexus uses Kailash SDK underneath
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import LocalRuntime

# Build workflow with SDK
workflow = WorkflowBuilder()
workflow.add_node("PythonCodeNode", "test", {...})

# Nexus registers and exposes it
app.register("test", workflow.build())
```

## Request Flow (v1.1.0)

### API Request Flow

```
1. Client sends HTTP POST to /workflows/name/execute
   ↓
2. Enterprise Gateway receives request (FastAPI)
   ↓
3. Gateway processes (built-in):
   - Authentication (if enabled)
   - Rate limiting (if configured)
   - Request validation
   ↓
4. Gateway retrieves workflow from registry
   ↓
5. Kailash Runtime executes workflow
   ↓
6. Gateway formats response
   ↓
7. Monitoring records metrics (if enabled)
   ↓
8. Response returned to client

NOTE: Session management uses lazy initialization (v1.1 planned feature)
NOTE: Response caching is optional (enable_durability flag)
```

### CLI Request Flow

```
1. User executes: nexus run workflow-name --param value
   ↓
2. CLI Channel parses arguments
   ↓
3. Converts to workflow request format
   ↓
4. Routes through Enterprise Gateway
   ↓
5. Workflow executed via Runtime
   ↓
6. Output formatted for terminal
   ↓
7. Displayed to user
```

### MCP Request Flow

```
1. AI agent discovers tools via MCP
   ↓
2. Agent calls tool with parameters
   ↓
3. MCP Channel receives request
   ↓
4. Routes through Enterprise Gateway
   ↓
5. Workflow executed
   ↓
6. Result formatted for AI consumption
   ↓
7. Returned to agent
```

## Parameter Broadcasting

```python
# How inputs flow to nodes
class ParameterBroadcaster:
    def broadcast_inputs(self, workflow, inputs):
        """
        Broadcast API inputs to ALL nodes in workflow
        Each node receives the full inputs dict
        """
        parameters = inputs  # inputs → parameters

        for node in workflow.nodes:
            # Each node gets full parameters
            node_params = {**node.config, **parameters}
            node.execute(node_params)
```

## Key Implementation Details

### Auto-Discovery

```python
class WorkflowDiscovery:
    PATTERNS = [
        "workflows/*.py",
        "*.workflow.py",
        "workflow_*.py",
        "*_workflow.py"
    ]

    def discover(self, paths):
        workflows = []
        for pattern in self.PATTERNS:
            for path in paths:
                workflows.extend(glob.glob(f"{path}/{pattern}"))
        return workflows

    def load_workflow(self, file_path):
        # Dynamic import
        spec = importlib.util.spec_from_file_location("module", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, 'workflow'):
            return module.workflow
```

### Health Checking

```python
class HealthChecker:
    def __init__(self):
        self.checks = {}

    def register_check(self, name, check_func):
        self.checks[name] = check_func

    def check_all(self):
        results = {}
        for name, check in self.checks.items():
            try:
                results[name] = check()
            except Exception as e:
                results[name] = {"status": "unhealthy", "error": str(e)}

        overall = "healthy" if all(
            r.get("status") == "healthy" for r in results.values()
        ) else "unhealthy"

        return {
            "status": overall,
            "components": results
        }
```

## Performance Optimizations

### 1. Connection Pooling

```python
# Database connections
pool = ConnectionPool(
    min_connections=5,
    max_connections=20,
    timeout=30
)
```

### 2. Response Caching

```python
# Cache expensive workflows
cache.set(
    key=f"workflow:{name}:{hash(inputs)}",
    value=result,
    ttl=300
)
```

### 3. Async Execution

```python
# Use async runtime for Docker/FastAPI
from kailash.runtime import AsyncLocalRuntime

runtime = AsyncLocalRuntime()
result = await runtime.execute_workflow_async(workflow, inputs)
```

## Key Takeaways (v1.1.0)

- **Multi-layer architecture**: Nexus → Enterprise Gateway → Kailash SDK
- **Zero-configuration**: `Nexus()` with smart defaults
- **Built on Kailash SDK**: Leverages proven workflow execution
- **Single registration path**: `Nexus.register()` handles all channels
- **Enterprise gateway integration**: FastAPI-based with multi-channel support
- **Parameter broadcasting**: Inputs broadcast to all nodes via runtime
- **v1.0 vs v1.1 features**: Event logging (v1.0) vs real-time broadcasting (v1.1)

**What's Real in v1.1.0:**
- ✅ Multi-channel exposure (API, CLI, MCP)
- ✅ Workflow registration and execution
- ✅ Custom REST endpoints with rate limiting
- ✅ Health monitoring and metrics
- ✅ Event logging (retrieve with `get_events()`)

**Planned for v1.1:**
- 🔜 Real-time event broadcasting (WebSocket/SSE)
- 🔜 Automatic workflow schema inference
- 🔜 Cross-channel session synchronization

## Related Skills

- [nexus-quickstart](#) - Get started quickly
- [nexus-multi-channel](#) - Multi-channel deep dive
- [nexus-enterprise-features](#) - Enterprise components
- [nexus-production-deployment](#) - Deploy architecture
