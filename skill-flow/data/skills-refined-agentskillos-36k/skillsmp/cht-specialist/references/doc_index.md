# CHT Documentation Index

This file provides a comprehensive index of the CHT documentation structure located at `/Users/romuald/Developer/Medic/cht-docs/content/en/`.

## Primary Documentation Categories

### 1. Building CHT Applications (`building/`)
Core documentation for developing and configuring CHT applications:

- **Forms** (`building/forms/`) - XForms, app forms, contact forms, form processing
- **Tasks** (`building/tasks/`) - Task configuration, scheduling, workflows
- **Targets** (`building/targets/`) - Target/goal configuration and widgets
- **Contact Management** (`building/contact-management/`) - Contact hierarchy, person and place configuration
- **Contact Summary** (`building/contact-summary/`) - Contact profile cards and context
- **Reports** (`building/reports/`) - Report configuration and management
- **Workflows** (`building/workflows/`) - Workflow design and implementation
- **Translations** (`building/translations/`) - Internationalization and localization
- **Branding** (`building/branding/`) - Customizing app appearance
- **Users** (`building/users/`) - User roles, permissions, authentication
- **Messaging** (`building/messaging/`) - SMS and messaging features
- **Integrations** (`building/integrations/`) - External system integrations
- **Interoperability** (`building/interoperability/`) - FHIR, HL7, data exchange
- **Reference** (`building/reference/`) - API references, configuration schemas
- **Local Setup** (`building/local-setup/`) - Development environment setup
- **Tutorials** (`building/tutorials/`) - Step-by-step guides

### 2. Technical Overview (`technical-overview/`)
Architecture and technical concepts:

- **Architecture** (`technical-overview/architecture/`) - System architecture, components, data flows
- **Concepts** (`technical-overview/concepts/`) - Core concepts and terminology
- **Data** (`technical-overview/data/`) - Data models, schemas, database structure

### 3. Hosting & Deployment (`hosting/`)
Production deployment and infrastructure:

- **CHT Core** (`hosting/cht/`) - Deployment options, requirements, configuration
- **Monitoring** (`hosting/monitoring/`) - System monitoring and alerting
- **Analytics** (`hosting/analytics/`) - Data analytics and reporting
- **SSO** (`hosting/SSO/`) - Single Sign-On configuration
- **Couch2PG** (`hosting/couch2pg/`) - CouchDB to PostgreSQL replication

### 4. Design (`design/`)
User experience and design resources:

- **Best Practices** (`design/best-practices/`) - UX best practices
- **Interface** (`design/interface/`) - UI components, colors, typography, icons
- **Personas** (`design/personas/`) - User personas and use cases
- **Mapping Hierarchy** (`design/mapping-hierarchy/`) - Contact hierarchy design

### 5. Reference Applications (`reference-apps/`)
Example implementations and templates:

- Supervisor Reference App
- Maternal & Newborn Health
- Contact Tracing
- Stock Monitoring
- COVID-19 RDT
- Pharmacovigilance
- Direct to Client
- And more...

### 6. Community & Contributing (`community/`)
- Contributing guidelines
- Community resources
- Development practices

### 7. Releases (`releases/`)
- Release notes
- Version history
- Migration guides

## Troubleshooting

Root-level troubleshooting guide: `/Users/romuald/Developer/Medic/cht-docs/troubleshooting.md`

## Search Patterns

When searching for specific topics, use these grep patterns:

- Configuration schemas: `grep -r "schema" building/reference/`
- API documentation: `grep -r "API" building/reference/`
- Form examples: `find building/forms/ -name "*.md"`
- Task configuration: `find building/tasks/ -name "*.md"`
- Architecture diagrams: `find technical-overview/architecture/ -name "*.md"`
- Deployment guides: `find hosting/ -name "*.md" | grep -v "medic"`

## Key Configuration Files

Common configuration file types discussed in documentation:
- `app_settings.json` - Main application settings
- `forms/` - XLSForm and XForm definitions
- `contact-summary.templated.js` - Contact profile logic
- `tasks.js` - Task generation rules
- `targets.js` - Target calculation logic
- `purge.js` - Data purging rules
- `nools-rules.js` - Legacy declarative configuration

---

## Skill Reference Files

Comprehensive documentation extracted from cht-docs:

### Core Configuration
- [tasks-reference.md](tasks-reference.md) - Complete tasks.js configuration schema
- [targets-reference.md](targets-reference.md) - Complete targets.js configuration schema
- [contact-summary-reference.md](contact-summary-reference.md) - Contact summary configuration
- [forms-reference.md](forms-reference.md) - XLSForm/XForm development guide
- [app-settings-reference.md](app-settings-reference.md) - Application settings reference

### Infrastructure & Operations
- [hosting-reference.md](hosting-reference.md) - Docker/Kubernetes deployment and monitoring
- [cht-conf-reference.md](cht-conf-reference.md) - CLI tool commands and configuration
- [version-compatibility.md](version-compatibility.md) - Version support, migration guides, breaking changes

### Data & Architecture
- [database-schema.md](database-schema.md) - CouchDB document schemas and data model
