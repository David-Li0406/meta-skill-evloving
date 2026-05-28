---
name: project-progress-tracking
description: Use this skill to check project progress, summarize recent work, and route to the next action, whether executing an existing plan or creating a new one.
---

# Objective
Check project progress, summarize recent work and what's ahead, then intelligently route to the next action - either executing an existing plan or creating the next one. Provides situational awareness before continuing work.

# Process

## Step 1: Verify Planning Structure
**Verify planning structure exists:**

- If no `.planning/` directory:
  ```
  No planning structure found.
  Run /ag4:new-project to start a new project.
  ```
  Exit.

- If missing `STATE.md`: suggest `/ag4:new-project`.

- If `ROADMAP.md` is missing but `PROJECT.md` exists: Go to **Route F** (between milestones).

- If missing both `ROADMAP.md` and `PROJECT.md`: suggest `/ag4:new-project`.

## Step 2: Load Full Project Context
**Load full project context:**
- Read `.planning/STATE.md` for living memory (position, decisions, issues).
- Read `.planning/ROADMAP.md` for phase structure and objectives.
- Read `.planning/PROJECT.md` for current state (What This Is, Core Value, Requirements).

## Step 3: Gather Recent Work Context
**Gather recent work context:**
- Find the 2-3 most recent `SUMMARY.md` files.
- Extract from each: what was accomplished, key decisions, any issues logged.

## Step 4: Parse Current Position
**Parse current position:**
- From `STATE.md`: current phase, plan number, status.
- Calculate: total plans, completed plans, remaining plans.
- Note any blockers or concerns.
- Check for `CONTEXT.md`: For phases without `PLAN.md` files, check if `{phase}-CONTEXT.md` exists in phase directory.
- Count pending todos: `ls .planning/todos/pending/*.md 2>/dev/null | wc -l`.
- Check for active debug sessions: `ls .planning/debug/*.md 2>/dev/null | grep -v resolved | wc -l`.

## Step 5: Present Rich Status Report
**Present rich status report:**
```
# [Project Name]

**Progress:** [████████░░] 8/10 plans complete

## Recent Work
- [Phase X, Plan Y]: [what was accomplished - 1 line]
- [Phase X, Plan Z]: [what was accomplished - 1 line]

## Current Position
Phase [N] of [total]: [phase-name]
Plan [M] of [phase-total]: [status]
CONTEXT: [✓ if CONTEXT.md exists | - if not]

## Key Decisions Made
- [decision 1 from STATE.md]
- [decision 2]

## Blockers/Concerns
- [any blockers or concerns from STATE.md]

## Pending Todos
- [count] pending — /ag4:check-todos to review

## Active Debug Sessions
- [count] active — /ag4:debug to continue
(Only show this section if count > 0)

## What's Next
[Next phase/plan objective from ROADMAP]
```

## Step 6: Determine Next Action Based on Verified Counts
**Determine next action based on verified counts:**

### Step 6.1: Count Plans, Summaries, and Issues in Current Phase
List files in the current phase directory:
```bash
ls -1 .planning/phases/[current-phase-dir]/*-PLAN.md 2>/dev/null | wc -l
ls -1 .planning/phases/[current-phase-dir]/*-SUMMARY.md 2>/dev/null | wc -l
ls -1 .planning/phases/[current-phase-dir]/*-UAT.md 2>/dev/null | wc -l
```
State: "This phase has {X} plans, {Y} summaries."

### Step 6.2: Check for Unaddressed UAT Gaps
Check for UAT.md files with status "diagnosed" (has gaps needing fixes).
```bash
grep -l "status: diagnosed" .planning/phases/[current-phase-dir]/*-UAT.md 2>/dev/null
```
Track:
- `uat_with_gaps`: UAT.md files with status "diagnosed" (gaps need fixing).

### Step 6.3: Route Based on Counts
| Condition                       | Meaning                 | Action            |
| ------------------------------- | ----------------------- | ----------------- |
| uat_with_gaps > 0               | UAT gaps need fix plans | Go to **Route E** |
| summaries < plans               | Unexecuted plans exist  | Go to **Route A** |
| summaries = plans AND plans > 0 | Phase complete          | Go to Step 7      |
| plans = 0                       | Phase not yet planned   | Go to **Route B** |

---

### Route A: Unexecuted Plan Exists
Find the first `PLAN.md` without matching `SUMMARY.md`. Read its `<objective>` section.
```
---

## ▶ Next Up

**{phase}-{plan}: [Plan Name]** — [objective summary from PLAN.md]

`/ag4:execute-plan [full-path-to-PLAN.md]`

<sub>`/clear` first → fresh context window</sub>

---
```

### Route B: Phase Needs Planning
Check if `{phase}-CONTEXT.md` exists in phase directory.
- If `CONTEXT.md` exists:
```
---

## ▶ Next Up

**Phase {N}: {Name}** — {Goal from ROADMAP.md}
<sub>✓ Context gathered, ready to plan</sub>

`/ag4:plan-phase {phase-number}`

<sub>`/clear` first → fresh context window</sub>

---
```
- If `CONTEXT.md` does NOT exist:
```
---

## ▶ Next Up

**Phase {N}: {Name}** — {Goal from ROADMAP.md}

`/ag4:plan-phase {phase}`

<sub>`/clear` first → fresh context window</sub>

---

**Also available:**
- `/ag4:discuss-phase {phase}` — gather context first
- `/ag4:research-phase {phase}` — investigate unknowns
- `/ag4:list-phase-assumptions {phase}` — see assumptions

---
```

### Route E: UAT Gaps Need Fix Plans
UAT.md exists with gaps (diagnosed issues). User needs to plan fixes.
```
---

## ⚠ UAT Gaps Found

**{phase}-UAT.md** has {N} gaps requiring fixes.

`/ag4:plan-phase {phase} --gaps`

<sub>`/clear` first → fresh context window</sub>

---

**Also available:**
- `/ag4:execute-plan [path]` — continue with other work first
- `/ag4:verify-work {phase}` — run more UAT testing

---
```

## Step 7: Check Milestone Status (Only When Phase Complete)
Read `ROADMAP.md` and identify:
1. Current phase number
2. All phase numbers in the current milestone section

Count total phases and identify the highest phase number.
State: "Current phase is {X}. Milestone has {N} phases (highest: {Y})."

### Route Based on Milestone Status
| Condition                     | Meaning            | Action            |
| ----------------------------- | ------------------ | ----------------- |
| current phase < highest phase | More phases remain | Go to **Route C** |
| current phase = highest phase | Milestone complete | Go to **Route D** |

---

### Route C: Phase Complete, More Phases Remain
Read `ROADMAP.md` to get the next phase's name and goal.
```
---

## ✓ Phase {Z} Complete

## ▶ Next Up

**Phase {Z+1}: {Name}** — {Goal from ROADMAP.md}

`/ag4:plan-phase {Z+1}`

<sub>`/clear` first → fresh context window</sub>

---

**Also available:**
- `/ag4:verify-work {Z}` — user acceptance test before continuing
- `/ag4:discuss-phase {Z+1}` — gather context first
- `/ag4:research-phase {Z+1}` — investigate unknowns

---
```

### Route D: Milestone Complete
```
---

## 🎉 Milestone Complete

All {N} phases finished!

## ▶ Next Up

**Complete Milestone** — archive and prepare for next

`/ag4:complete-milestone`

<sub>`/clear` first → fresh context window</sub>

---

**Also available:**
- `/ag4:verify-work` — user acceptance test before completing milestone

---
```

### Route F: Between Milestones
A milestone was completed and archived. Ready to start the next milestone cycle.
Read `MILESTONES.md` to find the last completed milestone version.
```
---

## ✓ Milestone v{X.Y} Complete

Ready to plan the next milestone.

## ▶ Next Up

**Discuss Next Milestone** — figure out what to build next

`/ag4:discuss-milestone`

<sub>`/clear` first → fresh context window</sub>

---

**Next milestone flow:**
1. `/ag4:discuss-milestone` — thinking partner, creates context file
2. `/ag4:new-milestone` — update PROJECT.md with new goals
3. `/ag4:research-project` — (optional) research ecosystem
4. `/ag4:define-requirements` — scope what to build
5. `/ag4:create-roadmap` — plan how to build it

---
```

## Step 8: Handle Edge Cases
**Handle edge cases:**
- Phase complete but next phase not planned → offer `/ag4:plan-phase [next]`.
- All work complete → offer milestone completion.
- Blockers present → highlight before offering to continue.
- Handoff file exists → mention it, offer `/ag4:resume-work`.

# Success Criteria
- [ ] Rich context provided (recent work, decisions, issues).
- [ ] Current position clear with visual progress.
- [ ] What's next clearly explained.
- [ ] Smart routing: `/ag4:execute-plan` if plans exist, `/ag4:plan-phase` if not.
- [ ] User confirms before any action.
- [ ] Seamless handoff to appropriate command.