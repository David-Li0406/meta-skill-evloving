# Attachments API

Files are called "Attachments" in v3. Use Messages/Drafts endpoints to add attachments; this API is for reading existing ones.

## Get Attachment Metadata
```
GET /v3/grants/{grant_id}/attachments/{attachment_id}?message_id={message_id}
```

`message_id` query parameter is required.

## Download Attachment
```
GET /v3/grants/{grant_id}/attachments/{attachment_id}/download?message_id={message_id}
```

Returns binary blob. `message_id` query parameter is required.

## Adding Attachments

See [sending.md](sending.md) for adding attachments to messages and drafts.
