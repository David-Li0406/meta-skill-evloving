# Threads API

Threads group related messages. Every message belongs to a thread.

## List Threads
```
GET /v3/grants/{grant_id}/threads
```

Query parameters similar to messages: `limit`, `page_token`, `subject`, `from`, `to`, `search_query_native`.

**Response:**
```json
{
  "data": [{
    "id": "string",
    "grant_id": "string",
    "subject": "string",
    "participants": [{"name": "string", "email": "string"}],
    "message_ids": ["string"],
    "draft_ids": ["string"],
    "folders": ["string"],
    "snippet": "string",
    "unread": "boolean",
    "starred": "boolean",
    "has_attachments": "boolean",
    "has_drafts": "boolean",
    "earliest_message_date": "number",
    "latest_message_received_date": "number",
    "latest_message_sent_date": "number",
    "latest_draft_or_message": { /* message object */ }
  }]
}
```

## Get Thread
```
GET /v3/grants/{grant_id}/threads/{thread_id}
```

## Update Thread
```
PUT /v3/grants/{grant_id}/threads/{thread_id}
```

Update `starred`, `unread`, `folders`.

## Delete Thread
```
DELETE /v3/grants/{grant_id}/threads/{thread_id}
```

Soft-deletes the thread.

## Threading Behavior

- Threads are non-linear (tree structure)
- Reply to specific message using `reply_to_message_id` in Send Message
- Thread endpoint does NOT return message body - use Messages endpoint for full content
