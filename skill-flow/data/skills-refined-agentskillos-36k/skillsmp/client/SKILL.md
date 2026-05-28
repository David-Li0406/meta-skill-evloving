---
name: client
description: Manage client relationships. USE WHEN user asks about clients, follow-ups, client emails, or who needs attention.
---

# Client Skill

Manage clients using `Clients/` folder.

## Quick Commands

| Say | Does |
|-----|------|
| "Who needs follow-up?" | Shows clients needing attention |
| "Tell me about [name]" | Client context and history |
| "Draft email to [name]" | Personalized follow-up email |
| "Add client [name]" | Creates new client file |

## Workflow Routing

- Check follow-ups → `workflows/check-followups.md`
- Draft client email → `workflows/draft-email.md`
- Add new client → `workflows/add-client.md`

## Data

Client files live in `Clients/*.md` with frontmatter:

```yaml
---
type: client
name: Sarah Chen
email: sarah@example.com
company: TechStartup Inc
stage: active       # lead, active, customer
next_action: 2026-01-10
next_action_note: Follow up on proposal
last_contact: 2026-01-05
---
```

## Quick Queries

**List all clients:**
```bash
ls Clients/*.md
```

**Find who needs follow-up:**
```bash
grep -l "next_action:" Clients/*.md | while read f; do
  echo "=== $(basename "$f" .md) ==="
  grep -E "^(next_action|next_action_note):" "$f"
done
```

**Find by stage:**
```bash
grep -l "stage: lead" Clients/*.md
```
