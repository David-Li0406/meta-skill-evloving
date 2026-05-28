---
name: cycle-aware-nodes
description: "Cycle-aware node patterns with state preservation and convergence. Use when asking 'cycle-aware nodes', 'cycle state', 'state preservation', 'cyclic node patterns', 'iteration state', or 'cycle convergence'."
---

# Cycle-Aware Nodes

Essential patterns for cycle-aware node development with state preservation and convergence.

> **Skill Metadata**
> Category: `core-patterns`
> Priority: `HIGH`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Cycle-aware node development with state management
- **Category**: core-patterns
- **Priority**: HIGH
- **Trigger Keywords**: cycle-aware nodes, cycle state, state preservation, cyclic node patterns

## Core Pattern - PythonCodeNode with Singleton State

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Cycle-aware state management using PythonCodeNode
workflow = WorkflowBuilder()
workflow.add_node("PythonCodeNode", "optimizer", {
    "code": """
# Singleton pattern for persistent state across cycles
class CycleState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.iteration = 0
            cls._instance.state = {}
        return cls._instance

    def get_iteration(self):
        return self.iteration

    def increment_iteration(self):
        self.iteration += 1

    def get_previous_state(self):
        return self.state.copy()

    def set_cycle_state(self, data):
        self.state.update(data)
        return data

# Initialize cycle state
cycle_state = CycleState()

# Get parameters with state fallback
quality = input_data.get("quality", 0.0)
target = input_data.get("target", cycle_state.get_previous_state().get("target", 0.8))

# Process one iteration
new_quality = min(1.0, quality + 0.1)
converged = new_quality >= target

# Update state and increment iteration
cycle_state.set_cycle_state({"target": target})
cycle_state.increment_iteration()

result = {
    "quality": new_quality,
    "converged": converged,
    "iteration": cycle_state.get_iteration()
}
"""
})

# Build BEFORE creating cycle
built_workflow = workflow.build()

# Create cycle with result.* mapping
cycle = built_workflow.create_cycle("optimizer_cycle")
cycle.connect("optimizer", "optimizer", mapping={"result.quality": "input_data"}) \
     .max_iterations(20) \
     .converge_when("converged == True") \
     .build()

runtime = LocalRuntime()
results, run_id = runtime.execute(built_workflow, parameters={
    "optimizer": {"target": 0.9}
})
```

## State Preservation Pattern

```python
# Adaptive learning rate with state preservation
workflow.add_node("PythonCodeNode", "adaptive_processor", {
    "code": """
class AdaptiveState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.learning_rate = 0.1
            cls._instance.previous_error = None
        return cls._instance

state = AdaptiveState()

# Get current error
data = input_data.get("data", [])
current_error = sum(abs(x - 50) for x in data) / len(data) if data else 1.0

# Adapt learning rate based on improvement
if state.previous_error is not None:
    improvement = state.previous_error - current_error
    if improvement < 0.01:
        state.learning_rate *= 0.9  # Reduce if not improving

# Process data
processed = [x * state.learning_rate for x in data]

# Update state
state.previous_error = current_error

result = {
    "result": processed,
    "learning_rate": state.learning_rate,
    "error": current_error
}
"""
})
```

## Convergence Patterns

### Self-Contained Convergence
```python
# Node determines its own convergence
workflow.add_node("PythonCodeNode", "self_converging", {
    "code": """
quality = input_data.get('quality', 0.0)
target = input_data.get('target', 0.8)

# Improve quality
new_quality = min(1.0, quality + 0.1)

# Self-determine convergence
converged = new_quality >= target

result = {
    'quality': new_quality,
    'converged': converged  # Built-in convergence check
}
"""
})

built_workflow = workflow.build()
cycle = built_workflow.create_cycle("self_converging_cycle")
cycle.connect("self_converging", "self_converging", mapping={"result.quality": "input_data"}) \
     .max_iterations(15) \
     .converge_when("converged == True") \
     .build()
```

### Accumulation Pattern
```python
# Track history with size limit
workflow.add_node("PythonCodeNode", "history_tracker", {
    "code": """
class HistoryState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.metrics = []
        return cls._instance

    def add_metric(self, value, max_history=10):
        self.metrics.append(value)
        if len(self.metrics) > max_history:
            self.metrics = self.metrics[-max_history:]
        return self.metrics

state = HistoryState()

# Calculate current metric
current_value = input_data.get("value", 0.0)

# Track history
history = state.add_metric(current_value, max_history=10)

# Calculate trend
if len(history) >= 3:
    recent_avg = sum(history[-3:]) / 3
    trend = "improving" if recent_avg > history[0] else "stable"
else:
    trend = "insufficient_data"

result = {
    "value": current_value,
    "trend": trend,
    "converged": current_value >= 0.95
}
"""
})
```

## Critical Rules

### 1. Always Build Before Creating Cycles
```python
# ✅ CORRECT
built_workflow = workflow.build()
cycle = built_workflow.create_cycle("my_cycle")

# ❌ WRONG
cycle = workflow.create_cycle("my_cycle")  # Will fail!
```

### 2. Use result.* Prefix for PythonCodeNode
```python
# ✅ CORRECT - PythonCodeNode outputs use result.* prefix
cycle.connect("python_node", "python_node",
              mapping={"result.quality": "input_data"})

# ❌ WRONG - Direct mapping will fail
cycle.connect("python_node", "python_node",
              mapping={"quality": "input_data"})
```

### 3. Parameters in Cycles
```python
# ✅ CORRECT - Use required=False for cycle parameters
from kailash.nodes.base import NodeParameter

def get_parameters(self):
    return {
        "data": NodeParameter(
            name="data", type=list,
            required=False, default=[]
        )
    }

# ❌ WRONG - required=True breaks cycles
# def get_parameters(self):
#     return {
#         "data": NodeParameter(name="data", type=list, required=True)
#     }
```

## Common Use Cases

- **Iterative Optimization**: Gradient descent, simulated annealing, genetic algorithms
- **Quality Improvement**: Progressive refinement until quality threshold met
- **Adaptive Processing**: Learning rate adjustment, parameter tuning
- **Convergence Detection**: Self-contained or external convergence checking
- **State Accumulation**: History tracking, trend analysis

## Related Patterns

- **For cycle basics**: See [`cyclic-workflows`](#)
- **For debugging**: See [`cycle-debugging`](#)
- **For testing**: See [`cycle-testing`](#)
- **For state persistence**: See [`cycle-state-persistence`](#)

## When to Escalate to Subagent

Use specialized subagents when:
- **pattern-expert**: Complex cycle patterns, multi-node cycles
- **testing-specialist**: Comprehensive cycle testing strategies
- **sdk-navigator**: Cycle-related errors, parameter issues

## Documentation References

### Primary Sources
- [`sdk-users/2-core-concepts/cheatsheet/021-cycle-aware-nodes.md`](../../../sdk-users/2-core-concepts/cheatsheet/021-cycle-aware-nodes.md)

## Quick Tips

- 💡 **Build First**: Always call workflow.build() before creating cycles
- 💡 **State Singleton**: Use singleton pattern for persistent state across iterations
- 💡 **Result Prefix**: PythonCodeNode outputs need result.* prefix in mappings
- 💡 **Self-Convergence**: Let nodes determine their own convergence when possible

## Keywords for Auto-Trigger

<!-- Trigger Keywords: cycle-aware nodes, cycle state, state preservation, cyclic node patterns, iteration state, cycle convergence -->
