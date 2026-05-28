---
name: plan-fixer
description: Fix implementation plans through iterative gap analysis. Use when user wants to verify a plan, fix a plan, check for gaps, validate an implementation plan, or ensure a plan is complete.
context: fork
allowed-tools: Task, Read, Write, Edit, Bash(node:*)
user-invocable: true
---

# Plan Fixer

Iteratively verify and optimize implementation plans for autonomous agent execution using a four-phase approach:

1. **Phase 0**: Structure & Conciseness (convert to agent-oriented format)
2. **Phase 1**: Claude self-review loop (find gaps in structured plan)
3. **Phase 2**: Codex cross-validation loop
4. **Phase 3**: Final polish (constraint extraction, size check)
5. **Phase 4**: Split & Initialize (split into individual plan files for orchestrator)

## Design Principle: Agent-Oriented Plans

Plans are optimized for **autonomous coding agent consumption**, not human reading:

| Human-Oriented (avoid) | Agent-Oriented (prefer) |
|------------------------|-------------------------|
| Explains rationale ("why") | Just gives instructions ("what") |
| Offers alternatives | Specifies ONE path |
| Uses prose paragraphs | Uses structured commands |
| Provides background context | Derives context from code |

**Why conciseness matters:**
- Context rot: LLM performance degrades as context grows
- Stay under 40% context utilization for optimal performance
- Structured plans make gaps MORE visible
- Verification steps improve quality by 2-3x

## Configuration

- **Gap Focus**: Completeness gaps (missing actionable instructions, unhandled branches, missing verification)
- **Fix Method**: Edit plan directly
- **Max Iterations**: 5 per phase
- **User Interaction**: Progress updates (no approval needed)
- **Size Limit**: Flag plans with >5 sub-tasks for splitting

## Parameters

Detect these parameters from the user's request:

| Parameter | Trigger Phrases | Effect |
|-----------|-----------------|--------|
| `codex-fix` | "let Codex fix", "Codex can fix", "Codex should fix", "have Codex fix" | Codex fixes gaps directly using `--full-auto` instead of just reviewing |
| `--no-split` | "--no-split", "don't split", "no split", "skip split" | Skip Phase 4 (do not create .long-run/ directory structure) |
| `split-only` | "split only", "phase 4 only", "just split", "only split" | Skip Phases 0-3, run only Phase 4 (for already-optimized plans) |

### Split-Only Mode (split-only: ON)

Use when you have an already-optimized PLAN.md and only need to split it into individual plan files:
- Skips Phase 0 (structure conversion)
- Skips Phase 1 (Claude review)
- Skips Phase 2 (Codex validation)
- Skips Phase 3 (final polish)
- Runs Phase 4 only (split & initialize)

This mode requires the input file to already be in agent-oriented format with `<task>` blocks.

### Output Behavior

**Always generates a new PLAN.md** - never modifies the original file.

This approach:
- Preserves original plan for human reference
- Creates agent-executable `PLAN.md` in GSD location
- Clear separation: "human spec" vs "agent prompt"
- Non-destructive workflow

**Output location:**
1. Extract the directory and base filename from the source plan path
2. Write optimized plan to: `<source-dir>/<source-basename>.PLAN.md`
3. Write mapping file to: `<source-dir>/<source-basename>.PLAN.mapping.md`
4. Report: "Generated: <source-dir>/<source-basename>.PLAN.md"

**Example:**
```
Input:  _docs/my-feature-idea.md
Output: _docs/my-feature-idea.PLAN.md
        _docs/my-feature-idea.PLAN.mapping.md
```

### Default Mode (codex-fix: OFF)
- Phase 1: Claude reviews → Claude fixes
- Phase 2: Codex reviews → Claude validates → **Claude fixes**

### Codex-Fix Mode (codex-fix: ON)
- Phase 1: Claude reviews → Claude fixes
- Phase 2: Codex reviews AND fixes directly → Claude validates the fix

## Workflow

### Phase 0: Structure & Conciseness

**Purpose:** Convert plan to agent-oriented format BEFORE gap analysis. This makes gaps more visible and sets the template for subsequent fixes.

**Skip condition:** If plan already uses structured format (has `<task>`, `<action>`, `<verify>` tags or equivalent markdown structure).

**Success criteria:** Requirement-verifier returns `✅ COMPLETE` status.

**Max iterations:** 3 (structure-optimizer runs, then re-runs if verification fails)

```
iteration = 0
while iteration < 3:
    1. Check if plan is already agent-formatted (skip to step 5 if yes)

    2. Spawn structure-optimizer agent:
       - Input: source plan path, output PLAN.md path
       - Extract ALL requirements, edge cases, constraints
       - Build cross-reference table
       - Write PLAN.md to output path
       - Write PLAN.mapping.md with cross-reference table

    3. Spawn requirement-verifier agent:
       - Input: source plan path, PLAN.md path, PLAN.mapping.md path
       - Compare source to PLAN.md using mapping table
       - Check for MISSING items and MUTATED content
       - Return status: ✅ COMPLETE | ❌ INCOMPLETE | ⚠️ NEEDS REVIEW

    4. If verification status is ❌ INCOMPLETE:
       - Extract list of missing/mutated items from verifier output
       - Re-run structure-optimizer with explicit instruction:
         "The following items were lost in conversion. Find and add them:
          [list of missing items with source quotes]"
       - iteration++
       - Continue loop

    5. If verification status is ✅ COMPLETE or ⚠️ NEEDS REVIEW:
       - Exit loop
       - If ⚠️ NEEDS REVIEW: log warning but proceed

Report: "Phase 0 complete after [N] iterations. Preservation: [N]/[N] requirements"
```

**Vague requirement handling:** Phase 0 preserves vague items as-is (no content loss). Phase 1 gap-analyzer will flag vague items for clarification. This maintains separation of concerns: Phase 0 = preserve, Phase 1 = clarify.

### Phase 1: Claude Self-Review Loop

```
iteration = 0
while iteration < 5:
    1. Spawn gap-analyzer agent on the plan
    2. If no critical gaps found → exit Phase 1
    3. For each critical gap:
       - Report: "Found gap: [description]"
       - Spawn gap-fixer agent to fix it
       - Report: "Fixed: [description]"
    4. iteration++

Report: "Phase 1 complete after [N] iterations"
```

### Phase 2: Codex Cross-Validation Loop

#### Default Mode (codex-fix: OFF)
```
iteration = 0
while iteration < 5:
    1. Call Codex via codex-bridge asking for completeness gaps
    2. Spawn codex-validator agent to verify each finding
    3. If no valid gaps → exit Phase 2
    4. For each validated gap:
       - Report: "Codex found valid gap: [description]"
       - Spawn gap-fixer agent to fix it (Claude fixes)
       - Report: "Fixed by Claude: [description]"
    5. iteration++

Report: "Phase 2 complete. Plan verification finished."
```

#### Codex-Fix Mode (codex-fix: ON)
```
iteration = 0
while iteration < 5:
    1. Call Codex via codex-bridge with --full-auto to find AND fix gaps
    2. Spawn codex-validator agent to verify the fixes are valid
    3. If no changes made or fixes invalid → exit Phase 2
    4. For each fix made:
       - Report: "Codex fixed: [description]"
       - If fix invalid, revert and spawn gap-fixer agent
    5. iteration++

Report: "Phase 2 complete."
```

### Phase 3: Final Polish

**Purpose:** Final optimization pass after all gaps are fixed.

```
1. Spawn final-polish agent to:
   - Extract remaining constraints into <constraints> section
   - Check plan size (flag if >5 sub-tasks per task group)
   - Verify all tasks have <verify> and <done> criteria
   - Remove any remaining verbose prose
2. If plan too large:
   - Report: "⚠️ Plan has [N] sub-tasks, recommend splitting"
3. Report: "Phase 3 complete. Plan optimized for agent execution."
```

### Phase 4: Split & Initialize Long-Run

**Purpose:** Split unified PLAN.md into individual task group files for orchestrator consumption.

**Skip condition:** If user passes `--no-split` flag or plan has only 1 task group.

**Directory determination:**
- `plan_dir` = directory containing the PLAN.md output file
- `.long-run/` is created inside `plan_dir`
- Example: If PLAN.md is at `specs/my-feature/my-feature.PLAN.md`, then `.long-run/` is created at `specs/my-feature/.long-run/`

```
1. Determine plan_dir from PLAN.md output path
   plan_dir = parent directory of PLAN.md

2. Parse PLAN.md for task groups (look for <task> blocks)
   - Count task groups
   - If count <= 1:
     - Still create .long-run/ directory structure
     - Create STATE.md with single task entry
     - Copy PLAN.md to .long-run/plans/01-PLAN.md (single file)
     - Create ISSUES.md (empty) and agent-history.json
     - Report: "Single task group detected, created 1 plan file"

3. Create .long-run/ directory structure:
   {plan_dir}/
   └── .long-run/
       ├── STATE.md
       ├── ISSUES.md          # Empty, for Rule 5 deviations
       ├── agent-history.json # { "version": "1.0", "agents": [] }
       ├── plans/
       │   ├── 01-PLAN.md
       │   ├── 02-PLAN.md
       │   └── ...
       └── summaries/

4. For each task group:
   - Extract task content with its context/constraints
   - Write to .long-run/plans/{NN}-PLAN.md
   - Include shared <context>, <constraints>, <objective> in each

5. Generate initial state files:
   - STATE.md with task list, config, and placeholder for start_commit
   - ISSUES.md (empty file for Rule 5 deviations)
   - agent-history.json with { "version": "1.0", "agents": [] }

6. Keep unified PLAN.md at plan_dir root (for human reference)

Report: "Phase 4 complete. Created {N} plan files in .long-run/plans/"
```

### STATE.md Template (Phase 4 Output)

```markdown
# Execution State: {spec_name}

## Status
- **Phase:** Ready to Execute
- **Current Task:** Task 1 - {first_task_name}
- **Progress:** [░░░░░░░░░░] 0/{total} tasks

## Task Groups

| # | Task Group | Agent | Status |
|---|------------|-------|--------|
| 1 | {name} | long-run-executor | Pending |
...

## Metrics
- **Started:** {date}
- **Commits:** 0
- **Files Modified:** 0

## Rollback Reference
- **start_commit:** (set by orchestrator on first execution)

## Configuration
clarification_timeout_minutes: 10
timeout_per_plan_minutes: 30
timeout_action: prompt
```

## How to Execute

When user asks to verify/fix a plan:

1. **Read the source plan file**
2. **Check for split-only mode:**
   - If `split-only` parameter detected:
     - Verify input has `<task>` blocks (fail if not)
     - SKIP to Step 8 (Execute Phase 4)
3. **Determine output location** (same folder as input):
   - Extract directory path from source file (e.g., `_docs/` from `_docs/my-feature.md`)
   - Extract base filename without extension (e.g., `my-feature` from `my-feature.md`)
   - Create output path: `<source-dir>/<source-basename>.PLAN.md`
   - Mapping file path: `<source-dir>/<source-basename>.PLAN.mapping.md`
4. **Execute Phase 0** (Structure & Conciseness) - with iteration loop:
   ```
   for iteration in 1..3:
     a. Spawn `structure-optimizer` with:
        - source_path: original plan file
        - output_path: PLAN.md location
        - mapping_path: PLAN.mapping.md location
        - (if iteration > 1) missing_items: list from previous verification
     b. Spawn `requirement-verifier` with:
        - source_path: original plan file
        - plan_path: PLAN.md location
        - mapping_path: PLAN.mapping.md location
     c. If verifier returns ✅ COMPLETE → exit loop
     d. If verifier returns ❌ INCOMPLETE → extract missing items, continue loop
     e. If verifier returns ⚠️ NEEDS REVIEW → log warning, exit loop
   ```
   - All subsequent phases edit new PLAN.md (not the original)
5. **Execute Phase 1** (Claude Self-Review):
   - Use Task tool with `gap-analyzer` agent on PLAN.md
   - Parse response for critical gaps (including vague items from Phase 0)
   - For each gap, use Task tool with `gap-fixer` agent on PLAN.md
   - Re-analyze until clean or max iterations
6. **Execute Phase 2** (Codex Cross-Validation):
   - Call codex-bridge with FULL source plan content AND PLAN.md content
   - Use Task tool with `codex-validator` agent to verify findings
     - Pass source plan path, PLAN.md path, AND mapping file path
   - For valid gaps, use Task tool with `gap-fixer` agent on PLAN.md
   - Re-ask Codex until clean or max iterations
7. **Execute Phase 3** (Final Polish):
   - Spawn `final-polish` agent on PLAN.md
   - Check size constraints, extract constraints, verify structure
8. **Execute Phase 4** (Split & Initialize) - unless `--no-split` flag:
   - Count task groups in PLAN.md
   - If only 1 task group: skip Phase 4
   - Extract plan directory from output path (plan_dir)
   - Create `.long-run/` directory structure inside plan_dir
   - For each task group:
     - Extract task content with shared context/constraints
     - Write to `.long-run/plans/{NN}-PLAN.md`
   - Generate STATE.md with task list and default config
   - Create ISSUES.md (empty file for Rule 5 deviations)
   - Create agent-history.json with { "version": "1.0", "agents": [] }
   - Create empty `summaries/` directory
9. **Report completion**:
   - Show path to generated PLAN.md and PLAN.mapping.md
   - Note original file was preserved
   - Show preservation rate from Phase 0 verification
   - Show iteration count if Phase 0 required multiple passes
   - Show Phase 4 split results (if applicable)

## Progress Update Format

Throughout execution, report progress like:

```
📋 Plan Fixer Starting...
📖 Source: [original filename]
📁 Output: [source-dir]/[source-basename].PLAN.md

🔧 Phase 0: Structure & Conciseness
   - Converting to agent-oriented format...
   - Extracted 3 constraints
   - Removed 12 lines of rationale
   - Writing to: [source-dir]/[source-basename].PLAN.md
   ✅ Phase 0 complete

🔄 Phase 1: Claude Self-Review
   Iteration 1/5:
   - Analyzing for completeness gaps...
   - Found 2 critical gaps
   - Gap 1: [description] → Fixing... ✓ Fixed
   - Gap 2: [description] → Fixing... ✓ Fixed

   Iteration 2/5:
   - Analyzing for completeness gaps...
   - No critical gaps found
   ✅ Phase 1 complete (2 iterations)

🔄 Phase 2: Codex Cross-Validation
   Iteration 1/5:
   - Asking Codex for completeness gaps...
   - Codex found 1 potential gap
   - Validating: [description] → Valid gap
   - Fixing... ✓ Fixed

   Iteration 2/5:
   - Asking Codex for completeness gaps...
   - No gaps found
   ✅ Phase 2 complete (2 iterations)

✨ Phase 3: Final Polish
   - Verifying all tasks have <verify> and <done>...
   - Checking plan size: 4 sub-tasks ✓
   - Extracting remaining constraints...
   ✅ Phase 3 complete

📂 Phase 4: Split & Initialize
   - Found 3 task groups
   - Creating .long-run/ directory structure...
   - Writing 01-PLAN.md (Task Group 1: Setup)
   - Writing 02-PLAN.md (Task Group 2: Core Features)
   - Writing 03-PLAN.md (Task Group 3: Integration)
   - Generating STATE.md...
   ✅ Phase 4 complete (3 plan files created)

🎉 Plan optimization complete!
   Source: [original filename] (preserved)
   Output: [source-dir]/[source-basename].PLAN.md
   Structure: Agent-oriented ✓
   Gaps fixed: 3
   Size: 4 sub-tasks (within limit)
   Long-run ready: .long-run/plans/ (3 files)
```

## Sub-Agents

This skill uses six sub-agents defined in the `agents/` folder:

1. **structure-optimizer**: Converts prose plans to agent-oriented structured format (Phase 0)
2. **requirement-verifier**: Verifies nothing was lost during conversion (Phase 0 checkpoint)
3. **gap-analyzer**: Analyzes plan for completeness gaps (Phase 1)
4. **gap-fixer**: Fixes a specific gap in the plan (Phase 1 & 2)
5. **codex-validator**: Validates whether a Codex-identified gap is real (Phase 2)
6. **final-polish**: Final optimization pass - constraints, size check, structure verification (Phase 3)

## Codex Integration

**Setup (run once per session):**
```bash
# Find codex-bridge script (marketplace install path)
CODEX_BRIDGE=$(ls -1 "$HOME/.claude/plugins/cache/saurun-marketplace/saurun/"*/skills/codex-bridge/codex-bridge.mjs 2>/dev/null | head -1)
```

**CRITICAL:** Always pass `--working-dir "<project-path>"` so Codex can read project files.

**Timeout:** Use `--timeout 1200000` (20 minutes) for all Codex calls to allow sufficient processing time.

### Default Mode: Review Only

```bash
node "$CODEX_BRIDGE" --timeout 1200000 "Analyze this implementation plan for COMPLETENESS GAPS.

IMPORTANT CONTEXT:
This PLAN.md was CONVERTED from a prose source plan. During conversion:
- Prose was restructured into <task>/<action>/<verify>/<done> format
- 'Why' explanations were removed (intentional)
- Requirements, edge cases, and constraints should have been preserved

Your job: Find gaps that would cause an autonomous coding agent to fail.
You have access to BOTH the converted PLAN.md AND the original source plan.

LOOK FOR:
1. CONVERSION LOSSES - compare source to PLAN.md:
   - Requirements in source but missing from PLAN.md
   - Edge cases mentioned in source prose but not in PLAN.md
   - Constraints in source but not in <constraints> section
   - Numbers/thresholds that may have been changed
2. GENUINE GAPS - things never specified in either:
   - Missing actionable instructions (agent would have to guess)
   - Unhandled error scenarios
   - Missing verification commands
   - Vague success criteria

DO NOT FLAG:
- Missing 'why' explanations (intentionally removed)
- Stylistic preferences
- Implementation details the agent can decide

Return a JSON array of gaps found:
[{\"gap\": \"description\", \"severity\": \"critical|minor\", \"location\": \"section\", \"likely_type\": \"conversion_loss|genuine_gap\", \"source_quote\": \"quote from source if conversion_loss\"}]

If no gaps found, return: []

===== SOURCE PLAN (ORIGINAL) =====
[FULL SOURCE PLAN CONTENT]
===== END SOURCE PLAN =====

===== PLAN.md (CONVERTED) =====
[FULL PLAN.md CONTENT]
===== END PLAN.md =====
" --working-dir "$PROJECT_PATH"
```

### Codex-Fix Mode: Review AND Fix

```bash
node "$CODEX_BRIDGE" --timeout 1200000 "Analyze this implementation plan for COMPLETENESS GAPS and FIX them directly.

IMPORTANT CONTEXT:
This PLAN.md was CONVERTED from a prose source plan. Content may have been lost.
You have access to BOTH the original source plan AND the converted PLAN.md.

LOOK FOR AND FIX:
1. CONVERSION LOSSES - compare source to PLAN.md and restore:
   - Requirements in source but missing → add to appropriate <task>
   - Edge cases in source prose → add to <action> with error handling
   - Constraints in source → add to <constraints> section
   - Numbers/thresholds changed → restore original values
2. GENUINE GAPS - add new content:
   - Missing requirements → add detailed <action> steps
   - Undefined edge cases → document handling in <action>
   - Unclear success criteria → add measurable <done> criteria

PRESERVE:
- Existing structured format
- All current content
- Agent-oriented style (no prose explanations)

After fixing, return a JSON summary:
[{\"gap\": \"description\", \"fix\": \"what was added/changed\", \"location\": \"section\", \"type\": \"conversion_loss|genuine_gap\", \"source_quote\": \"original text if restoration\"}]

If no gaps found, return: []

PLAN FILE TO EDIT: [filepath]

===== SOURCE PLAN (ORIGINAL - for reference) =====
[FULL SOURCE PLAN CONTENT]
===== END SOURCE PLAN =====

===== PLAN.md (CONVERTED - to be fixed) =====
[FULL PLAN.md CONTENT]
===== END PLAN.md =====
" --full-auto --working-dir "$PROJECT_PATH"
```

## Final Output (returned to parent context)

When the skill completes, return this summary to the parent context:

```
╔══════════════════════════════════════════════════════════════╗
║                   PLAN OPTIMIZATION REPORT                   ║
╠══════════════════════════════════════════════════════════════╣
║ Source: [original filename] (preserved)                      ║
║ Output: [source-dir]/[source-basename].PLAN.md               ║
║ Status: ✅ OPTIMIZED | ⚠️ NEEDS ATTENTION | ❌ MAX ITERATIONS ║
╠══════════════════════════════════════════════════════════════╣
║ PHASE 0: Structure & Conciseness                             ║
╟──────────────────────────────────────────────────────────────╢
║ Format: Converted to agent-oriented structure                ║
║ Constraints extracted: 3                                     ║
║ Prose removed: 12 lines                                      ║
╠══════════════════════════════════════════════════════════════╣
║ PHASE 1: Claude Self-Review                                  ║
╟──────────────────────────────────────────────────────────────╢
║ Iteration 1: Found 2 gaps → Fixed: [gap1], [gap2]            ║
║ Iteration 2: Found 1 gap  → Fixed: [gap3]                    ║
║ Iteration 3: No gaps found ✓                                 ║
╠══════════════════════════════════════════════════════════════╣
║ PHASE 2: Codex Cross-Validation                              ║
║ Mode: Review Only | Codex-Fix                                ║
╟──────────────────────────────────────────────────────────────╢
║ Iteration 1: Codex found 1 gap → Valid → Fixed: [gap]        ║
║ Iteration 2: No gaps found ✓                                 ║
╠══════════════════════════════════════════════════════════════╣
║ PHASE 3: Final Polish                                        ║
╟──────────────────────────────────────────────────────────────╢
║ All tasks have <verify> and <done>: ✓                        ║
║ Plan size: 4 sub-tasks (within limit)                        ║
║ Constraints section: Complete                                ║
╠══════════════════════════════════════════════════════════════╣
║ PHASE 4: Split & Initialize                                  ║
╟──────────────────────────────────────────────────────────────╢
║ Plan files created: 3                                        ║
║ Location: {plan_dir}/.long-run/plans/                        ║
║ STATE.md initialized: ✓                                      ║
╠══════════════════════════════════════════════════════════════╣
║ SUMMARY                                                      ║
╟──────────────────────────────────────────────────────────────╢
║ Structure: Agent-oriented ✓                                  ║
║ Gaps fixed: 4 (Claude: 3, Codex: 1)                          ║
║ Size: 4 sub-tasks (limit: 5)                                 ║
║ Iterations: Phase 1 (3) + Phase 2 (2)                        ║
║ Long-run ready: ✓                                            ║
╚══════════════════════════════════════════════════════════════╝
```

### Status Definitions

- **✅ OPTIMIZED**: All phases completed, plan is agent-ready
- **⚠️ NEEDS ATTENTION**: Completed but has warnings (e.g., plan too large, missing verification)
- **❌ MAX ITERATIONS**: Hit 5 iteration limit, gaps may remain

## References

See `references/gap-criteria.md` for detailed gap identification criteria.
