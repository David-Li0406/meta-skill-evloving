# Multi-Language Support

Create forms with multiple language translations.

## Translation Columns

Add language-specific columns using `::Language Name (code)` suffix.

### Survey Sheet

| type | name | label::English (en) | label::French (fr) | label::Swahili (sw) |
|------|------|---------------------|--------------------|--------------------|
| text | name | Name | Nom | Jina |
| integer | age | Age | Âge | Umri |
| select_one yes_no | consent | Do you agree? | Acceptez-vous? | Unakubali? |

### Choices Sheet

| list_name | name | label::English (en) | label::French (fr) | label::Swahili (sw) |
|-----------|------|---------------------|--------------------|--------------------|
| yes_no | yes | Yes | Oui | Ndiyo |
| yes_no | no | No | Non | Hapana |

---

## Translatable Columns

| Column | Description |
|--------|-------------|
| `label` | Question text |
| `hint` | Helper text |
| `constraint_message` | Validation error |
| `required_message` | Required field error |
| `guidance_hint` | Additional guidance |
| `image` | Image filename |
| `audio` | Audio filename |
| `video` | Video filename |

### Example with Hints

| type | name | label::English (en) | label::French (fr) | hint::English (en) | hint::French (fr) |
|------|------|---------------------|--------------------|--------------------|-------------------|
| text | phone | Phone Number | Numéro de téléphone | Enter with country code | Entrez avec indicatif |

---

## Language Codes

Use ISO 639-1 two-letter codes:

| Code | Language |
|------|----------|
| `en` | English |
| `fr` | French |
| `es` | Spanish |
| `sw` | Swahili |
| `ar` | Arabic |
| `pt` | Portuguese |
| `am` | Amharic |
| `hi` | Hindi |
| `zh` | Chinese |

---

## Default Language

Set in settings sheet:

| form_title | form_id | default_language |
|------------|---------|------------------|
| Patient Survey | survey | English (en) |

Or:

| form_title | form_id | default_language |
|------------|---------|------------------|
| Enquête Patient | survey | French (fr) |

---

## Mixed Default and Translated

If you have a non-translated `label` column alongside translated columns, it becomes a separate "Default" language option.

### Recommended Approach

Always use language-specific columns for all content:

| type | name | label::English (en) | label::French (fr) |
|------|------|---------------------|-------------------|

### Not Recommended

| type | name | label | label::French (fr) |
|------|------|-------|-------------------|

This creates confusing "Default" language option.

---

## Translated Media

Use same filename across languages (if identical) or different filenames:

### Same Media

| type | name | label::English (en) | label::French (fr) | image |
|------|------|---------------------|--------------------|-------|
| note | instructions | Instructions | Instructions | steps.png |

### Different Media per Language

| type | name | label::English (en) | label::French (fr) | image::English (en) | image::French (fr) |
|------|------|---------------------|--------------------|---------------------|-------------------|
| note | welcome | Welcome | Bienvenue | welcome_en.png | welcome_fr.png |

---

## Switching Languages

Users change language in ODK Collect:
- Menu → Change Language
- App remembers last selection per form

---

## Right-to-Left Languages

Arabic, Hebrew, and other RTL languages are automatically handled.

| type | name | label::English (en) | label::Arabic (ar) |
|------|------|---------------------|-------------------|
| text | name | Name | الاسم |
| integer | age | Age | العمر |

---

## Best Practices

### Translation Quality

- Use professional translators
- Review medical/technical terms carefully
- Test with native speakers

### Consistency

- Use consistent terminology throughout
- Create glossary for translators
- Keep choice labels consistent

### Completeness

- Translate ALL user-facing text
- Include error messages
- Don't forget hints and guidance

### Testing

- Test each language fully
- Check for text overflow
- Verify RTL rendering

### File Organization

Consider maintaining separate translation files and merging them during build.

---

## Example: Complete Multi-Language Form

### Survey Sheet

| type | name | label::English (en) | label::French (fr) | hint::English (en) | hint::French (fr) | required |
|------|------|---------------------|--------------------|--------------------|-------------------|----------|
| text | first_name | First Name | Prénom | Given name | Prénom | yes |
| text | last_name | Last Name | Nom de famille | Family name | Nom de famille | yes |
| integer | age | Age | Âge | Years | Années | yes |
| select_one gender | sex | Gender | Sexe | | | yes |
| date | dob | Date of Birth | Date de naissance | | | |

### Choices Sheet

| list_name | name | label::English (en) | label::French (fr) |
|-----------|------|---------------------|-------------------|
| gender | male | Male | Masculin |
| gender | female | Female | Féminin |
| gender | other | Other | Autre |

### Settings Sheet

| form_title::English (en) | form_title::French (fr) | form_id | default_language |
|--------------------------|-------------------------|---------|------------------|
| Patient Registration | Enregistrement Patient | patient_reg | English (en) |
