---
name: brainstorm
description: Brainstorm Business Goal into Milestones, Outcomes, and Work Units
allowed-tools: Read, Grep, Glob, mcp__linear-server__get_project, mcp__linear-server__create_project, mcp__linear-server__list_projects, mcp__linear-server__list_issues, mcp__linear-server__get_issue, mcp__linear-server__create_issue, mcp__linear-server__update_issue, mcp__linear-server__list_teams
---

# Brainstorm: Business Goal → Milestones → Outcomes → Work Units

Help user turn a business goal into well-defined Milestones, Outcomes, and Work Units.

**Linear Hierarchy:**
```
Project (Business Goal)
└── Milestone (Epic - major deliverable, optional target date)
    └── Issue (Outcome - user-facing value with success metric)
        └── Sub-issue (Work Unit - implementation with Gherkin specs)
```

| Level | Linear Object | What It Represents | Example |
|-------|---------------|-------------------|---------|
| Project | Project | Business Goal | "Land Intelligence App V1" |
| Milestone | Milestone | Epic / Major Deliverable | "User Authentication" |
| Outcome | Issue | User-facing value | "User can register" |
| Work Unit | Sub-issue | Implementation task | "WU: Registration API" |

## Usage
```
/brainstorm [initiative-name or goal description]
/brainstorm --status "Project Name"
```

## Important: Using Linear MCP

Use Linear MCP tools as direct function calls, NOT bash commands.

---

## Status Mode: `--status`

When invoked with `--status "Project Name"`, skip the brainstorm workflow and show current project state.

### How to Fetch Status

1. Find the project:
   ```
   mcp__linear-server__list_projects
   ```
   Match by name to get project ID.

2. Fetch all issues for the project:
   ```
   mcp__linear-server__list_issues:
     project: [project ID]
     includeArchived: false
   ```

3. For each issue, fetch details including relations:
   ```
   mcp__linear-server__get_issue:
     id: [issue ID]
     includeRelations: true
   ```

### Status Report Format

Present the status grouped by Milestone:

```
## Project Status: [Project Name]

**Overall Progress:** X of Y Work Units complete (Z%)

---

### Milestone: [Milestone 1 Name] 🎯
**Target:** [date or "No target"]
**Progress:** A of B Work Units (C%)

| Status | Issue | Title | Blocked By |
|--------|-------|-------|------------|
| ✅ | BHU-101 | [Outcome 1] | — |
| ✅ | └─ BHU-102 | WU: [title] | — |
| 🔄 | BHU-103 | [Outcome 2] | — |
| ⬜ | └─ BHU-104 | WU: [title] | BHU-102 |

---

### Milestone: [Milestone 2 Name] 🎯
**Target:** [date]
**Progress:** 0 of D Work Units (0%)
**Blocked by:** Milestone 1

| Status | Issue | Title | Blocked By |
|--------|-------|-------|------------|
| 🔴 | BHU-201 | [Outcome 3] | BHU-103 |

---

### Summary

| Milestone | Progress | Target | Status |
|-----------|----------|--------|--------|
| [Milestone 1] | 2/4 (50%) | Feb 15 | 🔄 In Progress |
| [Milestone 2] | 0/3 (0%) | Mar 1 | 🔴 Blocked |

### Critical Path
Milestone 1: BHU-102 → BHU-104 (completes milestone)
Then: Milestone 2: BHU-201 → BHU-203

**Next action:** Run `/work BHU-104` to continue Milestone 1.
```

### Status Icons

| Icon | Meaning |
|------|---------|
| ✅ | Completed |
| 🔄 | In Progress |
| 🟢 | Ready to Start (unblocked) |
| 🔴 | Blocked |
| ⬜ | Not Started |

---

## Workflow

### Phase 0: Identify Project

1. Fetch existing projects via `mcp__linear-server__list_projects`
2. Ask user:
   ```
   Which project should this work go into?
   1. [Project A] (existing)
   2. [Project B] (existing)
   ...
   N. Create new project

   Or specify: /brainstorm --project "Project Name" ...
   ```
3. If new project, get name and create via `mcp__linear-server__create_project`
4. Store project ID for later phases

### Phase 1: Understand the Goal

1. If user provided goal description, clarify it
2. Ask clarifying questions ONE AT A TIME:
   - What problem are we solving?
   - Who benefits? (user segment)
   - What does success look like?
   - Any constraints? (time, tech, scope)
3. Summarize understanding, confirm with user

### Phase 2: Propose Milestones

Milestones are major deliverables — significant chunks of functionality that can be shipped or demonstrated.

1. Based on the goal, identify natural phases/epics:
   - What are the major capability areas?
   - What could be shipped incrementally?
   - Are there natural dependencies between areas?

2. Propose 2-5 Milestones:
   ```
   ## Proposed Milestones

   1. **[Milestone name]** (e.g., "User Authentication")
      - Delivers: [what user can do when this is complete]
      - Target: [suggested timeframe or "TBD"]
      - Dependencies: [other milestones that must come first, or "None"]

   2. **[Milestone name]** (e.g., "Land Parcel CRUD")
      - Delivers: [what user can do]
      - Target: [timeframe]
      - Dependencies: [Milestone 1]

   3. **[Milestone name]**
      ...
   ```

3. Ask user to approve, modify, reorder, or remove
4. Confirm milestone sequence and any target dates

### Phase 3: Propose Outcomes (per Milestone)

For each approved Milestone:

**Before proposing, run a Necessity Check for each potential Outcome.**

Every line of code is a liability. The best solution is often no new code at all.

1. For each potential Outcome, investigate:
   - **Existing solution?** Search codebase for similar functionality
   - **Config change?** Could this be achieved by changing settings/env vars?
   - **Library/tool?** Is there an existing package that solves this?
   - **80/20 alternative?** Could we get 80% of the value with 20% of the effort?

2. Propose Outcomes for this Milestone:
   ```
   ## Milestone: [name]

   ### Proposed Outcomes

   1. **[Outcome name]** (e.g., "User can register")
      - Want: [1-2 sentences of user-facing value]
      - Success metric: [measurable]
      - Complexity: Low/Medium/High
      - Necessity check:
        - Existing solution: [None found / Found X but doesn't cover Y]
        - Config alternative: [Not applicable / Considered but Z]
        - Library option: [None suitable / X exists but Y reason not to use]
        - 80/20: [This IS the minimal approach / Could do X instead for less]

   2. **[Outcome name]** (e.g., "User can log in")
      ...
   ```

3. Ask user to approve, modify, or remove each Outcome
4. Confirm final set before proceeding to Work Units
5. Repeat for each Milestone

### Phase 4: Break Down into Work Units

For each approved Outcome:

1. Explore codebase to understand technical scope
2. Propose Work Units (one per repo — if feature spans repos, create separate linked WUs):
   ```
   ## Outcome: [name]

   Work Units:
   1. WU: [title]
      - Repo: [exact repo name, e.g., bhume-platform, bhume-mobile]
      - Proof type: [tdd/rn-component/dbt-test/infra-runbook]
      - Budget estimate: [small/medium/large]
      - Key scenarios (draft):
        - [scenario 1]
        - [scenario 2]

   2. WU: [title] (if multi-repo)
      - Repo: [different repo]
      - Blocked by: WU-1 (if dependent)
      ...
   ```

   **Multi-repo features:** Create separate Work Units for each repo with explicit dependencies.
   Example: API change (backend repo) → Mobile integration (mobile repo, blocked by API WU)

3. Get user approval on breakdown

### Phase 4.5: Map Dependencies

After all Work Units are approved, identify execution order:

1. Analyze dependencies at multiple levels:
   - **Milestone-level:** Which milestones depend on others?
   - **Outcome-level:** Which outcomes within a milestone depend on others?
   - **Work Unit-level:** Which WUs produce artifacts others need?

2. Present dependency graph:
   ```
   ## Execution Order

   ### Milestone 1: [name]

   Phase 1 (No blockers - can start now):
   - BHU-XXX: [title]
   - BHU-YYY: [title]

   Phase 2 (After Phase 1):
   - BHU-ZZZ: [title] ← blocked by BHU-XXX

   Critical Path: BHU-XXX → BHU-ZZZ → BHU-AAA

   ### Milestone 2: [name] (after Milestone 1)

   Phase 1:
   - BHU-BBB: [title] ← blocked by BHU-AAA (from Milestone 1)
   ```

3. Present summary table:
   ```
   | Milestone | Order | Issue | Title | Blocked By |
   |-----------|-------|-------|-------|------------|
   | Auth | 1 | BHU-XXX | [title] | — |
   | Auth | 2 | BHU-YYY | [title] | BHU-XXX |
   | CRUD | 3 | BHU-ZZZ | [title] | BHU-YYY |
   ```

4. Get user approval on dependencies before creating in Linear

### Phase 5: Create in Linear

**Hierarchy:** Project → Milestone → Issue (Outcome) → Sub-issue (Work Unit)

1. Get team ID via `mcp__linear-server__list_teams`

2. Check if Project exists for this Business Goal, or create one:
   ```
   mcp__linear-server__create_project:
     name: [Business Goal / Initiative name]
     team: [team ID]
     description: [1-2 sentence goal]
   ```

3. For each Milestone, note the name (milestones are created implicitly when first issue references them, or may already exist)

4. For each Outcome, create parent Issue associated with its Milestone:
   ```
   mcp__linear-server__create_issue:
     title: [Outcome name]
     team: [team ID]
     project: [project ID]
     milestone: [Milestone name]
     description: |
       ## Want
       [from approved outcome]

       ## Success Metric
       - Primary: [metric]
       - Secondary: [metric] (optional)

       ## Status
       - [ ] Work Units defined
       - [ ] Work Units complete
       - [ ] Success metric verified
   ```

5. For each Work Unit, create Sub-issue under Outcome (inherits milestone from parent):
   ```
   mcp__linear-server__create_issue:
     title: WU: [title]
     team: [team ID]
     project: [project ID]
     parentId: [Outcome issue ID from step 4]
     milestone: [Milestone name]
     labels: [proof type, budget]
     description: |
       ## Want
       [1-2 sentences]

       ## Repo
       [exact repo name, e.g., bhume-platform]

       ## Done When
       ```gherkin
       Scenario: [from draft scenarios]
         Given ...
         When ...
         Then ...
       ```

       ## Approach
       TBD - agent proposes during /work

       ## Decisions
       <!-- Added during implementation -->
   ```

6. Add blocking relationships from Phase 4.5:
   ```
   mcp__linear-server__update_issue:
     id: [Work Unit issue ID]
     blockedBy: ["BHU-XXX", "BHU-YYY"]  # Issues that must complete first
   ```

   Note: This includes cross-milestone dependencies (e.g., Milestone 2's first WU blocked by Milestone 1's last WU).

### Phase 6: Summary

Report what was created:
```
## Brainstorm Complete

**Project:** [Business Goal name] ([Linear URL])

---

### Milestone 1: [name] 🎯
**Target:** [date]
**Outcomes:** N

- [Outcome 1] ([Linear URL])
  - WU: [title] ([Linear URL])
  - WU: [title] ([Linear URL])
- [Outcome 2] ([Linear URL])
  - WU: [title] ([Linear URL])

### Milestone 2: [name] 🎯
**Target:** [date]
**Blocked by:** Milestone 1
**Outcomes:** M

- [Outcome 3] ([Linear URL])
  - WU: [title] ([Linear URL])

---

## Execution Summary

| Milestone | Outcomes | Work Units | Target |
|-----------|----------|------------|--------|
| [Milestone 1] | 2 | 4 | Feb 15 |
| [Milestone 2] | 1 | 2 | Mar 1 |
| **Total** | **3** | **6** | |

## Start Here (No Blockers)

| Issue | Title | Milestone |
|-------|-------|-----------|
| BHU-XXX | [title] | [Milestone 1] |
| BHU-YYY | [title] | [Milestone 1] |

## Critical Path

```
Milestone 1: BHU-XXX → BHU-ZZZ → BHU-AAA (milestone complete)
     ↓
Milestone 2: BHU-BBB → BHU-CCC (project complete)
```

**Next:** Run `/work BHU-XXX` to begin Milestone 1.
```

---

## Principles

- **One question at a time** — Don't overwhelm
- **User approves each phase** — Don't create without approval
- **Milestones are shippable** — Major deliverables, not arbitrary groupings
- **Outcomes are user-facing** — Not technical tasks
- **Work Units are implementation** — Technical, with Gherkin
- **YAGNI** — Remove anything not essential
- **Dependencies flow down** — Milestones → Outcomes → Work Units

---

## Quick Reference: What Goes Where

| Question | Answer |
|----------|--------|
| "When will Auth be done?" | Check Milestone target date |
| "What can the user do?" | Check Outcomes |
| "What needs to be built?" | Check Work Units |
| "What's blocking progress?" | Check dependencies in Status |
| "What should I work on next?" | Run `/brainstorm --status` |
