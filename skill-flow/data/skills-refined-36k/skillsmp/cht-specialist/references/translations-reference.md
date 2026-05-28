# CHT Translations Reference

Guide for localizing CHT applications to custom languages.

## File Structure

```
translations/
  messages-en.properties    # English (default)
  messages-fr.properties    # French
  messages-sw.properties    # Swahili
  messages-{code}.properties
```

## Upload Translations

```bash
# Upload custom translations
cht --local upload-custom-translations

# Or with explicit URL
cht --url=https://medic:password@localhost upload-custom-translations
```

## Translation Key Format

Properties file format:
```properties
# Tab names
Messages = Messages
Tasks = Tasks
Reports = Reports
People = Contacts
Targets = Analytics

# Task titles
task.anc.delivery.title = Delivery Task

# Target titles
targets.growth_monitoring.title = Growth Monitoring

# Contact types
contact.type.person = Person
contact.type.person.plural = People
contact.type.date_of_birth = Date of Birth

# Form fields
patient.name = Patient Name
```

## Configuring Languages

### Add Language to app_settings.json

```json
"locales": [
  { "code": "en", "name": "English" },
  { "code": "fr", "name": "French" },
  { "code": "sw", "name": "Swahili" }
]
```

### Set Default Language

In App Management: Display > Languages > Default Language

### RTL Support (4.18.0+)

Right-to-left languages (Arabic, Hebrew) supported. Configure via:
App Management > Display > Languages > Add/Edit language

## Form Translations

### XLSForm Labels

Add `label::{code}` columns in survey and choices sheets:

| type | name | label::en | label::fr | label::sw |
|------|------|-----------|-----------|-----------|
| text | name | Name | Nom | Jina |
| select_one sex | sex | Sex | Sexe | Jinsia |

### Hints and Constraints

| Column | Localized Version |
|--------|-------------------|
| `hint` | `hint::{code}` |
| `constraint_message` | `constraint_message::{code}` |
| `required_message` | `required_message::{code}` |

## Outgoing SMS Translations

### Message Configuration

```json
{
  "messages": [{
    "message": [
      {
        "content": "Thank you, visit for {{patient_name}} has been recorded.",
        "locale": "en"
      },
      {
        "content": "Asante, kuhudhuria kwa {{patient_name}} kumerekodiwa.",
        "locale": "sw"
      }
    ],
    "event_type": "report_accepted",
    "recipient": "reporting_unit"
  }]
}
```

### Translation Keys in Messages

```json
{
  "messages": [{
    "translation_key": "messages.visit.accepted",
    "event_type": "report_accepted",
    "recipient": "reporting_unit"
  }]
}
```

Then in `messages-sw.properties`:
```properties
messages.visit.accepted = Asante, kuhudhuria kumerekodiwa.
```

## Common Translation Keys

### Navigation
```properties
Messages = Messages
Tasks = Tasks
Reports = Reports
People = Contacts
Targets = Analytics
```

### Contact Types
```properties
contact.type.district_hospital = District Hospital
contact.type.health_center = Health Center
contact.type.clinic = Clinic
contact.type.person = Person
contact.type.{type} = Type Name
contact.type.{type}.plural = Type Name (Plural)
```

### Task States
```properties
task.overdue = Overdue
task.due = Due today
task.upcoming = Upcoming
```

### Target Labels
```properties
targets.{id}.title = Target Title
targets.{id}.subtitle = Target Subtitle
targets.this_month.subtitle = This month
targets.all_time.subtitle = All time
```

### Form Fields
```properties
patient.name = Patient Name
patient.sex = Sex
patient.dob = Date of Birth
```

## User Language Preference

Users can select language:
- First login popup
- App Settings > User Settings > Language

User's locale determines:
- UI text
- Outgoing SMS language
- Form display language

## Best Practices

1. **Use translation keys** in tasks.js, targets.js, forms
2. **Keep keys consistent** across all language files
3. **Test with actual users** who speak the language
4. **Consider SMS length** for translated messages
5. **Contribute core translations** to CHT community

## Contributing Translations

New language translations for CHT core can be contributed via:
- [CHT Contributing Guide](/community/contributing/translations)
- Transifex platform

## Version Notes

| Feature | Version |
|---------|---------|
| RTL Support | 4.18.0+ |
| Multiple SMS locales | All versions |
| XLSForm multilingual | All versions |
