# CHT Messaging Reference

SMS messaging for care coordination, alerts, and notifications.

## Architecture

CHT uses SMS gateways to send/receive messages:
- **CHT Gateway** - Android app for sending via phone
- **RapidPro** - Cloud-based messaging platform
- **Africa's Talking** - SMS aggregator

## SMS Message States

| State | Description |
|-------|-------------|
| `scheduled` | Not yet due. Part of configured schedule, changes to `pending` when due. |
| `pending` | Due to be sent. Gateway will pick up for sending. |
| `forwarded-to-gateway` | Sent to gateway. |
| `received-by-gateway` | Received by gateway. |
| `forwarded-by-gateway` | Gateway attempted sending. |
| `sent` | Delivered to SMS network. |
| `delivered` | Received by recipient's device. |
| `failed` | Sending failed. No automatic retry. |
| `denied` | Blocked by `outgoing_deny_list` or similar config. |
| `cleared` | Stopped by event (e.g., visit occurred before reminder). |
| `muted` | Deliberately stopped. Can be unmuted. |

## Message Timeline

1. Due date passes → `pending`
2. Gateway polls → `forwarded-to-gateway`
3. Gateway saves → received
4. Gateway sends → `forwarded-by-gateway`
5. Network confirms → `sent`
6. Device confirms → `delivered`

## CHT Gateway Configuration

### Install
1. Download CHT Gateway APK from releases
2. Install on Android phone (requires SMS permissions)
3. Configure server URL and credentials

### app_settings.json

```json
{
  "gateway": {
    "enabled": true
  },
  "sms": {
    "outgoing_service": "medic-gateway"
  }
}
```

## RapidPro Integration

### Configuration

```json
{
  "sms": {
    "outgoing_service": "rapidpro"
  },
  "rapidpro": {
    "url": "https://rapidpro.io",
    "token": "YOUR_API_TOKEN"
  }
}
```

### Webhook Endpoint
```
POST /api/v1/sms/rapidpro/incoming
```

## Africa's Talking

### Configuration

```json
{
  "sms": {
    "outgoing_service": "africas-talking"
  },
  "africas_talking": {
    "username": "YOUR_USERNAME",
    "api_key": "YOUR_API_KEY"
  }
}
```

### Webhook Endpoint
```
POST /api/v1/sms/africas-talking/incoming
```

## SMS Schedules

### Schedule Configuration

```json
{
  "schedules": [{
    "name": "ANC Reminders",
    "summary": "ANC visit reminders",
    "description": "Reminders for antenatal care visits",
    "start_from": "lmp_date",
    "messages": [
      {
        "group": 1,
        "offset": "4 weeks",
        "send_day": "monday",
        "send_time": "09:00",
        "message": [{
          "content": "Please visit the clinic for your ANC checkup.",
          "locale": "en"
        }],
        "recipient": "reporting_unit"
      }
    ]
  }]
}
```

### Schedule Properties

| Property | Description |
|----------|-------------|
| `name` | Unique schedule identifier |
| `start_from` | Field to calculate dates from |
| `messages` | Array of scheduled messages |
| `messages[].group` | Message group number |
| `messages[].offset` | Time offset from start_from |
| `messages[].send_day` | Day of week to send |
| `messages[].send_time` | Time of day to send |
| `messages[].recipient` | Message recipient |

### Assigning Schedules

In registrations config:
```json
{
  "events": [{
    "name": "on_create",
    "trigger": "assign_schedule",
    "params": "ANC Reminders",
    "bool_expr": ""
  }]
}
```

## SMS Forms

### JSON Form Definition

```json
{
  "forms": {
    "V": {
      "meta": {
        "code": "V",
        "label": "Visit"
      },
      "fields": {
        "patient_id": {
          "type": "string",
          "labels": { "short": "Patient ID" }
        }
      }
    }
  }
}
```

### Form Submission via SMS

```
V 12345
```

## Message Replies

### Automatic Replies

```json
{
  "registrations": [{
    "form": "P",
    "messages": [{
      "message": [{
        "content": "Patient {{patient_name}} registered successfully.",
        "locale": "en"
      }],
      "event_type": "report_accepted",
      "recipient": "reporting_unit"
    }]
  }]
}
```

### Event Types

| Event | Trigger |
|-------|---------|
| `report_accepted` | Valid report submitted |
| `registration_not_found` | Patient not found |
| `sys.facility_not_found` | Sender facility not found |
| `sys.empty` | Empty message received |

## Denylists

### Outgoing Deny List

```json
{
  "outgoing_deny_list": ["+1234567890", "+0987654321"]
}
```

### Deny Settings

| Setting | Description |
|---------|-------------|
| `outgoing_deny_list` | Array of blocked phone numbers |
| `outgoing_deny_with_alphas` | Block numbers with letters |
| `outgoing_deny_shorter_than` | Min phone number length |

## Message Loops Prevention

CHT detects and prevents message loops when:
- Same message repeatedly received
- Circular routing detected
- Excessive messages in short period

## Shortcodes

### Patient ID Shortcode

```json
{
  "generate_patient_id_on_people": true
}
```

Generates unique `patient_id` for SMS identification.

### Place ID Shortcode

```json
{
  "generate_shortcode_on_contacts": true
}
```

Generates `place_id` for place identification.

## Recipient Options

| Recipient | Description |
|-----------|-------------|
| `reporting_unit` | Person who submitted report |
| `clinic` | Facility contact |
| `parent` | Parent facility contact |
| `grandparent` | Grandparent facility contact |
| `{contact_type}` | Specific contact type |
| `+1234567890` | Direct phone number |

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Messages stuck in `pending` | Check gateway connection |
| Messages in `failed` | Check phone number format |
| Messages in `denied` | Check deny lists |
| No SMS received | Check incoming webhook config |

### Debug

1. Check Sentinel logs for message processing
2. Verify gateway status in admin
3. Test with direct API call
4. Check message state in database

## Version Notes

| Feature | Version |
|---------|---------|
| RapidPro integration | All |
| Africa's Talking | All |
| CHT Gateway | All |
| generate_shortcode_on_contacts | 3.8.0+ |
