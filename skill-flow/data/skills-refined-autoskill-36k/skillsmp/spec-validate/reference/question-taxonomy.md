# Question Taxonomy Reference

Templates for generating multiSelect clarification questions by taxonomy area.

---

## Question Format

Questions are batched by taxonomy area using AskUserQuestion with multiple questions.

**Batch format (multiple questions in same area):**

```
AskUserQuestion with questions array:

[
  {
    question: "First question about [area]?",
    header: "[Area]",
    multiSelect: false,
    options: [
      { label: "Option A", description: "[implication]" },
      { label: "Option B", description: "[implication]" },
      { label: "Option C", description: "[implication]" }
    ]
  },
  {
    question: "Second question about [area]?",
    header: "[Area]",
    multiSelect: false,
    options: [...]
  }
]
```

**Single question format:**

```
Question: [Clear question ending with ?]
Header: [Area name, max 12 chars]
multiSelect: false (unless multiple answers make sense)
Options:
- Option A: [choice] - [implication/trade-off]
- Option B: [choice] - [implication/trade-off]
- Option C: [choice] - [implication/trade-off]
- None: [default behavior / skip this concern]
```

**Batch limits:**
- Tasks: up to 3 questions per batch, up to 3 batches
- Features/Initiatives: up to 4 questions per batch (AskUserQuestion max), up to 7 batches

---

## Recommended Options

When one option is clearly preferred based on codebase patterns, industry standards, or project conventions, mark it as recommended.

**Pattern:**
1. Place recommended option first in the options list
2. Append "(Recommended)" to the label

**Example:**
```
Header: Behavior
Question: How should export handle invalid data?

- Skip and continue (Recommended): Log errors, export valid rows - Matches existing error handling
- Fail immediately: Stop on first error - Strict validation
- Quarantine: Separate valid/invalid files - Complete audit trail
- None: I'll specify the exact behavior
```

**Batch format example:**
```
{
  question: "How should export handle invalid data?",
  header: "Behavior",
  options: [
    { label: "Skip and continue (Recommended)", description: "Matches existing patterns" },
    { label: "Fail immediately", description: "Stop on first error" },
    { label: "Quarantine", description: "Separate valid/invalid files" }
  ]
}
```

**When to recommend:**
- Clear codebase precedent exists
- Industry standard practice applies
- One option significantly reduces complexity

**When NOT to recommend:**
- Options are equally valid trade-offs
- User context determines best choice
- No clear advantage to any option

---

## Scope

**Purpose:** Define boundaries of what's included vs excluded.

**Question patterns:**
- "What is in scope for this work?"
- "What should be explicitly excluded?"
- "How does this relate to [adjacent area]?"

**Option template:**
```
Header: Scope
Question: What boundaries define this [initiative/feature/task]?

- Narrow: [minimal scope] - Faster delivery, less complexity
- Balanced: [moderate scope] - Covers core needs, reasonable timeline
- Comprehensive: [broad scope] - Complete solution, longer timeline
- None: Keep scope as currently described
```

**Example:**
```
Header: Scope
Question: What should the export feature cover?

- Core formats only: CSV and JSON - Ship faster, add more later
- Common formats: CSV, JSON, Parquet - Covers most use cases
- All formats: CSV, JSON, Parquet, Excel, XML - Complete but complex
- None: Let me specify the exact formats needed
```

---

## Behavior

**Purpose:** Clarify how the system should act in specific situations.

**Question patterns:**
- "How should [component] behave when [scenario]?"
- "What happens if [condition]?"
- "Should [action] be [automatic/manual/configurable]?"

**Option template:**
```
Header: Behavior
Question: How should [component] handle [scenario]?

- Strict: [fail fast behavior] - Clear feedback, no ambiguity
- Lenient: [permissive behavior] - Flexible, may mask issues
- Configurable: [user chooses] - Most flexible, more complexity
- None: Use standard/existing behavior patterns
```

**Example (single question):**
```
Header: Behavior
Question: How should export handle invalid data?

- Fail immediately: Stop on first error - Clear feedback, strict validation
- Skip and continue: Log errors, export valid rows - Best effort, may lose data
- Quarantine: Separate valid/invalid into different files - Complete audit trail
- None: Follow existing error handling patterns in codebase
```

**Example (batch with multiple Behavior questions):**
```
AskUserQuestion([
  {
    question: "How should export handle invalid data?",
    header: "Behavior",
    options: [
      { label: "Fail immediately", description: "Stop on first error" },
      { label: "Skip and continue", description: "Log errors, export valid rows" },
      { label: "Quarantine", description: "Separate valid/invalid files" }
    ]
  },
  {
    question: "Should export operations be cancellable mid-stream?",
    header: "Behavior",
    options: [
      { label: "Yes, immediate", description: "Cancel and clean up partial output" },
      { label: "Yes, graceful", description: "Finish current batch, then stop" },
      { label: "No", description: "Run to completion once started" }
    ]
  }
])
```

---

## Data Model

**Purpose:** Define structure and relationships of data entities.

**Question patterns:**
- "What structure should [entity] have?"
- "How do [entity A] and [entity B] relate?"
- "What fields are required vs optional?"

**Option template:**
```
Header: Data Model
Question: What structure should [entity] have?

- Minimal: [few fields] - Simple, easy to extend later
- Standard: [common fields] - Covers typical use cases
- Rich: [many fields] - Comprehensive, more upfront work
- None: Use existing patterns from codebase
```

**Example:**
```
Header: Data Model
Question: What should an ExportConfig contain?

- Minimal: format, output_path only - Simple, extend as needed
- Standard: format, output_path, compression, encoding - Covers common needs
- Rich: All above + batch_size, streaming, callbacks, progress - Full control
- None: I'll specify the exact fields needed
```

---

## Constraints

**Purpose:** Identify limitations, requirements, or boundaries that must be respected.

**Question patterns:**
- "What performance requirements apply?"
- "Are there compatibility constraints?"
- "What external factors limit our options?"

**Option template:**
```
Header: Constraints
Question: What constraints should guide this design?

- Performance-first: [speed/efficiency focus] - May sacrifice flexibility
- Compatibility-first: [integration focus] - May sacrifice performance
- Simplicity-first: [minimal complexity] - May sacrifice features
- None: No specific constraints beyond standard practices
```

**Example:**
```
Header: Constraints
Question: What constraints apply to the export feature?

- Memory-limited: Must stream, no full dataset in memory - Handles large files
- Time-limited: Must complete within X seconds - Responsive UX
- Format-locked: Must match existing system's format exactly - Compatibility
- None: Standard performance is acceptable
```

---

## Edge Cases

**Purpose:** Identify unusual scenarios and how to handle them.

**Question patterns:**
- "What happens with [edge case]?"
- "How should we handle [unusual input]?"
- "What if [unexpected condition]?"

**Option template:**
```
Header: Edge Cases
Question: How should [component] handle [edge case]?

- Error: Fail with clear message - Explicit, no hidden behavior
- Fallback: Use default/safe value - Graceful, may mask issues
- Skip: Ignore silently (if safe) - Simplest, may confuse users
- None: Handle like any other case (no special treatment)
```

**Example:**
```
Header: Edge Cases
Question: How should export handle empty datasets?

- Error: Raise "No data to export" - Clear feedback
- Empty file: Create file with headers only - Consistent output
- Skip: Don't create file, log warning - No clutter
- None: I'll specify the exact behavior needed
```

---

## Integration

**Purpose:** Define how the work connects to existing systems.

**Question patterns:**
- "How does this integrate with [existing system]?"
- "What APIs/interfaces are involved?"
- "What dependencies exist?"

**Option template:**
```
Header: Integration
Question: How should [new component] integrate with [existing system]?

- Direct: Tight coupling - Simple, fast, harder to change later
- Adapter: Interface layer - Decoupled, more code
- Event-based: Async communication - Loosely coupled, more complex
- None: Standalone (no integration needed)
```

**Example:**
```
Header: Integration
Question: How should export integrate with the existing data pipeline?

- Direct: Call existing DataFrame methods - Reuse existing code
- Wrapper: New Export class wrapping pipeline - Clean interface
- Plugin: Pluggable exporters loaded dynamically - Extensible
- None: Standalone utility, no pipeline integration
```

---

## Terminology

**Purpose:** Align on naming and concepts for consistency.

**Question patterns:**
- "What should we call [concept]?"
- "How does [term A] differ from [term B]?"
- "Is [term] used consistently across the codebase?"

**Option template:**
```
Header: Terminology
Question: What should we call [concept]?

- [Term A]: Matches [existing usage] - Consistent with codebase
- [Term B]: More precise - Clearer meaning, new convention
- [Term C]: Industry standard - Familiar to newcomers
- None: Use whatever fits naturally
```

**Example:**
```
Header: Terminology
Question: What should we call the output format specification?

- format: Matches pandas/existing code - Consistent
- output_format: More explicit - Clearer in context
- file_type: Industry common - Familiar to users
- None: I'll specify the exact term to use
```

---

## Prioritization Heuristic

When selecting which taxonomy area to ask about next:

**Impact × Uncertainty scoring:**

| Factor | High (3) | Medium (2) | Low (1) |
|--------|----------|------------|---------|
| **Impact** | Affects architecture | Affects implementation | Affects details |
| **Uncertainty** | No information | Partial information | Clear from context |

**Priority order:**
1. High Impact × High Uncertainty (9) → Ask first
2. High Impact × Medium Uncertainty (6) → Ask second
3. Medium Impact × High Uncertainty (6) → Ask second
4. Lower scores → Ask if questions remain

**Stop conditions:**
- All taxonomy areas covered
- User signals "enough clarification"

---

## Re-evaluation Between Batches

After receiving answers, re-evaluate pending questions before the next batch:

**Check for invalidated questions:**
- If answer A makes question B irrelevant, skip B
- Example: If user says "no authentication needed", skip questions about auth flows

**Handle ambiguous "Other" answers:**
- If custom answer spans multiple areas, add follow-up clarification to next batch
- Keep follow-ups focused on the specific ambiguity

**Example re-evaluation:**
```
Batch 1 (Scope): User answers "MVP only - no advanced features"
→ Re-evaluate: Skip questions about advanced feature edge cases
→ Batch 2 (Behavior): Only ask about core behavior, not advanced scenarios
```
