---
name: managing-google-workspace
description: Use this skill to manage Google Workspace services including Gmail, Drive, Docs, Sheets, Slides, Calendar, and Contacts. Ideal for creating documents, managing files, sending emails, and scheduling events.
---

# Google Workspace Management

This skill provides tools for interacting with Google Workspace APIs, allowing you to manage various services effectively.

## Authentication

All tools require OAuth2 authentication. Set the following environment variables:
- `GOOGLE_OAUTH_CLIENT_ID`
- `GOOGLE_OAUTH_CLIENT_SECRET`

## Quick Reference

| Service | Common Operations |
|---------|-------------------|
| Gmail | Send, search, read emails |
| Drive | List, upload, download, share files |
| Docs | Create, read, edit documents |
| Sheets | Read, write, query spreadsheets |
| Slides | Create presentations, add slides |
| Calendar | List, create, update events |
| Contacts | Manage contacts and groups |
| Forms | Create forms, get responses |
| Tasks | Manage task lists and tasks |
| Chat | Send messages to spaces |

## Gmail Operations

```python
# Search emails
result = await gmail_search_emails(query="<query>", max_results=<max_results>)

# Send email
result = await gmail_send_email(
    to="<recipient_email>",
    subject="<subject>",
    body="<message_content>"
)

# Read email
result = await gmail_get_email(message_id="<message_id>")
```

## Drive Operations

```python
# List files
result = await drive_list_files(query="<query>", max_results=<max_results>)

# Upload file
result = await drive_upload_file(file_path="<local_file_path>", folder_id="<folder_id>")

# Download file
result = await drive_download_file(file_id="<file_id>", destination="<local_path>")

# Share file
result = await drive_share_file(file_id="<file_id>", email="<user_email>", role="<role>")
```

## Docs Operations

```python
# Create document
result = await docs_create_document(title="<document_title>")

# Read content
result = await docs_get_content(document_id="<document_id>")

# Append text
result = await docs_append_text(document_id="<document_id>", text="<text_to_append>")
```

## Sheets Operations

```python
# Read values
result = await google_sheets_read_values(spreadsheet_id="<spreadsheet_id>", range_notation="<range>")

# Write values
result = await google_sheets_write_values(
    spreadsheet_id="<spreadsheet_id>",
    range_notation="<range>",
    values=[["<value1>", "<value2>"], ["<value3>", "<value4>"]]
)

# Create spreadsheet
result = await google_sheets_create_spreadsheet(title="<spreadsheet_title>", sheet_names=["<sheet_name1>", "<sheet_name2>"])
```

## Slides Operations

```python
# Create presentation
result = await google_slides_create_presentation(title="<presentation_title>")

# Add slide
result = await google_slides_add_slide(presentation_id="<presentation_id>", layout="<layout_type>")

# Add text
result = await google_slides_add_text(
    presentation_id="<presentation_id>",
    slide_id="<slide_id>",
    text="<text_content>",
    x=<x_position>, y=<y_position>
)
```

## Calendar Operations

```python
# List events
result = await calendar_list_events(max_results=<max_results>)

# Create event
result = await calendar_create_event(
    summary="<event_summary>",
    start_time="<start_time>",
    end_time="<end_time>"
)
```

## Contacts Operations

```bash
# List contacts
uv run gws contacts list --max <max_results>

# Create contact
uv run gws contacts create "<contact_name>" --email "<email>" --phone "<phone_number>"

# Update contact
uv run gws contacts update <resource_name> --email "<new_email>"

# Delete contact
uv run gws contacts delete <resource_name>
```

## Document Conversion

```bash
# Markdown to Google Doc
uv run gws convert md-to-doc /path/to/document.md --title "<document_title>"

# Markdown to Google Slides
uv run gws convert md-to-slides /path/to/presentation.md --title "<presentation_title>"

# Markdown to PDF
uv run gws convert md-to-pdf /path/to/document.md /path/to/output.pdf
```

## Output Format

All commands return JSON for easy parsing:
```json
{
  "success": true,
  "data": { ... }
}
```
On error:
```json
{
  "success": false,
  "error": "<error_description>"
}
```

## Safety Guidelines

- Always confirm with the user before performing destructive operations such as deleting documents, files, or contacts.
- Read documents or spreadsheets before modifying to understand their structure.
- Preserve the user's original content when converting or editing documents.

## Additional Resources

For detailed setup instructions and OAuth configuration, refer to the relevant documentation.