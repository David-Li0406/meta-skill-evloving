---
name: goap-agent
description: Use this skill for complex multi-step tasks that require intelligent planning, decomposition, and coordination of multiple specialized agents, ensuring quality through validation checkpoints.
---

# GOAP Agent Skill: Goal-Oriented Action Planning

Enable intelligent planning and execution of complex multi-step tasks through systematic decomposition, dependency mapping, and coordinated multi-agent execution.

## Quick Reference

- **[Methodology](methodology.md)** - Core GOAP planning cycle and phases
- **[Skills Reference](skills.md)** - Available skills by category
- **[Agents Reference](agents.md)** - Available task agents and capabilities
- **[Patterns](patterns.md)** - Common GOAP execution patterns
- **[Examples](examples.md)** - Complete GOAP workflow examples

## When to Use

Use this skill when facing:

- **Complex Multi-Step Tasks**: Tasks requiring 5+ distinct steps or multiple specialized capabilities.
- **Cross-Domain Problems**: Issues spanning multiple areas (storage, API, testing, documentation).
- **Optimization Opportunities**: Tasks that could benefit from parallel, sequential, or hybrid execution strategies.
- **Quality-Critical Work**: Projects requiring validation checkpoints and quality gates.
- **Resource-Intensive Operations**: Large refactors or architectural changes.

## CRITICAL: Understanding Skills vs Task Agents

**Skills** (invoked via `Skill` tool): Instruction sets that guide Claude directly, providing specialized knowledge and workflows.

**How to invoke**: `Skill(command="skill-name")`

**Task Agents** (invoked via `Task` tool): Autonomous sub-processes that execute tasks independently using tools.

**How to invoke**: `Task(subagent_type="agent-name", prompt="...", description="...")`

### Common Error to Avoid

**WRONG**: `Task(subagent_type="rust-code-quality", ...)` → ERROR! rust-code-quality is a Skill!

**CORRECT**: `Skill(command="rust-code-quality")` → SUCCESS

## Core Process

1. **ANALYZE** → Understand goals, constraints, resources.
2. **DECOMPOSE** → Break into atomic tasks with dependencies.
3. **STRATEGIZE** → Choose execution pattern.
4. **COORDINATE** → Assign to specialized agents.
5. **EXECUTE** → Run with monitoring and quality gates.
6. **SYNTHESIZE** → Aggregate results and validate success.

See **[methodology.md](methodology.md)** for detailed phase-by-phase guidance and **[patterns.md](patterns.md)** for common execution patterns.