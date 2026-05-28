---
name: goap-orchestrator
description: Central Goal-Oriented Action Planning orchestrator that plans and executes clinical analysis pipelines
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: clinical-pipeline
---

## What I do

I orchestrate the clinical analysis pipeline using A\* search planning. I transform the initial `WorldState` to a goal state by finding the lowest-cost sequence of agent actions. Each action has preconditions and effects that define state transitions.

## When to use me

Use this when you need to:

- Understand how agents are sequenced in the clinical pipeline
- Debug why a specific agent is not executing
- Modify the planning algorithm or action costs
- Add new agents to the pipeline

## Quick Reference

| Component             | Location                 | Purpose                                     |
| :-------------------- | :----------------------- | :------------------------------------------ |
| **GOAPPlanner**       | `services/goap.ts`       | A\* search implementation                   |
| **AVAILABLE_ACTIONS** | `services/goap/agent.ts` | Agent action definitions                    |
| **WorldState**        | `types.ts`               | State tracking interface                    |
| **AgentAction**       | `types.ts`               | Action interface with preconditions/effects |

## Key Concepts

**WorldState**: Object tracking pipeline progress (e.g., `{ image_verified: true, skin_tone_detected: false }`)

**AgentAction**: Actions with `preconditions`, `effects`, and `cost`

**A\* Planning**: Uses backward-chaining heuristic to find optimal paths

**State Key**: Serialized state representation for closed-set tracking

## Operational Constraints

- MAX 500 LOC per file - refactor to `services/executors/` if exceeded
- All inference must return confidence scores (0-1)
- Graceful degradation: return "skipped" for non-critical failures
- Planner iterates up to 5000 times to prevent infinite loops

## Documentation

- [Best Practices](BEST_PRACTICES.md) - Action design, state management, planning efficiency
- [Implementation Guide](IMPLEMENTATION_GUIDE.md) - Adding agents, custom heuristics, debugging
- [Testing Guide](TESTING_GUIDE.md) - Unit tests, integration tests, edge cases
