# Messages API

## List Messages
```
GET /v3/grants/{grant_id}/messages
```

**Query Parameters:**
- `limit`: 1-100 (default 50)
- `page_token`: Pagination cursor
- `in`: Folder ID (NOT folder name for Google)
- `subject`, `from`, `to`: String filters
- `received_before`/`received_after`: Unix timestamps
- `search_query_native`: Provider-native search
- `unread`, `starred`, `has_attachments`: Boolean filters

**Response:**
```json
{
  "data": [{
    "id": "string",
    "grant_id": "string",
    "thread_id": "string",
    "subject": "string",
    "from": [{"name": "string", "email": "string"}],
    "to": [{"name": "string", "email": "string"}],
    "cc": [{"name": "string", "email": "string"}],
    "bcc": [{"name": "string", "email": "string"}],
    "date": "number (unix timestamp)",
    "unread": "boolean",
    "starred": "boolean",
    "snippet": "string",
    "body": "string (HTML)",
    "folders": ["folder_ids"],
    "attachments": [{
      "id": "string",
      "filename": "string",
      "content_type": "string",
      "size": "number",
      "is_inline": "boolean"
    }]
  }],
  "next_cursor": "string"
}
```

## Get Single Message
```
GET /v3/grants/{grant_id}/messages/{message_id}
```

**Query Parameters:**
- `fields=include_headers`: Include email headers
- `fields=raw_mime`: Get Base64url-encoded MIME data

## Update Message
```
PUT /v3/grants/{grant_id}/messages/{message_id}
```

```json
{
  "unread": "boolean",
  "starred": "boolean",
  "folders": ["folder_ids"]
}
```

## Delete Message
```
DELETE /v3/grants/{grant_id}/messages/{message_id}
```
Soft-deletes (moves to trash).

---

## Clean/Parse Messages

```
PUT /v3/grants/{grant_id}/messages/clean
```

Parse up to 20 messages with ML cleaning:

```json
{
  "message_id": ["id1", "id2"],
  "ignore_links": true,
  "ignore_images": true,
  "ignore_tables": true,
  "remove_conclusion_phrases": true,
  "html_as_markdown": false
}
```

Returns `conversation` (cleaned text) and optionally `email_as_markdown`.
