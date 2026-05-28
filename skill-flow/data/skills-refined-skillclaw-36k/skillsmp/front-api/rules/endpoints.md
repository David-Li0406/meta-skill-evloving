# Front API Endpoints

## Conversations

### Get Conversation

```
GET /conversations/{conversation_id}
```

Response: `Conversation`

### List Conversation Messages

```
GET /conversations/{conversation_id}/messages
```

Query params:
- `page_token` - Pagination token
- `limit` - Max results (default 50)

Response: `PaginatedResponse<Message>`

### Get Conversation Inboxes

```
GET /conversations/{conversation_id}/inboxes
```

Response: `PaginatedResponse<Inbox>`

### Create Draft Reply

```
POST /conversations/{conversation_id}/drafts
```

Body:
```json
{
  "author_id": "tea_xxx",          // Required
  "channel_id": "cha_xxx",         // Channel to send from
  "to": ["email@example.com"],     // Optional, defaults to conversation recipients
  "cc": ["cc@example.com"],        // Optional
  "bcc": ["bcc@example.com"],      // Optional
  "subject": "Re: Subject",        // Optional
  "body": "<p>HTML content</p>",   // Required, HTML
  "attachments": [file],           // Optional, multipart
  "signature_id": "sig_xxx",       // Optional
  "should_add_default_signature": false,  // Optional
  "mode": "shared"                 // "private" or "shared" (visible to team)
}
```

Response: `Draft` (or just `{ id: string }` with passthrough)

### Send Reply (Immediate)

```
POST /conversations/{conversation_id}/messages
```

Body: Same as draft, but sends immediately.

Response: `Message`

### Add Tags

```
POST /conversations/{conversation_id}/tags
```

Body:
```json
{
  "tag_ids": ["tag_xxx", "tag_yyy"]
}
```

Response: 204 No Content

### Remove Tags

```
DELETE /conversations/{conversation_id}/tags
```

Body:
```json
{
  "tag_ids": ["tag_xxx"]
}
```

Response: 204 No Content

## Messages

### Get Message

```
GET /messages/{message_id}
```

Response: `Message`

Note: Add `?format=eml` to get raw EML format.

## Drafts

### Update Draft

```
PATCH /drafts/{draft_id}
```

Body (all optional):
```json
{
  "author_id": "tea_xxx",
  "to": ["email@example.com"],
  "cc": ["cc@example.com"],
  "bcc": ["bcc@example.com"],
  "subject": "New subject",
  "body": "<p>Updated content</p>",
  "attachments": [file],
  "channel_id": "cha_xxx",
  "mode": "shared"
}
```

Response: 204 No Content

### Delete Draft

```
DELETE /drafts/{draft_id}
```

Response: 204 No Content

## Message Templates

### List Templates

```
GET /message_templates
```

Query params:
- `sort_by` - Field to sort by
- `sort_order` - `asc` or `desc`

Response: `PaginatedResponse<MessageTemplate>`

### List Template Folders

```
GET /message_template_folders
```

Response: `PaginatedResponse<MessageTemplateFolder>`

### Get Template

```
GET /message_templates/{message_template_id}
```

Response: `MessageTemplate`

### Create Template

```
POST /message_templates
```

Body:
```json
{
  "name": "Template Name",
  "subject": "Email Subject",
  "body": "<p>Template content with {{variables}}</p>",
  "folder_id": "fld_xxx",           // Optional
  "inbox_ids": ["inb_xxx"],         // Restrict to inboxes, or omit for all
  "attachments": [file]             // Optional, multipart
}
```

Response: `MessageTemplate`

### Create Inbox Template

```
POST /inboxes/{inbox_id}/message_templates
```

Body: Same as create template.

Response: `MessageTemplate`

### Update Template

```
PATCH /message_templates/{message_template_id}
```

Body (all optional):
```json
{
  "name": "New Name",
  "subject": "New Subject",
  "body": "<p>New content</p>",
  "folder_id": "fld_xxx",
  "inbox_ids": ["inb_xxx"]
}
```

Response: 204 No Content

### Delete Template

```
DELETE /message_templates/{message_template_id}
```

Response: 204 No Content

## Inboxes

### List Inboxes

```
GET /inboxes
```

Response: `PaginatedResponse<Inbox>`

### Get Inbox

```
GET /inboxes/{inbox_id}
```

Response: `Inbox`

### List Inbox Channels

```
GET /inboxes/{inbox_id}/channels
```

Response: `PaginatedResponse<Channel>`

## Channels

### Get Channel

```
GET /channels/{channel_id}
```

Response: `Channel`

## Tags

### List Tags

```
GET /tags
```

Response: `PaginatedResponse<Tag>`

### Create Tag

```
POST /tags
```

Body:
```json
{
  "name": "Tag Name",
  "highlight": "blue",       // Optional color
  "is_visible_in_conversation_lists": true
}
```

Response: `Tag`

## Contacts

### Get Contact

```
GET /contacts/{contact_id}
```

Response: `Contact`

### List Contacts

```
GET /contacts
```

Query params:
- `q` - Search query
- `page_token` - Pagination
- `limit` - Max results
- `sort_by` - Field
- `sort_order` - `asc` or `desc`

Response: `PaginatedResponse<Contact>`

## Teammates

### List Teammates

```
GET /teammates
```

Response: `PaginatedResponse<Teammate>`

### Get Teammate

```
GET /teammates/{teammate_id}
```

Response: `Teammate`

## Utility

### Get Token Info

```
GET /me
```

Response:
```json
{
  "_links": { "self": "..." },
  "id": "tea_xxx",
  "email": "user@example.com",
  "username": "user",
  "first_name": "First",
  "last_name": "Last",
  "is_admin": true,
  "is_available": true,
  "is_blocked": false
}
```

### Download Attachment

```
GET /download/{attachment_link_id}
```

Response: File binary

## Rate Limits

- 120 requests per minute per token
- 429 response when exceeded
- `Retry-After` header indicates wait time
