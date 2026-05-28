---
id: cross-tool-migration
name: "Cross-Tool Migration"
domain: PM
skill: faion-project-manager
category: "pm-tools"
---

# Cross-Tool Migration

## Overview

Migrating project management tools is a complex undertaking that involves data migration, process adaptation, team training, and maintaining productivity during transition. This methodology provides a structured approach to minimize disruption and maximize success.

## When to Use

- Organization switching PM tools (e.g., Jira to Linear)
- Consolidating multiple tools into one
- Scaling from simple to enterprise-grade solution
- Post-acquisition tool standardization
- Moving from legacy to modern tools

## Process/Steps

### 1. Migration Assessment

**Pre-Migration Audit:**
```yaml
audit_checklist:
  data_inventory:
    - total_projects: count
    - total_issues: count
    - total_attachments: size_gb
    - custom_fields: list
    - automations: count
    - integrations: list

  usage_patterns:
    - active_users: count
    - daily_active: percentage
    - key_workflows: list
    - power_users: list
    - pain_points: list

  dependencies:
    - ci_cd_integration: [tool, criticality]
    - slack_integration: [channels, automations]
    - documentation_links: [wiki, confluence]
    - reporting_systems: [dashboards, exports]

  compliance:
    - audit_requirements: [yes/no]
    - data_retention: [policy]
    - access_controls: [requirements]
```

### 2. Tool Mapping

**Field Mapping Template:**
| Source (Jira) | Target (Linear) | Transformation | Notes |
|---------------|-----------------|----------------|-------|
| Issue Type | Issue Label | Bug→bug, Story→feature | |
| Status | State | Map to closest | Review differences |
| Priority | Priority | 1:1 if available | |
| Story Points | Estimate | Direct transfer | |
| Sprint | Cycle | Match dates | |
| Epic | Project | Create projects | |
| Component | Label | Flatten hierarchy | |
| Fix Version | Milestone | Map by name | |
| Assignee | Assignee | Match by email | |
| Reporter | Creator | May lose data | API limitation |
| Comments | Comments | Preserve thread | |
| Attachments | Attachments | Upload separately | Check size limits |
| Custom Field: X | Custom Field: Y | Transform rule | |

### 3. Migration Phases

```
Phase 1: Planning (2-4 weeks)
├── Stakeholder alignment
├── Tool selection/evaluation
├── Migration scope definition
├── Timeline creation
└── Risk assessment

Phase 2: Preparation (2-3 weeks)
├── Target tool setup
├── Field mapping design
├── Migration script development
├── Test environment creation
└── Team communication

Phase 3: Pilot Migration (1-2 weeks)
├── Select pilot project
├── Execute migration
├── Validate data
├── Gather feedback
└── Adjust approach

Phase 4: Full Migration (1-4 weeks)
├── Execute in waves
├── Validate each wave
├── Address issues
└── Monitor progress

Phase 5: Cutover (1 week)
├── Final sync
├── Disable source tool
├── Enable target tool
└── Support team

Phase 6: Stabilization (2-4 weeks)
├── Active support
├── Fix issues
├── Training sessions
└── Document learnings
```

### 4. Data Migration Scripts

**Generic Migration Framework:**
```python
# migration_framework.py
from dataclasses import dataclass
from typing import Dict, List, Any
import json

@dataclass
class MigrationConfig:
    source_tool: str
    target_tool: str
    field_mapping: Dict[str, str]
    status_mapping: Dict[str, str]
    priority_mapping: Dict[str, str]
    dry_run: bool = True

class MigrationEngine:
    def __init__(self, config: MigrationConfig):
        self.config = config
        self.source_client = self._init_source()
        self.target_client = self._init_target()
        self.migration_log = []

    def extract(self, project_key: str) -> List[Dict]:
        """Extract all issues from source"""
        issues = self.source_client.get_issues(project_key)
        self.log(f"Extracted {len(issues)} issues")
        return issues

    def transform(self, issues: List[Dict]) -> List[Dict]:
        """Transform issues to target format"""
        transformed = []
        for issue in issues:
            try:
                transformed.append(self._transform_issue(issue))
            except Exception as e:
                self.log(f"Transform error {issue['key']}: {e}", "ERROR")
        return transformed

    def _transform_issue(self, issue: Dict) -> Dict:
        """Transform single issue"""
        return {
            "title": issue["summary"],
            "description": issue.get("description", ""),
            "state": self.config.status_mapping.get(
                issue["status"], "backlog"
            ),
            "priority": self.config.priority_mapping.get(
                issue["priority"], "medium"
            ),
            "labels": self._map_labels(issue),
            "assignee_email": issue.get("assignee", {}).get("email"),
            # Custom field mapping
            **self._map_custom_fields(issue)
        }

    def load(self, issues: List[Dict]) -> Dict[str, str]:
        """Load issues to target, return ID mapping"""
        id_mapping = {}
        for issue in issues:
            if self.config.dry_run:
                self.log(f"Would create: {issue['title']}")
                continue

            result = self.target_client.create_issue(issue)
            id_mapping[issue["source_id"]] = result["id"]
            self.log(f"Created: {result['id']}")

        return id_mapping

    def migrate_links(self, id_mapping: Dict[str, str]):
        """Migrate issue links using ID mapping"""
        # Implementation depends on source/target tools
        pass

    def migrate_attachments(self, issues: List[Dict], id_mapping: Dict):
        """Migrate attachments separately"""
        # Download from source, upload to target
        pass

    def validate(self, id_mapping: Dict[str, str]) -> Dict:
        """Validate migration completeness"""
        return {
            "total_source": len(id_mapping),
            "total_target": self.target_client.count_issues(),
            "missing": self._find_missing(id_mapping)
        }
```

### 5. Rollback Planning

**Rollback Strategy:**
```yaml
rollback_triggers:
  - data_loss_detected: immediate
  - critical_integration_failure: immediate
  - team_productivity_drop_50_percent: 48_hours
  - user_adoption_under_30_percent: 1_week

rollback_procedure:
  immediate:
    - pause_migration
    - notify_stakeholders
    - assess_damage
    - restore_source_access
    - document_failure

  planned:
    - disable_target_tool
    - sync_any_new_data_back
    - re_enable_source
    - communicate_timeline
    - reschedule_migration

data_preservation:
  - keep_source_read_only_30_days
  - export_target_data_before_rollback
  - document_mapping_for_retry
```

### 6. Change Management

**Communication Plan:**
```yaml
communications:
  - timing: "4 weeks before"
    audience: "all users"
    message: "Migration announcement"
    channel: ["email", "slack", "meeting"]

  - timing: "2 weeks before"
    audience: "all users"
    message: "Training schedule"
    channel: ["email", "calendar"]

  - timing: "1 week before"
    audience: "all users"
    message: "Final preparation checklist"
    channel: ["email", "slack"]

  - timing: "migration day"
    audience: "all users"
    message: "Go-live announcement"
    channel: ["email", "slack", "meeting"]

  - timing: "daily for 2 weeks"
    audience: "all users"
    message: "Daily tips and support"
    channel: ["slack"]
```

**Training Program:**
```yaml
training_tracks:
  basic_user:
    duration: 1_hour
    topics:
      - new_tool_navigation
      - creating_issues
      - updating_status
      - finding_your_work
    format: live_demo

  power_user:
    duration: 2_hours
    topics:
      - advanced_search
      - custom_views
      - automation_basics
      - integrations
    format: workshop

  admin:
    duration: 4_hours
    topics:
      - configuration
      - permissions
      - automation_rules
      - reporting
      - troubleshooting
    format: hands_on
```

## Best Practices

### Planning
1. **Involve stakeholders early** - Get buy-in before starting
2. **Document everything** - Current state, decisions, mappings
3. **Plan for parallel run** - Keep both tools temporarily
4. **Identify champions** - Power users to help others

### Data Migration
1. **Clean before migrating** - Don't migrate garbage
2. **Archive old data** - Don't migrate everything
3. **Test thoroughly** - Multiple test migrations
4. **Validate counts** - Ensure nothing lost

### Team Transition
1. **Training before cutover** - Everyone should be ready
2. **Support desk** - Dedicated help during transition
3. **Feedback loops** - Quick iteration on issues
4. **Celebrate milestones** - Acknowledge progress

### Risk Mitigation
1. **Rollback plan** - Always have exit strategy
2. **Incremental migration** - Migrate in waves
3. **Freeze period** - No changes during migration
4. **Audit trail** - Track all migration activities

## Templates/Examples

### Migration Project Plan

```markdown
# PM Tool Migration: Jira → Linear

## Project Overview
**Objective:** Migrate from Jira to Linear by Q2 2024
**Sponsor:** VP Engineering
**PM:** [Name]
**Timeline:** 12 weeks

## Scope
### In Scope
- All active projects (15)
- Issues from last 2 years
- Attachments under 10MB
- Key automations

### Out of Scope
- Archived projects
- Closed issues > 2 years
- Custom Jira plugins
- Time tracking data

## Timeline
| Phase | Duration | Dates | Owner |
|-------|----------|-------|-------|
| Planning | 2 weeks | Jan 1-14 | PM |
| Setup | 2 weeks | Jan 15-28 | Admin |
| Pilot | 2 weeks | Feb 1-14 | Team A |
| Migration | 4 weeks | Feb 15 - Mar 14 | PM |
| Cutover | 1 week | Mar 15-21 | All |
| Stabilization | 3 weeks | Mar 22 - Apr 11 | Support |

## Risk Register
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Data loss | High | Low | Multiple backups |
| Team resistance | Medium | Medium | Training + champions |
| Integration breaks | High | Medium | Test all integrations |
| Timeline slip | Medium | Medium | Buffer time included |

## Success Criteria
- [ ] 100% active issues migrated
- [ ] All integrations working
- [ ] Team adoption > 80% by week 2
- [ ] No critical bugs in first month
```

### Field Mapping Spreadsheet

```markdown
## Jira → Linear Field Mapping

### Standard Fields
| Jira Field | Linear Field | Transformation | Validated |
|------------|--------------|----------------|-----------|
| Summary | Title | Direct copy | Yes |
| Description | Description | Markdown convert | Yes |
| Issue Type | Label | Map: Story→feature | Yes |
| Status | State | See status mapping | Yes |
| Priority | Priority | See priority mapping | Yes |
| Assignee | Assignee | Match by email | Yes |
| Reporter | - | Not migrated | N/A |
| Created | - | System generated | N/A |
| Updated | - | System generated | N/A |
| Sprint | Cycle | Match by date range | Yes |
| Epic Link | Project | Create Linear projects | Yes |
| Story Points | Estimate | Direct copy | Yes |

### Status Mapping
| Jira Status | Linear State |
|-------------|--------------|
| Open | Backlog |
| To Do | Todo |
| In Progress | In Progress |
| In Review | In Review |
| Done | Done |
| Won't Do | Canceled |

### Priority Mapping
| Jira Priority | Linear Priority |
|---------------|-----------------|
| Highest | Urgent |
| High | High |
| Medium | Medium |
| Low | Low |
| Lowest | No Priority |
```

### Cutover Checklist

```markdown
## Migration Cutover Checklist

### T-24 Hours
- [ ] Final data export from source
- [ ] Backup target environment
- [ ] Notify all users of timeline
- [ ] Prepare support team

### T-4 Hours
- [ ] Set source tool to read-only
- [ ] Run final migration sync
- [ ] Validate issue counts
- [ ] Test critical integrations

### T-0 (Go Live)
- [ ] Enable target tool for all users
- [ ] Send go-live announcement
- [ ] Support team on standby
- [ ] Monitor for errors

### T+1 Hour
- [ ] Check user login success
- [ ] Verify automations running
- [ ] Address immediate issues
- [ ] Update status to stakeholders

### T+24 Hours
- [ ] Review error logs
- [ ] Collect user feedback
- [ ] Document known issues
- [ ] Plan remediation

### T+1 Week
- [ ] User adoption metrics
- [ ] Complete missing migrations
- [ ] Conduct retrospective
- [ ] Plan source tool decommission
```

## References

- [Atlassian Migration Guide](https://support.atlassian.com/jira-cloud/docs/migrate-from-jira-server-to-jira-cloud/)
- [Linear Import](https://linear.app/docs/import)
- [Change Management (ADKAR)](https://www.prosci.com/methodology/adkar)
- [Data Migration Best Practices](https://www.oreilly.com/library/view/data-migration/9780470392164/)
