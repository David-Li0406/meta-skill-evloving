---
name: state-edit
description: Modify fields in an account's state.md file. Use to update stage, contacts, next steps, or other status fields.
---

# State Edit

## When to use this skill

- User requests an update to account status
- Stage change (e.g., "move to Quoted")
- Contact information change
- Next steps or pending actions change

## Editable fields

| Field | Section | Format |
|-------|---------|--------|
| Stage | Status | Single value |
| Insurance Types | Status | Comma-separated list |
| Primary Email | Contacts | Email address |
| Primary Phone | Contacts | Phone number |
| Next Steps | Next Steps | Bullet list |
| Pending Actions | Pending Actions | Bullet list |

## Update process

1. Read current `state.md`
2. Parse the field to update
3. Apply the change
4. Write updated `state.md`
5. Record change in `history.md` (see history-chain skill)
6. Update Qdrant description (see qdrant-sync skill)

## Example: Stage update

Before:
```markdown
## Status
- **Stage**: Application Received
```

After:
```markdown
## Status
- **Stage**: Quote Pitched
```

## Handling vague updates

If the update is ambiguous (e.g., "update the account"):

1. Return `needs_clarification: true`
2. List the fields that could be updated
3. Ask user to specify which field and new value

## Important

- Always preserve fields that aren't being updated
- Maintain markdown formatting
- Update Last Contact if this is a contact-related change
