---
title: Post-Compact Memory Recovery
impact: CRITICAL
tags: orchestration, memory, compact
---

# Post-Compact Memory Recovery

```
   ─────────────────◆─────────────────
   CLORCH DETECTS COMPACT → LOADS MEMORY → CONTINUES

   This is the PRIMARY mechanism. No hooks needed.
   You detect. You recover. Seamlessly.
   ─────────────────◆─────────────────
```

## How to Detect You Were Compacted

**CHECK AT THE START OF EVERY RESPONSE.** If you see ANY of these:

1. `"This session is being continued from a previous conversation that ran out of context"`
2. `"The conversation is summarized below:"`
3. `"[Previous conversation context...]"` or similar bracketed summaries
4. A compact summary that describes what happened rather than showing actual messages
5. Your context feels "fresh" but user expects you to know something

**→ You were just compacted. Execute recovery IMMEDIATELY.**

## Recovery Protocol (Do This FIRST)

**BEFORE responding to user, load memory in this order:**

```
STEP 1: Load handoff (most important)
----------------------------------------
Read("thoughts/shared/handoffs/")  # Find most recent .yaml file
# OR
Read(".claude/memory/handoff.md")  # Fallback simple handoff

STEP 2: Load state files (details)
----------------------------------------
Read(".claude/memory/state.json")    # Current state, modified files
Read(".claude/memory/pending.md")    # Unfinished tasks

STEP 3: Invoke /resume if complex
----------------------------------------
If handoff has many tasks or complex state:
Use Skill tool: skill="resume"
```

**Exception:** You may use Read tool directly for recovery. This overrides the normal orchestrator rule.

## What Recovery Looks Like

**To the user, show:**

```
   ─────────────────◆─────────────────
   Context compacted. Memory recovered.
   ─────────────────◆─────────────────

Restored from: thoughts/shared/handoffs/2026-01-15_feature.yaml

• Goal: [from handoff]
• Status: [from handoff outcome]
• Focus: [from handoff now: field]
• Pending: [from next: list]

Continuing seamlessly. What's next?
```

## Why This Works

```
TIMELINE:
─────────────────────────────────────────────
[Working...] → Context fills → PreCompact hook fires
                                     │
                              Saves handoff + memory
                                     │
                              [Claude compacts]
                                     │
                              [User types message]
                                     │
                              YOU detect summary text
                                     │
                              YOU load memory files
                                     │
                              [Continue seamlessly]
─────────────────────────────────────────────
```

**No post-compact hook needed.** You are the recovery mechanism.

## Recovery Checklist

Before responding after compact:

- [ ] Checked for handoff in `thoughts/shared/handoffs/`
- [ ] Read handoff YAML/MD completely
- [ ] Loaded state.json if exists
- [ ] Acknowledged recovery to user
- [ ] Ready to continue from `now:` field

## If No Handoff Found

If `.claude/memory/` and `thoughts/shared/handoffs/` are empty:

```
Context was compacted but no saved memory found.
Starting fresh. What would you like to work on?
```

## Worker Mode (For Spawned Agents)

If you're a WORKER agent (not orchestrator), skip this rule. Workers don't manage context - they execute tasks and return.
