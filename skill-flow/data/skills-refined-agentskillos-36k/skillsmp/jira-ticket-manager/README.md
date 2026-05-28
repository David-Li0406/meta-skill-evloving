# Jira Ticket Manager Skill

Manage Jira tickets from Claude Code using curl + jq.

## Setup

**1. Create API token** at https://id.atlassian.com/manage-profile/security/api-tokens

**2. Add to shell profile:**
```bash
printf '\nexport JIRA_URL="https://your-company.atlassian.net"\nexport JIRA_USER="your-email@company.com"\nexport JIRA_TOKEN="your-api-token"\n' >> ~/.zshrc && source ~/.zshrc
```

**3. Verify:**
```bash
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null; echo "JIRA_URL: ${JIRA_URL:-(not set)}"; echo "JIRA_USER: ${JIRA_USER:-(not set)}"; echo "JIRA_TOKEN: ${JIRA_TOKEN:+set}"
```

## Usage

```
/jira-ticket-manager get PROJ-123
/jira-ticket-manager search project = PROJ AND status = Open
/jira-ticket-manager my tickets
/jira-ticket-manager create bug in PROJ: summary here
/jira-ticket-manager comment PROJ-123: your comment
/jira-ticket-manager transition PROJ-123 to Done
```

Or paste a Jira URL directly: `/jira-ticket-manager get https://company.atlassian.net/browse/PROJ-123`

## Data Storage

Responses are saved to `tickets/` for reliable parsing (Jira APIs return 30KB+ JSON). This directory is gitignored.

```
tickets/
├── .gitignore
├── PROJ-123.json
├── search-latest.json
└── my-tickets.json
```

Delete `tickets/` anytime to clear cached data.

## Operations

| Command | Description |
|---------|-------------|
| get | Fetch ticket details |
| search | Query with JQL |
| my tickets | Your open tickets |
| create | New ticket |
| update | Modify fields |
| comment | Add comment |
| transition | Change status |

## Requirements

- `curl` (standard)
- `jq` — install: `brew install jq`

## Troubleshooting

| Error | Fix |
|-------|-----|
| 401 Unauthorized | Check JIRA_USER (email) and JIRA_TOKEN |
| 403 Forbidden | User lacks permission |
| 404 Not Found | Check ticket key or JIRA_URL |
