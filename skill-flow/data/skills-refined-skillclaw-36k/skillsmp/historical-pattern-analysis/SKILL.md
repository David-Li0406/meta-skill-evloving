---
name: historical-pattern-analysis
description: Use when analyzing git history and past changes to identify patterns, recurring issues, and lessons learned from infrastructure changes.
---

# Historical Pattern Analysis

## Overview

Analyze git history and memory to learn from past infrastructure changes. Identify patterns, recurring issues, and apply lessons learned to current work.

**Announce at start:** "I'm using the historical-pattern-analysis skill to learn from past changes."

## When to Use

- Before making changes similar to past changes
- When investigating recurring issues
- To understand why infrastructure is configured a certain way
- To identify change patterns and team practices

## Process

### Step 1: Define Search Scope

Determine what history to analyze:
- Specific resources being changed
- Time period (last month, quarter, year)
- Specific team members or patterns

### Step 2: Git Archaeology

#### Find Related Commits

```bash
# Commits touching specific files
git log --oneline -20 -- "path/to/module/*.tf"

# Commits mentioning resource types
git log --oneline -20 --grep="aws_security_group"

# Commits by pattern in message
git log --oneline -20 --grep="fix\|rollback\|revert"

# Commits in date range
git log --oneline --since="2024-01-01" --until="2024-06-01" -- "*.tf"
```

#### Analyze Commit Patterns

```bash
# Most frequently changed files
git log --pretty=format: --name-only -- "*.tf" | sort | uniq -c | sort -rn | head -20

# Authors and their focus areas
git shortlog -sn -- "environments/prod/"

# Change frequency by day/time
git log --format="%ad" --date=format:"%A %H:00" -- "*.tf" | sort | uniq -c
```

#### Find Reverts and Fixes

```bash
# Revert commits
git log --oneline --grep="revert\|Revert"

# Fix commits following changes
git log --oneline --grep="fix\|hotfix\|Fix"

# Commits with "URGENT" or "EMERGENCY"
git log --oneline --grep="urgent\|emergency" -i
```

### Step 3: Analyze Change Patterns

#### Coupling Analysis

Which files change together?
```bash
# For a specific file, what else changes with it?
git log --pretty=format:"%H" -- "modules/vpc/main.tf" | \
  xargs -I {} git show --name-only --pretty=format: {} | \
  sort | uniq -c | sort -rn | head -20
```

#### Change Sequences

Common sequences of changes:
1. VPC changes → followed by security group changes
2. IAM role changes → followed by policy attachments
3. RDS changes → followed by parameter group changes

#### Time Patterns

- Are prod changes clustered on certain days?
- Are there "risky" times based on past incidents?
- How long between staging and prod deployments?

### Step 4: Query Memory

Check stored patterns:
```
memory/projects/<hash>/patterns.json
memory/projects/<hash>/incidents.json
```

Look for:
- Similar past changes and outcomes
- Known issues with these resources
- User preferences for this type of change

### Step 5: Identify Lessons

#### From Incidents

For each past incident:
- What was the trigger?
- How was it detected?
- What was the fix?
- What could have prevented it?

#### From Patterns

- What changes tend to cause problems?
- What practices lead to success?
- What review processes work well?

### Step 6: Generate Report

```markdown
## Historical Pattern Analysis

### Search Scope
- Resources: [resources being analyzed]
- Time period: [date range]
- Related commits found: [count]

### Change Frequency

| Resource/File | Changes (90d) | Last Changed | Primary Authors |
|--------------|---------------|--------------|-----------------|
| modules/vpc/main.tf | 12 | 2024-01-10 | alice, bob |
| environments/prod/main.tf | 8 | 2024-01-08 | alice |

### Change Coupling

These resources typically change together:
1. `aws_security_group.web` ↔ `aws_instance.web` (85% correlation)
2. `aws_iam_role.app` ↔ `aws_iam_policy.app` (100% correlation)

### Past Incidents Related to These Resources

#### Incident: [Date] - [Title]
- **Trigger:** [What caused it]
- **Impact:** [What happened]
- **Resolution:** [How it was fixed]
- **Lesson:** [What we learned]
- **Relevance:** [How this applies to current change]

### Patterns Identified

#### Pattern: [Pattern Name]
- **Observation:** [What we see in history]
- **Frequency:** [How often]
- **Implication:** [What this means for current change]

### Risk Indicators

Based on historical data:
| Indicator | Current Change | Historical Issues |
|-----------|---------------|-------------------|
| Similar to past incident | [Yes/No] | [Details] |
| Frequently problematic resource | [Yes/No] | [Details] |
| Changed by unfamiliar author | [Yes/No] | [Details] |

### Recommendations

Based on historical patterns:
1. [Recommendation 1]
2. [Recommendation 2]

### Questions Raised

[Questions that history suggests we should answer]
```

### Step 7: Update Memory

Store new patterns discovered:
```json
{
  "patterns": [
    {
      "name": "vpc-sg-coupling",
      "description": "VPC changes often require SG updates",
      "confidence": 0.85,
      "last_seen": "2024-01-15"
    }
  ]
}
```

## Common Patterns to Look For

### Positive Patterns
- Consistent naming conventions
- Regular, small changes vs. big-bang updates
- Changes preceded by plan review
- Post-change validation

### Warning Patterns
- Frequent reverts
- Emergency fixes following changes
- Clustered failures in specific areas
- "Temporary" changes that persist

### Anti-Patterns
- Direct prod changes without staging
- Large changes without incremental steps
- Missing documentation on complex changes
- Recurring manual interventions

## Integration with Other Skills

This skill feeds into:
- **terraform-plan-review**: Provides historical context for risk assessment
- **terraform-drift-detection**: Identifies if drift matches past patterns
- **provider-upgrade-analysis**: Shows past upgrade experiences
