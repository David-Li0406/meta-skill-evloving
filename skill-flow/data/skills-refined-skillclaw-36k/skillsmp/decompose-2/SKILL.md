---
name: decompose
description: Break a problem into atomic, testable subproblems. Use when facing complex tasks, unclear requirements, or planning implementation strategy.
allowed-tools: ["read_file", "update_plan"]
metadata:
  short-description: Decompose problems systematically
---

# Problem Decomposition

**Read these references:**
- `references/decomposition.md` - Problem breakdown strategies
- `~/.config/agent/core/task-management.md` - Creating TODO lists from decomposition
- `~/.config/agent/core/methodology.md` - Integration with problem-solving framework

## Instructions

Decompose problems into atomic, testable subproblems per references:

### Decomposition Steps

1. **Understand the whole problem**
   - Read all requirements and constraints
   - Identify inputs, outputs, and transformations
   - Note dependencies and assumptions

2. **Identify natural boundaries**
   - Where can the problem be split?
   - What are the logical units?
   - Which parts are independent?

3. **Break into subproblems**
   - Each subproblem should be:
     - **Atomic**: Single, clear responsibility
     - **Testable**: Can be verified independently
     - **Self-contained**: Minimal external dependencies
   - Name each subproblem clearly

4. **Map dependencies**
   - Which subproblems depend on others?
   - What's the dependency graph?
   - Which must be done sequentially?

5. **Identify parallelization opportunities**
   - Which subproblems are independent?
   - What can run concurrently?
   - How can we maximize throughput?

### Create TODO List

Per `task-management.md`, create a TODO list with:
- Each subproblem as an atomic task
- Dependencies clearly noted
- Parallelization opportunities marked
- Execution order specified

### Example Output

```
TODO List for Problem X:
1. [pending] Subproblem A (no dependencies)
2. [pending] Subproblem B (no dependencies) [can parallelize with A]
3. [pending] Subproblem C (depends on A, B)
4. [pending] Subproblem D (depends on C)
```

## Arguments

Problem to decompose: ${ARGUMENTS}
