# CHT-Conf CLI Reference

## Overview

CHT-Conf (Community Health Toolkit Project Configurer) is the official command-line interface tool for configuring and managing CHT deployments.

**Repository:** https://github.com/medic/cht-conf
**Version:** 6.0.2
**Node.js Requirement:** >= 20.0.0

---

## Installation

### Requirements
- Node.js 20.0.0 or higher
- Python 3.10+ (for XLSForm conversion)
- Git (optional, for version control checks)

### Install via npm
```bash
npm install -g cht-conf
```

### Verify Installation
```bash
cht --version
cht --supported-actions
```

### Shell Completion
```bash
# Bash
cht --shell-completion=bash >> ~/.bashrc

# Zsh
cht --shell-completion=zsh >> ~/.zshrc
```

---

## Basic Usage

```bash
cht <connection-flag> [actions...] [options] [-- extra-args]
```

### Connection Flags (Required - Choose One)

| Flag | Description | Example |
|------|-------------|---------|
| `--local` | Local instance (uses COUCH_URL env var) | `cht --local upload-app-forms` |
| `--instance=NAME` | Medic Cloud instance | `cht --instance=myproject upload-app-forms` |
| `--url=URL` | Custom URL | `cht --url=https://admin:pass@server.com upload-app-forms` |
| `--archive` | Export to files | `cht --archive --destination=./export compile-app-settings` |

### Global Options

| Option | Description |
|--------|-------------|
| `--help` | Display usage |
| `--version` | Display version |
| `--supported-actions` | List all actions |
| `--source=PATH` | Project folder (default: `.`) |
| `--user=USERNAME` | Custom username with `--instance` |
| `--session-token=TOKEN` | Session token authentication |
| `--force` | Auto-confirm all prompts |
| `--verbose` | Enable trace logging |
| `--silent` | Suppress output |
| `--accept-self-signed-certs` | Accept self-signed SSL |
| `--skip-git-check` | Skip git status check |
| `--skip-dependency-check` | Skip version check |
| `--skip-translation-check` | Skip translation validation |
| `--skip-validate` | Skip form validation |

---

## All Actions (42 Total)

### Configuration Actions

| Action | Instance Required | Description |
|--------|-------------------|-------------|
| `compile-app-settings` | No | Compile app_settings from modular config |
| `backup-app-settings` | Yes | Download settings from instance |
| `upload-app-settings` | Yes | Upload compiled settings |
| `check-git` | No | Verify git status |
| `check-for-updates` | No | Check for newer cht-conf |

### Form Actions

| Action | Instance Required | Description |
|--------|-------------------|-------------|
| `convert-app-forms` | No | Convert XLS app forms to XForm |
| `convert-collect-forms` | No | Convert ODK Collect forms |
| `convert-contact-forms` | No | Convert contact forms |
| `convert-training-forms` | No | Convert training forms |
| `validate-app-forms` | No | Validate app forms |
| `validate-collect-forms` | No | Validate collect forms |
| `validate-contact-forms` | No | Validate contact forms |
| `validate-training-forms` | No | Validate training forms |
| `upload-app-forms` | Yes | Upload app forms |
| `upload-collect-forms` | Yes | Upload collect forms |
| `upload-contact-forms` | Yes | Upload contact forms |
| `upload-training-forms` | Yes | Upload training forms |
| `backup-all-forms` | Yes | Download all forms |
| `delete-all-forms` | Yes | Delete all forms |
| `delete-forms` | Yes | Delete specific forms |

### Resource Actions

| Action | Instance Required | Description |
|--------|-------------------|-------------|
| `upload-resources` | Yes | Upload custom resources |
| `upload-branding` | Yes | Upload branding assets |
| `upload-partners` | Yes | Upload partner data |
| `upload-custom-translations` | Yes | Upload translations |
| `upload-privacy-policies` | Yes | Upload privacy policies |
| `upload-extension-libs` | Yes | Upload extension libraries |
| `upload-database-indexes` | Yes | Create database indexes |

### Data Management Actions

| Action | Instance Required | Description |
|--------|-------------------|-------------|
| `csv-to-docs` | No | Convert CSV to JSON documents |
| `upload-docs` | Yes | Upload JSON documents |
| `create-users` | Yes | Create users from CSV |
| `edit-contacts` | Yes | Edit contacts via CSV |
| `move-contacts` | Yes | Move contacts in hierarchy |
| `merge-contacts` | Yes | Merge multiple contacts |
| `delete-contacts` | Yes | Delete contacts recursively |
| `upload-sms-from-csv` | Yes | Upload SMS messages |

### Utility Actions

| Action | Instance Required | Description |
|--------|-------------------|-------------|
| `initialise-project-layout` | No | Create project structure |
| `watch-project` | Yes | Watch and auto-upload changes |
| `compress-images` | No | Compress PNG and SVG files |
| `compress-pngs` | No | Compress PNG files |
| `compress-svgs` | No | Compress SVG files |
| `fetch-forms-from-google-drive` | No | Download forms from GDrive |
| `fetch-csvs-from-google-drive` | No | Download CSVs from GDrive |

---

## Project Structure

```bash
cht initialise-project-layout
```

Creates:
```
project/
├── .eslintrc                          # ESLint configuration (required)
├── app_settings.json                  # Compiled settings (generated)
├── contact-summary.templated.js       # Contact summary template
├── targets.js                         # Target definitions
├── tasks.js                           # Task definitions
├── purge.js                           # Data purging rules
├── resources.json                     # Resource mappings
├── harness.defaults.json              # Test harness defaults
├── privacy-policies.json              # Privacy policy config
│
├── app_settings/                      # Modular settings
│   ├── base_settings.json             # Core configuration
│   ├── forms.json                     # Form settings
│   ├── schedules.json                 # Task schedules
│   └── assetlinks.json                # Android App Links
│
├── forms/
│   ├── app/                           # Application forms
│   │   ├── form_name.xlsx             # XLSForm source
│   │   ├── form_name.xml              # Generated XForm
│   │   ├── form_name.properties.json  # Form properties
│   │   └── form_name-media/           # Form media files
│   ├── contact/                       # Contact forms
│   ├── collect/                       # ODK Collect forms
│   └── training/                      # Training forms
│
├── translations/
│   ├── messages-en.properties         # English
│   ├── messages-fr.properties         # French
│   └── messages-ex.properties         # Extension placeholders
│
├── resources/                         # Icons and media
├── extension-libs/                    # Custom JS libraries
├── privacy-policies/                  # Privacy policy documents
├── branding/                          # Branding assets
├── partners/                          # Partner assets
│
├── csv/                               # CSV data files
│   ├── contact.csv
│   ├── person.csv
│   ├── place.clinic.csv
│   └── report.form_type.csv
│
├── json_docs/                         # Generated JSON documents
│
└── test/                              # Test directories
    ├── forms/
    ├── contact-summary/
    ├── tasks/
    └── targets/
```

### Extension File Conventions

| Main File | Extension Pattern | Purpose |
|-----------|-------------------|---------|
| `tasks.js` | `*.tasks.js` | Additional task definitions |
| `targets.js` | `*.targets.js` | Additional target definitions |
| `contact-summary.templated.js` | `*.contact-summary.js` | Additional contact summary cards |

Extensions are auto-discovered and merged (sorted alphabetically).

---

## Form Management

### Form Types

| Type | Directory | ID Prefix | Enketo | Use Case |
|------|-----------|-----------|--------|----------|
| App | `forms/app/` | None | Yes | User-facing data collection |
| Contact | `forms/contact/` | `contact:` | Yes | Contact creation/editing |
| Collect | `forms/collect/` | None | No | ODK Collect offline |
| Training | `forms/training/` | `training:` | Yes | Training/assessment |

### Converting Forms

```bash
# Convert all app forms
cht --local convert-app-forms

# Convert specific forms
cht --local convert-app-forms -- form1 form2

# Debug mode (no minification)
cht --local convert-app-forms -- --debug
```

### Uploading Forms

```bash
# Upload all app forms
cht --local upload-app-forms

# Upload specific forms
cht --local upload-app-forms -- form1 form2

# Skip validation
cht --local --skip-validate upload-app-forms
```

### Form Properties File

Create `form_name.properties.json`:

```json
{
  "title": [
    { "locale": "en", "content": "Patient Registration" },
    { "locale": "fr", "content": "Inscription du patient" }
  ],
  "icon": "icon-add-person",
  "context": {
    "person": true,
    "place": false,
    "expression": "contact.type === 'person' && contact.sex === 'female'"
  },
  "hidden_fields": ["internal_calc"],
  "xml2sms": "REG"
}
```

| Property | Type | Description |
|----------|------|-------------|
| `title` | string/array | Form display name (i18n supported) |
| `icon` | string | Icon name from resources |
| `context.person` | boolean | Show for person contacts |
| `context.place` | boolean | Show for place contacts |
| `context.expression` | string | Dynamic visibility expression |
| `context.permission` | string | Required permission |
| `hidden_fields` | array | Fields to hide from UI |
| `xml2sms` | string | SMS command trigger |
| `subject_key` | string | Translation key for subject |
| `duplicate_check` | object | Contact form duplicate detection |

### Form Validation Rules

| Rule | Description | Critical |
|------|-------------|----------|
| `has-instance-id` | Form must have `<meta><instanceID/></meta>` | Yes |
| `check-xpaths-exist` | XPath references must exist | No |
| `db-doc-is-valid` | `db-doc="true"` only on groups with `type` | No |
| `db-doc-ref-is-valid` | `db-doc-ref` must reference valid nodes | No |
| `deprecated-appearance` | Warns about deprecated UI appearances | No |
| `deprecated-tel-type` | Warns about deprecated phone field types | No |
| `no-required-notes` | Read-only notes cannot be required | No |

---

## App Settings Compilation

### Configuration Sources

| File | Required | Purpose |
|------|----------|---------|
| `app_settings/base_settings.json` | Yes* | Core application settings |
| `app_settings/forms.json` | No | Form-specific settings |
| `app_settings/schedules.json` | No | Task schedules |
| `app_settings/assetlinks.json` | No | Android App Links |
| `contact-summary.templated.js` | No | Contact profile config |
| `tasks.js` | No | Task definitions |
| `targets.js` | No | Target definitions |
| `purge.js` | No | Data purging rules |

*Or `app_settings.json` for legacy monolithic config

### Commands

```bash
# Compile settings
cht --local compile-app-settings

# Compile with debug mode
cht --local compile-app-settings -- --debug

# Backup, compile, and upload
cht --local compile-app-settings backup-app-settings upload-app-settings
```

### Configuration Inheritance

Use `settings.inherit.json`:

```json
{
  "inherit": "../parent-project",
  "delete": [
    "transitions.update_clinics",
    "forms.OLD_FORM"
  ],
  "replace": {
    "locale": "sw",
    "locales": [{ "code": "sw", "name": "Kiswahili" }]
  },
  "merge": {
    "kujua-reporting": [{ "code": "NEW_REPORT" }]
  },
  "filter": {
    "forms": ["FORM1", "FORM2", "FORM3"]
  }
}
```

**Transformation Order:** Delete → Replace → Merge → Filter

---

## Contact & Hierarchy Management

### Move Contacts

```bash
# Move contacts to new parent
cht --local move-contacts -- --contacts=contact1,contact2 --parent=new_parent_id

# Move to root (no parent)
cht --local move-contacts -- --contacts=contact1 --parent=root

# Skip confirmation
cht --local move-contacts -- --contacts=contact1 --parent=new_parent --force
```

### Merge Contacts

```bash
# Merge sources into destination
cht --local merge-contacts -- --destination=clinic1 --sources=clinic2,clinic3

# Disable users at merged places
cht --local merge-contacts -- --destination=clinic1 --sources=clinic2 --disable-users
```

### Delete Contacts

```bash
# Delete contacts and all descendants
cht --local delete-contacts -- --contacts=contact1,contact2

# Also disable associated users
cht --local delete-contacts -- --contacts=contact1 --disable-users

# Skip confirmation
cht --local delete-contacts -- --contacts=contact1 --force
```

**Warning:** Deletion is permanent and cannot be undone.

### Edit Contacts

```bash
# Edit contacts from CSV
cht --local edit-contacts -- --files=contact.csv

# Edit specific columns only
cht --local edit-contacts -- --columns=phone,address
```

**Reserved Columns (Cannot Edit):** `parent`, `_id`, `name`, `reported_date`

---

## CSV Data Import/Export

### CSV to Documents

```bash
# Convert all CSVs to JSON
cht --local csv-to-docs

# Upload generated documents
cht --local upload-docs
```

### CSV File Naming

| Prefix | Document Type | Example |
|--------|---------------|---------|
| `contact` | Contact | `contact.csv` |
| `person` | Person | `person.csv` |
| `place.<type>` | Place | `place.clinic.csv` |
| `report.<form>` | Data Record | `report.pregnancy.csv` |
| `users` | User | `users.csv` |

### Column Type Annotations

Format: `column_name:type`

| Type | Format | Description | Example Output |
|------|--------|-------------|----------------|
| (none) | `column` | String (default) | `"value"` |
| `string` | `col:string` | Explicit string | `"value"` |
| `int` | `col:int` | Integer | `42` |
| `float` | `col:float` | Decimal | `3.14` |
| `bool` | `col:bool` | Boolean | `true`/`false` |
| `date` | `col:date` | ISO date | `"2024-01-15T00:00:00.000Z"` |
| `timestamp` | `col:timestamp` | Unix timestamp | `1705276800000` |
| `rel-date` | `col:rel-date` | Days from now | ISO date string |
| `rel-timestamp` | `col:rel-timestamp` | MS from now | Timestamp |
| `excluded` | `col:excluded` | Exclude from output | (not included) |

### Document References

```csv
# Get property from referenced document
column:PROPERTY OF TYPE WHERE field=COL_VAL

# Get entire document reference
column:TYPE WHERE field=COL_VAL
```

**Examples:**
```csv
# Get _id of a place
location:_id OF place WHERE external_id=COL_VAL

# Get name of a person
manager:name OF person WHERE external_id=COL_VAL

# Get entire contact document
contact:contact WHERE external_id=COL_VAL
```

### Example CSV Files

**Person with References:**
```csv
external_id:excluded,name,age:int,facility:_id OF place WHERE ext_id=COL_VAL
person-001,Alice Smith,35,facility-001
person-002,Bob Jones,42,facility-002
```

**Users CSV:**
```csv
username,password,roles,name,phone,place,contact.name,contact.phone
jsmith,Secret123!,chw:data_entry,John Smith,+1234567890,facility-001,John Smith,+1234567890
```

### Upload Options

```bash
# Upload from json_docs/
cht --local upload-docs

# Custom directory
cht --local upload-docs -- --docDirectoryPath=/path/to/docs

# Disable users at deleted facilities (CHT 4.7+)
cht --local upload-docs -- --disable-users
```

---

## Resources and Translations

### Upload Resources

```bash
cht --local upload-resources
```

**Configuration:** `resources.json`
```json
{
  "icon-person": "person.png",
  "icon-place": "place.svg",
  "logo": "branding/logo.png"
}
```

**Directory:** `resources/`

### Upload Translations

```bash
cht --local upload-custom-translations
```

**File format:** `messages-{LANG_CODE}.properties`

```properties
# messages-en.properties
app.title=My CHT App
contact.type.person=Person
form.pregnancy.title=Pregnancy Registration
records.total={{count}} records found
```

### Upload Branding/Partners

```bash
cht --local upload-branding
cht --local upload-partners
```

### Upload Extension Libraries

```bash
cht --local upload-extension-libs
```

**Directory:** `extension-libs/` (all `.js` files uploaded)

---

## Development Tools

### Watch Mode

```bash
# Start watch mode with initial upload
cht --local watch-project

# Skip initial upload
cht --local watch-project -- --skip-initial-upload
```

**Monitored Changes:**
| File Type | Action |
|-----------|--------|
| `forms/app/*.xlsx` | Convert → Validate → Upload |
| `forms/app/*.xml` | Validate → Upload |
| `forms/*-media/*` | Upload form |
| `translations/*` | Upload translations |
| `app_settings/*` | Compile → Upload settings |
| `resources/*` | Upload resources |

### Logging Levels

```bash
# Verbose (trace level)
cht --verbose --local upload-app-forms

# Normal (info level - default)
cht --local upload-app-forms

# Silent (no output)
cht --silent --local upload-app-forms
```

---

## Authentication

### Local Development

```bash
cht --local upload-app-forms
```

Default: `http://admin:pass@localhost:5988`

**Custom URL:**
```bash
export COUCH_URL=http://admin:password@localhost:5984/medic
cht --local upload-app-forms
```

### Medic Cloud Instance

```bash
# Prompts for password
cht --instance=myproject upload-app-forms

# Custom username
cht --instance=myproject --user=supervisor upload-app-forms
```

### Custom URL

```bash
cht --url=https://admin:password@server.example.com/medic upload-app-forms
```

### Session Token

```bash
cht --url=https://server.example.com/medic \
    --session-token=AuthSession_token_here \
    upload-app-forms
```

### Self-Signed Certificates

```bash
cht --local --accept-self-signed-certs upload-app-forms
```

---

## Common Workflows

### Full Deployment

```bash
cht --instance=myproject
```

### Local Development Cycle

```bash
cht --local compile-app-settings upload-app-settings
cht --local convert-app-forms validate-app-forms upload-app-forms
```

### Watch Mode Development

```bash
cht --local watch-project
```

### Data Import

```bash
cht --local csv-to-docs upload-docs
```

### Hierarchy Management

```bash
cht --local move-contacts -- --contacts=c1 --parent=p1
cht --local upload-docs
```

### Backup Before Changes

```bash
cht --instance=prod backup-app-settings backup-all-forms
```

### Archive for Offline Distribution

```bash
cht --archive --destination=./export compile-app-settings upload-app-settings
```

---

## Error Reference

### Form Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Problem executing xls2xform` | Python not installed | Install Python 3.10+ |
| `Empty group or repeat` | Group with no fields | Add fields to group |
| `File name does not match form_id` | Filename/ID mismatch | Rename file or update settings |
| `Missing instanceID node` | Old form version | Regenerate from XLSForm |

### CSV Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Unrecognised column type` | Invalid type annotation | Use valid type |
| `Cannot set property 'form'` | Protected column | Remove from CSV |
| `Failed to match reference` | Document not found | Check WHERE clause |

### Hierarchy Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Circular hierarchy` | Would create loop | Choose different destination |
| `Cannot remove primary contact` | Primary contact of place | Update primary contact first |

---

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `COUCH_URL` | Local instance URL for `--local` |
| `NODE_TLS_REJECT_UNAUTHORIZED` | SSL certificate validation |

---

## Help

```bash
cht --help
cht --supported-actions
```
