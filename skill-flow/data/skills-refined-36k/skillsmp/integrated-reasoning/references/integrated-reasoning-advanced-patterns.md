# Integrated Reasoning - Advanced Patterns

## Overview

This document provides advanced patterns for applying Integrated Reasoning methodology, including temporal enrichment, decision tree examples, multi-pattern orchestration strategies, and synthesis rules.

---

## Pattern 1: Temporal Enrichment Strategies

### When to Enrich

**Always enrich when**:
- Problem involves technology that evolves rapidly (AI/ML, cloud platforms, frameworks)
- Decision has long-term implications (architecture, technology stack)
- User explicitly mentions "latest" or "current" or "modern"
- Confidence requirement is >85% (current context critical)

**Can skip when**:
- Problem is purely mathematical or logical (2+2=4 doesn't change)
- Domain is stable and well-established (basic data structures, algorithms)
- User explicitly provides temporal context ("using React 18.2...")
- Very tight time constraints and low confidence requirement (<70%)

### Date-Aware Search Query Patterns

**Pattern**: Always include current year in searches for recent developments

```bash
# Current date check
date +"%Y-%m-%d"
# Output: 2025-11-06

# Good queries (date-aware)
WebSearch: "Python async best practices 2025"
WebSearch: "microservices architecture patterns 2025"
WebSearch: "Kubernetes optimization techniques 2025"
WebSearch: "distributed caching recent developments 2025"

# Avoid queries (no temporal context)
WebSearch: "Python async best practices"  # Might return 2018 articles
WebSearch: "microservices patterns"        # Could be outdated
```

**Why year matters**:
- Search engines prioritize recent content when year specified
- Avoids outdated best practices (React class components vs hooks)
- Captures breaking changes (Python 2 vs 3, Node 12 vs 20)
- Identifies deprecations (libraries, APIs, patterns)

### Multi-Source Research Strategy

**For technical problems**:
```markdown
1. Latest best practices:
   WebSearch: "[technology] best practices 2025"
   WebSearch: "[framework] performance optimization 2025"

2. Version-specific changes:
   WebSearch: "[library] version [X] breaking changes"
   WebFetch: [official documentation changelog]

3. Real-world experience:
   WebSearch: "[technology] lessons learned 2025"
   WebSearch: "[pattern] pitfalls avoid 2025"

Example (React state management):
- WebSearch: "React state management best practices 2025"
- WebSearch: "Redux vs Zustand vs Jotai 2025 comparison"
- WebFetch: https://react.dev/blog (official React blog)
- WebSearch: "React Server Components state management 2025"
```

**For architectural decisions**:
```markdown
1. Industry trends:
   WebSearch: "[domain] architecture trends 2025"
   WebSearch: "[industry] technology adoption 2025"

2. Comparative analysis:
   WebSearch: "[approach A] vs [approach B] 2025"
   WebSearch: "[pattern] pros cons 2025"

3. Case studies:
   WebSearch: "[company] [technology] migration case study"
   WebSearch: "[pattern] production experience 2025"

Example (Microservices vs Serverless):
- WebSearch: "microservices vs serverless 2025 comparison"
- WebSearch: "serverless architecture pitfalls 2025"
- WebSearch: "Netflix Uber microservices architecture 2025"
- WebFetch: AWS/Azure/GCP serverless best practices docs
```

**For novel/emerging technologies**:
```markdown
1. State of the art:
   WebSearch: "[technology] state of the art 2025"
   WebSearch: "[field] latest research 2025"

2. Maturity assessment:
   WebSearch: "[technology] production ready 2025"
   WebSearch: "[technology] adoption rate 2025"

3. Community consensus:
   WebSearch: "[technology] community feedback 2025"
   WebSearch: "[technology] reddit hackernews discussion"

Example (AI model deployment):
   - WebSearch: "LLM deployment best practices 2025"
   - WebSearch: "LLM inference optimization 2025"
   - WebSearch: "vLLM TensorRT-LLM comparison 2025"
   - WebFetch: HuggingFace deployment documentation
```

### Research Summary Template

```markdown
## Temporal Context Summary

**Analysis Date**: [YYYY-MM-DD]

**Recent Developments** (Past 6 months):
- [Development 1]: [1-2 sentence summary] - Relevance: [High/Medium/Low]
- [Development 2]: [summary] - Relevance: [H/M/L]
- [Development 3]: [summary] - Relevance: [H/M/L]

**Recent Developments** (6-12 months ago):
- [Development 4]: [summary] - Relevance: [H/M/L]

**Key Version Changes**:
- [Library/Framework]: [Old version] → [New version]
  - Breaking changes: [List]
  - New features: [List relevant to problem]
  - Deprecations: [What to avoid]

**Temporal Confidence Bonus**:
- Recent material found (<6mo): +5%
- Moderate recency (6-12mo): +3%
- Limited recent material: +0%

**How This Affects Analysis**:
[2-3 sentences explaining how recent developments change the solution approach]
```

---

## Pattern 2: Decision Tree Examples

### Example 1: Unknown Solution Space → Breadth-of-Thought

**Problem**: "We need a new caching strategy but unsure if Redis, Memcached, CDN, or something else is best"

**Classification**:
```
Q1: Is solution space known?
└─ NO → Many possible approaches (Redis, Memcached, Varnish, CDN, edge caching, etc.)

Q2: Multiple valid solutions?
└─ YES → Likely 3-5 viable options depending on constraints

Q5: Confidence requirement?
└─ >85% → Need thorough exploration

Decision: Use breadth-of-thought
- Explore 8-10 caching strategies exhaustively
- Conservative pruning (keep confidence >40%)
- Return top 3-5 viable solutions
- Cross-validate with recent caching research (2025)
```

### Example 2: Clear Criteria + Find Best → Tree-of-Thoughts

**Problem**: "Choose the optimal database for our analytics pipeline - criteria: <1s query latency, <$5k/month, scales to 10TB"

**Classification**:
```
Q1: Is solution space known?
└─ YES → Databases are well-known category

Q2: Clear evaluation criteria?
└─ YES → Latency <1s, Cost <$5k, Scale 10TB (very clear)

Q7: One best answer or multiple?
└─ ONE BEST → Find optimal solution meeting all criteria

Q5: Confidence requirement?
└─ >85% → Need high confidence in THE optimal choice

Decision: Use tree-of-thoughts
- Explore 5+ database options in parallel (Level 0)
- Evaluate each against 3 clear criteria
- Recursively explore best candidate (Levels 1-3)
- Return single optimal recommendation
- Enrich with recent database benchmarks (2025)
```

### Example 3: Sequential Dependencies → Self-Reflecting-Chain

**Problem**: "Debug why our distributed transaction is failing intermittently"

**Classification**:
```
Q3: Sequential reasoning required?
└─ YES → Debugging requires step-by-step trace (request → service A → service B → DB → failure)

Q6: Error correction needed?
└─ YES → May need to backtrack if initial hypothesis wrong

Q4: How many dimensions?
└─ 2-3 → Network, state consistency, timing (manageable for sequential)

Decision: Use self-reflecting-chain
- Step 1: Trace request flow
- Step 2: Identify state inconsistency point
- Step 3: Analyze race condition hypothesis
- Step 4: Validate with evidence
- Backtrack if any step confidence <60%
- Enrich with recent distributed systems debugging patterns (2025)
```

### Example 4: Multi-Dimensional + High Confidence → BoT + ToT

**Problem**: "Design microservices architecture balancing: latency, consistency, cost, team expertise, scalability, maintainability"

**Classification**:
```
Q4: How many dimensions?
└─ 6 dimensions → High complexity

Q5: Confidence requirement?
└─ >90% → High stakes decision

Q1: Solution space known?
└─ PARTIALLY → Many patterns exist but combination unclear

Decision: Use breadth-of-thought → tree-of-thoughts
- Phase 1 (BoT): Explore 8-10 architectural patterns across all 6 dimensions
- Phase 2 (Evaluation): Identify top 3 patterns from BoT
- Phase 3 (ToT): Deep recursive exploration of best pattern (4+ levels)
- Phase 4 (Synthesis): Combine BoT breadth insights with ToT depth optimization
- Enrich both with recent microservices patterns (2025)
```

### Example 5: Novel + High Stakes → All 3 Patterns

**Problem**: "We're building a never-done-before real-time collaborative ML model training system. Need >95% confidence in approach."

**Classification**:
```
Q1: Solution space known?
└─ NO → Novel problem, no established patterns

Q5: Confidence requirement?
└─ >95% → Maximum rigor needed

Q4: Dimensions?
└─ 8+ → ML training, real-time sync, collaboration, distributed compute, fault tolerance, consistency, latency, security

Decision: Use ALL THREE patterns (maximum orchestration)
- Phase 1 (BoT): Explore 10+ approaches to novel problem exhaustively
- Phase 2 (ToT): Deep dive on top 2 BoT solutions (find optimal)
- Phase 3 (SRC): Step-by-step validation of ToT winner
  - Step 1: Verify ML training requirements
  - Step 2: Validate real-time sync feasibility
  - Step 3: Check distributed compute assumptions
  - Backtrack if any step reveals flaw
- Phase 4 (Synthesis): Cross-validate all 3 patterns
  - If all agree → +15% confidence boost → >95% achieved
  - If disagree → Resolve with evidence → Document resolution
- Enrich all patterns with 2025 research: collaborative ML, real-time systems, distributed training
```

### Example 6: Simple Problem → No Orchestration Needed

**Problem**: "Should we use async/await or promises for this single API call?"

**Classification**:
```
Q4: How many dimensions?
└─ 1 dimension → Code style choice only

Q5: Confidence requirement?
└─ >70% → Low stakes decision

Decision: NO cognitive pattern orchestration needed
- This is too simple for integrated-reasoning
- Direct answer: "Use async/await (modern standard since 2017+)"
- No need for tree-of-thoughts, breadth-of-thought, or self-reflecting-chain
```

**Key Lesson**: Integrated-reasoning is for COMPLEX problems. Simple problems get direct answers, not orchestration overhead.

---

## Pattern 3: Orchestration Strategies

### Strategy 1: Sequential Orchestration (Unknown → Optimal → Validated)

**Best for**: Problems where solution space unknown, need to find best, and validate thoroughly

**Workflow**:
```markdown
Step 1: Breadth-of-Thought (Exploration)
├─ Goal: Explore 8-10 fundamentally different approaches
├─ Method: "Explore all viable [problem] solutions. Recent developments (2025): [temporal context]. Return top 3-5 with confidence scores."
├─ Output: 3-5 viable solutions (e.g., 78%, 75%, 72%, 68%, 65% confidence)
└─ Duration: ~15-20 min for BoT application

Step 2: Tree-of-Thoughts (Optimization)
├─ Input: Top solution from BoT (78% confidence solution)
├─ Goal: Recursively explore and optimize the 78% solution
├─ Method: "Given [BoT top solution], explore 5+ refinements (Level 0), evaluate, recurse 4+ levels deep. Recent context: [temporal]. Find optimal implementation."
├─ Output: Optimized solution (e.g., 88% confidence after 4 levels)
└─ Duration: ~20-25 min for ToT application

Step 3: Self-Reflecting-Chain (Validation)
├─ Input: ToT optimized solution (88% confidence)
├─ Goal: Step-by-step validation with backtracking
├─ Method: "Validate [ToT solution] step-by-step. Self-reflect after each step. Backtrack if confidence <60%. Recent constraints: [temporal]."
├─ Output: Validated solution (e.g., 92% confidence after verification)
└─ Duration: ~10-15 min for SRC application

Step 4: Final Synthesis (Bayesian)
├─ Combine insights: BoT found 5 viable → ToT optimized best → SRC validated
└─ Total Duration: ~45-60 min

Deliverable:
- Primary recommendation: [ToT optimized, SRC validated solution]
- Alternatives: [BoT runners-up: 75% and 72% solutions]
- Confidence: 90-95%
- Reasoning trace: BoT exploration → ToT optimization → SRC validation
```

**Example**: "Design distributed caching system balancing latency, consistency, cost, scalability"

**Sequential Execution**:
```markdown
BoT Output:
1. Redis Cluster (78%) - Low latency, eventually consistent, moderate cost
2. Memcached + DB (75%) - Very low latency, weak consistency, low cost
3. CDN + Origin (72%) - Variable latency, strong consistency, high cost
4. Varnish + Redis (68%) - Low latency, configurable consistency, moderate cost
5. Edge caching (65%) - Ultra-low latency, weak consistency, very high cost

ToT Input: Redis Cluster (78%)
ToT Exploration:
- Level 0: 5 Redis deployment patterns → Best: Multi-region active-active (82%)
- Level 1: 5 consistency strategies → Best: Conflict-free replicated data types (85%)
- Level 2: 5 cost optimization approaches → Best: Tiered hot/cold storage (87%)
- Level 3: 5 scaling patterns → Best: Auto-scaling with predictive load (88%)

SRC Input: Redis multi-region + CRDTs + tiered storage + auto-scaling (88%)
SRC Validation:
- Step 1: Verify latency requirements → <10ms ✅ (confidence: 90%)
- Step 2: Verify consistency model → CRDTs handle conflicts ✅ (confidence: 85%)
- Step 3: Verify cost constraints → Tiered storage within budget ✅ (confidence: 92%)
- Step 4: Verify scalability → Auto-scaling proven pattern ✅ (confidence: 90%)
- Step 5: Check operational complexity → Team has Redis expertise ✅ (confidence: 95%)
- Average: 90% → Final SRC: 92%

Final Synthesis:
- Primary: Redis multi-region + CRDTs + tiered storage + auto-scaling
- Alternatives: Memcached+DB (75%), CDN+Origin (72%)
- Confidence: 95% (capped, all patterns converged)
```

### Strategy 2: Parallel Orchestration (Independent Perspectives)

**Best for**: Problems where two different reasoning approaches provide complementary insights

**Workflow**:
```markdown
Parallel Application:

Thread 1: Tree-of-Thoughts
├─ Goal: Find THE optimal solution via deep recursion
├─ Method: "Explore 5+ approaches, evaluate, recurse to 4+ levels. Find best solution for [problem]. Context: [temporal]."
├─ Output: Single optimal solution (e.g., 87% confidence)
└─ Duration: ~20 min

Thread 2: Breadth-of-Thought (simultaneously)
├─ Goal: Find ALL viable solutions via wide search
├─ Method: "Explore 8-10 approaches, prune conservatively, return top 3-5 solutions for [problem]. Context: [temporal]."
├─ Output: Multiple viable solutions (e.g., 85%, 80%, 75% confidence)
└─ Duration: ~20 min

You apply BOTH simultaneously (~20 min total, not 40)

Cross-Pattern Analysis:
├─ Agreement Check:
│  - Does ToT winner appear in BoT top 3?
│    └─ YES → Strong validation → +15% confidence
│    └─ NO → Investigate discrepancy → Flag for resolution
│
├─ Coverage Check:
│  - Did BoT find viable alternatives ToT missed?
│    └─ YES → Document as alternatives → Valuable for fallback
│    └─ NO → ToT was comprehensive → Confidence boost
│
└─ Synthesis:
   - Primary: ToT winner (if in BoT top 3) OR Highest confidence (if disagreement)
   - Alternatives: BoT runners-up
   - Confidence: (ToT_conf + BoT_top_conf) / 2 + agreement_bonus

Deliverable:
- Primary: [ToT winner OR BoT top if higher confidence]
- Alternatives: [BoT top 3-5 solutions]
- Confidence: [Synthesized with agreement bonus]
- Reasoning trace: ToT deep exploration + BoT wide coverage
```

### Strategy 3: Hybrid Orchestration (Parallel → Sequential)

**Best for**: Maximum rigor when >95% confidence required and problem has 8+ dimensions

**Workflow**:
```markdown
Phase A: Parallel Exploration (20-25 min)

Thread 1: Breadth-of-Thought
├─ Explore 8-10 diverse approaches
└─ Output: Top 5 solutions (e.g., 82%, 78%, 75%, 72%, 68%)

Thread 2: Tree-of-Thoughts (parallel)
├─ Explore 5+ approaches, recurse 4+ levels
└─ Output: Single optimized solution (e.g., 88%)

Phase B: Convergence Analysis (5 min)

Compare BoT and ToT results:
├─ Full Agreement: Both recommend same solution
│  └─ Action: Proceed to validation (Phase C)
│
├─ Partial Agreement: ToT winner is in BoT top 3
│  └─ Action: Strong signal, proceed with high confidence
│
└─ Disagreement: ToT winner NOT in BoT top 5
   └─ Action: Investigate discrepancy → Proceed to conflict resolution (Phase C)

Phase C: Sequential Resolution/Validation (10-15 min)

If Agreement (ToT in BoT top 3):
└─ Self-Reflecting-Chain validates ToT winner step-by-step
   ├─ Step 1-5: Verify each dimension systematically
   ├─ Backtrack if any step confidence <60%
   └─ Output: Validated solution (e.g., 92%)

If Disagreement (ToT NOT in BoT top 5):
└─ Self-Reflecting-Chain analyzes discrepancy
   ├─ Step 1: Why did BoT rank [X] higher?
   ├─ Step 2: Why did ToT choose [Y] instead?
   ├─ Step 3: Which reasoning was more complete?
   ├─ Step 4: Resolve with evidence (not preference)
   └─ Output: Resolved recommendation with rationale

Phase D: Final Synthesis (5 min)

Confidence Calculation:
├─ Agreement path:
│  Base: SRC validated (92%)
│  Temporal: +5%
│  Agreement: +15% (BoT, ToT, SRC all converged)
│  Rigor: +10% (3 patterns)
│  Final: MIN(99, (92+5+15+10)) = 99% ✅
│
└─ Disagreement path:
   Base: MIN(BoT_top, ToT_winner) - 10 = 78%
   Temporal: +5%
   Agreement: +0% (patterns disagreed)
   Rigor: +10% (3 patterns used)
   Final: 93% (still high, but penalty for disagreement)

Total Duration: ~40-45 min for maximum rigor
```

### Strategy Selection Guidelines

**Use Sequential (BoT → ToT → SRC) when**:
- Solution space unknown
- Need to explore widely first, then optimize deeply
- Confidence requirement >90%
- Time available: 45-60 min

**Use Parallel (ToT + BoT) when**:
- Want independent reasoning perspectives
- Need both depth and breadth insights
- Confidence requirement >85%
- Time available: 20-25 min (faster than sequential)

**Use Hybrid (Parallel → Sequential) when**:
- Maximum rigor required (>95% confidence)
- High-stakes decision
- 8+ dimensions to optimize
- Time available: 40-50 min
- Willing to invest in thoroughness

**Use Single Pattern when**:
- Problem clearly fits one pattern's strengths
- Confidence requirement <85%
- Time constrained (<20 min)
- Solution space well-understood

---

## Summary

Integrated Reasoning orchestrates multiple cognitive patterns to achieve maximum confidence:

1. **Temporal Enrichment**: Research current trends before applying patterns
2. **Pattern Selection**: Use decision tree to choose optimal pattern(s)
3. **Orchestration**: Sequence or parallelize patterns based on problem complexity
4. **Synthesis**: Combine insights with agreement bonuses for final recommendation

Use these patterns to achieve >90% confidence on complex, high-stakes decisions.
