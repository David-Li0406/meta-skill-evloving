# Plan Creation Guidelines

Additional best practices and examples for creating effective plan documents.

---

## The Three Document Types

### plan.md - "Why" and "How" at Conceptual Level

**Contains:**
- Overview (2-3 sentence summary)
- Context (why this task, current state, target state)
- Architectural approach (key design decisions, type design, module organization)
- Implementation strategy (major phases, dependencies)
- Risks & mitigations
- Success criteria

**Level:** High-level, strategic, architectural decisions

**Purpose:** Capture the reasoning and approach before diving into implementation. Answers "why are we doing this?" and "how will we structure the solution?"

### context.md - Living Implementation Details

**Contains:**
- Key files (with line ranges and descriptions)
- Key types & protocols (purpose, invariants, location)
- Implementation decisions log (date, context, decision, alternatives, impact)
- Gotchas & learnings
- Dependencies (internal and external)
- Open questions
- Future considerations

**Level:** Tactical, updated as you work, captures learnings

**Purpose:** Document the implementation reality as it unfolds. This is your "lab notebook" - record what works, what doesn't, why you made changes, and what you learned.

### tasks.yaml - Machine-Readable Work Checklist

**Contains:**
- `spec`: spec identifier
- `code`: ID prefix for tasks (e.g., FEAT → FEAT-001)
- `tasks`: list with id, content, status, active_form, optional evidence
- `meta`: created, last_updated, progress
- `phases`: optional grouping with checkpoints

**Level:** Granular, actionable, machine-readable

**Purpose:** Track progress with structured data. Used by dignity for task management. Each task should be completable in < 2 hours with obvious "done" criteria.

---

## Document Creation Guidelines

### Be Specific
- Use concrete file paths with line numbers when possible
- Name actual types, functions, and modules
- Avoid vague descriptions

### Be Current
- Base content on actual codebase state (read files first)
- Don't assume - verify by reading code
- Document what IS, not what you think should be

### Be Actionable
- Every task must have clear completion criteria
- Include specific commands to run
- Make it obvious when something is done

### Follow Project Style
- Type-driven development (types first, implementation follows)
- Immutable by default (`@dataclass(frozen=True)`)
- Composition over inheritance (protocols, not base classes)
- Parse-don't-validate (Pydantic at boundaries)
- Radical explicitness (`kw_only=True`, no hidden behavior)
- Pattern matching with keyword patterns (not positional)
- No behavioral inheritance except exceptions
- Exceptions by default (Result types only for: async task coordination, batching validation errors)

### Keep Synchronized
- Update documents as you work (not just at the end)
- Mark tasks complete immediately when finished
- Log decisions in context.md as they happen
- Add gotchas and learnings in real-time

## Examples

### Good Task Descriptions

```markdown
- [ ] **Add `TemporalJoin` type to `src/feature_link/dsl.py`**
  - **Files**: `src/feature_link/dsl.py`
  - **Approach**: Frozen dataclass with `left`, `right`, `time_column` fields
  - **Completion criteria**: Type exists, pyright passes, unit test validates construction
```

### Bad Task Descriptions

```markdown
- [ ] Work on temporal joins
  - Add some types
  - Make it work
```

### Good Decision Log Entry

```markdown
### 2025-11-05 - Use Ibis Expression for Join Conditions

**Context**: Need to represent join conditions in a way that integrates with Ibis backend.

**Decision**: Use `ir.Expr` type for join conditions instead of string predicates.

**Alternatives Considered**:
- String-based predicates: Too error-prone, no type safety
- Custom AST: Reinventing what Ibis already provides

**Impact**: Join construction becomes type-safe. Users get IDE completion for column references.
```

### Bad Decision Log Entry

```markdown
### Some Date - Made a choice

**Context**: Needed to decide something

**Decision**: Picked option A

**Alternatives**: Option B wasn't good
```

### Good File Descriptions

```markdown
### Core Implementation

- **`src/feature_link/compile.py`** (lines 45-120)
  Compilation logic that transforms View IR to Ibis expressions.
  Invariant: All RelationRef nodes must resolve to valid View objects before compilation.
  Uses pattern matching on IR node types (keyword patterns, not positional).
```

### Bad File Descriptions

```markdown
### Core Implementation

- **`src/feature_link/compile.py`**
  Has some code for compilation stuff.
```

## When NOT to Create Plan Documents

These documents are for **complex, multi-phase tasks** only. Skip this for:
- Simple bug fixes
- Trivial refactorings
- Single-file changes
- Tasks completable in < 30 minutes

For simple tasks, just use TodoWrite directly.

## Integration with CLAUDE.md

See [CLAUDE.md "Starting Large Tasks"](CLAUDE.md#starting-large-tasks) for:
- When to create plans
- How plans fit into workflow
- Integration with git commits and PRs

## Project Style Reference

All code in plan documents should follow [STYLE.md](STYLE.md) principles:
- Type-driven (make illegal states unrepresentable)
- Composition-first (protocols over ABC over inheritance)
- Parse-don't-validate (validation at boundaries, trust internally)
- Immutable by default (frozen dataclasses)
- Explicit over implicit (kw_only, no hidden dependencies)
