---
name: email-management-himalaya
description: Use this skill to manage emails via the Himalaya CLI client, allowing you to list, read, send, reply to, and organize emails across multiple accounts.
---

# Email Management with Himalaya

This skill provides comprehensive email management capabilities using the Himalaya CLI email client.

## Configured Accounts

Configure your accounts in `~/.config/himalaya/config.toml`. Example:

| Account Name | Email | Purpose |
|--------------|-------|---------|
| **Work** | work@example.com | Work - Default |
| **Personal** | personal@gmail.com | Personal |

## Core Commands

### Listing Emails

```bash
# List inbox (default account)
himalaya envelope list --page-size <size>

# List from specific account
himalaya envelope list --account "<Account Name>" --page-size <size>

# List from specific folder
himalaya envelope list --folder "<Folder Name>" --page-size <size>

# JSON output for parsing
himalaya envelope list --output json --page-size <size>
```

### Reading Emails

```bash
# Read email by ID
himalaya message read <id>

# Read in plain text
himalaya message read <id> --header "From,To,Subject,Date"
```

**IMPORTANT: Keeping Emails Unread**

To preserve the unread status after reading:

```bash
# After reading, mark back as unread
himalaya flag remove <id> Seen
```

### Sending Emails

```bash
# Send using heredoc
himalaya message send --account "<Account Name>" <<'EOF'
From: Display Name <email@example.com>
To: recipient@example.com
Subject: Subject Line

Email body here.

Signature
EOF
```

### Replying to Emails

```bash
# Reply to an email
himalaya message reply <id> <<'EOF'
Reply body here.
EOF
```

### Managing Flags

```bash
# Mark as read
himalaya flag add <id> Seen

# Mark as unread
himalaya flag remove <id> Seen

# Star/flag email
himalaya flag add <id> Flagged

# Remove star
himalaya flag remove <id> Flagged
```

### Searching Emails

```bash
# Search by subject
himalaya envelope list --query "subject:keyword"

# Search by sender
himalaya envelope list --query "from:sender@example.com"
```

### Folders

```bash
# List folders
himalaya folder list
```

## Workflow Guidelines

1. **Listing emails**: Use `envelope list` - this does NOT mark emails as read.
2. **Reading emails**: After reading with `message read`, immediately run `flag remove <id> Seen` to keep unread unless user indicates otherwise.
3. **Multiple accounts**: Always specify `--account "<Account Name>"` when working with non-default accounts.
4. **Sending emails**: Draft the email content and show to user for approval before sending.
5. **Replying**: Read the original email first to understand context, then draft reply for user approval.

## Common Tasks

### Check unread emails across both accounts

```bash
himalaya envelope list --account "Work" --page-size <size>
himalaya envelope list --account "Personal" --page-size <size>
```

### Read and keep unread

```bash
himalaya message read <id>
himalaya flag remove <id> Seen
```

### Send from personal account

```bash
himalaya message send --account "Personal" <<'EOF'
From: Your Name <personal@gmail.com>
To: recipient@example.com
Subject: Subject

Body
EOF
```

## Prerequisites

1. Himalaya CLI installed (`himalaya --version` to verify).
2. A configuration file at `~/.config/himalaya/config.toml`.
3. IMAP/SMTP credentials configured (password stored securely).

## Configuration Setup

Run the interactive wizard to set up an account:

```bash
himalaya account configure
```

Or create `~/.config/himalaya/config.toml` manually:

```toml
[accounts.personal]
email = "you@example.com"
display-name = "Your Name"
default = true

backend.type = "imap"
backend.host = "imap.example.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "you@example.com"
backend.auth.type = "password"
backend.auth.cmd = "pass show email/imap"  # or use keyring

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.example.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "you@example.com"
message.send.backend.auth.type = "password"
message.send.backend.auth.cmd = "pass show email/smtp"
```

## Tips

- Use `himalaya --help` or `himalaya <command> --help` for detailed usage.
- Message IDs are relative to the current folder; re-list after folder changes.
- Store passwords securely using `pass`, system keyring, or a command that outputs the password.