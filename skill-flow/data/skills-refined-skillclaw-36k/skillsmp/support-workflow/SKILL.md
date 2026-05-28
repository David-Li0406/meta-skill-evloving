---
name: support-workflow
description: |
  Support ticket workflow for FreeScout helpdesk. Use this skill when:
  - Processing support tickets (triage, analyze, respond)
  - Searching for tickets by status, assignee, or keywords
  - Managing ticket status and assignments
  - Drafting personalized customer responses
  - Adding internal notes for team collaboration
allowed-tools:
  - mcp__freescout__freescout_get_ticket
  - mcp__freescout__freescout_analyze_ticket
  - mcp__freescout__freescout_add_note
  - mcp__freescout__freescout_update_ticket
  - mcp__freescout__freescout_create_draft_reply
  - mcp__freescout__freescout_get_ticket_context
  - mcp__freescout__freescout_search_tickets
  - mcp__freescout__freescout_get_mailboxes
---

# Support Workflow Skill

Manage FreeScout support tickets efficiently using the **Triage-Analyze-Respond** pattern.

## Phase 1: TRIAGE (Discover & Prioritize)

### Search for Tickets

Find tickets needing attention:

```javascript
// Unassigned active tickets
mcp__freescout__freescout_search_tickets({
  status: "active",
  assignee: "unassigned",
  pageSize: 20
})

// Recent tickets in last 24 hours
mcp__freescout__freescout_search_tickets({
  status: "all",
  createdSince: "24h",
  includeLastMessage: true
})

// Search by keyword
mcp__freescout__freescout_search_tickets({
  textSearch: "login error",
  status: "active"
})
```

### List Mailboxes

Get available mailboxes for filtering:

```javascript
mcp__freescout__freescout_get_mailboxes({})
```

## Phase 2: ANALYZE (Understand the Issue)

### Get Full Ticket Details

```javascript
mcp__freescout__freescout_get_ticket({
  ticket: "<ticket-id-or-url>",
  includeThreads: true
})
```

### Analyze Issue Type & Solution

```javascript
mcp__freescout__freescout_analyze_ticket({
  ticket: "<ticket-id-or-url>"
})
```

The analysis returns:
- **Issue Type**: Bug, feature request, how-to, billing, etc.
- **Root Cause**: What's causing the problem
- **Suggested Solution**: Recommended resolution steps
- **Priority**: Based on impact and urgency

### Get Customer Context

```javascript
mcp__freescout__freescout_get_ticket_context({
  ticket: "<ticket-id-or-url>"
})
```

Returns customer history, previous tickets, and relevant context for personalization.

## Phase 3: RESPOND (Take Action)

### Create Draft Reply

Draft a response that can be reviewed before sending:

```javascript
mcp__freescout__freescout_create_draft_reply({
  ticket: "<ticket-id-or-url>",
  replyText: "Hi [Customer Name],\n\nThank you for reaching out..."
})
```

### Add Internal Note

Add notes for team collaboration (not visible to customer):

```javascript
mcp__freescout__freescout_add_note({
  ticket: "<ticket-id-or-url>",
  note: "Escalated to dev team - suspected bug in v2.3.1"
})
```

### Update Ticket Status

```javascript
mcp__freescout__freescout_update_ticket({
  ticket: "<ticket-id-or-url>",
  status: "pending",  // active, pending, closed, spam
  assignTo: 123       // User ID (optional)
})
```

## Response Templates

### Bug Report Response

```
Hi [Name],

Thank you for reporting this issue. I've reproduced the problem and can confirm [description].

Our development team is investigating, and I'll update you once we have a fix ready.

In the meantime, here's a workaround: [steps]

Best,
[Agent]
```

### Feature Request Response

```
Hi [Name],

Thanks for the suggestion! This is a great idea.

I've added your request to our feature backlog. While I can't promise a timeline, we do prioritize based on customer feedback like yours.

Is there anything else I can help with?

Best,
[Agent]
```

### How-To Response

```
Hi [Name],

Great question! Here's how to [task]:

1. [Step one]
2. [Step two]
3. [Step three]

I've also attached a quick guide that covers this in more detail.

Let me know if you have any other questions!

Best,
[Agent]
```

## Best Practices

### Do
- Always read the full conversation before responding
- Use customer's name and personalize responses
- Acknowledge the customer's frustration when appropriate
- Provide clear, step-by-step instructions
- Set realistic expectations for resolution times
- Add internal notes for complex issues

### Don't
- Send generic copy-paste responses
- Make promises you can't keep
- Ignore previous conversation context
- Use overly technical jargon
- Leave tickets unassigned indefinitely
