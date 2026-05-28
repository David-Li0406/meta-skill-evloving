# Advanced Parallel Execution Patterns

Deep-dive reference for parallel execution patterns, including detailed algorithms, integration examples, and advanced configuration.

## Part 1: DPTS Algorithm Details

### Dynamic Pruning Threshold Algorithm

```python
def calculate_dynamic_threshold(branches, margin=0.30, floor=0.40):
    """
    Calculate dynamic pruning threshold based on best-found confidence.

    Args:
        branches: List of (branch_id, confidence) tuples
        margin: How much below best is acceptable (default 0.30)
        floor: Minimum threshold regardless of best (default 0.40)

    Returns:
        float: Pruning threshold
    """
    if not branches:
        return floor

    best_confidence = max(conf for _, conf in branches)
    dynamic = best_confidence - margin

    return max(dynamic, floor)

# Example:
# branches = [("A", 0.82), ("B", 0.71), ("C", 0.55), ("D", 0.42)]
# threshold = max(0.82 - 0.30, 0.40) = max(0.52, 0.40) = 0.52
# Result: D pruned (0.42 < 0.52), A, B, C retained
```

### Worker Reallocation Strategy

```python
def reallocate_workers(branches, total_workers, min_per_branch=1):
    """
    Allocate workers proportionally to branch confidence.

    Args:
        branches: List of (branch_id, confidence) tuples
        total_workers: Total workers available
        min_per_branch: Minimum workers per retained branch

    Returns:
        dict: {branch_id: worker_count}
    """
    # Filter by threshold first
    threshold = calculate_dynamic_threshold(branches)
    retained = [(bid, conf) for bid, conf in branches if conf >= threshold]

    if not retained:
        return {}

    # Ensure minimum per branch
    base_allocation = {bid: min_per_branch for bid, _ in retained}
    remaining = total_workers - (len(retained) * min_per_branch)

    if remaining <= 0:
        return base_allocation

    # Allocate remaining proportionally
    total_conf = sum(conf for _, conf in retained)
    for bid, conf in retained:
        extra = int((conf / total_conf) * remaining)
        base_allocation[bid] += extra

    return base_allocation

# Example:
# branches = [("A", 0.82), ("B", 0.71), ("C", 0.55)]
# total_workers = 10, min_per_branch = 1
# retained: all 3 (threshold = 0.52)
# base: {"A": 1, "B": 1, "C": 1}, remaining = 7
# proportional: A gets 3 extra, B gets 2 extra, C gets 2 extra
# final: {"A": 4, "B": 3, "C": 3}
```

---

## Part 2: MCTS for ToT - Detailed Implementation

### UCB1 Selection

```python
import math

def ucb1_select(branches, exploration_constant=1.41):
    """
    Select branch using UCB1 formula for exploration/exploitation balance.

    Args:
        branches: List of dicts with 'id', 'avg_score', 'visits', 'total_visits'
        exploration_constant: C value in UCB1 (default sqrt(2))

    Returns:
        str: Selected branch ID
    """
    best_ucb = -float('inf')
    best_branch = None

    for branch in branches:
        if branch['visits'] == 0:
            # Unvisited branches have infinite priority
            return branch['id']

        exploitation = branch['avg_score']
        exploration = exploration_constant * math.sqrt(
            math.log(branch['total_visits']) / branch['visits']
        )
        ucb = exploitation + exploration

        if ucb > best_ucb:
            best_ucb = ucb
            best_branch = branch['id']

    return best_branch
```

### Parallel MCTS Rollout

```markdown
## Parallel MCTS Execution

### Round 1: Initial Exploration (All branches equal)
Spawn 1 rollout per branch (5 branches = 5 parallel rollouts)
├─ Branch A: rollout → score 72
├─ Branch B: rollout → score 68
├─ Branch C: rollout → score 81
├─ Branch D: rollout → score 55
└─ Branch E: rollout → score 63

### Round 2: UCB1 Selection
UCB1 scores (after 5 total rollouts each):
├─ A: 72 + 1.41 × sqrt(ln(5)/1) = 72 + 1.79 = 73.79
├─ B: 68 + 1.41 × sqrt(ln(5)/1) = 68 + 1.79 = 69.79
├─ C: 81 + 1.41 × sqrt(ln(5)/1) = 81 + 1.79 = 82.79 ← Best
├─ D: 55 + 1.41 × sqrt(ln(5)/1) = 55 + 1.79 = 56.79
└─ E: 63 + 1.41 × sqrt(ln(5)/1) = 63 + 1.79 = 64.79

Allocate 5 more rollouts based on UCB1:
├─ C: 2 rollouts (highest UCB)
├─ A: 1 rollout
├─ B: 1 rollout
└─ E: 1 rollout
(D skipped - too low)

### Round 3+: Iterative Refinement
Continue until:
- Total rollouts ≥ 50, OR
- Best branch has 2x more visits than second-best
```

---

## Part 3: MoA Advanced Configuration

### Multi-Layer MoA Architecture

```markdown
## 3-Layer MoA for Complex Problems

### Layer 0: Problem Decomposition
Input: Complex problem statement
Output: Sub-problem specifications

### Layer 1: Specialized Proposers
┌─────────────────────────────────────────────────────────────────┐
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐           │
│  │ ToT     │  │ BoT     │  │ HE      │  │ AT      │           │
│  │Proposer │  │Proposer │  │Proposer │  │Proposer │           │
│  │         │  │         │  │         │  │         │           │
│  │ Focus:  │  │ Focus:  │  │ Focus:  │  │ Focus:  │           │
│  │Optimal  │  │Options  │  │Diagnosis│  │Analogy  │           │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘           │
│       │            │            │            │                 │
│       └────────────┴────────────┴────────────┘                 │
│                          │                                      │
└──────────────────────────┼──────────────────────────────────────┘
                           ▼
### Layer 2: Domain Aggregators
┌─────────────────────────────────────────────────────────────────┐
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Technical    │  │ Business     │  │ Risk         │          │
│  │ Aggregator   │  │ Aggregator   │  │ Aggregator   │          │
│  │              │  │              │  │              │          │
│  │ Synthesizes: │  │ Synthesizes: │  │ Synthesizes: │          │
│  │ - Feasibility│  │ - Cost/ROI   │  │ - Security   │          │
│  │ - Performance│  │ - Timeline   │  │ - Compliance │          │
│  │ - Scalability│  │ - Resources  │  │ - Reliability│          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                 │                   │
│         └─────────────────┼─────────────────┘                   │
│                           │                                     │
└───────────────────────────┼─────────────────────────────────────┘
                            ▼
### Layer 3: Executive Synthesizer
┌─────────────────────────────────────────────────────────────────┐
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                 Executive Synthesizer                      │   │
│  │                                                            │   │
│  │  - Resolves cross-domain conflicts                        │   │
│  │  - Applies stakeholder weights                            │   │
│  │  - Generates final recommendation                         │   │
│  │  - Documents confidence and rationale                     │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Aggregator Conflict Resolution

```markdown
## Conflict Resolution Strategies

### Strategy 1: Weighted Voting
When: Proposers disagree on conclusion

Process:
1. Assign weights based on domain relevance
2. Calculate weighted vote
3. Document minority position

Example:
- ToT: "Use PostgreSQL" (weight 3, optimization-focused problem)
- BoT: "Use MongoDB" (weight 2)
- AT: "Use PostgreSQL" (weight 2, banking analogy)

Vote: PostgreSQL = 3+2 = 5, MongoDB = 2
Winner: PostgreSQL (71% weighted)

### Strategy 2: Dialectical Resolution
When: Both positions are valid for different contexts

Process:
1. Identify when each position is correct
2. Create contextual recommendation
3. Document trade-offs

Example:
- Position A: "Microservices for scalability"
- Position B: "Monolith for simplicity"

Resolution: "Start monolith (simplicity for MVP), plan migration to
microservices when team size exceeds 10 and traffic exceeds 1M requests/day"

### Strategy 3: Escalation
When: Disagreement reveals fundamental uncertainty

Process:
1. Document the disagreement
2. Identify additional evidence needed
3. Recommend gathering more information before deciding
```

---

## Part 4: GoT Implementation Patterns

### Graph State Management

```json
{
  "got_session": {
    "id": "got-session-001",
    "nodes": [
      {
        "id": "N1",
        "type": "problem",
        "content": "Design caching strategy",
        "confidence": 1.0,
        "status": "completed"
      },
      {
        "id": "N2",
        "type": "branch",
        "parent": "N1",
        "content": "Write-through approach",
        "confidence": 0.72,
        "status": "completed"
      },
      {
        "id": "N3",
        "type": "branch",
        "parent": "N1",
        "content": "Write-behind approach",
        "confidence": 0.68,
        "status": "completed"
      },
      {
        "id": "N4",
        "type": "merge",
        "parents": ["N2", "N3"],
        "content": "Hybrid: Write-through for hot data, write-behind for cold",
        "confidence": 0.81,
        "status": "completed"
      },
      {
        "id": "N5",
        "type": "refine",
        "parent": "N4",
        "content": "Add TTL-based hot/cold classification",
        "confidence": 0.85,
        "status": "active"
      }
    ],
    "edges": [
      {"from": "N1", "to": "N2", "type": "branch"},
      {"from": "N1", "to": "N3", "type": "branch"},
      {"from": "N2", "to": "N4", "type": "merge"},
      {"from": "N3", "to": "N4", "type": "merge"},
      {"from": "N4", "to": "N5", "type": "refine"}
    ],
    "current_node": "N5"
  }
}
```

### GoT Operations

```markdown
## Branch Operation
Create N new nodes from one parent.

Input: parent_node, branch_count
Output: N new nodes, N new edges

Rules:
- All branches are independent
- Each branch explores different direction
- Branches can be parallelized

## Merge Operation
Combine M nodes into one synthesized node.

Input: parent_nodes[], merge_strategy
Output: 1 new node, M new edges

Strategies:
- UNION: Include elements from all parents
- INTERSECT: Only common elements
- SYNTHESIZE: Create new insight from combination
- SELECT_BEST: Keep highest-confidence parent content

## Refine Operation
Improve a node through iteration.

Input: parent_node, refinement_instruction
Output: 1 new node, 1 new edge

Rules:
- Refinement must improve confidence
- Max 3 refinements on same lineage
- Document what changed

## Backtrack Operation
Return to earlier node when current path fails.

Input: from_node, to_node, reason
Output: to_node becomes active, from_node marked "abandoned"

Rules:
- Must document why backtracking
- Can backtrack to any ancestor
- Abandoned nodes may be revisited

## Cycle Operation
Re-evaluate a node with new information.

Input: node, new_information
Output: Updated node (same ID, new version)

Rules:
- Max 2 cycles on same node
- Must document what new information triggered cycle
- Confidence can go up or down
```

---

## Part 5: RASC Clustering Algorithm

### Rationale Similarity Computation

```python
def compute_rationale_similarity(rationale_a, rationale_b):
    """
    Compute similarity between two rationales using key concept overlap.

    Args:
        rationale_a, rationale_b: String rationales

    Returns:
        float: Similarity score (0-1)
    """
    # Extract key concepts (simplified - real implementation uses NLP)
    concepts_a = extract_key_concepts(rationale_a)
    concepts_b = extract_key_concepts(rationale_b)

    # Jaccard similarity
    intersection = len(concepts_a & concepts_b)
    union = len(concepts_a | concepts_b)

    return intersection / union if union > 0 else 0

def cluster_rationales(paths, similarity_threshold=0.6):
    """
    Cluster paths by rationale similarity.

    Args:
        paths: List of dicts with 'id', 'answer', 'rationale'
        similarity_threshold: Minimum similarity for same cluster

    Returns:
        List of clusters, each cluster is list of path dicts
    """
    clusters = []

    for path in paths:
        matched = False
        for cluster in clusters:
            # Check similarity with cluster representative
            representative = cluster[0]
            similarity = compute_rationale_similarity(
                path['rationale'],
                representative['rationale']
            )
            if similarity >= similarity_threshold:
                cluster.append(path)
                matched = True
                break

        if not matched:
            # Create new cluster
            clusters.append([path])

    return clusters
```

### RASC Aggregation

```markdown
## RASC Full Example

### Input: 10 reasoning paths for "Best programming language for web backend"

Path 1: Python - "rapid development, large ecosystem"
Path 2: JavaScript - "full-stack, single language"
Path 3: Python - "rapid development, ML integration"
Path 4: Go - "performance, concurrency"
Path 5: Python - "rapid development, readability"
Path 6: JavaScript - "isomorphic code, npm"
Path 7: Java - "enterprise support, stability"
Path 8: Go - "simplicity, performance"
Path 9: Python - "rapid development, Django"
Path 10: TypeScript - "type safety, JavaScript superset"

### Clustering (threshold = 0.6)

Cluster 1: "rapid development" rationale
- Path 1, 3, 5, 9 → Representative: Path 1 (Python)
- Size: 4

Cluster 2: "full-stack JavaScript" rationale
- Path 2, 6 → Representative: Path 2 (JavaScript)
- Size: 2

Cluster 3: "performance/concurrency" rationale
- Path 4, 8 → Representative: Path 4 (Go)
- Size: 2

Cluster 4: "enterprise/stability" rationale
- Path 7 → Representative: Path 7 (Java)
- Size: 1

Cluster 5: "type safety" rationale
- Path 10 → Representative: Path 10 (TypeScript)
- Size: 1

### Weighted Aggregation

Total weight: 4 + 2 + 2 + 1 + 1 = 10

Python: 4/10 = 40% (from rapid development cluster)
JavaScript: 2/10 = 20%
Go: 2/10 = 20%
Java: 1/10 = 10%
TypeScript: 1/10 = 10%

### Final Result

Winner: Python (40% weighted consensus)
Confidence: 40% (moderate - no strong majority)
Key Rationale: "Rapid development with large ecosystem"
Alternative: Go or JavaScript for performance or full-stack needs
```

---

## Part 6: Handover Protocol Integration

### Parallel Session State

```json
{
  "$schema": "parallel-session-v1",
  "session_id": "parallel-001",
  "timestamp": "2026-01-18T14:30:00Z",

  "parallel_config": {
    "pattern": "BSM",
    "max_workers": 8,
    "timeout_minutes": 30,
    "merge_strategy": "weighted_voting"
  },

  "fan_out_state": {
    "total_tasks": 5,
    "task_specs": [
      {"id": "task-1", "description": "Evaluate PostgreSQL", "pattern": "ToT"},
      {"id": "task-2", "description": "Evaluate MongoDB", "pattern": "ToT"},
      {"id": "task-3", "description": "Evaluate DynamoDB", "pattern": "ToT"},
      {"id": "task-4", "description": "Evaluate Redis", "pattern": "ToT"},
      {"id": "task-5", "description": "Evaluate Cassandra", "pattern": "ToT"}
    ]
  },

  "worker_states": {
    "task-1": {"status": "completed", "result": {"score": 87, "confidence": 0.82}},
    "task-2": {"status": "completed", "result": {"score": 71, "confidence": 0.75}},
    "task-3": {"status": "running", "progress": "Level 2"},
    "task-4": {"status": "completed", "result": {"score": 68, "confidence": 0.71}},
    "task-5": {"status": "failed", "error": "Timeout at Level 1"}
  },

  "fan_in_state": {
    "status": "waiting",
    "completed_count": 3,
    "pending_count": 1,
    "failed_count": 1,
    "merge_ready": false
  }
}
```

### Recovery Procedure

```markdown
## Recovery from Parallel Execution Failure

### Step 1: Load Checkpoint
Load parallel session state from:
.reasoning/session-{id}/parallel/worker-status.json

### Step 2: Analyze Worker States
- Completed: Results available, no action needed
- Running: May need timeout extension or manual check
- Failed: Decide retry/skip/abort
- Pending: Resume spawning

### Step 3: Handle Failed Workers

Option A - Retry:
1. Reset worker state to "pending"
2. Re-spawn with same specification
3. Extend timeout if timeout-related failure

Option B - Skip:
1. Mark as "skipped"
2. Proceed with partial results
3. Note reduced coverage in confidence

Option C - Abort:
1. Cancel all pending/running workers
2. Return best partial results
3. Document why abort was necessary

### Step 4: Resume Fan-In
When completed_count >= minimum_required:
1. Collect completed results
2. Apply merge strategy
3. Document skipped/failed contributions
4. Adjust confidence based on coverage
```

---

## Part 7: Performance Benchmarks

### Expected Speedup by Pattern

| Pattern | Sequential Time | Parallel Time | Speedup | Notes |
|---------|-----------------|---------------|---------|-------|
| BoT L0 (8 approaches) | 40 min | 10 min | 4x | Embarrassingly parallel |
| ToT L0-L1 (5 branches each) | 50 min | 20 min | 2.5x | Some sync needed |
| HE (10 hypotheses) | 30 min | 12 min | 2.5x | Evidence sync points |
| DPTS + ToT | 60 min | 18 min | 3.3x | Dynamic reallocation |
| MoA (4 proposers) | 45 min | 15 min | 3x | Aggregation overhead |
| RASC (10 paths) | 50 min | 8 min | 6x | Clustering reduces work |

### Overhead Considerations

| Overhead Type | Cost | Mitigation |
|---------------|------|------------|
| Task spawning | ~5 sec per task | Batch spawn |
| State serialization | ~2 sec per checkpoint | Checkpoint less frequently |
| Fan-in merge | ~10 sec per 5 results | Streaming merge |
| Worker communication | ~1 sec per message | Batch updates |

### When Parallel is NOT Faster

- Very small tasks (< 1 min): Overhead exceeds benefit
- Highly sequential problems: No parallelism available
- Resource-constrained environment: Context switching costs
- Single-threaded evidence: When evidence must be gathered serially

---

## Part 8: Advanced Configuration Examples

### High-Confidence Configuration (Critical Decisions)

```json
{
  "profile": "high-confidence",
  "description": "Maximum rigor, ensemble validation",

  "moa_config": {
    "proposers": ["ToT", "BoT", "AT", "HE"],
    "aggregation": "unanimous_required",
    "confidence_boost_on_agreement": 0.10,
    "disagreement_handling": "escalate_to_DR"
  },

  "rasc_config": {
    "paths": 20,
    "similarity_threshold": 0.7,
    "min_cluster_representation": 3
  },

  "pruning": {
    "enabled": false,
    "reason": "Keep all options for maximum coverage"
  },

  "checkpointing": {
    "interval_minutes": 5,
    "full_state": true
  }
}
```

### Fast-Iteration Configuration (Prototyping)

```json
{
  "profile": "fast-iteration",
  "description": "Speed over completeness",

  "dpts_config": {
    "initial_branches": 3,
    "max_depth": 2,
    "aggressive_pruning": true,
    "threshold": 0.50
  },

  "workers": {
    "max": 5,
    "timeout_minutes": 10
  },

  "early_termination": {
    "confidence_threshold": 0.70,
    "enabled": true
  },

  "checkpointing": {
    "enabled": false,
    "reason": "Speed over recoverability"
  }
}
```

### Balanced Configuration (Default)

```json
{
  "profile": "balanced",
  "description": "Good trade-off between speed and rigor",

  "parallel_config": {
    "max_workers": 8,
    "timeout_minutes": 30
  },

  "pruning": {
    "bot_threshold": 0.40,
    "dpts_margin": 0.30,
    "min_to_retain": 3
  },

  "merge_strategy": "weighted_voting",

  "checkpointing": {
    "interval_minutes": 15,
    "on_handover": true
  }
}
```
