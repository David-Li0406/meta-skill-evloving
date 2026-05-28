---
name: data-migrations
description: Plan and execute schema/data migrations safely with compatibility, backfills, and rollback. Use when changing data models, schemas, or storage.
---

# Name

data-migrations

---

## When to use

Use this skill when planning or executing changes that affect persisted data, including:

- Schema or data model changes
- Backfills or data transformations
- Index or storage migrations
- Coordinating data changes with application releases

---

## Inputs required

Before proposing any migration plan, this skill requires:

- Description of the current and target data model
- Estimated data volume and access patterns
- Downtime tolerance and availability requirements
- Existing migration or backup tooling
- Regulatory or data integrity constraints (if any)

If any input is missing, **stop and ask the DEV**.

### Mandatory DEV questions

- What datastore(s) are involved?
- Is downtime acceptable? If so, how much?
- What data is critical and must not be lost?
- Are there SLAs or availability guarantees to respect?

---

## Repo Signals (observation)

This section must be completed **before generating migration strategies**.  
If any item is `Unknown`, confirm with the DEV.

- **Datastore**: Type, version, and hosting model
- **Migration tooling**: ORM tools, scripts, or manual processes
- **Testing**: Coverage around data access and integrity
- **CI/CD**: Ability to run migrations safely in pipelines
- **Operational maturity**: Backups, restore procedures, monitoring
- **Traffic profile**: Read/write patterns and peak usage

Only record **observable facts** here.

---

## Implications (interpretation)

From the observed Repo Signals, infer implications such as:

- Risk level of long-running or blocking migrations
- Feasibility of multi-step or online migrations
- Cost of rollback if the migration fails
- Operational burden during and after the change

> **Explicit bias of this skill**  
> When operational maturity or observability is low, this skill prioritizes **reversibility and incremental change** over speed.

---

## Process

1. **Validate Repo Signals**  
   Ask the DEV:  
   > “Can I proceed assuming these repository signals are correct?”

2. **Define migration scope**  
   Identify affected tables, records, indexes, and application paths.  
   Confirm:  
   > “Is this migration scope accurate?”

3. **Identify critical constraints**  
   Data integrity, availability, performance, and compliance.

4. **Generate migration strategies**  
   Produce **at least two and preferably three viable strategies**, derived strictly from the current context.

5. **Evaluate strategies objectively**  
   Compare execution time, risk, rollback complexity, and operational cost.

6. **Formulate recommendation**  
   Recommend one strategy with explicit rationale.

7. **Confirm before execution**  
   Do not draft runbooks or scripts without DEV approval.

---

## Options & trade-offs

Based on the current context, generate **contextual migration strategies**, such as:

- A strategy optimized for zero or near-zero downtime
- A strategy optimized for speed with controlled downtime
- A transitional strategy allowing old and new models to coexist

For **each option**, include:

- **Description**: How the migration is performed
- **Pros**: Concrete benefits
- **Cons**: Concrete drawbacks
- **Risk profile**: Failure modes and blast radius
- **Operational cost**: Tooling, monitoring, coordination
- **Fit to current operational maturity**

Options must be **derived from observed signals**, not pre-defined templates.

---

## Recommendation

Select one strategy as the recommended approach.

### Recommendation criteria

The recommendation must explicitly consider:

- Industry best practices for similar data volumes and stores
- Cost vs. benefit over time
- Risk exposure given current operational maturity
- Ability to validate and rollback safely

### Rationale (required)

Provide a short rationale (3–6 bullets) explaining:

- Why this strategy best fits the current context
- Which trade-offs are consciously accepted
- Under what conditions the recommendation should be revisited

---

## Output format

The response must include:

1. Confirmed Repo Signals
2. Key assumptions and constraints
3. Generated migration strategies with trade-offs
4. Clear recommendation with rationale
5. High-level migration plan (steps, validation, rollback)
6. Coordination notes with application releases
7. Open questions for the DEV

---

## Safety checks

- Require verified backups before execution
- Avoid long-running locks during peak traffic
- Validate data integrity before and after migration
- Ensure old and new code paths can coexist when needed
- Treat irreversible steps as explicit risk points

---

## Dev confirmation gates

Explicit DEV approval is required before:

- Locking the migration strategy
- Defining downtime windows
- Executing backfills or destructive changes
- Applying schema or storage changes
- Running the migration in production

Without confirmation, **do not proceed**.
