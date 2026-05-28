---
name: connect
description: Use this skill to connect Claude to any app, enabling actions like sending emails, creating issues, posting messages, and updating databases across 1000+ services.
---

# Connect

Connect Claude to any app. Stop generating text about what you could do - actually do it.

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
Email <recipient> - Subject: "<subject>" Body: "<body>"
```

### Create GitHub Issue
```
Create issue in <org>/<repo>: "<issue_title>" with <labels>
```

### Post to Slack
```
Post to <channel>: "<message>"
```

### Chain Actions
```
Find GitHub issues labeled "<label>" from this week, summarize, post to <channel> on Slack
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
from claude_agent_sdk.client import ClaudeSDKClient
from claude_agent_sdk.types import ClaudeAgentOptions
import os

composio = Composio(api_key=os.environ["COMPOSIO_API_KEY"])
session = composio.create(user_id="user_123")

options = ClaudeAgentOptions(
    system_prompt="You can take actions in external apps.",
    mcp_servers={
        "composio": {
            "type": "http",
            "url": session.mcp.url,
            "headers": {"x-api-key": os.environ["COMPOSIO_API_KEY"]},
        }
    },
)

async with ClaudeSDKClient(options) as client:
    await client.query("Send Slack message to <channel>: <message>")
```

## Auth Flow

First time using an app:
```
To send emails, I need Gmail access.
Authorize here: https://...
Say "connected" when done.
```

Connection persists after that.

## Framework Support

| Framework | Install |
|-----------|---------|
| Claude Agent SDK | `pip install composio claude-agent-sdk` |
| OpenAI Agents | `pip install composio openai-agents` |
| Vercel AI | `npm install @composio/core @composio/vercel` |
| LangChain | `pip install composio-langchain` |
| Any MCP Client | Use `session.mcp.url` |

## Troubleshooting

- **Auth required** → Click link, authorize, say "connected"
- **Action failed** → Check permissions in target app
- **Tool not found** → Be specific: "Slack #general" not "send message"

---

<p align="center">
  <b>Join 20,000+ developers building agents that ship</b>
</p>

<p align="center">
  <a href="https://platform.composio.dev/?utm_source=Github&utm_content=AwesomeSkills">
    <img src="https://img.shields.io/badge/Get_Started_Free-4F46E5?style=for-the-badge" alt="Get Started"/>
  </a>
</p>