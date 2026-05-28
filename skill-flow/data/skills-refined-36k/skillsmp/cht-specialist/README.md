# CHT Specialist

A Claude Code skill for expert assistance with the [Community Health Toolkit (CHT)](https://communityhealthtoolkit.org/) - an open-source framework for building digital health applications in low-resource, offline-first settings.

## What is this?

This is a **Claude Code skill** that provides comprehensive guidance for CHT development, configuration, troubleshooting, and architecture. When installed, Claude Code gains deep expertise in:

- **ODK/XLSForm** - Complete ODK form syntax, question types, logic, functions, groups, repeats, external data, styling, and more
- **CHT Forms** - CHT-specific extensions, widgets (contact selector, countdown timer), and XPath functions
- **Tasks** - Task scheduling and workflow configuration (tasks.js)
- **Targets** - Analytics and KPI definition (targets.js)
- **Contact Summary** - Profile page customization
- **App Settings** - Application configuration (app_settings.json)
- **cht-conf CLI** - Command-line tool usage and deployment
- **Docker Deployment** - Local and production hosting
- **Database Schema** - CouchDB document structures

## Installation

### Option 1: Clone to skills directory

```bash
# Navigate to Claude Code skills directory
cd ~/.claude/skills/

# Clone the repository
git clone https://github.com/inromualdo/cht-specialist.git
```

### Option 2: Add as a submodule (for project-specific skills)

```bash
# In your project root
git submodule add https://github.com/inromualdo/cht-specialist.git .claude/skills/cht-specialist
```

## Usage

Once installed, the skill is automatically available when working on CHT projects. Simply ask Claude Code about CHT topics:

```
> How do I create a task that triggers 7 days after a delivery report?

> What's the schema for targets.js?

> Help me set up a countdown timer widget in my form

> Why isn't my task showing up for this patient?
```

## Repository Structure

```
cht-specialist/
├── SKILL.md                    # Main skill definition
├── references/                 # Detailed reference documentation
│   ├── app-settings-reference.md
│   ├── cht-conf-reference.md
│   ├── contact-summary-reference.md
│   ├── database-schema.md
│   ├── forms-reference.md
│   ├── hosting-reference.md
│   ├── targets-reference.md
│   ├── tasks-reference.md
│   ├── version-compatibility.md
│   └── odk-forms/              # ODK/XLSForm documentation
│       ├── 01-structure.md
│       ├── 02-question-types.md
│       ├── 03-form-logic.md
│       ├── 04-functions.md
│       ├── 05-groups-repeats.md
│       ├── 06-external-data.md
│       ├── 07-multilanguage.md
│       ├── 08-styling.md
│       ├── 09-entities.md
│       ├── 10-audit-logging.md
│       ├── 11-encryption.md
│       ├── 12-cht-extensions.md
│       └── 13-quick-reference.md
├── resources/
│   └── templates/              # Configuration templates
│       ├── contact-summary-template.js
│       ├── targets-template.js
│       └── tasks-template.js
└── scripts/                    # Utility scripts
```

## Topics Covered

### Core Configuration
| Topic | Reference File |
|-------|----------------|
| cht-conf CLI | [cht-conf-reference.md](references/cht-conf-reference.md) |
| Tasks.js | [tasks-reference.md](references/tasks-reference.md) |
| Targets.js | [targets-reference.md](references/targets-reference.md) |
| Contact Summary | [contact-summary-reference.md](references/contact-summary-reference.md) |
| Forms & XLSForm | [forms-reference.md](references/forms-reference.md) |
| App Settings | [app-settings-reference.md](references/app-settings-reference.md) |

### ODK/XLSForm
| Topic | Reference File |
|-------|----------------|
| Form Structure | [01-structure.md](references/odk-forms/01-structure.md) |
| Question Types | [02-question-types.md](references/odk-forms/02-question-types.md) |
| Form Logic | [03-form-logic.md](references/odk-forms/03-form-logic.md) |
| XPath Functions | [04-functions.md](references/odk-forms/04-functions.md) |
| Groups & Repeats | [05-groups-repeats.md](references/odk-forms/05-groups-repeats.md) |
| External Data | [06-external-data.md](references/odk-forms/06-external-data.md) |
| Multi-language | [07-multilanguage.md](references/odk-forms/07-multilanguage.md) |
| Styling | [08-styling.md](references/odk-forms/08-styling.md) |
| CHT Extensions | [12-cht-extensions.md](references/odk-forms/12-cht-extensions.md) |
| Quick Reference | [13-quick-reference.md](references/odk-forms/13-quick-reference.md) |

### Infrastructure
| Topic | Reference File |
|-------|----------------|
| Docker/Kubernetes | [hosting-reference.md](references/hosting-reference.md) |
| Version Compatibility | [version-compatibility.md](references/version-compatibility.md) |
| Database Schema | [database-schema.md](references/database-schema.md) |

## Requirements

For CHT development (not the skill itself):
- Node.js 20+
- Docker and Docker Compose
- cht-conf CLI (`npm install -g cht-conf`)

## External Resources

- [CHT Documentation](https://docs.communityhealthtoolkit.org)
- [CHT GitHub](https://github.com/medic/cht-core)
- [CHT Forum](https://forum.communityhealthtoolkit.org)
- [XLSForm Reference](https://xlsform.org)

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to improve the skill's coverage or accuracy.

## License

MIT
