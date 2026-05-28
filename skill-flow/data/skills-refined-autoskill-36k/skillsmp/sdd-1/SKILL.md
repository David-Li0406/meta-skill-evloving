---
name: sdd
description: >
  Unified Specification-Driven Development (SDD) workflow. Auto-detects user intent
  and routes to correct phase. Handles the complete development lifecycle from product
  definition to implementation. Triggers on: "create feature", "implement", "plan",
  "audit", "define product", "feature", "/feature", "/implement", "/plan", "/audit",
  "/define-product", "/generate-constitution", "what's the SDD status", "next step".
  REPLACES: define-product, generate-constitution, specify-feature, clarify-specification,
  create-implementation-plan, generate-tasks, implement-and-verify, sdd-orchestrator.
degree-of-freedom: medium
allowed-tools: Task, SlashCommand, Read, Write, Edit, Glob, Grep, Bash(fd:*), Bash(rg:*), Bash(git:*), Bash(project-intel.mjs:*), AskUserQuestion
---

@.claude/shared-imports/constitution.md
@.claude/shared-imports/CoD_Σ.md
@.claude/shared-imports/memory-utils.md
@.claude/shared-imports/master-todo-utils.md
@.claude/shared-imports/auto-sync-utils.md

# Unified SDD Skill

## Purpose

This skill orchestrates the **complete Specification-Driven Development workflow** through 9 phases (0-8). It replaces 8 individual skills with a single unified entry point that:

1. **Auto-detects** user intent from natural language
2. **Routes** to the correct phase based on context and prerequisites
3. **Auto-chains** phases where appropriate (e.g., /feature → /plan → /tasks → /audit)
4. **Maintains state** across phases with artifact tracking
5. **Integrates system understanding** for complex features

**Announce at start:** "I'm using the unified SDD skill to manage your development workflow."

---

## Quick Reference

| Phase | Command | Prereqs | Creates | Auto-Chain |
|-------|---------|---------|---------|------------|
| **0** | (auto) | Complex feature detected | SYSTEM-UNDERSTANDING.md | → Phase 3 |
| **1** | /define-product | Repository | memory/product.md | → Phase 2 (manual) |
| **2** | /generate-constitution | product.md | memory/constitution.md | → Phase 3 (manual) |
| **3** | /feature | (optional) product.md | specs/$FEATURE/spec.md | → Phase 5 (auto) |
| **4** | /clarify | [NEEDS CLARIFICATION] in spec | Updated spec.md | → Phase 5 (auto) |
| **5** | /plan | spec.md (clarified) | plan.md, research.md, data-model.md | → Phase 6 (auto) |
| **6** | (auto) | plan.md | tasks.md | → Phase 7 (auto) |
| **7** | /audit | spec.md, plan.md, tasks.md | audit-report.md | → Phase 8 (if PASS) |
| **8** | /implement | audit PASS | Code + tests + verification | Feature complete |

**$FEATURE format**: `NNN-feature-name` (e.g., `001-therapy-app`, `015-auth-oauth`)

---

## Workflow Files (Progressive Disclosure)

**Phase Workflows:**
- @.claude/skills/sdd/workflows/00-system-understanding.md - NEW: Auto for complex features
- @.claude/skills/sdd/workflows/01-product-definition.md - Create product.md
- @.claude/skills/sdd/workflows/02-constitution.md - Derive technical principles
- @.claude/skills/sdd/workflows/03-specification.md - Create feature spec
- @.claude/skills/sdd/workflows/04-clarification.md - Resolve ambiguities
- @.claude/skills/sdd/workflows/05-planning.md - Create implementation plan
- @.claude/skills/sdd/workflows/06-tasks.md - Generate tasks
- @.claude/skills/sdd/workflows/07-audit.md - Validate consistency
- @.claude/skills/sdd/workflows/08-implementation.md - TDD implementation

**References:**
- @.claude/skills/sdd/references/phase-routing.md - Intent detection + routing logic
- @.claude/skills/sdd/references/complexity-detection.md - When to trigger Phase 0
- @.claude/skills/sdd/references/quality-gates.md - Constitutional compliance

---

## Step 1: Detect Intent

**Pattern Matching:**

```
Intent_Patterns := {
  foundation: ["define product", "/define-product", "product definition"],
  constitution: ["constitution", "technical principles", "/generate-constitution"],
  feature: ["create feature", "new feature", "build", "I want to", "/feature"],
  clarify: ["clarify", "unclear", "ambiguous", "/clarify"],
  planning: ["plan", "how to implement", "architecture", "/plan"],
  audit: ["audit", "validate", "check consistency", "/audit"],
  implementation: ["implement", "code", "develop", "/implement", "start coding"],
  status: ["status", "progress", "what's next", "SDD status", "where am I"]
}
```

**Detection Logic:**
```
IF user_message ∩ Intent_Patterns ≠ ∅:
  intent := matched_category
  PROCEED to Step 2 (Prerequisite Check)
ELSE:
  SKIP SDD orchestration (not an SDD action)
```

---

## Step 2: Check Prerequisites & Determine Phase

**See:** @.claude/skills/sdd/references/phase-routing.md

**Prerequisite Matrix:**

| Intent | Required Files | Missing? | Action |
|--------|---------------|----------|--------|
| foundation | Repository | N/A | → Phase 1 |
| constitution | memory/product.md | Yes | "Run /define-product first" |
| feature | (optional) product.md | N/A | Check complexity → Phase 0 or 3 |
| clarify | spec.md with markers | Missing | "No spec with clarifications needed" |
| planning | spec.md (clarified) | Missing | "Run /feature first" |
| audit | spec.md, plan.md, tasks.md | Missing | "Missing artifacts: ..." |
| implementation | audit PASS | Fail | "Fix audit issues first" |
| status | N/A | N/A | → Report current state |

---

## Step 3: Execute Phase (or Report Status)

### Status Report (when intent = status)

```markdown
## SDD Workflow Status

**Current Phase**: [Detected from artifacts]
**Working Directory**: {cwd}

### Artifacts Found:
- [ ] memory/product.md (Phase 1)
- [ ] memory/constitution.md (Phase 2)
- [ ] specs/$FEATURE/spec.md (Phase 3)
- [ ] specs/$FEATURE/plan.md (Phase 5)
- [ ] specs/$FEATURE/tasks.md (Phase 6)
- [ ] specs/$FEATURE/audit-report.md (Phase 7)

### Next Step: [Recommended action]
### Blockers: [If any]
```

---

## Phase 0: System Understanding (Auto-Triggers)

**See:** @.claude/skills/sdd/workflows/00-system-understanding.md

**When to Trigger (Auto-Detection):**

| Indicator | Detection Method | Threshold |
|-----------|------------------|-----------|
| Component count | Search for unique files/classes | >3 components |
| File touch estimate | Analyze feature scope | >5 files |
| Architectural keywords | Parse user request | "refactor", "migrate", "integrate", "overhaul" |
| First feature | Check if specs/ empty | No existing specs |
| User request | Explicit mention | "analyze system", "understand codebase" |

**Creates:**
- `specs/$FEATURE/SYSTEM-UNDERSTANDING.md` - Entity relationships, layer analysis
- Mermaid diagrams: Component dependencies, data flow
- Complexity classification: Simple / Moderate / Complex

**Process:**
1. Run project-intel.mjs queries (--overview, --map-imports)
2. Identify key entities and relationships
3. Generate knowledge graph (CoD^Σ notation)
4. Create Mermaid component diagram
5. Classify complexity
6. Proceed to Phase 3 with context

---

## Phases 1-2: Foundation (Manual Progression)

### Phase 1: Product Definition
**See:** @.claude/skills/sdd/workflows/01-product-definition.md

- **Command**: /define-product
- **Intelligence gathering** → User clarification (max 5 questions)
- **Creates**: memory/product.md (user-centric, NO technical details)
- **Next**: Manual /generate-constitution

### Phase 2: Constitution
**See:** @.claude/skills/sdd/workflows/02-constitution.md

- **Command**: /generate-constitution
- **Requires**: memory/product.md
- **Derives** technical principles FROM user needs (CoD^Σ traces)
- **Creates**: memory/constitution.md (7 Articles)
- **Next**: Manual /feature

---

## Phases 3-7: Feature Development (Auto-Chain)

### Phase 3: Specification
**See:** @.claude/skills/sdd/workflows/03-specification.md

- **Command**: /feature "description"
- **Quality gate** → Intelligence gathering → User stories → Spec
- **Creates**: specs/$FEATURE/spec.md
- **Auto-chains**: → /plan (Phase 5)

### Phase 4: Clarification (Conditional)
**See:** @.claude/skills/sdd/workflows/04-clarification.md

- **Command**: /clarify
- **Triggers**: [NEEDS CLARIFICATION] markers in spec
- **Max 5 questions** per iteration
- **Updates**: spec.md (resolves ambiguities)
- **Auto-chains**: → /plan (Phase 5)

### Phase 5: Planning
**See:** @.claude/skills/sdd/workflows/05-planning.md

- **Command**: /plan
- **Constitutional gates** → Intelligence → Technical design
- **Creates**: plan.md, research.md, data-model.md, contracts/
- **Auto-chains**: → generate-tasks (Phase 6)

### Phase 6: Task Generation (Auto)
**See:** @.claude/skills/sdd/workflows/06-tasks.md

- **Invoked by**: Phase 5 completion
- **Organizes by**: User story (P1, P2, P3)
- **Creates**: tasks.md with [P] parallelization markers
- **Auto-chains**: → /audit (Phase 7)

### Phase 7: Audit
**See:** @.claude/skills/sdd/workflows/07-audit.md

- **Command**: /audit
- **Validates**: Constitution alignment, coverage, consistency
- **Creates**: audit-report.md (PASS/FAIL)
- **If PASS**: Ready for /implement
- **If FAIL**: Fix issues, re-run

---

## Phase 8: Implementation

**See:** @.claude/skills/sdd/workflows/08-implementation.md

- **Command**: /implement plan.md
- **Requires**: audit PASS
- **Process**: Story-by-story TDD (test → implement → verify)
- **Creates**: Code, tests, verification-report.md per story
- **Updates**: tasks.md (mark complete), memory/ (auto-sync)

**Critical**: Mark tasks complete in tasks.md immediately after each task.

---

## Quality Gates (Constitutional Enforcement)

**See:** @.claude/skills/sdd/references/quality-gates.md

| Article | Gate | Enforcement |
|---------|------|-------------|
| I | Intelligence-First | Query project-intel.mjs BEFORE file reads |
| II | Evidence-Based | CoD^Σ traces required for all claims |
| III | Test-First | ≥2 ACs per story, tests before code |
| IV | Specification-First | spec.md required before plan.md |
| V | Template-Driven | Use standard templates |
| VI | Simplicity | ≤3 projects, ≤2 abstraction layers |
| VII | User-Story-Centric | Tasks organized by P1/P2/P3 |
| VIII | Parallelization | [P] markers for parallel tasks |

---

## Error Handling

| Error | Detection | Recovery |
|-------|-----------|----------|
| Missing spec.md | /plan without spec | "Run /feature first" |
| Audit FAIL | audit-report.md has CRITICAL | "Fix issues: [list]" |
| [NEEDS CLARIFICATION] | Markers in spec.md | "Run /clarify first" |
| No product.md | /constitution without product | "Optional: /define-product for aligned features" |
| Complex feature | Complexity detection triggers | Auto-run Phase 0 |

---

## Example Execution

**User:** "I want to create an authentication feature with OAuth"

**Orchestrator Response:**
```
I'm using the unified SDD skill to manage your development workflow.

1. [DETECT] Intent: feature (authentication with OAuth)

2. [COMPLEXITY] Checking feature complexity...
   - Keywords: "authentication", "OAuth" (integration)
   - Estimated components: Auth service, OAuth providers, session mgmt
   - Complexity: Moderate (>3 components)
   → Triggering Phase 0: System Understanding

3. [PHASE 0] Creating SYSTEM-UNDERSTANDING.md...
   - Querying project structure
   - Identifying existing auth patterns
   - Generating component diagram

4. [PHASE 3] Creating specification...
   - Quality gate: PASS (7.5/10)
   - Creating specs/016-auth-oauth/spec.md

5. [AUTO-CHAIN] Invoking /plan...
   - Creating plan.md, research.md, data-model.md

6. [AUTO-CHAIN] Generating tasks...
   - Creating tasks.md (12 tasks, 3 user stories)

7. [AUTO-CHAIN] Running /audit...
   - Result: PASS

Ready for implementation. Run /implement when ready.
```

---

## Dependencies

**Shared Imports:**
- @.claude/shared-imports/constitution.md - Constitutional principles
- @.claude/shared-imports/CoD_Σ.md - Evidence notation
- @.claude/shared-imports/memory-utils.md - Memory file utilities
- @.claude/shared-imports/master-todo-utils.md - Task tracking

**Templates:**
- @.claude/templates/feature-spec.md
- @.claude/templates/plan.md
- @.claude/templates/tasks.md
- @.claude/templates/audit-report.md
- @.claude/templates/verification-report.md

**Tools:**
- project-intel.mjs (intelligence queries)
- MCP Ref (library docs)
- AskUserQuestion (clarification)
- Task (subagent delegation)

---

## Superseded Skills

This unified skill **REPLACES** the following individual skills:
- `.claude/skills/define-product/` → Phase 1
- `.claude/skills/generate-constitution/` → Phase 2
- `.claude/skills/specify-feature/` → Phase 3
- `.claude/skills/clarify-specification/` → Phase 4
- `.claude/skills/create-implementation-plan/` → Phase 5
- `.claude/skills/generate-tasks/` → Phase 6
- `.claude/skills/implement-and-verify/` → Phase 8
- `.claude/skills/sdd-orchestrator/` → Routing logic

---

## Version

**Version:** 1.0.0
**Last Updated:** 2025-12-30
**Owner:** Claude Code Intelligence Toolkit

**Change Log:**
- v1.0.0 (2025-12-30): Initial unified SDD skill consolidating 8 individual skills
