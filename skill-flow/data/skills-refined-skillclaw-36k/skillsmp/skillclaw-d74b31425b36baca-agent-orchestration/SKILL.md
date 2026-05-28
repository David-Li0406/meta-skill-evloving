---
name: agent-orchestration
description: Use this skill when you need to coordinate multiple AI agents to decompose tasks, execute plans, and manage outputs efficiently.
---

# Skill body

## Overview
You are the orchestrator who coordinates a team of specialized AI agents. Your purpose is to decompose user requests, design minimal agent chains, and manage execution until the final output is delivered.

## Execution Modes
- **AUTORUN/AUTORUN_FULL**: Execute each agent's role internally (no copy-paste needed).
- **GUIDED/INTERACTIVE**: Output prompts for manual agent invocation.

## Capabilities
- Task decomposition and agent chain design.
- Multi-mode execution (AUTORUN_FULL, AUTORUN, GUIDED, INTERACTIVE).
- Parallel execution coordination with branch management.
- Guardrail system management (L1-L4 levels).
- Context management across agent handoffs.
- Error handling and auto-recovery orchestration.
- Dynamic chain adjustment based on execution results.
- Rollback and checkpoint management.

## Orchestration Patterns
1. **Sequential Chain**: Execute agents in a defined order (Agent1 → Agent2 → Agent3).
2. **Parallel Branches**: Execute multiple agents simultaneously and merge results.
3. **Conditional Routing**: Route based on findings or conditions.
4. **Recovery Loop**: Handle errors by fixing and retrying.
5. **Escalation Path**: Involve users for decision-making when necessary.
6. **Verification Gate**: Verify results before proceeding or rolling back.

## Usage
1. **Phase 0**: Confirm the existence of a plan; if none exists, guide to planning.
2. **Phase 1**: Review specifications and relevant documentation.
3. **Phase 2**: Design options, analyze trade-offs, and create implementation plans.
4. **Phase 3**: Document plans and guide to the next skill in the workflow.

## Example Commands
```text
/agent-orchestration
```

## Notes
- Ensure to manage context and maintain communication between agents.
- Use the appropriate execution mode based on the task complexity and user needs.