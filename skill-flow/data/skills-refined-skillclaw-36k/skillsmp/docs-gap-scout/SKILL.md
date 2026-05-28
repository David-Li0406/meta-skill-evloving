---
name: docs-gap-scout
description: Identify documentation that may need updates based on planned changes. Use when planning a feature to identify which docs (README, CHANGELOG, API docs) will need updates after implementation.
---

# Docs Gap Scout

Documentation gap scout to identify which docs may need updates when a feature is implemented.

**Role**: Doc update identifier
**Purpose**: Find which documentation needs updating for a change
**Speed**: Fast - quick scan, do not read full docs

## Tool Requirements

**Required tools**: Glob, Read

**Degradation strategy** (if tools unavailable):
```
File tools not available. Please check manually:

1. User-facing docs:
   ls README* CHANGELOG* CONTRIBUTING*
   ls docs/ documentation/

2. API docs:
   ls openapi.* swagger.* api-docs/
   find . -name "*.openapi.yaml" -o -name "*.swagger.json"

3. Architecture docs:
   ls adr/ adrs/ decisions/ architecture/

4. Component docs:
   ls .storybook/ stories/
```

## Input

You receive:
- `REQUEST` - the feature/change being planned

## Process

### 1. Scan for doc locations

Look for common documentation patterns:

```bash
# User-facing docs
ls -la README* CHANGELOG* CONTRIBUTING* 2>/dev/null
ls -la docs/ documentation/ 2>/dev/null
ls -la website/ site/ pages/ 2>/dev/null

# API docs
ls -la openapi.* swagger.* api-docs/ 2>/dev/null
find . -name "*.openapi.yaml" -o -name "*.swagger.json" 2>/dev/null | head -5

# Component docs
ls -la .storybook/ stories/ 2>/dev/null

# Architecture
ls -la adr/ adrs/ decisions/ architecture/ 2>/dev/null

# Generated docs
ls -la typedoc.json jsdoc.json mkdocs.yml 2>/dev/null
```

### 2. Categorize what exists

Build a map:
- **User docs**: README, docs site, getting started guides
- **API docs**: OpenAPI specs, endpoint documentation
- **Component docs**: Storybook, component library docs
- **Architecture**: ADRs, design docs
- **Changelog**: CHANGELOG.md or similar

### 3. Match request to docs

Based on the REQUEST, identify which docs likely need updates:

| Change Type | Likely Doc Updates |
|-------------|-------------------|
| New feature | README usage, CHANGELOG |
| New API endpoint | API docs, README if public |
| New component | Storybook story, component docs |
| Config change | README config section |
| Breaking change | CHANGELOG, migration guide |
| Architectural decision | ADR |
| CLI change | README CLI section, --help text |

### 4. Check current doc state

For identified docs, quick scan to understand structure:
- Does README have a usage section?
- Does API doc cover related endpoints?
- Are there existing ADRs to follow as template?

## Output Format

```markdown
## Documentation Gap Analysis

### Doc Locations Found
- README.md (has: installation, usage, API sections)
- docs/ (mkdocs site with guides)
- CHANGELOG.md (keep-a-changelog format)
- openapi.yaml (API spec)

### Likely Updates Needed
- **README.md**: Update usage section for new feature
- **CHANGELOG.md**: Add entry under "Added"
- **openapi.yaml**: Add new /auth endpoint spec

### No Updates Expected
- Storybook (no UI components in this change)
- ADR (no architectural decisions)

### Templates/Patterns to Follow
- CHANGELOG uses keep-a-changelog format
- ADRs follow MADR template in adr/
```

If no docs found or no updates needed:
```markdown
## Documentation Gap Analysis

No documentation updates identified for this change.
- No user-facing docs found in repo
- Change is internal/refactor only
```

## Rules

- Speed over completeness - quick scan, do not read full docs
- Only flag docs that genuinely relate to the change
- Do not flag CHANGELOG for every change - only user-visible ones
- Note doc structure/templates so implementer can follow patterns
- If uncertain, err on side of flagging (implementer can skip if not needed)

## Verification

````bash
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
if [ -z "$REPO_ROOT" ]; then
  echo "Error: Set REPO_ROOT=/absolute/path/to/repo"
  exit 1
fi

ls "$REPO_ROOT/.factory/skills/docs-gap-scout/SKILL.md"
# Expected: file exists, exit code 0
````
