---
name: api-contracts
description: Define API contracts and typed boundaries between layers. Use when creating or modifying endpoints, schemas, or integrations.
---

# Name

api-contracts

---

## When to use

Use this skill when defining, changing, or validating API boundaries, including:

- Creation or modification of endpoints
- Definition or evolution of request/response schemas
- Sharing contracts between frontend, backend, or external consumers
- Introducing validation, versioning, or compatibility guarantees

---

## Inputs required

Before proposing any contract, this skill requires:

- API consumers (frontend, internal services, external clients)
- Expected usage patterns and frequency
- Compatibility and versioning requirements
- Existing error formats or conventions
- Regulatory or security constraints (if any)

If any input is missing, **stop and ask the DEV**.

### Mandatory DEV questions

- Who consumes this API and how often?
- Are there external or third-party consumers?
- What is the tolerance for breaking changes?
- Is formal versioning required now or later?

---

## Repo Signals (observation)

This section must be completed **before generating options**.  
If any item is `Unknown`, confirm with the DEV.

- **Stack**: Detected languages, runtimes, frameworks
- **Validation**: Existing schema or runtime validation (if any)
- **Testing**: Coverage around API boundaries
- **CI/CD**: Presence of checks enforcing contracts
- **Documentation**: Existing API docs or specs
- **Consumers**: Internal-only vs. external exposure

Only record **observable facts** here.

---

## Implications (interpretation)

From the observed Repo Signals, infer implications such as:

- Risk of breaking consumers
- Cost of enforcing stricter contracts
- Feasibility of code generation or shared schemas
- Operational overhead of documentation and validation

> **Explicit bias of this skill**  
> When consumer diversity and enforcement maturity are low, this skill prioritizes **evolutionary contracts** over rigid formalization.

---

## Process

1. **Validate Repo Signals**  
   Ask the DEV:  
   > “Can I proceed assuming these repository signals are correct?”

2. **Map API surface**  
   Identify endpoints, payloads, errors, and consumers.  
   Confirm:  
   > “Is this API surface map accurate?”

3. **Identify contract drivers**  
   Compatibility, safety, discoverability, performance, governance.

4. **Generate contract options**  
   Produce **at least two and preferably three viable options**, derived strictly from the current context.

5. **Evaluate options objectively**  
   Compare cost, risk, enforcement effort, and long-term impact.

6. **Formulate recommendation**  
   Recommend one option with explicit rationale.

7. **Confirm before advancing**  
   Do not propose implementation details without DEV approval.

---

## Options & trade-offs

Based on the current context, generate **contextual contract strategies**, such as:

- A lightweight, flexible contract optimized for internal iteration
- A formally specified contract optimized for multiple consumers
- A transitional or hybrid approach enabling gradual enforcement

For **each option**, include:

- **Description**: How contracts are defined and enforced
- **Pros**: Concrete benefits
- **Cons**: Concrete drawbacks
- **Risk profile**: Likelihood and impact of breaking changes
- **Operational cost**: Tooling, maintenance, CI impact
- **Fit to current repo maturity**

Options must be **derived from observed signals**, not pre-defined templates.

---

## Recommendation

Select one option as the recommended approach.

### Recom
