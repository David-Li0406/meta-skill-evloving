---
name: integrated-reasoning
description: Meta-orchestration guide for choosing optimal reasoning patterns. Analyzes problem characteristics and recommends which cognitive methodology to use - tree-of-thoughts (find best), breadth-of-thought (explore all), self-reflecting-chain (sequential logic), or direct analysis. Use when facing complex problems and unsure which reasoning approach fits best.
license: MIT
---

# Integrated Reasoning - Meta-Orchestration Guide

**Purpose**: Guide for selecting and orchestrating the optimal reasoning methodology for your problem. Analyzes problem characteristics and recommends tree-of-thoughts, breadth-of-thought, self-reflecting-chain, or direct analysis.

## When to Use Integrated Reasoning

**✅ Use when:**
- Facing complex problem, unsure which reasoning approach to use
- Problem has 8+ decision dimensions (architectural decision, strategic planning)
- Need >90% confidence in solution
- High-stakes decision with long-term implications
- Problem spans multiple domains (technical + business + organizational)

**❌ Don't use when:**
- Problem clearly fits one pattern (use that pattern directly)
- Simple decision with obvious answer
- Time-critical with straightforward trade-offs

---

## Reasoning Pattern Selection Guide

### Decision Tree: Which Pattern to Use?

**Question 1: Does problem require sequential reasoning?**
- ✅ **Yes** (steps have dependencies) → **Self-Reflecting Chain**
  - Examples: Debugging, mathematical proofs, causal analysis
  - Go to Section: Self-Reflecting Chain

- ❌ **No** (steps are independent) → Continue to Question 2

**Question 2: Are evaluation criteria clear?**
- ✅ **Yes** (can score/rank solutions) → **Tree of Thoughts**
  - Examples: Optimization problems, architectural choices with metrics
  - Go to Section: Tree of Thoughts

- ❌ **No** (unclear how to evaluate) → Continue to Question 3

**Question 3: Is solution space unknown?**
- ✅ **Yes** (don't know all options) → **Breadth of Thought**
  - Examples: Novel problems, comprehensive planning, debugging complex issues
  - Go to Section: Breadth of Thought

- ❌ **No** (solution space known) → **Direct Analysis**
  - No special reasoning pattern needed
  - Apply standard analytical thinking

---

## Pattern Comparison Matrix

| Characteristic | Tree of Thoughts | Breadth of Thought | Self-Reflecting Chain | Direct Analysis |
|----------------|------------------|--------------------|-----------------------|-----------------|
| **Exploration** | Deep (4-6 levels) | Wide (8-10 branches) | Sequential chain | Single path |
| **Output** | 1 best solution | 3-5 viable options | Logical conclusion | Direct answer |
| **Branching** | 5 per level | 8-10 per level | No branches | No branches |
| **Depth** | 4-6 levels | 2-3 levels | N steps (sequential) | Shallow |
| **When** | Clear criteria | Unknown space | Dependencies exist | Simple problem |
| **Time** | 30-60 min | 30-50 min | 20-40 min | 5-15 min |
| **Confidence** | 80-95% | 70-85% | 70-90% | 60-80% |

---

## Section: Tree of Thoughts

**Use when:**
- Problem has multiple viable solution approaches (3+)
- Can define clear evaluation criteria
- Need to find THE optimal solution (not just any solution)
- Trade-offs exist between competing approaches
- Strategic decisions with long-term impact

**Methodology**:
1. Decompose into 5+ distinct approaches
2. Explore each branch with self-reflection
3. Evaluate rigorously (5 criteria: Novelty, Feasibility, Completeness, Confidence, Alignment)
4. Select best branch, recurse 4-6 levels deep
5. Return optimal solution with 80-95% confidence

**Load skill**: `tree-of-thoughts`

**Examples**:
- "Choose API architecture: REST, GraphQL, gRPC, or WebSocket?"
- "Design caching strategy balancing latency, consistency, and cost"
- "Select database: SQL, NoSQL, NewSQL, or Time-Series?"

---

## Section: Breadth of Thought

**Use when:**
- Solution space is unknown or unexplored
- Need multiple viable options (3-5), not just one best
- Can't afford to miss viable alternatives
- Novel/unprecedented problem
- Debugging with multiple potential causes
- High-stakes where premature convergence is risky

**Methodology**:
1. Map solution space: 8-10 fundamentally distinct approaches
2. Explore each approach thoroughly
3. Prune conservatively (only remove <40% confidence)
4. Expand survivors into 5 sub-approaches each
5. Return top 3-5 solutions with trade-off analysis

**Load skill**: `breadth-of-thought`

**Examples**:
- "Redesign data pipeline - batch, streaming, hybrid, or other?"
- "System crashes intermittently - network, DB, memory, race, config?"
- "Comprehensive feature planning with multiple implementation strategies"

---

## Section: Self-Reflecting Chain

**Use when:**
- Steps have sequential dependencies
- Logical reasoning required (deductive, causal, mathematical)
- Need to trace exact reasoning path
- Error detection and correction critical
- Debugging (trace bug through execution flow)
- Sequential planning where order matters

**Methodology**:
1. Decompose into sequential steps
2. Execute each step with deep self-reflection
3. Validate logic at each step (confidence ≥70%)
4. Backtrack when errors detected or confidence low (<60%)
5. Return conclusion with full reasoning trace

**Load skill**: `self-reflecting-chain`

**Examples**:
- "Debug this race condition by tracing execution step-by-step"
- "Prove this mathematical theorem with logical steps"
- "Plan project where each phase depends on previous completion"

---

## Section: Direct Analysis

**Use when:**
- Problem is straightforward with clear solution
- Time-critical decision with simple trade-offs
- Solution space has 1-2 obvious options
- No special reasoning pattern needed

**Methodology**:
1. Analyze problem directly
2. Consider 1-2 obvious alternatives
3. Make decision based on clear criteria
4. Document briefly

**No skill needed** - use standard analytical thinking

**Examples**:
- "Fix this syntax error"
- "Choose between two similar libraries with clear documentation"
- "Schedule meeting for team of 5"

---

## Orchestration: Combining Multiple Patterns

**Complex problems may need multiple patterns:**

### Pattern 1: Sequential Orchestration

**When**: Problem has multiple phases with different reasoning needs

**Example**: System architecture redesign
1. **Phase 1**: Use **Breadth of Thought** to explore all architectural options (10 options)
2. **Phase 2**: Use **Tree of Thoughts** to find optimal within top 3 categories
3. **Phase 3**: Use **Self-Reflecting Chain** to validate migration path step-by-step

### Pattern 2: Parallel Comparison

**When**: Need to compare multiple reasoning approaches

**Example**: Critical business decision
1. **Branch A**: Apply **Tree of Thoughts** assuming clear criteria
2. **Branch B**: Apply **Breadth of Thought** exploring unknown alternatives
3. **Compare**: Which approach gave higher confidence?
4. **Use**: Solution from higher-confidence approach

---

## Confidence Calibration

**Expected confidence by pattern**:

- **Tree of Thoughts**: 80-95% (deep exploration of best path)
- **Breadth of Thought**: 70-85% (wide coverage, less depth)
- **Self-Reflecting Chain**: 70-90% (depends on weakest link in chain)
- **Direct Analysis**: 60-80% (quick analysis, less rigor)

**Confidence thresholds**:
- **90-95%**: Exceptional evidence, suitable for critical decisions
- **80-89%**: High confidence, suitable for important decisions
- **70-79%**: Medium confidence, consider additional validation
- **60-69%**: Low confidence, recommend further investigation
- **<60%**: Very low confidence, gather more information

---

## Quick Reference: Choose Your Pattern

```
START
  │
  ├─ Sequential dependencies? → YES → Self-Reflecting Chain
  │                             NO ↓
  ├─ Clear evaluation criteria? → YES → Tree of Thoughts
  │                               NO ↓
  ├─ Solution space unknown? → YES → Breadth of Thought
  │                           NO ↓
  └─ Simple/obvious solution → Direct Analysis
```

---

## Meta-Analysis Checklist

Before selecting pattern, ask:

- [ ] **Problem Complexity**: Simple (<3 options) vs Complex (8+ dimensions)?
- [ ] **Dependencies**: Sequential steps vs Independent branches?
- [ ] **Evaluation**: Clear criteria vs Unclear how to judge?
- [ ] **Solution Space**: Known options vs Unknown territory?
- [ ] **Output Needed**: 1 best vs Multiple options vs Logical proof?
- [ ] **Time Available**: Quick (<20min) vs Thorough (60min+)?
- [ ] **Confidence Required**: Low (70%) vs High (90%+)?

---

## Summary

Integrated Reasoning helps you choose the right cognitive tool:

- **Tree of Thoughts**: When you need the BEST solution (clear criteria, deep exploration)
- **Breadth of Thought**: When you need ALL options (unknown space, wide exploration)
- **Self-Reflecting Chain**: When you need LOGICAL proof (sequential steps, backtracking)
- **Direct Analysis**: When solution is OBVIOUS (simple problems, quick decisions)

**Load the appropriate skill and follow its methodology for optimal results.**

Most problems fit one pattern. Complex problems may need orchestration of multiple patterns sequentially or in parallel.

**Remember**: The right reasoning pattern depends on problem characteristics, not problem domain. A "database choice" could use ToT (if criteria clear), BoT (if exploring all options), or SRC (if migrating step-by-step).
