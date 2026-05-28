---
name: docs
description: Generate API documentation, component docs, schema docs, and changelogs. Use when documenting new endpoints, creating component documentation, updating READMEs, or writing release notes.
---

# Documentation Generator

Generate or update documentation for code, APIs, and features.

## Documentation Types

### 1. API Documentation
For routes in `app/api/`:
```markdown
## Endpoint Name

**Method:** GET|POST|PUT|DELETE
**Path:** `/api/v1/resource`
**Auth:** Required|Optional (role requirements)

### Request
- Headers
- Query parameters
- Body schema (with Zod validation)

### Response
- Success response shape
- Error response shape
- Status codes

### Examples
curl or fetch examples
```

### 2. Component Documentation
For React components:
```markdown
## ComponentName

Brief description of purpose

### Props
| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|

### Usage
Code example

### Variants
Different configurations

### Accessibility
ARIA roles, keyboard interactions
```

### 3. Database Schema Documentation
For tables in `lib/db/schema.ts`:
```markdown
## Table: table_name

Purpose and relationships

### Columns
| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|

### Relationships
- Foreign keys
- Related tables

### Indexes
- Index definitions and purpose

### RLS/Permissions
- Access control notes (RLS disabled, app-level guards)
```

### 4. Feature Documentation
For new features:
```markdown
## Feature Name

### Overview
What it does and why

### User Stories
- As a [role], I can...

### Architecture
- Components involved
- Data flow
- State management

### Configuration
- Environment variables
- Feature flags

### Usage Guide
Step-by-step for users
```

### 5. Changelog Entry
Per AGENTS.md guidelines:
```markdown
## [Version] - YYYY-MM-DD

### Added
- New features

### Changed
- Modifications to existing functionality

### Fixed
- Bug fixes

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Security
- Security-related changes
```

## Output Locations

Per AGENTS.md:
- API references: `docs/apis/`
- PRD updates: `docs/prds/`
- Inline comments: sparingly, for non-obvious logic
- README snippets: feature-specific READMEs

## Actions

1. Analyze the code/feature to document
2. Identify the appropriate documentation type
3. Generate documentation following templates
4. Suggest file location
5. Check for existing docs to update vs. create

## Principles

- Keep docs close to code when possible
- Update docs when behavior changes
- Include examples for complex features
- Document "why" not just "what"
- Per AGENTS.md: record noteworthy updates in changelog
