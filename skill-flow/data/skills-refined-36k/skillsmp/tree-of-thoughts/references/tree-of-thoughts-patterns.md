# Tree of Thoughts - Detailed Patterns and Templates

This document provides detailed templates for applying Tree of Thoughts methodology.

## Pattern 1: Branch Exploration Template

Use this template when exploring each branch in Step 2:

```markdown
## Branch [Letter]: [Approach Name]

### Overview
[1-2 sentence summary of this approach]

### Requirements Coverage
[How does this approach address each requirement?]
- Requirement 1: [Coverage analysis]
- Requirement 2: [Coverage analysis]
- Requirement 3: [Coverage analysis]

### Strengths
- [Strength 1]
- [Strength 2]
- [Strength 3]

### Weaknesses
- [Weakness 1]
- [Weakness 2]
- [Weakness 3]

### Trade-offs
- **Gain**: [What you get with this approach]
- **Lose**: [What you sacrifice]

### Implementation Complexity
- **Effort**: [Low/Medium/High]
- **Risk**: [Low/Medium/High]
- **Timeline**: [Estimate]

### Self-Reflection
- **Confidence**: [0-100]/100
- **Strengths**: [Key compelling aspects]
- **Weaknesses**: [Critical gaps or assumptions]
- **Trade-offs**: [Core trade-off summary]
- **Recommendation**: [Continue exploration? Prune? Why?]
```

---

## Pattern 2: Evaluation Matrix Template

Use this to systematically score branches in Step 3:

```markdown
## Branch Evaluation Matrix

| Branch | Novelty | Feasibility | Completeness | Confidence | Alignment | **Total** |
|--------|---------|-------------|--------------|------------|-----------|-----------|
| A      | 15/20   | 18/20       | 16/20        | 17/20      | 19/20     | **85/100** |
| B      | 18/20   | 16/20       | 18/20        | 18/20      | 17/20     | **87/100** |
| C      | 12/20   | 19/20       | 17/20        | 16/20      | 18/20     | **82/100** |
| D      | 16/20   | 17/20       | 15/20        | 15/20      | 16/20     | **79/100** |
| E      | 14/20   | 20/20       | 14/20        | 14/20      | 17/20     | **79/100** |

**Winner**: Branch B (87/100) - Selected for Level 1 exploration

**Rationale**: [Why Branch B scored highest - summarize strengths and evaluation reasoning]
```

---

## Pattern 3: Level Transition Template

Use this when moving from Level N to Level N+1:

```markdown
## Level [N] → Level [N+1] Transition

### Level [N] Winner
- **Branch**: [Identifier, e.g., B.3.2]
- **Approach**: [Name of approach]
- **Score**: [X/100]
- **Why selected**: [Key strengths that made it win]

### Level [N+1] Decomposition

Expanding [Winner] into 5+ sub-approaches:

1. **Branch [N+1].1**: [Sub-approach 1]
   - Focus: [What dimension this explores]

2. **Branch [N+1].2**: [Sub-approach 2]
   - Focus: [What dimension this explores]

3. **Branch [N+1].3**: [Sub-approach 3]
   - Focus: [What dimension this explores]

4. **Branch [N+1].4**: [Sub-approach 4]
   - Focus: [What dimension this explores]

5. **Branch [N+1].5**: [Sub-approach 5]
   - Focus: [What dimension this explores]

[Proceed with Step 2: Explore each sub-branch]
```

---

## Pattern 4: Using Task Tool for Parallel Exploration

If you have access to the Task tool, use this pattern for true parallel exploration:

```python
# Example: Level 0 parallel exploration
branches = [
    {
        "id": "A",
        "name": "Write-through consistency approach",
        "prompt": "Analyze write-through consistency for distributed caching. Consider: strong consistency guarantees, latency impact, implementation complexity. End with self-reflection."
    },
    {
        "id": "B",
        "name": "Eventual consistency approach",
        "prompt": "Analyze eventual consistency for distributed caching. Consider: performance benefits, consistency trade-offs, conflict resolution. End with self-reflection."
    },
    # ... 3 more branches
]

# Launch all tasks in parallel
for branch in branches:
    Task(
        subagent_type="general-purpose",
        description=f"Explore Branch {branch['id']}",
        prompt=branch['prompt']
    )

# Wait for all to complete, then evaluate in Step 3
```

**Without Task tool**: Explore branches sequentially, using TodoWrite to track progress through each branch.

---

## Pattern 5: Confidence Scoring Examples

### High Confidence Branch (85/100)

**Scores**: Novelty 17/20, Feasibility 19/20, Completeness 18/20, Confidence 16/20, Alignment 15/20

**Justification**:
- **Novelty 17**: Fresh approach with some proven elements
- **Feasibility 19**: Clear implementation path with known tech
- **Completeness 18**: Addresses all major requirements, minor gaps
- **Confidence 16**: Self-reflection shows 80% confidence with good reasoning
- **Alignment 15**: Good fit for constraints, minor context misalignment

**Likelihood Ratios**: 3.44, 3.81, 3.62, 3.25, 3.06
**Bayesian Confidence**: ~92%

### Medium Confidence Branch (65/100)

**Scores**: Novelty 12/20, Feasibility 14/20, Completeness 13/20, Confidence 13/20, Alignment 13/20

**Justification**:
- **Novelty 12**: Standard approach, incremental improvements
- **Feasibility 14**: Implementable but with moderate challenges
- **Completeness 13**: Covers most requirements, notable gaps
- **Confidence 13**: Self-reflection shows 65% confidence with uncertainties
- **Alignment 13**: Decent fit, some misalignment with constraints

**Likelihood Ratios**: 2.50, 2.87, 2.69, 2.69, 2.69
**Bayesian Confidence**: ~75%

---

## Pattern 6: Edge Case Handling

### Edge Case 1: Branches Converge

**Scenario**: At Level 2, all 5 branches essentially propose the same solution

**Action**:
1. Document convergence: "All approaches converge on [solution]"
2. This is a **stopping signal** (criterion #3)
3. Synthesize the common elements
4. Note confidence boost from independent convergence
5. No need for Level 3 if convergence is clear

### Edge Case 2: Insufficient Branch Diversity

**Scenario**: You identified 5 branches, but they're all variations of the same core approach

**Action**:
1. **Flag the issue**: "Warning: Branches are variations, not fundamentally different"
2. Re-brainstorm to find truly diverse approaches
3. Consider different dimensions:
   - Technical approach (sync vs async, push vs pull)
   - Organizational impact (centralized vs distributed)
   - Risk profile (conservative vs innovative)
   - Cost structure (upfront vs ongoing)

### Edge Case 3: No Clear Winner

**Scenario**: Top 3 branches score 82, 81, 80 - no clear leader

**Action**:
1. Note the close competition
2. Explore **all top branches** at next level (not just #1)
3. Branches may differentiate at deeper levels
4. If they remain tied after Level 2, document trade-offs clearly
5. Provide decision criteria: "Choose A if [X], choose B if [Y]"

### Edge Case 4: Winner Has Low Confidence

**Scenario**: Best branch scores 72/100, but confidence criterion is only 8/20

**Action**:
1. **Don't stop yet** - low confidence warrants deeper exploration
2. At next level, focus on addressing the uncertainty that caused low confidence
3. Decompose into branches that test different assumptions
4. If confidence remains low after 4+ levels, document uncertainties clearly
5. Recommend validation steps or pilot testing

---

## Summary

These patterns provide concrete templates for applying Tree of Thoughts methodology. Adapt them to your specific problem context while maintaining the core principles:

- **5+ branches per level** (diversity)
- **Self-reflection** (confidence)
- **Systematic evaluation** (5 criteria)
- **Recursive depth** (4+ levels)
- **Clear synthesis** (trace winning path)

The goal is rigorous exploration leading to high-confidence optimal solutions.
