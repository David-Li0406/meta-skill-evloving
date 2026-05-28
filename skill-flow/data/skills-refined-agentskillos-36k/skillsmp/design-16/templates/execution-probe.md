# Execution Probe Template

An Execution Probe is a **deliberate break in the closed reasoning loop**. It tests feasibility in the real environment before full spec investment.

---

## When to Use

| Project Scope | Use Probe? |
|---------------|------------|
| Typo fix, config change | No |
| Bug fix with clear repro | No |
| Single feature, known patterns | Optional |
| New feature, unknown territory | **Yes** |
| New product / major system | **Yes, multiple** |

---

## What a Probe Is

A probe is:
- A **thin vertical slice** of implementation
- **Disposable** — it never ships
- **Reality contact** — touches real codebase, real tools, real APIs
- **Assumption tester** — validates spec assumptions early

A probe is NOT:
- A prototype
- A spike
- A reduced spec
- Something that ships

---

## What a Probe Tests

A probe answers **only these questions**:

1. Can the agent understand our domain language?
2. Does the codebase support the intended change?
3. Are there hidden architectural constraints?
4. Do external tools/APIs behave as assumed?
5. Are there invariant violations we didn't anticipate?

Nothing else. No polish. No completeness.

---

## Probe Scope Rules

**MUST include:**
- One happy path only
- One real file modification
- One real test
- Real tooling (build, lint, test runner)

**MUST ignore:**
- Edge cases
- Error handling completeness
- Visual polish
- Emotional nuance
- Full test coverage
- Performance optimization

**HARD LIMITS:**
- Max 2 hours of agent time
- Max 3 files touched
- Max 1 external integration
- Zero refactoring of existing code

---

# EXECUTION PROBE — {Feature Name}

## Metadata

| Field | Value |
|-------|-------|
| Probe ID | PROBE-{number} |
| Related Spec | S-{number} |
| Related Journey | J-{number} |
| Created | {date} |
| Status | Draft / Running / Complete / Failed |

---

## Goal

Validate feasibility of **{one specific capability}** in the current codebase.

This probe is **successful** if:
- [ ] Agent can implement a minimal version
- [ ] At least one test passes
- [ ] No architectural blockers discovered
- [ ] No invariant violations surfaced

This probe **fails safely** if:
- [ ] Agent halts on ambiguity (expected behavior)
- [ ] Hidden constraints are discovered (valuable signal)
- [ ] Assumptions proven wrong (update spec)

---

## Hypothesis Being Tested

State the specific assumption this probe tests:

> "We assume that {assumption from spec}."

Example:
> "We assume that collection data can be grouped by fabric_type client-side without performance issues."

---

## Scope (Hard Limits)

### Implement ONLY:
- {One specific behavior}
- {One happy path}
- {One test case}

### Ignore ALL:
- Edge cases
- Error states
- Other requirements from spec
- Visual polish
- Performance optimization

### Authorized Files:
```
src/{module}/probe_{feature}.ts
tests/{module}/probe_{feature}.test.ts
```

No other files may be modified.

---

## Instructions for Agent

**DO:**
- Implement the minimum to test the hypothesis
- Write one passing test
- Use existing patterns from codebase
- Stop and report if blocked

**DO NOT:**
- Refactor existing code
- Add abstractions
- Optimize anything
- Touch files outside authorized list
- Invent behavior not in scope

**ON AMBIGUITY:**
- STOP execution
- Report: "PROBE BLOCKED: {specific ambiguity}"
- Do not guess or invent solutions

---

## Validation

```bash
# Must pass
{test command, e.g., pnpm test probe_{feature}}

# Must not break
{existing test command, e.g., pnpm test --existing}

# Must lint clean
{lint command, e.g., pnpm lint src/{module}/probe_*}
```

---

## Success Criteria

| Criterion | Pass/Fail |
|-----------|-----------|
| Agent completed without blocking | |
| Test passes | |
| No unauthorized file access | |
| No existing tests broken | |
| Lint passes | |

---

## Probe Outcome (Fill After Execution)

### Result: {SUCCESS / FAILED / BLOCKED}

### What Actually Happened
```
{Factual description — no interpretation}

- Agent attempted to...
- Test result was...
- Files touched were...
```

### Discoveries

#### Confirmed Assumptions
- {Assumption that held true}

#### Violated Assumptions
- {Assumption that was wrong}
- {Why it was wrong}

#### Hidden Constraints Found
- {Constraint not in spec}
- {Where it came from}

#### Invariant Violations Surfaced
- {Invariant #} — {how it was violated}

---

## Spec Corrections Required

Based on this probe, the following spec changes are needed:

| Spec Section | Current | Should Be |
|--------------|---------|-----------|
| {section} | {current text} | {corrected text} |

---

## Disposition

- [ ] Probe code deleted (required)
- [ ] Spec updated with corrections
- [ ] Invariant violations logged to Spec Delta
- [ ] Ready for full PRP generation

---

## Notes

{Any additional observations, questions for next probe, or patterns discovered}

---

*Probe is disposable. Learning is permanent.*
