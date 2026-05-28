---
title: "Frontmatter Schemas for Common Document Types"
description: "Essential YAML frontmatter templates for API docs, guides, tutorials, and reference documentation"
skill: writing-ai-docs
type: reference
created: 2025-10-20
lastUpdated: 2025-10-28
---

## Universal Core Fields (All Documents)

Every documentation file must include these fields:

```yaml
---
title: "Clear Document Title"                    # REQUIRED
description: "1-2 sentence summary"              # REQUIRED
type: api-endpoint | guide | tutorial | reference | concept  # REQUIRED
created: 2025-10-20                              # REQUIRED - ISO 8601 date
lastUpdated: 2025-10-20                          # REQUIRED - ISO 8601 date
---
```

## Optional Discovery Fields

These fields improve discoverability and help AI agents find relevant documentation based on user intent.
Add them to guides, tutorials, troubleshooting, and concept docs when they provide clear value.

```yaml
---
# ... required fields above ...

# OPTIONAL - improves discoverability
when-to-read:                    # User scenarios/contexts when this doc is relevant
  - "implementing authentication"
  - "debugging 401 errors"
  - "understanding OAuth flow"
related-to:                      # Links to related documentation
  - "api-endpoints-reference"
  - "security-best-practices"
code-references:                 # Relevant source code files
  - "src/middleware/auth.ts"
  - "src/services/oauth.ts"
---
```

**when-to-read**:
- Captures user intent and context (what problem are they solving?)
- Use action-oriented phrases: "implementing X", "debugging Y", "understanding Z"
- Keep phrases natural (how users would actually search)
- 3-5 scenarios max
- Enables fuzzy/semantic search by AI agents

**related-to**:
- Explicit links to related docs (complements automatic semantic similarity)
- Use document IDs, file paths, or titles
- Helps build documentation knowledge graph

**code-references**:
- Links conceptual docs to implementation
- Enables "show docs for this file" queries
- Use relative file paths from project root

**When to use**:
- ✅ Guides, tutorials, troubleshooting, concept explanations
- ❌ API reference (structure makes it discoverable)
- ❌ When it doesn't add value beyond title/description

## API Reference Documentation

For API endpoint documentation:

```yaml
---
title: "POST /api/v2/users"
description: "Create a new user account with email and profile information"
type: api-endpoint
method: POST
endpoint: /api/v2/users
authentication: required | optional | none
category: api-reference
tags:
  - users
  - authentication
  - rest-api
status: published | draft | deprecated
version: "2.1.0"
created: 2025-10-20
lastUpdated: 2025-10-20
---
```

**Required fields**: title, description, type, method, endpoint, created, lastUpdated

**Recommended fields**: authentication, category, tags, status, version

**Method values**: GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD

## Tutorial Documentation

For step-by-step learning tutorials:

```yaml
---
title: "Building Your First Todo App"
description: "Learn to build a complete todo application with React and TypeScript"
type: tutorial
difficulty: beginner | intermediate | advanced
duration: "30 minutes"
prerequisites:
  - Node.js 16+ installed
  - Basic understanding of React
  - Familiarity with JavaScript/TypeScript
outcomes:
  - Understand React component structure
  - Implement state management with hooks
  - Handle form inputs and validation
tags:
  - react
  - typescript
  - beginner-friendly
status: published
created: 2025-10-20
lastUpdated: 2025-10-20
# OPTIONAL - improves discoverability
when-to-read:
  - "learning React hooks for the first time"
  - "building a todo application"
  - "understanding state management basics"
related-to:
  - "react-hooks-reference"
  - "advanced-state-management-tutorial"
code-references:
  - "examples/todo-app/src/App.tsx"
---
```

**Required fields**: title, description, type, created, lastUpdated

**Recommended fields**: difficulty, duration, prerequisites, outcomes, tags

**Optional discovery fields**: when-to-read, related-to, code-references (see Optional Discovery Fields section)

**Difficulty values**: beginner, intermediate, advanced

## Guide Documentation

For task-oriented how-to guides:

```yaml
---
title: "How to Deploy to Production"
description: "Step-by-step guide for deploying your application to production environments"
type: guide
difficulty: intermediate
duration: "45 minutes"
prerequisites:
  - Completed application ready for deployment
  - Access to production servers
  - SSL certificates configured
tags:
  - deployment
  - production
  - devops
status: published
created: 2025-10-20
lastUpdated: 2025-10-20
# OPTIONAL - improves discoverability
when-to-read:
  - "deploying application to production"
  - "setting up production environment"
  - "troubleshooting deployment issues"
related-to:
  - "environment-configuration-guide"
  - "production-monitoring-setup"
code-references:
  - "deploy/production.yml"
---
```

**Required fields**: title, description, type, created, lastUpdated

**Recommended fields**: difficulty, duration, prerequisites, tags

**Optional discovery fields**: when-to-read, related-to, code-references (see Optional Discovery Fields section)

## Reference Documentation

For technical specifications and comprehensive references:

```yaml
---
title: "Configuration Options Reference"
description: "Complete reference of all configuration options and their parameters"
type: reference
category: reference
tags:
  - configuration
  - settings
  - reference
status: published
version: "3.1.0"
applicableVersions:
  - "3.x"
  - "2.9+"
created: 2025-10-20
lastUpdated: 2025-10-20
---
```

**Required fields**: title, description, type, created, lastUpdated

**Recommended fields**: version, applicableVersions, category, tags

## Conceptual Documentation

For explaining architecture and design decisions:

```yaml
---
title: "Understanding OAuth 2.0 Authentication Flow"
description: "Conceptual overview of OAuth 2.0 authentication and how it works in our system"
type: concept
category: explanation
audience: developers | architects | decision-makers
tags:
  - authentication
  - security
  - oauth
  - architecture
status: published
created: 2025-10-20
lastUpdated: 2025-10-20
# OPTIONAL - improves discoverability
when-to-read:
  - "understanding OAuth 2.0 flow"
  - "deciding on authentication strategy"
  - "designing secure API authentication"
related-to:
  - "api-authentication-guide"
  - "security-best-practices"
code-references:
  - "src/middleware/oauth.ts"
---
```

**Required fields**: title, description, type, created, lastUpdated

**Recommended fields**: audience, category, tags

**Optional discovery fields**: when-to-read, related-to, code-references (see Optional Discovery Fields section)

## Troubleshooting Documentation

For problem-solving and error resolution:

```yaml
---
title: "Troubleshooting Authentication Errors"
description: "Common authentication errors and their solutions"
type: troubleshooting
category: troubleshooting
applies_to:
  - version: ">=2.0.0"
  - platform: all
common_errors:
  - error_code: ERR_AUTH_FAILED
  - error_code: ERR_INVALID_TOKEN
tags:
  - troubleshooting
  - authentication
  - errors
status: published
created: 2025-10-20
lastUpdated: 2025-10-20
# OPTIONAL - improves discoverability
when-to-read:
  - "seeing ERR_AUTH_FAILED error"
  - "experiencing authentication failures"
  - "debugging 401/403 responses"
related-to:
  - "authentication-guide"
  - "oauth-concept-explanation"
code-references:
  - "src/middleware/auth.ts"
---
```

**Required fields**: title, description, type, created, lastUpdated

**Recommended fields**: applies_to, common_errors, category, tags

**Optional discovery fields**: when-to-read, related-to, code-references (see Optional Discovery Fields section)

## Field Guidelines

### Required Fields Explanation

**title**:

- Keep under 60-70 characters
- Be specific and descriptive
- Should match H1 heading in document body

**description**:

- 1-2 sentences (100-200 characters ideal)
- Focus on what and why
- Include key searchable terms
- Avoid generic phrases like "This document describes..."

**type**:

- Determines document structure and AI context
- Use standard values: `api-endpoint`, `guide`, `tutorial`, `reference`, `concept`, `troubleshooting`
- Consistent typing improves AI categorization

**created**:

- ISO 8601 format: YYYY-MM-DD
- Set once when document is first created
- Never change this date

**lastUpdated**:

- ISO 8601 format: YYYY-MM-DD
- Update whenever document content changes
- Helps users and AI understand content freshness

### Optional But Recommended Fields

**tags**:

- Use 3-7 relevant tags
- Lowercase, hyphen-separated
- Mix specific and general terms
- Include difficulty level for tutorials/guides

**status**:

- `published` - Ready for public consumption
- `draft` - Work in progress
- `deprecated` - Outdated, kept for reference

**version**:

- Semantic versioning (e.g., "2.1.0")
- Indicates which product version the documentation applies to

**difficulty**:

- For tutorials and guides only
- Values: `beginner`, `intermediate`, `advanced`
- Helps users assess if content matches their level

**duration**:

- For tutorials and guides only
- Estimated completion time (e.g., "15 minutes", "1 hour")
- Helps users plan their time

**prerequisites**:

- List of requirements before starting
- Be explicit with versions (e.g., "Node.js 16+")
- Include links to setup guides when applicable

## Common Mistakes

### ❌ Missing Required Fields

```yaml
---
title: "API Documentation"
# Missing: description, type, created, lastUpdated
---
```

### ❌ Vague Description

```yaml
---
description: "This document describes the API"  # Too generic
---
```

### ✅ Specific Description

```yaml
---
description: "Complete reference for the Users API including authentication, CRUD operations, and error handling"
---
```

### ❌ Inconsistent Dates

```yaml
---
created: "October 20, 2025"      # Wrong format
lastUpdated: 2025-10-20          # Correct format
---
```

### ✅ Consistent ISO 8601 Dates

```yaml
---
created: 2025-10-20
lastUpdated: 2025-10-20
---
```

### ❌ Too Many Tags

```yaml
---
tags: [api, rest, authentication, oauth, jwt, tokens, security, users, endpoints, http, requests, responses, json, documentation]
# 14 tags - too many
---
```

### ✅ Focused Tags

```yaml
---
tags: [api, authentication, oauth, rest-api, beginner-friendly]
# 5 tags - focused and relevant
---
```

## Validation

Frontmatter validation is handled by the maintaining-docs skill, which provides comprehensive documentation structure validation including:

- Required fields are present and non-empty
- YAML syntax is valid
- Date formats are ISO 8601
- Field values are in allowed ranges
- Document type specific requirements met

For single-file quality checks, use:

```bash
python scripts/check_doc_quality.py path/to/your-doc.md
```

For full documentation structure and frontmatter validation across your entire docs folder, invoke the maintaining-docs skill with `Skill(command='maintaining-docs')`
