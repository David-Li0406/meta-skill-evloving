---
name: release-management
description: Manage releases, deployments, and rollback strategy with clear versioning and environment policy. Use when planning or executing a release, or setting deployment workflow.
---

# Name

release-management

---

## Purpose

Guide the planning, execution, and validation of software releases **without assuming process maturity, tooling, or organizational structure upfront**.

This skill exists to turn code changes into **controlled, observable, and reversible releases**, balancing speed, safety, and operational cost based on the **actual state of the repository and team**, not on predefined release models.

---

## When to use

Use this skill when:

* Preparing to ship a new feature, fix, or refactor to users or production
* Coordinating multiple changes into a single release window
* Recovering from release-related incidents or regressions
* Introducing or revisiting release practices (tags, versions, rollouts, gates)
* Aligning engineering, product, and operations on “what it means to ship”

---

## Inputs required

Before proposing any release strategy or mechanics, gather:

* Scope and impact of the changes being released
* Target environments (staging, production, customers, regions)
* Risk tolerance for regressions or downtime
* Current validation signals (tests, monitoring, manual checks)
* Constraints on timing, coordination, or approvals

If any of this context is missing, **stop and ask the DEV**.

### Mandatory DEV questions

* What is the user or business impact of this release if it fails?
* Is this release reversible, and how quickly?
* Are releases frequent, rare, or irregular today?
* Who needs confidence before this goes live?
* Is there any external dependency on timing or versioning?

---

## Repo Signals (observation)

Capture only **observable facts** from a quick repo scan.
If anything is unclear, record it as `Unknown` and confirm with the DEV.

* **Stack**: Languages, runtimes, frameworks
* **Deployment surface**: Backend, frontend, mobile, libraries, APIs
* **Versioning signals**: Tags, changelogs, semantic versions, package metadata
* **Testing maturity**: Unit, integration, e2e presence
* **CI/CD**: Pipelines, gates, manual vs automated steps
* **Observability**: Logs, metrics, alerts relevant to releases
* **Rollback hints**: Feature flags, config toggles, migrations

Do not infer intent. Only record what is visible.

---

## Implications (interpretation)

Based on Repo Signals and inputs, derive implications such as:

* How risky releases are in practice, not in theory
* Whether failures are detectable quickly or silently
* How expensive rollback or hotfixes would be
* Whether coordination cost dominates technical risk
* Where human judgment is unavoidable

Explicitly state assumptions and uncertainty.

---

## Process

1. **Validate observations**
   Ask the DEV:

   > “Can I proceed assuming these repository signals are accurate?”

2. **Clarify release goals**
   Identify what the release must optimize for (speed, safety, coordination).
   Ask:

   > “What does a *successful* release look like here?”

3. **Map failure modes**
   Identify where releases historically fail or create stress.
   Ask:

   > “Are these the real failure points?”

4. **Identify constraints**
   Technical, organizational, or timing-related.

5. **Generate options from context**
   Produce **at least two and preferably three** viable release approaches, grounded entirely in the analysis above.

6. **Evaluate options objectively**
   Compare cost, confidence, recovery speed, and scalability.

7. **Recommend and confirm**
   Make a defensible recommendation and request approval before execution.

---

## Options & trade-offs

Based on the analysis above, generate **context-specific options**.
Do **not** use predefined release templates.

Each option must differ meaningfully in **scope, coordination cost, risk exposure, and recovery strategy**.

For **each option**, include:

* **Description**: How the release is executed and controlled
* **Confidence signals**: What validates correctness
* **Pros**: Concrete advantages
* **Cons**: Concrete limitations or risks
* **Operational cost**: Human and system effort per release
* **Failure handling**: Detection and rollback characteristics
* **Preconditions**: Tests, tooling, approvals, or discipline required

If only two options are viable, explain why a third is not.

---

## Recommendation

Select the option that offers the **best cost–benefit trade-off** given:

* Release frequency and urgency
* Risk of user-visible failure
* Team and repo maturity
* Observability and rollback capability
* Benchmarks from similar systems or past releases (if available)

### Rationale (required)

Provide a concise rationale (3–6 bullets) explaining:

* Why this option fits the current constraints
* Which trade-offs are consciously accepted
* What risks remain and how they are mitigated
* What should evolve as the system matures

State assumptions clearly if benchmarks or history are missing.

---

## Output format

The final response must include:

1. Confirmed Repo Signals
2. Release goals and constraints
3. Identified risks and failure modes
4. Generated options with trade-offs
5. Clear recommendation with rationale
6. Release execution, validation, and rollback plan
7. Open questions for the DEV

---

## Safety checks

* Avoid irreversible releases without rollback paths
* Do not rely on manual steps without explicit ownership
* Ensure failure is observable before users report it
* Prevent version drift between environments
* Treat first-time releases as higher risk by default

---

## Dev confirmation gates

Explicit DEV approval is required before:

* Changing release mechanics or cadence
* Introducing new versioning or tagging schemes
* Shipping changes that are hard to roll back
* Declaring a release process “standard” or “enforced”

Without confirmation, **do not proceed**.
