---
name: readability-review
description: Code review focused on readability, maintainability, and clarity. Use after code changes, before merging, or when reviewing pull requests.

---

# Name

readability-review

---

## Purpose

Evaluate and improve code **readability, clarity, and maintainability**
without assuming stylistic preferences, refactor scope, or repository maturity upfront.

Use this skill to surface **cognitive complexity, hidden coupling, and maintenance risks**
while preserving delivery flow and respecting existing constraints.

The goal is not stylistic perfection, but **code that is easier to understand, reason about, and change safely**.

---

## When to use

Use this skill when:

* Reviewing pull requests before merge
* Assessing large diffs or changes in critical areas
* Preparing code for long-term ownership or onboarding
* Noticing increasing friction when reading or modifying code
* Resolving ambiguity about whether a change is “good enough” to ship

---

## Inputs required

Before performing the review, gather:

* Target diff, PR, or commit range
* Functional intent of the change
* Areas of higher risk (security, data, performance, correctness)
* Existing conventions or guidelines (if any)
* Constraints on scope, timing, or refactoring appetite

If any of this context is missing, **stop and ask the DEV**.

### Mandatory DEV questions

* What is the primary goal of this change?
* Are there local conventions or patterns I should follow?
* Should the focus be narrow (readability only) or broader (structure, design)?
* Are refactors acceptable, or should suggestions stay minimal?
* Is this code expected to evolve further soon?

---

## Repo Signals (observation)

Capture only **observable facts** from the repository.
If anything is unclear, mark it as `Unknown` and confirm with the DEV.

* **Stack**: Languages, runtimes, frameworks
* **Code organization**: Folder structure, module boundaries
* **Conventions**: Naming, formatting, patterns actually used
* **Test coverage**: Presence and scope of tests near the diff
* **CI/CD**: Whether changes are automatically validated
* **Change surface**: Localized vs cross-cutting impact
* **Historical signals**: Similar patterns elsewhere in the codebase

Do not infer intent. Record only what is visible.

---

## Implications (interpretation)

From the observed signals and inputs, derive implications such as:

* Risk of misunderstanding or misusing the code later
* Cost of future changes given current structure
* Likelihood that readability issues mask deeper design problems
* Safety of suggesting refactors given test and CI maturity
* Trade-off between clarity improvements and delivery speed

Explicitly state assumptions and uncertainty.

---

## Process

1. **Validate observations**
   Ask the DEV:

   > “Can I proceed assuming these repository signals are accurate?”

2. **Understand intent before judging form**
   Clarify what the code is trying to achieve.
   Ask:

   > “Is my understanding of the intent correct?”

3. **Identify readability friction points**
   Look for naming ambiguity, cognitive load, hidden coupling, or over-complexity.

4. **Assess maintainability risk**
   Evaluate how easily this code can be modified or extended safely.

5. **Generate options from context**
   Produce **at least two and preferably three** viable review approaches,
   grounded entirely in the analysis above.

6. **Evaluate options objectively**
   Compare impact, risk, effort, and long-term value.

7. **Recommend and confirm**
   Make a defensible recommendation and request approval before proposing changes.

---

## Options & trade-offs

Based on the analysis above, generate **context-specific review strategies**.
Do **not** use predefined templates.

Each option must differ meaningfully in **scope, depth, and risk tolerance**.

For **each option**, include:

* **Description**: How the review is applied and what changes are suggested
* **Benefits**: Improvements to clarity, safety, or maintainability
* **Drawbacks**: Costs, risks, or deferred issues
* **Impact radius**: How much code or behavior is affected
* **Operational cost**: Review effort, refactor time, coordination needed
* **Preconditions**: Tests, alignment, or follow-up required

If only two options are viable, explain why a third is not.

---

## Recommendation

Select the option with the **best cost–benefit balance** given:

* Repository and team maturity
* Risk of regressions
* Time pressure and delivery constraints
* Expected lifespan of the code
* Benchmarks from similar codebases or past reviews (if available)

### Rationale (required)

Provide a concise rationale (3–6 bullets) explaining:

* Why this option best fits the current context
* Which trade-offs are consciously accepted
* What risks remain and how they can be mitigated
* What improvements should be deferred or scheduled later

Clearly state assumptions if benchmarks or historical data are missing.

---

## Output format

The final response must include:

1. Confirmed Repo Signals
2. Summary of intent and risk areas
3. Identified readability and maintainability issues
4. Generated options with trade-offs
5. Clear recommendation with rationale
6. Suggested scope of changes (if any)
7. Open questions for the DEV

---

## Safety checks

* Avoid refactors without test coverage
* Do not impose stylistic preferences without consensus
* Ensure suggested changes do not alter behavior unintentionally
* Flag changes that increase scope or coupling
* Treat readability improvements as iterative, not all-or-nothing

---

## Dev confirmation gates

Explicit DEV approval is required before:

* Suggesting structural refactors
* Changing public APIs or module boundaries
* Applying sweeping style changes
* Introducing new abstractions or patterns

Without confirmation, **do not proceed**.
