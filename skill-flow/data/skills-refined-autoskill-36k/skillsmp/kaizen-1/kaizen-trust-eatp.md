# Enterprise Agent Trust Protocol (EATP) - v0.8.0

**Cryptographically verifiable trust chains for AI agents**, enabling enterprise-grade accountability, authorization, and secure multi-agent communication.

## Overview

EATP provides complete trust infrastructure for AI agents:

- **Trust Lineage Chains**: Cryptographically linked chain of genesis, capabilities, delegations, and audit anchors
- **TrustedAgent**: BaseAgent extension with built-in trust verification
- **Agent Registry**: Capability-based discovery with health monitoring
- **Secure Messaging**: End-to-end encrypted, replay-protected agent communication
- **Trust-Aware Orchestration**: Workflow runtime with trust context propagation
- **Enterprise System Agent (ESA)**: Proxy agents for legacy systems
- **A2A HTTP Service**: REST/JSON-RPC API for trust operations

**Location**: `kaizen.trust` module

## Quick Start

### Basic Trust Establishment

```python
from kaizen.trust import (
    TrustOperations,
    PostgresTrustStore,
    OrganizationalAuthorityRegistry,
    TrustKeyManager,
    CapabilityRequest,
    CapabilityType,
)

# Initialize trust components
store = PostgresTrustStore(connection_string="postgresql://...")
registry = OrganizationalAuthorityRegistry()
key_manager = TrustKeyManager()
trust_ops = TrustOperations(registry, key_manager, store)
await trust_ops.initialize()

# Establish trust for an agent
chain = await trust_ops.establish(
    agent_id="agent-001",
    authority_id="org-acme",
    capabilities=[
        CapabilityRequest(
            capability="analyze_data",
            capability_type=CapabilityType.ACCESS,
        )
    ],
)

# Verify trust before action
result = await trust_ops.verify(
    agent_id="agent-001",
    action="analyze_data",
)

if result.valid:
    # Proceed with action
    print(f"Verification level: {result.level}")
```

### Human Traceability (v0.8.0)

Every action MUST be traceable to a human. PseudoAgents bridge human authentication to the agentic world.

```python
from kaizen.trust.execution_context import HumanOrigin, ExecutionContext
from kaizen.trust.pseudo_agent import PseudoAgent, PseudoAgentFactory, PseudoAgentConfig
from datetime import datetime

# Factory creates PseudoAgents from auth sources
factory = PseudoAgentFactory(
    trust_operations=trust_ops,
    default_config=PseudoAgentConfig(
        session_timeout_minutes=60,
        require_mfa=True,
        allowed_capabilities=["read_data", "process_data"],
    ),
)

# Create from session/JWT/HTTP headers
pseudo = factory.from_session(
    user_id="user-123",
    email="alice@corp.com",
    display_name="Alice Chen",
    session_id="sess-456",
    auth_provider="okta",
)

# Delegate to agent (ONLY way trust enters the system)
delegation, agent_ctx = await pseudo.delegate_to(
    agent_id="invoice-processor",
    task_id="november-invoices",
    capabilities=["read_invoices", "process_invoices"],
    constraints={"cost_limit": 1000},
)

# Agent executes with delegated context
result = await agent.execute_async(inputs, context=agent_ctx)

# Access human origin in context
print(f"Authorized by: {agent_ctx.human_origin.display_name}")
print(f"Delegation depth: {agent_ctx.delegation_depth}")

# Revoke when human logs out
await pseudo.revoke_all_delegations()
```

**Key Components**:
- **HumanOrigin**: Immutable (frozen=True) record of the authorizing human
- **ExecutionContext**: Context propagation via ContextVar for async operations
- **PseudoAgent**: Human facade - ONLY entity that can initiate trust chains
- **ConstraintValidator**: Validates constraint tightening (can only REDUCE permissions)

### TrustedAgent Usage

```python
from kaizen.trust import (
    TrustedAgent,
    TrustedAgentConfig,
    TrustOperations,
)
from kaizen.signatures import Signature, InputField, OutputField

class AnalyzeSignature(Signature):
    data: str = InputField(description="Data to analyze")
    result: str = OutputField(description="Analysis result")

# Create TrustedAgent (inherits from BaseAgent)
config = TrustedAgentConfig(
    agent_id="analyzer-001",
    authority_id="org-acme",
    capabilities=["analyze_data", "generate_reports"],
)

agent = TrustedAgent(
    config=config,
    trust_operations=trust_ops,
    signature=AnalyzeSignature(),
)

# Trust establishment happens automatically
await agent.establish_trust()

# Run with trust verification
result = await agent.run(data="sales data...")
# Trust context automatically propagated
```

### TrustedSupervisorAgent for Delegation

```python
from kaizen.trust import TrustedSupervisorAgent, TrustedAgent

# Supervisor delegates to workers
supervisor = TrustedSupervisorAgent(
    config=supervisor_config,
    trust_operations=trust_ops,
)

# Delegate capability to worker
await supervisor.delegate_to_worker(
    worker_agent=worker,
    capability="process_data",
    constraints={"max_records": 1000},
    duration_hours=24,
)

# Worker now has delegated capability
result = await worker.run(data=input_data)
```

## Core Concepts

### Trust Lineage Chain

A complete trust chain for an agent containing:

```python
from kaizen.trust import TrustLineageChain, GenesisRecord, CapabilityAttestation

# TrustLineageChain structure
chain = TrustLineageChain(
    agent_id="agent-001",
    genesis=GenesisRecord(
        agent_id="agent-001",
        authority_id="org-acme",
        authority_type=AuthorityType.ORGANIZATIONAL,
        timestamp=datetime.utcnow(),
        public_key=public_key,
        signature=signature,
    ),
    capabilities=[
        CapabilityAttestation(
            capability="analyze_data",
            capability_type=CapabilityType.ACCESS,
            attestor_id="org-acme",
            timestamp=datetime.utcnow(),
            signature=signature,
        )
    ],
    delegations=[],  # DelegationRecord list
    audit_anchors=[],  # AuditAnchor list
)
```

**Key Components**:
- **GenesisRecord**: Initial trust establishment (who created this agent)
- **CapabilityAttestation**: Attested capabilities (what can it do)
- **DelegationRecord**: Delegated capabilities from other agents
- **AuditAnchor**: Cryptographic proof of actions taken

### Trust Operations

Four core operations: ESTABLISH, DELEGATE, VERIFY, AUDIT

```python
from kaizen.trust import TrustOperations

# ESTABLISH - Create trust chain for new agent
chain = await trust_ops.establish(
    agent_id="agent-001",
    authority_id="org-acme",
    capabilities=[CapabilityRequest(capability="analyze", capability_type=CapabilityType.ACCESS)],
)

# DELEGATE - Grant capability from one agent to another
delegation = await trust_ops.delegate(
    from_agent_id="supervisor-001",
    to_agent_id="worker-001",
    capability="process_data",
    constraints={"max_records": 100},
    duration_hours=24,
)

# VERIFY - Check if agent can perform action
result = await trust_ops.verify(
    agent_id="agent-001",
    action="analyze_data",
)

# AUDIT - Record action for compliance
await trust_ops.audit(
    agent_id="agent-001",
    action="analyze_data",
    result=ActionResult.SUCCESS,
    metadata={"records_processed": 500},
)
```

### Agent Registry

Capability-based discovery with health monitoring:

```python
from kaizen.trust import (
    AgentRegistry,
    AgentHealthMonitor,
    DiscoveryQuery,
    AgentStatus,
    PostgresAgentRegistryStore,
)

# Initialize registry
store = PostgresAgentRegistryStore(connection_string="postgresql://...")
registry = AgentRegistry(store=store)

# Register agents
await registry.register(
    agent_id="analyzer-001",
    capabilities=["analyze_data", "generate_reports"],
    metadata={"version": "1.0", "owner": "data-team"},
)

# Discover agents by capability
agents = await registry.discover(
    DiscoveryQuery(
        capability="analyze_data",
        status=AgentStatus.ACTIVE,
    )
)

# Health monitoring
monitor = AgentHealthMonitor(registry=registry)
await monitor.start()

# Update agent health
await registry.update_status("analyzer-001", AgentStatus.ACTIVE)
await registry.heartbeat("analyzer-001")
```

### Secure Messaging

End-to-end encrypted, replay-protected communication:

```python
from kaizen.trust import (
    SecureChannel,
    MessageSigner,
    MessageVerifier,
    InMemoryReplayProtection,
)

# Create secure channel between agents
channel = SecureChannel(
    sender_id="agent-001",
    receiver_id="agent-002",
    signer=MessageSigner(private_key=sender_private_key),
    verifier=MessageVerifier(public_keys={"agent-001": sender_public_key}),
    replay_protection=InMemoryReplayProtection(),
)

# Send encrypted message
envelope = await channel.send(
    payload={"task": "analyze", "data": "..."},
)

# Receive and verify message
result = await channel.receive(envelope)
if result.valid:
    payload = result.payload
```

**SecureMessageEnvelope Structure**:
- HMAC-based message authentication
- Nonce-based replay protection
- Timestamp validation
- Sender/receiver verification

### Trust-Aware Orchestration

Workflow runtime with trust context propagation:

```python
from kaizen.trust import (
    TrustAwareOrchestrationRuntime,
    TrustAwareRuntimeConfig,
    TrustExecutionContext,
    TrustPolicyEngine,
    TrustPolicy,
    PolicyType,
)

# Configure trust-aware runtime
config = TrustAwareRuntimeConfig(
    verify_on_execute=True,  # Verify trust before each execution
    propagate_context=True,  # Propagate trust context through workflow
    enforce_policies=True,   # Enforce trust policies
)

# Create policy engine
policy_engine = TrustPolicyEngine()
policy_engine.add_policy(TrustPolicy(
    name="require-active-agents",
    policy_type=PolicyType.CAPABILITY,
    rule=lambda ctx: ctx.agent_status == AgentStatus.ACTIVE,
))

# Create trust-aware runtime
runtime = TrustAwareOrchestrationRuntime(
    trust_operations=trust_ops,
    policy_engine=policy_engine,
    config=config,
)

# Execute with trust context
context = TrustExecutionContext(
    agent_id="agent-001",
    capabilities=["analyze_data"],
    delegation_chain=[],
)

result = await runtime.execute(
    workflow=my_workflow,
    context=context,
)
```

### Enterprise System Agent (ESA)

Proxy agents for legacy systems:

```python
from kaizen.trust import (
    EnterpriseSystemAgent,
    ESAConfig,
    SystemMetadata,
    SystemConnectionInfo,
    CapabilityMetadata,
)

# Configure ESA for legacy system
config = ESAConfig(
    system_id="erp-system",
    system_metadata=SystemMetadata(
        name="Enterprise ERP",
        version="5.2",
        vendor="SAP",
    ),
    connection_info=SystemConnectionInfo(
        protocol="https",
        host="erp.company.com",
        port=443,
    ),
    capabilities=[
        CapabilityMetadata(
            name="get_inventory",
            description="Retrieve inventory levels",
            parameters={"warehouse_id": "string"},
        ),
    ],
)

# Create ESA
esa = EnterpriseSystemAgent(
    config=config,
    trust_operations=trust_ops,
)

# Establish trust for ESA
await esa.establish_trust(authority_id="org-acme")

# Execute operation through ESA
result = await esa.execute(
    operation="get_inventory",
    parameters={"warehouse_id": "WH-001"},
)
```

**ESA Use Cases**:
- Wrap legacy APIs with trust verification
- Bridge non-AI systems into agent ecosystem
- Provide accountability for external system calls

### A2A HTTP Service

REST/JSON-RPC API for trust operations:

```python
from kaizen.trust import create_a2a_app, A2AService, AgentCardGenerator

# Create A2A service
service = A2AService(
    trust_operations=trust_ops,
    agent_registry=registry,
)

# Generate agent cards
card_generator = AgentCardGenerator(trust_operations=trust_ops)
card = await card_generator.generate("agent-001")

# Create FastAPI app
app = create_a2a_app(service)

# Run server
# uvicorn app:app --host 0.0.0.0 --port 8000
```

**Available Endpoints**:
- `POST /a2a/verify` - Verify agent trust
- `POST /a2a/delegate` - Delegate capability
- `GET /a2a/card/{agent_id}` - Get agent card
- `POST /a2a/audit/query` - Query audit trail

**JSON-RPC Methods**:
- `trust.verify` - Verify trust
- `trust.delegate` - Delegate capability
- `trust.audit` - Record audit event
- `agent.card` - Get agent card

## Security Features

### Credential Rotation

```python
from kaizen.trust import CredentialRotationManager, RotationStatus

# Configure rotation manager
rotation_manager = CredentialRotationManager(
    key_manager=key_manager,
    trust_store=store,
)

# Schedule automatic rotation
await rotation_manager.schedule_rotation(
    agent_id="agent-001",
    interval_days=30,
)

# Manual rotation
result = await rotation_manager.rotate("agent-001")
if result.status == RotationStatus.SUCCESS:
    print(f"New key fingerprint: {result.new_key_fingerprint}")
```

### Rate Limiting

```python
from kaizen.trust import TrustRateLimiter, RateLimitExceededError

# Configure rate limiter
rate_limiter = TrustRateLimiter(
    max_verifications_per_minute=100,
    max_delegations_per_hour=10,
)

# Check rate limit
try:
    await rate_limiter.check("verify", agent_id="agent-001")
except RateLimitExceededError:
    print("Rate limit exceeded")
```

### Security Audit Logging

```python
from kaizen.trust import (
    SecurityAuditLogger,
    SecurityEvent,
    SecurityEventType,
    SecurityEventSeverity,
)

# Configure audit logger
audit_logger = SecurityAuditLogger(output="security.log")

# Log security events
await audit_logger.log(SecurityEvent(
    event_type=SecurityEventType.VERIFICATION_FAILED,
    severity=SecurityEventSeverity.WARNING,
    agent_id="agent-001",
    details={"reason": "capability not found"},
))
```

## Component Reference

| Component | Purpose | Location |
|-----------|---------|----------|
| `TrustLineageChain` | Complete trust chain | `kaizen.trust.chain` |
| `TrustOperations` | Core trust operations | `kaizen.trust.operations` |
| `TrustedAgent` | BaseAgent with trust | `kaizen.trust.trusted_agent` |
| `TrustedSupervisorAgent` | Delegation support | `kaizen.trust.trusted_agent` |
| `AgentRegistry` | Agent discovery | `kaizen.trust.registry` |
| `AgentHealthMonitor` | Health monitoring | `kaizen.trust.registry` |
| `SecureChannel` | Encrypted messaging | `kaizen.trust.messaging` |
| `MessageSigner/Verifier` | Message auth | `kaizen.trust.messaging` |
| `TrustExecutionContext` | Context propagation | `kaizen.trust.orchestration` |
| `TrustPolicyEngine` | Policy enforcement | `kaizen.trust.orchestration` |
| `TrustAwareOrchestrationRuntime` | Trust-aware runtime | `kaizen.trust.orchestration` |
| `EnterpriseSystemAgent` | Legacy system proxy | `kaizen.trust.esa` |
| `A2AService` | HTTP API | `kaizen.trust.a2a` |
| `CredentialRotationManager` | Key rotation | `kaizen.trust.rotation` |
| `TrustRateLimiter` | Rate limiting | `kaizen.trust.security` |
| `SecurityAuditLogger` | Audit logging | `kaizen.trust.security` |
| `PostgresTrustStore` | Persistent storage | `kaizen.trust.store` |
| `TrustChainCache` | Performance caching | `kaizen.trust.cache` |
| `HumanOrigin` | Immutable human record (v0.8.0) | `kaizen.trust.execution_context` |
| `ExecutionContext` | Human traceability context (v0.8.0) | `kaizen.trust.execution_context` |
| `PseudoAgent` | Human facade (v0.8.0) | `kaizen.trust.pseudo_agent` |
| `PseudoAgentFactory` | Create PseudoAgents (v0.8.0) | `kaizen.trust.pseudo_agent` |
| `ConstraintValidator` | Constraint tightening (v0.8.0) | `kaizen.trust.constraint_validator` |
| `EATPMigration` | DB migration for v0.8.0 | `kaizen.trust.migrations` |

## When to Use EATP

**Use EATP when you need**:
- Enterprise-grade accountability for AI agents
- Regulatory compliance (audit trails, provenance)
- Cross-organization agent coordination
- Secure agent-to-agent communication
- Capability-based access control
- Trust delegation with constraints

**Don't use EATP when**:
- Simple single-agent applications
- Internal-only prototypes
- No compliance requirements
- Performance-critical paths without trust needs

## Best Practices

### Trust Establishment
- ✅ Establish trust before first agent action
- ✅ Use specific capability types (ACCESS, EXECUTE, DELEGATE)
- ✅ Set appropriate constraints on capabilities
- ❌ Never skip trust verification in production

### Delegation
- ✅ Use time-limited delegations
- ✅ Apply principle of least privilege
- ✅ Record delegation chain for audit
- ❌ Never delegate more capabilities than needed

### Secure Messaging
- ✅ Always use SecureChannel for inter-agent communication
- ✅ Enable replay protection
- ✅ Verify message signatures
- ❌ Never send sensitive data without encryption

### Production Deployment
- ✅ Use PostgresTrustStore for persistence
- ✅ Enable TrustChainCache for performance
- ✅ Configure credential rotation
- ✅ Enable security audit logging
- ❌ Never disable trust verification in production

## Related Skills

- **[kaizen-agent-registry](kaizen-agent-registry.md)** - Distributed agent coordination (non-trust)
- **[kaizen-a2a-protocol](kaizen-a2a-protocol.md)** - Basic A2A capability cards
- **[kaizen-supervisor-worker](kaizen-supervisor-worker.md)** - Supervisor-worker patterns
- **[kaizen-observability-audit](kaizen-observability-audit.md)** - Compliance audit trails

## Support

- **Source**: `src/kaizen/trust/`
- **Tests**: `tests/unit/trust/`, `tests/integration/trust/`, `tests/e2e/trust/`
- **Examples**: `examples/trust/` (see EATP examples)
