# QCI Coherence States

## Overview

QCI (Quantum Coherence Interface) tracks coherence states across multi-agent systems.

## Key Concepts

- **Coherence Level**: 0.0 to 1.0 measure of agent alignment
- **Breathing Cycle**: Synchronization states (INHALE, HOLD, EXHALE)
- **Network Coherence**: Aggregate coherence across all agents

## Usage

```python
from mcp_b import QCI, QCIState, BreathingCycle

qci = QCI()

# Register agents
state1 = qci.register_agent("7C1", initial_coherence=0.95)
state2 = qci.register_agent("5510", initial_coherence=0.90)

# Calculate ROV-Q signal
state1.calculate_rov_q(resonance=12860.65, quality=1.0)
state1.calculate_signal(base=4414.94)

# Sync breathing
qci.sync_breathing(["7C1", "5510"], BreathingCycle.INHALE)

# Check network coherence
network_coherence = qci.calculate_network_coherence()
print(f"Network coherence: {network_coherence:.2f}")
```

## Breathing Cycles

| Cycle | Description |
|-------|-------------|
| INHALE | Gathering phase |
| HOLD | Processing phase |
| EXHALE | Output phase |

## Binary Representation

```python
from mcp_b import binary_from_coherence

# Convert coherence to binary flags
binary = binary_from_coherence(0.95)
print(f"Binary state: {binary:016b}")
```
