---
name: parallel-execution
description: Parallel execution patterns for cognitive reasoning tasks. Use when independent sub-problems can be solved simultaneously, multiple solution approaches need exploration, ensemble confidence is required, or time permits depth without sequential constraints. Integrates with ToT, BoT, HE, and AT for accelerated reasoning with fan-out/fan-in, MCTS-style search, and MoA aggregation patterns.
license: MIT
---

# Parallel Execution Patterns for Cognitive Reasoning

**Purpose**: Accelerate and improve cognitive reasoning by executing independent tasks simultaneously. Parallel execution can achieve 2-4x efficiency gains and 70% faster convergence when applied appropriately to reasoning patterns like ToT, BoT, HE, and AT.

## When to Use Parallel Execution

**Use parallel execution when:**
- Problem decomposes into independent sub-problems
- Multiple solution approaches need exploration (BoT, ToT branching)
- High confidence required (ensemble methods)
- Multiple hypotheses need simultaneous testing (HE)
- Time permits depth but sequential execution is unnecessary
- Cross-domain analogies need parallel investigation (AT)

**Do not parallelize when:**
- Steps have sequential dependencies (use SRC instead)
- Each step depends on previous results
- Problem is inherently linear (debugging traces)
- Resource constraints limit concurrent execution
- Merge strategy is undefined

**Parallelization Decision Matrix:**

| Problem Characteristic | Parallelize? | Rationale |
|------------------------|--------------|-----------|
| Independent sub-problems | Yes | No dependencies, safe to parallelize |
| Multiple valid approaches | Yes | BoT/ToT branches are independent |
| Hypothesis testing | Yes | HE hypotheses can test in parallel |
| Sequential reasoning | No | SRC chains have dependencies |
| Cause-effect tracing | No | Effects depend on causes |
| Resource gathering | Yes | Independent evidence sources |

---

## Core Patterns

### Pattern 1: Dynamic Parallel Tree Search (DPTS)

**Efficiency**: 2-4x improvement, 70% faster convergence

**Description**: Adaptive parallel exploration that dynamically allocates resources to promising branches while pruning unpromising ones. Unlike static parallel search, DPTS reallocates workers as branches are evaluated.

**Key Mechanisms:**
- **Dynamic worker allocation**: More workers on promising branches
- **Adaptive pruning thresholds**: Thresholds adjust based on best-found confidence
- **Early termination**: Stop exploring when confidence exceeds threshold
- **Resource rebalancing**: Move workers from exhausted/pruned branches

**Integration with ToT:**

```markdown
## DPTS + Tree of Thoughts

### Phase 1: Initial Parallel Expansion
- Spawn N workers for Level 0 branches (N = 5-10)
- Each worker explores one branch independently
- Workers report confidence scores as they complete

### Phase 2: Dynamic Reallocation
- As Level 0 completes, rank branches by score
- Top 2 branches get 3 workers each for Level 1
- Remaining branches get 1 worker each
- Prune branches below dynamic threshold

### Phase 3: Convergence
- Continue reallocation until:
  - Winning branch confidence > 85%
  - OR all branches at Level 4+
  - OR diminishing returns detected

### Pruning Threshold Formula
dynamic_threshold = max(0.40, best_confidence - 0.30)
```

**Example DPTS Execution:**

```
Level 0: 5 branches, 5 workers (parallel)
├─ Branch A: 75% confidence (3 workers assigned for L1)
├─ Branch B: 68% confidence (2 workers assigned for L1)
├─ Branch C: 52% confidence (1 worker, threshold = 45%)
├─ Branch D: 48% confidence (1 worker, threshold = 45%)
└─ Branch E: 35% confidence (PRUNED, below threshold)

Level 1: 8 workers reallocated
├─ A.1, A.2, A.3: parallel (3 workers)
├─ B.1, B.2: parallel (2 workers)
├─ C.1: sequential (1 worker)
└─ D.1: sequential (1 worker)

Best found: A.2 at 82% → New threshold: 52%
→ Branch D PRUNED (48% < 52%)
→ 1 worker reallocated to Branch A
```

---

### Pattern 2: Branch-Solve-Merge (BSM)

**Description**: Three-phase pattern that decomposes problems, solves sub-problems in parallel, then merges results. Ideal for problems that can be cleanly partitioned.

**Phases:**

```markdown
## Branch Phase (Decomposition)
1. Analyze problem structure
2. Identify independent sub-problems
3. Define interfaces between sub-problems
4. Create sub-problem specifications

## Solve Phase (Parallel Execution)
1. Spawn worker per sub-problem
2. Each worker solves independently
3. Workers report partial solutions
4. Monitor for blocking dependencies

## Merge Phase (Aggregation)
1. Collect all partial solutions
2. Apply merge strategy (see below)
3. Resolve conflicts
4. Synthesize final solution
```

**Merge Strategies:**

| Strategy | When to Use | Method |
|----------|-------------|--------|
| **Consensus** | Multiple workers on same problem | Majority agreement |
| **Voting** | Competing approaches | Weighted score aggregation |
| **Aggregation** | Complementary results | Union with deduplication |
| **Synthesis** | Conflicting valid results | Dialectical resolution |

**BSM Example - Architecture Decision:**

```markdown
## Branch: "Design authentication system"
Sub-problems:
1. Token format selection (JWT vs Session vs API Key)
2. Storage strategy (Redis vs DB vs Memory)
3. Security requirements (MFA, encryption, audit)
4. Performance requirements (latency, throughput)

## Solve: 4 parallel workers
Worker 1: Evaluates token formats → JWT (85%)
Worker 2: Evaluates storage → Redis (78%)
Worker 3: Analyzes security → MFA required (92%)
Worker 4: Benchmarks performance → < 50ms needed (88%)

## Merge: Aggregation strategy
- JWT + Redis + MFA + 50ms latency
- Check compatibility: All compatible
- Synthesize: "JWT tokens stored in Redis with MFA, target 50ms"
```

---

### Pattern 3: Mixture of Agents (MoA)

**Description**: Layered architecture where proposer agents generate solutions and aggregator agents synthesize them. Mimics ensemble learning for improved robustness.

**Architecture:**

```
┌─────────────────────────────────────────────────┐
│                 Aggregator Layer                 │
│  (Synthesizes proposals, resolves conflicts)    │
└────────────────────┬────────────────────────────┘
                     │ Proposals flow up
┌─────────────────────────────────────────────────┐
│                 Proposer Layer                   │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐           │
│  │Proposer1│ │Proposer2│ │Proposer3│  ...      │
│  │ (ToT)   │ │ (BoT)   │ │ (AT)    │           │
│  └─────────┘ └─────────┘ └─────────┘           │
└─────────────────────────────────────────────────┘
```

**MoA Configuration:**

```markdown
## Proposer Configuration

### Proposer 1: Optimization Focus (ToT)
- Objective: Find optimal solution
- Evaluation: Score-based ranking
- Output: Single best path with confidence

### Proposer 2: Exploration Focus (BoT)
- Objective: Map solution space
- Evaluation: Coverage-based
- Output: Top 5 viable options

### Proposer 3: Analogy Focus (AT)
- Objective: Cross-domain insights
- Evaluation: Structural mapping quality
- Output: Transferred principles

## Aggregator Configuration

### Aggregation Method: Weighted Synthesis
- Weight by proposer confidence
- Identify common themes across proposers
- Flag disagreements for explicit resolution

### Conflict Resolution
- If proposers agree: Boost confidence +5%
- If 2/3 agree: Use majority, document minority
- If no agreement: Escalate to DR (Dialectical Reasoning)
```

**MoA for Multi-Perspective Analysis:**

```markdown
## Problem: "Choose database for new microservice"

### Proposer 1 (ToT): Score-optimized
→ PostgreSQL (Score: 87/100)
  - Best for ACID compliance
  - Strong query performance

### Proposer 2 (BoT): Option-mapped
→ Top 3: PostgreSQL (72%), MongoDB (68%), DynamoDB (65%)
  - PostgreSQL: Relational, ACID
  - MongoDB: Flexible schema
  - DynamoDB: Serverless scale

### Proposer 3 (AT): Analogy-based
→ Recommendation: PostgreSQL
  - Analogy: Banking systems use relational for audit trails
  - Our use case: Financial transactions need same guarantees

### Aggregator Synthesis
Agreement Level: FULL (3/3 on PostgreSQL)
Combined Confidence: max(87%, 72%, 75%) + 5% = 92%

Final Recommendation: PostgreSQL with high confidence
- Optimization confirms performance
- Exploration confirms no better alternatives
- Analogy confirms domain fit
```

---

### Pattern 4: Graph of Thoughts (GoT)

**Description**: Arbitrary graph-structured reasoning where thoughts can merge, split, and form cycles. More flexible than tree-structured ToT.

**Graph Operations:**

| Operation | Description | Use Case |
|-----------|-------------|----------|
| **Branch** | Split one thought into multiple | Generate alternatives |
| **Merge** | Combine multiple thoughts into one | Synthesize findings |
| **Refine** | Iterate on a single thought | Improve solution |
| **Backtrack** | Return to previous thought | Error correction |
| **Cycle** | Re-evaluate with new information | Iterative improvement |

**GoT Structure:**

```
     [Problem]
        │
    ┌───┴───┐
    ▼       ▼
  [A]     [B]
    │       │
    ▼       ▼
  [A.1]   [B.1]
    │       │
    └───┬───┘
        ▼
    [Merged]──────┐
        │         │
        ▼         │ Cycle
    [Refined] ◄───┘
        │
        ▼
    [Solution]
```

**GoT Implementation:**

```markdown
## GoT Reasoning Session

### Step 1: Branch (Problem → A, B, C)
Generate three distinct approaches in parallel

### Step 2: Refine (A → A', B → B')
Improve promising approaches through iteration

### Step 3: Merge (A' + B' → AB)
Combine best elements of top approaches

### Step 4: Cycle (AB → AB')
Re-evaluate merged solution with fresh perspective

### Step 5: Converge (AB' → Solution)
Finalize when confidence threshold met
```

**GoT vs ToT Comparison:**

| Aspect | ToT | GoT |
|--------|-----|-----|
| Structure | Tree (no merges) | Arbitrary graph |
| Merging | Not supported | Core operation |
| Cycles | Not allowed | Allowed (iterative) |
| Flexibility | Fixed branching | Dynamic |
| Complexity | Lower | Higher |
| Best for | Clear evaluation criteria | Complex, iterative problems |

---

### Pattern 5: Self-Consistency with RASC

**Efficiency**: 70% compute reduction vs naive self-consistency

**Description**: Rationalized Self-Consistency (RASC) generates multiple reasoning paths, clusters by rationale similarity, then uses representative answers. Reduces redundant computation while maintaining ensemble benefits.

**RASC Process:**

```markdown
## Phase 1: Parallel Path Generation
- Generate K reasoning paths (K = 5-10)
- Each path solves problem independently
- Collect both answer AND rationale

## Phase 2: Rationale Clustering
- Cluster paths by rationale similarity
- Identify distinct reasoning approaches
- Group paths with similar logic

## Phase 3: Representative Selection
- Select representative from each cluster
- Weight by cluster size (more paths = more weight)
- Eliminates redundant similar paths

## Phase 4: Aggregation
- Combine representatives (not all K paths)
- Apply weighted voting
- Confidence = agreement level among representatives
```

**RASC Example:**

```markdown
## Problem: "Should we use microservices or monolith?"

### Generated Paths (K=10):
Path 1: Microservices - "team autonomy" rationale
Path 2: Microservices - "scalability" rationale
Path 3: Microservices - "team autonomy" rationale (similar to 1)
Path 4: Monolith - "simplicity" rationale
Path 5: Microservices - "scalability" rationale (similar to 2)
Path 6: Microservices - "team autonomy" rationale (similar to 1)
Path 7: Monolith - "simplicity" rationale (similar to 4)
Path 8: Microservices - "tech diversity" rationale (new cluster)
Path 9: Monolith - "performance" rationale (new cluster)
Path 10: Microservices - "scalability" rationale (similar to 2)

### Clusters:
Cluster A (size 3): "team autonomy" → Path 1 representative
Cluster B (size 3): "scalability" → Path 2 representative
Cluster C (size 2): "simplicity" → Path 4 representative
Cluster D (size 1): "tech diversity" → Path 8 representative
Cluster E (size 1): "performance" → Path 9 representative

### Weighted Vote:
Microservices: Clusters A(3) + B(3) + D(1) = 7 weight
Monolith: Clusters C(2) + E(1) = 3 weight

### Final: Microservices (70% weighted agreement)
Rationales: Team autonomy, Scalability, Tech diversity
```

---

## Integration with Cognitive Skills

### BoT Integration: Parallel Branch Exploration

```markdown
## BoT + Parallel Execution

### Standard BoT (Sequential):
Explore Approach 1 → Explore Approach 2 → ... → Explore Approach 8
Total time: 8 × T(explore)

### Parallel BoT:
Explore Approaches 1-8 simultaneously
Total time: 1 × T(explore) (with parallelism)

### Implementation:
1. Level 0: Spawn 8-10 parallel workers
2. Each worker explores one approach independently
3. Workers share evidence repository (./reasoning/evidence/)
4. Pruning happens after ALL Level 0 complete
5. Level 1: Spawn workers for retained approaches

### Pruning Threshold (BoT-specific):
Keep approaches with confidence > 40%
Do NOT dynamically adjust (conservative breadth philosophy)
```

### ToT Integration: MCTS-Style Search

```markdown
## ToT + Monte Carlo Tree Search (MCTS)

### MCTS Integration:
1. **Selection**: UCB1 formula to balance explore/exploit
2. **Expansion**: Parallel branch generation
3. **Simulation**: Parallel rollouts to estimate branch value
4. **Backpropagation**: Update ancestor scores

### UCB1 Formula:
UCB1(branch) = avg_score + C × sqrt(ln(N) / n_branch)
- avg_score: Average score from simulations
- C: Exploration constant (typically 1.41)
- N: Total simulations across all branches
- n_branch: Simulations for this branch

### Parallel MCTS for ToT:
1. Run parallel rollouts from each Level 0 branch
2. Use UCB1 to decide which branches get more rollouts
3. After budget exhausted, select best-scoring branch
4. Recurse with same strategy for Level 1, 2, 3...

### Configuration:
- Rollouts per branch: 10-20
- Exploration constant: 1.41
- Minimum rollouts before pruning: 5
```

### HE Integration: Parallel Hypothesis Testing

```markdown
## HE + Parallel Execution

### Sequential HE (Standard):
Test H1 → Test H2 → Test H3 → ...
Each test may affect others (evidence dependencies)

### Parallel HE (Accelerated):
Phase 1: Generate all hypotheses (8-15)
Phase 2: Identify INDEPENDENT evidence gathering
  - Evidence that affects only one hypothesis → parallelize
  - Evidence that affects multiple → sequence based on discrimination power
Phase 3: Parallel evidence gathering
Phase 4: Synchronized hypothesis update

### Evidence Parallelization Rules:
- Log analysis: Usually parallelizable (independent sources)
- Metrics queries: Parallelizable (independent systems)
- Reproduction tests: May conflict (shared test environment)
- Code tracing: Parallelizable (read-only)

### Synchronization Points:
After each parallel batch, synchronize to:
1. Update ALL hypothesis probabilities
2. Check for eliminations
3. Decide next evidence batch
```

### AT Integration: Multi-Perspective via MoA

```markdown
## AT + Mixture of Agents

### Standard AT:
Investigate Analogy 1 → Investigate Analogy 2 → ... → Synthesize

### MoA-Enhanced AT:
Layer 1 (Proposers): Parallel analogy investigation
  - Worker 1: Technology domain analogies
  - Worker 2: Nature/biology analogies
  - Worker 3: Business/economics analogies
  - Worker 4: Historical analogies

Layer 2 (Aggregator): Cross-analogy synthesis
  - Identify common principles across domains
  - Weight by structural mapping quality
  - Synthesize unified transferable insights

### Aggregation Strategy for AT:
- Principles appearing in 3+ analogies: High confidence
- Principles appearing in 2 analogies: Medium confidence
- Principles appearing in 1 analogy: Low confidence (needs validation)
```

---

## Implementation Patterns

### Fan-Out/Fan-In Pattern

```markdown
## Fan-Out/Fan-In Structure

### Fan-Out Phase:
1. Identify parallelizable work units
2. Create work unit specifications
3. Spawn workers (one per work unit)
4. Track worker status (pending/running/complete/failed)

### Fan-In Phase:
1. Wait for all workers OR timeout
2. Collect results from completed workers
3. Handle failed workers (retry/skip/abort)
4. Apply merge strategy

### Implementation with Task Tool:

# Fan-out
for approach in approaches:
    spawn_task(
        description=f"Explore {approach.name}",
        input=approach.specification,
        pattern="BoT-L1"
    )

# Fan-in
results = await_all_tasks(timeout=30min)
merged = apply_merge_strategy(results, strategy="aggregation")
```

### Checkpoint Integration

```markdown
## Parallel Execution + Handover Protocol

### Checkpoint Timing:
- Before fan-out: Checkpoint work unit specifications
- After fan-out: Checkpoint spawned worker IDs
- During execution: Workers checkpoint individually
- After fan-in: Checkpoint merged results

### Recovery from Parallel Failure:
1. Load checkpoint with worker states
2. Identify failed workers
3. Retry failed workers only
4. Resume fan-in when complete

### State File Structure:
.reasoning/session-{id}/
├── parallel/
│   ├── fan-out-spec.json      # Work unit specifications
│   ├── worker-status.json     # Worker states
│   ├── worker-001/            # Individual worker state
│   ├── worker-002/
│   └── fan-in-result.json     # Merged result
```

### Pruning Strategies

| Pattern | Threshold | Rationale |
|---------|-----------|-----------|
| **BoT** | Static 40% | Conservative breadth, never miss viable option |
| **ToT** | Static top-1/top-2 | Find single best, aggressive pruning OK |
| **DPTS** | Dynamic (best - 30%) | Adaptive to discovered landscape |
| **HE** | Evidence-based | Prune when evidence eliminates |
| **MoA** | Agreement-based | Prune minority positions after consensus |

---

## When to Parallelize: Decision Framework

### Parallelization Checklist

Before parallelizing, verify:

- [ ] **Independence**: Can work units execute without sharing state?
- [ ] **Merge Strategy**: Is there a clear way to combine results?
- [ ] **Resource Availability**: Are sufficient workers available?
- [ ] **Benefit Justification**: Will parallel execution actually save time?
- [ ] **Failure Handling**: What happens if some workers fail?

### Decision Tree

```
Is the task decomposable?
├─ NO → Use sequential execution
└─ YES → Are sub-tasks independent?
    ├─ NO → Use sequential with checkpoints
    └─ YES → Is merge strategy clear?
        ├─ NO → Define merge strategy first
        └─ YES → Is parallelization worth the overhead?
            ├─ NO (< 3 sub-tasks) → Sequential may be simpler
            └─ YES → Parallelize with fan-out/fan-in
```

---

## Anti-Patterns to Avoid

### 1. Parallelizing Sequential Dependencies

**Bad:**
```markdown
Step 1: Get user input (parallel) ─┐
Step 2: Validate input (parallel) ─┼─ WRONG: Step 2 needs Step 1!
Step 3: Process input (parallel) ──┘
```

**Good:**
```markdown
Step 1: Get user input
  └─→ Step 2: Validate input
      └─→ Step 3: Process input
```

### 2. Too Many Branches (Diminishing Returns)

**Bad:**
```
Level 0: 20 branches (overwhelming, redundant)
Level 1: 100 sub-branches (unmanageable)
```

**Good:**
```
Level 0: 5-10 branches (diverse, manageable)
Level 1: 5 sub-branches per retained branch
```

**Rule of Thumb**: Total branches = 5^depth is reasonable. 5^4 = 625 is the practical maximum.

### 3. No Merge Strategy Defined

**Bad:**
```markdown
Fan-out: Spawn 5 workers to explore approaches
Fan-in: ??? (no plan to combine results)
```

**Good:**
```markdown
Fan-out: Spawn 5 workers to explore approaches
Fan-in: Apply weighted voting based on confidence scores
        If disagreement > 30%, escalate to DR pattern
```

### 4. Ignoring Shared State

**Bad:**
Workers write to same file simultaneously → Race condition

**Good:**
- Workers write to isolated directories
- Fan-in phase merges results
- Use evidence repository with indexed access

### 5. Parallel Everything

**Bad:**
"I'll parallelize to go faster!" (on a sequential problem)

**Good:**
- Analyze problem structure first
- Parallelize only independent work
- Accept that some problems are inherently sequential

---

## Configuration Reference

### Default Parallel Settings

```json
{
  "parallel_execution": {
    "max_workers": 10,
    "worker_timeout_minutes": 30,
    "fan_in_timeout_minutes": 60,

    "pruning": {
      "bot_threshold": 0.40,
      "tot_keep_top": 2,
      "dpts_margin": 0.30,
      "min_confidence_to_continue": 0.40
    },

    "merge_strategies": {
      "default": "aggregation",
      "conflict_resolution": "weighted_voting",
      "confidence_agreement_boost": 0.05,
      "confidence_disagreement_penalty": 0.10
    },

    "checkpointing": {
      "checkpoint_on_fan_out": true,
      "checkpoint_on_fan_in": true,
      "worker_checkpoint_interval_minutes": 10
    },

    "mcts": {
      "exploration_constant": 1.41,
      "min_rollouts_per_branch": 5,
      "max_rollouts_per_branch": 20
    }
  }
}
```

---

## Quick Reference: Pattern Selection

| Situation | Pattern | Why |
|-----------|---------|-----|
| Explore unknown space fast | DPTS + BoT | Dynamic pruning, parallel breadth |
| Find optimal among known options | MCTS + ToT | Simulation-guided depth |
| Multi-source problem decomposition | BSM | Clean partition and merge |
| Need ensemble confidence | MoA or RASC | Multiple perspectives |
| Iterative refinement needed | GoT | Merge and cycle support |
| Test multiple hypotheses | Parallel HE | Independent evidence gathering |
| Cross-domain insights | MoA + AT | Multi-domain proposers |

---

## Summary

Parallel execution patterns provide 2-4x efficiency gains when applied appropriately:

1. **DPTS**: Dynamic worker allocation with adaptive pruning (best for ToT)
2. **BSM**: Decompose, parallel solve, merge (best for partitionable problems)
3. **MoA**: Layered proposer/aggregator (best for ensemble confidence)
4. **GoT**: Graph-structured reasoning with merge/cycle (best for iterative problems)
5. **RASC**: Rationalized self-consistency (best for reducing redundant computation)

**Key Integration Points:**
- BoT: Parallel branch exploration with static 40% pruning
- ToT: MCTS-style search with UCB1 selection
- HE: Parallel hypothesis testing with evidence synchronization
- AT: Multi-perspective investigation via MoA

**Critical Success Factors:**
- Verify task independence before parallelizing
- Define merge strategy before fan-out
- Use checkpoint integration for recovery
- Avoid parallelizing sequential dependencies
- Watch for diminishing returns with too many branches

**Reference**: See `reasoning-handover-protocol` for parallel branch merge protocol and checkpoint integration details.
