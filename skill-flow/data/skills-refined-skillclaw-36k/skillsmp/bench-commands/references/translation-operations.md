# Translation Operations

## Translation System Overview

Frappe supports two translation systems:
- **Legacy**: CSV files (older, being phased out)
- **Modern**: POT/PO/MO files (gettext standard, recommended)

Both systems can coexist during migration.

## Modern Translation Workflow (POT/PO/MO)

### Step 1: Generate POT File

```bash
# Generate POT (Portable Object Template) for all apps
bench --site development.localhost generate-pot-file

# Generate for specific app only
bench --site development.localhost generate-pot-file --app soldamundo
```

**What it does:**
- Scans all translatable strings in your app
- Creates `.pot` file in `app/translations/`
- Includes strings from:
  - Python files (`_("text")`)
  - JavaScript files (`__("text")`)
  - JSON/HTML templates

**Output:** `apps/soldamundo/soldamundo/translations/soldamundo.pot`

### Step 2: Create PO File for Locale

```bash
# Create Spanish (Peru) translation file
bench --site development.localhost create-po-file es-PE

# Create for specific app
bench --site development.localhost create-po-file es-PE --app soldamundo

# Create for multiple locales
bench --site development.localhost create-po-file es
bench --site development.localhost create-po-file fr
bench --site development.localhost create-po-file de
```

**What it does:**
- Creates `.po` (Portable Object) file for specified locale
- Copies all translatable strings from POT file
- Creates file at `app/translations/{locale}.po`

**Output:** `apps/soldamundo/soldamundo/translations/es-PE.po`

### Step 3: Translate Strings

Edit the PO file manually or use translation tools:

```po
# apps/soldamundo/soldamundo/translations/es-PE.po

msgid "Sales Order"
msgstr "Orden de Venta"

msgid "Customer"
msgstr "Cliente"

msgid "Submit"
msgstr "Enviar"
```

### Step 4: Update PO Files (After Code Changes)

```bash
# Sync all PO files with latest POT
bench --site development.localhost update-po-files

# Update specific app
bench --site development.localhost update-po-files --app soldamundo

# Update specific locale only
bench --site development.localhost update-po-files --locale es-PE

# Update specific app and locale
bench --site development.localhost update-po-files --app soldamundo --locale es-PE
```

**What it does:**
- Merges new strings from POT into existing PO files
- Preserves existing translations
- Marks obsolete strings
- Adds new untranslated strings

### Step 5: Compile PO to MO

```bash
# Compile all PO files to MO (binary format)
bench --site development.localhost compile-po-to-mo

# Compile specific app
bench --site development.localhost compile-po-to-mo --app soldamundo

# Compile specific locale
bench --site development.localhost compile-po-to-mo --locale es-PE

# Force recompile even if unchanged
bench --site development.localhost compile-po-to-mo --force

# Compile specific app and locale
bench --site development.localhost compile-po-to-mo --app soldamundo --locale es-PE --force
```

**What it does:**
- Converts PO (text) files to MO (binary) files
- MO files are used at runtime for better performance
- Places MO files in same directory as PO files

**Output:** `apps/soldamundo/soldamundo/translations/es-PE.mo`

### Step 6: Build and Deploy

```bash
# Build message files for all sites
bench --site development.localhost build-message-files

# Clear cache to see changes
bench clear-cache

# Build assets
bench build
```

## Legacy Translation Workflow (CSV)

### Create CSV File for Language

```bash
# Create CSV translation file
bench --site development.localhost new-language es-PE soldamundo
```

**Output:** `apps/soldamundo/soldamundo/translations/es-PE.csv`

### Migrating from CSV to PO

```bash
# Migrate all CSV files to PO format
bench --site development.localhost migrate-csv-to-po

# Migrate specific app
bench --site development.localhost migrate-csv-to-po --app soldamundo

# Migrate specific locale
bench --site development.localhost migrate-csv-to-po --locale es-PE
```

**What it does:**
- Converts CSV translations to PO format
- Preserves existing translations
- Allows gradual migration from old to new system

### Backporting PO to CSV

```bash
# Add PO translations back to CSV (for older branches)
bench --site development.localhost update-csv-from-po soldamundo

# Update specific locale only
bench --site development.localhost update-csv-from-po soldamundo --locale es-PE
```

**Use case:**
Backporting translations from new system to maintain compatibility with older branches that still use CSV.

## Download Official Translations

```bash
# Download latest community translations
bench download-translations
```

**What it does:**
- Downloads latest translations from Frappe translation server
- Updates translations for frappe and erpnext
- Useful for getting community-contributed translations

## Advanced Translation Operations

### Get Untranslated Strings

```bash
# Export untranslated strings to file
bench --site development.localhost get-untranslated es-PE untranslated.txt

# For specific app
bench --site development.localhost get-untranslated es-PE untranslated.txt --app soldamundo

# Get all strings (including translated)
bench --site development.localhost get-untranslated es-PE all_strings.txt --all
```

**Use case:**
Identify missing translations to send to translators.

### Import Translations

```bash
# Import translations from external file
bench --site development.localhost import-translations es-PE translations.csv
```

**Use case:**
Import translations from external translation services or tools.

### Update Translations from File

```bash
# Update with translated strings
bench --site development.localhost update-translations es-PE untranslated.txt translated.txt

# For specific app
bench --site development.localhost update-translations es-PE untranslated.txt translated.txt --app soldamundo
```

**Workflow:**
1. Export untranslated: `get-untranslated`
2. Send to translator
3. Import back: `update-translations`

### Migrate App-Specific Translations

```bash
# Migrate translations between apps
bench --site development.localhost migrate-translations frappe custom_app
```

**Use case:**
Copy translations for DocTypes/terms that moved from one app to another.

## Complete Translation Workflow

### For New App

```bash
# 1. Mark strings for translation in code
# Python: _("My String")
# JavaScript: __("My String")

# 2. Generate POT file
bench --site development.localhost generate-pot-file --app my_app

# 3. Create PO files for target languages
bench --site development.localhost create-po-file es-PE --app my_app
bench --site development.localhost create-po-file es --app my_app
bench --site development.localhost create-po-file fr --app my_app

# 4. Translate strings (edit .po files)

# 5. Compile translations
bench --site development.localhost compile-po-to-mo --app my_app

# 6. Build and test
bench --site development.localhost build-message-files
bench clear-cache
bench build

# 7. Test in browser by changing language
# User Settings → Language
```

### For Existing App (Adding New Strings)

```bash
# 1. Add new translatable strings to code

# 2. Regenerate POT file
bench --site development.localhost generate-pot-file --app my_app

# 3. Update existing PO files
bench --site development.localhost update-po-files --app my_app

# 4. Translate new strings (edit .po files)

# 5. Recompile
bench --site development.localhost compile-po-to-mo --app my_app --force

# 6. Build and test
bench --site development.localhost build-message-files
bench clear-cache
bench build
```

### For Multi-App Project

```bash
# Update all apps at once
for app in frappe erpnext soldamundo tweaks; do
  echo "Processing $app..."
  bench --site development.localhost generate-pot-file --app $app
  bench --site development.localhost update-po-files --app $app
  bench --site development.localhost compile-po-to-mo --app $app
done

bench --site development.localhost build-message-files
bench clear-cache
bench build
```

## Translation Best Practices

### Code Guidelines

**Python:**
```python
# Use _ function for translations
from frappe import _

# Simple translation
frappe.msgprint(_("Order submitted successfully"))

# With context
frappe.msgprint(_("Status changed to {0}").format(frappe.bold(_("Completed"))))

# Plural forms
_("1 item selected") if count == 1 else _("{0} items selected").format(count)
```

**JavaScript:**
```javascript
// Use __ function
frappe.msgprint(__("Order submitted successfully"));

// With formatting
frappe.msgprint(__("Status changed to {0}", [__("Completed")]));

// In Vue/HTML templates
{{ __("Submit") }}
```

### File Organization

```
app/
  translations/
    app.pot              # POT template (generated)
    es-PE.po            # Spanish (Peru) translations
    es.po               # Spanish (generic)
    es-PE.mo            # Compiled binary (generated)
    es.mo               # Compiled binary (generated)
    es-PE.csv           # Legacy (optional)
```

### Workflow Tips

1. **Generate POT regularly** - After adding new strings
2. **Update PO before translating** - Ensures you have latest strings
3. **Compile before testing** - MO files are what's actually used
4. **Force compile if needed** - If changes don't appear
5. **Clear cache always** - Translations are cached
6. **Build message files** - For site-wide updates

### Common Issues

**Translations not appearing:**
```bash
# Solution:
bench --site development.localhost compile-po-to-mo --force
bench --site development.localhost build-message-files
bench clear-cache
bench build
```

**New strings not in PO files:**
```bash
# Solution:
bench --site development.localhost generate-pot-file --app my_app
bench --site development.localhost update-po-files --app my_app
```

**Wrong locale:**
```bash
# Check user language setting
# Or set default in site_config.json:
bench --site development.localhost set-config lang "es-PE"
```

## Continuous Translation Workflow

### During Development

```bash
# Add to git pre-commit hook
bench --site development.localhost generate-pot-file --app my_app
bench --site development.localhost update-po-files --app my_app
git add apps/my_app/my_app/translations/
```

### For Translators

```bash
# 1. Export untranslated strings
bench --site development.localhost get-untranslated es-PE untranslated.txt --app my_app

# 2. Send to translator

# 3. Import completed translations
bench --site development.localhost import-translations es-PE translated.csv --app my_app

# 4. Compile and deploy
bench --site development.localhost compile-po-to-mo --app my_app
bench --site development.localhost build-message-files
bench clear-cache
```

### Production Deployment

```bash
# Before deploying to production:

# 1. Ensure all PO files are compiled
bench --site production.site compile-po-to-mo --force

# 2. Build message files
bench --site production.site build-message-files

# 3. Download community translations
bench download-translations

# 4. Build assets
bench build --production

# 5. Clear cache
bench --site production.site clear-cache

# 6. Restart
bench restart
```

## Translation Testing

### Test in Different Languages

```bash
# 1. Set language in site config
bench --site development.localhost set-config lang "es-PE"

# 2. Or change user language
# Login → User Settings → Language → Select language

# 3. Test all pages and forms

# 4. Check browser console for untranslated strings
```

### Automated Testing

```python
# In your test file
def test_translations():
    frappe.set_user_lang("es-PE")

    # Test doctype label translation
    meta = frappe.get_meta("Sales Order")
    assert meta.get_label() == "Orden de Venta"

    # Test field label translation
    field = meta.get_field("customer")
    assert field.get_label() == "Cliente"
```

## Tools and Resources

### PO File Editors

- **Poedit**: https://poedit.net/ (GUI editor)
- **Lokalize**: KDE translation tool
- **Virtaal**: Simple translation editor
- **VS Code Extensions**: gettext, i18n tools

### Online Translation Platforms

- **Weblate**: Self-hosted translation platform
- **Crowdin**: Cloud-based translation management
- **Transifex**: Translation management system

### Frappe Translation Platform

Access community translations:
- https://translate.erpnext.com
