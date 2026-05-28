---
name: task-management
description: Manage personal tasks using OmniFocus via the `of` CLI. Use when discussing tasks, projects, inbox processing, GTD workflow, or adding/organizing to-dos.
---

# Task Management with OmniFocus

Manage the user's personal tasks and projects through the `of` CLI. Apply GTD principles to clarify work.

**Use for:** Tasks, inbox processing, project planning, follow-ups, meeting action items
**Not for:** Code implementation planning, technical architecture

## CLI Reference

### Inbox

```bash
of inbox ls                      # List inbox items
of inbox count                   # Get inbox count
of inbox add "Task name"         # Quick capture
of inbox add "Task" --note "Details" --due "Friday" --flagged
```

### Tasks

```bash
of task ls                       # List all tasks
of task ls --flagged             # Flagged tasks only
of task ls --project "ProjectName"
of task ls --tag "waiting"
of task create "Task" --project "Project" --tag "home" --due "tomorrow"
of task view "task-id"
of task update "task-id" --flagged --due "next week"
of task delete "task-id"
```

### Projects

```bash
of project ls                    # List active projects
of project ls --folder "Work"
of project create "Project Name" --folder "Area" --sequential
of project update "project-id" --status "on hold"
```

### Search & Views

```bash
of search "keyword"              # Search tasks by name/note
of perspective ls                # List perspectives
of perspective view "Today"      # View tasks in perspective
```

### Tags & Folders

```bash
of tag ls                        # List tags with usage
of folder ls                     # Folder hierarchy
```

### Date Formats

Flexible: `today`, `tomorrow`, `Friday`, `next week`, `in 3 days`, `2024-01-15`, `Jan 15`

## Action Clarity

Transform vague into concrete:

| Vague                   | Concrete                            |
| ----------------------- | ----------------------------------- |
| "Follow up with client" | "Draft email about contract terms"  |
| "Handle the thing"      | "Call vendor about pricing"         |
| "Work on presentation"  | "Outline three key points for deck" |

Focus on effort, not results:

| Outcome-focused  | Controllable                          |
| ---------------- | ------------------------------------- |
| "Close the deal" | "Send proposal by Tuesday"            |
| "Get approval"   | "Submit complete proposal for review" |

**Project vs Single Action**: If multiple steps required, it's a project. Always identify the immediate next action first.

## Common Workflows

**Quick Capture**: `of inbox add "The thing they mentioned"`

**Process Inbox**: Review each item, decide: delete, do now, delegate, defer, or file with `of task update "item-id" --project "Relevant Project"`

**Weekly Review**: `of project ls` + `of task ls --tag "waiting"` + `of perspective view "Review"`

## Communication Style

Frame naturally: "Sounds like the next step is drafting that email?" / "Should I add that to your inbox?"

Avoid: "Here's your GTD structure with contexts..."

## Principles

- **Concrete beats vague**: Actual next step, not intention
- **Controllable beats outcome**: Effort over results
- **Capture beats remember**: Get it into OmniFocus immediately
