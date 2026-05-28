---
name: stack-evaluation
description: Generate and evaluate stack candidates with a decision matrix. Use when after architecture-refinement completes.
---

# Stack Options & Evaluation (Orchestrator)

Generate 2-5 coherent stack candidates, evaluate them across multiple dimensions (including local dev experience), and present a comparable decision matrix.
Different stacks can be optimize for specific vendor like AWS, GCP, Vercel.

## Prerequisites

Requires architecture brief from **architecture-refinement** skill. If not available, invoke that skill first.

## Process Overview

This skill orchestrates the following standalone skills (each can also be invoked directly):

1. **candidate-generator** - Generate 2-5 stack candidates based on requirements
2. **decision-matrix** - Build weighted comparison matrix
3. **Cost evaluators** - Estimate costs per provider:
   - **cost-aws** - AWS infrastructure costs
   - **cost-gcp** - GCP infrastructure costs
   - **cost-supabase** - Supabase platform costs
   - **cost-firebase** - Firebase platform costs
   - **cost-vercel** - Vercel platform costs
4. **local-dev-evaluator** - Assess local development experience
5. **offline-impact-evaluator** - Validate stack against offline requirement
6. **aspire-evaluator** - Check .NET Aspire fit (when applicable)
7. **custom-explorer** - Evaluate user-proposed combinations

All sub-skills are in the `stack-evaluation/` directory and can be triggered independently.
For example: "Estimate AWS costs for EKS + Aurora" triggers **cost-aws** directly.

## Evaluation Factors

Each candidate stack must be evaluated across:
- Monthly cost (baseline + scale curve)
- Maintainability / ops overhead
- Elasticity
- Reliability & DR posture
- Observability
- Security posture
- Vendor lock-in
- **Local Dev DX** (mandatory):
  - Time-to-first-run
  - Local dependency orchestration complexity
  - Prod parity (auth/data/async/config)
  - Local debugging + dev-time observability
- **Offline Capability** (when required):
  - Offline strategy (cache-only, IndexedDB/SQLite, event queue, CRDTs, background sync)
  - Data-loss prevention guarantees (none, ephemeral, session-durable, strong)
  - Consistency model (none, eventual, strong)
  - Sync complexity (1-5)

## Output Contract

```yaml
stack_evaluation:
  architecture_brief_id: "<reference>"
  candidates:
    - id: "<unique_id>"
      name: "<name>"
      summary: "<one-line>"
      components:
        frontend: { technology: "", hosting: "" }
        backend: { technology: "", hosting: "" }
        database: { technology: "", hosting: "" }
        auth: { provider: "" }
        async: { technology: "" }
        storage: { technology: "" }
      local_dev_story: "<how to run locally>"
      offline_profile:
        strategy: "<cache_only|indexeddb|sqlite|crdt|event_queue|none>"
        data_loss_guarantee: "<none|ephemeral|session_durable|strong>"
        consistency_model: "<none|eventual|strong>"
        sync_complexity: <1-5>
      cost_estimate:
        baseline: "<$/month>"
        at_scale: "<$/month>"
      scores:
        cost: <1-5>
        ops_overhead: <1-5>
        reliability: <1-5>
        scalability: <1-5>
        security: <1-5>
        vendor_lock_in: <1-5>
        local_dev_dx: <1-5>
        offline_capability: <1-5>
  decision_matrix:
    criteria_weights:
      cost: <1-5>
      ops_overhead: <1-5>
      reliability: <1-5>
      scalability: <1-5>
      security: <1-5>
      vendor_lock_in: <1-5>
      local_dev_dx: <1-5>
      offline_capability: <1-5>
    ranked_options:
      - candidate_id: "<id>"
        weighted_score: <score>
        rank: 1
  recommendation:
    top_choice: "<candidate_id>"
    rationale: "<why>"
    tradeoffs: "<key tradeoffs>"
```

## Presentation

Present as comparison table:

| Criterion | Weight | Candidate A | Candidate B | Candidate C |
|-----------|--------|-------------|-------------|-------------|
| Cost | 4 | 4 ($$) | 3 ($$$) | 5 ($) |
| Ops Overhead | 3 | 5 (minimal) | 3 (moderate) | 4 (low) |
| Local Dev DX | 4 | 4 (good) | 3 (fair) | 5 (excellent) |
| Offline Capability | 3 | 4 (session) | 2 (transient) | 5 (strong) |
| **Weighted Total** | - | **X.X** | **X.X** | **X.X** |

## Next Step

After user reviews candidates, proceed to **stack-selection** skill to confirm the chosen stack.
