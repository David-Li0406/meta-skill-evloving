---
name: dependency-upgrades
description: Dependency management and upgrades with a focus on risk, compatibility, and verification. Use when updating packages, fixing CVEs, or reducing technical debt.

---

# Skill: Build & CI Triage

## Purpose

Analyze and resolve build and CI failures by **diagnosing the root cause**, **deriving context-specific remediation options**, and **recommending a fix based on risk, cost, and impact**.

This skill must not assume that the fastest fix is always the best fix.  
All remediation strategies must be derived from the current repository context and validated with the DEV before execution.

---

## When to Use

- Local build failures (`npm run build`, `pnpm build`, etc.)
- CI job failures (lint, typecheck, tests, bundling)
- Dependency, configuration, or environment-related errors
- Regressions introduced by recent changes
- Flaky or intermittent CI behavior blocking progress

---

## Inputs Required

Before proposing any fix, collect and confirm:

- Full error logs (local and/or CI)
- Command(s) used to trigger the failure
- Execution environment details (local vs CI, OS, Node/runtime versions)
- Recent relevant changes (code, config, dependencies)

If any required input is missing, **stop and ask the DEV**.

### Mandatory DEV Questions

- Can you share the full error output?
- Does the failure occur locally, in CI, or both?
- Were there recent changes to dependencies, tooling, or configuration?
- Is restoring the build quickly more important than addressing root causes?

---

## Repo Signals (Observation Only)

This section must be completed **before proposing any remediation**.  
Only record **observable facts**. If anything is unclear, confirm with the DEV.

- **Stack**: Language(s), runtime(s), package manager
- **Build tooling**: Bundler, transpiler, type checker
- **Linting / formatting**: Presence, strictness, blocking behavior
- **Testing**: Whether tests are part of the build or CI
- **CI/CD**: Existence, scope, enforcement level
- **Failure behavior**: Deterministic vs intermittent
- **Recent churn**: Frequency of build-related changes

---

## Implications (Derived)

From the observed Repo Signals, derive implications such as:

- Urgency to restore developer workflow
- Risk of introducing secondary regressions
- Cost of modifying build or CI configuration
- Likelihood that the failure is a symptom vs a root cause
- Suitability of short-term vs structural fixes

Explicitly state assumptions and confirm them with the DEV if needed.

---

## Process

1. **Validate Repo Signals**  
   Ask the DEV:  
   > “Can I proceed assuming these repository signals are accurate?”

2. **Reproduce or Isolate the Failure**  
   Confirm scope, determinism, and reproduction path.  
   Ask:  
   > “Is this reproduction path correct?”

3. **Classify the Failure**  
   Examples: syntax/type error, dependency mismatch, config drift, environment issue, tooling regression.

4. **Derive Remediation Options**  
   Generate **at least two and preferably three viable options**, strictly derived from:
   - Repo Signals
   - Failure characteristics
   - Team constraints

5. **Evaluate Trade-offs**  
   Compare options objectively based on risk, effort, blast radius, and follow-up cost.

6. **Formulate a Recommendation**  
   Recommend one option with explicit rationale.

7. **Confirm Before Any Change**  
   No fixes, config changes, or dependency updates without DEV approval.

---

## Options & Trade-offs (Context-Derived)

This section must be generated **after analysis**, not pre-filled.

For each option, include:

- **Description**: What changes and where
- **Pros**: Concrete benefits (speed, safety, clarity)
- **Cons**: Concrete drawbacks (technical debt, partial fixes)
- **Risk Profile**: Likelihood and impact of side effects
- **Operational Cost**: CI time, coordination, maintenance
- **Fit to Current Repo Maturity**

Options must be **direct consequences of observed signals**, not generic templates.

---

## Recommendation

Select **one** option as the recommended path.

### Recommendation Criteria

The recommendation must explicitly consider:

- Time to restore a working build
- Risk of introducing new failures
- Cost and feasibility of rollback
- Current repository maturity
- Team velocity and delivery pressure

### Rationale (Required)

Provide a concise rationale explaining:

- Why this option best fits the current context
- Which trade-offs are consciously accepted
- What follow-up work should be scheduled later (if any)

---

## Output Format

The response must include:

1. Confirmed Repo Signals
2. Summary of the failure and suspected root cause
3. Context-derived remediation options with trade-offs
4. Clear recommendation with rationale
5. Proposed fix scope (files/configs affected)
6. Validation steps (commands to re-run)
7. Open questions for the DEV

---

## Safety Checks

- Avoid unrelated refactors during triage
- Do not mask errors without understanding impact
- Ensure the same failing command now passes
- Avoid environment-specific fixes leaking into CI
- Clearly flag temporary workarounds

---

## Dev Confirmation Gates

Explicit DEV approval is required before:

- Applying fixes beyond minimal scope
- Changing build or CI configuration
- Modifying dependency versions
- Introducing temporary workarounds
- Committing changes related to the failure

Without confirmation, **do not proceed**.
