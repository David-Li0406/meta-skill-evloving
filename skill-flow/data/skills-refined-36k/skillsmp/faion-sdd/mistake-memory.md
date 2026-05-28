---
id: mistake-memory
name: "Mistake Memory"
domain: SDD
skill: faion-sdd
category: "sdd"
---

# Mistake Memory

## Overview

Mistake Memory is the SDD system for capturing, analyzing, and preventing recurring mistakes. It transforms failures into learning opportunities by documenting what went wrong, why, and how to prevent similar issues in the future. The goal is not to assign blame but to build a collective knowledge base that helps everyone avoid known pitfalls.

## When to Use

- After encountering any bug, error, or failure
- When tasks take significantly longer than estimated
- During incident post-mortems
- When reviewing code with common anti-patterns
- For onboarding (teaching what to avoid)
- When updating process documentation

## Process/Steps

### 1. Mistake Memory Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Mistake Memory System                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │   Capture   │ →  │   Analysis  │ →  │ Prevention  │    │
│  │   Layer     │    │   Layer     │    │   Layer     │    │
│  └─────────────┘    └─────────────┘    └─────────────┘    │
│        │                  │                  │             │
│        ▼                  ▼                  ▼             │
│  Incident         Root Cause          Checklists          │
│  Detection        Analysis            Automations         │
│  & Logging                            Pre-task Warnings   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Storage Location:**
```
~/.sdd/memory/
├── mistakes_learned.jsonl       # Main mistake storage
├── mistakes_index.json          # Quick lookup index
├── mistakes_stats.json          # Analytics
├── prevention_rules.json        # Automated checks
└── incidents/                   # Detailed incident reports
    └── INC_2024_001.md
```

### 2. Mistake Schema

**Full Mistake Record:**
```json
{
  "id": "MIS_2024_001",
  "version": 1,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T15:45:00Z",

  "metadata": {
    "category": "implementation",
    "subcategory": "data-handling",
    "severity": "high",
    "language": "python",
    "domain": "database",
    "tags": ["migration", "data-loss", "production"]
  },

  "mistake": {
    "title": "Database Migration Without Backup",
    "summary": "Ran destructive migration on production without backup",

    "what_happened": {
      "description": "Executed ALTER TABLE DROP COLUMN on production table without taking a backup first. Lost 2 weeks of data in dropped column.",
      "timeline": [
        "10:00 - Started migration script",
        "10:02 - Migration completed (appeared successful)",
        "10:30 - User report: missing data",
        "11:00 - Confirmed data loss",
        "14:00 - Restored from nightly backup (lost 12 hours)"
      ],
      "impact": {
        "data_loss": "12 hours of column data",
        "downtime": "4 hours",
        "cost": "16 developer hours for recovery",
        "user_impact": "50 users affected"
      }
    },

    "root_cause_analysis": {
      "immediate_cause": "No backup before destructive migration",
      "contributing_factors": [
        "No pre-migration checklist",
        "Overconfidence in tested migration",
        "Production database same as staging (bad practice)",
        "No migration rollback plan"
      ],
      "root_cause": "Missing process for destructive database operations",
      "five_whys": [
        "Why was data lost? - Column was dropped",
        "Why was column dropped without backup? - No backup procedure",
        "Why no backup procedure? - Never formalized migration process",
        "Why not formalized? - Team grew fast, process didn't scale",
        "Why didn't process scale? - No designated process owner"
      ]
    },

    "prevention": {
      "immediate_actions": [
        "Implement pre-migration backup requirement",
        "Add migration approval workflow"
      ],
      "process_changes": [
        "Create database migration checklist",
        "Require peer review for destructive migrations",
        "Implement automatic pre-migration snapshots"
      ],
      "automation": [
        "CI check: detect DROP/DELETE in migrations",
        "Pre-deployment: automatic backup trigger",
        "Alert: flag production-targeted destructive queries"
      ],
      "detection_improvement": [
        "Add data integrity monitoring",
        "Set up row count alerts"
      ]
    },

    "checklist_additions": [
      {
        "checklist": "database-migration",
        "item": "Take full backup before any schema change",
        "position": "first"
      },
      {
        "checklist": "database-migration",
        "item": "Verify rollback procedure exists and tested",
        "position": "before-execution"
      }
    ]
  },

  "validation": {
    "occurrence_count": 1,
    "last_occurrence": "2024-01-15T10:00:00Z",
    "prevention_effectiveness": null,
    "related_incidents": []
  },

  "provenance": {
    "discovered_in": "INC_2024_001",
    "reported_by": "claude-agent",
    "verified_by": "human-review",
    "post_mortem_url": "https://docs.example.com/incidents/INC_2024_001"
  }
}
```

### 3. Mistake Categories

**Category Taxonomy:**
```yaml
mistake_categories:
  estimation:
    causes:
      - underestimating_complexity
      - missing_dependencies
      - optimistic_assumptions
      - unfamiliar_technology
    impact: "Schedule delays, rushed work"

  implementation:
    causes:
      - edge_cases_missed
      - error_handling_gaps
      - race_conditions
      - resource_leaks
    impact: "Bugs, instability"

  data_handling:
    causes:
      - no_backup
      - bad_migration
      - data_corruption
      - privacy_violation
    impact: "Data loss, compliance issues"

  security:
    causes:
      - hardcoded_secrets
      - missing_validation
      - improper_auth
      - exposed_endpoints
    impact: "Vulnerabilities, breaches"

  deployment:
    causes:
      - no_rollback_plan
      - untested_in_staging
      - config_mismatch
      - missing_dependencies
    impact: "Outages, rollbacks"

  communication:
    causes:
      - unclear_requirements
      - late_escalation
      - assumption_not_validated
      - missing_handoff
    impact: "Rework, delays"

  testing:
    causes:
      - insufficient_coverage
      - flaky_tests
      - wrong_test_data
      - skipped_tests
    impact: "Bugs reach production"

  process:
    causes:
      - skipped_review
      - ignored_warnings
      - shortcut_taken
      - documentation_gap
    impact: "Quality issues, tech debt"
```

### 4. Mistake Capture

**Capture Triggers:**
```yaml
capture_triggers:
  automatic:
    - "CI/CD pipeline failure"
    - "Production error alert"
    - "Test failure pattern detected"
    - "Estimation miss > 50%"

  manual:
    - "Developer reports issue"
    - "Code review finding"
    - "Retrospective action item"
    - "Customer-reported bug"

  ai_detected:
    - "Agent encounters known anti-pattern"
    - "Similar mistake pattern recognized"
    - "Repeated debugging cycles"
```

**Capture Process:**
```python
def capture_mistake(incident_data: dict) -> Mistake:
    """Capture a new mistake from an incident"""

    # 1. Create basic record
    mistake = Mistake(
        id=generate_mistake_id(),
        metadata=categorize_incident(incident_data),
        what_happened=document_incident(incident_data),
        provenance=create_provenance(incident_data)
    )

    # 2. Perform root cause analysis
    mistake.root_cause_analysis = analyze_root_cause(incident_data)

    # 3. Generate prevention strategies
    mistake.prevention = generate_prevention_strategies(mistake)

    # 4. Check for similar existing mistakes
    similar = find_similar_mistakes(mistake)
    if similar:
        mistake = link_or_merge_mistakes(mistake, similar)

    # 5. Store mistake
    store_mistake(mistake)

    # 6. Update prevention rules
    update_prevention_rules(mistake)

    # 7. Update checklists
    update_checklists(mistake.checklist_additions)

    return mistake
```

### 5. Root Cause Analysis

**Five Whys Framework:**
```python
def perform_five_whys(incident: dict) -> dict:
    """Structured root cause analysis"""

    whys = []
    current_cause = incident['immediate_cause']

    for i in range(5):
        why_question = f"Why: {current_cause}?"
        answer = analyze_why(current_cause, incident)

        whys.append({
            "level": i + 1,
            "question": why_question,
            "answer": answer
        })

        current_cause = answer

        # Stop if we've reached systemic/root cause
        if is_root_cause(answer):
            break

    return {
        "five_whys": whys,
        "root_cause": whys[-1]["answer"],
        "systemic_factors": identify_systemic_factors(whys)
    }
```

**Analysis Template:**
```markdown
## Root Cause Analysis: [Incident Title]

### Immediate Cause
[What directly caused the issue]

### Five Whys
1. Why did [immediate cause]?
   → [Answer 1]

2. Why [Answer 1]?
   → [Answer 2]

3. Why [Answer 2]?
   → [Answer 3]

4. Why [Answer 3]?
   → [Answer 4]

5. Why [Answer 4]?
   → [Root Cause]

### Contributing Factors
- [Factor 1]
- [Factor 2]
- [Factor 3]

### Systemic Issues
- [Process gap]
- [Tool limitation]
- [Knowledge gap]
```

### 6. Prevention System

**Prevention Rules:**
```json
{
  "rules": [
    {
      "id": "PREV_001",
      "source_mistake": "MIS_2024_001",
      "trigger": "file_contains_pattern",
      "pattern": "DROP (TABLE|COLUMN)",
      "file_types": ["*.sql", "migrations/*"],
      "action": "warn",
      "message": "Destructive migration detected. Ensure backup exists. See MIS_2024_001."
    },
    {
      "id": "PREV_002",
      "source_mistake": "MIS_2024_005",
      "trigger": "task_type",
      "task_type": "database_migration",
      "action": "require_checklist",
      "checklist": "database-migration-checklist"
    },
    {
      "id": "PREV_003",
      "source_mistake": "MIS_2024_010",
      "trigger": "estimate_context",
      "context_keywords": ["api integration", "third-party"],
      "action": "suggest",
      "message": "Consider spike first. Past integrations took 2x estimated. See MIS_2024_010."
    }
  ]
}
```

**Pre-Task Warning System:**
```python
def get_warnings_for_task(task: Task) -> List[Warning]:
    """Get relevant warnings before starting a task"""

    warnings = []
    mistakes = load_mistakes()

    # Match by category
    category_mistakes = [m for m in mistakes
                        if m.metadata.category in task.categories]

    # Match by keywords
    keyword_mistakes = find_mistakes_by_keywords(
        extract_keywords(task.description)
    )

    # Match by similar past tasks
    similar_task_mistakes = find_mistakes_from_similar_tasks(task)

    all_relevant = set(category_mistakes + keyword_mistakes + similar_task_mistakes)

    for mistake in all_relevant:
        warnings.append(Warning(
            severity=mistake.metadata.severity,
            title=f"Watch out: {mistake.title}",
            description=mistake.summary,
            prevention=mistake.prevention.immediate_actions,
            source=mistake.id
        ))

    return sorted(warnings, key=lambda w: severity_order(w.severity))
```

### 7. Mistake Tracking

**Occurrence Tracking:**
```python
def track_mistake_occurrence(mistake_id: str, occurred: bool):
    """Track if a known mistake occurred or was prevented"""

    mistake = load_mistake(mistake_id)

    if occurred:
        mistake.validation.occurrence_count += 1
        mistake.validation.last_occurrence = datetime.now()
        # Escalate if recurring
        if mistake.validation.occurrence_count >= 3:
            escalate_recurring_mistake(mistake)
    else:
        # Mistake was prevented
        if not mistake.validation.prevention_effectiveness:
            mistake.validation.prevention_effectiveness = {"prevented": 0, "total": 0}
        mistake.validation.prevention_effectiveness["prevented"] += 1
        mistake.validation.prevention_effectiveness["total"] += 1

    save_mistake(mistake)
```

**Metrics Dashboard:**
```yaml
mistake_metrics:
  overview:
    total_documented: 45
    this_month: 3
    prevented_this_month: 12

  by_category:
    implementation: 15
    estimation: 10
    data_handling: 8
    security: 5
    deployment: 4
    process: 3

  by_severity:
    critical: 5
    high: 15
    medium: 18
    low: 7

  recurring:
    - MIS_2024_005: 3 occurrences
    - MIS_2024_012: 2 occurrences

  most_prevented:
    - MIS_2024_001: 8 times (backup reminder)
    - MIS_2024_015: 6 times (test coverage check)

  trends:
    estimation_accuracy: "improving"
    production_incidents: "decreasing"
    review_findings: "stable"
```

### 8. Learning from Mistakes

**Post-Mortem Process:**
```yaml
post_mortem_process:
  timing: "Within 48 hours of incident"

  participants:
    - involved_parties
    - team_lead
    - affected_stakeholders

  agenda:
    1. timeline_reconstruction: 15min
    2. impact_assessment: 10min
    3. root_cause_analysis: 20min
    4. prevention_brainstorm: 15min
    5. action_items: 10min

  outputs:
    - incident_report
    - mistake_record
    - action_items
    - checklist_updates

  follow_up:
    - "1 week: Action items progress"
    - "1 month: Prevention effectiveness"
```

**Learning Integration:**
```python
def integrate_learning(mistake: Mistake):
    """Integrate mistake learning into systems"""

    # 1. Update relevant checklists
    for addition in mistake.checklist_additions:
        add_to_checklist(
            checklist_id=addition["checklist"],
            item=addition["item"],
            position=addition["position"]
        )

    # 2. Create prevention rules
    for rule in generate_prevention_rules(mistake):
        add_prevention_rule(rule)

    # 3. Update estimation factors
    if mistake.metadata.category == "estimation":
        update_estimation_factors(mistake)

    # 4. Notify relevant team members
    notify_stakeholders(mistake)

    # 5. Schedule follow-up
    schedule_effectiveness_review(mistake, days=30)
```

## Best Practices

### Blameless Culture
1. **Focus on systems** - Not individuals
2. **Assume good intent** - Everyone wants to succeed
3. **Share openly** - Transparency aids learning
4. **Celebrate finding** - Better to catch than hide

### Documentation Quality
1. **Be specific** - Vague descriptions don't help
2. **Include context** - What led to the situation
3. **Actionable prevention** - Concrete steps to avoid
4. **Keep updated** - Prevention evolves

### Prevention Focus
1. **Automate where possible** - Reduce human error
2. **Multiple layers** - Defense in depth
3. **Regular review** - Are preventions working?
4. **Low friction** - Easy to follow

## Templates/Examples

### Quick Mistake Capture

```markdown
## Mistake: [Brief Title]

**Date:** YYYY-MM-DD
**Severity:** Critical / High / Medium / Low
**Category:** [implementation / estimation / etc.]

**What Happened:**
[Brief description]

**Impact:**
[Time lost / data affected / users impacted]

**Root Cause:**
[Brief root cause]

**Prevention:**
- [ ] [Action 1]
- [ ] [Action 2]

**Discovered In:** TASK_XXX
```

### Monthly Mistake Review

```markdown
## Mistake Review: [Month Year]

### Summary
- New mistakes documented: X
- Recurring mistakes: Y
- Successfully prevented: Z

### Top Issues
1. [Mistake category]: [Count]
2. [Mistake category]: [Count]

### Prevention Effectiveness
| Prevention | Triggered | Prevented |
|------------|-----------|-----------|
| Backup reminder | 10 | 10 |
| Test coverage | 8 | 7 |

### Action Items
- [ ] Review MIS_XXX prevention (not effective)
- [ ] Add automation for MIS_YYY
- [ ] Update checklist for [category]

### Trends
[Are we getting better? Worse? Areas of concern?]
```

## References

- [reflexion-learning: Reflexion Learning](./reflexion-learning_reflexion_learning.md)
- [pattern-memory: Pattern Memory](./pattern-memory_pattern_memory.md)
- [Blameless Post-Mortems](https://sre.google/sre-book/postmortem-culture/)
- [The Five Whys](https://en.wikipedia.org/wiki/Five_whys)
- [Learning from Incidents](https://www.learningfromincidents.io/)
