---
name: tree-of-thoughts
description: Advanced recursive reasoning methodology for systematic problem-solving. Use when you need to explore multiple solution approaches in parallel, evaluate them rigorously, and recursively deepen the best path. Ideal for complex decisions with trade-offs, optimization problems, or strategic planning. Example: "Should we use microservices or monolith?" → Apply ToT to spawn 5+ architectural approaches, evaluate each systematically, recurse on the winner.
license: MIT
---

# Tree of Thoughts Reasoning Methodology

**Purpose**: Systematic parallel exploration of solution spaces through recursive branching, self-reflection, and rigorous evaluation. Use this methodology when facing complex problems with multiple viable solution paths.

## When to Use Tree of Thoughts

**✅ Use ToT when:**
- Problem has multiple viable solution approaches (3+ fundamentally different paths)
- Need to find optimal solution, not just any solution
- Can define clear evaluation criteria
- Complexity justifies systematic exploration
- Trade-offs exist between competing approaches
- Strategic or architectural decisions with long-term impact

**❌ Don't use ToT when:**
- Problem has obvious single solution path
- Time-critical decisions with simple trade-offs
- Problem is well-defined with standard solution
- Exploratory work where breadth matters more than depth

**Examples**:
- "Should we use REST, GraphQL, or gRPC?" (3 paths, clear trade-offs) ✅
- "Design distributed caching system balancing latency, consistency, cost" (multi-dimensional) ✅
- "Fix this syntax error" (single path) ❌
- "Research all available databases" (breadth-of-thought better) ❌

---

## Core Methodology: 5-Step Process

### Step 1: Problem Decomposition (5+ Branches)

**Objective**: Identify 5+ fundamentally different approaches to explore

**Actions**:
1. Analyze problem to identify key dimensions (technical, organizational, risk, cost, timeline)
2. Brainstorm 5-10 distinct approaches (**not variations** of same approach)
3. Define evaluation criteria from problem constraints
4. Validate diversity: Each branch explores different solution philosophy

**Example** (Distributed Caching):
```
Branch A: Write-through consistency (strong consistency, higher latency)
Branch B: Eventual consistency (performance, weaker guarantees)
Branch C: Hybrid tiered (hot data write-through, cold data eventual)
Branch D: Edge-centric (CDN-style, geography-aware)
Branch E: Cost-optimized minimal (single region, no replication)
```

**Deliverable**: 5+ distinct approach definitions

---

### Step 2: Parallel Branch Exploration

**Objective**: Explore each branch systematically with self-reflection

**For each branch**:
1. Analyze approach against problem requirements
2. Consider strengths, weaknesses, trade-offs
3. Identify assumptions and constraints
4. End with self-reflection (see template below)

**Self-Reflection Template** (REQUIRED for each branch):
```markdown
## Branch [X]: [Approach Name]

[Analysis of this approach: 2-4 paragraphs covering requirements, strengths, weaknesses, trade-offs]

### Self-Reflection
- **Confidence**: [0-100]/100
- **Strengths**: [What makes this approach compelling]
- **Weaknesses**: [Gaps, assumptions, limitations]
- **Trade-offs**: [What you gain vs what you lose]
- **Recommendation**: [Continue deeper exploration? Prune? Why?]
```

**Execution Options**:
- **With Task tool**: Spawn 5+ parallel tasks for independent exploration
- **Without Task tool**: Explore branches sequentially using TodoWrite to track progress
- **Hybrid**: Use Task for complex branches, sequential for simple ones

**Deliverable**: 5+ explored branches with self-reflections

---

### Step 3: Branch Evaluation (Scoring)

**Objective**: Systematically evaluate all branches against criteria

**Evaluation Criteria** (100 points total, 5 categories × 20 points):

1. **Novelty** (0-20): Does it explore new solution space vs obvious approaches?
   - 18-20: Innovative approach, fresh perspective
   - 12-17: Good approach with some novel elements
   - 6-11: Standard approach, minor tweaks
   - 0-5: Obvious/conventional approach

2. **Feasibility** (0-20): Practically implementable with reasonable resources?
   - 18-20: Proven technology, clear implementation path
   - 12-17: Feasible with moderate effort/risk
   - 6-11: Significant technical challenges
   - 0-5: Impractical or resource-intensive

3. **Completeness** (0-20): Addresses all stated requirements?
   - 18-20: Covers all requirements comprehensively
   - 12-17: Covers most requirements, minor gaps
   - 6-11: Missing key requirements
   - 0-5: Incomplete solution

4. **Confidence** (0-20): Branch's self-reflection confidence score?
   - 18-20: High confidence (80-100%) with justification
   - 12-17: Medium confidence (60-79%)
   - 6-11: Low confidence (40-59%)
   - 0-5: Very low confidence (<40%)

5. **Alignment** (0-20): Matches problem constraints and context?
   - 18-20: Perfect fit for constraints
   - 12-17: Good fit, minor misalignment
   - 6-11: Notable misalignment
   - 0-5: Poor fit for context

**Scoring Process**:
1. Review each branch's analysis and self-reflection
2. Score each branch on all 5 criteria (0-20 per criterion)
3. Calculate total score (0-100) for each branch
4. Rank branches by total score
5. Select highest-scoring branch for deeper exploration

**Deliverable**: Scored ranking of all branches, winner selected

---

### Step 4: Recursive Depth Exploration (Level 1+)

**Objective**: Recursively expand the best branch

**Actions**:
1. Take highest-scoring branch from Step 3
2. Decompose that branch into 5+ sub-approaches or refinements
3. Repeat Steps 2-3 for the new level (explore → evaluate → select)
4. Continue recursion until stopping criteria met

**Minimum Depth**: 4 levels (Level 0 → 1 → 2 → 3)

**Level Transition Example**:
```
Level 0: "Distributed caching system" (5 approaches)
  → Winner: Branch B (Eventual consistency)

Level 1: "Eventual consistency variants" (5 refinements)
  - B.1: Last-write-wins
  - B.2: Version vectors
  - B.3: CRDTs
  - B.4: Causal consistency
  - B.5: Session consistency
  → Winner: Branch B.3 (CRDTs)

Level 2: "CRDT implementations" (5 options)
  - B.3.1: G-Counter
  - B.3.2: PN-Counter
  - B.3.3: LWW-Element-Set
  - B.3.4: OR-Set
  - B.3.5: RGA (Replicated Growable Array)
  → Winner: Branch B.3.4 (OR-Set)

Level 3: "OR-Set optimizations" (5 variants)
  [Explore specific implementation strategies]
  → Winner: Branch B.3.4.2 (Tombstone compaction)
```

**Deliverable**: Recursive tree with minimum 4 levels explored

---

### Step 5: Final Synthesis

**Objective**: Synthesize insights into final recommendation

**Actions**:
1. **Trace winning path**: Document Level 0 → Level 1 → Level 2 → Level 3+
2. **Extract key insights**: What was learned at each level?
3. **Document pruned branches**: Why were alternatives discarded?
4. **Calculate confidence**: Final confidence score (see Bayesian formula below)
5. **State assumptions**: What assumptions underpin the recommendation?
6. **Provide recommendation**: Clear, actionable guidance

**Synthesis Template**:
```markdown
## Tree of Thoughts Analysis Complete

### Winning Path
- **Level 0**: [Chosen approach] (Score: X/100)
- **Level 1**: [Refinement] (Score: X/100)
- **Level 2**: [Sub-refinement] (Score: X/100)
- **Level 3**: [Implementation] (Score: X/100)

### Key Insights
1. [Insight from Level 0]
2. [Insight from Level 1]
3. [Insight from Level 2]
4. [Insight from Level 3]

### Alternatives Considered
- [Branch A]: Pruned because [reason]
- [Branch C]: Pruned because [reason]
- [Branch D]: Pruned because [reason]

### Final Confidence: [X]%

**Justification**: [Why this confidence level based on exploration depth, evidence, and remaining uncertainties]

### Recommendation
[Clear, actionable recommendation with next steps]

### Remaining Uncertainties
- [Assumption 1]
- [Assumption 2]
```

**Deliverable**: Comprehensive synthesis with traced path and confidence score

---

## Stopping Criteria

**Stop exploration when ANY of:**
1. ✅ Reached 4+ levels AND best branch confidence >80%
2. ✅ Reached 6 levels (maximum recommended depth)
3. ✅ All branches converge to same solution across multiple levels
4. ✅ Diminishing returns (Level N scores similar to Level N-1)

**Warning signs** (don't stop yet):
- ❌ Only 2-3 levels explored
- ❌ Confidence <80% without clear reason
- ❌ Winner not clearly superior to alternatives

---

## Bayesian Confidence Scoring

**Purpose**: Quantify confidence based on accumulated evidence

**Formula**:
```
Prior Odds = P(correct) / (1 - P(correct))
Likelihood Ratio = Evidence strength (from scores)
Posterior Odds = Prior Odds × Likelihood Ratio
Final Confidence = Posterior Odds / (1 + Posterior Odds)
```

**Practical Calculation**:
1. Start with prior confidence: 50% (neutral)
2. For each evaluation criterion score (0-20):
   - Convert to likelihood ratio: `LR = 0.25 + (score/20) * 3.75`
   - Update odds: `Odds = Odds × LR`
3. Convert back to probability: `Conf = Odds / (1 + Odds)`
4. Cap at 95% (Bayesian humility for unknown unknowns)

**Example**:
- Branch scores: Novelty 18/20, Feasibility 19/20, Completeness 17/20, Confidence 18/20, Alignment 19/20
- Likelihood ratios: 3.62, 3.81, 3.44, 3.62, 3.81
- Final odds: 1.0 × 3.62 × 3.81 × 3.44 × 3.62 × 3.81 = 1,782
- Confidence: 1782 / 1783 = 99.9% → **Capped at 95%**

**Confidence Interpretation**:
- **90-95%**: Exceptional evidence, suitable for critical decisions
- **80-89%**: High confidence, suitable for important decisions
- **70-79%**: Medium confidence, consider additional validation
- **60-69%**: Low confidence, recommend further investigation
- **<60%**: Very low confidence, gather more information

---

## Self-Critique Checklist

After applying ToT methodology, verify:

- [ ] **Branch Diversity**: Are all 5+ branches fundamentally different (not variations)?
- [ ] **Self-Reflection Quality**: Does each branch have genuine self-reflection (not boilerplate)?
- [ ] **Evaluation Rigor**: Did I systematically score all 5 criteria for each branch?
- [ ] **Depth Achievement**: Did I reach minimum 4 levels of exploration?
- [ ] **Confidence Validity**: Is final confidence score justified by exploration depth?
- [ ] **Pruning Rationale**: Can I explain why each non-selected branch was discarded?
- [ ] **Path Traceability**: Can I clearly trace the winning path from root to leaf?
- [ ] **Synthesis Clarity**: Does final output provide actionable recommendation?
- [ ] **Stopping Appropriateness**: Did I stop for valid reasons per criteria?

---

## Common Mistakes to Avoid

1. **Too Few Branches**: Using <5 branches reduces exploration quality
2. **Variation vs Diversity**: Creating 5 variations of same approach instead of 5 different approaches
3. **Shallow Depth**: Stopping at 1-2 levels instead of minimum 4
4. **Biased Evaluation**: Favoring familiar approaches without systematic scoring
5. **Missing Self-Reflection**: Skipping confidence assessment in branches
6. **Premature Convergence**: Selecting winner before thorough evaluation
7. **Over-Recursion**: Going beyond 6 levels without clear benefit
8. **Poor Synthesis**: Not clearly documenting winning path and rationale

---

## Reference Documentation

**Detailed Templates**: `~/.claude/skills/tree-of-thoughts/references/tree-of-thoughts-patterns.md`

Includes:
- Branch exploration template (detailed prompts)
- Self-reflection rubric (confidence scoring guide)
- Evaluation matrix (scoring examples per criterion)
- Level transition logic (when/how to deepen)
- Edge case handling (convergence, insufficient diversity)

---

## Quick Start Examples

### Example 1: Simple Decision (3 levels)

**Problem**: Choose between Redis, Memcached, or Hazelcast for caching

**Level 0** (3 branches):
- Branch A: Redis (rich data structures)
- Branch B: Memcached (pure speed)
- Branch C: Hazelcast (distributed computing)
→ Winner: Branch A (Redis) - 85/100

**Level 1** (Redis deployment options):
- A.1: Single instance
- A.2: Sentinel (high availability)
- A.3: Cluster (horizontal scaling)
- A.4: Redis Enterprise
- A.5: Managed service (AWS ElastiCache)
→ Winner: Branch A.3 (Cluster) - 88/100

**Level 2** (Cluster configuration):
- A.3.1: 3 masters, no replicas
- A.3.2: 3 masters, 3 replicas
- A.3.3: 6 masters, 6 replicas
- A.3.4: Auto-scaling cluster
- A.3.5: Hybrid (critical data replicated)
→ Winner: Branch A.3.2 (3+3) - 91/100

**Confidence**: 88% (3 levels, clear winner at each level)

### Example 2: Complex Architecture (5 levels)

**Problem**: Design microservices communication strategy

**Level 0**: REST, gRPC, Message Queue, Event Sourcing, GraphQL (5 approaches)
**Level 1**: [Winner] expanded into 5 sub-approaches
**Level 2**: [Winner] expanded into 5 implementation variants
**Level 3**: [Winner] expanded into 5 technology choices
**Level 4**: [Winner] expanded into 5 deployment patterns

**Confidence**: 93% (5 levels, 25+ branches explored total)

---

## Summary

Tree of Thoughts is a **systematic methodology** for exploring complex problem spaces through:
1. **Parallel branching** (5+ approaches per level)
2. **Self-reflection** (confidence scoring for each branch)
3. **Rigorous evaluation** (5 criteria, 0-100 scoring)
4. **Recursive depth** (minimum 4 levels)
5. **Bayesian confidence** (evidence-based scoring)

Use it for strategic decisions, architectural choices, and optimization problems where systematic exploration yields better outcomes than intuition alone.

**Remember**: Quality over speed. ToT trades time for rigor. The goal is high-confidence optimal solutions, not quick answers.
