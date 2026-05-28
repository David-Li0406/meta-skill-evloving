---
name: google-docs
description: View and edit Google Docs with rich formatting, tables, and modern Google Drawings diagrams using Google Docs/Drive APIs with gcloud ADC
license: MIT
compatibility: opencode
metadata:
  category: productivity
  system: google-workspace
---

# Google Docs Integration

Use this skill when working with Google Docs, Slides, Sheets, or Drive using the OpenCode custom tools.

## Authentication

The Google Workspace tools use `gcloud auth application-default` credentials. If you encounter a 403 error with `ACCESS_TOKEN_SCOPE_INSUFFICIENT`, the user needs to re-authenticate with the correct scopes.

### Required Scopes

| Scope | Purpose |
|-------|---------|
| `cloud-platform` | GCP resources, Secret Manager, etc. |
| `documents` | Google Docs read/write |
| `presentations` | Google Slides read/write |
| `drive` | Google Drive files and folders |
| `drive.file` | Files created by this app |
| `spreadsheets` | Google Sheets read/write |
| `calendar` | Google Calendar events |
| `calendar.events` | Calendar event management |
| `gmail.modify` | Read/write Gmail messages |
| `gmail.readonly` | Read-only Gmail access |
| `gmail.send` | Send emails |
| `gmail.labels` | Manage Gmail labels |
| `tasks` | Google Tasks |
| `userinfo.email` | User email address |
| `userinfo.profile` | User profile info |

### Detecting Current Quota Project

The quota project is stored in the ADC credentials file. To detect it:

```bash
cat ~/.config/gcloud/application_default_credentials.json | grep quota_project_id
```

Or use jq:
```bash
jq -r '.quota_project_id // empty' ~/.config/gcloud/application_default_credentials.json
```

### Full Authentication Setup

When you see errors like:
- `Request had insufficient authentication scopes`
- `ACCESS_TOKEN_SCOPE_INSUFFICIENT`
- `PERMISSION_DENIED` on Google Docs/Slides/Drive APIs
- `SERVICE_DISABLED`
- `API requires a quota project`

**First, detect or ask for the quota project:**

```bash
# Try to get existing quota project
PROJECT=$(jq -r '.quota_project_id // empty' ~/.config/gcloud/application_default_credentials.json 2>/dev/null)
echo "Current quota project: ${PROJECT:-not set}"
```

If not set, ask the user for their GCP project ID.

**Then run the setup commands:**

**Step 1: Enable the required APIs** on the quota project:

```bash
gcloud services enable \
  docs.googleapis.com \
  slides.googleapis.com \
  drive.googleapis.com \
  sheets.googleapis.com \
  calendar-json.googleapis.com \
  gmail.googleapis.com \
  tasks.googleapis.com \
  --project=$PROJECT
```

**Step 2: Authenticate with all scopes and set quota project**:

```bash
gcloud auth application-default login \
  --billing-project=$PROJECT \
  --scopes="\
https://www.googleapis.com/auth/cloud-platform,\
https://www.googleapis.com/auth/documents,\
https://www.googleapis.com/auth/presentations,\
https://www.googleapis.com/auth/drive,\
https://www.googleapis.com/auth/drive.file,\
https://www.googleapis.com/auth/spreadsheets,\
https://www.googleapis.com/auth/calendar,\
https://www.googleapis.com/auth/calendar.events,\
https://www.googleapis.com/auth/gmail.modify,\
https://www.googleapis.com/auth/gmail.readonly,\
https://www.googleapis.com/auth/gmail.send,\
https://www.googleapis.com/auth/gmail.labels,\
https://www.googleapis.com/auth/tasks,\
https://www.googleapis.com/auth/userinfo.email,\
https://www.googleapis.com/auth/userinfo.profile"
```

Note: `--billing-project` sets the quota project in ADC automatically.

### One-liner Setup (Auto-detect or Prompt)

This command auto-detects existing quota project or prompts for one, enables APIs, and authenticates with all scopes in a single flow:

```bash
PROJECT=${PROJECT:-$(jq -r '.quota_project_id // empty' ~/.config/gcloud/application_default_credentials.json 2>/dev/null)} && \
[ -z "$PROJECT" ] && read -p "Enter GCP project ID: " PROJECT && \
gcloud services enable docs.googleapis.com slides.googleapis.com drive.googleapis.com sheets.googleapis.com calendar-json.googleapis.com gmail.googleapis.com tasks.googleapis.com --project=$PROJECT && \
gcloud auth application-default login \
  --billing-project=$PROJECT \
  --scopes="https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/documents,https://www.googleapis.com/auth/presentations,https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/drive.file,https://www.googleapis.com/auth/spreadsheets,https://www.googleapis.com/auth/calendar,https://www.googleapis.com/auth/calendar.events,https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/gmail.readonly,https://www.googleapis.com/auth/gmail.send,https://www.googleapis.com/auth/gmail.labels,https://www.googleapis.com/auth/tasks,https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/userinfo.profile"
```

Note: `--billing-project` sets the quota project automatically, no need to run `set-quota-project` separately.

This opens a browser for the user to authenticate with all required scopes.

### Automatic Auth Check

If any Google Workspace tool returns a 403/permission error:

1. **Tell the user** they need to authenticate
2. **Provide the command** above
3. **Wait for them** to confirm authentication is complete
4. **Retry the operation**

## Available Tools

### Google Docs

| Tool | Purpose |
|------|---------|
| `google-docs_create` | Create a new Google Doc |
| `google-docs_read` | Read document contents |
| `google-docs_append` | Append text to end of doc |
| `google-docs_find_replace` | Find and replace text |
| `google-docs_get_structure` | Get document headings structure |

### Google Slides

| Tool | Purpose |
|------|---------|
| `google-slides_create` | Create a new presentation |
| `google-slides_read` | Read slide contents |
| `google-slides_add_slide` | Add a new slide |
| `google-slides_update_text` | Update text in a shape |
| `google-slides_get_info` | Get presentation info |
| `google-slides_get_slide_elements` | Get elements on a slide |

### Google Drive

| Tool | Purpose |
|------|---------|
| `google-drive_search` | Search for files |
| `google-drive_list` | List files in a folder |
| `google-drive_download` | Download file content |
| `google-drive_get_file_info` | Get file metadata |

### Google Sheets

| Tool | Purpose |
|------|---------|
| `google-sheets_create` | Create a new spreadsheet |
| `google-sheets_read` | Read cell values |
| `google-sheets_write` | Write cell values |
| `google-sheets_append_rows` | Append rows to sheet |
| `google-sheets_clear` | Clear a range |
| `google-sheets_get_info` | Get spreadsheet info |

### Google Calendar

| Tool | Purpose |
|------|---------|
| `google-calendar_list_events` | List upcoming events |
| `google-calendar_create_event` | Create a new event |
| `google-calendar_update_event` | Update an event |
| `google-calendar_delete_event` | Delete an event |
| `google-calendar_search_events` | Search events by query |
| `google-calendar_list_calendars` | List all calendars |

### Google Gmail

| Tool | Purpose |
|------|---------|
| `google-gmail_list` | List recent emails |
| `google-gmail_read` | Read email content |
| `google-gmail_search` | Search emails |
| `google-gmail_get_thread` | Get email thread |
| `google-gmail_mark_read` | Mark as read |
| `google-gmail_mark_unread` | Mark as unread |

## Creating Design Documents

When creating design documents:

1. **Create the base document** with `google-docs_create`
2. **Add content in sections** - the tool accepts plain text, structure with newlines
3. **For diagrams**, create a separate Google Slides presentation and link to it
4. **Use markdown-style formatting** in the content (will appear as plain text, can be formatted later)

### Example: Create a Design Doc

```
1. google-docs_create(title="My Design Doc", content="# Title\n\n## Overview\n...")
2. google-slides_create(title="My Design Doc - Diagrams")
3. google-slides_add_slide(presentation_id="...", layout="BLANK")
4. Link the slides in the doc
```

## Slide Layouts

Available layouts for `google-slides_add_slide`:

| Layout | Description |
|--------|-------------|
| `BLANK` | Empty slide |
| `TITLE` | Title slide |
| `TITLE_AND_BODY` | Title with body text |
| `TITLE_AND_TWO_COLUMNS` | Title with two columns |
| `TITLE_ONLY` | Just a title |
| `SECTION_HEADER` | Section divider |
| `CAPTION_ONLY` | Caption at bottom |
| `BIG_NUMBER` | Large number display |

## Troubleshooting

### Error: ACCESS_TOKEN_SCOPE_INSUFFICIENT

User needs to re-authenticate with scopes. Run Step 3 then Step 4 from Authentication section.

### Error: SERVICE_DISABLED or "API requires a quota project"

The APIs are not enabled on the quota project, or no quota project is set:

1. Ask user for their GCP project ID (e.g., `ck-orp-nick-dev`)
2. Run Step 1 and Step 2 from Authentication section
3. If still failing, run the full one-liner setup

### Error: Document not found

- Check the document ID is correct
- Verify user has access to the document
- Use `google-drive_search` to find the correct ID

### Error: Rate limit exceeded

Google APIs have rate limits. Wait a few seconds and retry.

### Error: Permission denied (not scope-related)

User may not have access to the document/resource. Check sharing settings in Google Drive.

## Dependencies

- `gcloud` CLI installed and configured
- `bun` runtime for OpenCode tools
- `@opencode-ai/plugin` npm package
