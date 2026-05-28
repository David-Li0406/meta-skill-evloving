---
name: reliability-resilience
description: Improve reliability via timeouts, retries, circuit breakers, degradation, and fault isolation. Use when failures, timeouts, or dependency flakiness impact users.
---

# Name

reliability-resilience

---

## Purpose

Guide the analysis and improvement of system reliability and resilience **without assuming architecture, tooling, or maturity upfront**.

This skill exists to help identify **where and why systems fail**, understand the **blast radius of failures**, and design **context-appropriate safeguards** that balance user experience, operational cost, and engineering effort.

Use this skill to move from vague reliability concerns (“timeouts”, “flaky deps”, “incidents”) to **explicit, testable resilience strategies** grounded in real constraints.

---

## When to use

Use this skill when:

* Users experience intermittent failures, timeouts, or degraded behavior
* External or internal dependencies are slow, unreliable, or poorly understood
* Failures cascade across services or features
* The system lacks clear reliability targets or guardrails
* There is disagreement about how “resilient enough” the system should be

---

## Inputs required

Before proposing any resilience changes, gather:

* Critical user-facing flows and their failure impact
* Known failure modes (timeouts, errors, saturation, dependency outages)
* Dependency map (services, APIs, queues, caches, third parties)
* Existing timeout, retry, or fallback behavior (if any)
* Availability, latency, or error-rate expectations (formal or informal)
* Operational constraints (cost, complexity, team expertise)

If any of this context is missing, **stop and ask the DEV**.

### Mandatory DEV questions

* Which user-facing flows are most critical to uptime or trust?
* What failures or slowdowns are observed most often?
* Where do failures originate (own code vs dependencies)?
* What level of failure is acceptable before users notice or complain?
* Are there explicit or implicit SLOs today?

---

## Repo Signals (observation)

Capture only **observable facts** from a quick repo scan.
If something is unclear, record it as *Unknown* and confirm with the DEV.

* **Stack**: Languages, runtimes, frameworks
* **Architecture shape**: Monolith, services, background workers, APIs
* **Dependency handling**: Presence of timeouts, retries, queues, async boundaries
* **Error handling**: Centralized vs ad-hoc, typed vs generic
* **Testing maturity**: Coverage of failure scenarios (if any)
* **CI/CD**: Release frequency and rollback capability
* **Observability**: Logs, metrics, traces, alerts (or absence of them)

Do not infer intent. Only record what is visible.

---

## Implications (interpretation)

Based on Repo Signals and inputs, derive implications such as:

* Likely blast radius of a single dependency failure
* Risk of cascading failures under load or partial outages
* Ability (or inability) to detect failures before users do
* Cost of adding resilience vs cost of continued incidents
* Areas where resilience changes could unintentionally harm UX

Explicitly state uncertainties and assumptions.

---

## Process

1. **Validate observations**
   Ask the DEV:

   > “Can I proceed assuming these repository signals are accurate?”

2. **Identify critical paths and failure modes**
   Map where failures hurt users most and why.

3. **Assess current safeguards**
   Determine what protections exist, if any, and where they break down.

4. **Clarify reliability targets**
   Ask:

   > “What level of failure or degradation is acceptable for these paths?”

5. **Generate options from context**
   Produce **at least two and preferably three** viable approaches, grounded entirely in the analysis above.

6. **Evaluate options objectively**
   Compare operational cost, failure containment, UX impact, and long-term scalability.

7. **Recommend and confirm**
   Make a defensible recommendation and request approval before action.

---

## Options & trade-offs

Based on the analysis above, generate **context-specific options**.
Do **not** use predefined templates or patterns by default.

Each option must differ meaningfully in **scope, cost, risk, and resilience strength**.

For **each option**, include:

* **Description**: What protections are added and where
* **Failures addressed**: Which failure modes are mitigated
* **Pros**: Concrete benefits
* **Cons**: Concrete risks or limitations
* **Operational cost**: Complexity, maintenance, and on-call impact
* **UX impact**: How users experience degradation or recovery
* **Preconditions**: Observability, testing, or process requirements

If only two options are viable, explain why a third is not.

---

## Recommendation

Select the option that offers the **best cost–benefit trade-off** given:

* Frequency and severity of failures
* User tolerance for degradation
* Team and repo maturity
* Operational and cognitive load
* Benchmarks from similar systems or past incidents (if available)

### Rationale (required)

Provide a concise rationale (3–6 bullets) explaining:

* Why this option fits the current constraints
* Which trade-offs are consciously accepted
* What risks remain and how they are mitigated
* What should be revisited as the system evolves

Clearly state assumptions if benchmarks or historical data are missing.

---

## Output format

The final response must include:

1. Confirmed Repo Signals
2. Critical paths and failure mode analysis
3. Identified gaps and constraints
4. Generated options with trade-offs
5. Clear recommendation with rationale
6. Rollout, validation, and monitoring plan
7. Open questions for the DEV

---

## Safety checks

* Avoid infinite retries or unbounded backoff
* Prevent cascading failures under partial outages
* Ensure fallbacks do not expose sensitive data
* Validate that resilience mechanisms do not hide critical errors
* Treat early improvements as incremental, not final

---

## Dev confirmation gates

Explicit DEV approval is required before:

* Introducing new resilience mechanisms that affect behavior
* Changing timeout, retry, or degradation semantics
* Adding infrastructure or middleware dependencies
* Accepting user-visible degradation as a strategy

Without confirmation, **do not proceed**.
