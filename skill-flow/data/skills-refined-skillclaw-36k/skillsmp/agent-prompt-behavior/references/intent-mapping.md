# Intent Mapping

Patterns for mapping natural language intents to tool calls.

---

## What is Intent Mapping?

Intent mapping translates what users **say** into what the agent **does**.

```
User: "I need to add a new task called buy groceries"
         │
         ▼
    ┌─────────────────────────────────────┐
    │        INTENT RECOGNITION           │
    │  "add" + "task" → create_task       │
    └─────────────────────────────────────┘
         │
         ▼
    ┌─────────────────────────────────────┐
    │        PARAMETER EXTRACTION         │
    │  title = "buy groceries"            │
    └─────────────────────────────────────┘
         │
         ▼
    Tool Call: create_task(title="buy groceries")
```

---

## Mapping Table Structure

### Basic Format

```markdown
## Intent Mapping

| Intent Pattern | Tool | Required Params | Optional Params | Confirm |
|----------------|------|-----------------|-----------------|---------|
| create/add/new + task | create_task | title | description, due | No |
| delete/remove + task | delete_task | task_id | - | Yes |
| show/list + tasks | list_tasks | - | filter | No |
```

### Extended Format with Variations

```markdown
## Intent Mapping

### Create Task
**Trigger phrases:**
- "create a task"
- "add a new task"
- "new task"
- "I need to add"
- "make a task"
- "remind me to" (maps to task creation)

**Tool:** `create_task`
**Parameters:**
- `title` (required): Extract from user's description
- `description` (optional): Additional details if provided
- `due_date` (optional): Parse natural language dates

**Confirmation:** No

**Examples:**
- "Add a task to buy milk" → create_task(title="buy milk")
- "Create task: finish report by Friday" → create_task(title="finish report", due_date="Friday")
```

---

## Intent Categories

### CRUD Operations

```markdown
## CRUD Intent Mapping

### CREATE
| User Says | Tool | Notes |
|-----------|------|-------|
| add, create, new, make | create_X | Extract entity from context |
| remind me to, I need to | create_task | Specific to tasks |
| start, begin | create_X | For workflows/processes |

### READ
| User Says | Tool | Notes |
|-----------|------|-------|
| show, list, what are | list_X | Default to user-scoped |
| get, view, open | get_X | Single item retrieval |
| find, search, look for | search_X | Requires query parameter |
| how many, count | count_X | Aggregate operation |

### UPDATE
| User Says | Tool | Notes |
|-----------|------|-------|
| change, update, modify | update_X | Requires ID + new values |
| rename, set | update_X | Specific field updates |
| mark as, make it | update_X | Status changes |
| done, complete, finish | complete_X | Special status update |

### DELETE
| User Says | Tool | Notes |
|-----------|------|-------|
| delete, remove, get rid of | delete_X | Always confirm |
| cancel, clear | delete_X | Context-dependent |
| undo | Maybe delete | Depends on what's being undone |
```

### Query Operations

```markdown
## Query Intent Mapping

| User Says | Tool | Parameters |
|-----------|------|------------|
| "show tasks for today" | list_tasks | due_date=today |
| "what's overdue" | list_tasks | filter=overdue |
| "completed tasks" | list_tasks | filter=completed |
| "find tasks about X" | search_tasks | query=X |
| "tasks due this week" | list_tasks | due_date=this_week |
| "how many tasks" | count_tasks | - |
| "high priority tasks" | list_tasks | priority=high |
```

### Action Operations

```markdown
## Action Intent Mapping

| User Says | Tool | Parameters | Confirm |
|-----------|------|------------|---------|
| "mark X as done" | complete_task | task_id | No |
| "complete all" | bulk_complete | filter | Yes |
| "move X to category Y" | update_task | task_id, category | No |
| "snooze X until tomorrow" | update_task | task_id, due_date | No |
| "archive completed" | archive_tasks | filter=completed | Yes |
```

---

## Parameter Extraction Patterns

### Named Entity Extraction

```markdown
## Parameter Extraction

### Task Title
Extract the main subject after intent keywords:
- "create task **buy groceries**" → title="buy groceries"
- "add **call mom** to my tasks" → title="call mom"
- "remind me to **finish the report**" → title="finish the report"

### Task ID
Extract from context or ask:
- "delete task **#42**" → task_id=42
- "remove **the first one**" → Clarify which task
- "delete it" → Use previous context or ask

### Dates
Parse natural language:
- "by **tomorrow**" → due_date=tomorrow
- "on **Friday**" → due_date=next_Friday
- "in **2 days**" → due_date=+2d
- "**next week**" → due_date=+7d
```

### Implicit Parameters

```markdown
## Implicit Parameters

Sometimes parameters are implied, not stated:

| Context | Implied Parameter |
|---------|-------------------|
| Previous task mentioned | task_id = last_mentioned_task |
| User context | user_id = current_user |
| Default time scope | filter = active |
| Single match in search | auto-select that item |
```

---

## Ambiguity Resolution

### When Multiple Tools Match

```markdown
## Disambiguation Rules

### Priority Order
When multiple intents could match, prefer:
1. Most specific match
2. Most recently used tool type
3. Most common intent for this user

### Example
User: "complete it"

Could mean:
- complete_task (mark as done)
- update_task (add more details)

Resolution:
1. Check context: Was a task just mentioned?
2. If yes: complete_task for that task
3. If no: Ask "Do you want to mark a task as complete? Which one?"
```

### Clarification Patterns

```markdown
## Clarification Strategies

### Ask When Ambiguous
"I found 3 tasks with 'report' in the name:
1. Quarterly report
2. Bug report
3. Expense report

Which one would you like to [action]?"

### Offer Most Likely
"Did you mean the task 'Buy groceries' (due today)?
Say yes, or tell me which task you meant."

### Show Options with Numbers
"Which task?
1. Task A
2. Task B
3. Task C

(Reply with the number)"
```

---

## Multi-Intent Handling

### Sequential Intents

```markdown
## Handling Multiple Intents

### Sequential (One at a Time)
User: "Create a task called X and then mark Y as done"

Process:
1. create_task(title="X")
2. complete_task(task_id=Y)
3. Report both results

Response:
"✓ Created 'X'
✓ Marked 'Y' as done"
```

### Compound Intents

```markdown
## Compound Intent Patterns

| User Says | Decompose Into |
|-----------|----------------|
| "add and complete task X" | create_task → complete_task |
| "delete all completed tasks" | list_tasks(filter=completed) → bulk_delete |
| "move X to Y and mark done" | update_task(category) → complete_task |
```

---

## Context-Aware Mapping

### Using Conversation Context

```markdown
## Context Rules

### Recent Entity Reference
If user says "it", "that", "the task":
- Look for most recently mentioned entity
- Must be same entity type (task → task, not task → category)

### Session State
Track during conversation:
- Last viewed task
- Last created task
- Current filter/view
- Recent search results

### Example
User: "Show my tasks"
Agent: [Lists tasks 1, 2, 3]
User: "Delete the first one"
Agent: Knows "first one" = task 1 from previous response
```

---

## Fallback Patterns

### Unknown Intent

```markdown
## When Intent Doesn't Match

If no tool matches the user's request:

1. **Acknowledge**: "I'm not sure what you want me to do."

2. **Clarify capabilities**:
   "I can help you with tasks:
   - Create, update, or delete tasks
   - List and search your tasks
   - Mark tasks as complete

   What would you like to do?"

3. **Offer closest match** (if partial match):
   "Did you want me to [closest matching action]?"
```

### Unsupported Action

```markdown
## Unsupported Intent Handling

When user asks for something you cannot do:

1. **Be honest**: "I can't do that."

2. **Explain why** (briefly):
   "I don't have access to your calendar."

3. **Offer alternative**:
   "But I can create a task with a due date as a reminder."

Example:
User: "Send an email reminder"
Agent: "I can't send emails, but I can create a task with a due date
so you'll see it in your task list. Would you like me to do that?"
```

---

## Testing Intent Mapping

### Test Cases to Cover

```markdown
## Intent Mapping Test Cases

### Positive Tests
- [ ] Standard phrasing works: "create a task"
- [ ] Variations work: "add", "make", "new"
- [ ] With parameters: "create task called X"
- [ ] Natural phrasing: "I need to remember to X"

### Negative Tests
- [ ] Out-of-scope gracefully rejected
- [ ] Similar but wrong intent clarified
- [ ] Missing parameters requested

### Edge Cases
- [ ] Empty/minimal input handled
- [ ] Multiple intents processed correctly
- [ ] Context correctly carried forward
```

### Validation Checklist

```markdown
## Mapping Validation

Before finalizing intent mapping:

- [ ] All CRUD operations covered
- [ ] Common phrasings included (3+ per intent)
- [ ] Parameter extraction rules defined
- [ ] Ambiguity resolution specified
- [ ] Unknown intent fallback defined
- [ ] Context rules documented
- [ ] Edge cases handled
```
