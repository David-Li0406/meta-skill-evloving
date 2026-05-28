---
name: plan-authoring-cycle
description: HAIOS Plan Authoring Cycle for structured plan population. Use when filling
  in implementation plan sections. Guides AMBIGUITY->ANALYZE->AUTHOR->VALIDATE workflow.
recipes:
- plan
generated: 2025-12-25
last_updated: '2026-01-19T17:31:15'
---
# Plan Authoring Cycle

This skill defines the AMBIGUITY-ANALYZE-AUTHOR-VALIDATE cycle for populating implementation plan sections after scaffolding. It ensures operator decisions are surfaced before plan authoring, and that plans have complete Goal, Design, and Tests sections before entering the DO phase.

## When to Use

**Manual invocation:** `Skill(skill="plan-authoring-cycle")` when a plan has placeholder content.
**Called from:** implementation-cycle PLAN phase when plan needs population.

---

## The Cycle

```
AMBIGUITY --> ANALYZE --> AUTHOR --> VALIDATE --> CHAIN
    |                                               |
    |                                       plan-validation-cycle
    +-- BLOCK if unresolved operator decisions
```

### 0. AMBIGUITY Phase (Gate 3)

**Goal:** Surface and resolve operator decisions BEFORE plan authoring begins.

> **INV-058:** This is Gate 3 of the Ambiguity Gating defense-in-depth strategy.
> - Gate 1 (E2-272): `operator_decisions` field in work_item.md template
> - Gate 2 (E2-273): "Open Decisions" section in implementation_plan.md template
> - **Gate 3 (E2-274): AMBIGUITY phase in plan-authoring-cycle (this phase)**
> - Gate 4 (E2-275): Decision check in plan-validation-cycle

**Actions:**
1. Read the work item: `docs/work/active/{backlog_id}/WORK.md`
2. Parse frontmatter for `operator_decisions` field:
   ```yaml
   # Structure of operator_decisions field:
   operator_decisions:
     - question: "Implement modules or remove references?"
       options: ["implement", "remove"]
       resolved: false  # MUST be true before proceeding
       chosen: null     # Filled when operator decides
   ```
3. Check for unresolved decisions (`resolved: false` or missing `chosen`):
4. **IF any unresolved decisions exist:**
   - **BLOCK** with message: "Unresolved operator decisions in work item."
   - Present `AskUserQuestion` with options from the work item:
     ```
     AskUserQuestion(questions=[{
       "question": "<question from operator_decisions>",
       "header": "Decision",
       "options": [{"label": opt, "description": ""} for opt in options],
       "multiSelect": false
     }])
     ```
   - Wait for operator response
   - Update work item WORK.md with `resolved: true` and `chosen: <value>`
5. **IF all decisions resolved (or `operator_decisions` is empty/missing):**
   - Proceed to ANALYZE phase
   - If any resolved decisions exist, populate "Open Decisions" section in plan:
     - Copy resolved decisions from work item to plan's "Open Decisions" table
     - Format: `| {question} | [{options}] | {chosen} | {rationale from operator} |`

**Exit Criteria:**
- [ ] Work item WORK.md read
- [ ] `operator_decisions` field checked
- [ ] All decisions resolved (or none exist)
- [ ] Open Decisions section populated in plan (if any decisions existed)

**Tools:** Read, AskUserQuestion, Edit

---

### 1. ANALYZE Phase

**Goal:** Read plan and identify sections needing population.

**Actions:**
1. Read the plan file: `docs/work/active/{backlog_id}/plans/PLAN.md` (or legacy `docs/plans/PLAN-{backlog_id}-*.md`)
2. Check each section for placeholder text:
   - Goal: `[One sentence: ...]`
   - Effort Estimation: `[N]` placeholders
   - Current/Desired State: `[What the system...]`
   - Tests First: `test_[descriptive_name]`
   - Detailed Design: `[path/to/file.py]`
3. Create checklist of sections to populate

**Exit Criteria:**
- [ ] Plan file read
- [ ] Empty sections identified
- [ ] Checklist created

**Tools:** Read

---

### 2. AUTHOR Phase

**Goal:** Systematically populate each section with real content.

**Guardrails (MUST follow):**
1. **MUST read all source specifications** - Parse References section, read each linked doc
2. **Goal section MUST be one sentence** - Clear, measurable outcome
3. **Effort Estimation MUST reference real files** - Glob for file counts, wc for lines
4. **Current/Desired State MUST show actual code** - Read files, copy snippets
5. **Tests MUST be written before design** - TDD mindset
6. **Detailed Design MUST match source spec interface** - Verify against spec, not assumptions

**MUST Gate: Read Source Specifications (E2-254 Learning)**
Before writing ANY design content:
1. Parse the plan's `## References` section
2. **MUST** read each referenced specification document
3. Extract interface definitions, required functions, data structures from spec
4. Detailed Design MUST implement the spec's interface, not a different one
5. If spec doesn't exist or is unclear, create investigation first

> **Anti-pattern prevented:** "Assume over verify (L1)" - designing from assumptions without reading the actual specification leads to implementations that don't match requirements.

**MUST Gate: Read Sibling Module Patterns (E2-255 Learning)**
When designing a module that **imports from sibling modules**:
1. Identify which sibling modules the new code will import from
2. **MUST** read at least one sibling module to verify:
   - Import pattern (relative vs absolute vs try/except conditional)
   - Error handling patterns (exception types, logging)
   - Path manipulation patterns (sys.path, Path usage)
3. Detailed Design MUST use the same patterns as existing siblings

Example: If designing `cycle_runner.py` that imports from `governance_layer.py`:
```python
# Check work_engine.py lines 45-50 for import pattern:
try:
    from .governance_layer import GovernanceLayer
except ImportError:
    from governance_layer import GovernanceLayer
```

> **Anti-pattern prevented:** "Assume over verify (L2)" - designing implementation patterns from assumptions without reading existing sibling code leads to import failures and inconsistent patterns.

**Section Order:**
1. **Goal** - What capability will exist?
2. **Effort Estimation** - Count files, estimate time
3. **Current State** - What exists now?
4. **Desired State** - What should exist? (MUST match spec interface)
5. **Tests First** - What tests verify success?
6. **Detailed Design** - How to implement? (MUST match spec)
   - **Key Design Decisions** - Document WHY each choice was made (see guidance below)
7. **Implementation Steps** - Ordered checklist
8. **Risks & Mitigations** - What could go wrong? (see guidance below)

**Actions:**
1. **MUST:** Read all referenced specifications first
2. **MUST:** Query memory for prior patterns and learnings (see Memory Query below)
3. For each empty section:
   - Read relevant source files
   - Write concrete content (not placeholders)
   - Verify content aligns with source spec
4. Populate Key Design Decisions table (see guidance below)
5. Populate Risks & Mitigations table (see guidance below)
6. Update plan status to `approved` when complete

**MUST Gate: Query Memory for Prior Work**
Before designing, **MUST** query memory:
```
mcp__haios-memory__memory_search_with_experience(
    query="patterns learnings {work_item_topic} {spec_name}",
    mode="knowledge_lookup"
)
```
- Look for prior implementations of similar modules
- Look for learnings about the spec domain
- Look for anti-patterns to avoid
- Document what memory returned (even if nothing relevant)

> **Anti-pattern prevented:** "Reinvent the wheel" - designing without checking if similar work exists leads to inconsistent patterns and repeated mistakes.

**Key Design Decisions Guidance:**
For each significant choice in Detailed Design, document in the table:

| Decision | Choice | Rationale |
|----------|--------|-----------|
| [What decision was made] | [Which option was chosen] | [WHY - include tradeoffs considered] |

**MUST document:**
- Any deviation from spec (with explicit rationale)
- Alternative approaches considered and why rejected
- Tradeoffs accepted (e.g., "simpler but less flexible")
- Dependencies chosen and why

**Risks & Mitigations Guidance:**
**MUST** identify at least these risk categories:

| Risk Category | Questions to Ask |
|---------------|------------------|
| Spec misalignment | "Could I be misinterpreting the spec?" |
| Integration | "What could break when this connects to other modules?" |
| Regression | "What existing functionality could this affect?" |
| Scope creep | "Am I adding things not in the spec?" |
| Knowledge gaps | "What don't I understand that could cause problems?" |

For each identified risk, document mitigation:
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Specific risk] | [High/Med/Low] | [Concrete action to reduce risk] |

**Exit Criteria:**
- [ ] **MUST:** All referenced specifications read
- [ ] **MUST:** Memory queried for prior patterns (document results)
- [ ] **MUST:** Detailed Design matches spec interface (not assumptions)
- [ ] **MUST:** If importing from siblings, sibling module patterns verified (E2-255)
- [ ] **MUST:** Key Design Decisions table populated with rationale
- [ ] **MUST:** Risks & Mitigations table populated
- [ ] Goal is one clear sentence
- [ ] Effort Estimation has real numbers from file analysis
- [ ] Current/Desired State shows actual code
- [ ] Tests section has concrete test definitions
- [ ] Design section has implementation details
- [ ] Steps section has actionable checklist

**Tools:** Read, Glob, Grep, Edit, memory_search_with_experience

---

### 3. VALIDATE Phase

**Goal:** Verify plan is ready for implementation.

**Actions:**
1. Re-read plan file
2. Check no placeholder text remains (`[...]` patterns)
3. Verify section completeness:
   - Goal: >20 characters, no placeholders
   - Effort: All metrics have values
   - Design: Has file paths and code snippets
   - Tests: Has at least one concrete test
4. Update plan status: `approved`

**Exit Criteria:**
- [ ] No placeholder text remains
- [ ] All required sections populated
- [ ] Plan status is `approved`

**Tools:** Read, Edit

---

### 4. CHAIN Phase (Post-VALIDATE)

**Goal:** Checkpoint context then chain to plan-validation-cycle.

After VALIDATE phase completes (plan status is `approved`):

#### 4a. Checkpoint (MUST - E2-287)

**MUST** invoke checkpoint-cycle to preserve context before context limit hit:

```
Skill(skill="checkpoint-cycle")
```

**Rationale:** Work complexity within hardened gating system makes context limits per work item likely. Checkpointing after plan authoring ensures continuity if context exhausts during validation or implementation.

#### 4b. Chain to Validation

After checkpoint completes, **MUST** invoke plan-validation-cycle:

```
Skill(skill="plan-validation-cycle")
```

This provides independent validation before implementation-cycle can begin.

**Exit Criteria:**
- [ ] **MUST:** checkpoint-cycle invoked (E2-287)
- [ ] plan-validation-cycle invoked
- [ ] Plan passes validation gate

**Tools:** Skill (checkpoint-cycle, plan-validation-cycle)

---

## Composition Map

| Phase | Primary Tool | Memory Integration |
|-------|--------------|-------------------|
| **AMBIGUITY** | Read, AskUserQuestion, Edit | - |
| ANALYZE | Read | - |
| AUTHOR | Read, Edit, Glob | Query for prior patterns |
| VALIDATE | Read, Edit | - |
| CHAIN | Skill (checkpoint-cycle, plan-validation-cycle) | Context preservation (E2-287) |

---

## Quick Reference

| Phase | Question to Ask | If NO |
|-------|-----------------|-------|
| **AMBIGUITY** | Is WORK.md read? | Read work item first |
| **AMBIGUITY** | Any unresolved operator_decisions? | BLOCK + AskUserQuestion |
| ANALYZE | Is plan read? | Read plan file |
| ANALYZE | Are empty sections identified? | Scan for placeholders |
| AUTHOR | Is Goal complete? | Write one-sentence goal |
| AUTHOR | Is Effort estimated? | Count files, estimate time |
| AUTHOR | Is Design complete? | Write implementation details |
| VALIDATE | Are all sections complete? | Return to AUTHOR |
| VALIDATE | Is status approved? | Update frontmatter |

---

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **AMBIGUITY phase (E2-274)** | Added as phase 0 before ANALYZE | Gate 3 of INV-058 defense-in-depth; prevents plan authoring on ambiguous work |
| Four phases | AMBIGUITY -> ANALYZE -> AUTHOR -> VALIDATE | AMBIGUITY catches decisions before plan effort begins |
| Optional skill | Not required by implementation-cycle | Some plans may come pre-filled |
| Section order | Goal -> Effort -> State -> Tests -> Design | Logical progression abstract to concrete |
| TDD before Design | Tests defined before implementation details | Enforces test-first thinking |

---

## Related

- **work-creation-cycle skill:** Parallel workflow for work items
- **close-work-cycle skill:** Parallel workflow for closure
- **implementation-cycle skill:** Uses this skill during PLAN phase
- **Implementation plan template:** `.claude/templates/implementation_plan.md`
- **/new-plan command:** Creates plan files
