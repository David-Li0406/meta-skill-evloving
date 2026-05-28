# Kaizen Checkpoint & Resume System

**Available in**: Autonomous agents
**Complexity**: Low
**Use Case**: Long-running agents, failure recovery, pause/resume workflows

---

## Quick Reference

```python
from kaizen.agents.autonomous.base import BaseAutonomousAgent, AutonomousConfig
from kaizen.core.autonomy.state.storage import FilesystemStorage
from kaizen.core.autonomy.state.manager import StateManager

# Configure with automatic checkpointing
config = AutonomousConfig(
    max_cycles=10,
    checkpoint_frequency=5,  # Save every 5 steps
    resume_from_checkpoint=True,  # Resume on restart
    llm_provider="ollama",
    model="llama3.2",
)

# Create state manager
storage = FilesystemStorage(
    base_dir=".kaizen/checkpoints",
    compress=True  # Enable gzip compression (>50% size reduction)
)
state_manager = StateManager(
    storage=storage,
    checkpoint_frequency=5,
    retention_count=10  # Keep only latest 10 checkpoints
)

# Create agent with checkpointing
agent = BaseAutonomousAgent(
    config=config,
    signature=TaskSignature(),
    state_manager=state_manager,
)

# Run with automatic checkpointing and resume
result = await agent._autonomous_loop("Perform a complex task")
```

---

## Core Features

### Automatic Checkpointing

**Save state every N steps**:
```python
config = AutonomousConfig(
    checkpoint_frequency=5,  # Save every 5 steps
)
```

**Save state every M seconds**:
```python
state_manager = StateManager(
    storage=storage,
    checkpoint_interval=30.0,  # Save every 30 seconds
)
```

**Hybrid (OR logic)**:
```python
# Checkpoint every 5 steps OR every 30 seconds (whichever comes first)
config = AutonomousConfig(checkpoint_frequency=5)
state_manager = StateManager(checkpoint_interval=30.0)
```

### Resume from Checkpoint

**Enable resume**:
```python
config = AutonomousConfig(
    resume_from_checkpoint=True,  # Load latest checkpoint on start
)

# Agent automatically loads latest checkpoint for agent_id
# If no checkpoint found, starts fresh
result = await agent._autonomous_loop("Continue task")
```

**How it works**:
1. Agent checks for latest checkpoint matching agent_id
2. If found, restores complete state (step, memory, plan, budget)
3. Continues execution from interruption point
4. If not found, starts fresh execution

### Compression

**Enable compression** to reduce storage by >50%:
```python
storage = FilesystemStorage(
    base_dir=".kaizen/checkpoints",
    compress=True  # gzip compression
)
```

**Performance**:
- Compression ratio: >50% size reduction
- Overhead: <10ms per checkpoint
- Auto-decompression: Transparent on load
- Backward compatible: Handles both compressed and uncompressed

### Retention Policy

**Keep only latest N checkpoints**:
```python
state_manager = StateManager(
    storage=storage,
    retention_count=10,  # Keep only 10 most recent
)
```

**Behavior**:
- Oldest checkpoints deleted automatically after each save
- Deletion is non-blocking (errors logged but don't fail saves)
- Per-agent enforcement (each agent_id has own retention)

---

## Hook Integration

### PRE_CHECKPOINT_SAVE Hook

**Triggered before checkpoint save**:
```python
from kaizen.core.autonomy.hooks import HookManager, HookEvent, HookResult

hook_manager = HookManager()

async def pre_checkpoint_hook(context):
    """Validate or modify state before save"""
    agent_id = context.data.get("agent_id")
    step = context.data.get("step_number")
    print(f"About to save checkpoint for {agent_id} at step {step}")
    return HookResult(success=True)

hook_manager.register(HookEvent.PRE_CHECKPOINT_SAVE, pre_checkpoint_hook)

state_manager = StateManager(storage=storage, hook_manager=hook_manager)
```

### POST_CHECKPOINT_SAVE Hook

**Triggered after checkpoint save**:
```python
async def post_checkpoint_hook(context):
    """Log or notify after checkpoint save"""
    checkpoint_id = context.data.get("checkpoint_id")
    step = context.data.get("step_number")
    print(f"Saved checkpoint {checkpoint_id} at step {step}")
    return HookResult(success=True)

hook_manager.register(HookEvent.POST_CHECKPOINT_SAVE, post_checkpoint_hook)
```

**Available in context.data**:
- `agent_id`: Agent identifier
- `step_number`: Current step
- `status`: Agent status ("running", "completed", "failed")
- `checkpoint_id`: Checkpoint ID (POST hook only)
- `timestamp`: Checkpoint timestamp

---

## Storage Configuration

### Filesystem Storage (Default)

```python
from kaizen.core.autonomy.state.storage import FilesystemStorage

storage = FilesystemStorage(
    base_dir=".kaizen/checkpoints",  # Checkpoint directory
    compress=True  # Enable compression
)
```

**File format**: JSONL (one checkpoint per line)
**Compression**: Optional gzip
**Location**: `.kaizen/checkpoints/{agent_id}/{timestamp}.jsonl[.gz]`

---

## Common Patterns

### Long-Running Autonomous Agent

```python
from kaizen.agents.autonomous.base import BaseAutonomousAgent, AutonomousConfig

config = AutonomousConfig(
    max_cycles=50,  # Long-running
    checkpoint_frequency=5,  # Checkpoint every 5 steps
    resume_from_checkpoint=True,  # Resume on restart
)

storage = FilesystemStorage(compress=True)
state_manager = StateManager(
    storage=storage,
    checkpoint_frequency=5,
    retention_count=10  # Keep latest 10
)

agent = BaseAutonomousAgent(
    config=config,
    signature=signature,
    state_manager=state_manager,
)

# Runs with automatic checkpointing
# Resumes automatically if interrupted
result = await agent._autonomous_loop("Complex long-running task")
```

### Development with Quick Iterations

```python
# Frequent checkpoints for debugging
config = AutonomousConfig(
    max_cycles=10,
    checkpoint_frequency=1,  # Checkpoint every step
    resume_from_checkpoint=True,
)

storage = FilesystemStorage(compress=False)  # Disable compression for speed
state_manager = StateManager(
    storage=storage,
    checkpoint_frequency=1,
    retention_count=5  # Keep only 5 recent
)
```

### Production with Error Recovery

```python
# Balance between performance and safety
config = AutonomousConfig(
    max_cycles=100,
    checkpoint_frequency=10,  # Every 10 steps
    checkpoint_interval_seconds=300.0,  # OR every 5 minutes
    resume_from_checkpoint=True,
)

storage = FilesystemStorage(compress=True)  # Compression for storage efficiency
state_manager = StateManager(
    storage=storage,
    checkpoint_frequency=10,
    checkpoint_interval=300.0,
    retention_count=20  # Keep 20 checkpoints for safety
)
```

---

## State Captured

**Complete agent state** is captured in each checkpoint:

- **Step number**: Current execution step
- **Conversation history**: All interactions
- **Memory**: Agent memory entries
- **Plan**: Current plan (if planning enabled)
- **Budget**: Cost tracking information
- **Status**: Agent status ("running", "completed", "failed")
- **Metadata**: Additional context

---

## Use Cases

### Long-Running Agents (30+ hour sessions)
- Checkpoint every 10 minutes
- Resume automatically on restart
- Prevent data loss from system failures

### Development Testing
- Checkpoint every step
- Quick iteration cycles
- Debug from specific states

### Production Autonomous Agents
- Balance checkpointing frequency with performance
- Enable compression for storage efficiency
- Retention policy to prevent storage bloat

### Cost Optimization
- Avoid repeating expensive operations
- Resume from checkpoint instead of restarting
- Save checkpoint before high-cost operations

---

## Performance

### Checkpoint Performance
- **Save**: 5-10ms (uncompressed), 8-15ms (compressed)
- **Load**: 2-5ms (uncompressed), 3-7ms (compressed)
- **Compression overhead**: <5ms (acceptable for >50% size reduction)

### Storage Efficiency
- **Typical checkpoint**: 500-2000 bytes uncompressed
- **After compression**: 200-800 bytes (>50% reduction)
- **100 checkpoints**: ~100KB uncompressed, ~40KB compressed

---

## Troubleshooting

### Checkpoint Not Saving

**Problem**: Agent runs but no checkpoints created

**Solutions**:
1. Check state_manager is provided: `agent = BaseAutonomousAgent(..., state_manager=state_manager)`
2. Verify checkpoint_frequency is set: `config = AutonomousConfig(checkpoint_frequency=5)`
3. Check storage directory exists and is writable

### Resume Not Working

**Problem**: Agent starts fresh instead of resuming

**Solutions**:
1. Enable resume: `config = AutonomousConfig(resume_from_checkpoint=True)`
2. Verify checkpoint files exist in storage directory
3. Check agent_id matches (default is "autonomous_agent")
4. Ensure checkpoint is not corrupted (check file size > 0)

### Storage Growing Too Large

**Problem**: Checkpoint directory size increasing

**Solutions**:
1. Enable compression: `storage = FilesystemStorage(compress=True)`
2. Set retention policy: `state_manager = StateManager(retention_count=10)`
3. Reduce checkpoint frequency: `config = AutonomousConfig(checkpoint_frequency=10)`

---

## Reference

**Documentation**: `docs/features/checkpoint-resume-system.md`
**Source**: `src/kaizen/agents/autonomous/base.py:192` (state capture/restore)
**Tests**: `tests/unit/agents/autonomous/test_auto_checkpoint.py` (114 tests passing)
**Storage**: `src/kaizen/core/autonomy/state/storage.py`
**Manager**: `src/kaizen/core/autonomy/state/manager.py`

---

## Related Skills

- **[kaizen-observability](kaizen-observability.md)** - Monitoring and tracing
- **[kaizen-memory-system](kaizen-memory-system.md)** - Agent memory patterns
- **[kaizen-testing-patterns](kaizen-testing-patterns.md)** - Testing checkpoint functionality
