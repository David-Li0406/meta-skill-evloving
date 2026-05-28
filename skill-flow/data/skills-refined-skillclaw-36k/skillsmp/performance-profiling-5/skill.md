---
name: performance-profiling
description: Performance analysis and profiling focused on bottlenecks, latency, and resource usage. Use when there is slowness, high resource consumption, or unmet performance targets.

---

# Name

performance-profiling

---

## When to use

Use this skill when performance characteristics are unclear, degraded, or strategically important, including:

- User-perceived slowness or timeouts
- Latency, throughput, or resource targets not being met
- High CPU, memory, or I/O usage
- Suspected performance regressions
- Before attempting optimizations based on intuition
- When planning scalability or cost optimizations

---

## Inputs required

Before proposing any profiling or optimization approach, this skill requires:

- Target performance goals (latency, throughput, cost, resource usage)
- Environment where performance should be measured (local, staging, prod)
- Expected load profile (steady, bursty, peak)
- Known critical paths or user journeys
- Existing metrics, logs, or traces (if any)

If any input is missing, **stop and ask the DEV**.

### Mandatory DEV questions

- What performance target is currently failing (and how)?
- In which environment should measurements be trusted?
- Under what load does the issue appear?
- Are there existing metrics or traces we can rely on?
- Is temporary instrumentation acceptable?

---

## Repo Signals (observation)

This section must be completed **before proposing options**.  
If any item is `Unknown`, confirm with the DEV.

- **Runtime & language**: execution model, concurrency
- **Architecture shape**: monolith, services, async boundaries
- **Workload type**: CPU-bound, I/O-bound, memory-bound
- **Traffic profile**: volume, concurrency, variance
- **Current observability**: metrics, traces, none, partial
- **Test coverage**: presence of performance or regression tests
- **Operational maturity**: CI, staging, rollback capability

Only record **observable facts** here.  
No prescriptions, no assumptions.

---

## Implications (interpretation)

From the observed Repo Signals, derive implications such as:

- Reliability of measurements and benchmarks
- Risk of optimizing the wrong bottleneck
- Cost of collecting accurate performance data
- Likelihood of regressions after changes
- Expected ROI of local vs structural optimizations
- Whether performance issues are systemic or localized

These implications **frame** the options; they do not decide them.

---

## Process

1. **Validate Repo Signals**  
   Ask the DEV:  
   > “Can I proceed assuming these repository signals are accurate?”

2. **Define the performance question**  
   Clarify whether the goal is diagnosis, baseline creation, regression detection, or optimization.

3. **Establish a baseline**  
   Identify current performance under representative conditions.

4. **Collect evidence**  
   Use profiling, tracing, metrics, or controlled experiments as appropriate.

5. **Generate optimization options**  
   Produce **at least two and preferably three viable options**, strictly derived from:
   - observed bottlenecks
   - system behavior
   - constraints and maturity

6. **Evaluate options objectively**  
   Compare expected gains, cost, risk, and maintainability.

7. **Formulate a recommendation**  
   Recommend one option with explicit, defensible rationale.

8. **Confirm before optimizing**  
   No optimization should be applied without DEV approval.

---

## Options & trade-offs

Based on the analysis above, generate **context-specific optimization strategies**.

Examples of dimensions to vary (not presets):

- Local vs cross-cutting changes
- Algorithmic vs infrastructural optimizations
- Code-level vs architectural adjustments
- Short-term wins vs long-term improvements
- Performance gain vs complexity increase

For **each option**, include:

- **Description**: What would change and where
- **Pros**: Expected performance or cost improvements
- **Cons**: Complexity, risk, or maintenance cost
- **Risk profile**: Likelihood of regressions or mis-optimization
- **Estimated impact**: Based on measurements or benchmarks
- **Fit to current repo maturity**

Options must be **fully derived from collected evidence**, never pre-selected.

---

## Recommendation

Select **one** option as the recommended path.

### Recommendation criteria

The recommendation must explicitly consider:

- Measured or benchmarked performance impact
- Cost–benefit ratio
- Risk of functional or performance regressions
- Ease of validation and rollback
- Alignment with system and team maturity

### Rationale (required)

Provide a short rationale (3–6 bullets) explaining:

- Why this option best addresses the observed bottleneck
- Which trade-offs are consciously accepted
- What data or benchmarks informed the choice
- What future optimizations are intentionally deferred

---

## Output format

The response must include:

1. Confirmed Repo Signals
2. Performance goals and baseline
3. Identified bottlenecks with evidence
4. Generated options with trade-offs
5. Clear recommendation with rationale
6. Proposed change scope
7. Validation and success criteria
8. Open questions for the DEV

---

## Safety checks

- Never optimize without measured evidence
- Avoid conflating correlation with causation
- Guard against performance gains that reduce correctness
- Watch for environment-specific artifacts
- Document how to revert changes if assumptions fail

---

## Dev confirmation gates

Explicit DEV approval is required before:

- Adding or modifying instrumentation
- Applying optimizations that affect behavior
- Refactoring for performance reasons
- Introducing performance-critical dependencies
- Shipping changes without regression validation

Without confirmation, **do not proceed**.
