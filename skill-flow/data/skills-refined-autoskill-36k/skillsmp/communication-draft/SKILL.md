---
name: communication-draft
description: Draft personalized follow-up communications (email, call script, SMS) based on account context and history.
---

# Communication Draft

## When to use this skill

- After identifying account needs follow-up
- User requests a draft for specific account
- Preparing batch follow-up communications

## Channels

### Email
- Subject line + body
- Professional but warm tone
- Include specific context from history

### Call Script
- Talking points, not word-for-word script
- Key questions to ask
- Objection handling notes

### SMS
- Brief, conversational
- Clear call-to-action
- Under 160 characters ideal

## Context to include

1. **From state.md**:
   - Stage and insurance types
   - Next steps and pending actions
   - Contact name

2. **From history.md**:
   - Last interaction summary
   - Previous commitments made

3. **From sources/**:
   - Recent communication topics
   - Client preferences/concerns

## Draft output

```json
{
  "channel": "email",
  "subject": "Following up on your GL quote - Sunny Days Childcare",
  "body": "Hi [Name],\n\nI wanted to follow up on the General Liability quote we discussed last week...",
  "context_used": ["state.md", "call_150734/summary.md"],
  "rationale": "Quote was pitched 4 days ago, client mentioned needing time to review with partner"
}
```

## Templates

See `assets/templates.md` for starter templates by channel and stage.

## Personalization rules

1. Reference specific details from their communications
2. Acknowledge their situation/concerns
3. Provide clear next step
4. Match tone to previous interactions
