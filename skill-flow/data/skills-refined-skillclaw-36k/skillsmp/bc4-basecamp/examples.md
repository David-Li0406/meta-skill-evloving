# BC4 Workflow Examples

## Daily Task Management

### Morning standup - see what's pending
```bash
# Check your todos across lists
bc4 todo lists
bc4 todo list "Sprint Tasks"

# Check card tables for bugs/requests
bc4 card table "Bug Tracker"
```

### Complete a task and add notes
```bash
# Mark todo complete
bc4 todo check 12345

# Add a completion comment
bc4 comment add todo 12345 "Completed - deployed to production"
```

## Card Table Workflows

### Investigate and work on a card
```bash
# View card details
bc4 card view 67890

# Move to "In Progress"
bc4 card move 67890 --column "In Progress"

# Check off steps as you work
bc4 card step check 111
bc4 card step check 222

# Move to "Done" when complete
bc4 card move 67890 --column "Done"
```

### Create a new bug card
```bash
# Quick creation
bc4 card add "Fix: Login button unresponsive on mobile"

# Or interactive with more details
bc4 card create
```

### Add steps to a card
```bash
bc4 card step add 67890 "Reproduce the issue"
bc4 card step add 67890 "Identify root cause"
bc4 card step add 67890 "Implement fix"
bc4 card step add 67890 "Test on staging"
bc4 card step add 67890 "Deploy to production"
```

## Todo Management

### Create a todo with due date and assignee
```bash
bc4 todo add "Review PR #123" --due "2024-01-20" --assignee "John"
```

### Bulk view todos in a project
```bash
# See all grouped
bc4 todo list --grouped

# JSON output for processing
bc4 todo list --json | jq '.[] | select(.completed == false) | .title'
```

## Team Communication

### Quick update to team
```bash
bc4 campfire post "Deployed v2.1.0 to production - all green!"
```

### Post a formal announcement
```bash
bc4 message post
# Interactive prompts for title, content, category
```

## Project Context Switching

### Switch between projects
```bash
# See available projects
bc4 project list

# Select a different project
bc4 project select

# Or set directly by ID
bc4 project set 12345678
```

### Work on a specific project without changing default
```bash
# Override project for single command
bc4 todo list "Tasks" --project 12345678
bc4 card table "Bugs" --project 87654321
```

## Scripting & Automation

### Get card IDs for a column
```bash
bc4 card table "Development" --json | jq '.[] | select(.column == "Ready") | .id'
```

### Count incomplete todos
```bash
bc4 todo list --json | jq '[.[] | select(.completed == false)] | length'
```

### Export todos to CSV
```bash
bc4 todo list --json | jq -r '.[] | [.id, .title, .completed] | @csv'
```
