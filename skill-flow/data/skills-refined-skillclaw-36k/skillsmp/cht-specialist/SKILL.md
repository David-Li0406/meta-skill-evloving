---
name: "CHT Specialist"
description: "Expert assistance with Community Health Toolkit (CHT) development, configuration, troubleshooting, and architecture. Use when working with CHT applications, forms (XLSForm/XForm), tasks.js, targets.js, contact-summary, app_settings.json, cht-conf CLI, Docker deployment, workflows, integrations, or any CHT-related questions. Provides guidance on building CHT apps, debugging issues, understanding architecture, and following best practices."
---

# CHT Specialist

## When to Consult Reference Files

**Read the detailed reference files** when the user asks about:

| Topic | Reference File |
|-------|----------------|
| cht-conf CLI commands, options, CSV imports, authentication | [references/cht-conf-reference.md](references/cht-conf-reference.md) |
| Tasks.js schema, events, actions, resolvedIf | [references/tasks-reference.md](references/tasks-reference.md) |
| Targets.js schema, counting modes, groupBy | [references/targets-reference.md](references/targets-reference.md) |
| Contact summary fields, cards, context | [references/contact-summary-reference.md](references/contact-summary-reference.md) |
| XLSForm syntax, CHT widgets, CHT-specific form patterns | [references/forms-reference.md](references/forms-reference.md) |
| app_settings.json configuration | [references/app-settings-reference.md](references/app-settings-reference.md) |
| REST API endpoints, export, users, contacts | [references/api-reference.md](references/api-reference.md) |
| Sentinel transitions, muting, death reporting, registrations | [references/transitions-reference.md](references/transitions-reference.md) |
| SMS messaging, gateways, schedules, states | [references/messaging-reference.md](references/messaging-reference.md) |
| Translations, localization, multilingual forms | [references/translations-reference.md](references/translations-reference.md) |
| Docker/Kubernetes deployment, monitoring | [references/hosting-reference.md](references/hosting-reference.md) |
| Version compatibility, migrations | [references/version-compatibility.md](references/version-compatibility.md) |
| Database document schemas | [references/database-schema.md](references/database-schema.md) |
| Utils functions (addDate, getField, isFormSubmittedInWindow, etc.) | [references/utils-reference.md](references/utils-reference.md) |
| CHT API (cht.v1 permissions, extension libs, analytics) | [references/cht-api-reference.md](references/cht-api-reference.md) |

### ODK/XLSForm Documentation

**When working with XLSForm/ODK forms**, consult these files based on the topic:

| User asks about... | Read this file |
|-------------------|----------------|
| Form structure, survey/choices/settings sheets | [references/odk-forms/01-structure.md](references/odk-forms/01-structure.md) |
| Question types (text, select, date, geopoint, image, etc.) or `appearance` options | [references/odk-forms/02-question-types.md](references/odk-forms/02-question-types.md) |
| Skip logic (`relevant`), validation (`constraint`), `calculation`, `default`, `trigger` | [references/odk-forms/03-form-logic.md](references/odk-forms/03-form-logic.md) |
| XPath functions (string, math, date, select, repeat functions) | [references/odk-forms/04-functions.md](references/odk-forms/04-functions.md) |
| Groups, repeats, `field-list`, nested structures, repeat counts | [references/odk-forms/05-groups-repeats.md](references/odk-forms/05-groups-repeats.md) |
| External CSV data, cascading selects, `choice_filter`, `instance()` | [references/odk-forms/06-external-data.md](references/odk-forms/06-external-data.md) |
| Multiple languages, translations, `label::language` columns | [references/odk-forms/07-multilanguage.md](references/odk-forms/07-multilanguage.md) |
| Markdown formatting, grids, themes, `style` column | [references/odk-forms/08-styling.md](references/odk-forms/08-styling.md) |
| ODK Entities, longitudinal data, `entity_create`, `entity_update` | [references/odk-forms/09-entities.md](references/odk-forms/09-entities.md) |
| Audit logging, tracking enumerator behavior, `audit` type | [references/odk-forms/10-audit-logging.md](references/odk-forms/10-audit-logging.md) |
| Form encryption, RSA keys, `public_key` setting | [references/odk-forms/11-encryption.md](references/odk-forms/11-encryption.md) |
| CHT-specific: `db:person`, `contact-summary`, countdown-timer, `cht:` functions | [references/odk-forms/12-cht-extensions.md](references/odk-forms/12-cht-extensions.md) |
| Quick patterns, common calculations (age, BMI, EDD), cheat sheets | [references/odk-forms/13-quick-reference.md](references/odk-forms/13-quick-reference.md) |

**Guidance:**
- For **CHT-specific form features** (contact selector, countdown timer, `cht:` XPath functions): read `12-cht-extensions.md` first
- For **standard ODK/XLSForm syntax**: use the topic-specific files above
- For **quick lookup** of common patterns: start with `13-quick-reference.md`
- When **analyzing or creating a form**: read `01-structure.md` + relevant topic files

### Assets

| Asset Type | Location |
|------------|----------|
| Form templates (home visit, assessment, registration) | [assets/templates/](assets/templates/) |
| Example configurations | [assets/examples/](assets/examples/) |

---

## Overview

Expert guidance for the Community Health Toolkit (CHT), an open-source framework for building digital health applications in low-resource, offline-first settings. CHT powers applications for community health workers (CHWs), nurses, supervisors, and data managers.

**Key Characteristics:**
- Offline-first architecture using CouchDB/PouchDB
- XLSForm-based care guides and reports
- JavaScript-based task and target configuration
- Role-based permissions and data replication
- SMS workflow support

## Prerequisites

- Node.js 20+ and npm
- Docker and Docker Compose
- cht-conf CLI tool (`npm install -g cht-conf`)

## Quick Start

### Local Development Setup

```bash
# Install cht-conf globally
npm install -g cht-conf

# Initialize a new CHT project
mkdir my-cht-app && cd my-cht-app
cht initialise-project-layout

# Deploy to local instance
cht --url=https://medic:password@localhost --accept-self-signed-certs
```

### Docker CHT Instance

```bash
# Create directory structure
mkdir -p ~/cht/{compose,certs,upgrade-service,couchdb}

# Download compose files (check for latest version)
cd ~/cht/
curl -s -o ./compose/cht-core.yml https://staging.dev.medicmobile.org/_couch/builds_4/medic:medic:4.21.1/docker-compose/cht-core.yml
curl -s -o ./compose/cht-couchdb.yml https://staging.dev.medicmobile.org/_couch/builds_4/medic:medic:4.21.1/docker-compose/cht-couchdb.yml
curl -s -o ./upgrade-service/docker-compose.yml https://raw.githubusercontent.com/medic/cht-upgrade-service/main/docker-compose.yml

# Start CHT
cd ~/cht/upgrade-service
docker compose up --detach
```

---

## Project Structure

```
my-cht-app/
  app_settings.json          # Main app configuration (compiled)
  app_settings/
    base_settings.json       # Base settings
    forms.json               # Form settings
    schedules.json           # SMS schedules
  contact-summary.templated.js  # Contact profile configuration
  tasks.js                   # Task definitions
  targets.js                 # Target/goal definitions
  purge.js                   # Data purging rules
  resources.json             # Icon and resource mappings
  resources/                 # Icons and media
  forms/
    app/                     # App forms (care guides)
      form_name.xlsx
      form_name.properties.json
      form_name-media/
    contact/                 # Contact creation forms
  translations/
    messages-en.properties
    messages-fr.properties
```

---

## Tasks Configuration

Tasks are reminders that appear in the Tasks tab, prompting users to complete follow-up activities. See [references/tasks-reference.md](references/tasks-reference.md) for complete schema, event timing, actions, and resolution logic.

---

## Targets Configuration

Targets display key performance indicators on the Analytics tab. See [references/targets-reference.md](references/targets-reference.md) for complete schema, counting modes (`idType`), date filtering, and `groupBy` aggregation.

---

## Contact Summary Configuration

Contact summary defines the profile page for contacts, including fields, condition cards, and context variables. See [references/contact-summary-reference.md](references/contact-summary-reference.md) for fields schema, cards configuration, and available filters.

---

## Forms (XLSForm)

CHT uses XLSForm format converted to ODK XForm. See [references/forms-reference.md](references/forms-reference.md) for form structure, CHT widgets, XPath functions, and properties.json configuration.

---

## cht-conf CLI Commands

**For detailed cht-conf documentation**, see [references/cht-conf-reference.md](references/cht-conf-reference.md) which covers all 42 CLI actions, CSV data import, authentication methods, and contact hierarchy management.

### Common Commands

| Command | Description |
|---------|-------------|
| `cht initialise-project-layout` | Initialize new project |
| `cht --local compile-app-settings upload-app-settings` | Compile and upload settings |
| `cht --local convert-app-forms upload-app-forms` | Convert and upload all app forms |
| `cht --local convert-app-forms upload-app-forms -- form1 form2` | Convert specific forms |
| `cht --local convert-contact-forms upload-contact-forms` | Convert and upload contact forms |
| `cht --local upload-resources` | Upload icons and media |
| `cht --local upload-custom-translations` | Upload translations |
| `cht --local csv-to-docs upload-docs` | Import CSV data |
| `cht --local move-contacts -- --contacts=<id> --parent=<id>` | Move contacts |
| `cht --local edit-contacts -- --columns=field --files=data.csv` | Bulk edit contacts |

### Connection Options

```bash
# Local with self-signed certs
cht --url=https://medic:password@localhost --accept-self-signed-certs

# Remote instance
cht --url=https://user:pass@your-instance.app.medicmobile.org

# Using instance shorthand
cht --instance=your-instance

# Skip server checks (offline compilation)
cht --no-check compile-app-settings
```

---

## Troubleshooting

### Common Issues

**Task not appearing:**
1. Check `appliesTo` and `appliesToType` match your data
2. Verify `appliesIf` returns true for your scenario
3. Check event timing (`days`, `start`, `end`)
4. Tasks only show for restricted users

**Target not counting correctly:**
1. Verify `appliesIf` logic
2. Check `date` filter ('reported' vs 'now')
3. For percent, check `passesIf` logic
4. Verify `appliesToType` matches form codes

**Form not showing:**
1. Check `context.expression` in properties.json
2. Verify user has required permissions
3. Check form was uploaded successfully

**Replication issues:**
1. Check user permissions and place assignment
2. Verify contact hierarchy
3. Check for document conflicts

### Debug Commands

```bash
# Check form conversion
cht --local convert-app-forms

# Validate app settings
cht --local compile-app-settings

# Check instance connection
cht --url=https://... fetch-forms-from-server
```

---

## Best Practices

### Forms
- Keep titles under 40 characters
- Use Title Case for titles
- Don't include patient name in form title
- Stack radio buttons vertically
- Use images to aid understanding
- Group related questions logically

### Tasks
- Limit task generation to near future (60 days past, 180 days future)
- Use unique task names
- Provide clear resolution conditions
- Consider performance with many contacts
- Use `appliesIf` to filter early for better performance

### Targets
- Use sentence case for titles
- Keep titles under 40-50 characters
- Choose appropriate date filter ('reported' vs 'now')
- Set meaningful goals
- Use `idType: 'contact'` to avoid double-counting

### Contact Summary
- Group related information in cards
- Only show actionable information
- Use icons for important statuses
- Keep field count reasonable for mobile

---

## Version Compatibility

| Feature | Minimum Version |
|---------|-----------------|
| Configurable contact types | 3.7.0 |
| CHT API (cht.v1) | 3.12.0 |
| Task priority scoring | 4.21.0 |
| Contact form task actions | 4.21.0 |
| `trigger` countdown timer | 4.7.0 |
| `string` tel input | 4.11.0 |
| `cht:difference-in-*` functions | 4.7.0 |
| `add-date` function | 4.0.0 |
| `userSummary` in expressions | 4.21.0 |
| `duplicate_check` in contact forms | 4.19.0 |

---

## CHT Docs MCP Server

The CHT provides an official MCP (Model Context Protocol) server for AI-assisted development.

**URL:** `https://mcp-docs.dev.medicmobile.org/mcp`

| Tool | Description |
|------|-------------|
| `ask_question` | Query CHT documentation via Kapa AI |
| `search_docs` | Direct documentation search |
| `get_sources` | List available knowledge sources |

**Installation:**
```bash
claude mcp add --transport http cht-kapa-docs https://mcp-docs.dev.medicmobile.org/mcp
```

---

## External Links

- [CHT Documentation](https://docs.communityhealthtoolkit.org)
- [CHT GitHub](https://github.com/medic/cht-core)
- [CHT Forum](https://forum.communityhealthtoolkit.org)
- [XLSForm Reference](https://xlsform.org)
- [CHT AI Tools](https://docs.communityhealthtoolkit.org/ai/)
