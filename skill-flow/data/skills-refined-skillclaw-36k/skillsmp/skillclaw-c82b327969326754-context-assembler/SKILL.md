---
name: context-assembler
description: Use this skill when you need to assemble relevant context packages for agent spawns, prioritizing by relevance and respecting token budgets.
---

# Context-Assembler Skill

You are the context-assembler skill. When invoked, you assemble relevant context packages for agent spawns, prioritizing by relevance and respecting token budgets.

## When to Invoke This Skill

**Invoke this skill when:**
- The orchestrator prepares to spawn an agent and needs relevant context.
- Any agent mentions "assemble context", "get context packages", or "context-assembler".
- Preparing developer, QA, tech lead spawns with session context.
- You need to check for relevant error patterns before agent spawn.

**Do NOT invoke when:**
- No active orchestration session exists.
- Manually reading specific files (use Read tool directly).
- Working outside BAZINGA orchestration.

---

## Your Task

When invoked, execute these steps in order:

### Step 1: Determine Context Parameters

Extract from the calling request or infer from conversation:
- `session_id`: Current orchestration session (REQUIRED)
- `group_id`: Task group being processed (OPTIONAL - use empty string "" if not provided)
- `agent_type`: Target agent - developer/senior_software_engineer/qa_expert/tech_lead/investigator (REQUIRED)
- `model`: Model being used - haiku/sonnet/opus or full model ID (OPTIONAL, for token budgeting)
- `current_tokens`: Current token usage in conversation (OPTIONAL, for zone detection)
- `iteration`: Current iteration number (optional, default 0)
- `include_reasoning`: Whether to include prior agent reasoning for handoff (OPTIONAL)
  - **DEFAULT BEHAVIOR:** Automatically `true` when reasoning context is beneficial:
    - `qa_expert`, `tech_lead`: ALWAYS (handoff recipients)
    - `senior_software_engineer`: ALWAYS (escalation needs prior context)
    - `investigator`: ALWAYS (debugging needs full context)
    - `developer`: When `iteration > 0` (retry needs prior reasoning; first attempt has none)
  - Explicitly set to `false` to disable reasoning for any agent.
- `reasoning_level`: Level of detail for reasoning retrieval (OPTIONAL)
  - `minimal`: 400 tokens - key decisions only.
  - `medium`: 800 tokens - decisions + approach (DEFAULT).
  - `full`: 1200 tokens - complete reasoning chain.

If `session_id` or `agent_type` are missing, check the request for errors.