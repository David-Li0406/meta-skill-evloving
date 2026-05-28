# Drafts API

Drafts sync with provider (Gmail, Outlook, etc.).

## Create Draft
```
POST /v3/grants/{grant_id}/drafts
```

Request body same as Send Message.

## List Drafts
```
GET /v3/grants/{grant_id}/drafts
```

## Get Draft
```
GET /v3/grants/{grant_id}/drafts/{draft_id}
```

## Update Draft
```
PUT /v3/grants/{grant_id}/drafts/{draft_id}
```

## Delete Draft
```
DELETE /v3/grants/{grant_id}/drafts/{draft_id}
```

## Send Draft
```
POST /v3/grants/{grant_id}/drafts/{draft_id}
```

Sends the draft immediately.
