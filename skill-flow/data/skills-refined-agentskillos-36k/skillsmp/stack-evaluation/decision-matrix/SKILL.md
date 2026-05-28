---
name: decision-matrix
description: Build a weighted decision matrix to compare options. Use when user needs to compare stacks, technologies, or any set of alternatives with multiple criteria.
---

# Decision Matrix Builder

Build a weighted decision matrix to objectively compare alternatives.

## Standalone Usage

Can be invoked directly:
- "Help me compare these three database options"
- "Create a decision matrix for AWS vs GCP vs Azure"
- "Score these frameworks against my requirements"

## Standard Criteria (Stack Comparison)

| Criterion | Description |
|-----------|-------------|
| **cost** | Total cost of ownership |
| **ops_overhead** | Operational complexity |
| **reliability** | Uptime, failover, DR |
| **scalability** | Handle growth and spikes |
| **security** | Security features, compliance |
| **vendor_lock_in** | Migration difficulty |
| **local_dev_dx** | Developer experience |
| **offline_capability** | Offline support level (when required) |

## Scoring Guide (1-5)

| Score | Meaning |
|-------|---------|
| 1 | Poor / Very expensive / High overhead |
| 2 | Below average |
| 3 | Average / Acceptable |
| 4 | Good / Affordable / Low overhead |
| 5 | Excellent / Very cheap / Minimal overhead |

### Scoring Examples

**Cost Score**:
- 5: < $50/mo
- 4: $50-200/mo
- 3: $200-500/mo
- 2: $500-1000/mo
- 1: > $1000/mo

**Ops Overhead Score**:
- 5: Fully managed, zero ops (Vercel, Firebase)
- 4: Minimal ops, managed platform (App Runner, Supabase)
- 3: Some ops required (ECS, Cloud Run)
- 2: Significant ops (EKS, GKE managed)
- 1: Heavy ops (self-managed K8s, bare metal)

**Offline Capability Score** (when required):
- 5: Strong offline-first (CRDT, local-first, guaranteed sync)
- 4: Session-durable (IndexedDB, background sync)
- 3: Transient offline (graceful degradation, retry logic)
- 2: Limited buffering, data at risk
- 1: No offline support

## Process

### Step 1: Define Criteria

Use standard criteria or customize for the comparison.

### Step 2: Gather Weights

Ask user to assign importance (1-5) to each criterion.

**Default weights by ops maturity**:

| Criterion | Low Ops | Medium Ops | High Ops |
|-----------|---------|------------|----------|
| cost | 4 | 3 | 3 |
| ops_overhead | 5 | 3 | 2 |
| reliability | 3 | 4 | 5 |
| scalability | 2 | 3 | 4 |
| security | 3 | 4 | 5 |
| vendor_lock_in | 2 | 3 | 4 |
| local_dev_dx | 4 | 3 | 3 |

### Step 3: Score Options

Rate each option on each criterion (1-5).

### Step 4: Calculate Weighted Scores

```
weighted_score = Σ(score × weight) / Σ(weights)
```

### Step 5: Rank Options

Order by weighted total, highest first.

## Output Contract

```yaml
decision_matrix:
  comparison_name: "<what's being compared>"

  criteria:
    - name: "<criterion>"
      weight: <1-5>
      description: "<what it measures>"

  options:
    - id: "<option id>"
      name: "<option name>"
      scores:
        <criterion>: <1-5>
      weighted_total: <calculated>
      rank: <1-N>
      notes: "<any notes>"

  summary:
    winner: "<option id>"
    runner_up: "<option id>"
    key_differentiators:
      - "<what made the difference>"
```

## Presentation Format

| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|
| Cost | 4 | 4 ($$) | 3 ($$$) | 5 ($) |
| Ops Overhead | 3 | 5 | 3 | 4 |
| Reliability | 4 | 4 | 5 | 3 |
| Scalability | 3 | 3 | 5 | 4 |
| Security | 4 | 4 | 5 | 3 |
| Lock-in | 2 | 2 | 3 | 5 |
| Local Dev DX | 4 | 5 | 3 | 4 |
| **Weighted Total** | - | **3.92** | **3.83** | **3.79** |
| **Rank** | - | **1st** | **2nd** | **3rd** |

## Example: Database Comparison

```yaml
decision_matrix:
  comparison_name: "Database for SaaS application"

  criteria:
    - name: "cost"
      weight: 4
    - name: "ops_overhead"
      weight: 5
    - name: "scalability"
      weight: 3
    - name: "query_flexibility"
      weight: 4

  options:
    - id: "supabase"
      name: "Supabase (PostgreSQL)"
      scores:
        cost: 4
        ops_overhead: 5
        scalability: 3
        query_flexibility: 5
      weighted_total: 4.31
      rank: 1

    - id: "firebase"
      name: "Firebase (Firestore)"
      scores:
        cost: 3
        ops_overhead: 5
        scalability: 5
        query_flexibility: 2
      weighted_total: 3.69
      rank: 2

    - id: "aurora"
      name: "Aurora Serverless v2"
      scores:
        cost: 2
        ops_overhead: 4
        scalability: 5
        query_flexibility: 5
      weighted_total: 3.88
      rank: 2
```

## Custom Criteria

For non-stack comparisons, define custom criteria:

```yaml
# Example: Framework comparison
criteria:
  - name: "learning_curve"
    weight: 4
    description: "Time to productivity"
  - name: "ecosystem"
    weight: 3
    description: "Libraries, tools, community"
  - name: "performance"
    weight: 3
    description: "Runtime performance"
  - name: "hiring"
    weight: 4
    description: "Availability of developers"
```
