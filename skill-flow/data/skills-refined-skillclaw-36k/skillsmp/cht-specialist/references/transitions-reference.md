# Sentinel Transitions Reference

Transitions are JavaScript functions executed by Sentinel when database documents change. They run in series (one at a time) and are repeatable.

## How Transitions Work

- `filter({ id, doc, info })` - Returns `true` if transition should run
- `onMatch({ id, doc, info })` - Executes when filter passes, returns `true` on success
- `init()` - Optional setup function, throws on invalid config
- Document is saved once after all transitions complete
- Check `transitions` property on infodoc to see if transition has run

## Configuration

Enable transitions in `app_settings.json`:

```json
{
  "transitions": {
    "registration": true,
    "muting": { "client_side": false },
    "death_reporting": { "disable": false }
  }
}
```

Use `"client_side": false` to disable client-side execution (3.12.0+).

## Available Transitions (in execution order)

| Transition | Description |
|------------|-------------|
| `maintain_info_document` | Records metadata about document replication. Enabled by default. |
| `update_clinics` | Attributes incoming SMS/report to appropriate contact using `rc_code` or phone number |
| `registration` | Registers patient/place to schedule, creates patient doc if needed |
| `accept_patient_reports` | Validates patient/place reports, silences reminders |
| `accept_case_reports` | Validates case reports, assigns place_uuid (3.9.0+) |
| `generate_shortcode_on_contacts` | Auto-generates `patient_id` and `place_id` (3.8.0+) |
| `default_responses` | Responds with confirmation or validation error |
| `update_sent_by` | Sets `sent_by` field from sender's phone |
| `death_reporting` | Updates patient's deceased status |
| `conditional_alerts` | Sends alert if configured condition met |
| `multi_report_alerts` | Flexible alerts across form types |
| `muting` | Mutes/unmutes people and places (3.2.0+, client-side 3.12.0+) |
| `mark_for_outbound` | Enables outbound pushes (3.5.0+) |
| `self_report` | Maps patient to sender (3.9.0+) |
| `create_user_for_contacts` | Auto-creates users from contact data (4.1.0+) |

## registration

Registers patients/places to schedules. Configuration in `app_settings.registrations`.

### Events

Only `on_create` is supported.

### Triggers

#### add_patient
Creates person doc and sets `patient_id`.

```json
{
  "name": "on_create",
  "trigger": "add_patient",
  "params": "{\"patient_id_field\": \"external_id\", \"contact_type\": \"patient\", \"parent_id\": \"parent_id\"}",
  "bool_expr": ""
}
```

| Param | Description |
|-------|-------------|
| `patient_id_field` | Field containing external ID (not `patient_id`) |
| `patient_name_field` | Alternative name field location |
| `contact_type` | Contact type for configurable hierarchies |
| `parent_id` | Field with parent's `place_id` (3.8.0+) |

**Events:** `parent_field_not_provided`, `parent_invalid`, `parent_not_found`

#### add_place (3.8.0+)
Creates place doc and sets `place_id`.

```json
{
  "params": "{ \"contact_type\": \"clinic\", \"parent_id\": \"parent_id\", \"place_name_field\": \"clinic_name\" }"
}
```

#### add_case (3.9.0+)
Sets `case_id` on registration document.

#### assign_schedule
Assigns SMS schedule to contact.

#### clear_schedule
Clears SMS schedule.

## death_reporting

Updates patient `date_of_death` field.

```json
"death_reporting": {
  "mark_deceased_forms": ["death"],
  "undo_deceased_forms": ["undo-death"],
  "date_field": "fields.death_date"
}
```

| Property | Description |
|----------|-------------|
| `mark_deceased_forms` | Forms that mark patient deceased |
| `undo_deceased_forms` | Forms that remove deceased status |
| `date_field` | Path to death date (default: `reported_date`) |

## muting

Mutes/unmutes persons and places. Sets `muted` property with ISO date.

### Configuration

```json
"muting": {
  "mute_forms": ["mute_person", "mute_clinic"],
  "unmute_forms": ["unmute_person", "unmute_clinic"],
  "validations": {
    "join_responses": true,
    "list": []
  },
  "messages": [
    { "translation_key": "", "event_type": "mute", "recipient": "reporting_unit" },
    { "translation_key": "", "event_type": "unmute", "recipient": "reporting_unit" },
    { "translation_key": "", "event_type": "already_muted", "recipient": "reporting_unit" },
    { "translation_key": "", "event_type": "already_unmuted", "recipient": "reporting_unit" },
    { "translation_key": "", "event_type": "contact_not_found", "recipient": "reporting_unit" }
  ]
}
```

### Muting Action
- Sets `muted` property on target and all descendants
- Updates `muting_history` in Sentinel info docs
- Changes unsent `scheduled_tasks` state to `muted`

### Unmuting Action
- Unmutes topmost muted ancestor and all descendants
- Changes future `muted` scheduled_tasks to `scheduled`
- Past scheduled_tasks remain unchanged

### Client-Side (3.12.0+)
- Runs offline on user's device
- Updates `muting_history` property on contact docs
- Sets `last_update` to `client_side`

### Server-Side
- Replays following muting events after processing
- Updates `last_update` to `server_side`

## multi_report_alerts

Send alerts when specific conditions across multiple reports are met.

```json
"multi_report_alerts": [{
  "name": "suspected_cholera",
  "is_report_counted": "function(report, latest_report) { return latest_report.contact.parent.parent._id === report.contact.parent.parent._id; }",
  "num_reports_threshold": 2,
  "message": "{{num_counted_reports}} patients with {{alert_name}} in {{time_window_in_days}} days",
  "recipients": ["+123456", "new_report.contact.phone"],
  "time_window_in_days": 7,
  "forms": ["C", "D"]
}]
```

| Property | Description |
|----------|-------------|
| `name` | Alert identifier |
| `is_report_counted` | Function to filter reports |
| `num_reports_threshold` | Minimum reports to trigger (max 100) |
| `time_window_in_days` | Time window for counting |
| `forms` | Form codes to monitor |
| `message` | Alert message (Mustache template) |
| `recipients` | Phone numbers or field paths |

## accept_patient_reports

Validates patient/place reports and manages schedules.

```json
"patient_reports": [{
  "form": "pregnancy_visit",
  "silence_type": "ANC Reminders",
  "silence_for": "8 days",
  "validations": {},
  "messages": [{
    "translation_key": "messages.pregnancy_visit",
    "event_type": "report_accepted",
    "recipient": "clinic"
  }]
}]
```

## self_report (3.9.0+)

Maps patient to sender for self-reporting workflows.

```json
"self_report": [{
  "form": "FORM",
  "messages": [
    { "event_type": "report_accepted", "recipient": "reporting_unit", "translation_key": "messages.accepted" },
    { "event_type": "sender_not_found", "recipient": "reporting_unit", "translation_key": "messages.not_found" }
  ]
}]
```

## create_user_for_contacts (4.1.0+)

Auto-creates users for contacts.

### Requirements
- `token_login` must be enabled
- `app_url` must be set

```json
{
  "app_url": "https://demo.app.medicmobile.org",
  "token_login": {
    "enabled": true,
    "translation_key": "sms.token.login.help"
  },
  "transitions": {
    "create_user_for_contacts": true
  }
}
```

### Contact Form Requirements
Include `user_for_contact.create` field set to `'true'`.

Required contact fields: `name`, `phone`, `roles` (or `role`).

### Replace User (4.1.0+)
Replace existing offline user on device.

```json
"create_user_for_contacts": {
  "replace_forms": ["replace_user"]
}
```

Form must set `replacement_contact_id` to new contact's ID.

## update_clinics

Attributes SMS/reports to contacts.

```json
"update_clinics": [{
  "form": "FORM",
  "messages": [{
    "event_type": "sys.facility_not_found",
    "recipient": "reporting_unit",
    "translation_key": "sys.facility_not_found"
  }]
}]
```

## Troubleshooting

### Resetting Sentinel Sequence

If backlog is too large:

1. Get current sequence: `curl -qs https://medic:pass@url/medic/ | jq ".update_seq"`
2. Stop Sentinel container
3. In Fauxton, edit `medic-sentinel/_local/transitions-seq` value field
4. Restart Sentinel

This skips processing the backlog.

## Version Compatibility

| Feature | Version |
|---------|---------|
| `create_user_for_contacts` | 4.1.0+ |
| `accept_case_reports` | 3.9.0+ |
| `self_report` | 3.9.0+ |
| `add_place` trigger | 3.8.0+ |
| `generate_shortcode_on_contacts` | 3.8.0+ |
| `mark_for_outbound` | 3.5.0+ |
| `muting` | 3.2.0+ |
| Client-side transitions | 3.12.0+ |
