---
name: session-handoff
description: Use this skill when you need to create or resume a handoff document for seamless AI agent session transfers, ensuring continuity and clarity in ongoing tasks.
---

# Handoff

Creates comprehensive handoff documents that enable fresh AI agents to seamlessly continue work with zero ambiguity. Solves the long-running agent context exhaustion problem.

## Mode Selection

Determine which mode applies:

**Creating a handoff?** User wants to save current state, pause work, or context is getting full.
- Follow: CREATE Workflow below

**Resuming from a handoff?** User wants to continue previous work, load context, or mentions an existing handoff.
- Follow: RESUME Workflow below

**Proactive suggestion?** After substantial work (5+ file edits, complex debugging, major decisions), suggest:
> "We've made significant progress. Consider creating a handoff document to preserve this context for future sessions. Say 'create handoff' when ready."

## CREATE Workflow

### Step 1: Generate Scaffold

Run the smart scaffold script to create a pre-filled handoff document:

```bash
python scripts/create_handoff.py [task-slug]
```

Example: `python scripts/create_handoff.py implementing-user-auth`

**For continuation handoffs** (linking to previous work):
```bash
python scripts/create_handoff.py "auth-part-2" --continues-from 2024-01-15-auth.md
```

The script will:
- Create `.claude/handoffs/` directory if needed
- Generate timestamped filename
- Pre-fill: timestamp, project path, git branch, recent commits, modified files
- Add handoff chain links if continuing from previous
- Output file path for editing

### Step 2: Complete the Handoff Document

Open the generated file and fill in all `[TODO: ...]` sections. Prioritize these sections:

1. **Current State Summary** - What's happening right now
2. **Important Context** - Critical info the next agent MUST know
3. **Immediate Next Steps** - Clear, actionable first steps
4. **Decisions Made** - Choices with rationale