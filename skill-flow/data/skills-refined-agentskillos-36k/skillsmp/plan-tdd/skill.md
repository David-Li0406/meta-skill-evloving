---
name: plan-tdd
description: Create TDD runbook with RED/GREEN/REFACTOR cycles from design document
model: sonnet
requires:
  - Design document from /design (TDD mode)
  - CLAUDE.md for project conventions (if exists)
outputs:
  - TDD runbook at plans/<feature-name>/runbook.md
  - Ready for prepare-runbook.py processing
---

# /plan-tdd Skill

Create detailed TDD runbooks with RED-GREEN-REFACTOR cycles from design documents. Transforms design into structured execution plans compatible with weak orchestrators and prepare-runbook.py.

---

## Purpose and Context

### What This Skill Does

1. Analyzes design documents to extract requirements and decisions
2. Decomposes features into atomic behavioral increments
3. Generates RED-GREEN-REFACTOR cycles for each increment
4. Creates structured runbook with numbered cycles (X.Y format)
5. Delegates to clean sonnet agent for comprehensive review
6. Applies review feedback to ensure completeness and correct test sequencing
7. Produces output compatible with prepare-runbook.py

### When to Use

**Use /plan-tdd when:**
- Design specifies TDD mode or strict RED-GREEN-REFACTOR discipline
- Feature requires atomic verification with test-first approach
- Working in projects with strong testing culture

**Do NOT use when:**
- Design is exploratory or requires iteration
- Implementation approach is unclear
- Feature is simple without TDD overhead
- Use /plan-adhoc for general runbooks

### Workflow Integration

```
/design (TDD mode) → /plan-tdd → [delegated review] → prepare-runbook.py → /orchestrate
```

**Note:** /plan-tdd now includes automatic delegation to a clean sonnet agent for runbook review before finalization.

---

## Process: Five-Phase Execution (with Review)

### Phase 1: Intake

**Objective:** Load design and project conventions.

**Actions:**

1. **Determine design path:**
   - `/plan-tdd` → Find latest `plans/*/design.md` using Glob (sort by mtime)
   - `/plan-tdd <path>` → Use absolute path
   - `/plan-tdd <feature>` → Use `plans/<feature>/design.md`

2. **Read design:** Use Read tool. STOP if: not found, empty, permission denied.

3. **Read CLAUDE.md (optional):** Extract testing patterns and conventions if exists.

4. **Validate TDD mode:** Check frontmatter for `type: tdd` or TDD keywords. If unclear, ask user.

**Outputs:** design_content, design_path, feature_name, conventions

---

### Phase 2: Analysis

**Objective:** Extract feature info and validate completeness.

**Actions:**

1. **Extract feature info:**
   - Goal: Find `**Goal:**`, `## Goal`, or H1 heading (1-2 sentences)
   - Name: From filename, H1, or frontmatter `name:` field
   - STOP if no goal: Ask user "What is the goal?"

2. **Extract design decisions:**
   - Pattern: `## Design Decisions`, `### Decision N:`
   - Format: `Decision N: [Title]\n- Choice: [what]\n- Rationale: [why]`
   - If missing: WARNING, create minimal Common Context

3. **Check unresolved items:**
   - Use Grep for: `(REQUIRES CONFIRMATION)`, `(TBD)`, `(TODO: decide)`, `[DECIDE:]`, `???`
   - If found: STOP, report with line numbers and context

4. **Identify structure:**
   - **Phases (X):** Look for `## Phase N:` or major sections
   - **Increments (Y):** Look for H3 subsections, bullet lists, test scenarios
   - Heuristics: action verbs (Add, Implement, Create, Test) = potential increments

5. **Estimate cycles:**
   - `estimated_cycles = base_increments + setup_cycles`
   - If >20: WARN "Large runbook ({N} cycles). Continue?"

**Outputs:** goal, feature_name, design_decisions, phases, increments, cycle_estimate

---

### Phase 3: Cycle Planning

**Objective:** Generate cycle definitions with RED/GREEN/Stop Conditions.

**Actions:**

1. **Number cycles:** X.Y format (1.1, 1.2, ..., 2.1, 2.2, ...)
   - Start at 1.1 (not 0.1 or 1.0)
   - Sequential within phases
   - No duplicates (error), gaps acceptable (warn)

2. **Generate RED specifications:**

```markdown
**RED Phase:**

**Test:** [What to test - specific assertion]

**Expected failure:**
```
[Exact error message or pattern]
```

**Why it fails:** [Missing implementation]

**Verify RED:** [Command with file/function]
- Must fail with [pattern]
- If passes, STOP - feature may exist
```

   **Logic:**
   - Parse increment for expected behavior
   - Infer test location (tests/, test_*.py)
   - Generate assertion from behavior
   - Predict failure message
   - Provide specific test command

3. **Generate GREEN specifications:**

```markdown
**GREEN Phase:**

**Implementation:** [Minimal code change]

**Changes:**
- File: [path]
  Action: [specific change]

**Verify GREEN:** [Test command]
- Must pass

**Verify no regression:** [Full test suite]
- All existing tests pass
```

   **Logic:**
   - Extract approach from design decisions
   - Identify file locations from design or project structure
   - Specify minimal change (single feature)
   - Use same test command as RED
   - Default regression: `pytest` or `just test`

4. **Assign dependencies:**
   - **Default:** Sequential within phase (1.1 → 1.2 → 1.3)
   - **Cross-phase:** `[DEPENDS: X.Y]` if design requires
   - **Regression:** `[REGRESSION]` for existing behavior tests
   - **Parallel:** Only if truly independent

5. **Generate stop conditions:**

```markdown
**Stop Conditions:**

**STOP IMMEDIATELY if:**
- Test passes on first run (expected RED failure)
- Test failure message doesn't match expected
- Test passes after partial GREEN implementation
- Any existing test breaks (regression failure)

**Actions when stopped:**
1. Document in plans/{feature}/reports/cycle-{X}-{Y}-notes.md
2. If test passes unexpectedly: Investigate, mark [REGRESSION] if already implemented, or fix test
3. If regression: STOP execution, report broken tests, escalate
4. If scope unclear: STOP, document ambiguity, request clarification
```

   **Custom conditions (add if needed):** External dependencies, performance, security

6. **Validate dependency graph:**
   - All referenced cycles exist
   - No circular dependencies (topological sort)
   - No forward dependencies
   - STOP on errors (see error-handling.md)

**Outputs:** cycles, dependency_graph, execution_order

---

### Phase 4: Runbook Generation

**Objective:** Create runbook file with all sections.

**Structure:**

```markdown
---
name: {feature_name}
type: tdd
model: haiku
---

# {Feature Name} TDD Runbook

**Context**: {goal}
**Design**: {design_path}
**Status**: Draft
**Created**: {date}

## Weak Orchestrator Metadata

**Total Steps**: {N}
**Execution Model**: All cycles: Haiku (TDD execution)
**Step Dependencies**: {sequential|parallel|mixed}
**Error Escalation**: Haiku → User on stop conditions/regression
**Report Locations**: plans/{name}/reports/
**Success Criteria**: All cycles GREEN, no regressions
**Prerequisites**: {from_design}

## Common Context

**Key Design Decisions:**
{numbered_list}

**TDD Protocol:**
Strict RED-GREEN-REFACTOR: 1) RED: Write failing test, 2) Verify RED, 3) GREEN: Minimal implementation, 4) Verify GREEN, 5) Verify Regression, 6) REFACTOR (optional)

**Project Paths:**
{paths_from_design}

**Conventions:**
- Use Read/Write/Edit/Grep tools (not Bash for file ops)
- Report errors explicitly (never suppress)
- Write notes to plans/{name}/reports/cycle-{X}-{Y}-notes.md

## Cycle {X.Y}: {Name} {[DEPENDS: A.B]} {[REGRESSION]}

**Objective**: {goal}
**Script Evaluation**: Direct execution (TDD cycle)
**Execution Model**: Haiku

**Implementation:**

{RED_phase}

---

{GREEN_phase}

---

{Stop_conditions}

**Expected Outcome**: GREEN verification, no regressions
**Error Conditions**: RED doesn't fail → STOP; GREEN doesn't pass → Debug; Regression → STOP
**Validation**: RED verified ✓, GREEN verified ✓, No regressions ✓
**Success Criteria**: Test fails during RED, passes during GREEN, no breaks
**Report Path**: plans/{name}/reports/cycle-{X}-{Y}-notes.md

---

[Repeat for each cycle]

## Design Decisions
{copy_from_design}

## Dependencies

**Before**: {prerequisites}
**After**: Feature implemented with test coverage, all cycles verified, ready for integration
```

**Write file:**
- Output: `plans/{feature_name}/runbook.md`
- If exists: Ask to overwrite
- STOP on write errors

**Outputs:** runbook_path, runbook file

---

### Phase 5: Validation and Review

**Objective:** Verify format, delegate comprehensive review, and ensure prepare-runbook.py compatibility.

**Actions:**

1. **Verify format:**
   - Valid YAML frontmatter with `type: tdd`
   - Required sections exist (Weak Orchestrator Metadata, Common Context)
   - Cycle headers match `## Cycle \d+\.\d+:` pattern
   - No duplicate cycle IDs

2. **Delegate to clean sonnet agent for comprehensive review:**

   **Review criteria:**
   - **Completeness**: All features from design document are covered in cycles
   - **Executability**: Instructions are clear, actionable, and unambiguous
   - **Context sufficiency**: Each cycle has adequate information for isolated execution
   - **Test sequencing**: New tests will RED (fail) before implementation exists
   - **Implementation hints**: If sequencing is critical for correct RED behavior, provide hints

   **Review process:**
   - Use Task tool to spawn clean sonnet agent
   - Provide runbook path and design path
   - Agent checks each cycle for RED correctness (will test actually fail?)
   - Agent identifies missing context or ambiguous instructions
   - Agent suggests implementation sequencing hints if needed for proper RED/GREEN flow

   **Example delegation:**
   ```
   Task(
     subagent_type="general-purpose",
     model="sonnet",
     description="Review TDD runbook",
     prompt="""Review the TDD runbook at plans/{name}/runbook.md against design at {design_path}.

     Check:
     1. Completeness - all design features covered
     2. Executability - clear, actionable instructions
     3. Context sufficiency - adequate info per cycle
     4. Test sequencing - tests will RED before GREEN
     5. Implementation hints - provide sequencing guidance if needed

     Report findings and suggest improvements."""
   )
   ```

3. **Apply review feedback:**
   - Read review report
   - Update runbook based on feedback
   - Add implementation hints to cycles if sequencing matters
   - Clarify ambiguous instructions
   - Fill context gaps

4. **Check prepare-runbook.py:**
   - Verify exists at `agent-core/bin/prepare-runbook.py`
   - If not found: WARNING (not fatal)
   - Simulate parsing: extract cycles, Common Context

5. **Revalidate dependencies:** Run topological sort again

6. **Generate success report:**

```markdown
TDD runbook created and reviewed successfully!

**Location**: {path}
**Cycles**: {count}
**Dependencies**: {structure}
**Review**: Completed by clean sonnet agent

**Next steps:**
1. Generate artifacts: python3 agent-core/bin/prepare-runbook.py {path}
2. Execute: /orchestrate plans/{name}/orchestrator-plan.md
3. Commit: Use /commit or /gitmoji + /commit

**Tips:**
- Follow stop conditions strictly
- Document unexpected results in cycle notes
- Regression failures require immediate attention
```

7. **Report to user:** Display success report with path and next steps

**Outputs:** Success report displayed, runbook ready

---

## Cycle Breakdown Guidance

**Key principles:**
- Each cycle: 1-3 assertions
- Clear RED failure expectation
- Minimal GREEN implementation
- Sequential dependencies within phase (default)

**Dependency markers:**
- **Sequential (default):** 1.1 → 1.2 → 1.3
- **[DEPENDS: X.Y]:** Cross-phase dependency
- **[REGRESSION]:** Testing existing behavior

**Detailed guidance:** See `references/patterns.md` for granularity criteria, numbering schemes, common patterns

---

## Constraints and Error Handling

**Tool usage:**
- **Required:** Read, Write, Grep, Glob
- **Prohibited:** Bash for file content, heredocs

**Error handling:** See `references/error-handling.md` for complete catalog, edge cases, recovery protocols

**Validation rules:**
- Cycle granularity: 1-3 assertions (warn if >5, reject if 0)
- Dependency validation: No circular, forward, or invalid references
- Format validation: Valid YAML, required sections, pattern-compliant cycle headers
- prepare-runbook.py: `type: tdd`, `## Cycle X.Y:` format, extractable Common Context

**Anti-patterns:** See `references/anti-patterns.md` for patterns to avoid

---

## Integration Notes

### prepare-runbook.py Processing

After /plan-tdd generates runbook:

1. User runs: `python3 agent-core/bin/prepare-runbook.py plans/{name}/runbook.md`
2. Script detects `type: tdd`, uses `agent-core/agents/tdd-task.md` baseline
3. Script generates:
   - `.claude/agents/{name}-task.md` (baseline + Common Context)
   - `plans/{name}/steps/cycle-{X}-{Y}.md` (individual cycles)
   - `plans/{name}/orchestrator-plan.md` (execution index)
4. Orchestrator executes cycles with plan-specific agent, isolated context, stop conditions

### Workflow After Generation

```
/plan-tdd → runbook.md
↓
User reviews
↓
prepare-runbook.py → Execution artifacts
↓
/orchestrate → Automated execution (or manual cycle-by-cycle)
↓
Feature implemented with test coverage
```

---

## Success Criteria

**Runbook succeeds when:**
1. ✓ Valid TDD runbook at `plans/{name}/runbook.md`
2. ✓ Frontmatter has `type: tdd`
3. ✓ All cycles have RED/GREEN/Stop Conditions
4. ✓ Valid dependency graph (no cycles)
5. ✓ prepare-runbook.py compatible
6. ✓ Common Context from design
7. ✓ Reasonable cycle count (1-50 typical)
8. ✓ User informed of next steps

**Expected stops (fatal):**
- Design not found
- Unresolved confirmations
- Invalid structure
- Circular dependencies
- Cannot write file

**Warnings (proceed with caution):**
- No design decisions section
- Large runbook (>20 cycles)
- prepare-runbook.py not found

---

## Additional Resources

- **`references/patterns.md`** - Granularity criteria, numbering, common patterns, decision trees
- **`references/anti-patterns.md`** - Patterns to avoid with corrections
- **`references/error-handling.md`** - Error catalog, edge cases, recovery protocols
- **`references/examples.md`** - Complete runbook examples

---
