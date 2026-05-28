# Multilingual Forms Reference

Support multiple languages in a single form. Users select their preferred language when opening the form.

## Basic Syntax

Add language columns using `column::language` format.

### label Translations

```
| label | label::en | label::fr | label::sw |
| Quel est votre nom? | What is your name? | Quel est votre nom? | Jina lako nani? |
```

- `label` - Default/fallback language
- `label::en` - English
- `label::fr` - French
- `label::sw` - Swahili
- `label::es` - Spanish
- `label::ar` - Arabic
- Add one column per language

### hint Translations

```
| hint | hint::en | hint::fr | hint::sw |
| Veuillez... | Please... | Veuillez... | Tafadhali... |
```

---

## Survey Sheet Example

```
| type | name | label::en | label::fr | label::sw | hint::en | hint::fr | hint::sw |
| text | name | What is your name? | Quel est votre nom? | Jina lako nani? | Full name | Nom complet | Jina kamili |
| integer | age | Age | Âge | Umri | In years | En années | Kwa miaka |
| select_one gender | gender | Gender | Genre | Jinsia | | | |
```

---

## Choices Sheet Translation

Translate choice labels the same way:

```
| list_name | name | label::en | label::fr | label::sw |
| gender | m | Male | Homme | Mwanamume |
| gender | f | Female | Femme | Mwanamke |
| gender | o | Other | Autre | Nyingine |
| yes_no | yes | Yes | Oui | Ndiyo |
| yes_no | no | No | Non | Hapana |
```

---

## Language Codes

Standard language codes (ISO 639-1):

| Code | Language |
|------|----------|
| en | English |
| fr | French |
| es | Spanish |
| sw | Swahili |
| pt | Portuguese |
| ar | Arabic |
| ru | Russian |
| zh | Chinese |
| de | German |
| it | Italian |
| ja | Japanese |
| ko | Korean |
| hi | Hindi |
| bn | Bengali |
| am | Amharic |

Full list: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes

---

## How It Works

1. **Form loads** - User opens form on device
2. **Language selection** - Device/user selects language (based on phone settings)
3. **Matching display** - Form displays labels in selected language
4. **Data stored** - Selected language noted in submission metadata
5. **Fallback** - If language not available, uses default `label` column

### Example Flow

**User phone language setting:** French

Form displays:
```
Quel est votre nom?
Quel âge avez-vous?
Quel genre êtes-vous?
```

**Another user, phone language: English**

Form displays:
```
What is your name?
How old are you?
What is your gender?
```

Both submit to same form, but saw labels in their language.

---

## Settings Sheet

Optionally specify default language:

```
| default_language |
| en |
```

If form loaded on device with unsupported language, uses this default.

---

## Complete Form Example

**Survey:**
```
| type | name | label::en | label::fr | label::sw | hint::en | hint::fr | hint::sw |
| text | respondent_name | Respondent name | Nom du répondant | Jina la mhojiwa | Full name | Nom complet | Jina kamili |
| date | visit_date | Date of visit | Date de visite | Tarehe ya ziyara | | | |
| select_one gender | gender | Gender | Genre | Jinsia | | | |
| integer | num_children | Number of children | Nombre d'enfants | Idadi ya watoto | | | |
| select_one yes_no | has_income | Has income? | A un revenu? | Ana mapato? | | | |
```

**Choices:**
```
| list_name | name | label::en | label::fr | label::sw |
| gender | m | Male | Homme | Mwanamume |
| gender | f | Female | Femme | Mwanamke |
| gender | o | Other | Autre | Nyingine |
| yes_no | yes | Yes | Oui | Ndiyo |
| yes_no | no | No | Non | Hapana |
```

---

## Special Considerations

### RTL Languages

Right-to-left languages (Arabic, Hebrew):
- Platform handles display direction automatically
- Translations should work with RTL text
- Test on actual device to verify

**Arabic Example:**
```
| label::ar |
| ما هو اسمك؟ |
| كم عمرك؟ |
```

### Character Encoding

- All forms must use **UTF-8** encoding
- Supports all unicode characters
- Most modern tools default to UTF-8
- Verify in Excel → File → Options → Encoding

### Language-Specific Logic

You can use skip logic based on language selection:

```
| relevant |
| ${auth_language} = 'en' |
```

(Show question only in English)

---

## Best Practices

### Do's
✓ Translate all labels and hints
✓ Test all languages on actual device
✓ Use consistent terminology across languages
✓ Include professional translators for languages you don't speak
✓ Test RTL languages separately if included
✓ Keep translations concise

### Don'ts
✗ Don't use Google Translate without review
✗ Don't mix languages (confusing for users)
✗ Don't forget to translate choice labels
✗ Don't use overly long translations (won't fit)
✗ Don't assume direct word-for-word translation
✗ Don't ignore cultural context (numbers, dates, formats)

---

## Translation Workflow

### Step 1: Create Bilingual Template
```
| label::en | label::fr |
| English text | Texte français |
```

### Step 2: Identify Strings to Translate
- All `label` columns
- All `hint` columns
- Choice `label` columns
- `note` messages

### Step 3: Get Translations
- Professional translator
- Community speakers
- Translation service (then review)

### Step 4: Add to Form
```
| label::en | label::fr | label::sw |
| English | Français | Kiswahili |
```

### Step 5: Test
1. Switch phone language to each language
2. Verify form displays correctly
3. Check text wrapping and readability
4. Test special characters display

---

## Testing Multilingual Forms

**Before Deployment:**

1. **Per-language testing:**
   - Set device language to English → test
   - Set device language to French → test
   - Set device language to Swahili → test

2. **Edge cases:**
   - Very long translations
   - Special characters and diacritics
   - Proper text wrapping

3. **Device-specific:**
   - Test on actual Android device
   - Test on actual iOS device
   - Verify language selection mechanism

4. **Offline:**
   - Download form
   - Change device language
   - Verify language switching works offline

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Missing language columns | Only English shows | Add `label::fr`, `label::sw`, etc. |
| Column name typo | Language not used | Check exact spelling: `label::Language` |
| Choice labels not translated | Choices show English only | Add `label::language` to choices sheet |
| Inconsistent language codes | Mixed columns | Use standard codes: `en`, `fr`, not `English`, `French` |
| Unicode issues | Special characters broken | Save as UTF-8 encoding |
| Truncated text | Long translations cut off | Shorter translations or test on device |

---

## Performance

- No performance impact from multiple languages
- All languages stored in single form file
- Device selects language at runtime
- Multilingual forms same size as English-only

---

## Supported Languages by Platform

| Language | ODK Collect | KoBoToolbox | SurveyCTO | Enketo |
|----------|---|---|---|---|
| English | ✓ | ✓ | ✓ | ✓ |
| French | ✓ | ✓ | ✓ | ✓ |
| Spanish | ✓ | ✓ | ✓ | ✓ |
| Swahili | ✓ | ✓ | ✓ | ✓ |
| Arabic | ✓ | ✓ | ✓ | ✓ |
| Amharic | ✓ | ✓ | ✓ | ✓ |
| Portuguese | ✓ | ✓ | ✓ | ✓ |

Most platforms support 20+ languages. Check your platform for specific support.

---

## Example: Healthcare Survey (3 Languages)

**Survey:**
```
| type | name | label::en | label::fr | label::sw |
| text | name | Full name | Nom complet | Jina kamili |
| date | dob | Birth date | Date de naissance | Tarehe ya kuzaliwa |
| select_one gender | gender | Gender | Genre | Jinsia |
| select_one yes_no | pregnant | Are you pregnant? | Êtes-vous enceinte? | Je na tukucha? |
| select_one condition | condition | Health condition | État de santé | Hali ya afya |
```

**Choices:**
```
| list_name | name | label::en | label::fr | label::sw |
| gender | m | Male | Homme | Mwanamume |
| gender | f | Female | Femme | Mwanamke |
| yes_no | yes | Yes | Oui | Ndiyo |
| yes_no | no | No | Non | Hapana |
| condition | good | Good | Bon | Nzuri |
| condition | fair | Fair | Moyen | Kawaida |
| condition | poor | Poor | Mauvais | Mbaya |
```

Users in English-speaking countries see English. Users in French regions see French. Users in Swahili-speaking areas see Swahili. All from same form.

---

## See Also

- [survey-sheet.md](survey-sheet.md) - Survey worksheet reference
- [choices-sheet.md](choices-sheet.md) - Choices worksheet reference
- [examples.md](../examples.md) - Example multilingual form
