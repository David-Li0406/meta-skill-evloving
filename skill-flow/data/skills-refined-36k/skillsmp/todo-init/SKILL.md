---
name: todo-init
description: Initialize todo tracking settings for the current project
trigger_keywords:
  - init todo
  - setup todo
  - configure todo
  - enable todo tracking
---

# Todo Init

## Purpose

Initialize and configure todo tracking for the current project by creating or updating the `.claude/todo-settings-local.json` configuration file.

## Execution Flow

### Phase 1: Check Existing Configuration

1. **Search for existing settings**:
   - Look for `.claude/todo-settings-local.json` in current directory
   - Search parent directories up to home

2. **If found**:
   ```json
   {
     "question": "Todo settings already exist. What would you like to do?",
     "header": "Existing Config",
     "options": [
       {"label": "View current settings", "description": "Display the current configuration"},
       {"label": "Update settings", "description": "Modify existing configuration"},
       {"label": "Reset to defaults", "description": "Overwrite with default settings"}
     ],
     "multiSelect": false
   }
   ```

3. **If not found**: Proceed to Phase 2

### Phase 2: Determine Todos Directory

Ask user where to store todo files:

```json
{
  "question": "Where should todo files be stored?",
  "header": "Todos Directory",
  "options": [
    {"label": "Auto-detect", "description": "Find existing Todos/ directory in knowledge base"},
    {"label": "Create new", "description": "Create Todos/ directory in specified location"},
    {"label": "Specify path", "description": "Enter a custom path for todos"}
  ],
  "multiSelect": false
}
```

**Auto-detect logic**:
1. Search for existing `Todos/` directory with `RULE.md`
2. If found, use that path
3. If not found, suggest creating one

**Create new logic**:
1. Ask for parent directory (knowledge base root)
2. Create `Todos/`, `Todos/active/`, `Todos/completed/`
3. Create governance files (RULE.md, README.md for each)

### Phase 3: Configure Tracking Options

```json
{
  "question": "Which directories should be tracked for todos?",
  "header": "Tracked Dirs",
  "options": [
    {"label": "All directories", "description": "Track all file operations in the project"},
    {"label": "Knowledge base only", "description": "Only track files in the knowledge base"},
    {"label": "Specific directories", "description": "Choose specific directories to track"}
  ],
  "multiSelect": false
}
```

If "Specific directories" selected:
- List available directories
- Allow multi-select

### Phase 4: Configure Detection Patterns

```json
{
  "question": "Use default detection patterns or customize?",
  "header": "Patterns",
  "options": [
    {"label": "Use defaults (Recommended)", "description": "Standard patterns for requests, deadlines, and actions"},
    {"label": "Customize patterns", "description": "Add or remove detection patterns"}
  ],
  "multiSelect": false
}
```

**Default patterns include**:
- Request: "please provide", "please reply", "need you to"
- Deadline: "by EOD", "deadline", "ASAP", "urgent"
- Action: "action item", "TODO", "follow up"

If customize:
- Show current patterns by category
- Allow add/remove for each category

### Phase 5: Configure Behavior

```json
{
  "question": "Configure additional settings",
  "header": "Options",
  "options": [
    {"label": "Require confirmation", "description": "Always ask before creating todos (Recommended)"},
    {"label": "Auto-create", "description": "Create todos without asking"}
  ],
  "multiSelect": false
}
```

```json
{
  "question": "Default priority for new todos?",
  "header": "Priority",
  "options": [
    {"label": "Medium (Recommended)", "description": "Standard priority unless urgency detected"},
    {"label": "High", "description": "Default to high priority"},
    {"label": "Low", "description": "Default to low priority"}
  ],
  "multiSelect": false
}
```

### Phase 6: Create Configuration File

1. **Ensure `.claude/` directory exists**:
   ```bash
   mkdir -p [project_root]/.claude
   ```

2. **Generate settings file**:
   ```json
   {
     "$schema": "https://json-schema.org/draft/2020-12/schema",
     "$comment": "Todo Tracker settings - managed by /todo-init",

     "enabled": true,

     "todos_directory": "[configured path]",

     "tracked_directories": [
       "[configured directories]"
     ],

     "patterns": {
       "request": ["..."],
       "deadline": ["..."],
       "action": ["..."]
     },

     "default_priority": "[selected priority]",

     "auto_due_date_detection": true,

     "confirmation_required": [true/false based on selection]
   }
   ```

3. **Write to `.claude/todo-settings-local.json`**

### Phase 7: Create Todos Directory Structure (if needed)

If creating new Todos directory:

1. **Create directory structure**:
   ```
   [todos_directory]/
   ├── RULE.md
   ├── README.md
   ├── active/
   │   └── README.md
   └── completed/
       └── README.md
   ```

2. **Create RULE.md**:
   ```markdown
   # Todos - Personal Task Management

   ## Purpose
   Centralized management of all todo items.

   ## Structure
   - active/: Active todos (pending, in_progress, blocked)
   - completed/: Archived completed todos

   ## Naming Convention
   YYYY-MM-DD_todo-title-slug.md

   ## Required Frontmatter
   - title: Brief description (required)
   - status: pending | in_progress | blocked | completed
   - priority: high | medium | low
   - created_at: YYYY-MM-DD

   ## Optional Fields
   - due_date: YYYY-MM-DD
   - source_file: Path to source file
   - source_type: email | document | meeting | manual
   - tags: List of tags
   - dependencies: List of dependent todos
   - related_files: Links to related files

   ## Allowed Operations
   - Create: Allowed
   - Update: Allowed (must update execution log)
   - Delete: Not allowed (archive to completed/ instead)
   - Move: Only between active/ and completed/
   ```

3. **Create README.md files** with initial content and indexes

### Phase 8: Report

```
Todo tracking initialized successfully!

Configuration:
- Settings file: [project_root]/.claude/todo-settings-local.json
- Todos directory: [todos_directory]
- Tracked directories: [list or "all"]
- Detection patterns: [count] patterns configured
- Confirmation required: [yes/no]
- Default priority: [priority]

The system will now automatically detect potential todos in your conversations.
When actionable items are detected, you will be asked to confirm before creating todos.

Available commands:
- /todo-add    - Manually add a new todo
- /todo-list   - View all active todos
- /todo-update - Update a todo
- /todo-complete - Mark a todo as complete
```

## Quick Setup

For users who want fast setup with defaults:

```
/todo-init --quick [todos_directory]
```

This will:
1. Create settings with all defaults
2. Set the specified todos directory
3. Enable tracking for all directories
4. Use default patterns
5. Require confirmation for todo creation

## Update Mode

When updating existing configuration:

```json
{
  "question": "What would you like to update?",
  "header": "Update",
  "options": [
    {"label": "Enable/Disable", "description": "Turn todo tracking on or off"},
    {"label": "Change directory", "description": "Update todos storage location"},
    {"label": "Update patterns", "description": "Add or remove detection patterns"},
    {"label": "Change behavior", "description": "Update confirmation and priority settings"}
  ],
  "multiSelect": true
}
```

## Error Handling

### Permission Denied

```
Cannot create settings file: Permission denied

Please ensure you have write access to:
[project_root]/.claude/

Or run the command from a directory where you have write permissions.
```

### Invalid Todos Directory

```
Invalid todos directory: [path]

The specified path does not exist or is not accessible.
Would you like to:
1. Create the directory
2. Specify a different path
```

### Settings Validation Failed

```
Settings validation failed:

- todos_directory: Path does not exist
- patterns.request: Must be an array

Please fix these issues and try again.
```

## Configuration Schema Reference

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["enabled"],
  "properties": {
    "enabled": {
      "type": "boolean",
      "description": "Enable or disable todo tracking"
    },
    "todos_directory": {
      "type": "string",
      "description": "Path to the Todos directory"
    },
    "tracked_directories": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Directories to track for todos (empty = all)"
    },
    "patterns": {
      "type": "object",
      "properties": {
        "request": {"type": "array", "items": {"type": "string"}},
        "deadline": {"type": "array", "items": {"type": "string"}},
        "action": {"type": "array", "items": {"type": "string"}}
      }
    },
    "default_priority": {
      "type": "string",
      "enum": ["high", "medium", "low"]
    },
    "auto_due_date_detection": {
      "type": "boolean"
    },
    "confirmation_required": {
      "type": "boolean"
    }
  }
}
```
