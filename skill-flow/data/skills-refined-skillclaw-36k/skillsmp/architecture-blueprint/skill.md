---
name: architecture-blueprint
description: Plan system architecture and design for new features, large refactors, and long-term decisions; use when there is impact on components, data, integrations, or scalability.
---

# Name

architecture-blueprint

---

## When to use

Use this skill when making architectural or system-level decisions with medium to long-term impact, including:

- New features spanning multiple components, services, or data flows
- Structural refactors that change module or domain responsibilities
- Decisions affecting data models, integrations, scalability, or deployment
- Selection or evolution of core technical patterns or infrastructure

---

## Inputs required

Before proposing any solution, this skill requires:

- Feature goal and success metrics
- Non-functional requirements (latency, scale, reliability, security)
- External integrations and dependencies
- Explicit constraints (timeline, budget, compliance)
- Acceptable risk level

If any of these are missing, **stop and ask the DEV**.

### Mandatory DEV questions

- What outcome matters most for this change?
- What scale and latency bounds must be respected?
- Are there hard constraints on stack, platform, or vendors?
- What level of risk is acceptable right now?

---

## Repo Signals (observation)

This section must be completed **before generating options**.  
If any item is `Unknown`, confirm with the DEV.

- **Stack**: Detected languages, runtimes, frameworks
- **Conventions**: Linting, formatting, folder structure, naming
- **Testing**: Type, coverage, execution cost
- **CI/CD**: Presence, maturity, enforcement
- **Architecture**: Existing boundaries, layers, or domain separation
- **Operational maturity**: Monitoring, rollback mechanisms, deploy frequency

Only record **observable facts** here.

---

## Implications (interpretation)

Based on the observed Repo Signals, derive implications such as:

- Risk level of large vs. incremental changes
- Cost of rollback and failure recovery
- Flexibility to introduce new boundaries or abstractions
- Likely maintenance burden over time

> **Explicit bias of this skill**  
> When structural maturity is low or unclear, this skill prioritizes **reversibility and controlled risk** over theoretical optimality.

---

## Process

1. **Validate Repo Signals**  
   Ask the DEV:  
   > “Can I proceed assuming these repository signals are correct?”

2. **Confirm decision scope**  
   Define what is explicitly in and out of scope.

3. **Identify decision drivers**  
   Data integrity, performance, security, team velocity, operational cost.

4. **Generate architectural options**  
   Produce **at least two and preferably three viable options**, derived strictly from the context above.

5. **Compare options objectively**  
   Evaluate each option against benchmarks, cost, risk, and long-term impact.

6. **Formulate recommendation**  
   Recommend one option, with a clear rationale.

7. **Confirm before advancing**  
   No implementation guidance without DEV approval.

---

## Options & trade-offs

Based on the current context, generate **contextual options**, such as:

- An option that optimizes for short-term safety and low disruption
- An option that optimizes for long-term scalability or clarity
- (Optional) A hybrid or transitional option

Each option must include:

- **Description**: What changes structurally
- **Pros**: Concrete benefits
- **Cons**: Concrete drawbacks
- **Risk profile**: Failure modes and reversibility
- **Operational cost**: Complexity, tooling, maintenance
- **Fit to current repo maturity**

Options must be derived from the observed signals — **not pre-defined templates**.

---

## Recommendation

Select one option as the recommended path.

### Recommendation criteria

The recommendation must explicitly consider:

- Industry benchmarks or common practices (where applicable)
- Cost vs. benefit over time
- Risk exposure given current repo maturity
- Team and operational constraints

### Rationale (required)

Provide a short rationale (3–6 bullets) explaining:

- Why this option best fits the current context
- What trade-offs are being consciously accepted
- Under which conditions this recommendation should be revisited

---

## Output format

The response must include:

1. Confirmed Repo Signals
2. Key assumptions and constraints
3. Generated options with trade-offs
4. Clear recommendation with rationale
5. High-level component and data flow sketch
6. Incremental execution plan
7. Open questions for the DEV

---

## Safety checks

- Identify breaking changes and compatibility risks
- Avoid irreversible decisions without explicit versioning
- Define rollback strategy and success criteria
- Surface performance and security risks early
- Never assume test or CI coverage without confirmation

---

## Dev confirmation gates

Explicit DEV approval is required before:

- Locking Repo Signals and scope
- Selecting the recommended option
- Introducing breaking changes
- Performing data migrations or storage changes
- Preparing or applying any code-level changes

Without confirmation, **do not proceed**.
