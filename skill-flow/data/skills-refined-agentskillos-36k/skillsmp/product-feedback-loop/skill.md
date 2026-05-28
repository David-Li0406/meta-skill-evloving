---
name: product-feedback-loop
description: Product analytics and feedback loop guidance for KPIs, funnels, and experimentation. Use when defining metrics instrumentation, experiments, or indicators of product success.
---

# Name

product-feedback-loop

---

## Purpose

Guide the definition, instrumentation, and validation of product feedback loops
(metrics, funnels, experiments, and signals of success) **without assuming tools,
maturity, or process upfront**.

Use this skill to turn product goals into **observable, decision-grade signals**
while respecting technical, organizational, and privacy constraints.

---

## When to use

Use this skill when:

- Defining success metrics for a new feature, initiative, or experiment
- Instrumenting critical user journeys or conversion funnels
- Investigating why a product outcome is unclear or disputed
- Planning experiments, rollouts, or UX improvements
- Aligning engineering, product, and data on what “success” means

---

## Inputs required

Before proposing any instrumentation or metrics, gather:

- Product or business objective(s) the initiative must influence
- Primary user journeys and key decision points
- Current analytics or telemetry capabilities (if any)
- Privacy, compliance, or consent constraints
- Tolerance for experimentation and iteration speed

If any of this context is missing, **stop and ask the DEV**.

### Mandatory DEV questions

- What outcome must change for this effort to be considered successful?
- Which user journeys or behaviors matter most right now?
- What data do we already collect, if any?
- Are there privacy, consent, or regulatory constraints?
- How quickly do we need feedback to make decisions?

---

## Repo Signals (observation)

Capture only **observable facts** from a quick repo scan.
If anything is unclear, record it as `Unknown` and confirm with the DEV.

- **Stack**: Languages, runtimes, frameworks
- **Client surfaces**: Web, mobile, backend-only, APIs
- **Data collection**: Existing events, logs, metrics, analytics SDKs
- **Experimentation**: Feature flags, A/B infra, config toggles
- **Testing maturity**: Unit, integration, e2e presence
- **CI/CD**: Release cadence and automation
- **Privacy signals**: Consent handling, PII exposure, data retention hints

Do not infer intent. Only record what is visible.

---

## Implications (interpretation)

Based on Repo Signals and inputs, derive implications such as:

- How fast feedback is realistically achievable
- Risk of collecting misleading or low-quality signals
- Operational cost of adding or maintaining instrumentation
- Suitability of experiments vs observational metrics
- Constraints imposed by privacy, testing, or release process

Explicitly state uncertainties and assumptions.

---

## Process

1. **Validate observations**  
   Ask the DEV:  
   > “Can I proceed assuming these repository signals are accurate?”

2. **Clarify goals and decision points**  
   Identify what decisions the metrics must enable.  
   Ask:  
   > “Which decisions should this data support?”

3. **Map critical journeys and signals**  
   Identify where signal loss, ambiguity, or bias may occur.  
   Ask:  
   > “Do these journeys and risks reflect reality?”

4. **Identify gaps and constraints**  
   Technical, organizational, or legal.

5. **Generate options from context**  
   Produce **at least two and preferably three** viable approaches,
   grounded entirely in the analysis above.

6. **Evaluate options objectively**  
   Compare cost, signal quality, latency, risk, and scalability.

7. **Recommend and confirm**  
   Make a defensible recommendation and request approval before action.

---

## Options & trade-offs

Based on the analysis above, generate **context-specific options**.
Do **not** use predefined templates.

Each option must differ meaningfully in **scope, cost, risk, and insight quality**.

For **each option**, include:

- **Description**: What is instrumented and how
- **Insights unlocked**: Decisions this enables
- **Pros**: Concrete advantages
- **Cons**: Concrete limitations or risks
- **Operational cost**: Ongoing maintenance and effort
- **Data quality risk**: Bias, noise, or blind spots
- **Preconditions**: Tests, consent, tooling, process

If only two options are viable, explain why a third is not.

---

## Recommendation

Select the option that offers the **best cost–benefit trade-off** given:

- Speed of feedback required
- Accuracy and actionability of signals
- Team and repo maturity
- Privacy and compliance risk
- Benchmarks from similar systems or past efforts (if available)

### Rationale (required)

Provide a concise rationale (3–6 bullets) explaining:

- Why this option fits the current constraints
- Which trade-offs are consciously accepted
- What risks remain and how they can be mitigated
- What follow-up work should be scheduled later

Clearly state assumptions if benchmarks or historical data are missing.

---

## Output format

The final response must include:

1. Confirmed Repo Signals
2. Goal → KPI → decision mapping
3. Identified gaps and constraints
4. Generated options with trade-offs
5. Clear recommendation with rationale
6. Rollout, validation, and monitoring plan
7. Open questions for the DEV

---

## Safety checks

- Avoid collecting PII or sensitive data without explicit consent
- Prevent event duplication or unstable naming
- Validate data freshness before acting on metrics
- Guard against over-instrumentation that slows delivery
- Treat early data as directional, not definitive

---

## Dev confirmation gates

Explicit DEV approval is required before:

- Introducing new analytics or experimentation tooling
- Defining KPIs used for performance or roadmap decisions
- Collecting user-identifiable or regulated data
- Publishing dashboards or alerts as “official”

Without confirmation, **do not proceed**.
