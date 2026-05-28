# Add New Client

## Steps

1. **Gather information**
   
   Ask for (if not provided):
   - Name
   - Email
   - Company (optional)

2. **Create client file**
   
   Create `Clients/[Name].md` with this structure:

```markdown
---
type: client
name: [Name]
email: [email]
company: [company]
stage: lead
next_action: [tomorrow's date]
next_action_note: Send intro email
last_contact: [today's date]
---

# [Name]

**Email:** [email]
**Company:** [company]

## Notes

- [How they found you / initial context]
```

3. **Confirm creation**
   
   "Added [Name] to your clients. Next action: Send intro email by [date]."

4. **Offer next step**
   
   "Want me to draft an intro email?"

## Example

**Input:** "Add client John Smith, john@acme.com, Acme Corp"

**Creates:** `Clients/John Smith.md`

**Response:** "Added John Smith to your clients. Want me to draft an intro email?"
