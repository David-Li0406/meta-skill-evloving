# Azure Boards CLI Reference

## Work Item Queries

### az boards query

Query work items using WIQL.

```bash
# Using WIQL directly
az boards query --wiql "SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.TeamProject] = @project ORDER BY [System.ChangedDate] DESC"

# Common query patterns:

# My work items
az boards query --wiql "SELECT [System.Id], [System.Title], [System.State], [System.WorkItemType] FROM WorkItems WHERE [System.AssignedTo] = @Me AND [System.State] <> 'Closed' ORDER BY [System.ChangedDate] DESC"

# Active bugs
az boards query --wiql "SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.WorkItemType] = 'Bug' AND [System.State] = 'Active'"

# Items in current sprint
az boards query --wiql "SELECT [System.Id], [System.Title] FROM WorkItems WHERE [System.IterationPath] UNDER @CurrentIteration"

# Recently updated
az boards query --wiql "SELECT [System.Id], [System.Title] FROM WorkItems WHERE [System.ChangedDate] >= @Today - 7 ORDER BY [System.ChangedDate] DESC"

# Using saved query ID
az boards query --id <query-id>

# Using saved query path
az boards query --path "Shared Queries/My Query"
```

**WIQL Field References:**

- `[System.Id]` - Work item ID
- `[System.Title]` - Title
- `[System.State]` - State (New, Active, Closed, etc.)
- `[System.AssignedTo]` - Assigned user
- `[System.WorkItemType]` - Type (Bug, Task, User Story, etc.)
- `[System.IterationPath]` - Sprint/iteration
- `[System.AreaPath]` - Area path
- `[System.Tags]` - Tags
- `[System.ChangedDate]` - Last modified
- `[System.CreatedDate]` - Created date

**WIQL Macros:**

- `@Me` - Current user
- `@Today` - Today's date
- `@CurrentIteration` - Current sprint
- `@project` - Current project

## Work Items

### az boards work-item show

Show work item details.

```bash
az boards work-item show --id <work-item-id> [--open] [--expand all|relations|fields]
```

### az boards work-item create

Create a work item.

```bash
# Basic creation
az boards work-item create --title "Task title" --type "Task"

# With description and assignment
az boards work-item create \
  --title "Fix login bug" \
  --type "Bug" \
  --description "Users cannot login with SSO" \
  --assigned-to user@email.com

# With area and iteration
az boards work-item create \
  --title "New feature" \
  --type "User Story" \
  --area "Project\\Team" \
  --iteration "Project\\Sprint 1"

# With additional fields
az boards work-item create \
  --title "Critical bug" \
  --type "Bug" \
  --fields "System.Tags=urgent;production" "Microsoft.VSTS.Common.Priority=1"
```

**Common work item types:**

- `Task` - Development task
- `Bug` - Bug/defect
- `User Story` - User story (Agile)
- `Product Backlog Item` - PBI (Scrum)
- `Feature` - Feature
- `Epic` - Epic
- `Issue` - Issue (Basic process)

### az boards work-item update

Update a work item.

```bash
# Update state
az boards work-item update --id <id> --state "In Progress"

# Update title
az boards work-item update --id <id> --title "New title"

# Update assignment
az boards work-item update --id <id> --assigned-to user@email.com

# Update area/iteration
az boards work-item update --id <id> --area "Project\\NewArea" --iteration "Project\\Sprint 2"

# Update multiple fields
az boards work-item update --id <id> --fields "System.Tags=tag1;tag2" "Microsoft.VSTS.Common.Priority=2"

# Update description
az boards work-item update --id <id> --description "Updated description"
```

### az boards work-item delete

Delete a work item.

```bash
az boards work-item delete --id <work-item-id> [--yes] [--destroy]
```

Note: `--destroy` permanently deletes; without it, item goes to recycle bin.

## Work Item Relations

### az boards work-item relation list-type

List available relation types.

```bash
az boards work-item relation list-type
```

Common relation types:

- `System.LinkTypes.Hierarchy-Forward` - Parent (child -> parent)
- `System.LinkTypes.Hierarchy-Reverse` - Child (parent -> child)
- `System.LinkTypes.Related` - Related
- `System.LinkTypes.Dependency-Forward` - Successor
- `System.LinkTypes.Dependency-Reverse` - Predecessor

### az boards work-item relation add

Add a relation.

```bash
# Link to parent
az boards work-item relation add \
  --id <work-item-id> \
  --relation-type "System.LinkTypes.Hierarchy-Forward" \
  --target-id <parent-id>

# Add related item
az boards work-item relation add \
  --id <work-item-id> \
  --relation-type "System.LinkTypes.Related" \
  --target-id <related-id>
```

### az boards work-item relation remove

Remove a relation.

```bash
az boards work-item relation remove \
  --id <work-item-id> \
  --relation-type "System.LinkTypes.Related" \
  --target-id <target-id>
```

### az boards work-item relation show

Show work item relations.

```bash
az boards work-item relation show --id <work-item-id>
```

## Area Paths

### az boards area project list

List area paths in project.

```bash
az boards area project list [--depth <n>]
```

### az boards area project show

Show area details.

```bash
az boards area project show --path "\\Project\\Area\\SubArea"
```

### az boards area project create

Create an area path.

```bash
az boards area project create --name "New Area" [--path "\\Project\\ParentArea"]
```

### az boards area project delete

Delete an area path.

```bash
az boards area project delete --path "\\Project\\Area" [--yes]
```

### az boards area team list

List areas for a team.

```bash
az boards area team list --team "Team Name"
```

### az boards area team add

Add area to team.

```bash
az boards area team add --team "Team Name" --path "\\Project\\Area" [--include-sub-areas true]
```

### az boards area team remove

Remove area from team.

```bash
az boards area team remove --team "Team Name" --path "\\Project\\Area"
```

## Iteration Paths (Sprints)

### az boards iteration project list

List iterations in project.

```bash
az boards iteration project list [--depth <n>]
```

### az boards iteration project show

Show iteration details.

```bash
az boards iteration project show --path "\\Project\\Sprint 1"
```

### az boards iteration project create

Create an iteration.

```bash
az boards iteration project create \
  --name "Sprint 5" \
  --path "\\Project" \
  [--start-date 2024-01-15] \
  [--finish-date 2024-01-29]
```

### az boards iteration project delete

Delete an iteration.

```bash
az boards iteration project delete --path "\\Project\\Sprint 5" [--yes]
```

### az boards iteration team list

List team iterations.

```bash
az boards iteration team list --team "Team Name"
```

### az boards iteration team add

Add iteration to team.

```bash
az boards iteration team add --team "Team Name" --id <iteration-id>
```

### az boards iteration team remove

Remove iteration from team.

```bash
az boards iteration team remove --team "Team Name" --id <iteration-id>
```

### az boards iteration team list-work-items

List work items in iteration.

```bash
az boards iteration team list-work-items --team "Team Name" --id <iteration-id>
```

### az boards iteration team set-backlog-iteration

Set backlog iteration for team.

```bash
az boards iteration team set-backlog-iteration --team "Team Name" --id <iteration-id>
```

### az boards iteration team set-default-iteration

Set default iteration for new work items.

```bash
az boards iteration team set-default-iteration --team "Team Name" --id <iteration-id>
```
