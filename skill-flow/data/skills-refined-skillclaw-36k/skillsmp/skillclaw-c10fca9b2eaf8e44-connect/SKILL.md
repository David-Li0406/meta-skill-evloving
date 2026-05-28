---
name: connect
description: Use this skill when you need Claude to take real actions across various applications, such as sending emails, creating issues, posting messages, and updating databases.
---

# Skill body

## When to Use This Skill

Use this skill when you need Claude to:

- **Send that email** instead of drafting it
- **Create that issue** instead of describing it
- **Post that message** instead of suggesting it
- **Update that database** instead of explaining how

## What Changes

| Without Connect | With Connect |
|-----------------|--------------|
| "Here's a draft email..." | Sends the email |
| "You should create an issue..." | Creates the issue |
| "Post this to Slack..." | Posts it |
| "Add this to Notion..." | Adds it |

## Supported Apps

**1000+ integrations** including:

- **Email:** Gmail, Outlook, SendGrid
- **Chat:** Slack, Discord, Teams, Telegram
- **Dev:** GitHub, GitLab, Jira, Linear
- **Docs:** Notion, Google Docs, Confluence
- **Data:** Sheets, Airtable, PostgreSQL
- **CRM:** HubSpot, Salesforce, Pipedrive
- **Storage:** Drive, Dropbox, S3
- **Social:** Twitter, LinkedIn, Reddit

## Setup

### 1. Get API Key

Get your free key at [platform.composio.dev](https://platform.composio.dev/?utm_source=Github&utm_content=AwesomeSkills)

### 2. Set Environment Variable

```bash
export COMPOSIO_API_KEY="your-key"
```

### 3. Install

```bash
pip install composio          # Python
npm install @composio/core    # TypeScript
```

Done. Claude can now connect to any app.

## Examples

### Send Email
```
Email sarah@acme.com - Subject: "Shipped!" Body: "v2.0 is live, let me know if issues"
```

### Create GitHub Issue
```
Create issue in my-org/repo: "Mobile timeout bug" with label:bug
```

### Post to Slack
```
Post to #engineering: "Deploy complete - v2.4.0 live"
```

### Chain Actions
```
Find GitHub issues labeled "bug" from this week, summarize, post to #bugs on Slack
```

## How It Works

Uses Composio Tool Router:

1. **You ask** Claude to do something
2. **Tool Router finds** the right tool (1000+ options)
3. **OAuth handled** automatically
4. **Action executes** and returns result

### Code

```python
from composio import Composio
import os

composio = Composio(api_key=os.environ["COMPOSIO_API_KEY"])
session = composio.create(user_id="user_123")
```