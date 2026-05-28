---
id: reflexion-learning
name: "Reflexion Learning"
domain: SDD
skill: faion-sdd
category: "sdd"
---

# Reflexion Learning

## Overview

Reflexion Learning is an SDD methodology for continuous improvement through systematic analysis of task execution, identification of patterns and mistakes, and integration of lessons learned into future work. It creates a feedback loop that improves both AI agent and human developer performance over time.

## When to Use

- After completing any task (success or failure)
- When encountering recurring issues
- During retrospectives
- When onboarding new team members
- For improving estimation accuracy
- When updating process documentation

## Process/Steps

### 1. Reflexion Framework

```
Task Execution
      │
      ▼
  Outcome Analysis
      │
      ├── Success Path
      │   ├── What worked well?
      │   ├── Why did it work?
      │   └── Can it be replicated?
      │
      └── Failure Path
          ├── What went wrong?
          ├── Root cause analysis
          └── Prevention strategy
      │
      ▼
Pattern Extraction
      │
      ├── Positive Patterns → patterns_learned.jsonl
      └── Mistakes to Avoid → mistakes_learned.jsonl
      │
      ▼
Memory Integration
      │
      └── Apply to future tasks
```

### 2. Post-Task Analysis

**Analysis Template:**
```yaml
reflexion_analysis:
  task_reference:
    id: "TASK_XXX"
    title: "Task title"
    outcome: "success|partial|failure"
    actual_time: "4h"
    estimated_time: "2h"

  what_went_well:
    - description: "Clear acceptance criteria"
      impact: "Reduced ambiguity, faster implementation"
      replicable: true

    - description: "Incremental testing approach"
      impact: "Caught bugs early"
      replicable: true

  what_could_improve:
    - description: "Underestimated database migration complexity"
      impact: "2 hours over estimate"
      root_cause: "Didn't consider data volume"
      prevention: "Always check data volume before estimating migrations"

  patterns_identified:
    positive:
      - "Break complex queries into CTEs for readability"
      - "Add index BEFORE running large data operations"

    negative:
      - "Don't assume empty tables in production"
      - "Don't skip local testing of migrations"

  knowledge_gaps:
    - "PostgreSQL partitioning strategies"
    - "Large-scale data migration patterns"

  action_items:
    - type: "learning"
      description: "Study PostgreSQL partitioning"
      priority: "medium"

    - type: "process"
      description: "Add data volume check to migration checklist"
      priority: "high"
```

### 3. Pattern Extraction

**Pattern Types:**
```yaml
pattern_categories:
  coding_patterns:
    description: "Reusable code solutions"
    examples:
      - "Error handling pattern for async operations"
      - "State management pattern for forms"
      - "API response normalization"

  process_patterns:
    description: "Workflow optimizations"
    examples:
      - "Test-first for complex algorithms"
      - "Spike before estimating unknowns"
      - "Review design doc before coding"

  debugging_patterns:
    description: "Problem-solving approaches"
    examples:
      - "Binary search for configuration issues"
      - "Check logs first for production bugs"
      - "Reproduce locally before fixing"

  communication_patterns:
    description: "Effective collaboration"
    examples:
      - "Ask clarifying questions early"
      - "Document assumptions explicitly"
      - "Share blockers immediately"
```

**Pattern Documentation Format:**
```json
{
  "id": "PAT_2024_001",
  "timestamp": "2024-01-15T10:30:00Z",
  "category": "coding_pattern",
  "name": "Async Error Boundary Pattern",
  "context": "React components with async data fetching",
  "problem": "Unhandled promise rejections crash the app",
  "solution": "Wrap async operations in try-catch with error state",
  "code_example": "...",
  "benefits": ["Graceful degradation", "Better UX", "Easier debugging"],
  "trade_offs": ["More code", "Need to design error states"],
  "learned_from": "TASK_042",
  "confidence": 0.9,
  "usage_count": 0
}
```

### 4. Mistake Documentation

**Mistake Record Format:**
```json
{
  "id": "MIS_2024_001",
  "timestamp": "2024-01-15T10:30:00Z",
  "category": "estimation",
  "severity": "medium",
  "description": "Underestimated database migration time",
  "context": "Migrating 10M+ rows with schema change",
  "what_happened": "Migration took 3 hours instead of estimated 30 minutes",
  "root_cause": "Didn't check row count before estimating",
  "impact": "Delayed release by half a day",
  "prevention_strategy": "Always run SELECT COUNT(*) before estimating migrations",
  "detection_improvement": "Add data volume to task preparation checklist",
  "learned_from": "TASK_055",
  "occurrence_count": 1,
  "last_occurrence": "2024-01-15"
}
```

**Common Mistake Categories:**
```yaml
mistake_categories:
  estimation:
    - underestimating_complexity
    - ignoring_dependencies
    - not_accounting_for_testing
    - optimistic_timelines

  implementation:
    - premature_optimization
    - over_engineering
    - ignoring_edge_cases
    - skipping_error_handling

  testing:
    - insufficient_coverage
    - testing_happy_path_only
    - not_testing_locally
    - ignoring_integration_tests

  communication:
    - late_escalation
    - unclear_requirements
    - assumptions_not_validated
    - not_documenting_decisions

  process:
    - skipping_code_review
    - not_reading_existing_code
    - ignoring_ci_failures
    - not_following_conventions
```

### 5. Memory System

**Memory Structure:**
```
~/.sdd/memory/
├── patterns_learned.jsonl      # Positive patterns
├── mistakes_learned.jsonl      # Mistakes to avoid
├── session_context.md          # Current session state
├── estimation_history.jsonl    # For calibration
└── decision_log.jsonl          # Architectural decisions
```

**Session Context:**
```markdown
# Session Context

## Current Task
- ID: TASK_XXX
- Status: in_progress
- Started: 2024-01-15T10:00:00Z

## Relevant Patterns
- PAT_2024_001: Async Error Boundary (confidence: 0.9)
- PAT_2024_015: Form Validation Pattern (confidence: 0.85)

## Relevant Mistakes to Avoid
- MIS_2024_001: Check data volume before migrations
- MIS_2024_008: Don't assume API response format

## Active Decisions
- Chose PostgreSQL over MySQL (see ADR-005)
- Using TypeScript strict mode

## Open Questions
- Need clarification on error message wording
```

### 6. Learning Integration

**Pre-Task Memory Check:**
```yaml
pre_task_protocol:
  1_load_context:
    - "Load patterns relevant to task type"
    - "Load mistakes related to task domain"
    - "Review estimation history for similar tasks"

  2_apply_patterns:
    - "Identify applicable positive patterns"
    - "List potential pitfalls from mistakes"
    - "Adjust estimate based on history"

  3_document:
    - "Note planned patterns in task notes"
    - "Flag potential risks from past mistakes"
```

**Post-Task Memory Update:**
```yaml
post_task_protocol:
  1_reflexion:
    - "Complete reflexion analysis template"
    - "Identify new patterns (positive and negative)"
    - "Note estimation accuracy"

  2_update_memory:
    - "Add new patterns to patterns_learned.jsonl"
    - "Add new mistakes to mistakes_learned.jsonl"
    - "Update pattern/mistake confidence scores"
    - "Increment usage counts for applied patterns"

  3_propagate:
    - "Update team documentation if broadly applicable"
    - "Share insights in retrospective"
    - "Update checklists if process improvement"
```

### 7. Confidence Calibration

**Confidence Scoring:**
```yaml
confidence_levels:
  high: 0.9
    criteria:
      - "Used successfully 5+ times"
      - "Validated in different contexts"
      - "No failures in recent usage"

  medium: 0.7
    criteria:
      - "Used successfully 2-4 times"
      - "Works in specific contexts"
      - "Minor issues encountered"

  low: 0.5
    criteria:
      - "Used once or twice"
      - "Limited context validation"
      - "Potential edge cases unknown"

  experimental: 0.3
    criteria:
      - "Newly identified"
      - "Not yet validated"
      - "Theoretical benefit"
```

**Confidence Update Rules:**
```python
def update_confidence(pattern, outcome):
    """Update pattern confidence based on usage outcome"""

    if outcome == "success":
        pattern.confidence = min(0.95, pattern.confidence + 0.05)
        pattern.usage_count += 1
    elif outcome == "partial":
        pattern.confidence = pattern.confidence * 0.95
    elif outcome == "failure":
        pattern.confidence = max(0.3, pattern.confidence - 0.15)

    # Decay unused patterns
    if pattern.days_since_use > 90:
        pattern.confidence *= 0.9

    return pattern
```

## Best Practices

### Analysis Quality
1. **Be specific** - Vague lessons aren't actionable
2. **Find root causes** - Don't stop at symptoms
3. **Quantify impact** - Numbers make it real
4. **Validate assumptions** - Test your conclusions

### Pattern Management
1. **Regular review** - Prune outdated patterns
2. **Confidence decay** - Old unused patterns lose confidence
3. **Context matters** - Note when patterns apply
4. **Share broadly** - Team-wide patterns in docs

### Continuous Improvement
1. **Consistent practice** - Reflexion after every task
2. **Action-oriented** - Turn insights into changes
3. **Track effectiveness** - Measure improvement
4. **Iterate process** - Improve how you learn

## Templates/Examples

### Quick Reflexion (5 minutes)

```markdown
## Quick Reflexion: TASK_XXX

**Outcome:** Success / Partial / Failure
**Time:** Estimated Xh, Actual Yh

**One thing that worked:**
[Brief description]

**One thing to improve:**
[Brief description]

**Pattern to remember:**
[One sentence pattern or "None new"]

**Mistake to avoid:**
[One sentence or "None new"]
```

### Sprint Reflexion Summary

```markdown
## Sprint Reflexion: Sprint N

### Metrics
| Metric | Target | Actual |
|--------|--------|--------|
| Velocity | X pts | Y pts |
| Estimation accuracy | 80% | Z% |
| Bugs escaped | 0 | N |

### Top Patterns Applied
1. [Pattern] - Used N times, Y% success
2. [Pattern] - Used N times, Y% success

### Mistakes Avoided
1. [Mistake] - Would have cost X hours
2. [Mistake] - Saved by early detection

### New Patterns Identified
1. [New pattern from this sprint]
2. [New pattern from this sprint]

### New Mistakes Documented
1. [New mistake to avoid]
2. [New mistake to avoid]

### Action Items
- [ ] Update [checklist/doc] with [learning]
- [ ] Share [pattern] with team
- [ ] Improve estimation for [task type]
```

### Memory Query Patterns

```python
# Load relevant patterns for a task
def get_relevant_patterns(task_type, domain, limit=5):
    patterns = load_patterns()
    relevant = [p for p in patterns
                if task_type in p.contexts or domain in p.domains]
    sorted_patterns = sorted(relevant,
                            key=lambda p: p.confidence * p.recency_score,
                            reverse=True)
    return sorted_patterns[:limit]

# Load relevant mistakes for a task
def get_relevant_mistakes(task_type, domain, limit=5):
    mistakes = load_mistakes()
    relevant = [m for m in mistakes
                if task_type in m.contexts or domain in m.domains]
    sorted_mistakes = sorted(relevant,
                            key=lambda m: m.severity * m.occurrence_count,
                            reverse=True)
    return sorted_mistakes[:limit]
```

## References

- [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)
- [reflexion-learning: Reflexion Learning (Original)](./reflexion-learning_reflexion_learning.md)
- [pattern-memory: Pattern Memory](./pattern-memory_pattern_memory.md)
- [mistake-memory: Mistake Memory](./mistake-memory_mistake_memory.md)
- [Learning from Failure in Software Development](https://www.oreilly.com/library/view/site-reliability-engineering/9781491929117/ch15.html)
