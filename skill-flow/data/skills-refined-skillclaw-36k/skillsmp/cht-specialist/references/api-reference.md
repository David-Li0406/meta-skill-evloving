# CHT REST API Reference

RESTful APIs for integrating with CHT applications.

## Timestamp Formats

Supported formats:
- ISO 8601: `YYYY-MM-DDTHH:mm:ssZ` or `YYYY-MM-DDTHH:mm:ss.SSSZ`
- Milliseconds since Unix Epoch: `1467383343484`

## Settings

### GET /api/v1/settings
Returns app settings in JSON format.

### PUT /api/v1/settings

| Parameter | Description |
|-----------|-------------|
| `overwrite` | Replace entire settings document (default: false) |
| `replace` | Replace existing settings for given properties (default: false, merging) |

## Export Endpoints

All export endpoints support `humanReadable` parameter for date formatting.

### GET /api/v2/export/dhis
Export target data as DHIS2 dataValueSet.

| Parameter | Description | Required |
|-----------|-------------|----------|
| `dataSet` | DHIS2 dataSet ID | Yes |
| `date.from` | Filter to month of this timestamp | Yes |
| `orgUnit` | Filter by contact's `dhis.orgUnit` attribute | No |

### GET /api/v2/export/reports
Export reports as CSV.

```json
POST /api/v2/export/reports
{
  "filters": {
    "forms": {
      "selected": [{ "code": "immunization_visit" }]
    }
  }
}
```

### GET /api/v2/export/messages
Export messages with columns: Record UUID, Patient ID, Reported Date, From, Contact Name, Message Type, State, Timestamps, Sent By, To Phone, Message Body.

### GET /api/v2/export/feedback
Export user feedback.

| Parameter | Description |
|-----------|-------------|
| `format` | 'csv' or 'xml' (default: csv) |
| `locale` | Locale for translations (default: 'en') |
| `tz` | Timezone offset in minutes from GMT |
| `skip_header_row` | Omit column headings |

### GET /api/v2/export/contacts
Returns JSON array of contacts with: id, rev, name, patient_id, type, contact_type, place_id.

### GET /api/v2/export/user-devices
*Added 4.7.0* - Returns CHT software versions and device info per user device.

## Forms

### GET /api/v1/forms
Returns list of installed forms. With `X-OpenRosa-Version: 1.0` header returns XML format.

### GET /api/v1/forms/{{id}}.{{format}}
Return form definition by ID and format (xml, json).

### POST /api/v1/forms/validate
*Added 3.12.0* - Validate XForm. Requires `can_configure` permission.

## Records

### POST /api/v2/records
Create record from JSON form.

**Form Parameters:**
| Parameter | Description |
|-----------|-------------|
| `message` | Message string (Muvuku/Textforms format) |
| `from` | Reporting phone number |
| `sent_timestamp` | MS since Unix Epoch (default: now) |

**JSON Properties:**
| Key | Description |
|-----|-------------|
| `_meta.form` | Form code |
| `_meta.from` | Phone number (optional) |
| `_meta.reported_date` | Timestamp (default: now) |
| `_meta.locale` | Locale string |

## Contact API

### GET /api/v1/contact/{{uuid}}
*Added 4.18.0* - Returns contact data. Permission: `can_view_contacts`.

| Parameter | Description |
|-----------|-------------|
| `with_lineage` | Include parent lineage (default: false) |

### GET /api/v1/contact/uuid
*Added 4.18.0* - Returns array of contact UUIDs.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `type` | Yes if no freetext | Contact type ID |
| `freetext` | Yes if no type | Search term (min 3 chars) |
| `cursor` | No | Pagination token |
| `limit` | No | Max results (default: 10000) |

## Person API

### GET /api/v1/person/{{uuid}}
*Added 4.9.0* - Returns person data. Permission: `can_view_contacts`.

### GET /api/v1/person
*Added 4.11.0* - Returns paginated array of people.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `type` | Yes | Contact type ID |
| `cursor` | No | Pagination token |
| `limit` | No | Max results (default: 100) |

### POST /api/v1/people
Create new people. Permissions: `can_create_people`, `can_create_places`.

**Required:** `name`, `type`
**Optional:** `place`, `reported_date`

```json
{
  "name": "Hannah",
  "phone": "+2548277210095",
  "type": "contact",
  "contact_type": "patient",
  "place": "1d83f2b4a27eceb40df9e9f9ad06d137"
}
```

## Place API

### GET /api/v1/place/{{uuid}}
*Added 4.10.0* - Returns place data.

### GET /api/v1/place
*Added 4.12.0* - Returns paginated array of places.

### POST /api/v1/places
Create new places. Permissions: `can_create_places`.

**Required:** `name`, `type`
**Optional:** `parent`, `contact`, `reported_date`

### POST /api/v1/places/{{uuid}}
Update existing place.

## Users

### GET /api/v1/users
Returns list of users and their associated places.

### GET /api/v1/users-info
Returns users summary info for admin.

### POST /api/v1/users
Create new user.

| Property | Description |
|----------|-------------|
| `username` | User's unique username |
| `password` | Password (min 8 chars, or use token_login) |
| `roles` | Array of role names |
| `place` | Place ID or object |
| `contact` | Contact ID or object |
| `phone` | Phone number (for token_login) |
| `token_login` | Enable SMS login link |

### POST /api/v1/users/{{username}}
Update existing user.

### DELETE /api/v1/users/{{username}}
Delete user.

## SMS

### POST /api/sms
Endpoint for cht-gateway to send SMS messages.

### POST /api/v1/sms/{aggregator}/{endpoint}
Integration endpoint for SMS aggregators (RapidPro, Africa's Talking).

## Reports

### GET /api/v1/report/{{uuid}}
*Added 4.13.0* - Returns report data.

### GET /api/v1/report
*Added 4.13.0* - Returns paginated array of reports.

## Hydration

### POST /api/v1/hydrate
*Added 4.10.0* - Hydrate documents with full lineage.

```json
{
  "doc_ids": ["uuid1", "uuid2"]
}
```

## Bulk Operations

### POST /api/v1/bulk-delete
Delete multiple docs.

```json
{
  "docs": [
    { "_id": "id1", "_rev": "1-abc" },
    { "_id": "id2", "_rev": "2-def" }
  ]
}
```

## Upgrades

### GET /api/v1/upgrade
Get current upgrade status.

### POST /api/v1/upgrade
Start upgrade to specified version.

### DELETE /api/v1/upgrade
Abort current upgrade.

## Monitoring

### GET /api/v2/monitoring
Returns server monitoring metrics.

## Login

### POST /api/v1/login
Token-based authentication.

### POST /{{locale}}/login/token/{{token}}
Login by SMS token (requires `token_login` enabled).

## Replication

### GET /api/v1/replication/get-ids
Get document IDs for replication.

### POST /api/v1/replication/get-deletes
Get deleted document IDs.

## Version Info

| Endpoint | Version Added |
|----------|---------------|
| Contact UUID endpoint | 4.18.0 |
| Report API | 4.13.0 |
| Place pagination | 4.12.0 |
| Person pagination | 4.11.0 |
| Place GET | 4.10.0 |
| Hydrate | 4.10.0 |
| Person GET | 4.9.0 |
| User devices export | 4.7.0 |
| Form validation | 3.12.0 |
