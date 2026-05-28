---
name: epic-story-planning
description: Epic and story planning with GitHub integration. This skill should be used when creating epics, detailing stories, managing acceptance criteria, or setting up GitHub issue templates. Triggers on "create epic", "plan epic", "detail story", "add gherkin", "acceptance criteria", "issue template".
---

# Epic and Story Planning

Provides structured planning workflows for epics and stories with GitHub issue integration and gherkin-based acceptance criteria.

## Planning Hierarchy

```text
Epic (strategic milestone)
├── Story 1 (user-facing feature)
│   ├── Gherkin scenarios
│   └── Tasks (implementation units)
├── Story 2
└── Story 3
```

## Epic Planning Workflow

1. **Define Epic Scope**
   - Clear business objective
   - Success criteria
   - Estimated complexity (DEEP: Days, not hours)

2. **Break Down into Stories**
   - Each story is independently deliverable
   - User-facing value per story
   - Linked to parent epic

3. **Create GitHub Issues**
   - Use epic.yml template for epics
   - Use story.yml template for stories
   - Apply appropriate labels

## Story Detailing Workflow

1. **User Story Format**
   ```text
   As a [user type]
   I want [feature]
   So that [benefit]
   ```

2. **Gherkin Acceptance Criteria**
   ```gherkin
   Feature: [Story title]

   Scenario: [Happy path]
     Given [context]
     When [action]
     Then [outcome]

   Scenario: [Edge case]
     Given [different context]
     When [action]
     Then [different outcome]
   ```

3. **Task Breakdown**
   - 15-30 minute implementation units
   - Clear done-when criteria
   - Dependencies identified

## GitHub Integration

### Issue Templates

Templates available in `templates/`:
- `epic.yml` - Epic creation with goals and criteria
- `story.yml` - Story creation with gherkin

### Label Strategy

| Label | Purpose |
|-------|---------|
| `type-epic` | Epic issues |
| `type-story` | Story issues |
| `status-planning` | In planning phase |
| `status-ready` | Ready for implementation |
| `priority-critical` | Critical priority |
| `priority-high` | High priority |
| `priority-medium` | Medium priority |
| `priority-low` | Low priority |

### Creating Issues

**Epic:**
```bash
gh issue create --template epic.yml --label "type-epic,status-planning"
```

**Story:**
```bash
gh issue create --template story.yml --label "type-story,status-planning" --milestone "Epic Name"
```

## References

- `references/gherkin-patterns.md` - Gherkin writing patterns
- `references/estimation-guide.md` - DEEP estimation methodology
