# Debugging Plan: {ISSUE_TITLE}

**Generated**: {TIMESTAMP}  
**Issue ID**: {ISSUE_REF}  
**Severity**: {SEVERITY}

## Problem Statement

{One-paragraph description of the observed behaviour, expected behaviour, and impact.}

## Context Summary

| Aspect | Details |
|--------|---------|
| First observed | {datetime or commit} |
| Reproduction rate | {percentage or conditions} |
| Affected components | {list} |
| Recent changes | {relevant deployments/updates} |

### Error Artefacts

```
{Stack trace, error message, or relevant log excerpt}
```

### Information Gaps

{List any context that could not be obtained and may affect hypothesis quality.}

---

## Hypotheses

### H1: {Hypothesis Title}

**Claim**: {Specific falsifiable statement about the root cause.}

**Plausibility**: {High | Medium | Low} — {Brief justification}

**Prediction**: If this hypothesis holds, then {observable consequence}.

#### Falsification Plan

| Step | Action | Expected Negative Result |
|------|--------|--------------------------|
| 1 | {Command or investigation} | {Outcome that would disprove H1} |
| 2 | {Follow-up if step 1 inconclusive} | {Outcome} |

**Tooling**: {Scripts, commands, or instrumentation required}

**Confidence on falsification**: {How decisively does a negative result rule this out?}

---

### H2: {Hypothesis Title}

**Claim**: {Specific falsifiable statement.}

**Plausibility**: {High | Medium | Low} — {Brief justification}

**Prediction**: If this hypothesis holds, then {observable consequence}.

#### Falsification Plan

| Step | Action | Expected Negative Result |
|------|--------|--------------------------|
| 1 | {Command or investigation} | {Outcome that would disprove H2} |

**Tooling**: {Scripts, commands, or instrumentation required}

**Confidence on falsification**: {How decisively does a negative result rule this out?}

---

{Repeat for H3–H5 as warranted. Omit if fewer hypotheses are justified.}

---

## Recommended Execution Order

1. **{Hn}** — {Rationale: cheapest/fastest/most decisive}
2. **{Hm}** — {Rationale}
3. ...

## Termination Criteria

- **Root cause identified**: A hypothesis survives all falsification attempts while others are eliminated.
- **Escalation trigger**: {Condition under which to escalate or revise hypotheses, e.g., all hypotheses falsified.}

## Notes for Executing Agent

{Any additional guidance: environment setup, access requirements, stakeholder contacts, time constraints.}
