# Error Handling and Edge Cases

Guidance for handling errors and edge cases during TDD runbook generation.

---

## Input Validation Errors

| Error | Trigger | Action | Example |
|-------|---------|--------|---------|
| **Design not found** | File doesn't exist | List recent designs, suggest /design, STOP | "Design not found at plans/auth/design.md. Recent: plans/reporting/design.md (2h ago). Create with /design first." |
| **Missing TDD sections** | No phases/increments/tests | Report missing sections, offer /plan-adhoc, STOP | "Missing: behavioral increments, test scenarios. Add to design or use /plan-adhoc?" |
| **Unresolved items** | Contains (TBD), (REQUIRES CONFIRMATION) | List all with context/line numbers, STOP | "Found 3 unresolved: Line 45 'OAuth2 or API keys (REQUIRES CONFIRMATION)'. Resolve before proceeding." |

---

## Cycle Generation Errors

| Error | Trigger | Action | Example |
|-------|---------|--------|---------|
| **Empty cycle** | No assertions | Suggest folding into next cycle, warn, ask to skip | "Cycle 2.3 'Set up logging' has no assertions. Fold into 2.4 'Test logging output'? Skip?" |
| **Circular dependency** | A→B→C→A | Report full chain, suggest breaking dependency, STOP | "Cycle detected: 2.1→3.2→4.1→2.1. Remove [DEPENDS: 2.1] from 4.1?" |
| **Invalid cycle ID** | Doesn't match X.Y | Report all invalid, show expected format, STOP | "Invalid: 'Cycle 1' (need X.Y), 'Cycle 2.0.1' (no X.Y.Z), 'Cycle A.1' (numeric only)" |
| **Duplicate IDs** | Same ID used twice | Report locations, STOP | "Cycle 2.2 appears twice: Line 234 'error handling', Line 389 'validation'. Renumber second to 2.3." |
| **Forward dependency** | Depends on future cycle | Report ordering issue, suggest fix, STOP | "Cycle 1.2 [DEPENDS: 2.1] invalid. Options: Renumber 2.1→1.2, remove dependency, or reorder phases." |
| **Complex cycle** | >5 assertions | Warn, suggest split, ask to proceed | "Cycle 3.2 has 7 assertions. Split: 3.2 (1-2), 3.3 (3-4), 3.4 (5-7). Proceed anyway?" |

---

## Integration Errors

| Error | Trigger | Action | Example |
|-------|---------|--------|---------|
| **Cannot write** | Permission/disk issues | Report path/error, check perms/space, suggest alternative, STOP | "Cannot write plans/auth/runbook.md: Permission denied. Check: ls -la plans/auth/" |
| **prepare-runbook.py missing** | Script not found | Report expected path, provide manual guidance, WARNING (proceed) | "WARNING: agent-core/bin/prepare-runbook.py not found. Runbook created but needs manual processing." |
| **Validation failure** | Format invalid after generation | Report issue, show expected vs actual, offer regenerate | "Invalid cycle header. Expected: '## Cycle 1.2' (H2). Actual: '### Cycle 1.2' (H3). Regenerate?" |

---

## Edge Cases

### Single-cycle feature
**Scenario:** Only one increment
**Handling:** Valid. Create Cycle 1.1 only with all standard sections, no dependencies.

### All cycles independent
**Scenario:** No dependencies between any cycles
**Handling:** Valid. Mark metadata as "Parallel", enable parallel execution. Common for regression suites.

### All regressions
**Scenario:** Feature exists, only adding tests
**Handling:** Valid. Mark all `[REGRESSION]`, adjust stop conditions (no RED expected), document in Common Context.

### Missing design decisions
**Scenario:** No "Design Decisions" section
**Handling:** Extract from content, create minimal Common Context, warn, proceed.

### Very large runbook
**Scenario:** >50 cycles
**Handling:** Warn about size/time/complexity, suggest splitting by phase, ask confirmation to proceed.

---

## Recovery Protocols

### Validation failure
1. Report specific issue with expected vs actual format
2. Offer to regenerate section
3. If declined: Save partial as `.draft` extension

**Example:** "Validation failed: Invalid cycle header format. Expected: '## Cycle 1.2'. Actual: '### Cycle 1.2'. Regenerate? (If no: saved to runbook.draft.md)"

### Partial generation
1. Save progress to `.partial.md`
2. Report failed section
3. Provide fix guidance
4. Offer to continue from checkpoint

**Example:** "Failed at Cycle 3.2 GREEN generation. Saved to runbook.partial.md. Cannot infer implementation. Options: 1) Add guidance to design, 2) Skip 3.2, 3) Abort."

### User intervention needed
1. Save state
2. Document issue clearly
3. Provide next action
4. Wait for input

**Example:** "Intervention needed: Cannot determine granularity for 'Implement comprehensive error handling'. Single cycle or one per error type? Design unclear. Clarify to continue."

### Dependency resolution failure
1. Show dependency graph
2. Highlight problem
3. Suggest specific fix
4. Offer auto-resolve if possible

**Example:** "Graph: 1.1→1.2→1.3→2.1→1.2 (CYCLE). Suggested: Remove [DEPENDS: 1.2] from 2.1. Auto-resolve? (yes: 2.1 depends on 1.3 instead)"

### prepare-runbook.py incompatibility
1. Report issue
2. Show problematic section
3. Offer regenerate with fix
4. Provide manual workaround

**Example:** "Compatibility issue: Cycle IDs have non-numeric chars ('Cycle 1.A'). prepare-runbook.py needs numeric only. Regenerate as 1.1? (no: manual processing required)"

---

## Error Handling Principles

**Fail fast:**
- Report exact path/line/context
- Suggest specific fixes
- STOP on fatal errors

**Never suppress:**
- Report all errors explicitly
- Escalate when stuck
- Document unexpected results

**Provide recovery:**
- Save progress on failures
- Offer alternatives
- Enable continuation from checkpoints

---
