---
name: docs-adr
description: Documentation and ADR updates for architectural decisions. Use when there are design changes, new features, or a need to record decisions.
---

# Skill: Documentation & ADRs

## Purpose

Produce and maintain **accurate, decision-oriented documentation** and **Architecture Decision Records (ADRs)** that reflect the current state of the system and its rationale.

This skill is intended to support **architectural clarity, long-term maintainability, and informed decision-making**, not to prescribe design choices in advance.

No documentation strategy or ADR format should be assumed before analyzing the repository context.

---

## When to Use

- Making or revisiting a significant architectural decision
- Introducing changes that affect system structure, APIs, or data flows
- Adding new features with non-trivial design implications
- Aligning documentation with evolved or refactored code
- Preserving decision rationale for future maintainers

---

## Inputs Required

Before drafting or updating documentation, collect:

- The decision, change, or topic to be documented
- Target audience(s) (internal developers, contributors, operators, users)
- Scope and impact of the change
- Existing documentation locations and formats (if any)

If any input is missing or ambiguous, **stop and ask the DEV**.

### Mandatory DEV Questions

- Who is the primary audience for this documentation?
- What decision or change must be recorded or explained?
- Is this a new decision or a revision of a past one?
- Should this be captured as a formal ADR or lightweight documentation?

---

## Repo Signals (Observation Only)

This section must be completed **before proposing any documentation approach**.  
Only record **observable facts**.

- **Project maturity**: early-stage, growing, or stable
- **Existing docs**: presence, structure, and freshness
- **ADR usage**: none, ad-hoc, or standardized
- **Change frequency**: architectural churn vs stability
- **Contribution model**: solo, small team, or open contributors

If any signal is unclear, confirm with the DEV.

---

## Implications (Derived)

From the observed Repo Signals, derive implications such as:

- Level of formality required in documentation
- Risk of documentation drift if over- or under-specified
- Cost of maintaining detailed records over time
- Importance of traceability versus speed
- Onboarding and knowledge-transfer needs

Explicitly state assumptions and validate them with the DEV when necessary.

---

## Process

1. **Validate Repo Signals**  
   Ask the DEV:  
   > “Can I proceed assuming these repository signals are accurate?”

2. **Clarify the Decision or Change**  
   Define what must be documented and why.  
   Ask:  
   > “Is this the correct scope for documentation?”

3. **Assess Documentation Needs**  
   Determine required depth, structure, and longevity based on context.

4. **Derive Documentation Options**  
   Based on analysis, generate **at least two and preferably three viable documentation approaches**, each consistent with the repository’s maturity and constraints.

5. **Evaluate Trade-offs**  
   Compare options using objective criteria such as cost, clarity, maintenance burden, and alignment with industry practices.

6. **Formulate a Recommendation**  
   Recommend one option with explicit rationale.

7. **Confirm Before Writing or Updating**  
   No documentation or ADR should be finalized without DEV approval.

---

## Options & Trade-offs (Context-Derived)

This section must be generated **after analysis**, not pre-filled.

For each option, include:

- **Description**: What will be documented and how
- **Pros**: Benefits in clarity, traceability, or alignment
- **Cons**: Costs in effort, maintenance, or rigidity
- **Longevity**: Expected useful lifespan of the documentation
- **Maintenance cost**: Ongoing effort to keep it accurate
- **Fit to current repo maturity**

Options must be **fully derived from the observed context**, not generic templates.

---

## Recommendation

Select **one** option as the recommended approach.

### Recommendation Criteria

The recommendation must explicitly consider:

- Cost–benefit ratio
- Repository maturity and expected growth
- Industry benchmarks or common practices
- Risk of under- or over-documentation
- Long-term maintenance implications

### Rationale (Required)

Provide a concise rationale explaining:

- Why this option best fits the current situation
- Which trade-offs are consciously accepted
- What future documentation work may be needed

---

## Output Format

The response must include:

1. Confirmed Repo Signals
2. Summary of the decision or change being documented
3. Context-derived documentation options with trade-offs
4. Clear recommendation with rationale
5. Proposed structure or outline (no full content unless approved)
6. Open questions for the DEV

---

## Safety Checks

- Do not document assumptions that are not validated
- Avoid documentation that contradicts the current codebase
- Clearly distinguish decisions from hypotheses
- Avoid unnecessary verbosity in early-stage repos
- Flag any documentation that may become stale quickly

---

## Dev Confirmation Gates

Explicit DEV approval is required before:

- Creating or updating ADRs
- Publishing or merging documentation
- Introducing new documentation standards or formats
- Recording decisions with long-term impact

Without confirmation, **do not proceed**.
