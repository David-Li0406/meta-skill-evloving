# Interpreting Consensus

This reference describes how to interpret multi-model review results and prioritize findings.

## Reviewer Consensus Levels

### Strong Consensus
- Multiple reviewers identified same issue
- High confidence in finding
- Prioritize for immediate attention

### Diverse Perspectives
- Different reviewers raised different concerns
- Indicates breadth of review coverage
- All perspectives valuable

### Conflicting Views
- Reviewers disagree on approach
- Both perspectives documented
- Requires human judgment

## Priority Assignment

| Level | Criteria | Action |
|-------|----------|--------|
| **CRITICAL** | Security vulnerabilities, blockers | Address immediately |
| **HIGH** | Design flaws, missing info | Address before implementation |
| **MEDIUM** | Improvements, unclear requirements | Consider addressing |
| **LOW** | Nice-to-have enhancements | Note for future |

## Consensus Detection Logic

Consensus is calculated based on **responding models only**, not requested models.

| Models Requested | Models Responded | Finding Agreement | Consensus Level |
|------------------|------------------|-------------------|-----------------|
| 3 | 3 | 3/3 agree | Strong |
| 3 | 3 | 2/3 agree | High |
| 3 | 2 | 2/2 agree | High (with reduced confidence note) |
| 3 | 2 | 1/2 flags | Moderate |
| 3 | 1 | 1/1 flags | Low (single-model) |
| 3 | 0 | N/A | Review failed |

**Edge case - partial failures:** If only 1 model responds due to timeouts or errors, all its findings are tagged as "single-model, lower confidence" and deprioritized by 1 level.

## Single-Model Weight Reduction

Single-model findings are reduced by exactly 1 priority level:

| Original Priority | Adjusted Priority |
|-------------------|-------------------|
| CRITICAL | HIGH |
| HIGH | MEDIUM |
| MEDIUM | LOW |
| LOW | LOW (floor) |

**Why:** Single-model findings lack cross-validation. The priority reduction reflects reduced confidence, not dismissal.

## Synthesis Algorithm

When merging findings from multiple models:

### 1. Deduplication

Findings addressing the same issue (same file/component + similar recommendation) are merged into one entry, listing all models that flagged it.

### 2. Priority Assignment

- **Multi-model findings**: Use the highest priority any model assigned
- **Single-model findings**: Apply weight reduction (see table above)

### 3. Conflict Resolution

- If models give conflicting recommendations for the same issue, document both under "Conflicting Views"
- Do NOT attempt to resolve conflicts - surface them for human judgment
- Conflicting findings retain their original priority levels

### 4. Category Assignment

Use the category from the first model that flagged the issue. If models disagree on category, use the more severe category.

## Acting on Findings

### By Priority

| Priority | Action |
|----------|--------|
| CRITICAL | Must address before proceeding. Block implementation until resolved. |
| HIGH | Should address before implementation. May require spec revision. |
| MEDIUM | Consider addressing. Document decision if skipping. |
| LOW | Optional. Add to backlog or note for future consideration. |

### By Consensus

| Consensus | Action |
|-----------|--------|
| Strong | High confidence - act on finding |
| Diverse | Review all perspectives - multiple valid concerns |
| Conflicting | Human judgment required - don't auto-resolve |
| Single-model | Lower confidence - verify independently if critical |
