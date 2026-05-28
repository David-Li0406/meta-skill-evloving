---
name: loop-agent
description: Use this skill when tasks require iterative refinement and progressive improvement through multiple cycles until quality criteria are met.
---

# Loop Agent Skill: Iterative Workflow Execution

Enable iterative refinement workflows through systematic loop execution with convergence detection, progress tracking, and intelligent termination.

## Quick Reference

Use loop-agent when:
- Code needs iterative refinement until quality standards are met
- Tests need repeated fix-validate cycles
- Performance requires progressive optimization
- Quality improvements need multiple passes
- Feedback loops are necessary for convergence

## When to Use This Skill

### Ideal Scenarios

**Code Refinement**:
- Iterative code review → fix → review cycles
- Progressive refactoring with validation
- Quality improvement until standards are met
- Incremental cleanup and optimization

**Testing & Validation**:
- Fix failures → retest → fix → retest loops
- Progressive test coverage improvement
- Iterative performance tuning
- Security hardening cycles

**Optimization**:
- Performance optimization until targets are met
- Resource usage reduction iterations
- Progressive complexity reduction
- Convergence-based improvements

**Documentation & Analysis**:
- Iterative documentation enhancement
- Progressive analysis deepening
- Coverage improvement loops
- Quality refinement cycles

### NOT Appropriate For

- Single-pass tasks (use appropriate specialized agent)
- Purely parallel work with no dependencies (use parallel-execution)
- Simple linear workflows (use sequential coordination)
- One-time analysis (use appropriate analysis agent)

## Core Concepts

### Loop Termination Modes

| Mode | Description | Use When |
|------|-------------|----------|
| **Fixed** | Run exactly N iterations | Known number of refinement passes needed |
| **Criteria** | Until success criteria met (with max limit) | Specific quality/performance targets exist |
| **Convergence** | Stop when improvements become negligible | Optimal result unknown, stop at diminishing returns |
| **Hybrid** | Combine multiple conditions | Complex requirements |

### Examples

- **Fixed Iteration Count**: "Run 3 quality improvement iterations."
- **Criteria-Based Termination**: "Optimize until response time < 100ms (max 10 iterations)."
- **Convergence Detection**: "Refactor until <5% quality improvement over 3 iterations."