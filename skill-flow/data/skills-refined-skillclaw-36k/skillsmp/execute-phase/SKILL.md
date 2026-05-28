---
name: execute-phase
description: Execute all plans in a phase with wave-based parallelization
argument-hint: "<phase-number>"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
  - TodoWrite
  - AskUserQuestion
---

<objective>
Execute all plans in a phase using wave-based parallel execution.

Orchestrator stays lean: discover plans, analyze dependencies, group into waves, spawn subagents, collect results. Each subagent loads the full execute-plan context and handles its own plan.

Context budget: ~15% orchestrator, 100% fresh per subagent.
</objective>

<execution_context>
@~/.claude/ag4one/references/principles.md
@~/.claude/ag4one/workflows/execute-phase.md
</execution_context>

<context>
Phase: $ARGUMENTS

@.planning/ROADMAP.md
@.planning/STATE.md
</context>

<process>
1. **Validate phase exists**
   - Find phase directory matching argument
   - Count PLAN.md files
   - Error if no plans found

2. **Discover plans**
   - List all *-PLAN.md files in phase directory
   - Check which have *-SUMMARY.md (already complete)
   - Build list of incomplete plans

3. **Group by wave**
   - Read `wave` from each plan's frontmatter
   - Group plans by wave number
   - Report wave structure to user

4. **Execute waves**
   For each wave in order:
   - Spawn `ag4-executor` for each plan in wave (parallel Task calls)
   - Wait for completion (Task blocks)
   - Verify SUMMARYs created
   - Proceed to next wave

5. **Aggregate results**
   - Collect summaries from all plans
   - Report phase completion status

6. **Verify phase goal**
   - Spawn `ag4-verifier` subagent with phase directory and goal
   - Verifier checks must_haves against actual codebase (not SUMMARY claims)
   - Creates VERIFICATION.md with detailed report
   - Route by status:
     - `passed` → continue to step 7
     - `human_needed` → present items, get approval or feedback
     - `gaps_found` → present gaps, offer `/ag4:plan-phase {X} --gaps`

7. **Update roadmap and state**
   - Update ROADMAP.md, STATE.md

8. **Update requirements**
   Mark phase requirements as Complete:
   - Read ROADMAP.md, find this phase's `Requirements:` line (e.g., "AUTH-01, AUTH-02")
   - Read REQUIREMENTS.md traceability table
   - For each REQ-ID in this phase: change Status from "Pending" to "Complete"
   - Write updated REQUIREMENTS.md
   - Skip if: REQUIREMENTS.md doesn't exist, or phase has no Requirements line

9. **Commit phase completion**
   Bundle all phase metadata updates in one commit:
   - Stage: `git add .planning/ROADMAP.md .planning/STATE.md`
   - Stage REQUIREMENTS.md if updated: `git add .planning/REQUIREMENTS.md`
   - Commit: `docs({phase}): complete {phase-name} phase`

10. **Offer next steps**
    - Route to next action (see `<offer_next>`)
</process>

<offer_next>
**MANDATORY: Present copy/paste-ready next command.**

After verification completes, route based on status:

| Status | Route |
|--------|-------|
| `gaps_found` | Route C (gap closure) |
| `human_needed` | Present checklist, then re-route based on approval |
| `passed` + more phases | Route A (next phase) |
| `passed` + last phase | Route B (milestone complete) |

---

**Route A: Phase verified, more phases remain**

```
## ✓ Phase {Z}: {Name} Complete

All {Y} plans finished. Phase goal verified.

---

## ▶ Next Up

**Phase {Z+1}: {Name}** — {Goal from ROADMAP.md}

`/ag4:plan-phase {Z+1}`

<sub>`/clear` first → fresh context window</sub>

---

**Also available:**
- `/ag4:verify-work {Z}` — manual acceptance testing before continuing
- `/ag4:discuss-phase {Z+1}` — gather context first
- `/ag4:research-phase {Z+1}` — investigate unknowns

---
```

---

**Route B: Phase verified, milestone complete**

```
🎉 ALL PHASES COMPLETE!

## ✓ Phase {Z}: {Name} Complete

All {N} phases finished. Phase goals verified.

---

## ▶ Next Up

**Audit milestone** — verify requirements, cross-phase integration, E2E flows

`/ag4:audit-milestone`

<sub>`/clear` first → fresh context window</sub>

---

**Also available:**
- `/ag4:verify-work` — manual acceptance testing
- `/ag4:complete-milestone` — skip audit, archive directly
- `/ag4:add-phase <description>` — add another phase first

---
```

---

**Route C: Gaps found — need additional planning**

```
## ⚠ Phase {Z}: {Name} — Gaps Found

**Score:** {N}/{M} must-haves verified
**Report:** .planning/phases/{phase_dir}/{phase}-VERIFICATION.md

### What's Missing

{Extract gap summaries from VERIFICATION.md}

---

## ▶ Next Up

**Plan gap closure** — create additional plans to complete the phase

`/ag4:plan-phase {Z} --gaps`

<sub>`/clear` first → fresh context window</sub>

---

**Also available:**
- `cat .planning/phases/{phase_dir}/{phase}-VERIFICATION.md` — see full report
- `/ag4:verify-work {Z}` — manual testing before planning

---
```

After user runs `/ag4:plan-phase {Z} --gaps`:
1. Planner reads VERIFICATION.md gaps
2. Creates plans 04, 05, etc. to close gaps
3. User runs `/ag4:execute-phase {Z}` again
4. Execute-phase runs incomplete plans (04, 05...)
5. Verifier runs again → loop until passed
</offer_next>

<wave_execution>
**Parallel spawning:**

Spawn all plans in a wave with a single message containing multiple Task calls:

```
Task(prompt="Execute plan at {plan_01_path}\n\nPlan: @{plan_01_path}\nProject state: @.planning/STATE.md", subagent_type="ag4-executor")
Task(prompt="Execute plan at {plan_02_path}\n\nPlan: @{plan_02_path}\nProject state: @.planning/STATE.md", subagent_type="ag4-executor")
Task(prompt="Execute plan at {plan_03_path}\n\nPlan: @{plan_03_path}\nProject state: @.planning/STATE.md", subagent_type="ag4-executor")
```

All three run in parallel. Task tool blocks until all complete.

**No polling.** No background agents. No TaskOutput loops.
</wave_execution>

<checkpoint_handling>
Plans with `autonomous: false` have checkpoints. The execute-phase.md workflow handles the full checkpoint flow:
- Subagent pauses at checkpoint, returns structured state
- Orchestrator presents to user, collects response
- Spawns fresh continuation agent (not resume)

See `@~/.claude/ag4one/workflows/execute-phase.md` step `checkpoint_handling` for complete details.
</checkpoint_handling>

<deviation_rules>
During execution, handle discoveries automatically:

1. **Auto-fix bugs** - Fix immediately, document in Summary
2. **Auto-add critical** - Security/correctness gaps, add and document
3. **Auto-fix blockers** - Can't proceed without fix, do it and document
4. **Ask about architectural** - Major structural changes, stop and ask user

Only rule 4 requires user intervention.
</deviation_rules>

<commit_rules>
**Per-Task Commits:**

After each task completes:
1. Stage only files modified by that task
2. Commit with format: `{type}({phase}-{plan}): {task-name}`
3. Types: feat, fix, test, refactor, perf, chore
4. Record commit hash for SUMMARY.md

**Plan Metadata Commit:**

After all tasks in a plan complete:
1. Stage plan artifacts only: PLAN.md, SUMMARY.md
2. Commit with format: `docs({phase}-{plan}): complete [plan-name] plan`
3. NO code files (already committed per-task)

**Phase Completion Commit:**

After all plans in phase complete (step 7):
1. Stage: ROADMAP.md, STATE.md, REQUIREMENTS.md (if updated), VERIFICATION.md
2. Commit with format: `docs({phase}): complete {phase-name} phase`
3. Bundles all phase-level state updates in one commit

**NEVER use:**
- `git add .`
- `git add -A`
- `git add src/` or any broad directory

**Always stage files individually.**
</commit_rules>

<success_criteria>
- [ ] All incomplete plans in phase executed
- [ ] Each plan has SUMMARY.md
- [ ] Phase goal verified (must_haves checked against codebase)
- [ ] VERIFICATION.md created in phase directory
- [ ] STATE.md reflects phase completion
- [ ] ROADMAP.md updated
- [ ] REQUIREMENTS.md updated (phase requirements marked Complete)
- [ ] User informed of next steps
</success_criteria>
