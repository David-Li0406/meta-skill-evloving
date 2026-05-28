# Contacts API

Access user's contacts from email providers.

## List Contacts
```
GET /v3/grants/{grant_id}/contacts
```

**Query Parameters:** `limit`, `page_token`, `email`, `phone_number`, `source`, `group`

## Get Contact
```
GET /v3/grants/{grant_id}/contacts/{contact_id}
```

## Create Contact
```
POST /v3/grants/{grant_id}/contacts
```

```json
{
  "given_name": "string",
  "surname": "string",
  "emails": [{"email": "string", "type": "work|home|other"}],
  "phone_numbers": [{"number": "string", "type": "string"}],
  "company_name": "string",
  "job_title": "string",
  "notes": "string"
}
```

## Update Contact
```
PUT /v3/grants/{grant_id}/contacts/{contact_id}
```

## Delete Contact
```
DELETE /v3/grants/{grant_id}/contacts/{contact_id}
```
