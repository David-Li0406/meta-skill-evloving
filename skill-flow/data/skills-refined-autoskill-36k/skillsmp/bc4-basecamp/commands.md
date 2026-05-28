# BC4 Command Reference

## Account & Authentication

```bash
bc4 auth status              # Check authentication state
bc4 auth login               # Authenticate with Basecamp
bc4 account list             # List all accounts
bc4 profile                  # Show current user profile
```

## Projects

```bash
bc4 project list             # List all projects
bc4 project select           # Interactively select default project
bc4 project set <id>         # Set default project by ID
```

## Todos

### Listing & Viewing
```bash
bc4 todo lists                        # List all todo lists
bc4 todo list                         # Todos in default list
bc4 todo list "List Name"             # Todos in named list
bc4 todo list --grouped               # Grouped by sections
bc4 todo view <id>                    # View single todo details
bc4 todo attachments <id>             # List todo attachments
```

### Creating & Managing
```bash
bc4 todo add "Description"            # Quick create todo
bc4 todo add "Task" --list "List"     # Create in specific list
bc4 todo add "Task" --assignee "Name" # Create with assignee
bc4 todo add "Task" --due "2024-01-15"# Create with due date
bc4 todo edit <id>                    # Edit todo interactively
bc4 todo check <id>                   # Mark complete
bc4 todo uncheck <id>                 # Mark incomplete
bc4 todo move <id>                    # Move todo position
```

### Todo Lists & Groups
```bash
bc4 todo create-list "New List"       # Create todo list
bc4 todo edit-list <id>               # Edit todo list
bc4 todo create-group "Group Name"    # Create group in list
bc4 todo reposition-group <id>        # Reposition group
bc4 todo select                       # Select default todo list
bc4 todo set <list-id>                # Set default todo list
```

## Cards (Kanban)

### Listing & Viewing
```bash
bc4 card list                         # List card tables
bc4 card table "Table Name"           # View cards in table
bc4 card view <id>                    # View card details + steps
bc4 card attachments <id>             # List card attachments
```

### Creating & Managing
```bash
bc4 card add "Title"                  # Quick card creation
bc4 card create                       # Interactive creation
bc4 card edit <id>                    # Edit card title/content
bc4 card move <id> --column "Name"    # Move to column
bc4 card archive <id>                 # Archive a card
bc4 card assign <id>                  # Assign people
bc4 card unassign <id>                # Remove assignees
```

### Card Steps
```bash
bc4 card step list <card-id>          # List steps
bc4 card step add <card-id> "Step"    # Add step
bc4 card step check <step-id>         # Complete step
bc4 card step uncheck <step-id>       # Uncomplete step
```

### Columns
```bash
bc4 card column list <table-id>       # List columns
bc4 card column add "Column Name"     # Add column
bc4 card column rename <id> "New"     # Rename column
```

## Messages & Documents

```bash
bc4 message post                      # Post message (interactive)
bc4 message list                      # List messages
bc4 message view <id>                 # View message
bc4 document list                     # List documents
bc4 document view <id>                # View document
```

## Campfire (Team Chat)

```bash
bc4 campfire post "Message"           # Quick post to campfire
bc4 campfire list                     # List recent messages
```

## Comments

```bash
# Add comment to any resource type
bc4 comment add todo <id> "Comment"
bc4 comment add card <id> "Comment"
bc4 comment add message <id> "Comment"

# List comments
bc4 comment list todo <id>
bc4 comment list card <id>
```

## Output Formats

All commands support `--json` for machine-readable output:
```bash
bc4 todo list --json | jq '.[] | .title'
bc4 card table "Bugs" --json
```
