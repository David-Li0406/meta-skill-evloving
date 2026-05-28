# [PRODUCT_NAME] Product Constitution

> Project: [PROJECT_NAME]
> Created: [CREATED_DATE]
> Last Updated: [UPDATED_DATE]

This document provides shared constraints and domain information for all product management activities.

---

## Product Overview

### Basic Information

| Item                    | Content                |
| ----------------------- | ---------------------- |
| **Product Name**        | [PRODUCT_NAME]         |
| **One-line Definition** | [ONE_LINE_DESCRIPTION] |
| **Slogan**              | [SLOGAN]               |

### Target Users

| User Type           | Description                  |
| ------------------- | ---------------------------- |
| **Primary Users**   | [PRIMARY_USER_DESCRIPTION]   |
| **Secondary Users** | [SECONDARY_USER_DESCRIPTION] |

### Core Value Proposition

[CORE_VALUE_PROPOSITION]

---

## Domain Information

### Industry/Market Context

[INDUSTRY_CONTEXT]

### Core Terminology

| Term         | Definition     |
| ------------ | -------------- |
| **[TERM_1]** | [DEFINITION_1] |
| **[TERM_2]** | [DEFINITION_2] |

### Compliance Requirements

- [ ] No special compliance requirements
- [ ] GDPR
- [ ] SOC 2
- [ ] Other: [SPECIFY]

---

## Technical Constraints

| Constraint          | Description       |
| ------------------- | ----------------- |
| **Language**        | [LANGUAGE]        |
| **Runtime**         | [RUNTIME]         |
| **Main Framework**  | [FRAMEWORK]       |
| **Package Manager** | [PACKAGE_MANAGER] |

---

## Business Constraints

| Constraint Type | Description            |
| --------------- | ---------------------- |
| **Budget**      | [BUDGET_CONSTRAINTS]   |
| **Timeline**    | [TIMELINE_CONSTRAINTS] |
| **Resources**   | [RESOURCE_CONSTRAINTS] |

---

## Standards

### Documentation Language

- [ ] Chinese
- [ ] English
- [ ] Bilingual

### Naming Conventions

| Type           | Convention       | Example        |
| -------------- | ---------------- | -------------- |
| Version Number | Semantic Version | v1.0.0, v1.1.0 |
| Story ID       | S-XXX            | S-001, S-002   |
| Task ID        | T-XXX            | T-001, T-002   |

### Versioning

- Follow Semantic Versioning (SemVer)
- Format: `v{major}.{minor}.{patch}`
- Major: Breaking changes, not backward compatible
- Minor: New features, backward compatible
- Patch: Bug fixes

---

## Project Structure

```
docs/reference/
├── pm/
│   ├── constitution.md     # This document
│   ├── versions/           # Version plans
│   │   └── v1.0.0.md
│   └── stories/            # User stories
│       ├── S-001.md
│       └── ...
├── frontend/
│   ├── design-system.md    # Design system
│   ├── constraints.md      # Frontend constraints
│   ├── designs/            # Page designs
│   └── tasks/              # Frontend tasks
└── backend/
    ├── constraints.md      # Backend constraints
    └── tasks/              # Backend tasks
```

---

## Git Conventions

### Commit Messages

- Use Conventional Commits
- Format: `type(scope): subject`
- Types: feat, fix, docs, style, refactor, test, chore

### Branch Naming

```
feature/[feature-name]
fix/[bug-description]
refactor/[area]
```
