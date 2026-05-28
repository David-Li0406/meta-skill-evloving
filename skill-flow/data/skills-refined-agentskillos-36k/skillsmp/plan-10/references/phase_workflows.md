# Phase Workflows

This document provides detailed workflows for each phase, including best practices for memory management and context isolation.

## Core Principles

### Memory Optimization
- **Phase Isolation**: Each phase operates with minimal context from previous phases
- **Summary-First Loading**: Always load phase summaries before full context
- **Knowledge Base Pattern**: Store cross-phase references in `.plans/knowledge-base/`
- **Explicit Outputs**: Each phase defines clear, minimal outputs for next phase

### Context Management
- **Load Only What's Needed**: Don't load full previous phase context
- **Structured Summaries**: Every phase creates a `phase_summary.md` under 500 words
- **On-Demand References**: Load knowledge base files only when explicitly needed
- **Progressive Disclosure**: Start with summaries, dive deeper only if necessary

## Phase Workflows

### 1. Research Phase

**Purpose**: Gather information to understand the problem space.

**Memory Budget**: High (comprehensive exploration allowed)

**Workflow**:
1. Read project goal from CURRENT_PLAN.md
2. Explore codebase/context as needed
3. Document findings in structured format:
   - Create `.plans/knowledge-base/` files for future reference
   - Write `research_findings.md` with detailed discoveries
   - Create `phase_summary.md` (concise, <500 words)

**Outputs**:
- `.plans/research/research_findings.md` - Detailed findings
- `.plans/knowledge-base/*.md` - Reference docs (schemas, APIs, patterns)
- `.plans/research/phase_summary.md` - Concise summary for next phase

**Transition to Planning**:
- Update CURRENT_PLAN.md: mark research complete
- Planning phase will load ONLY `research/phase_summary.md`

---

### 2. Planning Phase

**Purpose**: Design the solution based on research.

**Memory Budget**: Medium (focused on design, not exploration)

**Workflow**:
1. Load `../research/phase_summary.md` (do NOT load full research)
2. Read project goal from CURRENT_PLAN.md
3. Design solution approach:
   - Create implementation plan
   - Document architecture decisions
   - Break down into steps
4. Create outputs:
   - `plan.md` - Detailed implementation plan
   - `architecture.md` - Design decisions
   - `phase_summary.md` - Concise plan overview (<300 words)

**Inputs Used**:
- ✅ `CURRENT_PLAN.md`
- ✅ `../research/phase_summary.md`
- ❌ NOT full research context

**Outputs**:
- `.plans/planning/plan.md` - Implementation plan
- `.plans/planning/architecture.md` - Architecture decisions
- `.plans/planning/phase_summary.md` - Plan overview

**Transition to Revision**:
- Update CURRENT_PLAN.md: mark planning complete
- Revision phase will load planning outputs

---

### 3. Revision Phase

**Purpose**: Review and refine the plan.

**Memory Budget**: Medium (review existing plan)

**Workflow**:
1. Load `../planning/phase_summary.md`
2. Load `../planning/plan.md` for detailed review
3. Review for:
   - Completeness
   - Feasibility
   - Gaps or risks
   - Alignment with goal
4. Create outputs:
   - `review_notes.md` - Feedback and concerns
   - `revised_plan.md` - Updated plan (if changes needed)
   - `phase_summary.md` - Summary of revisions

**Inputs Used**:
- ✅ `CURRENT_PLAN.md`
- ✅ `../planning/phase_summary.md`
- ✅ `../planning/plan.md`
- ✅ `../research/phase_summary.md` (if needed for validation)
- ❌ NOT full research context

**Outputs**:
- `.plans/revision/review_notes.md` - Review findings
- `.plans/revision/revised_plan.md` - Updated plan (if needed)
- `.plans/revision/phase_summary.md` - Revision summary

**Transition to Building**:
- Update CURRENT_PLAN.md: mark revision complete
- Building phase will load plan and revision summary

---

### 4. Building Phase

**Purpose**: Implement the solution.

**Memory Budget**: Low for plan context, high for implementation work

**Workflow**:
1. Load `../revision/phase_summary.md`
2. Load `../planning/plan.md` (the implementation plan)
3. Execute implementation:
   - Follow plan step by step
   - Reference knowledge base files on-demand
   - Document deviations in `implementation_log.md`
4. Create outputs:
   - Actual implementation artifacts (code, configs, etc.)
   - `implementation_log.md` - Deviations and decisions
   - `phase_summary.md` - Implementation summary

**Inputs Used**:
- ✅ `CURRENT_PLAN.md`
- ✅ `../planning/plan.md`
- ✅ `../revision/phase_summary.md`
- ✅ `.plans/knowledge-base/*.md` (on-demand only)
- ❌ NOT full research or planning exploration context

**Outputs**:
- Implementation artifacts (in project, not .plans/)
- `.plans/building/implementation_log.md` - Log of what was built
- `.plans/building/phase_summary.md` - Implementation summary

**Transition to Validation**:
- Update CURRENT_PLAN.md: mark building complete
- Validation phase will load building summary

---

### 5. Validation Phase

**Purpose**: Verify implementation meets requirements.

**Memory Budget**: Low (focused validation)

**Workflow**:
1. Load `../building/phase_summary.md`
2. Load `../building/implementation_log.md` if needed
3. Execute validation:
   - Run tests if applicable
   - Verify against requirements
   - Check for issues
4. Create outputs:
   - `validation_results.md` - Test results
   - `issues.md` - Problems found (if any)
   - `phase_summary.md` - Validation summary

**Inputs Used**:
- ✅ `CURRENT_PLAN.md`
- ✅ `../building/phase_summary.md`
- ✅ `../building/implementation_log.md` (if needed)
- ❌ NOT full building context

**Outputs**:
- `.plans/validation/validation_results.md` - Results
- `.plans/validation/issues.md` - Issues (if any)
- `.plans/validation/phase_summary.md` - Validation summary

**Transition to Cleanup**:
- Update CURRENT_PLAN.md: mark validation complete
- If issues found, may loop back to building
- Otherwise proceed to cleanup

---

### 6. Cleanup Phase

**Purpose**: Finalize project and remove plan files.

**Memory Budget**: Minimal (load summaries only)

**Workflow**:
1. Load all `phase_summary.md` files from each phase
2. Create final summary:
   - Project goal
   - What was accomplished
   - Key decisions
   - Final artifacts
3. Confirm cleanup with user:
   - Ask if plan files should be removed
   - If yes, run cleanup utility
   - If no, keep for reference
4. Create output:
   - `final_summary.md` - Complete project summary

**Inputs Used**:
- ✅ All `phase_summary.md` files
- ❌ NOT full phase contexts

**Outputs**:
- `.plans/cleanup/final_summary.md` - Project summary
- Optional: Move to project root or remove all plan files

**Completion**:
- Update CURRENT_PLAN.md: mark as completed
- Run cleanup if approved

---

## Iteration Strategy

### When to Iterate

Plans may need iteration when:
- Validation reveals issues requiring fixes
- Building phase discovers plan gaps
- Revision identifies major concerns

### Iteration Workflow

1. **Identify Need**: Phase determines iteration is needed
2. **Document Reason**: Write clear reason in phase_summary.md
3. **Update CURRENT_PLAN.md**: Add note about iteration
4. **Return to Phase**: Jump back to appropriate phase
5. **Create Iteration Log**: Track iteration number and reason

### Iteration Best Practices

- Limit iterations to avoid infinite loops (max 2-3 per phase)
- Each iteration should have clear entry/exit criteria
- Document why iteration is needed
- Load only iteration-specific context

### Example Iteration Flow

```
Building Phase
  ↓
Discovers plan gap
  ↓
Update CURRENT_PLAN.md with iteration note
  ↓
Return to Planning Phase
  ↓
Load building/phase_summary.md for context
  ↓
Create planning/iteration_01_plan.md
  ↓
Resume to Building Phase
```

---

## Memory Management Patterns

### Pattern 1: Summary Cascade

Each phase creates a summary that the next phase loads:

```
Research → phase_summary.md → Planning
Planning → phase_summary.md → Revision
Revision → phase_summary.md → Building
Building → phase_summary.md → Validation
Validation → phase_summary.md → Cleanup
```

### Pattern 2: Knowledge Base

Cross-phase references stored centrally:

```
Research creates:
  .plans/knowledge-base/api_schema.md
  .plans/knowledge-base/database_structure.md

Building loads on-demand:
  - Read api_schema.md when implementing API
  - Read database_structure.md when implementing DB code
```

### Pattern 3: Minimal Context Transfer

Only essential information passes between phases:

```
❌ Bad: Load all research findings in building phase
✅ Good: Load research/phase_summary.md + specific knowledge base file

❌ Bad: Load full planning exploration in validation
✅ Good: Load planning/phase_summary.md only

❌ Bad: Copy detailed research into planning phase
✅ Good: Reference research summary, load details if needed
```

### Pattern 4: Progressive Disclosure

Load context in layers:

```
1. First: Load phase_summary.md
2. If needed: Load specific section from detailed file
3. If needed: Load knowledge base reference
4. Never: Load full previous phase context
```

---

## Best Practices

### DO:
- Create concise phase_summary.md files (<500 words)
- Store cross-phase references in knowledge-base
- Load only summaries unless details are needed
- Document deviations from plan
- Update CURRENT_PLAN.md after each phase
- Use structured outputs (markdown, JSON)

### DON'T:
- Load full previous phase context by default
- Copy content between phases
- Create circular dependencies
- Skip phase_summary.md creation
- Forget to update CURRENT_PLAN.md
- Mix phase concerns

### Key Metrics:
- **Phase summary**: <500 words
- **Planning phase summary**: <300 words
- **Knowledge base files**: <2000 words each
- **Implementation log**: Only deviations, not full implementation
