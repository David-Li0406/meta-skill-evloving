---
name: breadth-of-thought
description: Exhaustive solution space exploration methodology. Use when solution space is unknown, you need multiple viable options (not just one best), or can't afford to miss alternatives. Explores 8-10 approaches in parallel at each level, prunes conservatively (keep above 40% confidence), returns 3-5 viable solutions. Example - data pipeline options - Apply BoT to explore all architectures exhaustively.
license: MIT
---

# Breadth of Thought Reasoning Methodology

**Purpose**: Exhaustive exploration of solution spaces through systematic parallel breadth-first reasoning. Maintains multiple hypotheses, explores diverse approaches, and returns 3-5 viable solutions instead of prematurely converging on one.

## When to Use Breadth of Thought

**✅ Use BoT when:**
- **Unknown solution space** (you don't know what you don't know)
- **Multiple valid solutions needed** (need 3-5 good options, not just 1 best)
- **High-stakes decisions** (can't afford to miss viable alternatives)
- **Novel problems** (no clear best practice exists)
- **Debugging complex issues** (multiple potential root causes)
- **Comprehensive planning** (need to evaluate ALL options before deciding)

**❌ Don't use BoT when:**
- Clear evaluation criteria exist and you need THE single best solution → Use tree-of-thoughts
- Problem requires deep sequential reasoning with dependencies → Use self-reflecting-chain
- Single obvious approach exists → Solve directly
- Time-critical with simple trade-offs → Quick analysis sufficient

**Examples**:
- "Redesign data pipeline: batch, streaming, hybrid, or other?" (unknown space) ✅
- "System crashes intermittently: network, DB, memory, race, or config?" (multiple causes) ✅
- "Choose caching strategy: write-through, eventual, hybrid?" (clear criteria - use ToT) ❌
- "Fix syntax error" (obvious solution) ❌

---

## Breadth vs Depth Comparison

| Dimension | **Breadth of Thought** | **Tree of Thoughts** |
|-----------|----------------------|---------------------|
| **Exploration** | Wide: 8-10 branches per level | Deep: 5 branches → 1 best |
| **Pruning** | Conservative: Keep >40% | Aggressive: Keep top 1-2 |
| **Levels** | Shallow: 2-3 levels | Deep: 4-6 levels |
| **Output** | 3-5 viable solutions | 1 optimal solution |
| **Use when** | Solution space unknown | Evaluation criteria clear |
| **Total exploration** | 50-100 branches | 25-40 branches |
| **Philosophy** | "Don't miss anything" | "Find the best" |

---

## Core Methodology: 4-Step Process

### Step 1: Solution Space Mapping (8-10 Approaches)

**Objective**: Identify 8-10 fundamentally distinct approaches

**Actions**:
1. Analyze problem from multiple perspectives:
   - **Technical**: Different technologies, architectures, patterns
   - **Business**: Different cost models, value propositions
   - **Organizational**: Different team structures, processes
   - **Risk**: Conservative vs innovative approaches
   - **Timeline**: Quick wins vs long-term solutions

2. Generate 8-10 distinct approaches (not variations)
3. For each approach, create brief description and viability estimate
4. **Do NOT prune yet** - explore all in parallel

**Approach Diversity Requirement**:
- ❌ **Variations**: "Use PostgreSQL" vs "Use MySQL" (both relational)
- ✅ **Distinct**: "Relational DB" vs "Document store" vs "Event sourcing" vs "In-memory cache"

**Example** (Data Pipeline):
```
1. **Batch processing** (traditional ETL)
2. **Real-time streaming** (Kafka/Flink)
3. **Micro-batch** (Spark Structured Streaming)
4. **Lambda architecture** (batch + stream hybrid)
5. **Kappa architecture** (stream-only)
6. **Event sourcing** (immutable log)
7. **Change data capture** (DB triggers)
8. **Serverless functions** (FaaS on events)
```

**Deliverable**: 8-10 distinct approaches ready for parallel exploration

---

### Step 2: Level 0 Breadth Exploration (Parallel)

**Objective**: Explore EACH approach in depth with self-reflection

**For each of 8-10 approaches**:
1. Research the approach comprehensively
2. Analyze strengths, weaknesses, constraints
3. Identify use cases where it excels vs struggles
4. Estimate feasibility, complexity, risk
5. Rate confidence (0-100%) in viability
6. Document trade-offs and assumptions

**Exploration Template** (per approach):
```markdown
## Approach [N]: [Name]

### Overview
[2-3 sentence description]

### Strengths
- [Strength 1]
- [Strength 2]
- [Strength 3]

### Weaknesses
- [Weakness 1]
- [Weakness 2]
- [Weakness 3]

### Use Cases
- **Excels when**: [Scenario where this is optimal]
- **Struggles when**: [Scenario where this is problematic]

### Feasibility Assessment
- **Technical**: [Complexity, maturity, team expertise]
- **Operational**: [Maintenance, monitoring, scaling]
- **Business**: [Cost, time-to-market, ROI]

### Confidence: [0-100]%

**Rationale**: [Why this confidence level]

### Key Assumptions
- [Assumption 1]
- [Assumption 2]
```

**Execution Options**:
- **With Task tool**: Spawn 8-10 parallel tasks for independent exploration
- **Without Task tool**: Explore sequentially, using TodoWrite to track progress
- **Hybrid**: Use Task for complex approaches, sequential for simpler ones

**Deliverable**: 8-10 explored approaches with confidence scores

---

### Step 3: Conservative Pruning (Keep >40%)

**Objective**: Evaluate all branches and prune ONLY the clearly non-viable

**Pruning Philosophy**: Breadth of Thought is **conservative** - we keep branches that might work, even if not optimal. Only prune if confidence <40% AND fatal blocker exists.

**Actions**:
1. Review all Level 0 explorations
2. Score each approach:
   - **Feasibility**: Technical, operational, business viability
   - **Completeness**: How thoroughly was it explored?
   - **Risk vs Reward**: What's the upside/downside balance?
3. **Prune ONLY if**:
   - Confidence <40% **AND**
   - Fatal technical blocker identified **AND**
   - No mitigating strategies possible
4. For retained branches (typically 5-7), document why kept
5. Rank retained branches for Level 1 expansion

**Pruning Examples**:

**✅ Keep** (50% confidence):
- Approach is technically feasible but has implementation challenges
- Team lacks expertise but can hire/learn
- Cost is high but ROI justifies it
- **Reason**: Viable with mitigation, worth exploring deeper

**❌ Prune** (35% confidence):
- Approach requires technology that doesn't exist yet
- Violates hard constraint (e.g., regulatory compliance impossible)
- Cost exceeds budget by 10x with no path to reduce
- **Reason**: Fundamentally not viable, no mitigating strategies

**Typical Outcome**: Prune 2-3 approaches, retain 5-7 for Level 1

**Deliverable**: 5-7 retained approaches ranked by viability

---

### Step 4: Level 1+ Expansion (5 Sub-Approaches Each)

**Objective**: For each retained approach, explore 5 variations/implementations

**Actions**:
1. Take each of the 5-7 retained approaches from Step 3
2. For each approach, identify 5 sub-approaches (variations, implementations, configurations)
3. Explore each sub-approach (same depth as Level 0)
4. Evaluate and prune conservatively (keep >40%)
5. **(Optional) Level 2**: If time allows and depth needed, repeat for top branches

**Level 1 Decomposition** (per retained approach):
```markdown
## Level 1: Expanding Approach [N]

### Sub-Approach [N].1: [Variation 1]
[Exploration...]

### Sub-Approach [N].2: [Variation 2]
[Exploration...]

### Sub-Approach [N].3: [Variation 3]
[Exploration...]

### Sub-Approach [N].4: [Variation 4]
[Exploration...]

### Sub-Approach [N].5: [Variation 5]
[Exploration...]
```

**Example** (Expanding "Real-time Streaming"):
```
Approach 2: Real-time Streaming
├─ 2.1: Kafka + Flink
├─ 2.2: Kafka + Spark Streaming
├─ 2.3: AWS Kinesis + Lambda
├─ 2.4: Pulsar + custom processors
└─ 2.5: Redis Streams + Node.js workers
```

**Stopping Criteria**:
- **After Level 1**: If you have 10-15 viable sub-approaches (sufficient breadth)
- **Continue to Level 2**: If approaches still too abstract, need implementation details
- **Maximum Depth**: 3 levels (breadth over depth philosophy)

**Deliverable**: 10-20 viable solutions across all expanded approaches

---

## Final Synthesis: Return Top 3-5 Solutions

**Objective**: Synthesize exploration into actionable recommendations

**Actions**:
1. Review ALL explored branches (Level 0 + Level 1 + Level 2)
2. Identify top 10-15 branches by confidence score
3. Group similar approaches together
4. Select **top 3-5 distinct solutions** representing different trade-off profiles
5. For each selected solution, document:
   - Full path (e.g., Approach 2 → Sub-approach 2.3)
   - Confidence score and rationale
   - Key strengths and weaknesses
   - Best use case
   - Implementation considerations

**Synthesis Template**:
```markdown
## Breadth of Thought Analysis Complete

### Total Exploration
- **Level 0**: 8 approaches explored → 6 retained
- **Level 1**: 30 sub-approaches explored → 12 retained
- **Total branches analyzed**: 38
- **Time**: [X] minutes

### Top 5 Viable Solutions

#### Solution 1: [Name] (Confidence: [X]%)
- **Path**: Approach [N] → Sub-approach [N.M]
- **Best for**: [Use case where this excels]
- **Strengths**: [Key strengths]
- **Weaknesses**: [Key weaknesses]
- **Implementation**: [Complexity, timeline, resources]

#### Solution 2: [Name] (Confidence: [X]%)
[Same structure...]

#### Solution 3: [Name] (Confidence: [X]%)
[Same structure...]

#### Solution 4: [Name] (Confidence: [X]%)
[Same structure...]

#### Solution 5: [Name] (Confidence: [X]%)
[Same structure...]

### Trade-Off Analysis

**If you prioritize [X]**, choose **Solution [N]**
**If you prioritize [Y]**, choose **Solution [M]**
**If you prioritize [Z]**, choose **Solution [P]**

### Recommendation

Based on [stated priorities/constraints], I recommend:
1. **Primary**: Solution [N] ([X]% confidence)
2. **Alternative**: Solution [M] ([X]% confidence) if [condition]
3. **Backup**: Solution [P] ([X]% confidence) if [condition]

### Branches Not Explored

Due to time/scope constraints, the following were not explored:
- [Potential approach 1]
- [Potential approach 2]

These could be investigated if none of the top 5 solutions work out.
```

**Deliverable**: 3-5 viable solutions with clear trade-off analysis

---

## Resource Management

**Time Budget** (if resource-constrained):
- Level 0: 15-20 minutes (8-10 approaches)
- Level 1: 20-30 minutes (5-7 approaches × 5 sub-approaches)
- Level 2: 15-20 minutes (optional, if time allows)
- Total: 50-70 minutes maximum

**Batch Execution** (with Task tool):
1. Spawn Level 0 tasks in single batch (8-10 tasks)
2. Wait for completion, evaluate, prune
3. Spawn Level 1 tasks in batches of 10-15
4. Monitor time, stop spawning if approaching limit

**Early Termination** (if time runs out):
- Evaluate completed branches only
- Return partial results with note about incomplete exploration
- State confidence level based on partial coverage

---

## Self-Critique Checklist

After applying BoT methodology, verify:

- [ ] **Sufficient Breadth**: Did I explore 8-10 approaches at Level 0?
- [ ] **Approach Diversity**: Are approaches fundamentally different (not variations)?
- [ ] **Conservative Pruning**: Did I keep all branches >40% confidence?
- [ ] **Depth Per Branch**: Did each branch get thorough exploration (not surface-level)?
- [ ] **Multiple Solutions**: Am I returning 3-5 solutions (not just 1 "best")?
- [ ] **Trade-Off Clarity**: Can user choose based on their priorities?
- [ ] **Confidence Validity**: Are confidence scores justified by exploration depth?
- [ ] **Completeness**: Did I explore enough to confidently say "I didn't miss anything major"?

---

## Common Mistakes to Avoid

1. **Premature Pruning**: Cutting branches at 50-60% confidence instead of <40%
2. **Depth Over Breadth**: Going 5 levels deep on 2 approaches instead of 2 levels on 8 approaches
3. **Variation vs Diversity**: Exploring PostgreSQL, MySQL, MariaDB as "3 approaches" (all relational)
4. **Single Winner**: Returning only 1 solution like ToT, defeating purpose of BoT
5. **Shallow Exploration**: Brief 1-paragraph analyses instead of thorough investigation
6. **Ignoring Unknown Unknowns**: Not exploring "wild card" unconventional approaches
7. **Over-Execution**: Going to Level 3-4 when Level 2 already gave 20+ viable solutions

---

## Breadth-First vs Depth-First Decision Guide

| Problem Characteristic | Use BoT (Breadth) | Use ToT (Depth) |
|------------------------|-------------------|-----------------|
| **Solution space** | Unknown, unexplored | Well-understood |
| **Output needed** | Multiple options | Single best |
| **Evaluation criteria** | Unclear or multiple | Clear and agreed |
| **Risk tolerance** | Can't miss alternatives | Can commit to best |
| **Problem novelty** | Novel/unprecedented | Has precedents |
| **Time available** | Moderate (1 hour) | Flexible (2+ hours) |

**Rule of thumb**:
- If you're asking "What are ALL my options?", use **Breadth of Thought**
- If you're asking "Which option is BEST?", use **Tree of Thoughts**

---

## Reference Documentation

**Detailed Templates**: `~/.claude/skills/breadth-of-thought/references/breadth-of-thought-patterns.md`

Includes:
- Approach exploration template (deep-dive structure)
- Conservative pruning guidelines (when to keep vs cut)
- Level transition logic (when to go to Level 2)
- Trade-off analysis framework
- Edge case handling (convergence, insufficient diversity)

---

## Summary

Breadth of Thought is a **systematic methodology** for exhaustive solution space exploration through:
1. **Wide branching** (8-10 approaches per level)
2. **Conservative pruning** (keep >40% confidence)
3. **Shallow depth** (2-3 levels maximum)
4. **Multiple solutions** (return top 3-5, not just 1)
5. **Trade-off analysis** (help user choose based on priorities)

Use it when you need comprehensive exploration and can't afford to miss viable alternatives. The goal is thorough coverage of solution space, not finding a single optimal answer.

**Remember**: Breadth of Thought trades depth for coverage. You'll explore more branches but less deeply than Tree of Thoughts. Perfect for "What are my options?" questions, not "Which option is best?" questions.
