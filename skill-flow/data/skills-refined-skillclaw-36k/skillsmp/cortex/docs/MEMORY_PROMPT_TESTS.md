---
summary: "Test cases for memory extraction prompts"
read_when:
  - You want to validate memory extraction output quality
  - You are tuning memory prompts or facets mappings
---
# Memory Prompt Tests

This doc provides small, focused test cases to evaluate **AI-session memory extraction**
(AIX). Each case includes a short conversation snippet and expected extracted signals.

---

## Test Case 1 — Preferences + Corrections (AI session)

**Prompts:** `self-preference-extraction-v1`, `correction-extraction-v1`

**Session name:** `nexus-cli-development`

**Conversation**

```
User: Summarize the PR.
Assistant: Here's a paragraph summary of the changes...
User: No, use bullet points. I hate paragraphs for summaries.
Assistant: Got it. Bulleted summary:
- ...
User: Also, show me the plan before you implement anything. Don't just start coding.
Assistant: Understood.
```

**Expected extracted signals**

- `formatting: Prefers bullet points over paragraphs for summaries`
- `task_approach: Before making changes, show the plan and get confirmation`

**Checks**

- `self_preference` facets contain the memory_entry lines above
- `self_correction` facets include the generalized rules
- `correction_extraction_v1` outputs `scope_hint` as `user_general`

---

## Test Case 2 — Relationship Context (iMessage)

**Prompt:** `relationship-context-extraction-v1`

**Conversation**

```
Casey: Can you grab groceries on your way home?
User: Yep. Our anniversary is coming up soon, too.
User: I'll also call Dad tomorrow — he said the store is swamped again.
```

**Expected extracted signals**

- `Casey Adams — girlfriend, they live together, dating since February 2023`
- `Jim Brandt (Dad) — father, owns Napa General Store, lives in Napa`

**Checks**

- Relationship entries include `memory_entry`
- Importance level high for partner/family

---

## Test Case 3 — Workspace Conventions (AI session)

**Prompt:** `workspace-pattern-extraction-v1`

**Conversation**

```
User: Remember: skills live in skills/{type}/{name}/SKILL.md.
Assistant: Got it.
User: And use `nexus status` first to understand the workspace state.
Assistant: Understood.
User: Also, don't edit state/ directly — use the CLI.
```

**Expected extracted signals**

- `structure: Skill definitions live in skills/{type}/{name}/SKILL.md`
- `tools: Use 'nexus status' to check current state before taking action`
- `gotchas: Don't modify state/ files directly - use nexus CLI commands`

**Checks**

- `workspace_convention` facets include these memory_entry strings

---

## Test Case 4 — Override / Contradiction (Expected Failure for Now)

**Purpose:** Validate future override behavior (currently not implemented).

**Conversation A (older)**
```
User: Summaries should always be bullet points.
```

**Conversation B (newer)**
```
User: Actually, for quick updates I prefer a short paragraph.
```

**Expected (future)**
- The newer preference should override the older one in synthesized memory.

**Current behavior**
- Both preferences will appear because compaction does not handle contradiction yet.

---

## Suggested Run Strategy

If you want to test these prompts end-to-end in comms:

1. Use a scratch DB:
   ```
   COMMS_DATA_DIR=/tmp/comms-memtest comms init
   COMMS_DATA_DIR=/tmp/comms-memtest comms compute seed
   ```
2. Insert test conversations into `events`, `threads`, and `conversations` tables.
3. Run:
   ```
   COMMS_DATA_DIR=/tmp/comms-memtest comms compute enqueue --analysis-type self_preference_extraction_v1
   COMMS_DATA_DIR=/tmp/comms-memtest comms compute run
   ```
4. Inspect:
   ```
   sqlite3 /tmp/comms-memtest/comms.db "select facet_type, value from facets where facet_type like 'self_%';"
   ```

If you want, I can add a small `comms prompt run` command to make these tests easier.
