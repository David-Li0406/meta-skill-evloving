# CHT-Specific Extensions

Additional features available when using Community Health Toolkit (CHT).

## Overview

CHT extends ODK XForm with:
- Custom XPath functions
- Specialized widgets
- Contact integration
- Form properties file
- Task/target integration

---

## CHT XPath Functions

### Date Functions

| Function | Description | Version |
|----------|-------------|---------|
| `add-date(date, y, m, d, h, min)` | Add time to date | 4.0.0+ |
| `cht:difference-in-days(d1, d2)` | Whole days between | 4.7.0+ |
| `cht:difference-in-weeks(d1, d2)` | Whole weeks between | 4.7.0+ |
| `cht:difference-in-months(d1, d2)` | Whole months between | All |
| `cht:difference-in-years(d1, d2)` | Whole years between | 4.7.0+ |

### Examples

```
add-date(${lmp_date}, 0, 9, 0, 0, 0)           # EDD calculation
cht:difference-in-days(today(), ${birth_date})  # Days since birth
cht:difference-in-months(${start}, ${end})      # Months between dates
```

### Utility Functions

| Function | Description | Version |
|----------|-------------|---------|
| `cht:extension-lib(name, params)` | Call extension library | 4.2.0+ |
| `cht:strip-whitespace(str)` | Remove whitespace | 4.10.0+ |
| `cht:validate-luhn(num, len)` | Luhn algorithm validation | 4.10.0+ |
| `parse-timestamp-to-date(ts)` | Parse timestamp | 3.13.0+ |
| `to-bikram-sambat(date)` | Convert to Bikram Sambat | 3.14.0+ |
| `z-score(table, sex, age, val)` | Calculate z-score | All |

### Z-Score Example

```
z-score('weight-for-age', ${sex}, ${age_days}, ${weight})
```

Tables available: `weight-for-age`, `height-for-age`, `weight-for-height`

---

## CHT Widgets

### Contact Selector

Select contacts from CHT hierarchy:

| type | name | label | appearance |
|------|------|-------|------------|
| string | patient | Select Patient | select-contact type-person |
| string | facility | Select Facility | select-contact type-health_center |

### Contact Types

- `type-person`
- `type-clinic`
- `type-health_center`
- `type-district_hospital`
- Custom contact types

### Countdown Timer

| type | name | label | appearance | instance::cht:duration |
|------|------|-------|------------|------------------------|
| trigger | timer | Count respirations | countdown-timer | 60 |

### Phone Validation

| type | name | label | appearance | instance::cht:unique_tel |
|------|------|-------|------------|--------------------------|
| string | phone | Phone Number | numbers tel | true |

- `numbers tel`: Phone keyboard
- `cht:unique_tel`: Validate uniqueness in system

---

## Form Properties File

Create `form_name.properties.json` alongside XLSForm:

```json
{
  "title": [
    { "locale": "en", "content": "Patient Registration" },
    { "locale": "fr", "content": "Enregistrement Patient" }
  ],
  "icon": "icon-person",
  "subject_key": "contact.name",
  "hidden_fields": ["internal_calc", "meta_field"],
  "context": {
    "person": true,
    "place": false,
    "expression": "contact.type === 'person' && ageInYears(contact) >= 18",
    "permission": "can_register_patients"
  }
}
```

### Properties

| Property | Description |
|----------|-------------|
| `title` | Localized form titles |
| `icon` | Icon from resources.json |
| `subject_key` | Translation key for report list title |
| `hidden_fields` | Fields to hide in report view |
| `context` | When form appears |

### Context Options

| Option | Description |
|--------|-------------|
| `person` | Show on person profiles |
| `place` | Show on place profiles |
| `expression` | JavaScript condition |
| `permission` | Required permission key |

### Expression Functions

Available in `context.expression`:

| Function | Description |
|----------|-------------|
| `ageInYears(contact)` | Contact's age in years |
| `ageInMonths(contact)` | Contact's age in months |
| `ageInDays(contact)` | Contact's age in days |

### Variables in Expression

- `contact` - Current contact
- `summary` - Contact summary context
- `user` - Current user
- `userSummary` - User's contact summary (4.21.0+)

---

## Contact Summary Access

Access contact summary data in forms:

```
instance('contact-summary')/context/pregnant
instance('contact-summary')/context/risk_level
```

User's contact summary (4.21.0+):

```
instance('user-contact-summary')/context/facility_name
```

---

## Standard Form Structure

CHT forms typically include an inputs group:

| type | name | label | relevant | appearance |
|------|------|-------|----------|------------|
| begin group | inputs | Inputs | ./source = 'user' | field-list |
| hidden | source | | | |
| hidden | source_id | | | |
| begin group | contact | | | |
| string | _id | Patient ID | | select-contact type-person |
| string | patient_id | Medic ID | | hidden |
| string | name | Patient Name | | hidden |
| end group | | | | |
| end group | | | | |
| calculate | _id | | | ../inputs/contact/_id |
| calculate | patient_id | | | ../inputs/contact/patient_id |
| calculate | name | | | ../inputs/contact/name |

---

## Summary Group

End forms with summary for review:

| type | name | label | appearance |
|------|------|-------|------------|
| begin group | group_summary | Summary | field-list summary |
| note | r_patient | **${name}** | |
| note | r_info | Age: ${age} years | |
| note | r_date | Visit: ${visit_date} | |
| end group | | | |

---

## Build Commands

### Convert and Upload

```bash
# All app forms
cht --local convert-app-forms upload-app-forms

# Specific forms
cht --local convert-app-forms upload-app-forms -- pregnancy assessment

# Contact forms
cht --local convert-contact-forms upload-contact-forms
```

### Connection Options

```bash
# Local development
cht --url=https://medic:password@localhost --accept-self-signed-certs

# Remote instance
cht --url=https://user:pass@instance.app.medicmobile.org
```

---

## CHT-Specific Considerations

### Performance

- Forms load contact data
- Minimize contact-summary calculations
- Test on low-end devices

### Offline Support

- All data available offline
- Forms work without connectivity
- Sync when connected

### Report Association

Forms create reports linked to contacts via:
- `patient_id` or `fields.patient_id`
- `patient_uuid` or `fields.patient_uuid`
- `place_id` or `fields.place_id`
