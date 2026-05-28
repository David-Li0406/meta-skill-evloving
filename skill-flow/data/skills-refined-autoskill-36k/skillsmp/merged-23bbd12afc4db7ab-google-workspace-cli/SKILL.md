---
name: google-workspace-cli
description: Use this skill for managing Gmail, Calendar, Drive, Contacts, Sheets, and Docs through a command-line interface.
---

# Google Workspace CLI

This skill utilizes the `gog` CLI for interacting with various Google Workspace services, including Gmail, Calendar, Drive, Contacts, Sheets, and Docs. Ensure OAuth setup is completed before use.

## Setup (once)
- Authenticate with your credentials:
  ```bash
  gog auth credentials /path/to/client_secret.json
  gog auth add you@gmail.com --services gmail,calendar,drive,contacts,docs,sheets
  gog auth list
  ```

## Common Commands

### Gmail
- Search emails:
  ```bash
  gog gmail search 'newer_than:7d' --max 10
  ```
- Send email:
  ```bash
  gog gmail send --to a@b.com --subject "Hi" --body "Hello"
  ```
- Send email with multi-line body:
  ```bash
  gog gmail send --to a@b.com --subject "Hi" --body-file ./message.txt
  ```
- Create draft:
  ```bash
  gog gmail drafts create --to a@b.com --subject "Hi" --body-file ./message.txt
  ```

### Calendar
- List events:
  ```bash
  gog calendar events <calendarId> --from <iso> --to <iso>
  ```
- Create event:
  ```bash
  gog calendar create <calendarId> --summary "Title" --from <iso> --to <iso>
  ```

### Drive
- Search files:
  ```bash
  gog drive search "query" --max 10
  ```
- Upload file:
  ```bash
  gog drive upload ./file.pdf --parent <folderId>
  ```

### Contacts
- List contacts:
  ```bash
  gog contacts list --max 20
  ```

### Sheets
- Get sheet data:
  ```bash
  gog sheets get <sheetId> "Tab!A1:D10" --json
  ```
- Update sheet:
  ```bash
  gog sheets update <sheetId> "Tab!A1:B2" --values-json '[["A","B"],["1","2"]]' --input USER_ENTERED
  ```

### Docs
- Export document:
  ```bash
  gog docs export <docId> --format txt --out /tmp/doc.txt
  ```

## Email Formatting
- Prefer plain text for emails. Use `--body-file` for multi-paragraph messages.
- For HTML formatting, use `--body-html` with appropriate HTML tags.

## Notes
- Set `GOG_ACCOUNT=you@gmail.com` to avoid repeating `--account`.
- Use `--json` for parseable output and `--no-input` for scripting.
- Confirm actions before sending emails or creating events.

For more detailed command options, use `--help` on any command.