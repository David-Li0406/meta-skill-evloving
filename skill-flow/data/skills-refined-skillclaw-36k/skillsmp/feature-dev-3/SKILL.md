---
name: feature-dev
description: >-
  This skill should be used when the user asks to "implement a feature",
  "add a new feature", "develop feature", "refactor module", "upgrade API",
  "migrate database", or invokes "/feature". Also triggers on complex multi-file
  bugfixes, architectural changes, or when user mentions "feature workflow".
  Provides a 5-phase systematic approach: Discovery -> Exploration ->
  Documentation -> Implementation -> Review.
version: 1.0.4
context: fork
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

# Feature Development Workflow

> Systematic feature development: Discovery → Exploration → Documentation → Implementation → Review

## Overview

A comprehensive 5-phase workflow for feature development that emphasizes:
- **Documentation-first**: Spec documents before code
- **Progressive context**: Fork context prevents main session pollution
- **Progress persistence**: Resume interrupted work seamlessly
- **Multi-model agents**: Right model for each task (Haiku/Sonnet/Opus)

## Hard Rules

- Speak with user in **Simplified Chinese**, write all artifacts in **English**
- Do not skip decision gates without explicit user confirmation
- Keep diffs minimal; avoid unrelated refactors
- Update progress.md after each phase transition
- Run verification before marking tasks complete

## Workflow Overview

```
Phase 1: Discovery     ->  Phase 2: Exploration  ->  Phase 3: Documentation
   (clarify & decide)       (understand codebase)     (contracts & specs)
         |                         |                         |
         v                         v                         v
   [GATE: confirm]           [parallel agents]         [GATE: approve]
                                                             |
                                                             v
                              Phase 3c: Readiness Gate (NEW - 95% check)
                                 (structural + semantic scoring)
                                         |
                                         v
                              Phase 4: Implementation  <-  Phase 3b: Tasks
                                 (incremental, verified)    (breakdown)
                                         |
                                         v
                              Phase 5: Review & PR
```

## File Structure

All artifacts live under `.works/spec/{feature-name}/` (gitignored):

```
.works/spec/{feature-name}/
├── progress.md          # Progress tracking (YAML frontmatter + markdown)
├── README.md            # Index + core decisions
├── contracts.md         # Data contracts (input/output/API)
├── tasks.md             # Task breakdown with status
├── PR.md                # PR description template
├── qa.md                # Q&A log (Phase 3c question rounds)
├── score.json           # Readiness scoring results (Track A)
├── semantic-check.json  # Semantic check results (Track B)
├── verification.log     # Test/build output history
├── assumptions.md       # Assumptions pack (if question budget exhausted)
└── spec.lock            # Spec locked marker (created when gate passes)
```

Initialize with: `bash ${CLAUDE_PLUGIN_ROOT}/scripts/init.sh {feature-name}`

---

## Phase 1: Discovery

**Goal**: Transform vague requirements into actionable decisions

**Agents**: `product-thinker` (Opus) for deep product analysis

**Actions**:
1. Initialize workspace with `init.sh {feature-name}`
2. Create progress.md with initial state
3. Ask clarifying questions using numbered format (Q1, Q2...)
4. Record decisions in README.md

**GATE**: Confirm all decisions with user before proceeding.

---

## Phase 2: Codebase Exploration

**Goal**: Understand relevant existing code and patterns

**Agents**: `codebase-explorer` (Haiku, fast) - launch 2-3 in parallel

**Actions**:
1. Launch parallel agents targeting:
   - Similar features and implementation patterns
   - Architecture and abstractions
   - UI patterns and state management
2. Read all key files identified by agents
3. Present comprehensive findings summary
4. Update progress.md
5. if the `ast-grep` tool is exsiting, please use it. here is the Command line usage example :
   ```bash
      ## ast-grep has following form.
      ast-grep --pattern 'var code = $PATTERN' --rewrite 'let code = new $PATTERN' --lang ts
      ## Example : Rewrite code in null coalescing operator
      ast-grep -p '$A && $A()' -l ts -r '$A?.()'
      ## Example : Rewrite Zodios
      ast-grep -p 'new Zodios($URL,  $CONF as const,)' -l ts -r 'new Zodios($URL, $CONF)' -i
   ```

---

## Phase 3: Documentation & Tasks

**Goal**: Create spec documents and task breakdown

**Agents**: `architect` (Sonnet) for implementation blueprint

### Sub-phase 3a: Documentation
1. Write contracts.md with field definitions, types, examples
2. Update README.md with decisions summary

**GATE**: User approves spec documents

### Sub-phase 3b: Task Breakdown
1. Launch `architect` agent for implementation design
2. Split feature into atomic, verifiable tasks in tasks.md
3. Each task: Goal, Size (S/M/L), Files, Acceptance criteria

**GATE**: User confirms task list

---

## Phase 3c: Readiness Gate (95% Confidence)

**Goal**: Verify specification completeness before implementation

**CRITICAL**: Do not proceed to implementation until this gate passes.

### Dual-Track Scoring

The readiness gate uses two complementary checks:

1. **Track A: Structural Scoring** (Deterministic)
   - Checks for required sections, type definitions, test commands
   - Scores 0-100 based on concrete rubric
   - Fast, consistent, no API calls needed

2. **Track B: Semantic Sufficiency** (LLM-based)
   - Checks for ambiguity, hidden assumptions, logical gaps
   - Requires evidence citations from spec
   - Uses Claude API (Haiku model)

### Execution Steps

**1. Run structural scoring**:
```bash
bun run ${CLAUDE_PLUGIN_ROOT}/scripts/score-spec.ts \
  --feature {feature-name} \
  --threshold 95
```
Result written to `.works/spec/{feature}/score.json`

**2. Run semantic check**:
```bash
ANTHROPIC_API_KEY=xxx bun run ${CLAUDE_PLUGIN_ROOT}/scripts/check-semantic.ts \
  --feature {feature-name}
```
Result written to `.works/spec/{feature}/semantic-check.json`

**3. Evaluate gate condition**:
- `readiness_score >= 95` AND `semantic_ok == true`
- If **PASS**: Create `spec.lock` file, update progress, proceed to Phase 4
- If **FAIL**: Go to step 4

**4. Information Gathering (if gate fails)**:

a. Generate blocking questions list:
   - Combine gaps from `score.json` + `semantic-check.json`
   - Filter to blocking items only
   - Max 3-5 questions per round

b. Check question budget:
   - If `question_round < question_budget` (default: 2):
     - Use AskUserQuestion to ask targeted questions
     - Record Q&A in `qa.md`
     - Update `question_round` in progress.md
     - Re-run readiness gate (steps 1-3)
   - If budget exhausted: Go to step 5

**5. Assumptions Pack (budget exhausted)**:

Write to `.works/spec/{feature}/assumptions.md`:
```markdown
## Unresolved Gaps
[List blocking gaps from score.json + semantic-check.json]

## Proposed Assumptions
- Gap: [description]
  Assumption: [what we'll assume]
  Risk: [what could go wrong]

## Acceptance
[ ] User accepts assumptions (allows Phase 4)
[ ] User rejects (requires more info or cancels feature)
```

Use AskUserQuestion with 2 options:
- "Accept assumptions and proceed (Recommended if risks are acceptable)"
- "Provide more information (will ask targeted questions)"

**If accepted**: Mark `assumptions_accepted: true`, create `spec.lock`, proceed to Phase 4
**If rejected**: Output Stuck Report and mark `status: blocked`

**6. Stuck Report format** (if assumptions rejected):
```markdown
# Feature Blocked: {feature-name}

## Blocking Gaps
[List from score.json + semantic-check.json]

## Information Needed
[Specific questions that must be answered]

## Attempts Made
- Question rounds: {question_round}/{question_budget}
- Assumptions offered: Yes
- User response: Rejected assumptions

## Recommendation
Please provide answers to "Information Needed" section, then:
1. Update contracts.md and/or tasks.md with missing info
2. Re-run readiness gate: bun run scripts/score-spec.ts --feature {feature-name}
```

### Gate Pass Criteria

- **Track A**: `readiness_score >= confidence_threshold` (default 95)
- **Track B**: `semantic_ok == true`
- **Combined**: Both must pass

### Post-Gate Actions

When gate passes:
1. Create `.works/spec/{feature}/spec.lock` (empty file, timestamp only)
2. Update progress.md:
   ```bash
   bash ${CLAUDE_PLUGIN_ROOT}/scripts/update-progress.sh {feature-name} \
     --set-field spec_locked=true \
     --set-field phase=4 \
     --set-field phase_name=implementation
   ```
3. Spec files (contracts.md, tasks.md) now protected by write-guard hook

---

## Phase 4: Implementation

**Goal**: Build the feature incrementally

**Workflow**:
```bash
# 1. Create feature branch
git checkout -b feat/{feature-name}

# 2. For each task:
#    - Update tasks.md status to "in_progress"
#    - Implement changes
#    - Run verification
#    - Update tasks.md status to "completed"
#    - Update progress.md

# 3. Periodic verification
bun run check && bun run test
```

**DO NOT START WITHOUT USER APPROVAL**

---

## Phase 5: Review & PR

**Goal**: Ensure quality and submit

**Agents**: `reviewer` (Sonnet) for code quality review

**Actions**:
1. Launch `reviewer` agent to check simplicity, correctness, conventions
2. Present findings and ask user decision (fix now/later/proceed)
3. Final verification: `bun run check && bun run test && bun run build`
4. Create PR with spec reference
5. Update CHANGELOG.md
6. Mark progress.md as completed

---

## Progress Tracking

progress.md uses YAML frontmatter for structured data:

```yaml
---
feature: feature-name
phase: 2
phase_name: exploration
status: in_progress
branch: feat/feature-name
started_at: 2025-01-13T10:00:00Z
updated_at: 2025-01-13T11:30:00Z
decisions:
  - id: Q1
    question: API output format
    answer: JSON with pagination
completed_phases:
  - phase: 1
    completed_at: 2025-01-13T10:30:00Z
---
```

## Resuming Workflow

When resuming an interrupted session:
1. Check for existing progress.md in .works/spec/
2. Read current phase and context
3. Continue from last recorded state
4. Ask user to confirm before proceeding

## Available Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| `product-thinker` | Opus | Deep product decisions, UX analysis |
| `codebase-explorer` | Haiku | Fast codebase exploration |
| `architect` | Sonnet | Architecture design, implementation blueprints |
| `reviewer` | Sonnet | Code quality review |
| `react-coder` | Sonnet | React Code developer  |


## Scripts

| Script | Purpose |
|--------|---------|
| `init.sh` | Initialize feature workspace with all required files |
| `check-progress.sh` | Check for incomplete features (SessionStart hook) |
| `update-progress.sh` | Update progress file (supports --set-field for loop mode) |
| `update-changelog.sh` | Update CHANGELOG.md on completion |
| `score-spec.ts` | Track A: Structural readiness scoring (0-100) |
| `check-semantic.ts` | Track B: Semantic sufficiency check (requires API key) |
| `loop-stop.sh` | Stop hook: Controls loop mode iteration lifecycle |
| `guard-writes.sh` | PreToolUse hook: Prevents spec edits after spec.lock |

## Additional Resources

### References
- **`references/workflow-phases.md`** - Detailed phase instructions
- **`references/file-structure.md`** - Spec file templates
- **`references/code-organization.md`** - Code layer conventions

### Examples
- **`examples/sample-progress.md`** - Example progress file
- **`examples/sample-contracts.md`** - Example contracts file

## Quick Reference

```bash
# Initialize
bash ${CLAUDE_PLUGIN_ROOT}/scripts/init.sh {feature-name}

# Development
git checkout -b feat/{feature-name}
# ... implement tasks ...
bun run check && bun run test && bun run build

# Submit
git push -u origin feat/{feature-name}
gh pr create --title "feat: {Feature}" --body-file .works/spec/{feature-name}/PR.md
```
