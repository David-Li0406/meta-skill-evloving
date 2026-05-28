---
name: reality-analysis
description: Use this skill when you need to assess project state, identify discrepancies between documented plans and actual implementation, or analyze plan drift and alignment.
---

# Skill body

Knowledge and patterns for analyzing project state, detecting plan drift, and creating prioritized reconstruction plans.

## Architecture Overview

```
/reality-check:scan
        │
        ├─→ collectors.js (pure JavaScript)
        │   ├─ scanGitHubState()
        │   ├─ analyzeDocumentation()
        │   └─ scanCodebase()
        │
        └─→ plan-synthesizer (Opus)
            └─ Deep semantic analysis with full context
```

**Data collection**: Pure JavaScript (no LLM overhead)  
**Semantic analysis**: Single Opus call with complete context

## Drift Detection Patterns

### Types of Drift

**Plan Drift**: When documented plans diverge from actual implementation
- PLAN.md items remain unchecked for extended periods
- Roadmap milestones slip without updates
- Sprint/phase goals not reflected in code changes

**Documentation Drift**: When documentation falls behind implementation
- New features exist without corresponding docs
- README describes features that don't exist
- API docs don't match actual endpoints

**Issue Drift**: When issue tracking diverges from reality
- Stale issues that no longer apply
- Completed work without closed issues
- High-priority items neglected

**Scope Drift**: When project scope expands beyond original plans
- More features documented than can be delivered
- Continuous addition without completion
- Ever-growing backlog with no pruning

### Detection Signals

```
HIGH-CONFIDENCE DRIFT INDICATORS:
- Milestone 30+ days overdue with open issues
- PLAN.md < 30% completion after 90 days
- 5+ high-priority issues stale > 60 days
- README features not found in codebase

MEDIUM-CONFIDENCE INDICATORS:
- Documentation files unchanged for 180+ days
- Draft PRs open > 30 days
- Issue themes don't match code activity
- Large gap between documented and implemented features

LOW-CONFIDENCE INDICATORS:
- Many TODOs in codebase
- Stale dependencies
- Old git branches not merged
```

## Prioritization Framework

### Priority Calculation

```javascript
function calculatePriority(item, weights) {
  let score = 0;

  // Severity base score
  const severityScores = {
    critical: 15,
    high: 10,
    medium: 5,
    low: 1
  };
  // Additional logic for calculating priority based on item and weights
}
```