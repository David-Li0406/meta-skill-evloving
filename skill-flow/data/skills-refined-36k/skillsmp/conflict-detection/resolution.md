# Conflict Resolution Strategies

## Resolution Framework

### Step 1: Present the Conflict Clearly

```markdown
**Conflict Detected**

I've noticed a conflict between two things we've discussed:

**Item A**: [Clear description with source reference]
**Item B**: [Clear description with source reference]

**Why they conflict**:
[Plain language explanation of incompatibility]

This needs to be resolved before we can continue.
```

### Step 2: Offer Resolution Options

Always present at least 3 options with clear implications:

```markdown
**How would you like to resolve this?**

1. **Keep A, drop B**
   - [What A provides]
   - [What we lose by dropping B]

2. **Keep B, drop A**
   - [What B provides]
   - [What we lose by dropping A]

3. **Modify to make compatible**
   - [Possible modification]
   - [Trade-off involved]

4. **Accept both with trade-off**
   - [What we gain]
   - [What we sacrifice]

5. **Defer this decision**
   - [What can proceed without resolution]
   - [What gets blocked]
```

### Step 3: Record Resolution

```markdown
**Resolution recorded**

Choice: [User's selection]
Rationale: [User's reasoning or inferred reason]
Impact: [What changes as a result]

[Any follow-up actions needed]
```

---

## Resolution Strategies by Conflict Type

### Requirement vs Requirement

**Strategy: Priority-Based Resolution**

1. Identify which requirement aligns more closely with core goals
2. Consider user personas - who benefits from each?
3. Evaluate implementation complexity difference
4. Present priority-based options

**Example Resolution**:
```markdown
Conflict: Real-time sync vs Offline mode

Options:
1. Real-time primary, limited offline (cached reads only)
2. Offline primary, eventual sync when connected
3. User chooses mode in settings
4. Offline for reads, real-time for writes when connected
```

---

### Decision vs Decision

**Strategy: Timeline-Based Resolution**

1. Identify which decision came first
2. Understand what changed between decisions
3. Determine if new information invalidates old decision
4. Present options acknowledging context change

**Example Resolution**:
```markdown
Conflict: "No database" vs "Need PostgreSQL"

Context: Original decision was for prototype, scope expanded.

Options:
1. Stay with original scope, no database
2. Accept scope change, add PostgreSQL
3. Compromise: Use SQLite for simpler persistence
4. Defer database decision to Phase 2
```

---

### New vs Existing Plan

**Strategy: Dependency-Based Resolution**

1. Map task dependencies
2. Identify which tasks are affected
3. Determine if reordering resolves conflict
4. Consider if tasks can be merged or split

**Example Resolution**:
```markdown
Conflict: New TASK-010 modifies UserService,
         pending TASK-005 also modifies UserService

Options:
1. Complete TASK-005 first, then create TASK-010
2. Merge both changes into single task
3. Split TASK-005 into smaller pieces, interleave
4. Redesign TASK-010 to work with current UserService
```

---

### Scope vs Timeline

**Strategy: MoSCoW Prioritization**

1. Categorize features: Must/Should/Could/Won't
2. Calculate rough effort for each
3. Fit Must-haves within timeline
4. Present trade-off options

**Example Resolution**:
```markdown
Conflict: 15 features requested, 2-week timeline

Analysis:
- Must-have: 5 features (~8 days)
- Should-have: 5 features (~6 days)
- Could-have: 3 features (~4 days)
- Won't-have: 2 features (cut)

Options:
1. Must-haves only (2 weeks)
2. Must + some Should (3 weeks)
3. All except Won't (4+ weeks)
4. Split into phases
```

---

### Tech vs Requirement

**Strategy: Alternative-Finding Resolution**

1. Confirm requirement is truly needed
2. Research alternative technologies
3. Consider requirement modification
4. Present tech or requirement changes

**Example Resolution**:
```markdown
Conflict: Chosen ORM doesn't support required query type

Options:
1. Switch to different ORM
2. Use raw SQL for this query only
3. Modify requirement to fit ORM capabilities
4. Build custom query builder extension
```

---

## Resolution Patterns

### The Priority Ladder

When multiple items conflict, establish priority:

```markdown
Priority Order (established):
1. Security requirements
2. Core functionality
3. User experience
4. Performance
5. Maintainability
6. Nice-to-haves

Conflict between UX and Performance:
→ Performance wins (priority 4 > priority 3)
→ Unless user explicitly overrides
```

### The Scope Fence

Draw clear boundaries:

```markdown
In Scope (agreed):
- Feature A
- Feature B (modified from original)

Out of Scope (moved):
- Feature C (conflicts with timeline)
- Feature D (conflicts with tech choice)

Future Consideration:
- Feature E (deferred)
```

### The Trade-off Table

Document what's gained vs lost:

```markdown
| Keeping | Gains | Loses |
|---------|-------|-------|
| Option A | [benefits] | [costs] |
| Option B | [benefits] | [costs] |
| Compromise | [benefits] | [costs] |

User chose: [Option]
Rationale: [Why acceptable]
```

---

## Conflict Prevention

### During DISCUSS Phase

- Ask clarifying questions early
- Validate understanding before recording decisions
- Explicitly check for conflicts with prior decisions
- Use trade-off questions to surface priorities

### During PLAN Phase

- Cross-reference all requirements before task creation
- Check file modifications don't overlap
- Verify dependency graph has no cycles
- Validate tech choices support all planned tasks

### During EXECUTE Phase

- Re-validate before starting each task
- Check for state drift from original plan
- Pause if new information suggests conflict
- Don't proceed on assumptions

---

## Conflict Escalation

### When Resolution Fails

If user cannot decide or resolution is unclear:

```markdown
**Unable to resolve conflict**

We've been unable to resolve this conflict. Options:

1. **Pause workflow** - Stop here and revisit later
2. **Partial proceed** - Continue with non-conflicting work
3. **External input** - Bring in additional stakeholder
4. **Time-box** - Make decision by [date] or use default
```

### Default Resolution Rules

If forced to proceed without resolution:

1. Choose the safer option (less risk)
2. Choose the simpler option (less complexity)
3. Choose the reversible option (easier to undo)
4. Document that default was used

---

## Resolution Anti-Patterns

### The Wishful Merge
```markdown
BAD: "Let's just do both and figure it out later"
WHY: Defers conflict, doesn't resolve it
```

### The Silent Override
```markdown
BAD: Changing earlier decision without discussion
WHY: Loses traceability, may surprise user
```

### The Scope Creep Acceptance
```markdown
BAD: "Sure, we can add that too"
WHY: Accumulates conflicts, timeline explodes
```

### The Vague Compromise
```markdown
BAD: "We'll find a middle ground"
WHY: Not actionable, conflict persists
```
