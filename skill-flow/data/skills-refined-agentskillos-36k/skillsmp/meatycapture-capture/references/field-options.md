# Field Options Reference

Complete catalog of valid field values for MeatyCapture request-log items. This reference provides the full set of options for each field, including global defaults and project-specific customizations.

## Field Catalog

### type (Required)

Item classification determining workflow and prioritization.

| Value | Description | Use When |
|-------|-------------|----------|
| `enhancement` | New feature or improvement to existing functionality | Proposing new capabilities, UX improvements, feature extensions |
| `bug` | Defect, error, or incorrect behavior | Code crashes, incorrect output, validation failures, edge cases |
| `idea` | Exploratory concept or future consideration | Brainstorming, research topics, architectural possibilities |
| `task` | Actionable work item (non-bug, non-feature) | Refactoring, documentation, testing, configuration, cleanup |
| `question` | Open question requiring investigation or decision | Architectural decisions, technology choices, clarifications |

**Default**: None (must be specified)

**Examples**:
- Bug: "Serializer crashes on null item fields"
- Enhancement: "Add keyboard shortcuts for wizard navigation"
- Idea: "Explore GraphQL API for query flexibility"
- Task: "Add unit tests for tag aggregation"
- Question: "Should we support YAML in addition to JSON config?"

---

### domain (Required)

Technical domain or system component affected by the item.

**Format**: Array of strings (e.g., `["web"]`, `["api", "core"]`)

#### Global Domains

| Value | Description | Typical Components |
|-------|-------------|-------------------|
| `core` | Headless domain logic (UI-agnostic) | models, validation, serializer, ports |
| `web` | React web UI components | wizard, admin, shared components |
| `api` | Backend API and services | REST endpoints, GraphQL resolvers, webhooks |
| `cli` | Command-line interface | CLI commands, argument parsing, output formatting |
| `mobile` | Mobile app (iOS/Android) | Native components, mobile-specific logic |
| `desktop` | Desktop app (Tauri/Electron) | Window management, native integrations |
| `adapters` | Port implementations | fs-local, config-local, remote storage |
| `docs` | Documentation | README, guides, API docs, tutorials |
| `testing` | Test infrastructure | Unit tests, integration tests, E2E tests |
| `devops` | Build, deployment, CI/CD | Docker, GitHub Actions, deployment scripts |
| `security` | Security-related concerns | Authentication, authorization, input validation |
| `performance` | Performance optimization | Profiling, caching, query optimization |

#### Project-Specific Domains

Projects may define additional domains in their field catalogs:

**MeatyCapture Project**:
- `serializer` - Request-log markdown serialization
- `wizard` - Multi-step capture wizard
- `field-manager` - Field catalog administration

**Default**: None (must be specified)

**Best Practice**: Use global domains when possible. Create project-specific domains only when global domains don't capture the component accurately.

---

### subdomain (Required)

Sub-categorization within the domain for finer-grained filtering and organization.

**Format**: Array of strings (e.g., `["discovery"]`, `["bulk-import"]`)

**Examples**:
- `["discovery"]` - Discovery feature area
- `["bulk-import"]` - Bulk import functionality
- `["user-facing"]` - User-visible features
- `["validation"]` - Input validation subsystem
- `["auth", "jwt"]` - Multiple sub-areas (authentication with JWT focus)

**Default**: None (must be specified)

**Best Practice**: Use subdomain to narrow scope within the broader domain. Helps with filtering, search, and organizing related items.

---

### context (Optional)

Specific module, component, or sub-domain providing additional context.

**Format**: Free-form string, typically module name or component identifier.

**Examples**:
- `serializer` - Within core domain
- `wizard/step-3` - Specific wizard step
- `DocStore` - Interface name
- `fs-local/backup` - Adapter subsystem
- `auth/jwt` - Authentication module
- `api/v1/projects` - API endpoint

**Default**: Empty string

**Best Practice**: Use context to narrow scope within broader domain. Helps with filtering and search.

---

### priority (Optional)

Urgency and impact level determining work scheduling.

| Value | Description | Response Time | Examples |
|-------|-------------|---------------|----------|
| `critical` | Immediate action required | Hours | Security vulnerabilities, data corruption, system crashes, production outages |
| `high` | Significant impact, near-term fix | Days | User-facing bugs, broken core features, blocking issues |
| `medium` | Moderate impact, schedule appropriately | Weeks | Minor bugs, enhancements, technical debt, non-blocking issues |
| `low` | Minimal impact, address when convenient | Months | Polish, nice-to-haves, future ideas, cosmetic issues |

**Default**: `medium`

**Guidelines**:
- **critical**: Affects security, data integrity, or core functionality for all users
- **high**: Impacts significant user workflows or blocks development
- **medium**: Worthwhile improvements with moderate user/developer impact
- **low**: Would be nice but not essential for product success

**Best Practice**: Reserve `critical` for true emergencies. Over-prioritizing dilutes meaning.

---

### status (Optional)

Current state in item lifecycle.

| Value | Description | Next Action | Who |
|-------|-------------|-------------|-----|
| `triage` | Newly captured, awaiting review | Validate, prioritize, assign | Product/Tech Lead |
| `backlog` | Reviewed and accepted, not yet scheduled | Add to sprint, estimate effort | Product Manager |
| `planned` | Scheduled for upcoming sprint/milestone | Begin implementation | Developer |
| `in-progress` | Actively being worked on | Complete implementation, test | Developer |
| `done` | Completed and verified | Close, document, deploy | Team |
| `wontfix` | Reviewed and declined | Archive, document reason | Product/Tech Lead |

**Default**: `triage`

**Workflow**:

```
triage → backlog → planned → in-progress → done
   ↓
wontfix
```

**Best Practice**: AI agents typically create items in `triage` status. Human review moves to `backlog` or `wontfix`.

---

### tags (Optional)

Free-form metadata for categorization, filtering, and search.

**Format**: Array of lowercase, hyphenated strings.

**Tag Categories**:

#### Technical Tags
- `async`, `concurrency`, `caching`, `optimization`
- `validation`, `error-handling`, `logging`
- `file-io`, `network`, `database`
- `typescript`, `react`, `node`

#### Functional Tags
- `security`, `performance`, `accessibility`, `ux`
- `testing`, `documentation`, `refactoring`
- `api`, `cli`, `web`, `mobile`

#### Process Tags
- `code-review`, `tech-debt`, `breaking-change`
- `needs-discussion`, `blocked`, `help-wanted`

#### Domain Tags
- `tags`, `wizard`, `serializer`, `fields`
- `projects`, `documents`, `items`

**Default**: Empty array `[]`

**Tag Aggregation**: When items are added to a document, their tags are automatically merged into the document's frontmatter `tags` array (unique, sorted).

**Best Practices**:
- 2-5 tags per item (focused)
- Use existing tags when possible (consistency)
- Lowercase with hyphens: `input-validation` not `InputValidation`
- Specific over generic: `tag-aggregation` better than `tags`

**Examples**:

```json
"tags": ["security", "input-validation", "injection"]
"tags": ["performance", "caching", "optimization"]
"tags": ["ux", "accessibility", "keyboard-nav"]
"tags": ["testing", "unit-tests", "edge-case"]
```

---

### notes (Optional)

Detailed description as an array of note strings.

**Format**: Array of strings. Each string becomes a separate note entry with timestamp.

**Recommended Structure** (use separate array elements for Problem/Goal):

```json
"notes": [
  "Problem: Validation logic duplicated across 3 components.",
  "Goal: Extract to shared validator utility with unit tests."
]
```

**With Additional Context**:

```json
"notes": [
  "Problem: Tag aggregation fails on Unicode characters.",
  "Goal: Use locale-aware sorting for tag lists.",
  "Context: Discovered during i18n testing. Related to REQ-20251228-project-03."
]
```

**Default**: Empty array `[]`

**Best Practices**:

1. **Separate Problem/Goal** into distinct array elements for clarity
2. **Include Context** as additional array elements:
   - File/line references: `"Found in serializer.ts:87"`
   - Related items: `"Related to REQ-20251228-meatycapture-05"`
   - Stack traces, error messages
3. **Keep each note focused** - one concept per string
4. **Use markdown within notes** - each string supports full markdown

**Example with multiple notes**:

```json
"notes": [
  "Problem: Tag aggregation fails when items array is empty.",
  "Goal: Handle empty arrays gracefully, return empty tags array.",
  "Found in serializer.ts:87",
  "Related to REQ-20251228-meatycapture-05"
]
```

---

## Field Validation Rules

### Required Fields

All items **must** include:
- `title` (string, 1-200 characters)
- `type` (enum: enhancement, bug, idea, task, question)
- `domain` (array of strings, e.g., `["web"]`)
- `subdomain` (array of strings, e.g., `["discovery"]`)

### Optional Fields

May be omitted (defaults apply):
- `context` (string, default: "")
- `priority` (enum: low, medium, high, critical, default: medium)
- `status` (enum: triage, backlog, planned, in-progress, done, wontfix, default: triage)
- `tags` (array of strings, default: [])
- `notes` (array of strings, default: [])

### Validation Constraints

| Field | Type | Pattern | Notes |
|-------|------|---------|-------|
| `title` | string | 1-200 chars | Concise, descriptive |
| `type` | enum | One of 5 values | enhancement, bug, idea, task, question |
| `domain` | array | `["value", ...]` | Each value: `[a-z0-9-/]+` |
| `subdomain` | array | `["value", ...]` | Each value: `[a-z0-9-/]+` |
| `context` | string | 0-100 chars | Empty allowed |
| `priority` | enum | One of 4 values | low, medium, high, critical |
| `status` | enum | One of 6 values | triage, backlog, planned, in-progress, done, wontfix |
| `tags` | array | `["tag", ...]` | Each tag: `[a-z0-9-]+` |
| `notes` | array | `["note", ...]` | Each note: markdown string |

---

## Project-Specific Customization

Projects can extend global field catalogs with project-specific options.

### Configuration File

**Location**: `~/.meatycapture/fields.json`

**Structure**:

```json
{
  "global": {
    "type": ["enhancement", "bug", "idea", "task", "question"],
    "priority": ["low", "medium", "high", "critical"],
    "status": ["triage", "backlog", "planned", "in-progress", "done", "wontfix"]
  },
  "projects": {
    "meatycapture": {
      "domain": ["core", "web", "cli", "adapters", "serializer", "wizard"],
      "tags": ["tags", "wizard", "serializer", "fields", "projects"]
    },
    "another-project": {
      "domain": ["api", "web", "mobile"],
      "tags": ["auth", "payments", "notifications"]
    }
  }
}
```

### Effective Options

When capturing items, effective field options = global + project-specific.

**Example**: For `meatycapture` project:
- `domain` options: All global domains + `serializer`, `wizard`
- `type` options: Global only (project didn't override)
- `tags`: Project-specific are suggestions, but any tag allowed

---

## CLI Field Validation

The MeatyCapture CLI validates fields before writing:

### Validation Errors

```bash
# Invalid type
echo '{"project":"xyz","items":[{"title":"Test","type":"feature","domain":"web"}]}' | meatycapture log create --json

# Error response:
{
  "success": false,
  "error": "Validation failed",
  "details": {
    "field": "type",
    "value": "feature",
    "allowed": ["enhancement", "bug", "idea", "task", "question"]
  }
}
```

### Validation Warnings

Non-critical issues that allow capture but suggest improvements:

```bash
# Unknown domain (not in catalog)
echo '{"project":"xyz","items":[{"title":"Test","type":"bug","domain":"unknown-domain"}]}' | meatycapture log create --json

# Success with warning:
{
  "success": true,
  "doc_id": "REQ-20251229-xyz",
  "warnings": [{
    "field": "domain",
    "message": "Domain 'unknown-domain' not in project catalog. Consider using existing domain or adding to fields.json"
  }]
}
```

---

## Examples by Use Case

### Security Bug

```json
{
  "title": "SQL injection in project search endpoint",
  "type": "bug",
  "domain": ["api"],
  "subdomain": ["security"],
  "context": "projects/search",
  "priority": "critical",
  "status": "triage",
  "tags": ["security", "sql-injection", "api", "input-validation"],
  "notes": [
    "Problem: User input not sanitized in /api/projects/search?q={query}. Direct string interpolation allows SQL injection.",
    "Goal: Use parameterized queries, add input validation.",
    "Severity: High - allows data exfiltration."
  ]
}
```

### Performance Enhancement

```json
{
  "title": "Cache aggregated tags to improve append performance",
  "type": "enhancement",
  "domain": ["core"],
  "subdomain": ["serializer"],
  "context": "serializer/tags",
  "priority": "medium",
  "status": "backlog",
  "tags": ["performance", "caching", "tags", "optimization"],
  "notes": [
    "Goal: Reduce tag aggregation time on append by caching results.",
    "Current: 200ms to re-aggregate 1000 item tags on every append.",
    "Proposed: Cache aggregated tags, invalidate on item changes.",
    "Benefit: 95% reduction in append latency for large documents."
  ]
}
```

### Documentation Task

```json
{
  "title": "Document request-log format specification",
  "type": "task",
  "domain": ["docs"],
  "subdomain": ["specification"],
  "priority": "high",
  "status": "planned",
  "tags": ["documentation", "specification", "request-log"],
  "notes": [
    "Goal: Create comprehensive spec for request-log markdown format.",
    "Sections: YAML frontmatter fields, Item structure, ID generation rules, Tag aggregation behavior, Backup strategy",
    "Target: docs/specs/request-log-format.md"
  ]
}
```

### Research Question

```json
{
  "title": "Should we support remote storage backends?",
  "type": "question",
  "domain": ["adapters"],
  "subdomain": ["architecture"],
  "context": "architecture",
  "priority": "low",
  "status": "triage",
  "tags": ["architecture", "storage", "cloud", "needs-discussion"],
  "notes": [
    "Question: Is local file storage sufficient, or should we support S3/GCS/etc?",
    "Pros (remote storage): Team collaboration, Backup/sync automatic, Access from multiple devices",
    "Cons: Complexity, Auth/permissions, Latency",
    "MVP Decision: File-first, defer remote until proven need."
  ]
}
```

---

## Reference

- **Main Skill**: `../SKILL.md`
- **JSON Schemas**: `./json-schemas.md`
- **Templates**: `../templates/`
- **MeatyCapture Docs**: `../../../../docs/`
