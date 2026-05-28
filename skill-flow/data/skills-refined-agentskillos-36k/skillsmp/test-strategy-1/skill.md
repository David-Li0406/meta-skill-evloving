---
name: test-strategy
description: Define a testing strategy (unit, integration, end-to-end) based on repository risk and maturity. Use it when test coverage is lacking or when planning new features.
---

# Name

test-strategy

---

## Purpose

Guide the definition, prioritization, and evolution of a **test strategy grounded in observed risk, system behavior, and repository maturity** — **without assuming tooling, coverage targets, or testing pyramids upfront**.

This skill exists to help teams move from *uncertain quality* to *defensible confidence*, producing a test approach that is:

- Technically justifiable
- Adaptable to immature and mature repositories
- Compatible with Codex, Copilot, and human review
- Explicit about trade-offs, blind spots, and cost

---

## When to use

Use this skill when:

- A repository has little or no test coverage
- Coverage exists but confidence in changes is still low
- Planning a large refactor, migration, or risky feature
- Tests exist but are slow, flaky, or misaligned with risk
- Engineering velocity is constrained by fear of regressions
- Teams disagree on *what* should be tested and *why*

---

## Inputs required

Before proposing any test strategy, gather:

- Critical user-facing and system-facing behaviors
- Areas where failures would be most costly (business, data, trust)
- Current test presence (if any) and how it is used
- Release cadence and rollback tolerance
- Team capacity and appetite for test investment
- Constraints imposed by CI, infra, or runtime environments

If any of this context is missing, **stop and ask the DEV**.

### Mandatory DEV questions

- Which failures would be most damaging if they reached production?
- Where do regressions historically occur (if known)?
- How often do we release, and how quickly can we roll back?
- What currently gives us confidence when changing code?
- What is the acceptable cost (time/complexity) of testing right now?

---

## Repo Signals (observation)

Capture only **observable facts** from a lightweight repo scan.  
If unclear, mark as `Unknown` and confirm with the DEV.

- **Stack**: Languages, runtimes, frameworks
- **System shape**: Monolith, services, libraries, clients
- **Test presence**: Unit, integration, e2e (or none)
- **Test execution**: Local-only, CI, blocking vs advisory
- **Release mechanics**: Manual, automated, staged
- **Change surface**: Frequency and size of diffs
- **Historical signals**: Test failures, flaky behavior, skipped suites

Do **not** infer intent or maturity. Only record what is visible.

---

## Implications (interpretation)

From Repo Signals and inputs, derive implications such as:

- Where tests would reduce real risk vs add noise
- Which parts of the system are hardest to reason about
- Whether fast feedback or deep coverage matters more right now
- The realistic ceiling for test investment at this stage
- How much confidence can be achieved per unit of effort

Explicitly state:

- Assumptions
- Uncertainties
- Known blind spots

---

## Process

1. **Validate observations**  
   Ask the DEV:  
   > “Can I proceed assuming these repository signals are accurate?”

2. **Identify risk-bearing behaviors**  
   Focus on *what must not break*, not abstractions.

3. **Map behaviors to confidence gaps**  
   Ask:  
   > “Where do we currently rely on hope instead of evidence?”

4. **Assess constraints**  
   Technical, organizational, and temporal.

5. **Generate options from context**  
   Produce **at least two and preferably three** viable strategies, derived entirely from the analysis above.

6. **Evaluate options objectively**  
   Compare cost, confidence gained, feedback latency, and long-term maintainability.

7. **Recommend and confirm**  
   Make a defensible recommendation and request approval before execution.

---

## Options & trade-offs

Based on the analysis above, generate **context-specific options**.  
Do **not** use predefined templates or pyramids.

Each option must differ meaningfully in **scope, cost, risk, and confidence profile**.

For **each option**, include:

- **Description**: What is tested, at which boundaries, and why
- **Confidence gained**: What failures this would reliably catch
- **Pros**: Concrete advantages
- **Cons**: Concrete limitations or risks
- **Operational cost**: Writing, maintaining, and running tests
- **Feedback speed**: How quickly failures surface
- **Failure blind spots**: What this option does *not* protect against
- **Preconditions**: Tooling, CI support, refactors, or process changes required

If only two options are viable, explicitly explain why a third is not.

---

## Recommendation

Select the option with the **best cost–confidence trade-off** given:

- Risk profile of the system
- Expected change frequency
- Team capacity and experience
- CI and release constraints
- Benchmarks from similar systems or prior efforts (if available)

### Rationale (required)

Provide a concise rationale (3–6 bullets) covering:

- Why this option fits current constraints
- Which trade-offs are intentionally accepted
- Which risks remain and why they are acceptable
- How this strategy can evolve over time
- What evidence would justify revisiting the decision

State assumptions clearly if benchmarks or historical data are missing.

---

## Output format

The final response must include:

1. Confirmed Repo Signals  
2. Risk-bearing behaviors and failure modes  
3. Identified confidence gaps and constraints  
4. Generated options with explicit trade-offs  
5. Clear recommendation with rationale  
6. Execution, validation, and evolution plan  
7. Open questions for the DEV  

---

## Safety checks

- Do not over-test low-risk or volatile code paths
- Avoid brittle tests coupled to implementation details
- Treat early coverage as directional, not absolute
- Guard against slow or flaky suites blocking delivery
- Ensure tests increase confidence, not ceremony

---

## Dev confirmation gates

Explicit DEV approval is required before:

- Introducing new test tooling or frameworks
- Making tests blocking in CI
- Refactoring code solely to enable testing
- Enforcing coverage thresholds or quality gates

Without confirmation, **do not proceed**.
