---
name: pms-domain
description: Project Management System domain knowledge including entities, business rules, workflows, and industry standards. Use for understanding PMS requirements, implementing features, and ensuring domain accuracy.
allowed-tools: Read, Grep
---

# PMS Domain Knowledge

## Core Entities

### Project
The container for all work items. Projects have:
- **Lifecycle:** Draft -> Active -> On Hold -> Completed -> Archived
- **Visibility:** Private (owner only), Team (members), Public (organization)
- **Key:** Unique identifier (e.g., "PMS-123" prefix for tasks)

### Task
The fundamental unit of work. Tasks have:
- **States:** Backlog -> Todo -> In Progress -> In Review -> Done
- **Types:** Story, Bug, Task, Epic, Subtask
- **Priority:** Critical, High, Medium, Low
- **Relationships:** Parent/child (subtasks), blocking/blocked by

### Sprint
Time-boxed iteration for Agile workflows:
- **Duration:** Typically 1-4 weeks
- **States:** Planning -> Active -> Review -> Closed
- **Metrics:** Velocity, burndown, completion rate

### User
System participant with role-based access:
- **Roles:** Super Admin, Org Admin, Project Manager, Team Member, Viewer
- **Attributes:** Profile, preferences, notification settings, timezone

## Business Rules

### Task Rules
1. Tasks must belong to exactly one project
2. Subtasks inherit project from parent
3. Task key is auto-generated: {PROJECT_KEY}-{SEQUENCE}
4. Completed tasks cannot be edited without reopening
5. Epic tasks can have Story/Task children but not Bug children
6. Circular blocking relationships are not allowed

### Sprint Rules
1. Sprint dates cannot overlap within a project
2. Tasks can only be in one active sprint at a time
3. Unfinished tasks roll over to next sprint on close
4. Sprint capacity based on team member availability
5. Retrospective required before starting new sprint

### Permission Rules
1. Project owners have full control
2. Only PM+ can manage sprint settings
3. Members can only assign tasks to themselves or unassigned
4. Viewers cannot modify any data
5. Deleted users' tasks become unassigned

## Workflows

### Task State Machine
```
                    +-----------------------------+
                    |                             |
                    v                             |
Backlog --> Todo --> In Progress --> In Review --> Done
   |         |           |               |
   |         |           |               |
   +---------+-----------+---------------+
           (can move backward)
```

### Sprint Workflow
```
1. Sprint Planning
   - Select tasks from backlog
   - Estimate story points
   - Set sprint goal
   - Assign to team members

2. Daily Standup
   - Update task status
   - Log blockers
   - Adjust assignments

3. Sprint Execution
   - Work on tasks
   - Log time (if enabled)
   - Update progress

4. Sprint Review
   - Demo completed work
   - Gather feedback
   - Update task status

5. Sprint Retrospective
   - What went well
   - What to improve
   - Action items

6. Sprint Close
   - Archive sprint
   - Move incomplete to backlog
   - Calculate velocity
```

## Metrics & Calculations

### Velocity
```
velocity = sum(completed_story_points) / num_sprints
rolling_velocity = average(last_3_sprints_velocity)
```

### Burndown
```
ideal_burndown[day] = total_points * (days_remaining / total_days)
actual_burndown[day] = remaining_points_at_day
```

### Cycle Time
```
cycle_time = task_completion_date - task_start_date
average_cycle_time = sum(cycle_times) / completed_tasks
```

### Lead Time
```
lead_time = task_completion_date - task_creation_date
```

## Common UI Patterns

### Kanban Board
- Columns represent states
- Cards are tasks
- Drag-drop to change state
- WIP limits per column
- Swimlanes by assignee/priority

### Sprint Board
- Similar to Kanban
- Scoped to active sprint
- Shows sprint progress
- Burndown chart visible

### Backlog View
- Prioritized list
- Drag to reorder
- Quick estimate
- Bulk actions
- Filter by various criteria

### Timeline/Gantt
- Tasks as horizontal bars
- Dependencies shown as arrows
- Drag to adjust dates
- Critical path highlighted
