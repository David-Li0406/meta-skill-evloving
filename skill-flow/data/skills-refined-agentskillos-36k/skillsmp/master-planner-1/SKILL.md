---
name: master-planner
description: Master planning orchestrator. This skill MUST be activated when the /plan command is executed or when creating implementation plans. Transforms user requests into research-backed, execution-ready plans (PRP) using Context7 (official docs), Tavily (web research), and Sequential Thinking (structured reasoning). Follows R.P.I.V workflow: Research → Plan → (optional) Implement → Validate.
---

# 🎯 Master Planner — PRP Edition v6.0

> **CORE**: Context Density > Brevity | Research-First > Implementation | Planning > Coding

```yaml
METHODOLOGY: "PRP (Product Requirement Prompt) + ACE (Agentic Context Engineering)"
PHILOSOPHY: "One-pass implementation success through comprehensive context"
TRIGGER: "/plan command OR any planning/architecture request"
```

---

## 🔴 Activation Triggers

This skill is **MANDATORY** when:

1. User executes `/plan` command
2. Building a plan, roadmap, or architecture (new feature/system/migration)
3. High uncertainty, many unknowns, or risk of hallucination without research
4. Need to align with **current** best practices / official docs
5. Multi-step execution requiring task decomposition, validations, and rollback
6. Integrations (APIs, frameworks, infra, security/compliance)

**Do NOT use** for:

- Pure copywriting/creative tasks with no research needed
- Simple Q&A with no implementation required
- Tasks fully solvable from provided context

---

## 🧠 Foundational Principles

**PRP = PRD + Curated Codebase Intelligence + Agent Runbook**

```yaml
PRP_LAYERS:
  layer_1: "What + Why (goal)"
  layer_2: "Curated codebase intelligence (files, patterns)"
  layer_3: "Agent execution playbook (steps, validations, rollback)"

ACE_MECHANISM:
  generator: "Executes reasoning, tool calls"
  reflector: "Extracts insights from execution"
  curator: "Applies incremental updates to context"
  grow_and_refine: "Add insights → Track helpfulness → Prune redundancy"
```

---

## 📊 Complexity Classification

| Level  | Indicators                | Thinking Budget | Research Depth |
| ------ | ------------------------- | --------------- | -------------- |
| L1-L2  | Bug fix, single function  | 1K-4K tokens    | Repo-only      |
| L3-L5  | Feature, multi-file       | 8K-16K tokens   | Docs + repo    |
| L6-L8  | Architecture, integration | 16K-32K tokens  | Deep           |
| L9-L10 | Migrations, multi-service | 32K+ tokens     | Comprehensive  |

---

## 🔧 MCP Tools (Mandatory Usage)

### Context7 — Official Documentation

```yaml
triggers:
  - Convex (queries, mutations, schema)
  - Clerk (auth, users, sessions)
  - TanStack Router (routes, loaders)
  - shadcn/ui (components)
  - Recharts (charts, visualization)
  - Any npm library/API
  - Vite, Biome, TypeScript config

usage: "resolve-library-id → query-docs"
```

### Tavily — Web Research

```yaml
triggers:
  - Context7 returns insufficient info
  - Deploy/runtime errors without clear solution
  - Best practices / modern patterns (2024+)
  - Undocumented integrations

usage: "tavily-search → tavily-extract if URL promising"
```

### Sequential Thinking — Structured Reasoning

```yaml
triggers:
  - L4+ complexity tasks
  - After any build/deploy/runtime error
  - Every 5 implementation steps (progress check)
  - Multiple approaches possible (trade-off analysis)
  - Architectural decisions

usage: "Break into steps, analyze root cause, compare options"
```

---

## 🔬 R.P.I.V Workflow (Mandatory Order)

### Phase 0: RESEARCH (Always First)

**Goal:** Eliminate unknowns and lock in best-practice approach.

```yaml
priority_order:
  1: "Search codebase for patterns, conventions"
  2: "Query Context7 for official docs"
  3: "Tavily web search for best practices, security"
  4: "Delegate to specialists if domain-specific"

outputs:
  - "Findings Table: | # | Finding | Confidence (1-5) | Source | Impact |"
  - "Knowledge Gaps: what you still don't know"
  - "Assumptions to Validate: explicit assumptions requiring confirmation"
  - "Edge Cases / Failure Modes: at least 5 when complexity ≥ L4"

anti_hallucination:
  - "NEVER speculate about unopened code"
  - "MUST read files before making claims"
  - "Search and verify BEFORE responding"
  - "If fact unknown: research it OR mark as Knowledge Gap"
```

### Phase 1: PLAN (Before Any Implementation)

**Goal:** Convert research into execution runbook with atomic tasks.

```yaml
decomposition:
  method: "Atomic Task Decomposition"
  principle: "Each task completable in isolation with clear validation"

task_template:
  id: "AT-XXX"
  title: "Action verb + specific target"
  phase: "1-5 (foundation → core → integration → polish → validation)"
  priority: "critical | high | medium | low"
  dependencies: "[AT-XXX]"
  parallel_safe: "true/false (mark ⚡ PARALLEL-SAFE when true)"
  files_to_create: "[paths]"
  files_to_modify: "[paths]"
  validation: "Specific command/check"
  rollback: "Exact undo steps"
  acceptance_criteria: "[measurable bullets]"

parallel_safe_when:
  - "No shared file modifications"
  - "No dependency chain"
  - "Independent validation"
```

### Phase 2: IMPLEMENT (Only If Requested)

**Goal:** Execute per atomic tasks with validation gates.

```yaml
behavior: "PROACTIVE"
instruction: |
  Implement changes instead of suggesting.
  Infer intent and proceed using tools.
  Trust existing references, execute directly.

pattern: "Implement → Validate → Commit (or Rollback)"
validation_after_each: true

quality_gates:
  - "bun run lint"
  - "bun run typecheck"
  - "bun run test"
  - "bun run build"

anti_hardcoding: |
  Write general-purpose solutions for ALL valid inputs.
  Never hard-code for specific test cases.
  Report incorrect tests instead of workarounds.
```

### Phase 3: VALIDATE (Always)

```yaml
tasks:
  - "Build: zero errors"
  - "Lint: zero warnings"
  - "Tests: all passing"
  - "@code-reviewer if security involved"
  - "@database-specialist if schema changes"

reflection: |
  After each result, reflect on quality and
  determine optimal next steps before proceeding.

success: "All gates pass, no regressions, docs updated, backward compatible"
```

---

## 🎯 Operating Modes

### CONSERVATIVE (Default for /plan command)

- Deliver research synthesis + plan + validation gates
- Do NOT produce code unless explicitly requested
- Output: `docs/PLAN-{task-slug}.md`

### PROACTIVE (For implementation requests)

- Proceed from plan → implementation steps
- Still follow research-first and validation gates
- Pattern: Implement → Validate → Commit (or Rollback)

---

## 📄 Output Contract

### When /plan is executed:

**Artifact A — Research Digest** (in plan file)

- Findings Table
- Knowledge Gaps
- Assumptions to Validate
- Recommended approach + rationale
- Risks + mitigations

**Artifact B — PLAN-{slug}.md** (implementation-ready)

```yaml
# File: docs/PLAN-{task-slug}.md

# [Task Title]

## Metadata
complexity: "L[1-10] — [JUSTIFICATION]"
estimated_time: "[DURATION]"
parallel_safe: [true/false]

## Objective
task: "[ACTION VERB] + [TARGET] + [OUTCOME]"
context: "[PROJECT], [STACK], [CONSTRAINTS]"
why_this_matters: "[MOTIVATION]"

## Environment
runtime: "Bun 1.x"
framework: "React 19"
database: "Convex"
auth: "Clerk"
ui: "shadcn/ui"
testing: "Vitest"

## Research Summary
### Findings Table
| # | Finding | Confidence | Source | Impact |

### Knowledge Gaps
- [gaps]

### Assumptions to Validate
- [assumptions]

## Relevant Files
### Must Read
- path: "[PATH]"
  relevance: "[WHY]"

### May Reference
- path: "[PATH]"
  relevance: "[WHY]"

## Existing Patterns
naming: "[DESCRIBE]"
file_structure: "[DESCRIBE]"
error_handling: "[DESCRIBE]"
state_management: "[DESCRIBE]"

## Constraints
non_negotiable: ["[CONSTRAINT_1]", "[CONSTRAINT_2]"]
preferences: ["[PREFERENCE_1]"]

## Chain of Thought
### Research
- Codebase patterns: _____
- Docs consulted: _____
- Security: _____
- Edge cases: _____

### Analyze
- Core requirement: _____
- Technical constraints: _____
- Integration points: _____

### Think
step_by_step: ["First: _____", "Then: _____", "Finally: _____"]
tree_of_thoughts:
  approach_a: {description, pros, cons, score}
  approach_b: {description, pros, cons, score}
  selected: "[CHOSEN]"
  rationale: "[WHY]"

## Atomic Tasks
- id: "AT-001"
  title: "[ACTION] [TARGET]"
  phase: 1
  priority: "critical"
  dependencies: []
  parallel_safe: true
  files_to_create: ["[PATH]"]
  files_to_modify: ["[PATH]"]
  validation: "[COMMAND]"
  rollback: "[UNDO]"
  acceptance_criteria: ["[CRITERION]"]

## Validation Gates
automated:
  - {id: "VT-001", command: "bun run build", expected: "Exit 0"}
  - {id: "VT-002", command: "bun run lint", expected: "No errors"}
  - {id: "VT-003", command: "bun run test", expected: "All pass"}
manual_review:
  - {reviewer: "@code-reviewer", focus: "[ASPECT]", required_if: "[CONDITION]"}

## Output
format: "[DELIVERABLE]"
files_created: [{path, purpose}]
files_modified: [{path, changes}]
success_definition: "[CRITERIA]"
failure_handling: "If [CONDITION], then [ACTION]. Rollback: [STEPS]"
```

---

## 📋 Naming Convention (for PLAN files)

| Request                           | Plan File                     |
| --------------------------------- | ----------------------------- |
| `/plan e-commerce site with cart` | `docs/PLAN-ecommerce-cart.md` |
| `/plan mobile app for fitness`    | `docs/PLAN-fitness-app.md`    |
| `/plan add dark mode feature`     | `docs/PLAN-dark-mode.md`      |
| `/plan SaaS dashboard`            | `docs/PLAN-saas-dashboard.md` |

**Rules:**

1. Extract 2-3 key words from request
2. Lowercase, hyphen-separated
3. Max 30 characters

---

## ⚠️ Anti-Patterns

| Bad                | Good                                                                           |
| ------------------ | ------------------------------------------------------------------------------ |
| "Implement auth"   | Research → Search codebase → Query docs → Then implement                       |
| "Build entire CRM" | Decompose: AT-001 schema, AT-002 API, AT-003 UI...                             |
| "Create dashboard" | Create dashboard with: real-time, responsive, dark/light, loading states, a11y |
| Skip research      | ALWAYS research first, even for "simple" tasks                                 |
| Guess file paths   | Search and verify paths before referencing                                     |

---

## ✅ Pre-Submission Checklist

```yaml
research:
  - [ ] Codebase searched?
  - [ ] Docs consulted (Context7)?
  - [ ] Web research done (Tavily)?
  - [ ] Security/compliance identified?
  - [ ] Edge cases considered (min 5 for L4+)?

context:
  - [ ] Findings Table included?
  - [ ] Knowledge Gaps listed?
  - [ ] Assumptions to Validate listed?
  - [ ] Relevant files specified?
  - [ ] WHY included for instructions?

tasks:
  - [ ] Truly atomic?
  - [ ] Validation command each?
  - [ ] Dependencies mapped?
  - [ ] Rollback defined?
  - [ ] Parallel-safe marked?

behavior:
  - [ ] Mode specified (CONSERVATIVE/PROACTIVE)?
  - [ ] Output format explicit?
  - [ ] Success criteria measurable?
  - [ ] Failure handling defined?
```

---

## 🚀 Quick Reference

```
R.P.I.V: RESEARCH → PLAN → IMPLEMENT → VALIDATE

GOLDEN RULES:
✓ RESEARCH FIRST — never implement blind
✓ Be EXPLICIT — agent follows literally
✓ Explain WHY — enables generalization
✓ CONTEXT DENSITY > BREVITY
✓ ATOMIC TASKS — small, validated, rollback-ready
✓ PARALLEL TOOLS — unless dependencies
✓ REFLECT AFTER TOOLS — think before next action

COMPLEXITY → BUDGET:
L1-L2: 1K-4K   | Bug fix, refactor
L3-L5: 8K-16K  | Feature, API
L6-L8: 16K-32K | Architecture
L9-L10: 32K+   | New systems
```

---

## 📝 Example Execution

**User:** `/plan add SSO with Okta to our SaaS`

**Agent (this skill) does:**

1. **RESEARCH:**
   - Context7: Auth framework docs
   - Tavily: Okta best practices, security pitfalls
   - Codebase: Current auth patterns
2. **Produce Research Digest** with findings table
3. **Create `docs/PLAN-okta-sso.md`** with:
   - AT-001: Choose SSO flow + threat model
   - AT-002: Implement OIDC config
   - AT-003: Add audit logs
   - AT-004: Add tests + rollout plan
   - Validation gates + rollback steps

---

## 🔔 Post-Planning Message

After creating the plan file, inform user:

```
✅ Plan created: docs/PLAN-{slug}.md

Next steps:
- Review the plan
- Run `/implement` to start implementation
- Or modify plan manually
```
