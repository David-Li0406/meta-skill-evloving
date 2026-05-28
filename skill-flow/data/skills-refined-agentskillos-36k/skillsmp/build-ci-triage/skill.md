---
name: build-ci-triage
description: Triage build and CI failures with a focus on fixing errors quickly using minimal diffs. Use when the build fails locally or in CI.
---

# Name

build-ci-triage

---

## When to use

Use this skill when build or CI failures block development, including:

- Local build failures (`npm run build`, `pnpm build`, etc.)
- CI job failures (lint, typecheck, test, bundle)
- Dependency, configuration, or environment-related errors
- Regressions introduced by recent changes

---

## Inputs required

Before proposing any fix, this skill requires:

- Full error logs (local and/or CI)
- Command used to trigger the failure
- Execution environment (local, CI, OS, Node/runtime versions)
- Recent relevant changes (code, config, dependencies)

If any input is missing, **stop and ask the DEV**.

### Mandatory DEV questions

- Can you share the full error output?
- Does the failure happen locally, in CI, or both?
- Were there recent dependency or config changes?
- Is restoring the build quickly the top priority?

---

## Repo Signals (observation)

This section must be completed **before proposing fixes**.  
If any item is `Unknown`, confirm with the DEV.

- **Stack**: Detected language, runtime, package manager
- **Build tooling**: Bundler, transpiler, type checker
- **Linting / formatting**: Presence and strictness
- **Testing**: Whether tests run as part of the build
- **CI/CD**: Existence, scope, and enforcement level
- **Failure surface**: Deterministic vs intermittent failures

Only record **observable facts** here.

---

## Implications (interpretation)

From the observed Repo Signals, derive implications such as:

- Urgency to restore developer flow
- Risk of introducing secondary regressions
- Cost of touching build or CI configuration
- Likelihood that the failure is symptomatic vs root-cause

> **Explicit bias of this skill**  
> When build maturity or observability is low, this skill prioritizes **fast recovery and minimal diffs** over structural cleanup.

---

## Process

1. **Validate Repo Signals**  
   Ask the DEV:  
   > “Can I proceed assuming these repository signals are correct?”

2. **Reproduce or isolate the failure**  
   Confirm scope and determinism.  
   Ask:  
   > “Is this reproduction path accurate?”

3. **Identify failure category**  
   Syntax/type error, dependency mismatch, config drift, environment issue, tooling regression.

4. **Generate remediation options**  
   Produce **at least two and preferably three viable options**, derived strictly from the current context.

5. **Evaluate options objectively**  
   Compare time-to-fix, risk, blast radius, and follow-up cost.

6. **Formulate recommendation**  
   Recommend one option with explicit rationale.

7. **Confirm before applying changes**  
   No fixes or config changes without DEV approval.

---

## Options & trade-offs

Based on the current context, generate **contextual remediation strategies**, such as:

- A narrowly scoped fix addressing the immediate failure
- A tooling or configuration adjustment reducing recurrence
- A stabilizing workaround enabling progress while deferring root-cause work

For **each option**, include:

- **Description**: What changes and where
- **Pros**: Concrete benefits (speed, safety, clarity)
- **Cons**: Concrete drawbacks (technical debt, partial fixes)
- **Risk profile**: Likelihood of side effects
- **Operational cost**: CI time, maintenance, coordination
- **Fit to current repo maturity**

Options must be **derived from observed signals**, not pre-defined templates.

---

## Recommendation

Select one option as the recommended path.

### Recommendation criteria

The recommendation must explicitly consider:

- Time to restore a working build
- Risk of introducing new failures
- Cost of rollback if the fix is wrong
- Team velocity and delivery pressure

### Rationale (required)

Provide a short rationale (3–6 bullets) explaining:

- Why this option best fits the current situation
- Which trade-offs are consciously accepted
- What follow-up work should be scheduled later

---

## Output format

The response must include:

1. Confirmed Repo Signals
2. Summary of the failure and suspected root cause
3. Generated remediation options with trade-offs
4. Clear recommendation with rationale
5. Proposed fix scope (files/configs affected)
6. Validation steps (commands to re-run)
7. Open questions for the DEV

---

## Safety checks

- Avoid unrelated refactors while triaging
- Do not mask errors without understanding impact
- Ensure the same command that failed now passes
- Watch for environment-specific fixes leaking into CI
- Flag temporary workarounds explicitly

---

## Dev confirmation gates

Explicit DEV approval is required before:

- Applying any fix beyond minimal scope
- Changing build or CI configuration
- Modifying dependency versions
- Introducing temporary workarounds
- Committing changes related to the failure

Without confirmation, **do not proceed**.
