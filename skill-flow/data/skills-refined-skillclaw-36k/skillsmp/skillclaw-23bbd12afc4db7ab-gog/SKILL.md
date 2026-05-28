---
name: gog
description: Use this skill when you need to interact with Google Workspace services like Gmail, Calendar, Drive, Contacts, Sheets, and Docs via the command line.
---

# Skill body

## Setup (once)
1. Authenticate with your Google account:
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
- Send an email:
  ```bash
  gog gmail send --to a@b.com --subject "Hi" --body "Hello"
  ```
- Send an email with a file:
  ```bash
  gog gmail send --to a@b.com --subject "Hi" --body-file ./message.txt
  ```
- Create a draft:
  ```bash
  gog gmail drafts create --to a@b.com --subject "Hi" --body-file ./message.txt
  ```

### Calendar
- List events:
  ```bash
  gog calendar events <calendarId> --from <iso> --to <iso>
  ```
- Create an event:
  ```bash
  gog calendar create <calendarId> --summary "Title" --from <iso> --to <iso>
  ```

### Drive
- Search files:
  ```bash
  gog drive search "query" --max 10
  ```
- Upload a file:
  ```bash
  gog drive upload ./file.pdf --parent <folderId>
  ```

### Contacts
- List contacts:
  ```bash
  gog contacts list --max 20
  ```

### Sheets
- Get data from a sheet:
  ```bash
  gog sheets get <sheetId> "Tab!A1:D10" --json
  ```
- Update a sheet:
  ```bash
  gog sheets update <sheetId> "Tab!A1:B2" --values-json '[["A","B"],["1","2"]]' --input USER_ENTERED
  ```

### Docs
- Export a document:
  ```bash
  gog docs export <docId> --format txt --out /tmp/doc.txt
  ```

Use `--json` for parseable output and `--help` on any command for options.