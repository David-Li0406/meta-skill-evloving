---
name: mcts-dataset
description: Manage the MCTS prompt dataset with CRUD operations, import/export, and reset functionality. Use for viewing, editing, backing up, and restoring prompt templates.
disable-model-invocation: true
---

# MCTS Prompt Dataset Manager

Manage your prompt dataset for MCTS operations.

## Available Operations

### 1. LIST - View all prompts
```
/mcts:mcts-dataset list
```
Use MCP tool: `mcts_dataset_list`

### 2. GET - Retrieve a specific prompt
```
/mcts:mcts-dataset get <prompt_id>
```
Use MCP tool: `mcts_dataset_get` with `prompt_id`

### 3. CREATE - Add a new prompt
```
/mcts:mcts-dataset create
```
Use MCP tool: `mcts_dataset_create` with:
- `name`: Prompt name/identifier
- `category`: Category (research/planning/coding/general)
- `template`: The prompt template text
- `description`: What this prompt is for
- `variables`: List of template variables (e.g., ["problem", "context"])

### 4. UPDATE - Modify an existing prompt
```
/mcts:mcts-dataset update <prompt_id>
```
Use MCP tool: `mcts_dataset_update` with:
- `prompt_id`: ID of prompt to update
- Fields to update (name, category, template, description, variables)

### 5. DELETE - Remove a prompt
```
/mcts:mcts-dataset delete <prompt_id>
```
Use MCP tool: `mcts_dataset_delete` with `prompt_id`

---

## EXPORT - Backup your dataset

**IMPORTANT: Always export before importing to avoid data loss!**

```
/mcts:mcts-dataset export
```
Use MCP tool: `mcts_dataset_export` with optional:
- `filepath`: Custom export path (default: mcts_prompts_backup_<timestamp>.json)
- `format`: json or yaml (default: json)

This creates a backup file you can use to restore your prompts.

---

## IMPORT - Load prompts from file

**WARNING: Import will merge with existing prompts. Duplicates will be overwritten.**

**Please export your current dataset first for backup!**

```
/mcts:mcts-dataset import <filepath>
```
Use MCP tool: `mcts_dataset_import` with:
- `filepath`: Path to the import file
- `merge_strategy`: "merge" (default) or "replace"
  - merge: Add new prompts, update existing by ID
  - replace: Clear all and import fresh

---

## RESET - Restore default prompts

**DANGER: This will DELETE all custom prompts and restore defaults!**

To reset, you must type "yes" to confirm:

```
/mcts:mcts-dataset reset
```

When prompted, type exactly: **yes**

This will:
1. Delete ALL current prompts (custom and modified)
2. Restore the original default prompt set
3. This action CANNOT be undone!

**Recommendation: Export your prompts before reset!**

---

## Operation: $ARGUMENTS

Execute the requested dataset operation using the appropriate MCP tools.

### For CREATE/UPDATE operations:
1. Ask user for the required fields
2. Validate the input
3. Execute the operation
4. Confirm success

### For DELETE/RESET operations:
1. Show what will be affected
2. Request explicit confirmation
3. For RESET: require typing "yes"
4. Execute only after confirmation

### For EXPORT:
1. Generate the backup file
2. Report the file path
3. Remind user to keep this safe

### For IMPORT:
1. FIRST remind user to export current data
2. Validate the import file exists
3. Preview what will be imported
4. Execute the import
5. Report results
