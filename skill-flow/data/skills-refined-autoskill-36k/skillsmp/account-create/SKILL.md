---
name: account-create
description: Create a new account when one doesn't exist. Use after lookup fails and user confirms they want to create a new account.
---

# Account Create

## When to use this skill

- Lookup returned no matching accounts
- User confirmed creation of new account
- Have minimum required information (company name)

## Required information

| Field | Required | Example |
|-------|----------|---------|
| Company Name | Yes | "ABC Contractors LLC" |
| Stage | No (defaults to "New Lead") | "Intake" |
| Primary Email | No | "owner@abc.com" |
| Primary Phone | No | "(555) 123-4567" |
| Insurance Types | No | ["General Liability"] |

## Creation process

1. Generate unique account ID
2. Create directory structure:
   ```
   mem/accounts/{account_id}/
   ├── state.md
   ├── history.md
   └── sources/
       ├── emails/
       ├── calls/
       └── sms/
   ```
3. Write initial `state.md` with provided fields
4. Write initial `history.md` with creation entry
5. Index in Qdrant (name + description)

## State.md template

```markdown
# {Company Name} (Account {ID})

## Status
- **Stage**: {Stage or "New Lead"}
- **Insurance Types**: {Types or "None"}

## Contacts
- **Primary Email**: {Email or "Not provided"}
- **Primary Phone**: {Phone or "Not provided"}

## Next Steps
- Initial outreach needed

## Pending Actions
- Gather business details

## Last Contact
- **Date**: {Creation date}
- **Type**: account created
```

## After creation

- Return the new account ID and path
- Continue with any pending update request
