# Spec Framework: Design Rationale

A task-tracking framework with graduated context capture for AI-assisted development.

## The Problem with Spec-Driven Development

Spec-driven development emerged as a [key engineering practice in 2025](https://www.thoughtworks.com/en-gb/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices), but Birgitta Böckeler's [analysis of SDD tools](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) identifies fundamental problems with current approaches:

| Problem | Manifestation |
|---------|---------------|
| **One-size-fits-all workflows** | Kiro's 3-step process turned a small bug into 4 "user stories" with 16 acceptance criteria |
| **Markdown proliferation** | spec-kit generates 8+ files per feature—more reviewing than coding |
| **False sense of control** | Agents ignore elaborate instructions despite large context windows |
| **Spec maintenance burden** | Unclear if specs should live forever or die after implementation |

The tools she reviewed (Kiro, spec-kit, Tessl) share a flawed assumption: **specs as normative truth that code must conform to.**

## Our Approach: Specs as Ephemeral Scaffolding

This framework inverts the relationship:

| SDD Tools | This Framework |
|-----------|----------------|
| Spec is source of truth | Git is source of truth |
| Code generated from spec | Spec provides context for focused work |
| Specs maintained forever | Specs archived when done—immutable |
| One workflow for all sizes | Graduated complexity by issue type |
| Normative (prescriptive) | Descriptive (records intent and decisions) |

### Core Principles

**1. Specs are immutable records of intent**

Changes don't modify existing specs—they create new ones. The archive is a permanent trail of decisions, not a living documentation system. Git shows *what* changed; specs show *why*.

**2. Graduated complexity**

| Issue Type | Duration | Output | Validation |
|------------|----------|--------|------------|
| Task | Hours/days | 2 files | 3 questions max |
| Feature | Days/weeks | 5 files | 5 questions, opt-in sections |
| Initiative | Weeks/months | 5 files | Full taxonomy, gates |

Most SDD tools apply maximum ceremony to every change. This framework scales complexity with scope.

**3. Task tracking over specification**

The real artifact is `tasks.yaml`—a machine-readable task list that syncs with TodoWrite and tracks progress. The spec documents provide context; the task list drives execution.

**4. Human vs. tooling artifacts**

```
For humans (review these):
├── spec.md      # Strategic "why"
└── context.md   # Tactical "what we learned"

For tooling / deep auditing:
├── tasks.yaml        # Progress tracking, TodoWrite sync
├── dependencies.yaml # Parallel dispatch DAG
└── validation.yaml   # Audit trail, gate checks
```

Review burden: 2 documents, not 8. The YAML files are infrastructure.

## Why LLMs Need Scaffolding

[Research on LLM context limitations](https://www.infoq.com/minibooks/ai-assisted-development-2025/) explains why structured scaffolding helps:

### The "Lost in the Middle" Problem

LLMs exhibit a U-shaped attention pattern—they retrieve information well from the beginning and end of context, but accuracy drops from 80%+ to under 40% for [information buried in the middle](https://medium.com/@shashwatabhattacharjee9/the-context-window-paradox-engineering-trade-offs-in-modern-llm-architecture-d22d8f954a05). As context grows, attention probability spreads thinner across tokens.

### Context Rot

LLMs have an "attention budget" that depletes as more tokens are added—a phenomenon called "[context rot](https://www.understandingai.org/p/context-rot-the-emerging-challenge)." By keeping each interaction focused on a specific subtask, you minimize distractor tokens and preserve the model's ability to attend to relevant information.

### Task Decomposition Works

[Breaking work into focused chunks](https://blog.continue.dev/task-decomposition/):
- Avoids attention dilution across irrelevant tokens
- Prevents the "lost in the middle" problem by keeping context small
- Enables the model to focus its attention budget on the task at hand
- Reduces quadratic scaling costs through smaller sequence lengths

This framework creates **focused scaffolds for a day's work**—enough context to keep the LLM on track without overwhelming its attention capacity.

## Learning from Past Failures

### Model-Driven Development (MDD)

Böckeler draws parallels to MDD, which also promised code generation from specifications. [MDD](https://www.infoq.com/articles/mdd-misperceptions-challenges/) [failed](https://neil-crofts.medium.com/whatever-happened-to-model-driven-development-ec0175139720) because:

- Added more complexity than it removed
- Tools were expensive, unreliable, or both
- Incompatible with developer mental models
- Round-trip engineering was painful

LLMs remove some MDD constraints (no predefined spec language, no elaborate generators), but introduce non-determinism. This framework accepts non-determinism by:
- Using specs as context, not contracts
- Validating through tests, not spec conformance
- Archiving specs after completion rather than maintaining them

### "Just Enough" Documentation

Scott Ambler's Agile principle of "[just barely good enough](https://agilemodeling.com/essays/agiledocumentation.htm)" documentation applies here:

- **Too little**: LLM lacks context, produces incorrect code
- **Too much**: Review burden, documentation rot, wasted effort

The framework's graduated complexity applies the Pareto principle: [80% of value from 20% of documentation effort](https://beyondthebacklog.com/2024/09/21/minimum-viable-documentation-2/). Tasks get 2 files. Initiatives get 5.

## The Temporal Dimension

Böckeler identifies [three levels of SDD](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) that tools conflate:

| Pattern | Duration | Spec Lifecycle |
|---------|----------|----------------|
| **Spec-first** | Single task | Created → Used → Deleted |
| **Spec-anchored** | Feature lifetime | Created → Used → Maintained |
| **Spec-as-source** | Forever | Spec replaces code as artifact |

This framework is **spec-anchored at the feature level, but immutable**:
- Spec created when feature work begins
- Spec provides context throughout implementation
- Spec archived (not maintained) when complete
- New features get new specs

The archive is a historical record. Looking at archived specs reveals the pattern:

```
sdd-integration:        created 2025-12-17, completed 2025-12-17
spec-validate-batch:    created 2025-12-11, completed 2025-12-11
task-dispatch-redesign: created 2025-12-14, completed 2025-12-14
```

These are day-scale scaffolds, not permanent architecture documents.

## Integration with TDD

The framework aligns with Test-Driven Development:

| TDD | Spec Framework |
|-----|----------------|
| RED: Write failing test | Create spec with acceptance criteria |
| GREEN: Make test pass | Implement until criteria met |
| REFACTOR: Clean up | Archive spec, start fresh |

Both enforce:
- Clear success criteria before implementation
- Tight feedback loops
- Concrete examples over abstract descriptions
- Validation through execution, not inspection

The `code-test` skill enforces TDD at the code level. The spec framework applies the same discipline at the feature level.

## Key Differences from SDD Tools

### vs. [Kiro](https://kiro.dev/)
- **Kiro**: Single workflow (Requirements → Design → Tasks) for everything
- **This**: Graduated complexity—Tasks skip validation.yaml entirely

### vs. [spec-kit](https://github.com/github/spec-kit)
- **spec-kit**: 8+ markdown files, branch per spec, checklists everywhere
- **This**: 2 human-facing docs, YAML for tooling, archive when done

### vs. [Tessl](https://docs.tessl.io/)
- **Tessl**: Spec-as-source with 1:1 spec-to-code mapping
- **This**: Spec-as-context—git remains source of truth

### Common Thread

All three tools treat specs as normative artifacts that must be maintained and synchronized with code. This framework treats specs as **working memory frames** that exist to keep the LLM focused, then become historical records.

## Practical Implications

### When to Create Specs

**DO use for:**
- Multi-step features requiring coordination
- Work where decisions need recording
- Tasks benefiting from explicit acceptance criteria

**DON'T use for:**
- Single-file changes
- Trivial bug fixes
- Tasks completable in < 30 minutes

### The Validation Loop

`spec-validate` runs an ambiguity scan before asking questions:
- If all areas are clear → proceed silently (no confirmation needed)
- If gaps found → ask prioritized questions (Impact × Uncertainty)

Question limits force prioritization:
- Tasks: 3 questions max
- Features/Initiatives: 5 questions max

### Status Synchronization

`spec-update` syncs `tasks.yaml` status with reality via git history analysis. The spec documents themselves remain immutable—only task completion status needs synchronization. This is rarely needed since TodoWrite hooks handle real-time updates, but useful when resuming work in a new session or on another machine.

## Key Insight

**Don't fight LLM limitations—work with them.**

Short-lived specs, tight feedback loops, verification through tests, fresh context per task. The SDD machinery (gates, markers, taxonomy) exists to help *you* think clearly before writing tasks—not to constrain the LLM.

| Traditional SDD | This Framework |
|-----------------|----------------|
| Spec constrains LLM behavior | Spec provides LLM context |
| Control via spec compliance | Control via test verification |
| Fight non-determinism | Accept non-determinism |
| Long-lived specs requiring maintenance | Short-lived specs, then archive |

The spec doesn't need to perfectly capture requirements. It needs to capture *enough* for the LLM to write good tasks. The tests verify correctness—not the spec.

## Deterministic Enforcement with Cupcake

The framework integrates with [Cupcake](https://cupcake.eqtylab.io/)—a policy enforcement layer that provides **deterministic control without consuming context tokens**.

### Three-Legged Control

| Mechanism | Role | Deterministic? |
|-----------|------|----------------|
| **Specs** | Provide focused context | No (LLM interprets) |
| **Tests** | Verify correctness | Yes (pass/fail) |
| **Cupcake** | Enforce operational rules | Yes (policy-as-code) |

Traditional SDD tries to control LLMs through elaborate specs. This framework accepts that LLMs are non-deterministic and adds deterministic layers:

```
LLM (non-deterministic) + Tests (deterministic) + Cupcake (deterministic) = Control
```

### Policy Examples

**Skill suggestions** (`skill_suggestions.rego`):
```rego
add_context contains msg if {
    input.hook_event_name == "UserPromptSubmit"
    contains(lower(input.prompt), "debug")
    msg := "Consider using `code-debug` skill for systematic debugging."
}
```

**Workflow transitions** (`todo_transitions.rego`):
```rego
add_context contains msg if {
    input.hook_event_name == "PostToolUse"
    input.tool_name == "TodoWrite"
    all_completed
    msg := "All tasks completed. Consider using `spec-archive` skill."
}
```

### Why This Matters

Rules in `CLAUDE.md` consume context and may be ignored. Cupcake policies:
- **Run outside the model** - No token cost
- **Evaluate deterministically** - OPA Rego compiled to WASM
- **Intercept tool calls** - Block, modify, or allow with feedback
- **Trigger automation** - Suggest skills, enforce workflows

This moves operational rules from "hope the LLM follows them" to "enforce them deterministically."

## References

### Primary Source
- Böckeler, B. (2025). [Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html). Martin Fowler's blog.

### LLM Context and Attention
- [The Context Window Paradox: Engineering Trade-offs in Modern LLM Architecture](https://medium.com/@shashwatabhattacharjee9/the-context-window-paradox-engineering-trade-offs-in-modern-llm-architecture-d22d8f954a05)
- [Context rot: the emerging challenge that could hold back LLM progress](https://www.understandingai.org/p/context-rot-the-emerging-challenge)
- [Stop Asking AI to Build the Whole Feature: The Art of Focused Task Decomposition](https://blog.continue.dev/task-decomposition/)

### Agile Documentation
- Ambler, S. [Lean/Agile Documentation: Strategies for Agile Software Development Teams](https://agilemodeling.com/essays/agiledocumentation.htm)
- [Minimum Viable Documentation for Agile Product Teams](https://beyondthebacklog.com/2024/09/21/minimum-viable-documentation-2/)

### AI-Assisted Development Patterns
- [AI Assisted Development: Real World Patterns, Pitfalls, and Production Readiness](https://www.infoq.com/minibooks/ai-assisted-development-2025/)
- [Spec-driven development: Unpacking 2025's key new engineering practices](https://www.thoughtworks.com/en-gb/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)

### Historical Context
- [Model Driven Development Misperceptions and Challenges](https://www.infoq.com/articles/mdd-misperceptions-challenges/)
- [Whatever happened to model driven development?](https://neil-crofts.medium.com/whatever-happened-to-model-driven-development-ec0175139720)

### Policy Enforcement
- [Cupcake: Make AI agents follow the rules](https://cupcake.eqtylab.io/)
- [Open Policy Agent (OPA)](https://www.openpolicyagent.org/)
