---
name: microsoft-outlook
description: This skill should be used when the user asks to "read emails", "check outlook", "read hotmail", "list messages", "download email", "check inbox", "microsoft mail", "outlook messages", "get my emails", or mentions Outlook/Hotmail email access. Provides Microsoft Graph API integration for reading and downloading emails from Outlook/Hotmail accounts.
version: 1.0.0
---

# Microsoft Outlook Email Skill

Access Outlook and Hotmail emails via the Microsoft Graph API. Supports reading messages, listing inbox contents, and downloading emails as `.eml` files.

## Prerequisites

Before using email commands, ensure authentication is configured:

1. **Setup credentials** (one-time): `pnpm --prefix "${CLAUDE_PLUGIN_ROOT}" tsx scripts/microsoft.ts setup`
   * *Note: For personal accounts, ensure the app is registered as **Multitenant + Personal Accounts** in the Azure Portal. See the README for detailed steps.*
2. **Authenticate** (per-project): `pnpm --prefix "${CLAUDE_PLUGIN_ROOT}" tsx scripts/microsoft.ts auth`
   * *Tip: Use `auth --browser Safari` on macOS if your default browser is causing issues.*

## Available Commands

All commands output JSON for easy parsing.

### Authentication & Setup

| Command | Description |
|---------|-------------|
| `setup` | Configure Microsoft API credentials (interactive) |
| `auth` | Run OAuth flow - opens browser for login |
| `auth --global` | Store token globally instead of per-project |
| `check` | Verify authentication status |

### User Information

| Command | Description |
|---------|-------------|
| `me` | Get authenticated user profile |

### Email Operations

| Command | Description |
|---------|-------------|
| `messages` | List recent messages (default: 10) |
| `messages --limit N` | List N recent messages |
| `download <id>` | Download specific message as `.eml` file |
| `download-all` | Download recent messages to `./downloads` |
| `download-all --limit N` | Download N recent messages |

## Usage Pattern

Execute commands via:

```bash
pnpm --prefix "${CLAUDE_PLUGIN_ROOT}" tsx scripts/microsoft.ts <command> [options]
```

### Example Workflows

**Check inbox:**
```bash
pnpm --prefix "${CLAUDE_PLUGIN_ROOT}" tsx scripts/microsoft.ts messages --limit 5
```

**Download specific email:**
```bash
pnpm --prefix "${CLAUDE_PLUGIN_ROOT}" tsx scripts/microsoft.ts download <message-id>
```

**Get user profile:**
```bash
pnpm --prefix "${CLAUDE_PLUGIN_ROOT}" tsx scripts/microsoft.ts me
```

## Output Format

All commands return JSON:

**messages response:**
```json
[
  {
    "id": "AAMk...",
    "subject": "Meeting Tomorrow",
    "receivedDateTime": "2024-01-15T10:30:00Z",
    "from": {"emailAddress": {"name": "John", "address": "john@example.com"}},
    "isRead": false,
    "hasAttachments": true
  }
]
```

**me response:**
```json
{
  "id": "user-id",
  "displayName": "User Name",
  "mail": "user@outlook.com",
  "userPrincipalName": "user@outlook.com"
}
```

## Token Storage

- **Project tokens**: `.claude/microsoft-skill.local.json` (default)
- **Global tokens**: `~/.config/microsoft-skill/tokens.json` (with `--global`)

Project tokens allow different Microsoft accounts per project.

## Authentication Flow

The skill uses OAuth 2.0 with PKCE:

1. Run `auth` command
2. Browser opens to Microsoft login
3. Grant permissions (Mail.Read, User.Read)
4. Callback received on `localhost:3000`
5. Token stored for future use

Tokens auto-refresh when expired.

## Troubleshooting

**"Token not found" error:**
Run authentication: `pnpm --prefix "${CLAUDE_PLUGIN_ROOT}" tsx scripts/microsoft.ts auth`

**"No credentials found" error:**
Run setup: `pnpm --prefix "${CLAUDE_PLUGIN_ROOT}" tsx scripts/microsoft.ts setup`

**Token expired:**
The skill auto-refreshes tokens. If issues persist, re-run `auth`.

## Additional Resources

### Reference Files

- **`references/setup-guide.md`** - Detailed Microsoft Entra app registration guide
- **`references/api-reference.md`** - Microsoft Graph API endpoints and types

### Scripts

The main CLI script is at `scripts/microsoft.ts` with supporting libraries in `scripts/lib/`.
