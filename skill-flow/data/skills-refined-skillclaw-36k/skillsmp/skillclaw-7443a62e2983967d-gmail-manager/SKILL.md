---
name: gmail-manager
description: Use this skill when you want to manage your Gmail account, including sending, reading, searching emails, and managing labels and drafts.
---

# Gmail Manager Skill

This skill provides comprehensive Gmail integration through lightweight CLI scripts. All operations are token-efficient and composable.

## First-Time Setup

Before using this skill, you must set up OAuth authentication:

1. **Install dependencies:**
   ```bash
   cd ~/.claude/skills/gmail-manager && npm install
   ```

2. **Set up Google Cloud credentials:**
   - Follow the guide in `docs/google-cloud-setup.md`
   - Download `credentials.json` and save to `scripts/auth/credentials.json`

3. **Authenticate:**
   ```bash
   cd ~/.claude/skills/gmail-manager && npm run setup
   ```

This will open a browser for Google OAuth and save your token locally.

## Multi-Account Support

The Gmail Manager skill supports multiple accounts (e.g., personal and work email):

### Add Additional Accounts

```bash
# Add a second account (from skill directory)
npm run setup -- --account work

# Add a third account
npm run setup -- --account personal
```

Each account needs separate OAuth authentication.

### Manage Accounts

```bash
# List all configured accounts
node scripts/manage-accounts.js --list

# Set default account (used when --account is not specified)
node scripts/manage-accounts.js --set-default work

# Remove an account
node scripts/manage-accounts.js --remove old-account
```

### Using Specific Accounts

All Gmail operations support the `--account` parameter:

```bash
# Send email from work account
node gmail-send.js --account work --to "user@example.com" --subject "..." --body "..."

# Send from personal (or omit --account to use default)
node gmail-send.js --account personal --to "friend@example.com" --subject "..." --body "..."

# Search work emails
node gmail-search.js --account work --query "is:unread"
```

If `--account` is not specified, the default account is used.

## Usage Guidelines

### 1. Read Documentation On-Demand

When first using Gmail operations, read the comprehensive README:
```bash
cat ~/.claude/skills/gmail-manager/README.md
```

This provides detailed usage examples for all operations.

### 2. Execute Scripts via Bash

All scripts are in the `scripts/` directory and output JSON for easy parsing:

```bash
cd ~/.claude/skills/gmail-manager/scripts
```

### 3. Parse JSON Output

All scripts return JSON. Parse the output and present relevant information as needed.