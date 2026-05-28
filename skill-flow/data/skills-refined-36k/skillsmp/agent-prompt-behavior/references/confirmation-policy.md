# Confirmation Policy

When and how agents should confirm actions before executing.

---

## Why Confirmation Matters

```
┌─────────────────────────────────────────────────────────────┐
│                    WITHOUT CONFIRMATION                     │
│                                                             │
│  User: "delete my tasks"                                    │
│  Agent: [Deletes ALL tasks]                                 │
│  User: "Wait, I meant just the completed ones!"            │
│  Agent: "Too late. Data is gone."                          │
│                                                             │
│  ❌ Trust destroyed. User upset. Data lost.                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    WITH CONFIRMATION                        │
│                                                             │
│  User: "delete my tasks"                                    │
│  Agent: "I'll delete ALL 47 tasks. Confirm? (yes/no)"      │
│  User: "No, just completed ones"                            │
│  Agent: "Got it. Delete 12 completed tasks? (yes/no)"      │
│  User: "Yes"                                                │
│  Agent: "✓ Deleted 12 completed tasks."                    │
│                                                             │
│  ✅ User in control. Data protected. Trust maintained.     │
└─────────────────────────────────────────────────────────────┘
```

---

## Confirmation Categories

### 1. Always Confirm (High Risk)

| Action Type | Examples | Why |
|-------------|----------|-----|
| **Destructive** | Delete, remove, clear, purge | Data loss is irreversible |
| **Financial** | Purchase, transfer, refund | Real money at stake |
| **External** | Send email, post message, notify | Visible to others |
| **Bulk** | Delete all, update all, mass change | Large blast radius |
| **Permanent** | Close account, revoke access | Cannot be undone |

```markdown
## Always Confirm Actions

Before executing these actions, ALWAYS confirm:
- delete_task
- delete_all_tasks
- clear_completed
- send_notification
- export_data
- bulk_update

No exceptions. Even if user seems certain.
```

### 2. Sometimes Confirm (Medium Risk)

| Action Type | Confirm When | Skip When |
|-------------|--------------|-----------|
| **Updates** | Major changes, multiple fields | Single field, minor edit |
| **Status changes** | Irreversible status | Togglable status |
| **Moves** | To archive, to trash | Between categories |

```markdown
## Conditional Confirmation

Confirm update_task when:
- Changing due date to past
- Changing priority to lowest
- Updating more than 3 fields

Skip confirmation when:
- Marking complete/incomplete (easily reversed)
- Changing category (easily reversed)
- Adding description to empty task
```

### 3. Never Confirm (Low Risk)

| Action Type | Examples | Why Safe |
|-------------|----------|----------|
| **Read-only** | List, view, search, count | No state change |
| **Reversible** | Toggle complete, change category | Easy to undo |
| **Additive** | Create task, add note | Adds, doesn't destroy |

```markdown
## No Confirmation Needed

These actions proceed immediately:
- list_tasks
- search_tasks
- get_task
- create_task
- complete_task (toggle)
- add_note
```

---

## Confirmation Message Format

### Structure

```
[What will happen] + [Specific details] + [Confirm prompt]
```

### Good Examples

```markdown
## Confirmation Formats

### Single Item
"I'll delete the task 'Buy groceries' (due tomorrow).
Confirm? (yes/no)"

### Bulk Action
"I'll delete ALL 47 tasks in your list.
This includes 12 incomplete tasks.
Confirm? (yes/no)"

### External Action
"I'll send a reminder email about 'Project deadline' to team@company.com.
Confirm? (yes/no)"

### Financial
"I'll process a refund of $49.99 to your original payment method.
This may take 3-5 business days.
Confirm? (yes/no)"
```

### Bad Examples (Avoid)

```markdown
## Anti-Patterns

❌ Too vague:
"Delete? (yes/no)"

❌ No details:
"Confirm action? (yes/no)"

❌ Scary without context:
"WARNING: This action cannot be undone! Proceed? (yes/no)"

❌ Too many options:
"Delete task? (yes/no/cancel/maybe later/show me first)"
```

---

## Confirmation Flow

### Standard Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    CONFIRMATION FLOW                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. USER REQUEST                                            │
│     "delete all completed tasks"                            │
│                    │                                        │
│                    ▼                                        │
│  2. AGENT PREPARES (no execution yet)                       │
│     - Count affected items: 12 tasks                        │
│     - Prepare summary                                       │
│                    │                                        │
│                    ▼                                        │
│  3. CONFIRMATION PROMPT                                     │
│     "I'll delete 12 completed tasks. Confirm? (yes/no)"    │
│                    │                                        │
│          ┌────────┴────────┐                               │
│          ▼                 ▼                                │
│  4a. USER: "yes"      4b. USER: "no"                       │
│      │                     │                                │
│      ▼                     ▼                                │
│  5a. EXECUTE          5b. CANCEL                           │
│      delete_tasks()        "Okay, cancelled."              │
│      "✓ Deleted 12"                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Handling Confirmation Response

```markdown
## Confirmation Response Handling

### Affirmative (proceed)
- "yes", "y", "yeah", "yep", "sure", "ok", "do it", "confirm"
- → Execute the action
- → Report success

### Negative (cancel)
- "no", "n", "nope", "cancel", "stop", "wait", "nevermind"
- → Do NOT execute
- → Acknowledge cancellation: "Okay, cancelled. Nothing was deleted."

### Ambiguous
- "maybe", "I guess", "not sure"
- → Ask again more directly
- → "I need a clear yes or no. Delete the 12 tasks?"

### Modified
- "yes but only the old ones"
- → Acknowledge modification
- → Re-confirm with new scope: "Delete only tasks older than 30 days (8 tasks)?"
```

---

## Contextual Confirmation

### Repeat Action Optimization

```markdown
## Reducing Confirmation Fatigue

If user is doing repeated similar actions, offer batch mode:

First time:
Agent: "Delete 'Task 1'? (yes/no)"
User: "yes"

Second time:
Agent: "Delete 'Task 2'? (yes/no, or 'all' to delete remaining)"
User: "all"

Agent: "Delete remaining 5 tasks? (yes/no)"
User: "yes"
Agent: "✓ Deleted 5 tasks."
```

### Smart Confirmation Skipping

```markdown
## When to Skip Confirmation

Even for normally-confirmed actions, skip if:

1. **Explicit bulk intent**: "delete ALL my tasks, I'm sure"
   - User explicitly confirmed in their request

2. **Undo operation**: "undo that delete"
   - Undoing is itself a safety mechanism

3. **Empty set**: "delete completed tasks" (0 completed)
   - Nothing to delete, just inform: "No completed tasks to delete."
```

---

## Confirmation in Batch Operations

### Batch Confirmation Strategies

```markdown
## Batch Operation Confirmation

### Strategy 1: Confirm Once (Recommended for homogeneous batches)
User: "Delete all completed tasks"
Agent: "Delete 12 completed tasks? (yes/no)"
- One confirmation for entire batch

### Strategy 2: Sample Confirmation (For heterogeneous batches)
User: "Update all tasks to high priority"
Agent: "I'll set 47 tasks to high priority. Here are a few:
- 'Buy groceries' (currently low)
- 'Finish report' (currently medium)
- 'Call mom' (currently high - no change)
Confirm all? (yes/no)"

### Strategy 3: Threshold Confirmation
- < 5 items: List all, confirm once
- 5-20 items: Count + sample, confirm once
- > 20 items: Count + warning, confirm once
```

---

## Confirmation UI Patterns

### Text-Based (Chat)

```markdown
## Chat Confirmation

Simple yes/no:
"Delete 'Task name'? (yes/no)"

With details:
"I'll delete 'Project report' which is due tomorrow and has 3 subtasks.
Reply yes to confirm, or no to cancel."

Numbered options:
"What would you like to do with 'Old task'?
1. Delete it
2. Archive it
3. Keep it
(Reply with number)"
```

### Structured Response (API)

```json
{
  "confirmation_required": true,
  "action": "delete_task",
  "details": {
    "task_id": "123",
    "task_title": "Buy groceries",
    "affected_subtasks": 3
  },
  "message": "Delete 'Buy groceries' and its 3 subtasks?",
  "options": ["confirm", "cancel"]
}
```

---

## Implementation Pattern

### Code Pattern

```python
# Confirmation policy implementation

class ConfirmationPolicy:
    """Determine when confirmation is required."""

    ALWAYS_CONFIRM = {
        "delete_task",
        "delete_all_tasks",
        "bulk_delete",
        "send_notification",
        "export_data",
    }

    CONDITIONAL_CONFIRM = {
        "update_task": lambda params: len(params) > 3,
        "move_task": lambda params: params.get("to") == "archive",
    }

    NEVER_CONFIRM = {
        "list_tasks",
        "get_task",
        "search_tasks",
        "create_task",
        "complete_task",
    }

    @classmethod
    def requires_confirmation(cls, tool: str, params: dict) -> bool:
        if tool in cls.ALWAYS_CONFIRM:
            return True
        if tool in cls.NEVER_CONFIRM:
            return False
        if tool in cls.CONDITIONAL_CONFIRM:
            return cls.CONDITIONAL_CONFIRM[tool](params)
        return True  # Default to confirm if unknown


def build_confirmation_message(tool: str, params: dict, context: dict) -> str:
    """Build human-readable confirmation message."""
    templates = {
        "delete_task": "Delete '{title}'? (yes/no)",
        "delete_all_tasks": "Delete ALL {count} tasks? (yes/no)",
        "bulk_delete": "Delete {count} tasks matching '{filter}'? (yes/no)",
    }
    template = templates.get(tool, "Confirm {tool}? (yes/no)")
    return template.format(tool=tool, **params, **context)
```

---

## Confirmation Checklist

```markdown
## Before Deploying Confirmation Policy

- [ ] All destructive actions require confirmation
- [ ] Financial actions require confirmation with amounts
- [ ] External/visible actions require confirmation with recipients
- [ ] Bulk actions show count before confirming
- [ ] Confirmation messages include specific details
- [ ] Yes/no responses are clearly handled
- [ ] Ambiguous responses trigger re-confirmation
- [ ] Cancel is always an option
- [ ] Confirmation timeout/expiry defined (if applicable)
- [ ] Audit log captures confirmation responses
```
