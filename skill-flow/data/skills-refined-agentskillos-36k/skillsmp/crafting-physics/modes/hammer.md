# Hammer Mode — Multi-File Architecture

Hammer mode orchestrates full-stack feature implementation through the Loa sequence.

<when_to_use>
## When Hammer Activates

**Scope Detection Score ≥2:**

| Signal | Score | Examples |
|--------|-------|----------|
| "build", "implement", "create feature" | +1 | "build rewards system" |
| "feature", "system", "flow" | +1 | "notification feature" |
| Contract/indexer work implied | +1 | "add staking" |
| Multi-file scope explicit | +1 | "across the app" |
| Financial/critical domain | +1 | "payment flow" |

**OR existing Hammer session in progress.**
</when_to_use>

<scope_detection>
## Scope Detection Box

```
┌─ Scope Detection ─────────────────────────────────────────┐
│                                                           │
│  This looks like HAMMER work:                             │
│  • "{keyword}" — {reason}                                 │
│  • "{keyword}" — {reason}                                 │
│                                                           │
│  Full-stack implementation requires architecture.         │
│  I'll run the complete sequence:                          │
│                                                           │
│  1. /plan-and-analyze → Requirements (PRD)                │
│  2. /architect → Design (SDD)                             │
│  3. /sprint-plan → Tasks                                  │
│  4. Review plan                                           │
│  5. /run sprint-plan → Implementation                     │
│                                                           │
│  [Proceed with Hammer] [Chisel anyway (UI only)]          │
│                                                           │
└───────────────────────────────────────────────────────────┘
```
</scope_detection>

<workflow>
## Hammer Workflow

### Step H1: Initialize State

1. Create/update `grimoires/loa/hammer-state.json`:
```json
{
  "feature": "{description}",
  "started_at": "{ISO8601}",
  "current_phase": "initializing",
  "phases_complete": [],
  "artifacts": {},
  "context_seed": {}
}
```

2. Aggregate Sigil context for PRD seeding:
   - Read observations for user insights
   - Read taste.md for physics preferences
   - Extract relevant learnings

### Step H2: Check Existing Artifacts

```
┌─ Existing Artifacts Detected ────────────────────────────┐
│                                                          │
│  PRD: grimoires/loa/prd.md (2 days old) ✓ relevant      │
│  SDD: grimoires/loa/sdd.md (2 days old) ✓ relevant      │
│                                                          │
│  Options:                                                │
│  1. Use existing → Skip to sprint planning               │
│  2. Regenerate PRD → Full sequence                       │
│  3. Regenerate SDD only → Keep PRD, redo architecture    │
│  4. Chisel anyway → UI only                              │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Artifact Relevance Check:**
- If artifact exists and < 7 days old: Check content relevance
- If artifact matches current feature context: Mark as usable
- If artifact is stale or unrelated: Offer regeneration

### Step H3: Execute Loa Sequence

Execute in order, showing progress:

1. **PRD Phase** (if needed):
   ```
   [Invoking /plan-and-analyze with seeded context...]
   ```
   Update hammer-state.json: `current_phase: "prd"`
   On completion: `phases_complete.push("prd")`

2. **SDD Phase** (if needed):
   ```
   [Invoking /architect...]
   ```
   Update state accordingly.

3. **Sprint Phase**:
   ```
   [Invoking /sprint-plan...]
   ```

4. **Review Checkpoint**:
   ```
   ┌─ Hammer Plan Complete ────────────────────────────────────┐
   │                                                           │
   │  Feature: {description}                                   │
   │                                                           │
   │  Artifacts:                                               │
   │  • PRD: grimoires/loa/prd.md                             │
   │  • SDD: grimoires/loa/sdd.md                             │
   │  • Sprint: grimoires/loa/sprint.md                       │
   │                                                           │
   │  Components to implement:                                 │
   │  1. [Backend] {component}                                 │
   │  2. [Frontend] {component}                                │
   │  ...                                                      │
   │                                                           │
   │  Ready to implement. Run:                                 │
   │    /run sprint-plan                                       │
   │                                                           │
   └───────────────────────────────────────────────────────────┘
   ```

### Step H4: Implementation Phase

When user runs `/run sprint-plan`:
- Execute sprint tasks
- Apply Sigil physics to each component
- Track progress in hammer-state.json

### Step H5: Completion

On successful completion:
- Archive hammer-state.json
- Log to taste.md: `HAMMER_COMPLETE`
- Show summary of implemented components
</workflow>

<checkpoints>
## Progress Checkpoints

Show after each phase completion:

```
┌─ Checkpoint: SDD Complete ────────────────────────────────┐
│                                                           │
│  ✓ PRD created                                            │
│  ✓ SDD created ← current                                  │
│  ○ Sprint planning                                        │
│  ○ Implementation                                         │
│                                                           │
│  Elapsed: 12 minutes                                      │
│                                                           │
│  [c] Continue to sprint planning                          │
│  [p] Pause here (can resume later)                        │
│  [r] Review artifacts before continuing                   │
│                                                           │
└───────────────────────────────────────────────────────────┘
```
</checkpoints>

<safety>
## Safety Guardrails

### Duration Warning

Track elapsed time. Warn at 30 minutes:

```
┌─ Duration Warning ────────────────────────────────────────┐
│                                                           │
│  Hammer mode has been running for 30 minutes.             │
│                                                           │
│  Progress:                                                │
│  ✓ PRD, SDD complete                                      │
│  → Sprint planning in progress                            │
│                                                           │
│  [c] Continue                                             │
│  [p] Pause and save progress                              │
│  [a] Abort hammer mode                                    │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### File Limit

Maximum 10 files per batch operation:

```
┌─ File Limit Warning ──────────────────────────────────────┐
│                                                           │
│  This operation would modify 15 files.                    │
│  Maximum per batch: 10                                    │
│                                                           │
│  [s] Split into 2 batches                                 │
│  [p] Pick 10 most important files                         │
│  [a] Abort operation                                      │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### Circuit Breaker

If 3+ consecutive errors during implementation:
1. Pause execution
2. Checkpoint progress
3. Show error summary
4. Offer recovery options
</safety>

<resume>
## Resume Interrupted Session

When craft detects existing hammer-state.json:

```
┌─ Hammer Mode In Progress ─────────────────────────────────┐
│                                                           │
│  Feature: "{feature}"                                     │
│  Phase: {current_phase}                                   │
│  Started: {time ago}                                      │
│                                                           │
│  Options:                                                 │
│  1. Resume from current phase                             │
│  2. Abandon and start fresh                               │
│  3. Switch to chisel mode for quick work                  │
│                                                           │
└───────────────────────────────────────────────────────────┘
```
</resume>

<escalation_from>
## Escalation from Debug/Explore

When Debug or Explore mode discovers architectural needs:

1. **Checkpoint findings** to craft-state.md
2. **Log signal**: `DEBUG_ESCALATED` or `EXPLORE_ESCALATED`
3. **Show handoff summary**:
   ```
   ┌─ Escalating to Hammer Mode ─────────────────────────────────┐
   │                                                             │
   │  Findings preserved: grimoires/sigil/craft-state.md        │
   │                                                             │
   │  Key discoveries:                                           │
   │  • {discovery 1}                                            │
   │  • {discovery 2}                                            │
   │                                                             │
   │  These findings will seed /plan-and-analyze.               │
   │                                                             │
   │  Proceed with Hammer sequence? (y/n)                        │
   │                                                             │
   └─────────────────────────────────────────────────────────────┘
   ```
4. **Seed PRD**: Pass findings to `/plan-and-analyze` context
</escalation_from>

<error_handling>
## Error Handling

| Error | Recovery |
|-------|----------|
| Loa command fails | Retry once, then pause with diagnostic |
| Artifact generation incomplete | Offer to regenerate or skip |
| Context exhausted | Checkpoint to craft-state.md, resume later |
| User aborts | Save progress, offer resume path |

### Failure Box

```
┌─ Hammer Error ─────────────────────────────────────────────┐
│                                                            │
│  Phase {phase} encountered an error:                       │
│  {error description}                                       │
│                                                            │
│  Progress saved to: grimoires/loa/hammer-state.json       │
│                                                            │
│  [r] Retry this phase                                      │
│  [s] Skip and continue                                     │
│  [p] Pause (resume with /craft later)                      │
│  [a] Abort hammer mode                                     │
│                                                            │
└────────────────────────────────────────────────────────────┘
```
</error_handling>

<examples>
## Examples

### Example: Fresh Start

```
User: /craft "build rewards claiming feature"

[Scope Detection: Score = 4]
• "build" (+1)
• "feature" (+1)
• "claiming" implies contract interaction (+1)
• "rewards" implies financial (+1)

┌─ Scope Detection ─────────────────────────────────────────┐
│  This looks like HAMMER work...                           │
│  [Proceed with Hammer] [Chisel anyway]                    │
└───────────────────────────────────────────────────────────┘

User: Proceed with Hammer

[Initializing hammer-state.json...]
[Aggregating Sigil context...]
[Invoking /plan-and-analyze with seeded context...]

... [PRD interview runs] ...
... [SDD design runs] ...
... [Sprint planning runs] ...

┌─ Hammer Plan Complete ────────────────────────────────────┐
│  Ready to implement. Run: /run sprint-plan               │
└───────────────────────────────────────────────────────────┘
```

### Example: Using Existing Artifacts

```
User: /craft "implement notification system"

[Checking existing artifacts...]

┌─ Existing Artifacts Detected ────────────────────────────┐
│  PRD: grimoires/loa/prd.md (2 days old) ✓ relevant      │
│  SDD: grimoires/loa/sdd.md (2 days old) ✓ relevant      │
│                                                          │
│  Options:                                                │
│  1. Use existing → Skip to sprint planning               │
│  ...                                                     │
└──────────────────────────────────────────────────────────┘

User: 1

[Using existing PRD and SDD...]
[Invoking /sprint-plan...]
```

### Example: Chisel Override

```
User: /craft "build portfolio dashboard"

[Scope Detection: HAMMER (score = 2)]

User: Chisel anyway

⚠ Proceeding chisel-only. Supporting infrastructure not included.

[Falls back to chisel workflow...]
```

### Example: Debug Escalation

```
User: /craft "fix the rewards not showing up"

[Mode Detection: DEBUG]
[Investigation reveals missing backend infrastructure]

┌─ Scope Check ──────────────────────────────────────────────────┐
│  Root cause type: ARCHITECTURE (missing infrastructure)       │
│  This requires Hammer mode (full-stack implementation).       │
└────────────────────────────────────────────────────────────────┘

User: Escalate to Hammer

[Checkpointing findings...]
[Escalating to Hammer Mode...]
[Seeding /plan-and-analyze with investigation findings...]
```
</examples>
