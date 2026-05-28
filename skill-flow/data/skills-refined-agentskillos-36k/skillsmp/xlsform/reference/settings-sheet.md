# Settings Sheet Reference

The optional settings worksheet contains form-level metadata and configuration. Most forms don't need this, but it's useful for specifying form name, version, and other properties.

## When You Need Settings Sheet

- Specify official form name/title
- Set form version for tracking changes
- Configure submission format
- Set form default language
- Configure instance/submission naming
- Customize form behavior

**When You Don't Need It:**
- Simple surveys (basic form will work)
- Testing/prototype forms
- Single-language forms without special requirements

---

## Common Settings Columns

### form_title
Official name of the form displayed in form lists.

**Rules:**
- Free text (any language, characters)
- Displayed in form picker on mobile/web
- Different from question labels
- If not specified, form filename is used

**Example:**
```
| form_title |
| Community Health Survey |

| form_title |
| Mambo Yenye Utanzu: Kabila la Wanawake |
```

---

### form_id
Unique identifier for form (for database/server purposes).

**Rules:**
- Alphanumeric + underscore only
- Should be unique across all your forms
- Used by servers to identify form version/updates
- If not specified, system generates one

**Example:**
```
| form_id |
| community_health_v2 |

| form_id |
| household_census_2024 |
```

---

### version
Version number tracking form changes and updates.

**Rules:**
- Any format (numeric, date, semantic)
- Each update should increment
- Helps track which version respondent used
- Stored with submission data

**Example:**
```
| version |
| 1.0 |

| version |
| 2.5 |

| version |
| 2024.10.30 |
```

**Good Practice:**
- Version 1.0: Initial release
- Version 1.1: Minor fixes
- Version 2.0: Significant changes
- Date-based: 2024.10.30 (date of release)

---

### submission_url
Server endpoint where forms submit (if using ODK Central, KoBoToolbox, etc.).

**Rules:**
- Full HTTPS URL
- Server-specific configuration
- Usually set in mobile app, not in form
- Rarely needed in XLSForm itself

---

### public_key
Encryption public key (for encrypted submissions).

**Rules:**
- Long hex string from encryption key pair
- Only if form requires encryption
- Server provides this

---

### instance_name
Pattern for naming submission instances.

**Rules:**
- Can reference question names: `${question_name}`
- Creates readable submission names
- Helps identify submissions in server

**Example:**
```
| instance_name |
| ${respondent_name}_${visit_date} |

| instance_name |
| Survey_${id}_${date} |
```

Results in:
```
John_Smith_2024-10-30
Mary_Jones_2024-10-29
```

---

### default_language
Default language code when form loads.

**Rules:**
- Language code (en, fr, es, sw, etc.)
- Must match a language column in survey/choices
- Used if device language not matched
- If not set, first language used

**Example:**
```
| default_language |
| en |

(Form loads in English if available)

| default_language |
| sw |

(Form loads in Swahili)
```

---

## Advanced Settings

### class
Form-level appearance class (affects all questions).

**Values:**
- `theme-grid` - Grid layout
- `theme-border` - Bordered questions
- `field-list` - List view

---

### style
Global styling CSS (platform-specific).

---

## Example Settings Sheet

**Minimal (common):**
```
| form_title | form_id | version |
| Community Survey | comm_survey_2024 | 2.1 |
```

**Complete:**
```
| form_title | form_id | version | instance_name | default_language |
| Household Census | household_census | 3.0 | Census_${hh_id}_${date} | en |
```

**Multilingual Form:**
```
| form_title | form_id | version | default_language |
| Census Form | census_2024 | 1.0 | en |
```

---

## Notes

- Settings worksheet is optional
- Most forms work without it
- Useful for professional deployments
- Each row typically has one setting
- Settings affect form behavior and metadata, not data collection

See examples.md for complete forms with and without settings sheet.
