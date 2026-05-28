# Symbol API Reference

Complete API documentation for all symbol query functions provided by `scripts/symbol_tools.py`.

## Overview

The Symbol API provides six core functions for efficient codebase navigation:

1. **query_symbols** - Search symbols by name, kind, domain, or path
2. **load_domain** - Load complete symbol set for a specific domain
3. **load_api_layer** - Load symbols from a specific architectural layer
4. **search_patterns** - Advanced pattern-based search with layer filtering
5. **get_symbol_context** - Get detailed information about a specific symbol
6. **update_symbols** - Trigger symbol graph regeneration

All functions are available in `scripts/symbol_tools.py` and can be executed directly or imported.

---

## 1. query_symbols

Query symbols by name, kind, domain, or path without loading the entire symbol graph.

### Purpose

Find specific symbols, search by partial name, filter by type or location. Most efficient way to search for specific code elements.

### Parameters

- **name** (optional, string) - Symbol name with partial/fuzzy matching support
  - Example: `"Button"` matches `Button`, `IconButton`, `ButtonGroup`
  - Case-insensitive by default

- **kind** (optional, string) - Symbol kind to filter by
  - Valid values: `component`, `hook`, `function`, `class`, `interface`, `type`, `method`
  - Example: `kind="component"` returns only React components

- **domain** (optional, string) - Domain filter (project-configured)
  - Examples: `ui`, `web`, `api`, `shared`, `mobile`
  - Configured in `symbols.config.json`

- **path** (optional, string) - File path pattern
  - Example: `"components"`, `"hooks"`, `"services"`
  - Supports partial matching

- **limit** (optional, number) - Maximum results to return
  - Default: `20`
  - Use lower limits for quick scans

- **summary_only** (optional, boolean) - Return only name and summary
  - Default: `false`
  - Use `true` for quick overviews with minimal token usage

### Returns

List of matching symbols with:
- `name` - Symbol name
- `kind` - Symbol type (component, function, etc.)
- `file` - File path and location
- `line` - Line number in file
- `domain` - Domain classification
- `summary` - Brief description
- `signature` - Function/method signature (if applicable)

### Usage Examples

**Find React components:**
```python
from symbol_tools import query_symbols

# Find all components with "Card" in name
results = query_symbols(name="Card", kind="component", domain="ui", limit=10)

# Output:
# [
#   {
#     "name": "Card",
#     "kind": "component",
#     "file": "src/components/Card.tsx",
#     "line": 15,
#     "domain": "ui",
#     "summary": "Base card component with variants"
#   },
#   {
#     "name": "CardHeader",
#     "kind": "component",
#     "file": "src/components/Card.tsx",
#     "line": 42,
#     "domain": "ui",
#     "summary": "Card header with title and actions"
#   }
# ]
```

**Find authentication-related functions:**
```python
# Search by name and path pattern
results = query_symbols(name="auth", kind="function", path="services")

# Find all hooks (quick scan)
hooks = query_symbols(kind="hook", domain="web", summary_only=True)
```

**Find custom hooks:**
```python
# Get all custom hooks in frontend app
hooks = query_symbols(kind="hook", domain="web", limit=20)

# Find specific hook by name
user_hooks = query_symbols(name="useUser", kind="hook", domain="web")
```

### Edge Cases

- **No matches**: Returns empty list `[]`
- **Too many results**: Use `limit` parameter to control size
- **Ambiguous names**: Returns all matches; use additional filters
- **Invalid kind**: Ignores filter if kind is not recognized

---

## 2. load_domain

Load complete symbol set for a specific domain (UI, Web, API, Shared, etc.).

### Purpose

Need broader context for a domain, implementing features that touch multiple files within a domain. Use when targeted queries are insufficient.

### Parameters

- **domain** (required, string) - Domain to load
  - Configured in `symbols.config.json`
  - Common values: `ui`, `web`, `api`, `shared`, `mobile`

- **include_tests** (optional, boolean) - Include test file symbols
  - Default: `false`
  - Set to `true` for debugging workflows

- **max_symbols** (optional, number) - Limit number of symbols returned
  - Default: all symbols in domain
  - Recommended: `50-100` for most use cases

### Returns

Dictionary with:
- `domain` - Domain name
- `type` - "domain" (distinguishes from layer loading)
- `totalSymbols` - Count of symbols in result
- `symbols` - Array of symbol objects

### Usage Examples

**Load UI symbols for component work:**
```python
from symbol_tools import load_domain

# Load UI components (excludes tests)
ui_context = load_domain(domain="ui", include_tests=False, max_symbols=100)

# Output:
# {
#   "domain": "ui",
#   "type": "domain",
#   "totalSymbols": 87,
#   "symbols": [
#     { "name": "Button", "kind": "component", ... },
#     { "name": "Card", "kind": "component", ... },
#     ...
#   ]
# }
```

**Load web domain for frontend development:**
```python
# Load frontend app symbols
web_context = load_domain(domain="web", include_tests=False, max_symbols=100)
```

**Load API with tests for debugging:**
```python
# Include test symbols for debugging
api_context = load_domain(domain="api", include_tests=True)
```

**Load first 50 shared symbols:**
```python
# Quick reference of shared utilities
shared_context = load_domain(domain="shared", max_symbols=50)
```

### Token Efficiency

- Loading 50-100 symbols: ~10-15KB
- Full domain: ~250KB+
- **Savings: 93-96% reduction**

### Note for Backend Domains

For backend APIs, consider using `load_api_layer()` instead to load only the specific architectural layer you need (routers, services, repositories, schemas). This provides 50-80% additional token reduction.

### Edge Cases

- **Invalid domain**: Returns error message
- **Empty domain**: Returns dict with `totalSymbols: 0`
- **max_symbols exceeded**: Returns first N symbols only

---

## 3. load_api_layer

Load symbols from a specific architectural layer for token-efficient backend development.

### Purpose

Backend development requiring only one architectural layer. Provides 50-80% token reduction versus loading entire backend domain.

**Use when:**
- Working on specific backend layer (routers, services, repositories)
- Need DTO/schema patterns
- Implementing business logic in service layer
- Adding new API endpoints

### Parameters

- **layer** (required, string) - Architectural layer to load
  - Configured per project in `symbols.config.json`
  - Common values: `routers`, `services`, `repositories`, `schemas`, `cores`
  - May vary based on project architecture

- **max_symbols** (optional, number) - Limit number of symbols returned
  - Default: all symbols in layer
  - Recommended: `50-100` for most tasks

### Returns

Dictionary with:
- `layer` - Layer name
- `type` - "layer" (distinguishes from domain loading)
- `totalSymbols` - Count of symbols in result
- `symbols` - Array of symbol objects

### Usage Examples

**Load service layer for backend development:**
```python
from symbol_tools import load_api_layer

# Load only service layer
services = load_api_layer("services", max_symbols=50)

# Output:
# {
#   "layer": "services",
#   "type": "layer",
#   "totalSymbols": 42,
#   "symbols": [
#     { "name": "UserService", "kind": "class", "layer": "service", ... },
#     { "name": "AuthService", "kind": "class", "layer": "service", ... },
#     ...
#   ]
# }
```

**Load schemas for DTO work:**
```python
# Get all DTOs and request/response schemas
schemas = load_api_layer("schemas", max_symbols=100)
```

**Load routers for endpoint development:**
```python
# Get all API route handlers
routers = load_api_layer("routers")
```

**Load repositories for data access patterns:**
```python
# Get all data access patterns
repositories = load_api_layer("repositories")
```

**Load cores for models and utilities:**
```python
# Get domain models and core utilities
cores = load_api_layer("cores", max_symbols=200)
```

### Token Efficiency

**Compared to loading full backend domain:**

- Service layer only: **80-85% reduction**
- Router layer only: **85-90% reduction**
- Schema layer only: **85-90% reduction**
- Repository layer only: **80-85% reduction**

**Example:**
- Full backend domain: ~200KB
- Service layer only: ~30KB (85% reduction)

### Common Layer Types

Layer types are configured per project but typically include:

- **routers** / **controllers** - HTTP endpoints, route handlers, request validation
- **services** - Business logic, DTO mapping, orchestration between layers
- **repositories** - Database operations, data access patterns, query logic
- **schemas** / **dtos** - Request/response data transfer objects, validation schemas
- **cores** / **models** - Domain models, core utilities, database entities

### Edge Cases

- **Invalid layer**: Returns error message
- **Layer not chunked**: Falls back to full domain loading
- **Empty layer**: Returns dict with `totalSymbols: 0`

---

## 4. search_patterns

Advanced pattern-based search with architectural layer tags for precise filtering.

### Purpose

Find symbols matching regex patterns, filter by architectural layer tag, validate layered architecture patterns. Use when you need pattern-based discovery or architecture validation.

### Parameters

- **pattern** (optional, string) - Search pattern with regex support
  - Example: `"Service"` matches any symbol containing "Service"
  - Example: `"^[A-Z].*Card"` matches capitalized names ending in "Card"
  - Example: `"router|Router"` matches variations

- **layer** (optional, string) - Architectural layer tag
  - Common backend layers: `router`, `service`, `repository`, `schema`, `model`, `core`, `auth`, `middleware`
  - Common frontend layers: `component`, `hook`, `page`, `util`
  - Test layer: `test`
  - Configured per project

- **priority** (optional, string) - Priority filter
  - Valid values: `high`, `medium`, `low`
  - Used for prioritizing symbols

- **domain** (optional, string) - Domain filter
  - Same as other functions: `ui`, `web`, `api`, `shared`, etc.

- **limit** (optional, number) - Maximum results
  - Default: `30`

### Returns

List of matching symbols with layer tag, domain, and summary.

### Usage Examples

**Find all service layer classes:**
```python
from symbol_tools import search_patterns

# Find services in backend
services = search_patterns(pattern="Service", layer="service", domain="api")

# Output:
# [
#   {
#     "name": "UserService",
#     "kind": "class",
#     "layer": "service",
#     "domain": "api",
#     "summary": "User management business logic"
#   },
#   {
#     "name": "AuthService",
#     "kind": "class",
#     "layer": "service",
#     "domain": "api",
#     "summary": "Authentication and authorization logic"
#   }
# ]
```

**Find router endpoints:**
```python
# Find all routers
routers = search_patterns(pattern="router|Router", layer="router")
```

**Find React components following naming pattern:**
```python
# Find all Card components
components = search_patterns(
    pattern="^[A-Z].*Card",
    layer="component",
    domain="ui"
)
```

**Find middleware implementations:**
```python
# Get all middleware
middleware = search_patterns(layer="middleware", domain="api")
```

**Find observability-tagged code:**
```python
# Get all telemetry/logging code
telemetry = search_patterns(layer="observability", domain="api")
```

### Layer Tags Reference

All symbols include a `layer` field enabling precise architectural filtering.

**Backend Layers (example):**
- `router` - HTTP endpoints, route handlers
- `service` - Business logic
- `repository` - Data access
- `schema` - DTOs and validation
- `model` - Domain models
- `core` - Core utilities
- `auth` - Authentication/authorization
- `middleware` - Middleware functions

**Frontend Layers (example):**
- `component` - UI components
- `hook` - React hooks
- `page` - Application pages/routes
- `util` - Utilities and helpers

**Test Layer:**
- `test` - Test files and utilities

### Edge Cases

- **No pattern + no layer**: Returns first N symbols (use `limit`)
- **Invalid regex**: Returns error message
- **No matches**: Returns empty list
- **Layer not found**: Returns empty list

---

## 5. get_symbol_context

Get full context for a specific symbol including definition location and related symbols.

### Purpose

Need detailed information about a specific symbol, want to find related symbols (props interfaces, same-file symbols, imports).

**Use when:**
- Examining a specific component/function
- Understanding symbol relationships
- Finding props interfaces for components
- Discovering same-file symbols

### Parameters

- **name** (required, string) - Exact symbol name
  - Must match symbol name exactly (case-sensitive)

- **file** (optional, string) - File path if name is ambiguous
  - Use when multiple symbols have same name
  - Example: `"src/components/Button.tsx"`

- **include_related** (optional, boolean) - Include related symbols
  - Default: `false`
  - When `true`, returns related symbols (props, imports, usages)

### Returns

Dictionary with:
- `symbol` - Main symbol object with full details
- `related` - Array of related symbols (if `include_related=true`)

### Usage Examples

**Get full context for a component:**
```python
from symbol_tools import get_symbol_context

# Get component with props interface
context = get_symbol_context(name="Button", include_related=True)

# Output:
# {
#   "symbol": {
#     "name": "Button",
#     "kind": "component",
#     "file": "src/components/Button.tsx",
#     "line": 15,
#     "signature": "Button(props: ButtonProps): JSX.Element",
#     "summary": "Base button component with variants"
#   },
#   "related": [
#     {
#       "name": "ButtonProps",
#       "kind": "interface",
#       "file": "src/components/Button.tsx",
#       "line": 8,
#       "summary": "Props for Button component"
#     }
#   ]
# }
```

**Get service definition with related symbols:**
```python
# Specify file to disambiguate
service = get_symbol_context(
    name="UserService",
    file="api/services/user_service.py",
    include_related=True
)
```

**Get basic symbol info (no relationships):**
```python
# Fast lookup without relationships
symbol = get_symbol_context(name="formatDate")
```

### Relationship Detection

Automatically finds:
- **Props interfaces** for React components
- **Same-file symbols** (interfaces, types, helpers)
- **Imported symbols** (from same domain)
- **Usage patterns** (where symbol is used)

### Edge Cases

- **Symbol not found**: Returns error message
- **Multiple matches**: Use `file` parameter to disambiguate
- **No related symbols**: Returns empty `related` array
- **Circular relationships**: Limited to depth of 2

---

## 6. update_symbols

Trigger symbol graph regeneration when code changes require updated symbols.

### Purpose

Update symbol indices after significant code changes, when symbol files are out of sync with codebase.

**Use when:**
- Added new files or components
- Refactored code structure
- Changed architectural layers
- Symbol queries return outdated results

### Primary Approach: symbols-engineer Agent

**Recommended:** Use the `symbols-engineer` agent for orchestration:

```python
# Update symbols for specific domain
Task("symbols-engineer", "Update symbols for the API domain after schema changes")

# Incremental update for recent changes
Task("symbols-engineer", "Perform incremental symbol update for recent file changes")

# Full regeneration with re-chunking
Task("symbols-engineer", "Regenerate full symbol graph and re-chunk by domain")
```

The `symbols-engineer` agent handles:
1. Configuration review
2. Symbol extraction with appropriate scripts
3. Layer tag assignment
4. Optional chunking by layer
5. Validation

### Manual Extraction Workflow

If manually updating symbols:

**1. Review configuration:**
```bash
# Check symbols.config.json for domain paths and output files
cat symbols.config.json
```

**2. Extract symbols:**
```bash
# TypeScript/React symbols
python scripts/extract_symbols_typescript.py apps/web --output=ai/symbols-web.json

# Python symbols
python scripts/extract_symbols_python.py services/api --output=ai/symbols-api.json
```

**3. Add layer tags:**
```bash
python scripts/add_layer_tags.py ai/symbols-api.json
```

**4. Chunk by layer (OPTIONAL, for backend efficiency):**
```bash
python scripts/split_api_by_layer.py ai/symbols-api.json --output-dir=ai/
```

This creates layer-specific files:
- `symbols-api-routers.json` - Router layer only
- `symbols-api-services.json` - Service layer only
- `symbols-api-repositories.json` - Repository layer only
- `symbols-api-schemas.json` - Schema layer only
- `symbols-api-cores.json` - Core utilities/models

**Result:** 50-80% token reduction when loading backend symbols.

### Programmatic API

```python
from symbol_tools import update_symbols

# Incremental update for recent changes
result = update_symbols(mode="incremental")

# Full regeneration (use sparingly)
result = update_symbols(mode="full", chunk=True)

# Update specific domain only
result = update_symbols(mode="domain", domain="ui")
```

### Parameters

- **mode** (optional, string) - Update mode
  - `incremental` - Update only changed files (default)
  - `full` - Complete regeneration
  - `domain` - Update specific domain

- **domain** (optional, string) - Specific domain to update
  - Required when `mode="domain"`

- **files** (optional, array) - Specific files to update
  - Used for `mode="incremental"`

- **chunk** (optional, boolean) - Re-chunk symbols after update
  - Default: `true`
  - Applies layer-based chunking to backends

### Returns

Dictionary with:
- `status` - "success" or "error"
- `message` - Description of what was updated
- `domainsUpdated` - List of domains that were regenerated
- `symbolsAdded` - Count of new symbols
- `symbolsRemoved` - Count of removed symbols

### Extraction Requirements

- Scripts read `symbols.config.json` to understand project structure
- You must specify input directory path and output file as arguments
- Example: `python extract_symbols_typescript.py apps/web --output=ai/symbols-web.json`

### Edge Cases

- **No changes detected**: Returns success with 0 updates
- **Invalid domain**: Returns error
- **Script failure**: Returns error with script output
- **Chunk failure**: Warns but continues with non-chunked symbols

---

## Complete Usage Example

Combining multiple functions for a development workflow:

```python
from symbol_tools import (
    query_symbols,
    load_domain,
    load_api_layer,
    search_patterns,
    get_symbol_context
)

# 1. Quick search to find relevant components
cards = query_symbols(name="Card", kind="component", domain="ui", limit=5)

# 2. Load broader UI context
ui_symbols = load_domain(domain="ui", max_symbols=50)

# 3. Find service patterns in backend
services = load_api_layer("services", max_symbols=30)

# 4. Search for authentication patterns
auth_patterns = search_patterns(
    pattern="auth|Auth",
    layer="service",
    domain="api"
)

# 5. Get detailed context for specific component
button_context = get_symbol_context(
    name="Button",
    include_related=True
)

# Result: Comprehensive context with ~5-10KB loaded (95-98% token reduction)
```

---

## Error Handling

All functions follow consistent error handling:

**Success:**
```python
{
  "status": "success",
  "data": { ... }
}
```

**Error:**
```python
{
  "status": "error",
  "message": "Description of error",
  "code": "ERROR_CODE"
}
```

Common error codes:
- `INVALID_DOMAIN` - Domain not found in configuration
- `INVALID_LAYER` - Layer not found or not chunked
- `SYMBOL_NOT_FOUND` - Requested symbol does not exist
- `CONFIG_ERROR` - symbols.config.json is invalid or missing
- `FILE_NOT_FOUND` - Symbol file does not exist

---

## Performance Notes

**Token Efficiency Comparison:**

| Loading Method | Token Size | Reduction |
|----------------|------------|-----------|
| Full codebase | ~500KB+ | 0% (baseline) |
| Full domain | ~250KB | 50% |
| Domain with limit | ~10-15KB | 93-97% |
| Single layer | ~20-30KB | 85-90% |
| Targeted query | ~2-5KB | 95-99% |
| Layer-filtered query | ~1-3KB | 99%+ |

**Best Practices:**
- Start with targeted queries (`query_symbols`)
- Use `load_api_layer` instead of full domain for backends
- Apply `max_symbols` limits to control size
- Use `summary_only=True` for quick scans

---

## See Also

- **[symbol-workflows-by-role.md](./symbol-workflows-by-role.md)** - Practical workflows by developer role
- **[symbol-script-operations.md](./symbol-script-operations.md)** - Symbol extraction and maintenance scripts
- **[symbol-schema-architecture.md](./symbol-schema-architecture.md)** - Symbol structure and layer taxonomy
- **[symbol-performance-metrics.md](./symbol-performance-metrics.md)** - Detailed performance benchmarks
