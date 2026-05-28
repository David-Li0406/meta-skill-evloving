# Email Reply Templates

## Meeting Request

```
Hi [Name],

Thanks for reaching out. [Accept: I'd be happy to meet / Decline: Unfortunately I'm not available].

[If accepting: How about [suggested time]? / If declining: Could we [alternative]?]

Best,
[User]
```

## Information Request

```
Hi [Name],

Thanks for your question about [topic].

[Direct answer or: I'll look into this and get back to you by [timeframe].]

Let me know if you need anything else.

Best,
[User]
```

## Acknowledgment

```
Hi [Name],

Got it, thanks for letting me know. [Brief acknowledgment of content].

[If action needed: I'll [action] by [timeframe].]

Best,
[User]
```

## Out of Office

```
Hi,

Thank you for your email. I'm currently out of the office [until date/with limited access].

[For urgent matters, please contact [alternative]. / I'll respond when I return.]

Best,
[User]
```

---

# Triage Rules

| Pattern | Category | Action |
|---------|----------|--------|
| `from:*@github.com` | Dev Notifications | Summarize, no reply needed |
| `from:*@linkedin.com` | Social | Low priority |
| `subject:invoice OR receipt` | Finance | Flag for review |
| `from:[known contacts]` | Personal | High priority |
| `has:attachment` | Documents | Extract attachment names |

---

# Priority Categories

- **P1 (Urgent)**: Keywords: urgent, asap, deadline, critical
- **P2 (Important)**: From known contacts, requires action
- **P3 (Informational)**: Newsletters, notifications, FYI
- **P4 (Low)**: Marketing, spam-adjacent

---

# Gmail Search Query Syntax

- `is:unread` - Unread emails
- `from:user@example.com` - From specific sender
- `subject:urgent` - Subject contains word
- `newer_than:1d` - Within last day
- `has:attachment` - Has attachments
- `in:inbox` - In inbox
- `label:important` - Has label
