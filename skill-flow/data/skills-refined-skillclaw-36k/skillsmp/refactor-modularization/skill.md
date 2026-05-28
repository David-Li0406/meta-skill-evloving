---
name: refactor-modularization
description: Refactoring and safe modularization to reduce coupling, duplication, and complexity. Use when there is large code, cross-dependencies, or a need to extract modules.
---

# Name

refactor-modularization

---

## Purpose

Guide safe and incremental refactoring and modularization efforts **without assuming
architecture, maturity, or target structure upfront**.

Use this skill to reduce coupling, duplication, and cognitive load while **preserving
behavior**, enabling future evolution, and respecting the current constraints of the
repository and team.

This skill prioritizes **evidence-driven decisions**, not idealized architectures.

---

## When to use

Use this skill when:

* Codebases show growing complexity or unclear boundaries
* Files or modules have multiple responsibilities
* Logic is duplicated across components or layers
* Dependencies are tangled or implicitly coupled
* The team wants to refactor safely without destabilizing delivery
* Architectural improvements are desired but constraints are unclear

---

## Inputs required

Before proposing any refactor or modularization, gather:

* Primary motivation (maintainability, velocity, risk reduction, scalability)
* Areas of the code perceived as problematic or fragile
* Behaviors that **must not change**
* Acceptable risk level and delivery constraints
* Availability (or absence) of tests
* Expected lifetime of the system or feature

If any of this context is missing, **stop and ask the DEV**.

### Mandatory DEV questions

* What problem are we trying to solve with this refactor?
* Which behaviors are critical and must remain unchanged?
* Where is change currently risky or slow?
* How much disruption is acceptable in the short term?
* Can we add tests, even temporary ones, if needed?

---

## Repo Signals (observation)

Capture only **observable facts** from a quick repo scan.
If something is unclear, record it as `Unknown` and confirm with the DEV.

* **Stack**: Languages, runtimes, frameworks
* **Structure**: Folder layout, module boundaries, file sizes
* **Coupling signals**: Circular imports, shared globals, cross-layer dependencies
* **Duplication**: Repeated logic or patterns across files
* **Testing maturity**: Unit, integration, characterization tests
* **CI/CD**: Presence of automated validation
* **Change patterns**: Large diffs, frequent hotfixes, fragile areas

Do not infer intent. Only record what is visible.

---

## Implications (interpretation)

Based on Repo Signals and inputs, derive implications such as:

* How risky structural changes are in this repo
* Whether refactoring must be defensive and incremental
* Where boundaries are unclear vs. merely undocumented
* How much confidence tests (or lack thereof) provide
* Whether modularization should precede or follow cleanup

Explicitly state uncertainties and assumptions.

---

## Process

1. **Validate observations**
   Ask the DEV:

   > “Can I proceed assuming these repository signals are accurate?”

2. **Clarify goals and non-goals**
   Identify what success looks like — and what is out of scope.
   Ask:

   > “What should *not* change as a result of this refactor?”

3. **Identify hotspots**
   Locate areas of high churn, complexity, or duplication.
   Ask:

   > “Do these hotspots match your experience?”

4. **Establish invariants**
   Define stable inputs, outputs, and behaviors.

5. **Generate options from context**
   Produce **at least two and preferably three** viable approaches,
   derived entirely from the analysis above.

6. **Evaluate options objectively**
   Compare risk, scope, effort, reversibility, and long-term impact.

7. **Recommend and confirm**
   Make a defensible recommendation and request approval before changes.

---

## Options & trade-offs

Based on the analysis above, generate **context-specific options**.
Do **not** use predefined refactoring templates.

Each option must differ meaningfully in **scope, risk, effort, and reversibility**.

For **each option**, include:

* **Description**: What changes structurally and what stays the same
* **Problems addressed**: Which pains this option reduces
* **Pros**: Concrete benefits
* **Cons**: Concrete risks or limitations
* **Change surface**: Size and spread of diffs
* **Reversibility**: Ease of rollback
* **Preconditions**: Tests, documentation, alignment needed

If only two options are viable, explain why a third is not.

---

## Recommendation

Select the option that offers the **best cost–benefit trade-off** given:

* Current repo and test maturity
* Risk tolerance and delivery pressure
* Expected lifetime of the system
* Team familiarity with the codebase
* Benchmarks from similar refactors (if available)

### Rationale (required)

Provide a concise rationale (3–6 bullets) explaining:

* Why this option fits current constraints
* Which trade-offs are intentionally accepted
* What risks remain and how they are mitigated
* What follow-up refactors may be needed later

Clearly state assumptions if benchmarks or historical data are missing.

---

## Output format

The final response must include:

1. Confirmed Repo Signals
2. Identified hotspots and invariants
3. Key constraints and uncertainties
4. Generated refactoring options with trade-offs
5. Clear recommendation with rationale
6. Incremental execution and validation plan
7. Open questions for the DEV

---

## Safety checks

* Do not change behavior without validation
* Avoid large renames or cosmetic churn
* Keep diffs reviewable and incremental
* Preserve public APIs or version changes explicitly
* Prefer reversible steps over “big rewrites”

---

## Dev confirmation gates

Explicit DEV approval is required before:

* Large structural moves or module extraction
* Introducing new public boundaries or APIs
* Removing or consolidating existing modules
* Refactors that span multiple subsystems

Without confirmation, **do not proceed**.
