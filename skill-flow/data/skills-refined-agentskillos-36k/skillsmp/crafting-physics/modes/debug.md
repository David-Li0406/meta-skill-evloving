# Debug Mode — Systematic Investigation

Debug mode provides systematic investigation for issues, bugs, and problems.

<when_to_use>
## When Debug Activates

**Keyword Triggers:**
- "fix", "debug", "broken", "failing", "error", "not working"
- "investigate", "diagnose", "figure out"

**Context Triggers:**
- craft-state.md shows iteration 3+ with PARTIAL results
- Loop detection triggered
- User reports something is "off"
</when_to_use>

<mode_confirmation>
## Mode Confirmation

```
┌─ Mode: DEBUG ─────────────────────────────────────────────┐
│                                                           │
│  Detected: {keywords found}                               │
│                                                           │
│  I'll investigate systematically:                         │
│  1. Reproduce the issue                                   │
│  2. Identify root cause                                   │
│  3. Propose fix                                           │
│  4. Verify resolution                                     │
│                                                           │
│  [Proceed] [Switch to Chisel] [Switch to Explore]         │
│                                                           │
└───────────────────────────────────────────────────────────┘
```
</mode_confirmation>

<workflow>
## Debug Workflow

### Step D1: Understand the Problem

1. **Parse the error/issue description:**
   - Extract error messages, stack traces
   - Identify affected files/components
   - Note reproduction steps if provided

2. **Gather context:**
   ```
   Read relevant error logs
   Read mentioned files
   Check recent changes (git diff, git log)
   ```

3. **Show understanding:**
   ```
   ┌─ Debug Analysis ───────────────────────────────────────────┐
   │                                                            │
   │  Issue: [description]                                      │
   │  Affected: [files/components]                              │
   │  Error: [key error message if present]                     │
   │                                                            │
   │  Hypothesis: [initial theory based on signals]             │
   │                                                            │
   │  Investigation plan:                                       │
   │  1. [first thing to check]                                 │
   │  2. [second thing to check]                                │
   │  3. [third thing to check]                                 │
   │                                                            │
   │  Proceed with investigation? (y/n)                         │
   │                                                            │
   └────────────────────────────────────────────────────────────┘
   ```

### Step D2: Investigate

1. **Follow the investigation plan:**
   - Check each item systematically
   - Document findings as you go
   - Update hypothesis if evidence contradicts

2. **Root cause identification:**
   - Trace the issue to its source
   - Verify with evidence (logs, code, tests)
   - Consider edge cases

3. **Check for escalation triggers:**
   - If > 5 files touched, or 2+ systems involved → Show Scope Check
   - If root cause is architectural → Suggest escalation to Hammer
   - If investigation depth > 3 "why" levels → Checkpoint findings

4. **Show findings:**
   ```
   ┌─ Root Cause Found ─────────────────────────────────────────┐
   │                                                            │
   │  Root cause: [description]                                 │
   │  Location: [file:line]                                     │
   │  Evidence: [what confirmed this]                           │
   │                                                            │
   │  Proposed fix:                                             │
   │  [description of fix]                                      │
   │                                                            │
   │  Apply fix? (y/n)                                          │
   │                                                            │
   └────────────────────────────────────────────────────────────┘
   ```

### Step D3: Fix and Verify

1. **Apply the fix:**
   - Make minimal, targeted changes
   - Preserve existing behavior where possible
   - Add guards against recurrence if appropriate

2. **Verify resolution:**
   - Run relevant tests if available
   - Manually verify if needed
   - Check for side effects

3. **Log to taste.md:**
   ```markdown
   ## [YYYY-MM-DD HH:MM] | DEBUG_RESOLVED
   Issue: [description]
   Root cause: [cause]
   Fix: [what was changed]
   Files: [files modified]
   ---
   ```
</workflow>

<error_handling>
## Error Handling

| Situation | Recovery |
|-----------|----------|
| Can't reproduce | Ask for more details, check environment differences |
| Multiple possible causes | Investigate each, prioritize by likelihood |
| Fix doesn't work | Re-analyze, check assumptions |
| Out of scope | Suggest escalation, document findings |

**If stuck:**
```
┌─ Investigation Blocked ───────────────────────────────────────┐
│                                                               │
│  I've checked [what was checked] but can't identify the root  │
│  cause. The issue might require:                              │
│                                                               │
│  • More context about [specific thing]                        │
│  • Access to [logs/systems not available]                     │
│  • Domain expertise in [area]                                 │
│                                                               │
│  What I've learned so far:                                    │
│  [summary of findings]                                        │
│                                                               │
│  [Provide more context] [Try different approach] [Stop here]  │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```
</error_handling>

<escalation>
## Escalation Protocol

During investigation, watch for these signals:

| Signal | Threshold | Indicates |
|--------|-----------|-----------|
| **Files touched** | > 5 files | Cross-cutting concern |
| **Domain boundaries** | 2+ systems involved | Integration work |
| **Missing infrastructure** | API/indexer/contract needed | Full-stack work |
| **Root cause is architectural** | Design flaw, not bug | Needs redesign |
| **Investigation depth** | 3+ levels of "why" | Systemic issue |

### Mid-Investigation Check

```
┌─ Scope Check ──────────────────────────────────────────────────┐
│                                                                │
│  Investigation scope has grown:                                │
│  • Files examined: [count]                                     │
│  • Systems involved: [list]                                    │
│  • Root cause type: [bug | design | architecture]              │
│                                                                │
│  This may require Hammer mode (full architecture).             │
│                                                                │
│  Options:                                                      │
│  1. Continue debugging (local fix)                             │
│  2. Escalate to Hammer (preserve findings, plan architecture)  │
│  3. Document and stop (hand off to human)                      │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Delta-Synthesis (Preserve Findings)

When escalating, checkpoint findings to `grimoires/sigil/craft-state.md`:

```markdown
## [YYYY-MM-DD HH:MM] | INVESTIGATION_CHECKPOINT

### Context
Mode: Debug
Original request: [user's request]

### Findings So Far
- [Finding 1 with file:line evidence]
- [Finding 2 with file:line evidence]

### Hypothesis
[Current understanding of the issue]

### Escalation Reason
[Why this needs architecture vs. local fix]

### Recommended Next Mode
Hammer

### Seed Context for Next Mode
[Key information to pass forward]
---
```

### Lightweight Identifiers

Use file:line references instead of copying full content:
```
${PROJECT_ROOT}/src/auth/middleware.ts:45-89 (session validation)
${PROJECT_ROOT}/src/api/routes.ts:120 (route protection)
```
</escalation>

<loop_detection>
## Loop Detection Integration

When Debug mode is triggered from loop detection:

```
┌─ Craft Loop Detected ──────────────────────────────────────┐
│                                                            │
│  Pattern: {each_fix_reveals_new_issue | repeated_fix |     │
│           stuck_hypothesis}                                │
│                                                            │
│  Iteration history:                                        │
│  • Iteration 1: {what happened}                            │
│  • Iteration 2: {what happened}                            │
│  • Iteration 3: {what happened}                            │
│                                                            │
│  This suggests: {interpretation}                           │
│                                                            │
│  Recommended actions:                                      │
│  [d] /observe diagnose — Capture user context              │
│  [u] /understand — Research the domain                     │
│  [p] /plan-and-analyze — Rethink requirements              │
│  [c] Continue debugging (risky)                            │
│                                                            │
└────────────────────────────────────────────────────────────┘
```
</loop_detection>

<examples>
## Examples

### Example: Deployment Issue

```
User: /craft "fix the docs deployment, build is failing"

[Mode Detection: DEBUG]

┌─ Debug Analysis ───────────────────────────────────────────┐
│                                                            │
│  Issue: Docs deployment build failing                      │
│  Affected: Build pipeline, docs site                       │
│                                                            │
│  Hypothesis: Configuration or dependency issue             │
│                                                            │
│  Investigation plan:                                       │
│  1. Check recent commits to docs config                    │
│  2. Review build logs for specific error                   │
│  3. Verify dependencies are up to date                     │
│                                                            │
│  Proceed with investigation? (y/n)                         │
│                                                            │
└────────────────────────────────────────────────────────────┘

User: y

[Reading build logs...]
[Checking vocs.config.ts...]

┌─ Root Cause Found ─────────────────────────────────────────┐
│                                                            │
│  Root cause: Invalid sidebar configuration                 │
│  Location: vocs.config.ts:47                               │
│  Evidence: Build error "Cannot read property of undefined" │
│                                                            │
│  Proposed fix:                                             │
│  Add null check for sidebar items                          │
│                                                            │
│  Apply fix? (y/n)                                          │
│                                                            │
└────────────────────────────────────────────────────────────┘

User: y

[Applies fix, verifies build passes]
[Logs DEBUG_RESOLVED to taste.md]
```

### Example: Can't Identify Root Cause

```
User: /craft "debug the intermittent crash on mobile"

[Mode Detection: DEBUG]

... [investigation proceeds] ...

┌─ Investigation Blocked ───────────────────────────────────────┐
│                                                               │
│  I've checked crash logs, recent changes, and device-specific │
│  code but can't identify the root cause. The issue might      │
│  require:                                                     │
│                                                               │
│  • More context about reproduction steps                      │
│  • Access to device-specific crash reports                    │
│  • Real device testing (not simulator)                        │
│                                                               │
│  What I've learned so far:                                    │
│  - Crash only occurs on iOS 16+                               │
│  - Related to animation timing                                │
│  - Memory pressure may be a factor                            │
│                                                               │
│  [Provide more context] [Try different approach] [Stop here]  │
│                                                               │
└───────────────────────────────────────────────────────────────┘

User: The crash happens when scrolling fast through a long list

[Updates hypothesis with new information...]
[Continues investigation...]
```

### Example: Escalation to Hammer

```
User: /craft "fix the rewards not showing up"

[Mode Detection: DEBUG]
[Investigation proceeds...]
[Discovers: Frontend exists, backend infrastructure missing]

┌─ Scope Check ──────────────────────────────────────────────────┐
│                                                                │
│  Investigation scope has grown:                                │
│  • Files examined: 7                                           │
│  • Systems involved: Frontend, API, Indexer, Contract          │
│  • Root cause type: ARCHITECTURE (missing infrastructure)      │
│                                                                │
│  The rewards feature is incomplete:                            │
│  - Contract emits RewardsClaimed event ✓                       │
│  - Indexer handler: MISSING                                    │
│  - API endpoint: MISSING                                       │
│  - Frontend hook: calls non-existent API                       │
│                                                                │
│  This requires Hammer mode (full-stack implementation).        │
│                                                                │
│  Options:                                                      │
│  1. Continue debugging (won't help — infrastructure missing)   │
│  2. Escalate to Hammer (preserve findings, plan architecture)  │
│  3. Document and stop (hand off to human)                      │
│                                                                │
└────────────────────────────────────────────────────────────────┘

User: 2

[Checkpointing findings to craft-state.md...]
[Logging DEBUG_ESCALATED...]
[Escalating to Hammer Mode with preserved findings...]
```
</examples>
