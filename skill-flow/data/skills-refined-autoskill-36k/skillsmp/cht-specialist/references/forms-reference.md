# Forms Reference

Complete reference for CHT XLSForm and app form configuration.

## Overview

App forms are care guides used within the CHT web/mobile app. When submitted, they create `data_record` documents (Reports).

**Form Files:**
- `form_name.xlsx` - XLSForm definition (recommended)
- `form_name.xml` - XForm definition (generated or manual)
- `form_name.properties.json` - Meta information
- `form_name-media/` - Media files directory

## XLSForm Structure

### survey Sheet

| type | name | label | relevant | appearance | calculate |
|------|------|-------|----------|------------|-----------|
| begin group | inputs | Inputs | ./source = 'user' | field-list | |
| hidden | source | | | | |
| hidden | source_id | | | | |
| hidden | task_id | Task ID | | | |
| begin group | contact | | | | |
| string | _id | Patient ID | | select-contact type-person | |
| string | patient_id | Medic ID | | hidden | |
| string | name | Patient Name | | hidden | |
| end group | | | | | |
| end group | | | | | |
| calculate | _id | | | | ../inputs/contact/_id |
| calculate | patient_id | | | | ../inputs/contact/patient_id |
| calculate | name | | | | ../inputs/contact/name |
| ... | | | | | |
| begin group | group_summary | Summary | | field-list summary | |
| note | r_patient_info | **${patient_name}** ID: ${patient_id} | | | |
| note | r_followup | Follow Up | | | |
| end group | | | | | |

### settings Sheet

| form_title | form_id | version | namespaces |
|------------|---------|---------|------------|
| Pregnancy Registration | pregnancy | 2024-01 | cht=https://communityhealthtoolkit.org |

### choices Sheet

| list_name | name | label |
|-----------|------|-------|
| yes_no | yes | Yes |
| yes_no | no | No |

## Properties File Schema

```json
{
  "title": [
    { "locale": "en", "content": "Form Title" },
    { "locale": "fr", "content": "Titre du Formulaire" }
  ],
  "icon": "icon-name",
  "subject_key": "translation.key.for.report.title",
  "hidden_fields": ["internal_field", "private_field"],
  "context": {
    "person": true,
    "place": false,
    "expression": "contact.type === 'person' && ageInYears(contact) >= 18",
    "permission": "can_submit_form"
  }
}
```

| Property | Description | Required |
|----------|-------------|----------|
| `title` | Localized form title array | Yes |
| `icon` | Icon key from resources.json | Yes |
| `subject_key` | Custom report list title translation | No |
| `hidden_fields` | Fields to hide in report view | No |
| `context.person` | Show on person profiles | No |
| `context.place` | Show on place profiles | No |
| `context.expression` | JavaScript expression for visibility | No |
| `context.permission` | Required permission key | No |

### Expression Functions

Available in `context.expression`:

| Function | Description |
|----------|-------------|
| `ageInYears(contact)` | Contact's age in years |
| `ageInMonths(contact)` | Contact's age in months |
| `ageInDays(contact)` | Contact's age in days |

**Variables available:** `contact`, `summary`, `user`, `userSummary` (4.21.0+)

## CHT XPath Functions

| Function | Description | Version |
|----------|-------------|---------|
| `add-date(date, years, months, days, hours, minutes)` | Add time to date | 4.0.0+ |
| `cht:difference-in-days(date1, date2)` | Whole days between dates | 4.7.0+ |
| `cht:difference-in-weeks(date1, date2)` | Whole weeks between dates | 4.7.0+ |
| `cht:difference-in-months(date1, date2)` | Whole months between dates | All |
| `cht:difference-in-years(date1, date2)` | Whole years between dates | 4.7.0+ |
| `cht:extension-lib(name, ...params)` | Call extension library | 4.2.0+ |
| `cht:strip-whitespace(string)` | Remove whitespace | 4.10.0+ |
| `cht:validate-luhn(number, length)` | Luhn algorithm validation | 4.10.0+ |
| `parse-timestamp-to-date(timestamp)` | Parse timestamp to date | 3.13.0+ |
| `to-bikram-sambat(date)` | Convert to Bikram Sambat | 3.14.0+ |
| `z-score(table, sex, age, measurement)` | Calculate z-score | All |

## CHT XForm Widgets

### Contact Selector

```
| type | appearance |
|------|------------|
| string | select-contact type-person |
```

### Countdown Timer

```
| type | appearance | instance::cht:duration |
|------|------------|------------------------|
| trigger | countdown-timer | 30 |
```

### Phone Number with Validation

```
| type | appearance | instance::cht:unique_tel | constraint |
|------|------------|--------------------------|------------|
| string | numbers tel | true | true |
```

### Bikram Sambat Datepicker

Used by default for appropriate languages. No special configuration needed.

### Android App Launcher

```
| type | name | appearance |
|------|------|------------|
| begin group | camera-app | android-app-launcher |
| text | action | |
| begin group | inputs | android-app-inputs |
| text | param1 | |
| end group | | |
| begin group | outputs | android-app-outputs |
| text | result | |
| end group | | |
| end group | | |
```

## Supported Meta Fields

| Element | Description |
|---------|-------------|
| `start` | Timestamp when form entry started |
| `end` | Timestamp when form was submitted |
| `today` | Day form entry started |

## Binary Attachments

To include binary data (images):

```
| type | name | instance::type |
|------|------|----------------|
| image | photo | binary |
```

## Contact Association

Reports are associated with contacts via top-level fields:
- `patient_id` or `fields.patient_id`
- `patient_uuid` or `fields.patient_uuid`
- `place_id` or `fields.place_id`

## Build Commands

```bash
# Convert XLSForm to XForm
cht --local convert-app-forms

# Upload app forms
cht --local upload-app-forms

# Combined
cht --local convert-app-forms upload-app-forms
```
