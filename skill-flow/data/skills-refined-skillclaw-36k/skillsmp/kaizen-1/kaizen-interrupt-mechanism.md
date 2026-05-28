---
name: kaizen-interrupt-mechanism
description: "Kaizen interrupt mechanism for graceful shutdown - Ctrl+C handling, timeout/budget auto-stop, checkpoint preservation. Use when asking about 'interrupt mechanism', 'graceful shutdown', 'Ctrl+C handling', 'timeout handler', 'budget handler', 'signal handling', 'SIGINT', 'interrupt propagation', 'checkpoint on interrupt', or 'autonomous agent shutdown'."
---

# Kaizen Interrupt Mechanism (v0.6.0)

Production-ready graceful shutdown with checkpoint preservation for autonomous agents.

## Overview

The interrupt mechanism provides:
- **3 Interrupt Sources**: USER (Ctrl+C), SYSTEM (timeout/budget), PROGRAMMATIC (API/hooks)
- **2 Shutdown Modes**: GRACEFUL (finish cycle + checkpoint) vs IMMEDIATE (stop now)
- **Checkpoint Preservation**: Automatically saves state on interrupt for recovery
- **Signal Propagation**: Parent interrupts cascade to children
- **Hook Integration**: PRE/POST_INTERRUPT hooks for custom handling

## Quick Start

### Basic Interrupt Configuration

```python
from kaizen.agents.autonomous.base import BaseAutonomousAgent
from kaizen.agents.autonomous.config import AutonomousConfig
from kaizen.core.autonomy.interrupts.handlers import TimeoutInterruptHandler

# Enable interrupts in config
config = AutonomousConfig(
    llm_provider="ollama",
    model="llama3.2:1b",
    enable_interrupts=True,              # Enable interrupt handling
    graceful_shutdown_timeout=5.0,       # Max time for graceful shutdown
    checkpoint_on_interrupt=True         # Save checkpoint before exit
)

# Create agent with interrupt support
agent = BaseAutonomousAgent(config=config, signature=MySignature())

# Add timeout handler (auto-stop after 30s)
timeout_handler = TimeoutInterruptHandler(timeout_seconds=30.0)
agent.interrupt_manager.add_handler(timeout_handler)

# Run agent - gracefully handles Ctrl+C, timeouts, budget limits
try:
    result = await agent.run_autonomous(task="Analyze data")
except InterruptedError as e:
    print(f"Agent interrupted: {e.reason.message}")
    checkpoint_id = e.reason.metadata.get("checkpoint_id")
```

## Interrupt Sources

### 1. USER Interrupts (Ctrl+C)

```python
from kaizen.core.autonomy.interrupts.handlers import SignalInterruptHandler

# Handle Ctrl+C gracefully
signal_handler = SignalInterruptHandler()
agent.interrupt_manager.add_handler(signal_handler)

# Run agent - press Ctrl+C to interrupt
result = await agent.run_autonomous(task="Long task")

# First Ctrl+C: GRACEFUL shutdown (finish cycle + checkpoint)
# Second Ctrl+C: IMMEDIATE shutdown (stop now)
```

### 2. SYSTEM Interrupts (Timeout/Budget)

```python
from kaizen.core.autonomy.interrupts.handlers import (
    TimeoutInterruptHandler,
    BudgetInterruptHandler
)

# Timeout handler (30 seconds)
timeout = TimeoutInterruptHandler(timeout_seconds=30.0)
agent.interrupt_manager.add_handler(timeout)

# Budget handler ($0.10 limit)
budget = BudgetInterruptHandler(max_cost=0.10)
agent.interrupt_manager.add_handler(budget)

# Agent stops automatically when timeout or budget exceeded
result = await agent.run_autonomous(task="Expensive task")
```

### 3. PROGRAMMATIC Interrupts (API/Hooks)

```python
from kaizen.core.autonomy.interrupts import InterruptSource, InterruptMode

# Manual interrupt via API
agent.interrupt_manager.request_interrupt(
    source=InterruptSource.PROGRAMMATIC,
    mode=InterruptMode.GRACEFUL,
    reason="Manual shutdown requested",
    metadata={"user": "admin"}
)

# Interrupt from hook
async def pre_tool_hook(context: HookContext) -> HookResult:
    if context.data.get("tool") == "delete_database":
        context.agent.interrupt_manager.request_interrupt(
            source=InterruptSource.PROGRAMMATIC,
            mode=InterruptMode.IMMEDIATE,
            reason="Dangerous operation detected"
        )
    return HookResult(success=True)
```

## Shutdown Modes

### GRACEFUL (Default)

Finish current cycle, save checkpoint, exit cleanly:

```python
from kaizen.core.autonomy.interrupts import InterruptMode

# Request graceful shutdown
agent.interrupt_manager.request_interrupt(
    source=InterruptSource.USER,
    mode=InterruptMode.GRACEFUL,
    reason="User requested shutdown"
)

# Agent will:
# 1. Finish current cycle
# 2. Save checkpoint with interrupt metadata
# 3. Return result with status="interrupted"
```

### IMMEDIATE

Stop as soon as possible (best effort):

```python
# Request immediate shutdown
agent.interrupt_manager.request_interrupt(
    source=InterruptSource.USER,
    mode=InterruptMode.IMMEDIATE,
    reason="Emergency shutdown"
)

# Agent will:
# 1. Stop at next check point (may not finish cycle)
# 2. Attempt to save checkpoint (best effort)
# 3. Return result with status="interrupted"
```

## Multi-Agent Propagation

Parent interrupts propagate to all children:

```python
# Setup parent-child relationships
parent = SupervisorAgent(config)
child1 = WorkerAgent(config)
child2 = WorkerAgent(config)

parent.interrupt_manager.add_child(child1.interrupt_manager)
parent.interrupt_manager.add_child(child2.interrupt_manager)

# When parent interrupted, children also stop
parent.interrupt_manager.request_interrupt(
    source=InterruptSource.USER,
    mode=InterruptMode.GRACEFUL,
    reason="User requested shutdown"
)
# child1 and child2 also receive interrupt signal
```

## Checkpoint Preservation

Interrupts automatically save checkpoint with metadata:

```python
# Run agent with interrupts enabled
result = await agent.run_autonomous(task="Long task")

if result.get("status") == "interrupted":
    checkpoint_id = result["checkpoint_id"]
    reason = result["interrupt_reason"]

    print(f"Interrupted: {reason}")
    print(f"Checkpoint: {checkpoint_id}")

    # Resume from checkpoint in next run
    agent_resumed = BaseAutonomousAgent(config=config, signature=MySignature())
    result = await agent_resumed.run_autonomous(
        task="Long task",
        resume_from_checkpoint=checkpoint_id
    )
```

## Hook Integration

Custom interrupt handling via hooks:

```python
from kaizen.core.autonomy.hooks import HookEvent, HookContext, HookResult

async def pre_interrupt_hook(context: HookContext) -> HookResult:
    """Custom logic before interrupt"""
    print(f"⚠️  Interrupt triggered: {context.data.get('reason')}")
    # Send notification, log to monitoring, etc.
    return HookResult(success=True)

async def post_interrupt_hook(context: HookContext) -> HookResult:
    """Custom logic after interrupt"""
    checkpoint_id = context.data.get("checkpoint_id")
    print(f"✅ Checkpoint saved: {checkpoint_id}")
    return HookResult(success=True)

# Register hooks
hook_manager.register(HookEvent.PRE_INTERRUPT, pre_interrupt_hook)
hook_manager.register(HookEvent.POST_INTERRUPT, post_interrupt_hook)
```

## Examples

### Example 1: Ctrl+C Interrupt

```python
# examples/autonomy/interrupts/01_ctrl_c_interrupt.py
from kaizen.agents.autonomous.base import BaseAutonomousAgent
from kaizen.core.autonomy.interrupts.handlers import SignalInterruptHandler

config = AutonomousConfig(
    llm_provider="ollama",
    model="llama3.2:1b",
    enable_interrupts=True,
    checkpoint_on_interrupt=True
)

agent = BaseAutonomousAgent(config=config, signature=MySignature())
signal_handler = SignalInterruptHandler()
agent.interrupt_manager.add_handler(signal_handler)

# Run agent - press Ctrl+C to interrupt
result = await agent.run_autonomous(task="Analyze data")
```

### Example 2: Timeout Interrupt

```python
# examples/autonomy/interrupts/02_timeout_interrupt.py
from kaizen.core.autonomy.interrupts.handlers import TimeoutInterruptHandler

agent = BaseAutonomousAgent(config=config, signature=MySignature())
timeout = TimeoutInterruptHandler(timeout_seconds=10.0)
agent.interrupt_manager.add_handler(timeout)

# Agent stops automatically after 10 seconds
result = await agent.run_autonomous(task="Long task")
```

### Example 3: Budget Interrupt

```python
# examples/autonomy/interrupts/03_budget_interrupt.py
from kaizen.core.autonomy.interrupts.handlers import BudgetInterruptHandler

agent = BaseAutonomousAgent(config=config, signature=MySignature())
budget = BudgetInterruptHandler(max_cost=0.10)
agent.interrupt_manager.add_handler(budget)

# Agent stops when cost exceeds $0.10
result = await agent.run_autonomous(task="Expensive task")
```

## Key Features

- **Cooperative**: Agent checks `is_interrupted()` at cycle boundaries
- **Non-blocking**: `request_interrupt()` sets flag, doesn't stop immediately
- **Thread-safe**: Safe for concurrent multi-agent systems
- **Resume-aware**: Checkpoints include interrupt metadata for intelligent resume
- **Signal-safe**: Properly handles SIGINT/SIGTERM for clean process termination

## When to Use

Use interrupts when you need:
- **Ctrl+C Handling**: Graceful shutdown for long-running autonomous agents
- **Timeout Protection**: Auto-stop agents after maximum duration
- **Budget Limits**: Prevent runaway costs with automatic shutdown
- **Multi-Agent Coordination**: Propagate shutdown across agent hierarchies
- **Production Reliability**: Ensure clean exits with checkpoint preservation

## Common Patterns

### Production Agent with All Handlers

```python
from kaizen.agents.autonomous.base import BaseAutonomousAgent
from kaizen.core.autonomy.interrupts.handlers import (
    TimeoutInterruptHandler,
    BudgetInterruptHandler,
    SignalInterruptHandler
)

config = AutonomousConfig(
    llm_provider="ollama",
    model="llama3.2:1b",
    enable_interrupts=True,
    graceful_shutdown_timeout=5.0,
    checkpoint_on_interrupt=True
)

agent = BaseAutonomousAgent(config=config, signature=MySignature())

# Add all handlers
agent.interrupt_manager.add_handler(SignalInterruptHandler())
agent.interrupt_manager.add_handler(TimeoutInterruptHandler(timeout_seconds=300.0))
agent.interrupt_manager.add_handler(BudgetInterruptHandler(max_cost=1.0))

# Run with full protection
result = await agent.run_autonomous(task="Complex task")
```

## References

- **Implementation**: `src/kaizen/core/autonomy/interrupts/`
- **Examples**: `examples/autonomy/interrupts/`
- **Tests**: `tests/e2e/autonomy/test_interrupt_mechanism.py` (34 E2E tests)
- **Guide**: `docs/guides/interrupt-mechanism-guide.md`
- **ADR**: `docs/architecture/adr/016-interrupt-mechanism-design.md`

## Related Skills

- **[kaizen-checkpoint-resume](kaizen-checkpoint-resume.md)** - Checkpoint and resume system
- **[kaizen-observability-hooks](kaizen-observability-hooks.md)** - Lifecycle hooks
- **[kaizen-control-protocol](kaizen-control-protocol.md)** - Bidirectional communication
