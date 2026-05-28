---
name: roadmap-manager
description: Manages the project roadmap in .dev/planning/ROADMAP.yaml. Use when adding tasks, completing tasks, updating status, generating reports, sprint planning, or any roadmap operations. Triggers on "add task", "complete task", "roadmap status", "what's next", "sprint planning", "mark done", "update roadmap".
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Roadmap Manager

You manage the project roadmap stored in `.dev/planning/ROADMAP.yaml`.

## File Locations

- **Main Roadmap**: `.dev/planning/ROADMAP.yaml`
- **Roles Reference**: `.dev/planning/ROLES.md`
- **Decisions Log**: `.dev/planning/DECISIONS.md`
- **Archive**: `.dev/planning/archive/YYYY-MM/`

## Task Schema

Each task in ROADMAP.yaml follows this structure:

```yaml
- id: prefix-NNN # Unique ID (e.g., seo-001, calc-002)
  title: "Short title" # What needs to be done
  description: "Details" # More context
  status: pending # pending | in_progress | blocked | completed | archived
  priority: medium # critical | high | medium | low
  assignee: "@claude" # @human | @claude | @agent:* | @tool:* | @skill:*
  effort: 4 # Hours estimated
  tags: [tag1, tag2] # Categorization
  dependencies: [id-xxx] # Tasks that must complete first
  notes: "Optional info" # Additional context
  completed_date: null # Set when completed
  subtasks: [] # Nested tasks if needed
```

## Operations

### Adding a Task

When the user says "add task for X" or "we need to do Y":

1. Read current ROADMAP.yaml
2. Determine appropriate section and subsection
3. Generate unique ID (section prefix + next number)
4. Ask for priority and effort if not specified
5. Add task with all required fields
6. Update `metadata.last_updated`
7. Confirm addition

Example:

```yaml
- id: seo-025
  title: "Add Open Graph meta tags"
  description: "Social media sharing optimization"
  status: pending
  priority: medium
  assignee: "@claude"
  effort: 2
  tags: [seo, social]
```

### Completing a Task

When the user says "mark X as done" or "completed task Y":

1. Find the task by ID or title match
2. Update status to `completed`
3. Add `completed_date: "YYYY-MM-DD"`
4. Update `metadata.last_updated`
5. Confirm completion

### Generating Status Report

When asked "roadmap status" or "what's our progress":

1. Read ROADMAP.yaml
2. Count tasks by status and priority
3. Calculate completion percentage per section
4. List high-priority pending items
5. Sum remaining effort estimates
6. Present clear summary

Output format:

```
## Roadmap Status (YYYY-MM-DD)

**Overall**: X/Y tasks completed (Z%)

### By Section
- SEO & Discovery: 3/15 (20%)
- Content & Calculators: 1/10 (10%)
- ...

### High Priority Pending
1. [seo-001] Add meta descriptions (@claude, 3h)
2. [eeat-001] Add author credentials (@human, 2h)

### Blocked Items
- None

### Estimated Remaining Effort: XXh
```

### Sprint Planning

When asked "plan next sprint" or "what should we work on":

1. Identify unblocked high/critical priority tasks
2. Consider dependencies
3. Balance human vs AI work
4. Sum to reasonable sprint capacity (e.g., 20h)
5. Create sprint plan in `.claude/sprints/current.md`

### Archive Operation

When tasks have been completed for over 30 days:

1. Move completed tasks to `.dev/planning/archive/YYYY-MM/`
2. Keep reference ID in main roadmap for history
3. Update archive index

## Role Assignment Guidelines

When adding tasks, assign based on:

- **@human**: Decisions, external accounts, medical expertise, approvals
- **@claude**: Code, documentation, technical implementation
- **@agent:explore**: Research, codebase analysis
- **@agent:business**: Market research, competitive analysis
- **@agent:architect**: System design, major refactors
- **@tool:playwright**: Test execution
- **@skill:commit**: Git operations

## Important Rules

1. Always preserve existing task IDs - never change them
2. Update `metadata.last_updated` on any change
3. Ask for clarification if priority/effort unclear
4. Check dependencies before marking tasks in_progress
5. Validate YAML syntax before saving
