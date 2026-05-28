# App Settings Reference

Reference for CHT app_settings.json configuration.

## Overview

App settings control CHT application behavior. They're defined in `app_settings.json` and stored in the `settings` document in CouchDB.

**Configuration Structure:**
```
app_settings/
  base_settings.json      # Core settings
  forms.json              # Form definitions
  schedules.json          # SMS schedules
```

## Optional Settings

| Setting | Description | Default | Version |
|---------|-------------|---------|---------|
| `phone_validation` | `"full"`, `"partial"`, or `"none"` | `"full"` | 3.1.0 |
| `uhc.contacts_default_sort` | `"alpha"` or `"last_visited_date"` | `"alpha"` | 2.18.0 |
| `uhc.visit_count.month_start_date` | Day of month to reset visit count | 1 | 2.18.0 |
| `uhc.visit_count.visit_count_goal` | Monthly visit count goal | 0 | 2.18.0 |
| `outgoing_deny_list` | Comma-delimited phone prefixes to deny | "" | |
| `outgoing_deny_shorter_than` | Minimum phone number length | 6 | 3.3.0 |
| `outgoing_deny_with_alphas` | Deny phones with letters | true | 3.3.0 |
| `task_day_limit` | Days before task due to show date | 4 | 3.9.0 |
| `app_url` | Application URL | | 3.10.0 |
| `task_days_overdue` | Show overdue days in task list | false | 3.13.0 |
| `languages` | Array of `{locale, enabled}` objects | | 4.2.0 |
| `place_hierarchy_types` | Contact type IDs for Place Filter | | 2.15.0 |
| `assetlinks` | Digital Asset Links for Android | | 4.7.0 |
| `sms.clear_failing_schedules` | Clear failing scheduled messages | false | 5.1.0 |

## Contact Hierarchy Configuration

```json
{
  "contact_types": [
    {
      "id": "district_hospital",
      "name_key": "contact.type.district_hospital",
      "group_key": "contact.type.district_hospital.plural",
      "create_key": "contact.type.district_hospital.new",
      "edit_key": "contact.type.district_hospital.edit",
      "icon": "medic-district-hospital",
      "create_form": "form:contact:district_hospital:create",
      "edit_form": "form:contact:district_hospital:edit"
    },
    {
      "id": "health_center",
      "name_key": "contact.type.health_center",
      "parents": ["district_hospital"],
      "icon": "medic-health-center"
    },
    {
      "id": "clinic",
      "name_key": "contact.type.clinic",
      "parents": ["health_center"],
      "icon": "medic-clinic",
      "count_visits": true
    },
    {
      "id": "person",
      "name_key": "contact.type.person",
      "parents": ["clinic", "health_center"],
      "icon": "medic-person",
      "person": true
    }
  ]
}
```

## Permissions

```json
{
  "permissions": {
    "can_view_contacts": ["chw", "nurse", "manager"],
    "can_view_reports": ["chw", "nurse", "manager"],
    "can_view_tasks": ["chw"],
    "can_view_analytics": ["nurse", "manager"],
    "can_create_records": ["chw", "nurse"],
    "can_edit_contacts": ["nurse", "manager"],
    "can_delete_contacts": ["manager"],
    "can_configure": ["manager"],
    "can_export_all": ["manager"]
  }
}
```

## SMS Workflows

### Registrations

```json
{
  "registrations": [
    {
      "form": "P",
      "events": [
        {
          "name": "on_create",
          "trigger": "add_patient",
          "params": "",
          "bool_expr": ""
        }
      ],
      "validations": {
        "join_responses": false,
        "list": [
          {
            "property": "patient_name",
            "rule": "lenMin(3) && lenMax(50)",
            "translation_key": "validation.patient_name"
          }
        ]
      },
      "messages": [
        {
          "event_type": "report_accepted",
          "translation_key": "messages.registration.accepted",
          "recipient": "reporting_unit"
        }
      ]
    }
  ]
}
```

### Schedules

```json
{
  "schedules": [
    {
      "name": "ANC Reminders",
      "start_from": "lmp_date",
      "messages": [
        {
          "group": 1,
          "offset": "4 weeks",
          "send_day": "monday",
          "send_time": "09:00",
          "translation_key": "messages.schedule.anc.visit1",
          "recipient": "patient"
        },
        {
          "group": 2,
          "offset": "12 weeks",
          "send_day": "monday",
          "send_time": "09:00",
          "translation_key": "messages.schedule.anc.visit2",
          "recipient": "patient"
        }
      ]
    }
  ]
}
```

### Patient Reports

```json
{
  "patient_reports": [
    {
      "form": "V",
      "validations": {
        "join_responses": true,
        "list": [
          {
            "property": "patient_id",
            "rule": "regex('^[0-9]{5}$')",
            "translation_key": "validation.patient_id"
          }
        ]
      },
      "messages": [
        {
          "event_type": "report_accepted",
          "translation_key": "messages.visit.accepted",
          "recipient": "reporting_unit"
        },
        {
          "event_type": "registration_not_found",
          "translation_key": "messages.patient_not_found",
          "recipient": "reporting_unit"
        }
      ]
    }
  ]
}
```

## SMS Recipient Resolution

| Value | Resolves To |
|-------|-------------|
| (empty) | Submitter |
| `reporting_unit` | Submitter |
| `patient` | Patient contact |
| `parent` | Primary contact of subject's parent place |
| `grandparent` | Primary contact of grandparent place |
| `clinic` | Primary contact of clinic in lineage |
| `health_center` | Primary contact of health center |
| `district` | Primary contact of district hospital |
| `ancestor:<type>` | Primary contact of place with type |
| `link:<tag>` | Linked document with tag (3.10+) |
| Custom path | e.g., `patient.parent.contact.phone` |

## Validation Rules

| Function | Description |
|----------|-------------|
| `equals(value)` | Exact match |
| `iEquals(value)` | Case-insensitive match |
| `lenMin(n)` | Minimum length |
| `lenMax(n)` | Maximum length |
| `lenEquals(n)` | Exact length |
| `min(n)` | Minimum value |
| `max(n)` | Maximum value |
| `between(min, max)` | Value range |
| `in(v1, v2, ...)` | One of values |
| `required` | Must have value |
| `optional` | Always valid |
| `numeric` | Numbers only |
| `integer` | Integer only |
| `alpha` | Letters only |
| `alphaNumeric` | Letters and numbers |
| `email` | Email format |
| `regex("pattern")` | Custom regex |
| `unique(*fields)` | No duplicate |
| `uniquePhone(field)` | Phone not registered |
| `validPhone(field)` | Valid phone number |
| `exists(form, field)` | Report exists |
| `isISOWeek(week, year)` | Valid ISO week |
| `isAfter(duration)` | Date after duration |
| `isBefore(duration)` | Date before duration |

### Validation Example

```json
{
  "property": "patient_id",
  "rule": "regex('\\d{5}') && unique('patient_id')",
  "translation_key": "validation.patient_id_invalid"
}
```

## Message Variables

All report fields and message context are available:

```properties
# translations/messages-en.properties
messages.registration.accepted = Thank you {{contact.name}} for registering {{patient_name}}. ID: {{patient_id}}
```

### Date Filters

| Filter | Description |
|--------|-------------|
| `date` | Format per `date_format` setting |
| `datetime` | Format per `reported_date_format` |
| `bikram_sambat_date` | Bikram Sambat format |

## Build Command

```bash
cht --local compile-app-settings backup-app-settings upload-app-settings
```
