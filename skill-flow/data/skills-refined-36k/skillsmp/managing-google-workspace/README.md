# Google Workspace Tools

This directory contains tools for interacting with Google Workspace services.

## Available Tools

| Service | Tools |
|---------|-------|
| Gmail | Search, read, send emails, list labels |
| Calendar | List calendars, get/create/delete events |
| Drive | List files, search, get file details, read text files |
| Tasks | Manage task lists and individual tasks |
| Docs | Search, create, edit documents, find/replace |
| Sheets | Read, write, create spreadsheets, manage sheets |
| Slides | Create presentations, add slides and text |
| Forms | Create forms, read responses |
| Chat | List spaces, send/read messages |

## Setup

### 1. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click **Select a project** → **New Project**
3. Enter a project name (e.g., "HuMCP") and click **Create**

### 2. Enable Required APIs

Navigate to **APIs & Services** → **Library** and enable the APIs you need:

- Gmail API
- Google Calendar API
- Google Drive API
- Google Tasks API
- Google Docs API
- Google Sheets API
- Google Slides API
- Google Forms API
- Google Chat API

### 3. Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. Select **External** (or **Internal** if using Google Workspace)
3. Fill in the required fields:
   - App name: "HuMCP"
   - User support email: your email
   - Developer contact: your email
4. Click **Save and Continue**
5. Skip scopes (they're requested programmatically)
6. **Add test users**: Add your Google account email
7. Click **Save and Continue**

### 4. Create OAuth Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. Select application type:
   - **Desktop app** (recommended for local development)
   - Or **Web application** (add `http://localhost` to redirect URIs)
4. Enter a name (e.g., "HuMCP Desktop Client")
5. Click **Create**
6. Copy the **Client ID** and **Client Secret**

### 5. Configure Environment

Add to your `.env` file:

```bash
GOOGLE_OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=GOCSPX-your-client-secret
```

### 6. First-Time Authentication

When you first call any Google tool:
1. A browser window opens for Google login
2. Sign in with a test user account
3. Grant the requested permissions
4. Tokens are saved to `~/.humcp/google_token.json`

Subsequent calls use the cached token (auto-refreshes when expired).

## Tool Reference

### Gmail (`gmail.py`)

| Tool | Description |
|------|-------------|
| `gmail_search` | Search emails by query |
| `gmail_read` | Read full email content |
| `gmail_send` | Send an email |
| `gmail_labels` | List all labels |

### Calendar (`calendar.py`)

| Tool | Description |
|------|-------------|
| `calendar_list` | List all calendars |
| `calendar_events` | Get upcoming events |
| `calendar_create_event` | Create a new event |
| `calendar_delete_event` | Delete an event |

### Drive (`drive.py`)

| Tool | Description |
|------|-------------|
| `drive_list` | List files in a folder |
| `drive_search` | Search for files |
| `drive_get_file` | Get file metadata |
| `drive_read_text_file` | Read text file content |

### Tasks (`tasks.py`)

| Tool | Description |
|------|-------------|
| `tasks_list_task_lists` | List all task lists |
| `tasks_get_task_list` | Get task list details |
| `tasks_create_task_list` | Create a new task list |
| `tasks_delete_task_list` | Delete a task list |
| `tasks_list_tasks` | List tasks in a list |
| `tasks_get_task` | Get task details |
| `tasks_create_task` | Create a new task |
| `tasks_update_task` | Update a task |
| `tasks_delete_task` | Delete a task |
| `tasks_complete_task` | Mark task as completed |
| `tasks_clear_completed` | Clear completed tasks |

### Docs (`docs.py`)

| Tool | Description |
|------|-------------|
| `docs_search` | Search for documents |
| `docs_get_content` | Get document content |
| `docs_create` | Create a new document |
| `docs_append_text` | Append text to document |
| `docs_find_replace` | Find and replace text |
| `docs_list_in_folder` | List docs in a folder |

### Sheets (`sheets.py`)

| Tool | Description |
|------|-------------|
| `sheets_list_spreadsheets` | List spreadsheets |
| `sheets_get_info` | Get spreadsheet info |
| `sheets_read_values` | Read cell values |
| `sheets_write_values` | Write cell values |
| `sheets_append_values` | Append rows |
| `sheets_create_spreadsheet` | Create spreadsheet |
| `sheets_add_sheet` | Add a sheet tab |
| `sheets_clear_values` | Clear a range |

### Slides (`slides.py`)

| Tool | Description |
|------|-------------|
| `slides_list_presentations` | List presentations |
| `slides_get_presentation` | Get presentation details |
| `slides_create_presentation` | Create presentation |
| `slides_add_slide` | Add a new slide |
| `slides_add_text` | Add text to slide |
| `slides_get_thumbnail` | Get slide thumbnail |

### Forms (`forms.py`)

| Tool | Description |
|------|-------------|
| `forms_list_forms` | List forms |
| `forms_get_form` | Get form details |
| `forms_create_form` | Create a new form |
| `forms_list_responses` | List form responses |
| `forms_get_response` | Get response details |

### Chat (`chat.py`)

| Tool | Description |
|------|-------------|
| `chat_list_spaces` | List chat spaces |
| `chat_get_space` | Get space details |
| `chat_get_messages` | Get messages in space |
| `chat_get_message` | Get a specific message |
| `chat_send_message` | Send a message |

## Authentication Scopes

The tools request only the scopes they need. Available scopes are defined in `auth.py`:

- Gmail: `gmail.readonly`, `gmail.send`, `gmail.modify`
- Calendar: `calendar`, `calendar.readonly`
- Drive: `drive`, `drive.readonly`, `drive.file`
- Tasks: `tasks`, `tasks.readonly`
- Docs: `documents`, `documents.readonly`
- Sheets: `spreadsheets`, `spreadsheets.readonly`
- Slides: `presentations`, `presentations.readonly`
- Forms: `forms.body`, `forms.body.readonly`, `forms.responses.readonly`
- Chat: `chat.spaces.readonly`, `chat.messages`, `chat.messages.readonly`
