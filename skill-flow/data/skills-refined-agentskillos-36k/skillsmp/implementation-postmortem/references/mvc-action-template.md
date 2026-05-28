# MVC / Action-Command Pipeline Postmortem Template

Use this template when reviewing implementations following MVC patterns with action/command pipelines, particularly GPUI-based applications or similar frameworks where "if there is no command, the feature doesn't exist."

## Architecture-Specific Dimensions

### Action/Command Pipeline Integrity

The central invariant: all user-visible behaviour flows through Action → Command.

**Examine:**
- Features that bypass the command bus (direct state mutation)
- Actions not invocable from all surfaces (UI, keyboard, scripting, tests)
- Commands that aren't undoable when they should be
- Command grouping correctness (macro operations as atomic undo units)

**Specific questions:**
- Can every user-visible operation be replayed from a command log?
- Are there "god commands" that do too much? Commands that do too little?
- Does the scripting surface expose the same operations as the UI?
- Are command names/IDs stable enough for script compatibility across versions?

**Smell test:** Record a macro via scripting. Replay it. Does it produce identical results? If not, where does determinism break?

### Model/View/Controller Boundaries

**Model (Engine/Core State):**
- Document model changes require commands, always?
- Is the model the single source of truth?
- Are there view-specific concerns polluting the model?

**View (UI Layer):**
- Are views purely projections of model state + action dispatchers?
- Views holding derived state that can drift from source?
- Excessive logic in `render()` methods that belongs elsewhere?

**Controller (Command Bus / Tools):**
- Validation happening at the right layer?
- Routing logic clean or accumulating special cases?
- History management correct (clear-on-open, save-point tracking)?

**Boundary violation patterns:**
- View code importing model internals (should only see public API)
- Model code knowing about UI framework types
- Commands containing view/UI concepts

### Framework Register Discipline

For frameworks with explicit state categories (e.g., GPUI's entities/views/elements):

**Entities (state & services):**
- Is authoritative state in entities, not views?
- Are services cleanly separated?
- Any entity holding UI-specific state?

**Views (declarative UI):**
- Are views purely projections + dispatchers?
- Views holding derived state that drifts?
- Too much logic in render methods?

**Elements (imperative rendering):**
- Are elements doing computation that belongs elsewhere?
- Element code mutating entity state directly? (violation)
- Custom elements that should be framework widgets (or vice versa)?

**Context safety:** Any code holding context objects across async boundaries that shouldn't?

### Tool/FSM Evaluation

If tools are implemented as finite state machines:

**Per-tool assessment:**

| Tool | States | Input Coverage | Command Emission | Cancellation | Verdict |
|------|--------|----------------|------------------|--------------|---------|
| | count | mouse/key/a11y | clean/interleaved | clean/leaky | |

**Cross-tool questions:**
- Clear tool trait/interface, or each tool invented its own patterns?
- Tool activation/deactivation lifecycle—leaked state between activations?
- Do tools update state via commands, not directly?

**State machine smells:**
- State explosion (FSM becoming untractable)
- Missing transitions (input combinations not handled)
- Commands interleaved with state logic (should be separate)

### Cross-Cutting Concerns

#### Accessibility (if applicable)

- Stable node ID generation (deterministic from state)?
- All interactive controls have roles, labels, states, actions?
- Keyboard-only operation path tested?
- Screen-reader-blocking patterns?

#### Localization (if applicable)

- Inline strings that escaped the message catalog?
- Command names/shortcut descriptions localized?
- UI layout tolerates string expansion?

#### Scripting (if applicable)

- API stability across versions?
- Read-only access truly read-only?
- Long operations report progress?
- Error messages actionable from script context?

### Invariant Scorecard

If the architecture defines explicit invariants, assess each:

| Invariant | Status | Evidence |
|-----------|--------|----------|
| All behaviour through commands | ✓/✗ | |
| Single source of truth | ✓/✗ | |
| Deterministic state transitions | ✓/✗ | |
| [Add project-specific invariants] | | |

For any ✗:
- What violated it
- Why (intentional tradeoff vs oversight)
- Remediation path

## MVC-Specific Smells

| Smell | Symptom | Likely Cause |
|-------|---------|--------------|
| Fat controller | Controller > 500 lines | Business logic not in model |
| Zombie state | View state drifts from model | Derived state not invalidated |
| Command bypass | Direct model mutation | Missing command abstraction |
| Tool spaghetti | Inconsistent tool implementations | No clear tool trait/interface |
| Undo amnesia | Some operations not undoable | Command grouping issues |

## Module/Crate Boundary Enforcement

If the architecture specifies a module structure:

**Check:**
- Core module has no UI framework dependency?
- UI module depends on core, not vice versa?
- Circular dependencies between modules?
- Types in wrong modules?

**Visualise:** Draw actual dependency graph. Compare to intended structure. Explain every deviation.
