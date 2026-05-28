# Folders API

Gmail uses "labels", others use "folders" - Nylas consolidates both.

## List Folders
```
GET /v3/grants/{grant_id}/folders
```

**Response:**
```json
{
  "data": [{
    "id": "string",
    "grant_id": "string",
    "name": "string",
    "parent_id": "string (Microsoft only)",
    "system_folder": "boolean",
    "total_count": "number",
    "unread_count": "number",
    "attributes": ["\\Inbox", "\\Sent", "\\Drafts", "\\Trash", "\\Junk", "\\Archive"],
    "text_color": "string (Google only)",
    "background_color": "string (Google only)"
  }]
}
```

## Get Folder
```
GET /v3/grants/{grant_id}/folders/{folder_id}
```

## Create Folder
```
POST /v3/grants/{grant_id}/folders
```

```json
{
  "name": "string",
  "parent_id": "string (Microsoft/EWS only)",
  "text_color": "#000000 (Google only)",
  "background_color": "#FFFFFF (Google only)"
}
```

## Update Folder
```
PUT /v3/grants/{grant_id}/folders/{folder_id}
```

## Delete Folder
```
DELETE /v3/grants/{grant_id}/folders/{folder_id}
```

**WARNING**: Deletes ALL contained messages.

## Important Notes

- Cannot filter folders by keyword (e.g., `in:inbox` returns 400)
- Use folder IDs, not names, for filtering messages
- Use `attributes` field to identify semantic folders across providers
- Nested folders are flattened with `parent_id` field
