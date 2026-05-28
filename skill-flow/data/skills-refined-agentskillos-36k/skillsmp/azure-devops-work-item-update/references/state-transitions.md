# Azure DevOps State Transitions

Valid state transitions for different work item types.

---

## Task

**Available States**:
- New
- Active
- Ready for Testing
- Closed
- Removed

**Valid Transitions**:
```
New → Active
New → Removed

Active → Ready for Testing
Active → Closed
Active → Removed

Ready for Testing → Closed
Ready for Testing → Active (if failed testing)
Ready for Testing → Removed

Closed → Active (if reopened)
Closed → Removed
```

**Recommended After Implementation**:
- **Active → Ready for Testing** (implementation complete, ready for QA)
- Use "Closed" only after testing verified

---

## User Story

**Available States**:
- New
- Active
- Resolved
- Closed
- Removed

**Valid Transitions**:
```
New → Active
New → Removed

Active → Resolved (implementation complete)
Active → Removed

Resolved → Closed (after acceptance)
Resolved → Active (if rejected)
Resolved → Removed

Closed → Active (if reopened)
Closed → Removed
```

**Recommended After Implementation**:
- **Active → Resolved** (all tasks complete, ready for stakeholder review)
- Use "Closed" only after stakeholder acceptance

---

## Bug

**Available States**:
- New
- Active
- Resolved
- Closed

**Valid Transitions**:
```
New → Active
Active → Resolved (fix implemented)
Resolved → Closed (fix verified)
Resolved → Active (if fix didn't work)
Closed → Active (if bug reappears)
```

**Recommended After Implementation**:
- **Active → Resolved** (bug fix complete, ready for verification)
- Use "Closed" only after verification complete

---

## Feature

**Available States**:
- New
- Active
- Resolved
- Closed
- Removed

**Valid Transitions**:
```
New → Active
New → Removed

Active → Resolved
Active → Removed

Resolved → Closed
Resolved → Active
Resolved → Removed

Closed → Active
Closed → Removed
```

**Note**: Features are typically updated when all child User Stories complete.

---

## Epic

**Available States**:
- New
- Active
- Resolved
- Closed
- Removed

**Valid Transitions**:
```
New → Active
New → Removed

Active → Resolved
Active → Removed

Resolved → Closed
Resolved → Active
Resolved → Removed

Closed → Active
Closed → Removed
```

**Note**: Epics are typically updated when all child Features complete.

---

## Custom States

Some Azure DevOps projects may have custom states. Common additions:

- **In Review** (code review in progress)
- **Blocked** (work stopped due to dependency)
- **Ready for Deployment** (approved for production)
- **In Testing** (QA in progress)

Check your project's work item process template for available states.

---

## State Transition Best Practices

### 1. Use Appropriate Target States

**For Tasks**:
- ✅ Use "Ready for Testing" when implementation complete
- ❌ Don't use "Closed" immediately after implementation

**For User Stories/Bugs**:
- ✅ Use "Resolved" when implementation complete
- ❌ Don't use "Closed" until acceptance/verification complete

### 2. Document State Transitions

When changing state, always add a comment explaining why:
- What was completed
- What changed
- What's next

### 3. Check Current State First

Before updating:
```
mcp__azure-devops__wit_get_work_item(
  project: "ProjectName",
  id: 1234
)
```

Verify current state allows transition to target state.

### 4. Handle Invalid Transitions

If transition not allowed:
- Check valid transitions table
- Use intermediate state if needed
- Example: New → Active → Ready for Testing (can't go directly New → Ready for Testing)

---

## Error Messages

**"The state transition is not valid"**
- Check valid transitions table above
- May need to go through intermediate state
- Verify work item type

**"The state value is not valid"**
- State name may be misspelled (case-sensitive)
- State may not exist for this work item type
- Check custom states in your project

---

## Implementation Notes

### Validation Before Update

```python
valid_transitions = {
    "Task": {
        "New": ["Active", "Removed"],
        "Active": ["Ready for Testing", "Closed", "Removed"],
        "Ready for Testing": ["Closed", "Active", "Removed"]
    },
    "User Story": {
        "New": ["Active", "Removed"],
        "Active": ["Resolved", "Removed"],
        "Resolved": ["Closed", "Active", "Removed"]
    }
}

def is_valid_transition(work_item_type, current_state, target_state):
    return target_state in valid_transitions.get(work_item_type, {}).get(current_state, [])
```

### Update Payload

```json
{
  "op": "add",
  "path": "/fields/System.State",
  "value": "Ready for Testing"
}
```

---

**Last Updated**: 2025-01-21
