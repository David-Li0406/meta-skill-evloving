---
name: query-language
description: Use when user needs complex data queries, multi-entity joins, aggregations, or analysis across Affinity data. Also use when user wants to filter, group, sort, or aggregate CRM records programmatically. Triggers: "query language", "structured query", "SQL-like", "find all persons where", "count opportunities by", "sum deal values", "average amount", "group by status", "filter AND/OR", "include companies with persons".
---

# Affinity Query Language

This skill covers the structured query language for querying Affinity CRM data via the `query` MCP tool.

> ⚠️ **Before running queries:** Complete the pre-flight checklist from `affinity-mcp-workflows` skill (read data-model, run discover-commands, state what you learned). This ensures you use current syntax and don't miss useful flags.

## When to Use This Tool

Use the `query` tool instead of individual CLI commands when you need:
- **Complex filtering** with multiple conditions (AND, OR, NOT)
- **Include relationships** (e.g., get persons with their companies)
- **Aggregations** (count, sum, avg, min, max, percentile)
- **Grouping** (count opportunities by status)
- **Multi-field sorting**
- **Batch analysis** across large datasets

For simple lookups, prefer `execute-read-command` with individual commands.

## Quick Start

```json
// Simplest query - get 10 persons
{"from": "persons", "limit": 10}

// Add a filter
{"from": "persons", "where": {"path": "email", "op": "contains", "value": "@acme.com"}, "limit": 10}

// Include related companies
{"from": "persons", "include": ["companies"], "limit": 10}

// Query list entries
{"from": "listEntries", "where": {"path": "listName", "op": "eq", "value": "Dealflow"}, "limit": 10}
```

## Query Structure

```json
{
  "$version": "1.0",
  "from": "persons",
  "where": { "path": "email", "op": "contains", "value": "@acme.com" },
  "include": ["companies", "opportunities"],
  "select": ["id", "firstName", "lastName", "email"],
  "orderBy": [{ "field": "lastName", "direction": "asc" }],
  "limit": 100
}
```

### Required Fields

| Field | Description |
|-------|-------------|
| `from` | Entity type: `persons`, `companies`, `opportunities`, `listEntries`, `interactions`, `notes` |

### Optional Fields

| Field | Description |
|-------|-------------|
| `$version` | Query format version (default: "1.0") |
| `where` | Filter conditions |
| `include` | Related entities to fetch |
| `expand` | Computed data to add to records (e.g., `interactionDates`) |
| `select` | Fields to return (default: all) |
| `orderBy` | Sort order |
| `groupBy` | Field to group by (requires `aggregate`) |
| `aggregate` | Aggregate functions to compute |
| `having` | Filter on aggregate results |
| `limit` | Maximum records to return |

## Filter Operators

### Comparison Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `eq` | Equal | `{"path": "status", "op": "eq", "value": "Active"}` |
| `neq` | Not equal | `{"path": "status", "op": "neq", "value": "Closed"}` |
| `gt` | Greater than | `{"path": "amount", "op": "gt", "value": 10000}` |
| `gte` | Greater than or equal | `{"path": "amount", "op": "gte", "value": 10000}` |
| `lt` | Less than | `{"path": "amount", "op": "lt", "value": 5000}` |
| `lte` | Less than or equal | `{"path": "amount", "op": "lte", "value": 5000}` |

### String Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `contains` | Contains substring (case-insensitive) | `{"path": "email", "op": "contains", "value": "@gmail"}` |
| `starts_with` | Starts with (case-insensitive) | `{"path": "name", "op": "starts_with", "value": "Acme"}` |
| `ends_with` | Ends with (case-insensitive) | `{"path": "email", "op": "ends_with", "value": "@acme.com"}` |

### Collection Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `in` | Value in list | `{"path": "status", "op": "in", "value": ["New", "Active"]}` |
| `between` | Value in range | `{"path": "amount", "op": "between", "value": [1000, 5000]}` |
| `contains_any` | String contains any substring (case-insensitive) | `{"path": "bio", "op": "contains_any", "value": ["python", "java"]}` |
| `contains_all` | String contains all substrings (case-insensitive) | `{"path": "bio", "op": "contains_all", "value": ["senior", "engineer"]}` |
| `has_any` | Array field contains any of the values | `{"path": "fields.Team Member", "op": "has_any", "value": ["LB", "MA"]}` |
| `has_all` | Array field contains all of the values | `{"path": "fields.Team Member", "op": "has_all", "value": ["LB", "MA"]}` |

### Multi-Select Field Filtering

Multi-select dropdown fields (like "Team Member") return arrays from the API. The `eq` and `neq` operators handle these automatically:

| Operator | Single-value field | Multi-select field |
|----------|-------------------|-------------------|
| `eq` | Exact match | Scalar: membership check / List: set equality |
| `neq` | Not equal | Scalar: not in array / List: set inequality |
| `in` | Value in list | Any intersection between arrays |
| `has_any` | Returns false | Any specified value present |
| `has_all` | Returns false | All specified values present |

**Examples:**

```json
// Find entries where Team Member includes "LB"
{ "path": "fields.Team Member", "op": "eq", "value": "LB" }

// Find entries where Team Member includes any of ["LB", "DW"]
{ "path": "fields.Team Member", "op": "has_any", "value": ["LB", "DW"] }

// Find entries where Team Member includes both "LB" and "MA"
{ "path": "fields.Team Member", "op": "has_all", "value": ["LB", "MA"] }
```

### Null/Empty Checks

| Operator | Description | Example |
|----------|-------------|---------|
| `is_null` | Field is null or empty string | `{"path": "email", "op": "is_null"}` |
| `is_not_null` | Field is not null and not empty | `{"path": "email", "op": "is_not_null"}` |
| `is_empty` | Field is null, empty string, or empty array | `{"path": "emails", "op": "is_empty"}` |

## Compound Conditions

### AND

```json
{
  "where": {
    "and": [
      { "path": "status", "op": "eq", "value": "Active" },
      { "path": "amount", "op": "gt", "value": 10000 }
    ]
  }
}
```

### OR

```json
{
  "where": {
    "or": [
      { "path": "email", "op": "contains", "value": "@acme.com" },
      { "path": "email", "op": "contains", "value": "@acme.io" }
    ]
  }
}
```

### NOT

```json
{
  "where": {
    "not": { "path": "status", "op": "eq", "value": "Closed" }
  }
}
```

## Advanced Filtering (Quantifiers, Exists, Count)

Filter based on related entities using quantifiers and existence checks.

> **Include vs Quantifiers:** Use `include` to **get** related data in the response (e.g., `"include": ["companies"]`). Use quantifiers to **filter** by related data (e.g., `{"path": "companies._count", "op": "gte", "value": 2}`). You can use both together.

### ALL Quantifier

All related items must match the condition:

```json
{
  "from": "persons",
  "where": {
    "all": {
      "path": "companies",
      "where": { "path": "domain", "op": "contains", "value": ".com" }
    }
  }
}
```

**Note:** Returns `true` for records with no related items (vacuous truth). To require at least one, combine with `_count`:

```json
{
  "where": {
    "and": [
      { "path": "companies._count", "op": "gte", "value": 1 },
      { "all": { "path": "companies", "where": { "path": "domain", "op": "contains", "value": ".com" }}}
    ]
  }
}
```

### NONE Quantifier

No related items may match the condition:

```json
{
  "from": "persons",
  "where": {
    "none": {
      "path": "interactions",
      "where": { "path": "type", "op": "eq", "value": "spam" }
    }
  }
}
```

### EXISTS Clause

At least one related item exists (optionally matching a filter):

```json
// Simple existence check
{
  "from": "persons",
  "where": { "exists": { "from": "interactions" }}
}

// With filter
{
  "from": "persons",
  "where": {
    "exists": {
      "from": "interactions",
      "where": { "path": "type", "op": "eq", "value": "meeting" }
    }
  }
}
```

### Count Pseudo-Field

Count related items and compare:

```json
// Persons with 2 or more companies
{
  "from": "persons",
  "where": { "path": "companies._count", "op": "gte", "value": 2 }
}

// Persons with no interactions
{
  "from": "persons",
  "where": { "path": "interactions._count", "op": "eq", "value": 0 }
}
```

### Available Relationships for Quantifiers

| From Entity | Available Relationship Paths |
|-------------|------------------------------|
| `persons` | `companies`, `opportunities`, `interactions`, `notes`, `listEntries` |
| `companies` | `persons`, `opportunities`, `interactions`, `notes`, `listEntries` |
| `opportunities` | `persons`, `companies`, `interactions` |

### Limitations

- **Nested quantifiers not supported**: Cannot use `all`/`none`/`exists` inside another quantifier
- **N+1 API calls**: Quantifiers fetch relationship data for each record (use dry-run to preview)

## Include Relationships

Fetch related entities in a single query:

```json
{
  "from": "persons",
  "include": ["companies", "opportunities"],
  "limit": 50
}
```

### Available Relationships

| From | Can Include |
|------|-------------|
| `persons` | `companies`, `opportunities`, `interactions`, `notes`, `listEntries` |
| `companies` | `persons`, `opportunities`, `interactions`, `notes`, `listEntries` |
| `opportunities` | `persons`, `companies`, `interactions` |
| `lists` | `entries` |
| `listEntries` | `entity`, `persons`, `companies`, `opportunities`, `interactions` |

**Note:** For `listEntries`:
- `entity` dynamically resolves to person/company/opportunity based on entityType
- `persons`, `companies`, `opportunities`, `interactions` fetch related entities for each list entry

### Include Output Format

Included data appears in a separate `included` section keyed by relationship name:

```json
{
  "data": [{"id": 123, "firstName": "John", "organizationIds": [456]}],
  "included": {
    "companies": [{"id": 456, "name": "Acme Inc", "domain": "acme.com"}]
  }
}
```

In **markdown** format, included data appears as separate tables with headers like "Included: companies".

**Note:** Parent records reference included entities via ID fields (e.g., `organizationIds` for companies). The `included` section contains deduplicated records.

## Expand Computed Data

Unlike `include` (which fetches related entities), `expand` adds computed data directly to each record.

⚠️ **ALWAYS use `dryRun: true` first** before running expand queries to see estimated API calls:

```json
// STEP 1: Preview with dryRun
{"query": {"from": "companies", "expand": ["interactionDates"], "limit": 50}, "dryRun": true}

// STEP 2: If API calls look reasonable (<200 calls), run without dryRun
{"from": "companies", "expand": ["interactionDates"], "limit": 50}
```

### Available Expansions

| Expansion | Supported Entities | Description |
|-----------|-------------------|-------------|
| `interactionDates` | `persons`, `companies`, `listEntries` | Last/next meeting dates, email dates, team members |
| `unreplied` | `persons`, `companies`, `opportunities`, `listEntries` | Detect unreplied incoming messages - email/chat (date, daysSince, type, subject) |

### Interaction Dates Output

When using `expand: ["interactionDates"]`, each record includes:

```json
{
  "id": 123,
  "name": "Acme Corp",
  "interactionDates": {
    "lastMeeting": {
      "date": "2026-01-08T10:00:00Z",
      "daysSince": 5,
      "teamMembers": ["Bob Smith", "Carol Jones"]
    },
    "nextMeeting": {
      "date": "2026-01-20T14:00:00Z",
      "daysUntil": 7,
      "teamMembers": ["Alice Wong"]
    },
    "lastEmail": {
      "date": "2026-01-10T09:30:00Z",
      "daysSince": 3
    },
    "lastInteraction": {
      "date": "2026-01-10T09:30:00Z",
      "daysSince": 3
    }
  }
}
```

### Include vs Expand

| Feature | `include` | `expand` |
|---------|-----------|----------|
| Purpose | Fetch related entities | Add computed data to records |
| Output | Separate `included` section | Merged into each record |
| Example | `include: ["companies"]` → company records | `expand: ["interactionDates"]` → dates on each record |

### Parameterized Includes for listEntries

When including `interactions` for listEntries, you can customize the fetch with parameters:

```json
{
  "from": "listEntries",
  "where": {"path": "listName", "op": "eq", "value": "Dealflow"},
  "include": [
    {"interactions": {"limit": 50, "days": 180}},
    {"opportunities": {"list": "Pipeline"}}
  ]
}
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `limit` | Max interactions per entity | 100 |
| `days` | Lookback window in days | 90 |
| `list` | Scope opportunities to specific list name/ID | All |
| `where` | Filter included entities | None |

### Example: Pipeline with Interaction Dates

```json
{
  "from": "listEntries",
  "where": {"path": "listName", "op": "eq", "value": "Dealflow"},
  "expand": ["interactionDates"],
  "select": ["entityId", "entityName", "fields.Status"],
  "limit": 100
}
```

**Note:** `expand` causes N+1 API calls (one per record). Use `dryRun: true` to preview the cost.

## Aggregations

### Basic Aggregates

```json
{
  "from": "opportunities",
  "aggregate": {
    "total": { "count": true },
    "totalValue": { "sum": "amount" },
    "avgValue": { "avg": "amount" },
    "minValue": { "min": "amount" },
    "maxValue": { "max": "amount" }
  }
}
```

### Group By

```json
{
  "from": "opportunities",
  "groupBy": "status",
  "aggregate": {
    "count": { "count": true },
    "totalValue": { "sum": "amount" }
  }
}
```

### Having (Filter on Aggregates)

```json
{
  "from": "opportunities",
  "groupBy": "status",
  "aggregate": {
    "count": { "count": true }
  },
  "having": { "path": "count", "op": "gte", "value": 5 }
}
```

## Querying List Entries

`listEntries` requires either `listId` or `listName` filter:

```json
// By ID
{"from": "listEntries", "where": {"path": "listId", "op": "eq", "value": 12345}}

// By name (executor resolves name → ID at runtime)
{"from": "listEntries", "where": {"path": "listName", "op": "eq", "value": "Dealflow"}}
```

**Invalid paths:** `list.name`, `list.id` - use `listName` or `listId` directly.

**Note:** When using `listName`, the query executor looks up the list by name and resolves it to a `listId` before fetching entries. This adds one API call but allows using human-readable names.

### Custom Field Values

When querying listEntries with `groupBy`, `aggregate`, or `where` on `fields.*` paths, the query engine automatically detects which fields are referenced and requests their values from the API.

```json
{
  "from": "listEntries",
  "where": {"path": "listName", "op": "eq", "value": "Dealflow"},
  "groupBy": "fields.Status",
  "aggregate": {"count": {"count": true}}
}
```

**Best practice: Select only the fields you need:**

```json
{
  "from": "listEntries",
  "where": {"path": "listName", "op": "eq", "value": "Dealflow"},
  "select": ["entityName", "fields.Status", "fields.Owner"],
  "limit": 100
}
```

⚠️ **Performance warning:** The `fields.*` wildcard fetches ALL custom field values. For lists with many fields (50+), this can take 60+ seconds per API page. Only use `fields.*` when you genuinely need every field - otherwise select specific fields like `fields.Status`, `fields.Owner`.

### Available Select Fields

| Field | Description |
|-------|-------------|
| `listEntryId` | List entry ID (same as `id`) |
| `entityId` | ID of the company/person/opportunity |
| `entityName` | Name of the entity |
| `entityType` | "company", "person", or "opportunity" |
| `listId` | Parent list ID |
| `createdAt` | Entry creation timestamp |
| `fields.<Name>` | Custom field value by name (preferred) |
| `fields.*` | All custom fields (⚠️ slow for lists with 50+ fields) |

### Field Value Normalization

Reference field values are **normalized to display strings** for readability:

| Field Type | API Returns | Normalized To |
|------------|-------------|---------------|
| Dropdown | `{"text": "Active", "id": 1}` | `"Active"` |
| Multi-select | `[{"text": "A"}, {"text": "B"}]` | `["A", "B"]` |
| Person reference | `{"firstName": "Jane", "lastName": "Doe"}` | `"Jane Doe"` |
| Company reference | `{"name": "Acme Corp", "id": 456}` | `"Acme Corp"` |

**Note:** Use `expand` or `include` to get full entity objects when you need IDs or other properties.

## Field Paths

Access nested fields using dot notation:

```json
{
  "from": "listEntries",
  "where": { "path": "fields.Status", "op": "eq", "value": "Active" }
}
```

Common paths:
- `fields.<FieldName>` - Custom list fields on listEntries (preferred - select specific fields)
- `fields.*` - All custom fields (⚠️ avoid for lists with 50+ fields - very slow)
- `emails[0]` - First email in array
- `company.name` - Nested object field (on included relationships)

## Date Filtering

### Relative Dates

```json
{
  "from": "interactions",
  "where": { "path": "created_at", "op": "gte", "value": "-30d" }
}
```

Supported formats:
- `-30d` - 30 days ago
- `+7d` - 7 days from now
- `today` - Start of today
- `now` - Current time
- `yesterday` - Start of yesterday
- `tomorrow` - Start of tomorrow

## Dry-Run Mode

⚠️ **MANDATORY for expand/include queries**: Always use `dryRun: true` first to preview API cost.

**When to use dryRun:**
- ✅ ALWAYS before any query with `expand` or `include`
- ✅ ALWAYS before quantifier queries (`all`, `none`, `exists`, `_count`)
- ✅ Before large result sets (100+ records)
- Optional for simple filters without relationships

```json
{
  "query": {
    "from": "persons",
    "include": ["companies", "opportunities"]
  },
  "dryRun": true
}
```

Returns execution plan with:
- Estimated API calls (**key metric** - if >200, consider reducing limit)
- Estimated records
- Step breakdown
- Warnings about expensive operations

**Decision guide based on dryRun results:**
| API Calls | Action |
|-----------|--------|
| <100 | ✅ Safe to run |
| 100-200 | ⚠️ Will take 2-5 minutes |
| 200-400 | ⚠️ May take 5-10 minutes, near ceiling |
| 400+ | ❌ Reduce limit or batch the query |

## Examples

### Find VIP Contacts

```json
{
  "from": "persons",
  "where": {
    "and": [
      { "path": "email", "op": "is_not_null" },
      { "path": "fields.VIP", "op": "eq", "value": true }
    ]
  },
  "include": ["companies"],
  "orderBy": [{ "field": "lastName", "direction": "asc" }],
  "limit": 100
}
```

### Pipeline Summary by Status

```json
{
  "from": "listEntries",
  "where": { "path": "listId", "op": "eq", "value": 12345 },
  "groupBy": "fields.Status",
  "aggregate": {
    "count": { "count": true },
    "totalValue": { "sum": "fields.Deal Value" }
  }
}
```

### Recent Interactions

```json
{
  "from": "interactions",
  "where": {
    "and": [
      { "path": "created_at", "op": "gte", "value": "-7d" },
      { "path": "type", "op": "in", "value": ["call", "meeting"] }
    ]
  },
  "include": ["persons"],
  "orderBy": [{ "field": "created_at", "direction": "desc" }],
  "limit": 50
}
```

### Companies Without Recent Activity

```json
{
  "from": "companies",
  "where": {
    "or": [
      { "path": "lastInteraction.date", "op": "lt", "value": "-90d" },
      { "path": "lastInteraction.date", "op": "is_null" }
    ]
  },
  "limit": 100
}
```

## Tool Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | object | required | The JSON query object |
| `dryRun` | boolean | false | Preview execution plan without running |
| `maxRecords` | integer | 1000 | Safety limit (max 10000). Same limits enforced on CLI commands. |
| `timeout` | integer | auto | Query timeout in seconds (auto-calculated from estimated API calls if not specified) |
| `maxOutputBytes` | integer | 50000 | Truncation limit for results |
| `format` | string | "toon" | Output format (see Output Formats below) |

### Timeout Auto-Calculation

When `timeout` is not specified, it's automatically calculated based on the query's estimated API calls:
- **Formula**: ~2 seconds per API call, minimum 30 seconds
- **Example**: Query with 100 API calls → 200 second timeout

The auto-calculation runs a quick dry-run internally to estimate API calls, then sets an appropriate timeout. Specify `timeout` explicitly to override.

## Output Formats

The `format` parameter controls how results are returned. Choose based on your use case:

| Format | Token Efficiency | Best For | Description |
|--------|-----------------|----------|-------------|
| `toon` | **High (~40% fewer)** | **Default** - large datasets | Full envelope with `data`, `pagination`, `included` |
| `json` | Low | Programmatic use | Full JSON structure (same data as TOON) |
| `markdown` | Medium-High | **LLM analysis** | GitHub-flavored table + pagination footer (best comprehension) |
| `jsonl` | Medium | Streaming | One JSON object per line (data only) |
| `csv` | Medium | Spreadsheets | Comma-separated values (data only) |

### Format Recommendations

- **For LLM analysis tasks**: Use `markdown` - LLMs are trained on documentation and tables
- **For large result sets**: Use `toon` to minimize tokens (30-60% smaller than JSON)
- **For programmatic processing**: Use `json` for full structure
- **For streaming workflows**: Use `jsonl` for line-by-line processing

### Format Examples

**JSON:**
```json
{"data": [{"id": 1, "name": "Acme"}], "included": {...}, "pagination": {...}}
```

**JSONL:**
```jsonl
{"id": 1, "name": "Acme"}
{"id": 2, "name": "Beta"}
```

**Markdown:**
```markdown
| id | name |
| --- | --- |
| 1 | Acme |
| 2 | Beta |
```

**TOON (default):**
```
data[2]{id,name}:
  1,Acme
  2,Beta
pagination:
  hasMore: false
  total: 2
```

**Note:** `jsonl` and `csv` are data-only export formats (no envelope). `toon`, `json`, and `markdown` preserve pagination and included entity information.

## Performance

### Expand InteractionDates

The `interactionDates` expansion fetches meeting/email dates and team member names for each record. Performance optimizations:

- **Parallel fetching**: Entity fetches and person name resolution run in parallel
- **Shared concurrency limits**: Person API calls are bounded to prevent rate limiting
- **Graceful degradation**: If person name lookup fails, falls back to "Person {id}" instead of failing the query
- **Progress reporting**: Shows per-record progress for large expansions

**Recommendations:**
- For large datasets (500+ records), expect ~2 seconds per record
- Use `limit` to scope the expansion appropriately
- The timeout auto-calculates based on estimated API calls

### Environment Variables

For advanced tuning (power users only):

| Variable | Default | Description |
|----------|---------|-------------|
| `XAFFINITY_QUERY_CONCURRENCY` | 15 | Max concurrent API calls for fetches/expansions |

## Best Practices

1. **Start with dry-run** for complex queries to see API call estimates
2. **Use limit** to avoid fetching too much data
3. **Be specific with where** to reduce client-side filtering
4. **Avoid deep includes** which cause N+1 API calls
5. **Use groupBy + aggregate** for reports instead of fetching all records
6. **For quantifier queries** on large databases, always add `maxRecords`

## Quantifier Query Performance

**Quick decision:**
- `listEntries` → Safe (bounded by list size)
- `persons`/`companies`/`opportunities` with quantifiers → Requires `maxRecords`

**Important**: Queries using `all`, `none`, `exists`, or `_count` on unbounded
entities (`persons`, `companies`, `opportunities`) require explicit `maxRecords`.

**Why?** These operations make N+1 API calls (one per record). On a database with
50,000 persons, this could take 26+ minutes.

**Recommended approach:**
1. Start from `listEntries` (bounded by list size) instead of unbounded entities
2. Add cheap pre-filters before quantifier conditions to reduce N+1 calls
3. Use `maxRecords` to explicitly limit scope: `maxRecords: 100`
4. Use `dryRun: true` to preview estimated API calls before running

**Example - safe quantifier query:**
```json
{
  "query": {
    "from": "listEntries",
    "where": {
      "and": [
        {"path": "listName", "op": "eq", "value": "Target Companies"},
        {"path": "persons._count", "op": "gte", "value": 3}
      ]
    }
  },
  "maxRecords": 1000
}
```

## Limitations

- All filtering except `listEntries` field filters happens client-side
- Includes cause N+1 API calls (1 per parent record)
- No cross-entity joins (use includes instead)
- Maximum 10,000 records per query for safety
- Nested quantifiers (`all`/`none`/`exists` inside each other) not supported
- OR clauses containing quantifiers cannot benefit from lazy loading optimization
