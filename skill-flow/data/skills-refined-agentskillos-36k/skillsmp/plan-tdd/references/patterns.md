# TDD Runbook Patterns

Guidance for decomposing features into atomic TDD cycles with proper granularity, numbering, and dependencies.

---

## Granularity Criteria

**Each cycle should have:**
- 1-3 assertions (focused verification)
- Clear RED failure expectation
- Minimal GREEN implementation
- Independent verification

**Too granular (avoid):** Single trivial assertion, setup-only, <30 seconds to implement

**Too coarse (split):** >5 assertions, multiple distinct behaviors, complex setup + verification, spans multiple modules

**Example - Just Right:**
```
Cycle 2.1: Test -rp flag shows passed tests
- Single assertion: "## Passes" section exists
```

**Example - Too Coarse:**
```
Cycle 2.1: Implement complete pass reporting
- Passes section exists + format correct + verbose mode + quiet mode
→ Split into 4 cycles
```

---

## Numbering Scheme

**Format: X.Y**
- **X (Phase):** Logical grouping (Core, Error handling, Edge cases, Integration)
- **Y (Increment):** Sequential within phase, starts at 1

**Rules:**
- Start at 1.1 (not 0.1 or 1.0)
- Sequential within phase (1.1 → 1.2 → 1.3)
- Gaps acceptable but discouraged
- No duplicates (error)

**Example:**
```
Phase 1: Separate Errors
  1.1: Add setup error fixture
  1.2: Test errors in separate section
  1.3: Test default mode shows both

Phase 2: Pass Reporting
  2.1: Test -rp flag shows passes
  2.2: Test verbose mode shows passes
```

---

## Dependency Management

| Type | Marker | Usage |
|------|--------|-------|
| **Sequential (default)** | None | Within same phase: 1.1 → 1.2 → 1.3 |
| **Cross-phase** | `[DEPENDS: X.Y]` | Requires cycle from different phase |
| **Regression** | `[REGRESSION]` | Testing existing behavior, no RED expected |

**Invalid:** Circular (A→B→C→A), forward (2.1 depends on 3.1 without explicit marker), self-dependencies

**Validation:** All references exist, topological sort succeeds

---

## Stop Conditions

**Standard template (all cycles):**
```markdown
**STOP IMMEDIATELY if:**
- Test passes on first run (expected RED failure)
- Failure message doesn't match expected
- Partial implementation passes
- Regression detected

**Actions:**
1. Document in cycle notes
2. Investigate unexpected results
3. Mark [REGRESSION] if already implemented, or fix test
4. Escalate regression failures
```

**Custom conditions:** Add for external dependencies, performance requirements, security concerns, complex setup/teardown

---

## Common Patterns

| Pattern | Structure | Example |
|---------|-----------|---------|
| **CRUD** | 1 cycle per operation | 1.1: Create, 1.2: Read, 1.3: Update, 1.4: Delete |
| **Feature flag** | 1 per mode + default | 2.1: -rp (enable), 2.2: default, 2.3: -rN (disable) |
| **Authentication** | Happy path + errors | 3.1: Success, 3.2: Invalid creds, 3.3: Expired token, 3.4: Missing creds |
| **External service** | Connection + operations | 4.1: Connect, 4.2: Retrieve, 4.3: Submit, 4.4: Retry |
| **Edge cases** | 1 per boundary | 5.1: Empty, 5.2: Max length, 5.3: Special chars, 5.4: Null |
| **Refactoring** | Regression + refactor | 6.1: Regression tests [REGRESSION], 6.2: Refactor (tests pass) |
| **Multi-step setup** | Setup + incremental | 7.1: Fixture (setup), 7.2: Core test, 7.3: Edge case |
| **Composite** | Components + integration | 8.1: Component A, 8.2: Component B, 8.3: A+B [DEPENDS: 8.1,8.2] |

**Note:** Minimize setup-only cycles. Prefer folding setup into first test cycle.

---

## Granularity Decision Tree

```
Does increment have testable behavior?
├─ No → Fold into next increment or skip
└─ Yes
    ├─ Assertions?
    │   ├─ 1-3 → Good cycle
    │   ├─ 4-5 → Acceptable, consider splitting
    │   └─ >5 → Split into multiple cycles
    └─ Implementation complexity?
        ├─ Single function → Good cycle
        ├─ Multiple files → Consider splitting
        └─ Multiple modules → Definitely split
```

---

## Cycle Breakdown Algorithm

1. **Identify phases** (major feature groupings)
2. **Identify increments** per phase (behavioral changes)
3. **Number cycles** (X.Y format)
4. **For each cycle:**
   - Define RED (what to test, expected failure)
   - Define GREEN (minimal implementation)
   - Assign dependencies (default: sequential within phase)
   - Generate stop conditions (standard + custom if needed)
5. **Validate:**
   - Granularity (1-3 assertions ideal)
   - Dependencies (no cycles, valid references)
   - RED/GREEN completeness

---
