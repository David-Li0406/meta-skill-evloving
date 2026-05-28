# Database/ Folder Schemas

Complete property definitions and relationship patterns for the standardized Database/ folder structure.

## Overview

The Database/ folder contains six interconnected databases for managing tasks, projects, contacts, companies, meetings, and bookmarks. All use wikilinks for relationships and Obsidian Bases for dynamic views.

## Tasks

**Purpose**: Task management and tracking
**Location**: `Database/Tasks/`
**Base File**: `Database/Tasks.base`

### Properties

| Property | Type | Values | Description |
|----------|------|--------|-------------|
| `type` | text | `"task"` | Entity classification (required) |
| `status` | select | `backlog`, `active`, `blocked`, `done` | Task state |
| `priority` | select | `urgent`, `high`, `medium`, `low` | Task priority |
| `assignee` | link | `[[Database/People/Name]]` | Person assigned to task |
| `project` | link | `[[Database/Projects/Name]]` | Related project |
| `due` | date | YYYY-MM-DD | Due date |
| `created` | date | YYYY-MM-DD | Creation date |
| `tags` | list | Array of tags | Categorization |

### Common Formulas

```yaml
formulas:
  is_overdue: due && due < today() && status == "active"
  days_until_due: 'due ? (due - today()).format("days") : ""'
  status_emoji: 'status == "done" ? "✅" : status == "active" ? "🔄" : status == "blocked" ? "🚫" : "📋"'
```

### Relationships

- **Tasks → Projects**: via `project` property
- **Tasks → People**: via `assignee` property

### Example Entry

```yaml
---
type: task
status: active
priority: high
assignee: "[[Database/People/Person-Name]]"
project: "[[Database/Projects/Project-Name]]"
due: 2026-01-20
created: 2026-01-14
tags:
  - task
  - status/active
---
```

## Projects

**Purpose**: Project management and planning
**Location**: `Database/Projects/`
**Base File**: `Database/Projects.base`

### Properties

| Property | Type | Values | Description |
|----------|------|--------|-------------|
| `type` | text | `"project"` | Entity classification (required) |
| `status` | select | `planning`, `active`, `on-hold`, `completed`, `archived` | Project state |
| `priority` | select | `urgent`, `high`, `medium`, `low` | Project priority |
| `lead` | link | `[[Database/People/Name]]` | Project lead |
| `team` | list | Array of people links | Team members |
| `start_date` | date | YYYY-MM-DD | Project start |
| `target_date` | date | YYYY-MM-DD | Target completion |
| `budget` | number | Dollar amount | Project budget |
| `total_tasks` | number | Count | Total tasks |
| `completed_tasks` | number | Count | Completed tasks |

### Common Formulas

```yaml
formulas:
  task_count: file.backlinks.filter(x => x.type == "task").length
  active_task_count: file.backlinks.filter(x => x.type == "task" && x.status == "active").length
  completion_rate: 'total_tasks > 0 ? ((completed_tasks / total_tasks) * 100).toFixed(0) + "%" : "N/A"'
  is_overdue: target_date && target_date < today() && status != "completed"
  days_until_target: 'target_date ? (target_date - today()).format("days") : ""'
```

### Relationships

- **Projects ← Tasks**: backlinks from tasks
- **Projects → People**: via `lead` and `team` properties

### Example Entry

```yaml
---
type: project
status: active
priority: high
lead: "[[Database/People/Project-Lead]]"
team:
  - "[[Database/People/Team-Member-1]]"
  - "[[Database/People/Team-Member-2]]"
start_date: 2026-01-01
target_date: 2026-03-01
budget: 50000
total_tasks: 20
completed_tasks: 5
tags:
  - project
---
```

## People

**Purpose**: Contact relationship management (CRM)
**Location**: `Database/People/`
**Base File**: `Database/People.base`

### Properties

| Property | Type | Values | Description |
|----------|------|--------|-------------|
| `type` | text | `"person"` | Entity classification (required) |
| `company` | link | `[[Database/Companies/Name]]` | Employer/affiliation |
| `role` | text | Job title | Position/role |
| `email` | text | Email address | Contact email |
| `linkedin` | text | URL | LinkedIn profile |
| `twitter` | text | Handle | Twitter/X handle |
| `location` | text | City/region | Geographic location |
| `relationship` | select | `team`, `contact`, `colleague`, `client`, `partner`, `investor` | Relationship type |
| `last_contact` | date | YYYY-MM-DD | Last interaction |
| `next_action` | text | Description | Follow-up action |

### Common Formulas

```yaml
formulas:
  full_contact: 'email || linkedin || twitter ? "✓" : "✗"'
  interaction_count: file.backlinks.length
  days_since_last_contact: 'last_contact ? (today() - last_contact).format("days") : ""'
```

### Relationships

- **People → Companies**: via `company` property
- **People ← Tasks**: backlinks from assigned tasks
- **People ← Projects**: backlinks from projects they lead/join

### Example Entry

```yaml
---
type: person
company: "[[Database/Companies/Company-Name]]"
role: Job Title
email: person@company.com
linkedin: https://linkedin.com/in/username
location: City, Country
relationship: team
last_contact: 2026-01-14
tags:
  - person
  - team
---
```

## Companies

**Purpose**: Company relationship management (CRM)
**Location**: `Database/Companies/`
**Base File**: `Database/Companies.base`

### Properties

| Property | Type | Values | Description |
|----------|------|--------|-------------|
| `type` | text | `"company"` | Entity classification (required) |
| `industry` | text | Industry name | Industry/sector |
| `stage` | select | `seed`, `series-a`, `series-b`, `series-c`, `public`, `private` | Funding stage |
| `size` | text | Range | Employee count (e.g., "1-10", "50-200") |
| `website` | text | URL | Company website |
| `linkedin` | text | URL | LinkedIn page |
| `relationship` | select | `internal`, `prospect`, `partner`, `client`, `vendor`, `investor` | Relationship type |
| `last_interaction` | date | YYYY-MM-DD | Last contact |
| `next_action` | text | Description | Follow-up action |

### Common Formulas

```yaml
formulas:
  people_count: file.backlinks.filter(x => x.type == "person").length
  has_website: 'website ? "✓" : "✗"'
  contact_status: 'people_count > 0 ? people_count + " contacts" : "No contacts"'
```

### Relationships

- **Companies ← People**: backlinks from people working there

### Example Entry

```yaml
---
type: company
industry: Industry Name
stage: seed
size: 1-10
website: https://company.com
relationship: client
last_interaction: 2026-01-14
tags:
  - company
---
```

## Meetings

**Purpose**: Meeting notes and scheduling
**Location**: `Database/Meetings/`
**Base File**: `Database/Meetings.base`

### Properties

| Property | Type | Values | Description |
|----------|------|--------|-------------|
| `type` | text | `"meeting"` | Entity classification (required) |
| `meeting_date` | datetime | YYYY-MM-DD HH:mm | Meeting date/time |
| `meeting_type` | select | `team`, `client`, `standup`, `1on1`, `planning`, `review` | Meeting category |
| `attendees` | list | Array of people links | Participants |
| `organizer` | link | `[[Database/People/Name]]` | Meeting organizer |
| `project` | link | `[[Database/Projects/Name]]` | Related project |
| `company` | link | `[[Database/Companies/Name]]` | Related company |
| `status` | select | `scheduled`, `completed`, `cancelled` | Meeting status |
| `duration` | text | Duration | Length (e.g., "1h", "30min") |
| `location` | text | Location/URL | Physical or virtual location |
| `recording` | text | URL | Recording link |

### Common Formulas

```yaml
formulas:
  days_until_meeting: 'meeting_date ? (meeting_date - today()).format("days") : ""'
  is_upcoming: 'meeting_date && meeting_date >= today()'
  is_past: 'meeting_date && meeting_date < today()'
  attendee_count: 'attendees ? attendees.length : 0'
```

### Relationships

- **Meetings → People**: via `attendees` and `organizer`
- **Meetings → Projects**: via `project` property
- **Meetings → Companies**: via `company` property

### Example Entry

```yaml
---
type: meeting
meeting_date: 2026-01-15 14:00
meeting_type: planning
attendees:
  - "[[Database/People/Attendee-1]]"
  - "[[Database/People/Attendee-2]]"
organizer: "[[Database/People/Organizer]]"
project: "[[Database/Projects/Project-Name]]"
status: scheduled
duration: 1h
location: Zoom
tags:
  - meeting
  - planning
---
```

## Bookmarks

**Purpose**: URL bookmarks and reading list
**Location**: `Database/Bookmarks/`
**Base File**: `Database/Bookmarks.base`

### Properties

| Property | Type | Values | Description |
|----------|------|--------|-------------|
| `type` | text | `"bookmark"` | Entity classification (required) |
| `url` | text | URL | Full URL |
| `category` | text | Category | Topic/category |
| `description` | text | Description | Brief description |
| `saved` | checkbox | true/false | Content saved/read |
| `rating` | number | 1-5 | Rating (stars) |
| `last_accessed` | date | YYYY-MM-DD | Last access date |

### Common Formulas

```yaml
formulas:
  domain: 'url ? url.split("/")[2] : ""'
  is_saved: 'saved ? "✓" : "✗"'
  days_since_added: '(today() - file.ctime).format("days")'
```

### Example Entry

```yaml
---
type: bookmark
url: https://help.obsidian.md/bases
category: documentation
description: Official Obsidian Bases documentation
saved: true
rating: 5
last_accessed: 2026-01-14
tags:
  - bookmark
  - obsidian
  - reference
---
```

## Relationship Patterns

### Task → Project

```yaml
# In Database/Tasks/task-name.md
project: "[[Database/Projects/Project-Name]]"
```

View project's tasks:
```yaml
filters:
  and:
    - file.inFolder("Database/Tasks")
    - project == link(this.file)
```

### Task → Person (Assignee)

```yaml
# In Database/Tasks/task-name.md
assignee: "[[Database/People/Person-Name]]"
```

View person's tasks:
```yaml
filters:
  and:
    - file.inFolder("Database/Tasks")
    - assignee == link(this.file)
```

### Project → People (Lead & Team)

```yaml
# In Database/Projects/project-name.md
lead: "[[Database/People/Lead-Name]]"
team:
  - "[[Database/People/Member-1]]"
  - "[[Database/People/Member-2]]"
```

### Person → Company

```yaml
# In Database/People/person-name.md
company: "[[Database/Companies/Company-Name]]"
```

View company's contacts:
```yaml
filters:
  and:
    - file.inFolder("Database/People")
    - company == link(this.file)
```

### Meeting → Multiple Entities

```yaml
# In Database/Meetings/meeting-name.md
attendees:
  - "[[Database/People/Person-1]]"
  - "[[Database/People/Person-2]]"
project: "[[Database/Projects/Project-Name]]"
company: "[[Database/Companies/Company-Name]]"
```

## Best Practices

### Required Properties

Always set these for each entity type:
- `type` - Enables filtering by entity type
- Entity-specific required fields (see above)

### Naming Conventions

**Files**: Use descriptive names
- Tasks: `Add-Authentication-Feature.md`, `Fix-Bug-123.md`
- Projects: `AGI-Assistant.md`, `Q1-2026-Planning.md`
- People: `Team-Member.md`, `Team-Member-2.md`
- Companies: `Placeholder-Labs.md`, `Anthropic.md`
- Meetings: `2026-01-15-Weekly-Planning.md`
- Bookmarks: `Obsidian-Bases-Docs.md`

**Properties**: Use lowercase with underscores
- Good: `due_date`, `last_contact`, `meeting_type`
- Avoid: `dueDate`, `LastContact`, `MeetingType`

### Link Formatting

Always use full paths for clarity:
```yaml
# Good
assignee: "[[Database/People/Team-Member]]"
project: "[[Database/Projects/AGI-Assistant]]"

# Avoid (ambiguous)
assignee: "[[Team Member]]"
project: "[[AGI Assistant]]"
```

### Date Handling

Use ISO format for consistency:
```yaml
# Good
due: 2026-01-20
meeting_date: 2026-01-15 14:00

# Avoid
due: 01/20/2026
meeting_date: Jan 15, 2026 2:00 PM
```

### Tags

Use consistent tag hierarchies:
```yaml
tags:
  - entity-type       # task, project, person, company, meeting, bookmark
  - status/state      # status/active, status/done
  - category          # ai, infrastructure, research
  - team/member       # team/member1, team/member2
```
