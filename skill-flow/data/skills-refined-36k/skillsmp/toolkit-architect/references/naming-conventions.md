# Naming Conventions

## Table of Contents

- [Overview](#overview)
- [General Rules](#general-rules)
- [Component-Specific Naming](#component-specific-naming)
- [Cross-Component Consistency](#cross-component-consistency)
- [Naming Anti-Patterns](#naming-anti-patterns)
- [File Extension Guidelines](#file-extension-guidelines)
- [Version-Specific Naming](#version-specific-naming)
- [Best Practices Checklist](#best-practices-checklist)
- [Migration from Legacy Naming](#migration-from-legacy-naming)
- [Quick Reference Table](#quick-reference-table)
- [Examples by Plugin Type](#examples-by-plugin-type)

## Overview

Consistent, descriptive naming is crucial for maintainable plugins. Follow these conventions across all plugin components.

## General Rules

### Kebab-Case Required
All directories, files, and component names MUST use kebab-case:
- Lowercase letters
- Hyphens between words
- No spaces or underscores
- No special characters

**Examples:**
- ✅ Good: `code-review`, `api-testing`, `user-authentication`
- ❌ Bad: `codeReview`, `API_testing`, `user auth`

### Length Guidelines
- **Component names**: 2-4 words (15-30 characters)
- **Skill directories**: 2-3 words (10-25 characters)
- **Command files**: 2-3 words (10-25 characters)
- **Agent files**: 2-4 words (12-30 characters)
- **Script files**: 2-5 words (10-35 characters)

## Component-Specific Naming

### Plugin Name

**Format**: `kebab-case` (lowercase with hyphens)

**Requirements:**
- Unique across installed plugins
- Descriptive of plugin purpose
- Professional appearance
- 2-5 words maximum

**Examples:**
- `code-review-assistant`
- `test-runner`
- `api-docs-generator`
- `database-migrator`

**Avoid:**
- Generic names: `my-plugin`, `tool`
- Brand-specific: `company-name-plugin`
- Technical jargon: `orm-helper`

### Skills

**Directory format**: `kebab-case` directories

**Naming guidelines:**
- Topic-focused (what the skill does)
- Action-oriented (imperative or noun form)
- Clear value proposition

**Examples:**
- ✅ Good: `api-testing`, `database-migrations`, `error-handling`
- ✅ Good: `code-review`, `test-generation`, `performance-analysis`
- ❌ Bad: `utilities`, `helpers`, `misc`

**Skill file**: All skills MUST have `SKILL.md` (exact name)

### Commands

**File format**: `kebab-case.md` files

**Naming guidelines:**
- Action-oriented (what the command does)
- User-friendly (what user would type)
- Concise but descriptive

**Mapping**: File name becomes slash command
- `code-review.md` → `/code-review`
- `run-tests.md` → `/run-tests`
- `generate-docs.md` → `/generate-docs`

**Examples:**
- ✅ Good: `review-pr`, `run-tests`, `deploy-app`, `sync-data`
- ❌ Bad: `review-pull-request`, `execute-test-suite`

### Agents

**File format**: `kebab-case.md` files

**Naming guidelines:**
- Role-oriented (what the agent is)
- Professional tone
- Domain expertise indicated

**Examples:**
- ✅ Good: `code-reviewer`, `test-generator`, `security-analyzer`
- ✅ Good: `database-specialist`, `performance-consultant`
- ❌ Bad: `helper`, `tool`, `worker`

### Hooks

**Configuration file**: `hooks.json` (exact name)

**Script naming**: `kebab-case` with appropriate extensions

**Guidelines:**
- Action-oriented
- Clear purpose

**Examples:**
- ✅ Good: `validate-input.sh`, `check-style.sh`, `setup-environment.sh`
- ✅ Good: `format-code.py`, `lint-files.js`

### MCP Servers

**Server name**: `kebab-case` identifier

**Naming guidelines:**
- Service-oriented
- Clear external reference

**Examples:**
- ✅ Good: `asana-api`, `github-issues`, `stripe-payments`
- ✅ Good: `database-connection`, `file-system`

### Supporting Files

#### Scripts

**Naming**: `kebab-case` with appropriate extensions

**Guidelines:**
- Descriptive of script purpose
- Action-oriented

**Examples by type:**

**Bash scripts**:
- `validate-input.sh`
- `run-tests.sh`
- `deploy-app.sh`
- `setup-environment.sh`

**Python scripts**:
- `generate-report.py`
- `process-data.py`
- `sync-database.py`
- `analyze-logs.py`

**Node.js scripts**:
- `compile-assets.js`
- `watch-files.js`
- `build-package.js`

**Configuration files**:
- `hooks.json`
- `.mcp.json`
- `plugin.json`

#### Documentation

**Naming**: `kebab-case.md` files

**Guidelines:**
- Purpose-oriented
- User-friendly

**Examples:**
- `api-reference.md`
- `migration-guide.md`
- `best-practices.md`
- `troubleshooting.md`
- `examples.md`

#### Reference Directories

**Naming**: `references`, `examples`, `scripts` (exact names)

These directories have fixed names:
- `references/` - Detailed documentation
- `examples/` - Working code examples
- `scripts/` - Utility scripts

## Cross-Component Consistency

### Related Components

When components work together, use consistent naming:

**Example 1: Test workflow**
```
skills/
└── test-generation/
commands/
└── run-tests.sh     ← References "test-generation"
agents/
└── test-validator.sh  ← References "test"
```

**Example 2: Code review**
```
skills/
└── code-review/
commands/
└── review-pr.sh      ← References "code-review"
agents/
└── code-analyzer.sh  ← References "code"
```

### Namespace Strategy

For complex plugins, use namespaces:

**Without namespace** (simple plugin):
```
my-plugin/
├── skills/
│   └── api-testing/
└── commands/
    └── run-api-tests/
```

**With namespace** (complex plugin):
```
my-plugin/
├── skills/
│   ├── api-testing/
│   └── db-validation/
└── commands/
    ├── api-run-tests/
    └── db-verify-data/
```

## Naming Anti-Patterns

### Generic Names
❌ Avoid:
- `utils/`
- `helpers/`
- `misc/`
- `tools/`
- `common/`

✅ Use instead:
- `file-operations/`
- `data-validation/`
- `configuration-management/`

### Technical Jargon
❌ Avoid:
- `orm-helper/`
- `oauth-authenticator/`
- `rest-api-client/`

✅ Use instead:
- `database-integration/`
- `user-authentication/`
- `api-integration/`

### Inconsistent Styles
❌ Avoid:
- `api_testing/` (underscore)
- `CodeReview/` (camelCase)
- `test-generation` (hyphen in skill name)

✅ Use:
- `api-testing/` (kebab-case throughout)

### Overly Generic
❌ Avoid:
- `my-plugin/`
- `test-plugin/`
- `tool/`

✅ Use:
- `code-quality-analyzer/`
- `api-test-runner/`
- `deployment-automation/`

## File Extension Guidelines

### Markdown Files
- `.md` - All documentation and component files
- Examples: `README.md`, `SKILL.md`, `command.md`

### Script Files
- `.sh` - Bash shell scripts
- `.py` - Python scripts
- `.js` - Node.js scripts
- `.ts` - TypeScript scripts

### Configuration Files
- `.json` - JSON configuration
- `.yaml` or `.yml` - YAML configuration

### Data Files
- `.sql` - SQL scripts
- `.csv` - CSV data
- `.xml` - XML data

## Version-Specific Naming

### Skill Versions
Skills support version field in frontmatter:
```markdown
---
name: skill-name
version: 1.0.0  # Semantic versioning
---
```

### Plugin Versions
Plugin version in `plugin.json`:
```json
{
  "name": "plugin-name",
  "version": "1.0.0"  # Semantic versioning
}
```

### MCP Server Versions
2026 date-based versioning:
```json
{
  "server-name": {
    "version": "2026-01-20"  # Date-based versioning
  }
}
```

## Best Practices Checklist

- [ ] All names use kebab-case
- [ ] Names are descriptive and purpose-focused
- [ ] Length is appropriate (2-5 words)
- [ ] Consistent naming across related components
- [ ] No generic or technical jargon names
- [ ] Correct file extensions used
- [ ] Proper versioning format applied
- [ ] Professional and user-friendly

## Migration from Legacy Naming

If migrating from non-standard naming:

1. **Audit current names**: List all files/directories
2. **Identify patterns**: Find inconsistencies
3. **Plan migration**: Map old names to new names
4. **Update references**: Update all internal references
5. **Test thoroughly**: Verify all components work
6. **Document changes**: Note breaking changes

## Quick Reference Table

| Component Type | Format | Example | Command/Usage |
|---------------|--------|---------|---------------|
| Plugin | kebab-case | `code-review-assistant` | N/A |
| Skill directory | kebab-case | `api-testing/` | Auto-discovery |
| Skill file | SKILL.md | `SKILL.md` | Required name |
| Command | kebab-case.md | `run-tests.md` | `/run-tests` |
| Agent | kebab-case.md | `code-reviewer.md` | Manual invoke |
| Hook config | hooks.json | `hooks.json` | Event-driven |
| MCP server | kebab-case | `asana-api` | Tool access |
| Scripts | kebab-case.ext | `validate-input.sh` | Called by components |

## Examples by Plugin Type

### Testing Plugin
```
testing-plugin/
├── skills/
│   ├── test-generation/
│   └── coverage-analysis/
├── commands/
│   └── run-tests/
├── agents/
│   ├── test-validator/
│   └── coverage-reporter/
└── hooks/
    └── hooks.json
```

### API Documentation Plugin
```
api-docs-plugin/
├── skills/
│   ├── openapi-parser/
│   └── doc-generation/
├── commands/
│   ├── generate-docs/
│   └── update-api-ref/
├── agents/
│   ├── spec-validator/
│   └── content-reviewer/
└── .mcp.json
```

### Database Plugin
```
db-tools-plugin/
├── skills/
│   ├── migration-manager/
│   └── query-builder/
├── commands/
│   ├── run-migrations/
│   └── backup-database/
├── agents/
│   ├── schema-analyzer/
│   └── data-validator/
└── scripts/
    ├── setup-connection.sh
    └── export-data.sh
```
