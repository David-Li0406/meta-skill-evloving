---
id: trello-kanban
name: "Trello Kanban"
domain: PM
skill: faion-project-manager
category: "pm-tools"
---

# Trello Kanban

## Overview

Trello is a visual, card-based project management tool ideal for kanban workflows. Its simplicity, intuitive interface, and Power-Up ecosystem make it accessible for teams new to project management while still offering advanced features through automation and integrations.

## When to Use

- Small to medium teams needing simple task tracking
- Visual thinkers preferring card-based management
- Teams practicing Kanban methodology
- Projects requiring quick onboarding
- Cross-functional teams with diverse tech skills

## Process/Steps

### 1. Board Structure

**Basic Kanban Structure:**
```
Board: [Project Name]
├── Backlog
├── To Do (This Sprint)
├── In Progress (WIP: 3)
├── In Review
├── Testing
└── Done
```

**Enhanced Structure:**
```
Board: Product Development
├── Icebox (Future Ideas)
├── Backlog (Prioritized)
├── Ready for Dev
├── In Development [WIP: 3]
├── Code Review [WIP: 2]
├── QA Testing [WIP: 2]
├── Ready for Deploy
├── Done (Current Sprint)
└── Archive
```

### 2. Card Anatomy

```yaml
card_structure:
  title: "Clear, actionable title"

  labels:
    - type: ["Feature", "Bug", "Tech Debt", "Docs"]
    - priority: ["Urgent", "High", "Medium", "Low"]
    - team: ["Frontend", "Backend", "Design"]

  members:
    - assigned_to: ["@dev1", "@dev2"]

  due_date:
    start: "2024-01-15"
    due: "2024-01-20"

  description: |
    ## Context
    [Background information]

    ## Acceptance Criteria
    - [ ] Criterion 1
    - [ ] Criterion 2

    ## Resources
    - [Design mockup](link)
    - [API spec](link)

  checklists:
    - name: "Implementation Tasks"
      items:
        - "Setup project structure"
        - "Implement API endpoint"
        - "Write unit tests"

  attachments:
    - "design.png"
    - "requirements.pdf"

  custom_fields:
    story_points: 5
    sprint: "Sprint 24"
```

### 3. Labels Configuration

**Recommended Label System:**
```yaml
labels:
  # Type (left side of card)
  - name: "Feature"
    color: green

  - name: "Bug"
    color: red

  - name: "Tech Debt"
    color: orange

  - name: "Documentation"
    color: purple

  # Priority (differentiate by shade)
  - name: "P0 - Critical"
    color: red

  - name: "P1 - High"
    color: orange

  - name: "P2 - Medium"
    color: yellow

  - name: "P3 - Low"
    color: blue

  # Status indicators
  - name: "Blocked"
    color: black

  - name: "Needs Discussion"
    color: pink

  - name: "Quick Win"
    color: lime
```

### 4. Power-Ups

**Essential Power-Ups:**

| Power-Up | Purpose | Configuration |
|----------|---------|---------------|
| **Butler** | Automation | Rules, buttons, calendar commands |
| **Custom Fields** | Extra metadata | Story points, sprint, effort |
| **Calendar** | Timeline view | Due date visualization |
| **Card Aging** | Stale card detection | Highlight untouched cards |
| **Voting** | Prioritization | Team voting on features |
| **GitHub** | Code integration | Link PRs and commits |
| **Slack** | Notifications | Card updates to channels |

### 5. Butler Automation

**Rule Examples:**
```yaml
butler_rules:
  # Auto-assign on list move
  - trigger: "when a card is moved to 'In Development'"
    action: "add member @{creator} to the card"

  # Auto-label by list
  - trigger: "when a card is moved to 'Code Review'"
    action: "add the 'Needs Review' label to the card"

  # Due date reminder
  - trigger: "when a card is due in 1 day"
    action: "post comment '@card review this before due date'"

  # Complete checklist action
  - trigger: "when all checklists on a card are completed"
    action: "move the card to 'Done'"

  # Blocked notification
  - trigger: "when the 'Blocked' label is added to a card"
    action: "post comment 'This card is blocked! Please add details in comments.'"
```

**Button Examples:**
```yaml
butler_buttons:
  # Card button: Start Work
  - name: "Start Work"
    actions:
      - "move the card to 'In Development'"
      - "add me to the card"
      - "set due date to 3 working days from now"

  # Card button: Submit for Review
  - name: "Submit for Review"
    actions:
      - "move the card to 'Code Review'"
      - "add the 'Needs Review' label"
      - "remove me from the card"
      - "add @reviewer to the card"

  # Board button: Archive Done Cards
  - name: "Archive Completed"
    actions:
      - "archive all cards in list 'Done'"
```

### 6. Custom Fields Setup

```yaml
custom_fields:
  - name: "Story Points"
    type: number
    show_on_front: true

  - name: "Sprint"
    type: dropdown
    options: ["Sprint 1", "Sprint 2", "Sprint 3", "Backlog"]

  - name: "Estimate"
    type: dropdown
    options: ["XS", "S", "M", "L", "XL"]

  - name: "Component"
    type: dropdown
    options: ["Frontend", "Backend", "API", "Database", "DevOps"]

  - name: "PR Link"
    type: text
```

### 7. Board Templates

**Sprint Board Template:**
```yaml
template: "Sprint Board"
lists:
  - "Sprint Backlog"
  - "In Progress"
  - "Review"
  - "Done"
  - "Sprint Info"

cards:
  - list: "Sprint Info"
    cards:
      - name: "Sprint Goal"
        description: "[Sprint objective]"
      - name: "Sprint Capacity"
        description: |
          | Member | Days |
          |--------|------|
          | @dev1 | 10 |
      - name: "Sprint Metrics"
        checklist:
          - "Velocity: X points"
          - "Committed: X points"
          - "Completed: X points"
```

## Best Practices

### Board Organization
1. **Limit lists** - 5-7 lists maximum
2. **Clear WIP limits** - Add to list names: "In Progress (WIP: 3)"
3. **Consistent naming** - Use verb phrases for actionable lists
4. **Archive regularly** - Move done cards to keep board clean

### Card Quality
1. **Atomic cards** - One deliverable per card
2. **Clear titles** - Action-oriented, specific
3. **Description template** - Use consistently
4. **Checklists for subtasks** - Break down work

### Labels Strategy
1. **Color meaning** - Consistent color coding
2. **Limited labels** - 8-12 maximum
3. **Single type per card** - Feature OR Bug, not both
4. **Update labels** - Remove resolved states

### Team Workflow
1. **Daily board review** - Virtual standup via board
2. **Card comments** - Async communication
3. **Due dates** - Set realistic deadlines
4. **Archive sprints** - Create new boards or archive lists

## Templates/Examples

### Card Template: Feature

```markdown
## Feature: {Title}

### User Story
As a [user type], I want [capability] so that [benefit].

### Acceptance Criteria
- [ ] Users can...
- [ ] System validates...
- [ ] Error messages show...

### Design
- [Figma mockup](link)
- [Flow diagram](link)

### Technical Notes
- API endpoint: /api/v1/...
- Database changes: None
- Dependencies: None

### Definition of Done
- [ ] Code complete
- [ ] Tests written
- [ ] PR approved
- [ ] Deployed to staging
- [ ] PO accepted
```

### Card Template: Bug

```markdown
## Bug: {Title}

### Description
Brief description of the issue.

### Steps to Reproduce
1. Navigate to...
2. Click...
3. Observe...

### Expected Behavior
What should happen.

### Actual Behavior
What actually happens.

### Environment
- Version: X.Y.Z
- Browser: Chrome 120
- OS: macOS 14

### Screenshots
[Attach images]

### Severity
- [x] Critical (System down)
- [ ] High (Major feature broken)
- [ ] Medium (Workaround exists)
- [ ] Low (Cosmetic)

### Root Cause
[To be filled during investigation]
```

### Sprint Planning Card

```markdown
## Sprint {N} Planning

### Sprint Goal
[One sentence objective]

### Duration
{Start Date} - {End Date}

### Capacity
| Member | Days Available | Hours/Day | Focus |
|--------|----------------|-----------|-------|
| @dev1 | 10 | 6 | Backend |
| @dev2 | 8 | 6 | Frontend |

**Total Capacity:** XX hours

### Committed Work
Total Story Points: XX

### Risks
- Risk 1: [mitigation]
- Risk 2: [mitigation]

### Sprint Board
[Link to sprint board]
```

### Butler Automation Recipes

```yaml
# Complete sprint workflow
recipe_1:
  name: "Sprint Card Flow"
  rules:
    - trigger: "card created in Sprint Backlog"
      actions:
        - "add Sprint 24 custom field"
        - "add checklist 'Definition of Done'"

    - trigger: "card moved to In Progress"
      actions:
        - "start due date"
        - "add current member"

    - trigger: "card moved to Done"
      actions:
        - "mark due date complete"
        - "remove all labels"

# Stale card management
recipe_2:
  name: "Stale Card Alert"
  rules:
    - trigger: "card has no activity for 7 days"
      conditions:
        - "card is not in Done"
      actions:
        - "add 'Stale' label"
        - "post comment 'This card has been inactive for 7 days'"

# Blocked item escalation
recipe_3:
  name: "Blocked Escalation"
  rules:
    - trigger: "'Blocked' label added"
      actions:
        - "move to top of list"
        - "add @manager to card"
        - "post comment 'BLOCKED: Please add details'"
```

### API Integration

```javascript
// Trello API - Create Card
const response = await fetch(
  `https://api.trello.com/1/cards?key=${API_KEY}&token=${TOKEN}`,
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: 'New Feature Card',
      desc: '## Description\nFeature details here',
      idList: 'list-id',
      idLabels: ['label-id-1', 'label-id-2'],
      due: '2024-01-20T12:00:00.000Z',
      idMembers: ['member-id']
    })
  }
);

// Move Card to List
await fetch(
  `https://api.trello.com/1/cards/${cardId}?key=${API_KEY}&token=${TOKEN}`,
  {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      idList: 'new-list-id'
    })
  }
);

// Add Checklist
await fetch(
  `https://api.trello.com/1/checklists?key=${API_KEY}&token=${TOKEN}`,
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      idCard: 'card-id',
      name: 'Definition of Done',
      pos: 'top'
    })
  }
);
```

## References

- [Trello Documentation](https://support.atlassian.com/trello/)
- [Trello Power-Ups](https://trello.com/power-ups)
- [Butler Automation](https://trello.com/butler)
- [Trello REST API](https://developer.atlassian.com/cloud/trello/rest/)
- [Trello Templates](https://trello.com/templates)
