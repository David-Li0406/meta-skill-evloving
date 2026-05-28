---
name: google-workspace
description: Use this skill when you need to integrate with Google Workspace APIs, including Docs, Sheets, Drive, Gmail, and Calendar, for automation and data management.
---

# Google Workspace Integration Skill

This skill provides integration with Google Workspace APIs, allowing for automation of tasks involving Google Docs, Sheets, Drive, Gmail, and Calendar.

## ⚠️ Important: Accessing Google Drive/Docs URLs

**Direct access to Google Drive/Docs URLs via WebFetch is not possible!** Due to JavaScript dynamic loading, external content retrieval is not feasible.

```
┌─────────────────────────────────────────────────────────────┐
│  Accessing Google URLs                                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ❌ Not Possible:                                           │
│     WebFetch("https://drive.google.com/drive/folders/...")│
│     → Returns an empty page or login page only             │
│                                                             │
│  ✅ Correct Method:                                         │
│     1. Use this skill's Python code (API authentication required)│
│     2. Extract folder ID → call list_files() function      │
│                                                             │
│  Extracting ID from URL:                                   │
│     drive.google.com/drive/folders/{FOLDER_ID}            │
│     docs.google.com/document/d/{DOC_ID}/edit              │
│     docs.google.com/spreadsheets/d/{SHEET_ID}/edit        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### URL to API Conversion Example

| URL Type     | Example URL                              | Extracted ID | API Call   |
|--------------|------------------------------------------|---------------|------------|
| Drive Folder  | `drive.google.com/drive/folders/1Jwdl...` | `1Jwdl...`    | `list_files()` |