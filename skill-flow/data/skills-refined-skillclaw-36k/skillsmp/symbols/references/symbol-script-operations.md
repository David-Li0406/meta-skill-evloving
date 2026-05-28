# Symbol Script Operations

Complete documentation for all symbol extraction, maintenance, and update scripts. This guide covers configuration, script usage, workflows, and troubleshooting.

## Overview

The symbol system uses a pipeline of scripts to extract, tag, chunk, and maintain symbol graphs:

1. **Configuration** - `symbols.config.json` defines project structure
2. **Extraction** - Language-specific scripts extract symbols from code
3. **Tagging** - `add_layer_tags.py` assigns architectural layer tags
4. **Chunking** - `split_api_by_layer.py` creates layer-specific files (optional)
5. **Merging** - `merge_symbols.py` handles incremental updates
6. **Validation** - Quality checks and consistency validation

All scripts are located in `.claude/skills/symbols/scripts/`.

---

## Configuration: symbols.config.json

### Purpose

The **source of truth** for your project's symbol system. Defines structure, domains, paths, and layer patterns.

### Location

```
.claude/skills/symbols/symbols.config.json
```

### Structure

```json
{
  "version": "1.0",
  "projectName": "YourProject",
  "domains": {
    "ui": {
      "source": "packages/ui/src",
      "output": "ai/symbols-ui.json",
      "include": ["*.ts", "*.tsx"],
      "exclude": ["**/*.test.*", "**/*.spec.*"],
      "language": "typescript"
    },
    "web": {
      "source": "apps/web/src",
      "output": "ai/symbols-web.json",
      "include": ["*.ts", "*.tsx"],
      "exclude": ["**/*.test.*", "**/*.spec.*"],
      "language": "typescript"
    },
    "api": {
      "source": "services/api/app",
      "output": "ai/symbols-api.json",
      "include": ["*.py"],
      "exclude": ["**/tests/**", "**/__pycache__/**"],
      "language": "python",
      "enableLayerSplit": true
    },
    "shared": {
      "source": "packages/shared/src",
      "output": "ai/symbols-shared.json",
      "include": ["*.ts"],
      "exclude": ["**/*.test.*"],
      "language": "typescript"
    }
  },
  "layers": {
    "backend": {
      "router": ["app/api/*", "app/routers/*", "*/routers/*"],
      "service": ["app/services/*", "*/services/*"],
      "repository": ["app/repositories/*", "*/repositories/*"],
      "schema": ["app/schemas/*", "app/dtos/*", "*/schemas/*"],
      "core": ["app/core/*", "app/models/*", "*/core/*"],
      "middleware": ["app/middleware/*", "*/middleware/*"],
      "auth": ["app/auth/*", "*/auth/*"]
    },
    "frontend": {
      "component": ["components/*", "*/components/*"],
      "hook": ["hooks/*", "*/hooks/*"],
      "page": ["pages/*", "app/*", "*/pages/*"],
      "util": ["utils/*", "lib/*", "*/utils/*", "*/lib/*"],
      "context": ["contexts/*", "*/contexts/*"]
    },
    "test": {
      "test": ["**/*.test.*", "**/*.spec.*", "**/tests/*", "**/__tests__/*"]
    }
  },
  "regenerateOnStart": false,
  "cacheEnabled": true,
  "outputDirectory": "ai"
}
```

### Configuration Fields

**Global Settings:**
- `version` - Config schema version
- `projectName` - Project identifier
- `outputDirectory` - Where symbol files are saved
- `regenerateOnStart` - Auto-regenerate symbols on session start
- `cacheEnabled` - Enable symbol caching

**Domain Configuration:**
- `source` - Source directory to scan
- `output` - Output JSON file path
- `include` - File patterns to include
- `exclude` - File patterns to exclude
- `language` - Language for extraction (`typescript`, `python`)
- `enableLayerSplit` - Enable layer-based chunking (optional)

**Layer Patterns:**
- `backend` - Backend architectural layers with path patterns
- `frontend` - Frontend architectural layers with path patterns
- `test` - Test file patterns

### Customization

Edit `symbols.config.json` to match your project structure:

1. **Add/remove domains** - Match your codebase organization
2. **Update source paths** - Point to your actual directories
3. **Customize layer patterns** - Match your architectural patterns
4. **Set output locations** - Choose where symbols are saved

---

## Extraction Scripts

### 1. extract_symbols_typescript.py

Extracts symbols from TypeScript and React codebases.

**Features:**
- Extracts components, hooks, functions, classes, interfaces, types
- Parses JSDoc comments for summaries
- Handles React component props
- Filters test files

**Usage:**

```bash
python .claude/skills/symbols/scripts/extract_symbols_typescript.py \
  <source-directory> \
  --output=<output-file>
```

**Examples:**

```bash
# Extract UI component symbols
python scripts/extract_symbols_typescript.py \
  packages/ui/src \
  --output=ai/symbols-ui.json

# Extract web app symbols
python scripts/extract_symbols_typescript.py \
  apps/web/src \
  --output=ai/symbols-web.json

# Extract shared utility symbols
python scripts/extract_symbols_typescript.py \
  packages/shared/src \
  --output=ai/symbols-shared.json
```

**Options:**

- `<source-directory>` (required) - Directory to scan
- `--output=<file>` (required) - Output JSON file path
- `--exclude-tests` (optional) - Skip test files (default: true)
- `--verbose` (optional) - Show detailed progress

**Output Format:**

```json
{
  "domain": "ui",
  "language": "typescript",
  "extractedAt": "2025-11-06T10:30:00Z",
  "totalSymbols": 142,
  "symbols": [
    {
      "name": "Button",
      "kind": "component",
      "file": "packages/ui/src/components/Button.tsx",
      "line": 15,
      "signature": "Button(props: ButtonProps): JSX.Element",
      "summary": "Base button component with variants",
      "parent": null,
      "docstring": "/** Base button component with variants */",
      "category": "component"
    }
  ]
}
```

**Extracted Symbol Kinds:**

- `component` - React components
- `hook` - React hooks (built-in and custom)
- `function` - Functions and arrow functions
- `class` - Class declarations
- `method` - Class methods
- `interface` - TypeScript interfaces
- `type` - TypeScript type aliases

---

### 2. extract_symbols_python.py

Extracts symbols from Python codebases.

**Features:**
- Extracts modules, classes, functions, methods
- Pulls function signatures and docstrings
- Filters test files and internal imports
- Handles decorators and async functions

**Usage:**

```bash
python .claude/skills/symbols/scripts/extract_symbols_python.py \
  <source-directory> \
  --output=<output-file>
```

**Examples:**

```bash
# Extract API backend symbols
python scripts/extract_symbols_python.py \
  services/api/app \
  --output=ai/symbols-api.json

# Extract shared Python utilities
python scripts/extract_symbols_python.py \
  packages/shared-py \
  --output=ai/symbols-shared-py.json
```

**Options:**

- `<source-directory>` (required) - Directory to scan
- `--output=<file>` (required) - Output JSON file path
- `--exclude-tests` (optional) - Skip test files (default: true)
- `--verbose` (optional) - Show detailed progress

**Output Format:**

```json
{
  "domain": "api",
  "language": "python",
  "extractedAt": "2025-11-06T10:30:00Z",
  "totalSymbols": 387,
  "symbols": [
    {
      "name": "UserService",
      "kind": "class",
      "file": "services/api/app/services/user_service.py",
      "line": 12,
      "signature": "class UserService",
      "summary": "User management business logic",
      "parent": null,
      "docstring": "User management business logic and orchestration",
      "category": "service"
    }
  ]
}
```

**Extracted Symbol Kinds:**

- `module` - Python modules
- `class` - Class definitions
- `function` - Functions (including async)
- `method` - Class methods

---

## Layer Tagging: add_layer_tags.py

### Purpose

Assigns architectural layer tags to all symbols based on file path patterns defined in `symbols.config.json`.

### When to Use

Run after extraction to enable layer-based filtering and querying.

### Usage

```bash
python .claude/skills/symbols/scripts/add_layer_tags.py \
  <symbol-file>
```

### Examples

```bash
# Add layer tags to API symbols
python scripts/add_layer_tags.py ai/symbols-api.json

# Add layer tags to web symbols
python scripts/add_layer_tags.py ai/symbols-web.json

# Add layer tags to UI symbols
python scripts/add_layer_tags.py ai/symbols-ui.json
```

### How It Works

1. Reads `symbols.config.json` for layer patterns
2. Matches each symbol's file path against patterns
3. Assigns appropriate layer tag
4. Updates symbol file in-place

### Layer Assignment Logic

**Backend layers** (example patterns from config):

```python
# File: services/api/app/routers/user_router.py
# Pattern: "app/routers/*"
# Assigned layer: "router"

# File: services/api/app/services/user_service.py
# Pattern: "app/services/*"
# Assigned layer: "service"

# File: services/api/app/repositories/user_repository.py
# Pattern: "app/repositories/*"
# Assigned layer: "repository"
```

**Frontend layers** (example patterns):

```python
# File: apps/web/src/components/Button.tsx
# Pattern: "components/*"
# Assigned layer: "component"

# File: apps/web/src/hooks/useUser.ts
# Pattern: "hooks/*"
# Assigned layer: "hook"
```

**Test layers:**

```python
# File: apps/web/src/components/Button.test.tsx
# Pattern: "**/*.test.*"
# Assigned layer: "test"
```

### Output

Updates symbol file with `layer` field:

```json
{
  "name": "UserService",
  "kind": "class",
  "file": "services/api/app/services/user_service.py",
  "line": 12,
  "layer": "service",
  "summary": "User management business logic"
}
```

---

## Layer Chunking: split_api_by_layer.py

### Purpose

**OPTIONAL** - Splits large backend symbol files into layer-specific files for maximum token efficiency.

### When to Use

- Backend APIs with many symbols (100+ symbols)
- When you frequently work on specific layers
- To achieve 50-80% token reduction for backend work

### Usage

```bash
python .claude/skills/symbols/scripts/split_api_by_layer.py \
  <symbol-file> \
  --output-dir=<directory>
```

### Examples

```bash
# Split API symbols by layer
python scripts/split_api_by_layer.py \
  ai/symbols-api.json \
  --output-dir=ai/

# Result: Creates layer-specific files in ai/ directory
```

### Output Files

Creates separate files for each layer:

```
ai/
├── symbols-api.json              # Original file (unchanged)
├── symbols-api-routers.json      # Router layer only
├── symbols-api-services.json     # Service layer only
├── symbols-api-repositories.json # Repository layer only
├── symbols-api-schemas.json      # Schema layer only
├── symbols-api-cores.json        # Core utilities/models
└── symbols-api-tests.json        # Test files (if included)
```

### File Structure

Each layer file contains:

```json
{
  "layer": "services",
  "domain": "api",
  "language": "python",
  "totalSymbols": 45,
  "symbols": [
    {
      "name": "UserService",
      "kind": "class",
      "layer": "service",
      "file": "services/api/app/services/user_service.py",
      "line": 12,
      "summary": "User management business logic"
    }
  ]
}
```

### Token Efficiency Gains

**Before chunking:**
- Full backend: ~250KB (387 symbols)

**After chunking:**
- Router layer: ~35KB (58 symbols) - **86% reduction**
- Service layer: ~45KB (72 symbols) - **82% reduction**
- Repository layer: ~38KB (61 symbols) - **85% reduction**
- Schema layer: ~42KB (68 symbols) - **83% reduction**
- Core layer: ~52KB (85 symbols) - **79% reduction**

### Prerequisites

Must run `add_layer_tags.py` first to assign layer tags.

---

## Symbol Merging: merge_symbols.py

### Purpose

Merges programmatically extracted symbols into existing graphs for incremental updates.

### When to Use

- Incremental updates after code changes
- Avoiding full regeneration
- Maintaining symbol relationships

### Usage

```bash
python .claude/skills/symbols/scripts/merge_symbols.py \
  --domain=<domain> \
  --input=<extracted-symbols-file>
```

### Examples

```bash
# Merge newly extracted UI symbols
python scripts/merge_symbols.py \
  --domain=ui \
  --input=extracted_ui_symbols.json

# Merge API symbols incrementally
python scripts/merge_symbols.py \
  --domain=api \
  --input=extracted_api_symbols.json
```

### Options

- `--domain=<domain>` (required) - Target domain to merge into
- `--input=<file>` (required) - File containing extracted symbols
- `--validate` (optional) - Validate consistency after merge
- `--dry-run` (optional) - Show what would be merged without applying

### Merge Logic

1. Loads existing symbol graph
2. Identifies new, modified, and removed symbols
3. Updates existing symbols or adds new ones
4. Maintains symbol relationships and cross-references
5. Validates for duplicates and consistency

### Output

```
Merging symbols for domain: ui
  New symbols: 5
  Modified symbols: 12
  Removed symbols: 2
  Total symbols: 145
Merge completed successfully.
```

---

## Complete Update Workflows

### Workflow 1: Full Symbol Regeneration

Complete regeneration of all symbol files.

**When to use:**
- Initial setup
- Major code restructuring
- Symbol system corruption

**Steps:**

```bash
# 1. Review configuration
cat .claude/skills/symbols/symbols.config.json

# 2. Extract TypeScript symbols (UI)
python scripts/extract_symbols_typescript.py \
  packages/ui/src \
  --output=ai/symbols-ui.json

# 3. Extract TypeScript symbols (Web)
python scripts/extract_symbols_typescript.py \
  apps/web/src \
  --output=ai/symbols-web.json

# 4. Extract Python symbols (API)
python scripts/extract_symbols_python.py \
  services/api/app \
  --output=ai/symbols-api.json

# 5. Extract shared symbols
python scripts/extract_symbols_typescript.py \
  packages/shared/src \
  --output=ai/symbols-shared.json

# 6. Add layer tags to all files
python scripts/add_layer_tags.py ai/symbols-ui.json
python scripts/add_layer_tags.py ai/symbols-web.json
python scripts/add_layer_tags.py ai/symbols-api.json
python scripts/add_layer_tags.py ai/symbols-shared.json

# 7. OPTIONAL: Chunk backend by layer for efficiency
python scripts/split_api_by_layer.py \
  ai/symbols-api.json \
  --output-dir=ai/

# Result: Complete symbol graph with layer-based access
```

**Time estimate:** 5-10 minutes for medium codebase

---

### Workflow 2: Incremental Domain Update

Update symbols for a specific domain after code changes.

**When to use:**
- Code changes in one domain
- New files added
- Refactoring within domain

**Steps:**

```bash
# 1. Extract updated symbols for domain
python scripts/extract_symbols_typescript.py \
  apps/web/src \
  --output=extracted_web_symbols.json

# 2. Add layer tags
python scripts/add_layer_tags.py extracted_web_symbols.json

# 3. Merge with existing symbols
python scripts/merge_symbols.py \
  --domain=web \
  --input=extracted_web_symbols.json

# 4. Validate merge
python scripts/merge_symbols.py \
  --domain=web \
  --input=extracted_web_symbols.json \
  --validate

# Result: Updated symbols for web domain only
```

**Time estimate:** 1-2 minutes

---

### Workflow 3: Layer-Specific Update

Update symbols for a specific architectural layer.

**When to use:**
- Changes in specific layer only
- Fastest update method
- Layer-based development

**Steps:**

```bash
# 1. Extract symbols from layer directory
python scripts/extract_symbols_python.py \
  services/api/app/services \
  --output=extracted_services.json

# 2. Add layer tags
python scripts/add_layer_tags.py extracted_services.json

# 3. Merge into main symbol file
python scripts/merge_symbols.py \
  --domain=api \
  --input=extracted_services.json

# 4. Re-chunk by layer
python scripts/split_api_by_layer.py \
  ai/symbols-api.json \
  --output-dir=ai/

# Result: Updated service layer only, re-chunked
```

**Time estimate:** 30-60 seconds

---

## Automation with symbols-engineer Agent

### Recommended Approach

Instead of running scripts manually, use the `symbols-engineer` agent:

```python
# Full regeneration
Task("symbols-engineer", "Regenerate all symbol files and chunk by layer")

# Domain-specific update
Task("symbols-engineer", "Update symbols for the API domain after recent changes")

# Incremental update
Task("symbols-engineer", "Perform incremental symbol update for modified files")
```

### Agent Capabilities

The `symbols-engineer` agent:
- Analyzes what needs to be updated
- Runs appropriate scripts in correct order
- Validates output
- Reports results

---

## Validation and Quality Checks

### Manual Validation

```bash
# Check symbol counts
jq '.totalSymbols' ai/symbols-*.json

# Verify layer tags are assigned
jq '.symbols[] | select(.layer == null) | .name' ai/symbols-api.json

# Check for duplicates
jq '.symbols[].name' ai/symbols-ui.json | sort | uniq -d

# Validate JSON structure
jq empty ai/symbols-*.json
```

### Automated Validation

```python
# Run validation script
python scripts/validate_symbols.py ai/symbols-api.json

# Checks:
# - Valid JSON structure
# - Required fields present
# - No duplicate symbols
# - Layer tags assigned
# - File paths valid
```

---

## Troubleshooting

### Issue: Extraction Script Fails

**Symptoms:**
- Script exits with error
- Empty output file
- Incomplete symbol extraction

**Solutions:**

```bash
# 1. Verify source directory exists
ls -la packages/ui/src

# 2. Check Python dependencies
pip install -r requirements.txt

# 3. Run with verbose output
python scripts/extract_symbols_typescript.py \
  packages/ui/src \
  --output=ai/symbols-ui.json \
  --verbose

# 4. Check for syntax errors in source files
# Fix any TypeScript/Python syntax errors first
```

---

### Issue: Layer Tags Not Assigned

**Symptoms:**
- `layer` field is null or missing
- Layer-based queries return no results

**Solutions:**

```bash
# 1. Verify symbols.config.json has layer patterns
cat .claude/skills/symbols/symbols.config.json | jq '.layers'

# 2. Re-run add_layer_tags.py
python scripts/add_layer_tags.py ai/symbols-api.json

# 3. Verify layer tags were added
jq '.symbols[] | select(.layer != null) | {name, layer}' ai/symbols-api.json
```

---

### Issue: Chunking Fails

**Symptoms:**
- Layer-specific files not created
- split_api_by_layer.py exits with error

**Solutions:**

```bash
# 1. Verify layer tags are assigned first
jq '.symbols[0] | .layer' ai/symbols-api.json

# 2. If null, run add_layer_tags.py first
python scripts/add_layer_tags.py ai/symbols-api.json

# 3. Then run chunking
python scripts/split_api_by_layer.py \
  ai/symbols-api.json \
  --output-dir=ai/

# 4. Verify output files created
ls -la ai/symbols-api-*.json
```

---

### Issue: Merge Conflicts

**Symptoms:**
- Duplicate symbols after merge
- Symbols disappear after merge

**Solutions:**

```bash
# 1. Run merge with dry-run first
python scripts/merge_symbols.py \
  --domain=api \
  --input=extracted_symbols.json \
  --dry-run

# 2. Validate before applying
python scripts/merge_symbols.py \
  --domain=api \
  --input=extracted_symbols.json \
  --validate

# 3. If issues persist, do full regeneration
# (See Workflow 1: Full Symbol Regeneration)
```

---

### Issue: Performance Degradation

**Symptoms:**
- Slow symbol loading
- Large symbol files

**Solutions:**

```bash
# 1. Check file sizes
ls -lh ai/symbols-*.json

# 2. If too large, enable layer chunking
# Edit symbols.config.json
{
  "domains": {
    "api": {
      "enableLayerSplit": true
    }
  }
}

# 3. Re-run chunking
python scripts/split_api_by_layer.py \
  ai/symbols-api.json \
  --output-dir=ai/

# 4. Use layer-specific loading in queries
load_api_layer("services", max_symbols=50)
```

---

## Best Practices

### 1. Configuration Management

- Keep `symbols.config.json` in version control
- Document project-specific layer patterns
- Review configuration after major refactoring

### 2. Update Frequency

- **Daily**: Incremental updates for active development
- **Weekly**: Full regeneration during maintenance
- **On-demand**: After major refactoring or restructuring

### 3. Layer Chunking

- Enable for backend APIs with 100+ symbols
- Skip for small codebases or simple structures
- Always run after updating backend symbols

### 4. Automation

- Use `symbols-engineer` agent for orchestration
- Set up git hooks for automatic updates (optional)
- Validate after every update

### 5. Version Control

- Commit symbol files to git (they're artifacts)
- Include in .gitignore if too large
- Document regeneration process in README

---

## Script Reference Summary

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `extract_symbols_typescript.py` | Extract TypeScript/React symbols | Initial extraction, full regeneration |
| `extract_symbols_python.py` | Extract Python symbols | Initial extraction, full regeneration |
| `add_layer_tags.py` | Assign architectural layer tags | After extraction, before querying |
| `split_api_by_layer.py` | Chunk symbols by layer | Backend optimization, after tagging |
| `merge_symbols.py` | Incremental updates | Merge new symbols without full regeneration |
| `validate_symbols.py` | Quality checks | After updates, during CI/CD |

---

## See Also

- **[symbol-api-reference.md](./symbol-api-reference.md)** - Complete API documentation
- **[symbol-workflows-by-role.md](./symbol-workflows-by-role.md)** - Practical workflows
- **[symbol-schema-architecture.md](./symbol-schema-architecture.md)** - Symbol structure specification
- **[symbol-performance-metrics.md](./symbol-performance-metrics.md)** - Performance benchmarks
