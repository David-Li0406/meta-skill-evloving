---
name: SPECLAN Query
description: This skill should be used when querying SPECLAN specifications by type, status, or parent relationship. Use when user asks to "list features", "find requirements", "show approved specs", "get children of feature", "index specs", or needs to search/filter SPECLAN entities programmatically.
version: 0.1.0
context: fork
---

# SPECLAN Query

Fast, flexible querying of SPECLAN entities with JSON output. Query by type, filter by status or parent, with optional full metadata extraction.

## Why Use This Skill

- **Fast**: Filename-based parsing without reading files (unless filters require it)
- **Reliable**: Uses `{PREFIX}-{ID}-{slug}` naming pattern as source of truth
- **Flexible**: Query any entity type, filter by status/parent
- **Structured**: Clean JSON output for programmatic consumption
- **zsh-safe**: Avoids reserved word conflicts (uses `entity_status` not `status`)

## Entity Types

| Type | Prefix | Pattern | Location |
|------|--------|---------|----------|
| goal | G- | G-###-*.md | goals/ |
| feature | F- | F-####-*.md | features/ (recursive) |
| requirement | R- | R-####-*.md | features/.../requirements/ |
| scenario | S- | S-####-*.md | features/.../scenarios/ |
| acceptance-criterion | AC- | AC-####-*.md | features/.../acceptance-criteria/ |
| test | T- | T-####-*.md | features/.../tests/ |
| change-request | CR- | CR-####-*.md | Anywhere in change-requests/ |

## Usage

### Script Location

```
${PLUGIN_ROOT}/skills/speclan-query/scripts/query.sh
```

### Command Line

```bash
./query.sh [OPTIONS] [speclan-dir]
```

**Options:**
- `-t, --type TYPE` - Entity type to query (required)
- `-s, --filter-status STATUS` - Filter by status (draft|review|approved|in-development|under-test|released|deprecated)
- `-p, --parent ID` - Filter by parent ID (e.g., F-1234)
- `-f, --full` - Include title and status in output (reads frontmatter)
- `-h, --help` - Show usage

**Arguments:**
- `speclan-dir` - Path to speclan directory (default: ./speclan)

**Output:**
- JSON array to stdout
- Errors to stderr
- Exit code: 0 = success, 1 = error

## Examples

### List all features (fast - filename only)

```bash
./query.sh --type feature speclan
```

Output:
```json
[
  {"id":"F-1049","slug":"pet-management","type":"feature","path":"speclan/features/F-1049-pet-management/F-1049-pet-management.md"},
  {"id":"F-2847","slug":"user-auth","type":"feature","path":"speclan/features/F-2847-user-auth/F-2847-user-auth.md"}
]
```

### List features with full details

```bash
./query.sh --type feature --full speclan
```

Output:
```json
[
  {"id":"F-1049","slug":"pet-management","type":"feature","path":"...","title":"Pet Management","status":"draft"},
  {"id":"F-2847","slug":"user-auth","type":"feature","path":"...","title":"User Authentication","status":"approved"}
]
```

### Filter by status

```bash
./query.sh --type feature --filter-status approved speclan
```

### Find requirements for a feature

```bash
./query.sh --type requirement --parent F-1049 speclan
```

### Find change-requests for a requirement

```bash
./query.sh --type change-request --parent R-2046 speclan
```

### Combine filters

```bash
./query.sh --type requirement --parent F-1049 --filter-status approved --full speclan
```

### Query all entity types

```bash
./query.sh --type all speclan
```

## Query Modes

### Fast Mode (Default)

Only parses filenames, no file content read:
- Extracts ID and slug from filename pattern
- Infers type from ID prefix
- Fastest for simple listing

**Activated when:** No `--full`, `--filter-status`, or `--parent` flags

### Full Mode (Frontmatter Read)

Reads YAML frontmatter when needed:
- Extract title, status from frontmatter
- Required for filtering or full output

**Activated when:** `--full`, `--filter-status`, or `--parent` specified

## JSON Output Schema

### Minimal (fast mode)

```json
{
  "id": "F-1049",
  "slug": "pet-management",
  "type": "feature",
  "path": "speclan/features/F-1049-pet-management/F-1049-pet-management.md"
}
```

### Full (with --full flag)

```json
{
  "id": "F-1049",
  "slug": "pet-management",
  "type": "feature",
  "path": "speclan/...",
  "title": "Pet Management",
  "status": "draft"
}
```

## Parent Filtering

The `--parent` flag checks multiple locations:

1. **Structural parent** - ID appears in file path (e.g., `F-1049-slug/requirements/R-2046-slug/`)
2. **Frontmatter fields** - `feature:`, `requirement:`, `parentId:`
3. **Array fields** - Goals array (`- G-123`)

## Integration Examples

### In sync-from-session Command

```bash
# Index existing features
FEATURES_JSON=$("${PLUGIN_ROOT}/skills/speclan-query/scripts/query.sh" --type feature --full speclan)

# Check if feature exists
if echo "$FEATURES_JSON" | grep -q '"id":"F-1049"'; then
  echo "Feature exists"
fi

# Get editable features (not locked)
EDITABLE=$("${PLUGIN_ROOT}/skills/speclan-query/scripts/query.sh" --type feature --filter-status draft speclan)
```

### Extract specific fields with grep

```bash
# Get all feature IDs
./query.sh --type feature speclan | grep -oE '"id":"[^"]+"' | cut -d'"' -f4

# Get all paths
./query.sh --type feature speclan | grep -oE '"path":"[^"]+"' | cut -d'"' -f4

# Count entities
./query.sh --type requirement speclan | grep -c '"id"'
```

### Process each entity

```bash
./query.sh --type feature --full speclan | grep -oE '"id":"[^"]+"' | cut -d'"' -f4 | while read -r fid; do
  echo "Processing feature: $fid"
  req_count=$(./query.sh --type requirement --parent "$fid" speclan | grep -c '"id"' || echo 0)
  echo "  Requirements: $req_count"
done
```

## Status Lifecycle Reference

**Editable statuses** (can be modified directly):
- `draft`
- `review`
- `approved`

**Locked statuses** (require change-request):
- `in-development`
- `under-test`
- `released`
- `deprecated`

Use this for classification:

```bash
# Get editable features
./query.sh --type feature --filter-status draft speclan
./query.sh --type feature --filter-status review speclan
./query.sh --type feature --filter-status approved speclan

# Or check in code
case "$entity_status" in
  draft|review|approved) editable=true ;;
  *) editable=false ;;
esac
```

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Missing speclan dir | Error message, exit 1 |
| Invalid entity type | Error message, exit 1 |
| No matches found | Empty JSON array `[]`, exit 0 |
| Malformed filename | Skipped silently |
| Template files | Skipped automatically |
| Archived files | Skipped automatically |

## Performance Notes

- **Fast mode**: ~50ms for 100 features (filename parsing only)
- **Full mode**: ~500ms for 100 features (frontmatter reads)
- No caching between queries
- No depth limits on recursive search
- Files in `/templates/` and `/_archived/` are excluded
