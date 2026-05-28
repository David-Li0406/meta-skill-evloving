---
name: connect-apps
description: Use this skill to connect Claude to external apps like Gmail, Slack, and GitHub, enabling actions such as sending emails, creating issues, and posting messages.
---

# Connect Apps

Connect Claude to 1000+ apps. Actually send emails, create issues, post messages - not just generate text about it.

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

### Step 1: Get API Key

Get your free key at [platform.composio.dev](https://platform.composio.dev/?utm_source=Github&utm_content=AwesomeSkills).

### Step 2: Set Environment Variable

```bash
export COMPOSIO_API_KEY="your-key"
```

### Step 3: Install

```bash
pip install composio          # Python
npm install @composio/core    # TypeScript
```

### Step 4: Install the Plugin

```
/plugin install composio-toolrouter
```

### Step 5: Run Setup

```
/composio-toolrouter:setup
```

This will configure Claude's connection to 1000+ apps and take about 60 seconds.

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

1. **You ask** Claude to do something.
2. **Tool Router finds** the right tool (1000+ options).
3. **OAuth handled** automatically.
4. **Action executes** and returns result.

## Auth Flow

First time using an app:
```
To send emails, I need Gmail access.
Authorize here: https://...
Say "connected" when done.
```

Connection persists after that.

## Troubleshooting

- **Auth required** → Click link, authorize, say "connected".
- **Action failed** → Check permissions in target app.
- **Tool not found** → Be specific: "Slack #general" not "send message".
- **"Plugin not found"** → Make sure you ran `/plugin install composio-toolrouter`.
- **"Need to authorize"** → Click the OAuth link Claude provides, then say "done".

---
<p align="center">
  <b>Join 20,000+ developers building agents that ship</b>
</p>

<p align="center">
  <a href="https://platform.composio.dev/?utm_source=Github&utm_content=AwesomeSkills">
    <img src="https://img.shields.io/badge/Get_Started_Free-4F46E5?style=for-the-badge" alt="Get Started"/>
  </a>
</p>