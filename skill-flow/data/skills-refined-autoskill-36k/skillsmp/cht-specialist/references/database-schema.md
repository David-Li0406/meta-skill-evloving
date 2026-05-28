# Database Schema Reference

Complete reference for CHT CouchDB/PouchDB document schemas.

## Overview

CHT uses CouchDB (server) and PouchDB (client) as JSON-based NoSQL datastores. While there's no enforced schema, code follows consistent conventions.

## Common Properties

All documents have:

| Property | Description | Required |
|----------|-------------|----------|
| `_id` | CouchDB's unique identifier | All records |
| `_rev` | CouchDB's revision marker | All records |
| `type` | General document type | User-created docs |
| `reported_date` | Timestamp of creation | User-created docs |

## Contacts (Persons and Places)

### Contact Types

**Version 3.7+:**
- `type: 'contact'`
- `contact_type: 'configured_type'`

**Earlier versions:**
- `type: 'district_hospital'` | `'health_centre'` | `'clinic'` | `'person'`

### Person Document

```json
{
  "_id": "person-uuid",
  "_rev": "1-abc123",
  "type": "person",
  "name": "Jane Doe",
  "date_of_birth": "1990-01-15",
  "sex": "female",
  "phone": "+1234567890",
  "patient_id": "12345",
  "reported_date": 1609459200000,
  "parent": {
    "_id": "clinic-id",
    "parent": {
      "_id": "health_center-id",
      "parent": {
        "_id": "district_hospital-id"
      }
    }
  },
  "linked_docs": {
    "custom_tag": "other-doc-id"
  }
}
```

### Place Document

```json
{
  "_id": "clinic-uuid",
  "_rev": "1-xyz789",
  "type": "clinic",
  "name": "Smith Family",
  "reported_date": 1609459200000,
  "contact": {
    "_id": "primary-contact-person-id",
    "name": "John Smith"
  },
  "parent": {
    "_id": "health_center-id",
    "parent": {
      "_id": "district_hospital-id"
    }
  }
}
```

### Parent Hierarchy

**Stored (minified):**
```json
{
  "parent": {
    "_id": "clinic-id",
    "parent": {
      "_id": "health_center-id"
    }
  }
}
```

**Hydrated (in app):**
```json
{
  "parent": {
    "_id": "clinic-id",
    "name": "A clinic",
    "reported_date": 1234,
    "parent": {
      "_id": "health_center-id",
      "name": "A Health Centre",
      "reported_date": 1134
    }
  }
}
```

### Linked Docs (3.10+)

```json
{
  "linked_docs": {
    "referral_facility": "health-center-id",
    "emergency_contact": "other-person-id"
  }
}
```

## Reports (data_record)

### Report Structure

```json
{
  "_id": "report-uuid",
  "_rev": "1-def456",
  "type": "data_record",
  "form": "pregnancy",
  "content_type": "xml",
  "reported_date": 1609459200000,
  "from": "+1234567890",
  "contact": {
    "_id": "submitter-person-id",
    "parent": {
      "_id": "clinic-id"
    }
  },
  "fields": {
    "patient_id": "12345",
    "patient_uuid": "patient-contact-uuid",
    "lmp_date": "2024-01-15",
    "edd": "2024-10-22",
    "risk_factors": ["anemia", "hypertension"],
    "danger_signs": []
  },
  "_attachments": {
    "content": {
      "content_type": "application/xml",
      "data": "base64-encoded-xml..."
    }
  }
}
```

### SMS Report Additional Fields

```json
{
  "sms_message": {
    "from": "+1234567890",
    "message": "P 12345 2024-01-15",
    "sent_timestamp": 1609459200000
  }
}
```

### Subject Association

Reports link to contacts via:
1. `doc.fields.patient_id` or `doc.fields.patient_uuid` (person)
2. `doc.fields.place_id` (place)
3. `doc.patient_id` or `doc.place_id` (top-level)

## Forms

### XML Form Document

```json
{
  "_id": "form:pregnancy",
  "type": "form",
  "internalId": "pregnancy",
  "title": "Pregnancy Registration",
  "context": {
    "person": true,
    "place": false,
    "expression": "contact.type === 'person'"
  },
  "_attachments": {
    "xml": {
      "content_type": "application/xml",
      "data": "base64-xform-definition..."
    }
  }
}
```

## Users

### User Document (_users database)

```json
{
  "_id": "org.couchdb.user:username",
  "type": "user",
  "name": "username",
  "roles": ["chw", "data_entry"],
  "password_scheme": "pbkdf2",
  "iterations": 10,
  "derived_key": "...",
  "salt": "..."
}
```

### User Settings Document (medic database)

```json
{
  "_id": "org.couchdb.user:username",
  "type": "user-settings",
  "name": "username",
  "roles": ["chw", "data_entry"],
  "contact_id": "person-contact-uuid",
  "facility_id": "place-uuid",
  "known": true,
  "language": "en"
}
```

## Tasks

### Task Document

```json
{
  "_id": "task~org.couchdb.user:agatha~pregReport~pregnancy-visit~2~523435132468",
  "type": "task",
  "authoredOn": 523435132468,
  "user": "org.couchdb.user:agatha",
  "requester": "requester-contact-guid",
  "owner": "owner-contact-guid",
  "forId": "for-contact-guid",
  "state": "Ready",
  "emission": {
    "_id": "pregReport~pregnancy-visit~2",
    "forId": "for-contact-guid",
    "dueDate": "2024-01-15",
    "startDate": "2024-01-12",
    "endDate": "2024-01-22",
    "priority": "high",
    "priorityLabel": "task.priority.high"
  },
  "stateHistory": [
    {
      "state": "Draft",
      "timestamp": 523435132400
    },
    {
      "state": "Ready",
      "timestamp": 523435132468
    }
  ]
}
```

### Task States

| State | Description |
|-------|-------------|
| Draft | Calculated but scheduled in future |
| Ready | Currently showing to user |
| Cancelled | Not emitted on refresh or invalid emission |
| Completed | Emitted with `resolved: true` |
| Failed | Never terminated and endDate passed |

### Requester vs Owner

- **requester**: Contact whose data triggered task generation
- **owner**: Contact whose profile shows the task
- **forId**: Contact passed to form when task action opens

Example: Delivery form for woman1 generates task for child1.
- requester = woman1 (delivery report triggered it)
- owner = child1 (task shows on child's profile)

## Targets

### Target Document

```json
{
  "_id": "target~2024-01~user-contact-guid~org.couchdb.user:agatha",
  "type": "target",
  "user": "org.couchdb.user:agatha",
  "owner": "user-contact-guid",
  "updated_date": 523435132468,
  "reporting_period": "2024-01",
  "targets": [
    {
      "id": "births-this-month",
      "type": "count",
      "goal": 10,
      "value": {
        "pass": 5,
        "total": 5
      }
    },
    {
      "id": "deliveries-with-visit",
      "type": "percent",
      "goal": 100,
      "value": {
        "pass": 8,
        "total": 10
      }
    }
  ]
}
```

### Target Update Frequency

- Updated when user loads app or views targets tab
- Maximum once per day
- One document per reporting period
