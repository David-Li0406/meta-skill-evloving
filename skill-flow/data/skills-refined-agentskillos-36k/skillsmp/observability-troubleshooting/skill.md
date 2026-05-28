---
name: observability-troubleshooting
description: Add or improve observability (logs, metrics, traces, alerts) and troubleshoot production or performance issues. Use when diagnosing incidents, defining SLOs, or instrumenting critical paths.
---

# Name

observability-troubleshooting

---

## When to use

Use this skill when visibility gaps or unclear signals prevent confident diagnosis, including:

* Production incidents or degraded user experience
* Performance issues without a clear root cause
* Hard-to-reproduce bugs or intermittent failures
* Missing, noisy, or misleading logs, metrics, or traces
* Need to define or validate SLOs, alerts, or dashboards
* Instrumenting critical paths before scaling or refactoring

---

## Inputs required

Before proposing any observability or troubleshooting approach, this skill requires:

* Clear description of symptoms and user impact
* Time window and frequency of the issue
* Known critical user flows or business paths
* Existing observability signals (logs, metrics, traces), if any
* Constraints (cost, privacy, PII, data retention)

If any input is missing, **stop and ask the DEV**.

### Mandatory DEV questions

* What is the primary user impact and when does it occur?
* Is this issue reproducible or intermittent?
* What telemetry do we currently have (if any)?
* Which paths or operations are business-critical?
* Are there privacy, compliance, or cost constraints?

---

## Repo Signals (observation)

This section must be completed **before proposing options**.
If any item is `Unknown`, confirm with the DEV.

* **Runtime & stack**: language, framework, execution model
* **Architecture shape**: monolith, services, async boundaries
* **Traffic profile**: volume, burstiness, criticality
* **Current telemetry**: logs, metrics, traces, none, partial
* **Operational maturity**: alerts, on-call, runbooks
* **Failure mode**: deterministic, intermittent, silent

Only record **observable facts** here.
No assumptions, no prescriptions.

---

## Implications (interpretation)

From the observed Repo Signals, derive implications such as:

* Depth of visibility currently available
* Confidence level in existing signals
* Cost of adding or expanding telemetry
* Risk of blind spots during incidents
* Likelihood of performance or cost regressions
* Urgency of restoring observability vs long-term improvement

These implications **frame** the options — they do not decide them.

---

## Process

1. **Validate Repo Signals**
   Ask the DEV:

   > “Can I proceed assuming these repository signals are accurate?”

2. **Clarify the diagnostic goal**
   Incident response, root-cause analysis, baseline visibility, or future-proofing.

3. **Map critical paths and unknowns**
   Identify where visibility is missing or unreliable.

4. **Generate observability options**
   Produce **at least two and preferably three viable options**, strictly derived from:

   * repo maturity
   * system behavior
   * operational constraints

5. **Evaluate options objectively**
   Compare signal quality, cost, operational overhead, and risk.

6. **Formulate a recommendation**
   Recommend one option with explicit, defensible rationale.

7. **Confirm before instrumentation**
   No telemetry changes without DEV approval.

---

## Options & trade-offs

Based on the analysis above, generate **context-specific observability strategies**.

Examples of dimensions to vary (not presets):

* Scope of instrumentation (narrow vs broad)
* Signal types emphasized (logs, metrics, traces)
* Sampling vs full capture
* Build-time vs runtime instrumentation
* Tooling complexity vs signal depth

For **each option**, include:

* **Description**: What would be added or changed
* **Pros**: Concrete benefits (diagnostic power, speed, clarity)
* **Cons**: Concrete drawbacks (cost, noise, complexity)
* **Risk profile**: Likelihood of side effects or blind spots
* **Operational cost**: Infra, ingestion, maintenance
* **Fit to current repo maturity**

Options must be **entirely derived from current context**, never pre-selected.

---

## Recommendation

Select one option as the recommended path.

### Recommendation criteria

The recommendation must explicitly consider:

* Diagnostic confidence gained vs effort required
* Mean time to detect and resolve issues
* Cost and performance impact
* Alignment with repo and team maturity
* Ease of rollback or iteration

### Rationale (required)

Provide a short rationale (3–6 bullets) explaining:

* Why this option best fits the observed context
* Which trade-offs are consciously accepted
* What signals or benchmarks informed the choice
* What follow-up improvements are intentionally deferred

---

## Output format

The response must include:

1. Confirmed Repo Signals
2. Diagnostic goal and impact summary
3. Identified observability gaps
4. Generated options with trade-offs
5. Clear recommendation with rationale
6. Proposed scope of instrumentation
7. Validation and success criteria
8. Open questions for the DEV

---

## Safety checks

* Never log secrets, credentials, or PII
* Avoid high-cardinality labels and unbounded dimensions
* Guard against performance regressions
* Explicitly mark temporary or exploratory instrumentation
* Ensure signals align with real failure modes

---

## Dev confirmation gates

Explicit DEV approval is required before:

* Adding or expanding telemetry
* Introducing observability dependencies or agents
* Defining SLOs or alerts
* Increasing data retention or sampling rates
* Rolling changes into production

Without confirmation, **do not proceed**.
