---
name: simpy
description: Use this skill when building simulations of systems with processes, queues, resources, and time-based events such as manufacturing systems, service operations, network traffic, logistics, or any system where entities interact with shared resources over time.
---

# SimPy - Discrete-Event Simulation

## Overview

SimPy is a process-based discrete-event simulation framework based on standard Python. It allows modeling systems where entities (customers, vehicles, packets, etc.) interact with each other and compete for shared resources (servers, machines, bandwidth, etc.) over time.

**Core capabilities:**
- Process modeling using Python generator functions
- Shared resource management (servers, containers, stores)
- Event-driven scheduling and synchronization
- Real-time simulations synchronized with wall-clock time
- Comprehensive monitoring and data collection

## When to Use This Skill

Use the SimPy skill when:

1. **Modeling discrete-event systems** - Systems where events occur at irregular intervals.
2. **Resource contention** - Entities compete for limited resources (servers, machines, staff).
3. **Queue analysis** - Studying waiting lines, service times, and throughput.
4. **Process optimization** - Analyzing manufacturing, logistics, or service processes.
5. **Network simulation** - Packet routing, bandwidth allocation, latency analysis.
6. **Capacity planning** - Determining optimal resource levels for desired performance.
7. **System validation** - Testing system behavior before implementation.

**Not suitable for:**
- Continuous simulations with fixed time steps (consider SciPy ODE solvers).
- Independent processes without resource sharing.
- Pure mathematical optimization (consider SciPy optimize).

## Quick Start

### Basic Simulation Structure

```python
import simpy

def process(env, name):
    """A simple process that waits and prints."""
    print(f'{name} starting at {env.now}')
    yield env.timeout(5)
    print(f'{name} finishing at {env.now}')

# Create environment
env = simpy.Environment()

# Start processes
env.process(process(env, 'Process 1'))
env.process(process(env, 'Process 2'))

# Run simulation
env.run(until=10)
```

### Resource Usage Pattern

```python
import simpy

def customer(env, name, resource):
    """Customer requests resource, uses it, then releases."""
    with resource.request() as req:
        yield req  # Wait for resource
        print(f'{name} using resource at {env.now}')
```