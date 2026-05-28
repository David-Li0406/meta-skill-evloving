---
name: nylas-email
description: |
  Nylas Email API v3 integration for reading, sending, and managing emails across providers (Google, Microsoft, IMAP).
  Use when: (1) Reading/listing emails or threads, (2) Sending emails with attachments, (3) Managing drafts,
  (4) Working with folders/labels, (5) Scheduling email sends, (6) Email tracking (opens/clicks),
  (7) Smart compose with AI, (8) Working with contacts, or (9) Any Nylas email API integration.
---

# Nylas Email API v3

## Quick Reference

**Base URL:** `https://api.us.nylas.com/v3` (US) or `https://api.eu.nylas.com/v3` (EU)

**Auth:** `Authorization: Bearer <NYLAS_API_KEY>`

**Key Concept:** `grant_id` identifies an authenticated user account.

## Common Operations

### List Messages
```
GET /v3/grants/{grant_id}/messages?limit=50&unread=true
```

### Send Message
```
POST /v3/grants/{grant_id}/messages/send
```
```json
{
  "to": [{"email": "recipient@example.com"}],
  "subject": "Subject",
  "body": "<p>HTML body</p>"
}
```

### Reply to Thread
```json
{
  "to": [{"email": "recipient@example.com"}],
  "subject": "Re: Original",
  "body": "<p>Reply</p>",
  "reply_to_message_id": "original_message_id"
}
```

### List Folders
```
GET /v3/grants/{grant_id}/folders
```

Use `attributes` field to find semantic folders (`\Inbox`, `\Sent`, `\Drafts`, `\Trash`).

## Reference Documentation

- **[messages.md](references/messages.md)** - List, read, update, delete messages; clean/parse API
- **[sending.md](references/sending.md)** - Send messages, attachments, scheduled send, unsubscribe headers
- **[drafts.md](references/drafts.md)** - Create, update, send drafts
- **[threads.md](references/threads.md)** - Thread management and threading behavior
- **[folders.md](references/folders.md)** - Folders/labels across providers
- **[attachments.md](references/attachments.md)** - Download and manage attachments
- **[contacts.md](references/contacts.md)** - Contact CRUD operations
- **[tracking.md](references/tracking.md)** - Open/click tracking and webhooks
- **[smart-compose.md](references/smart-compose.md)** - AI email generation
- **[webhooks.md](references/webhooks.md)** - Webhook event types
- **[providers.md](references/providers.md)** - Google/Microsoft/IMAP differences
- **[errors.md](references/errors.md)** - Error codes and rate limits

## Critical Notes

1. **Folder filtering**: Use folder IDs, not names (especially for Google)
2. **Send timeout**: Set 150 seconds (Exchange can take 2 minutes)
3. **Attachment limits**: 10MB instant, 3MB scheduled
4. **Thread body**: Thread endpoint doesn't return body - fetch messages separately
