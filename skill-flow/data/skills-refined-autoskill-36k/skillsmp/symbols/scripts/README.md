# Symbols Scripts

Management and extraction scripts for the MeatyPrompts symbols system - a token-efficient codebase indexing system that provides 95-99% token reduction for AI-assisted development.

## What is the Symbols System?

The symbols system pre-generates structured metadata (symbols) about all code entities in the codebase - functions, classes, components, hooks, types, and more. This metadata enables AI agents to quickly locate and understand code without loading full file contents, achieving 95-99% token reduction compared to traditional code reading approaches.

**Key Benefits:**
- **0.1 second** symbol queries vs **2-3 minute** full codebase scans
- **~$0.001** per query vs **~$0.01-0.02** for full exploration
- **Domain chunking**: Load only UI (191KB), API (1.7MB), or Web (~500KB) symbols
- **Layer chunking**: Load only routers, services, repositories, schemas, or cores for 50-80% API token reduction
- **Architectural awareness**: Symbols tagged by layer (router, service, repository, component, hook, etc.)

## Scripts Overview

### Unified Pipeline

| Script | Purpose |
|--------|---------|
| `__main__.py` | **Unified pipeline orchestrator** - runs extract → tag → split → validate in one command |

```bash
# Run full pipeline
python .claude/skills/symbols/scripts/__main__.py

# Domain-specific
python .claude/skills/symbols/scripts/__main__.py --domain=api
python .claude/skills/symbols/scripts/__main__.py --domain=web

# Incremental update (for hooks)
python .claude/skills/symbols/scripts/__main__.py --changed-only --skip-validate

# Skip optional steps
python .claude/skills/symbols/scripts/__main__.py --skip-split --skip-validate
```

### Configuration & Setup

| Script | Purpose |
|--------|---------|
| `init_symbols.py` | Interactive wizard to create/customize symbols.config.json with auto-detection of project structure |
| `config.py` | Configuration loader with graceful fallback; loads symbols.config.json and provides typed access |
| `config_example.py` | Example configuration for reference when customizing your setup |

### Symbol Extraction

| Script | Purpose |
|--------|---------|
| `extract_symbols_typescript.py` | Extract symbols from TypeScript/JavaScript (components, hooks, types, interfaces, functions) |
| `extract_symbols_python.py` | Extract symbols from Python code (classes, functions, methods, async functions) |
| `generate_api_symbols.py` | High-level API symbol generation orchestrator |

### Symbol Processing

| Script | Purpose |
|--------|---------|
| `add_layer_tags.py` | Add architectural layer tags to all symbols based on file path (router, service, repository, etc.) |
| `split_api_by_layer.py` | Split symbols-api.json into 5 layer-specific files for 50-80% token reduction |
| `merge_symbols.py` | Merge newly extracted symbols into existing symbol files with duplicate detection |

### Validation & Testing

| Script | Purpose |
|--------|---------|
| `validate_symbols.py` | Comprehensive validation of symbol files (schema, freshness, duplicates, source integrity) |
| `validate_schema.py` | JSON schema validation for symbol files and configuration |
| `test_init_symbols.py` | Unit tests for init_symbols.py functionality |
| `test_update_claude_md.py` | Unit tests for CLAUDE.md integration |

### Integration & Querying

| Script | Purpose |
|--------|---------|
| `symbol_tools.py` | Core library for loading and querying symbols; used by codebase-explorer agent |
| `update_claude_md.py` | Safely integrate symbols guidance into CLAUDE.md using HTML comment markers |
| `backfill_schema.py` | Migrate old symbol files to latest schema version |

## Configuration: symbols.config.json

The `symbols.config.json` file is the central configuration that defines:

1. **Project metadata**: Name, version, description
2. **Symbols directory**: Where symbol files are stored (default: `ai/`)
3. **Domains**: High-level groupings (ui, web, api, shared) with separate files
4. **API Layers**: Fine-grained backend splits (routers, services, repositories, schemas, cores)
5. **Extraction paths**: Which directories to scan for each language
6. **Exclusion patterns**: What to skip (node_modules, tests, __pycache__, etc.)

### Configuration Structure

```json
{
  "projectName": "MeatyPrompts",
  "symbolsDir": "ai",
  "domains": {
    "ui": {
      "file": "symbols-ui.json",
      "description": "UI primitives - components, hooks, utilities",
      "testFile": "symbols-ui-tests.json",
      "enabled": true
    },
    "web": {
      "file": "symbols-web.json",
      "description": "Next.js app - pages, app router, web-specific code"
    },
    "api": {
      "file": "symbols-api.json",
      "description": "Unified backend API symbols",
      "testFile": "symbols-api-tests.json"
    }
  },
  "apiLayers": {
    "routers": {
      "file": "symbols-api-routers.json",
      "description": "API route handlers - FastAPI routers"
    },
    "services": {
      "file": "symbols-api-services.json",
      "description": "Business logic services"
    },
    "repositories": {
      "file": "symbols-api-repositories.json",
      "description": "Data access layer - DB queries, RLS"
    },
    "schemas": {
      "file": "symbols-api-schemas.json",
      "description": "DTOs - Pydantic models for serialization"
    },
    "cores": {
      "file": "symbols-api-cores.json",
      "description": "Core utilities - auth, observability, middleware"
    }
  },
  "extraction": {
    "python": {
      "directories": ["services/api"],
      "extensions": [".py"],
      "excludes": ["__pycache__", "*.pyc", ".pytest_cache"],
      "excludeTests": true
    },
    "typescript": {
      "directories": ["apps/web", "apps/mobile", "packages/ui"],
      "extensions": [".ts", ".tsx", ".js", ".jsx"],
      "excludes": ["node_modules/", "*.test.*", "dist/", ".next/"],
      "excludeTests": true
    }
  }
}
```

### Creating Configuration

```bash
# Interactive wizard with auto-detection (recommended)
python scripts/init_symbols.py

# Auto-detect without prompts
python scripts/init_symbols.py --auto-detect

# Quick setup with template
python scripts/init_symbols.py --template=react-typescript-fullstack

# List available templates
python scripts/init_symbols.py --list

# See what would be created (dry-run)
python scripts/init_symbols.py --dry-run
```

The wizard detects:
- Package managers (pnpm, npm, yarn, uv, poetry)
- Monorepo type (pnpm-workspace, turborepo, lerna)
- Backend code (Python/FastAPI, Node.js)
- Frontend code (React, Next.js, Vue)
- Mobile code (React Native, Expo)
- Shared packages
- **Package-based structures** (e.g., `mypackage/api/`, `mypackage/web/`) - detects Python packages with `__init__.py` and looks for code subdirectories within them

## Complete Lifecycle

### Quick Start: Unified Pipeline

The fastest way to generate symbols is using the unified pipeline:

```bash
# 1. Initialize configuration (one-time)
python .claude/skills/symbols/scripts/init_symbols.py --auto-detect

# 2. Run full pipeline (extract → tag → split → validate)
python .claude/skills/symbols/scripts/__main__.py

# Or domain-specific
python .claude/skills/symbols/scripts/__main__.py --domain=api
python .claude/skills/symbols/scripts/__main__.py --domain=web
```

### Manual Steps (Alternative)

For more control, you can run individual scripts:

### 1. Initialize Configuration

```bash
# Create symbols.config.json with auto-detection
cd /path/to/project
python .claude/skills/symbols/scripts/init_symbols.py --auto-detect

# Result: symbols.config.json created with detected paths
```

### 2. Extract Symbols

Extract symbols from source code using the configured paths:

```bash
# Extract TypeScript symbols from all configured directories
python scripts/extract_symbols_typescript.py apps/web \
  --output=ai/symbols-web-raw.json \
  --exclude-tests

python scripts/extract_symbols_typescript.py packages/ui \
  --output=ai/symbols-ui-raw.json \
  --exclude-tests

# Extract Python symbols from backend
python scripts/extract_symbols_python.py services/api \
  --output=ai/symbols-api-raw.json \
  --exclude-tests

# The scripts read symbols.config.json to determine:
# - Which directories to scan
# - What file extensions to include
# - What patterns to exclude
```

### 3. Add Layer Tags

Add architectural layer tags to all symbols:

```bash
# Tag all symbols based on file paths
python scripts/add_layer_tags.py \
  --input ai/symbols-api-raw.json \
  --output ai/symbols-api.json

python scripts/add_layer_tags.py \
  --input ai/symbols-ui-raw.json \
  --output ai/symbols-ui.json

# Process all configured symbol files at once
python scripts/add_layer_tags.py --all --inplace
```

Layer tags identify architectural role:
- **Backend**: `router`, `service`, `repository`, `schema`, `model`, `core`, `auth`, `middleware`
- **Frontend**: `component`, `hook`, `page`, `util`
- **Test**: `test`

### 4. Split API by Layer (Optional but Recommended)

Split the large API symbol file into layer-specific chunks for 50-80% token reduction:

```bash
# Split symbols-api.json into 5 layer files
python scripts/split_api_by_layer.py

# Result: Creates 5 files in ai/ directory:
# - symbols-api-routers.json (HTTP endpoints)
# - symbols-api-services.json (business logic)
# - symbols-api-repositories.json (data access)
# - symbols-api-schemas.json (DTOs and types)
# - symbols-api-cores.json (auth, observability, utilities)

# Validate without splitting
python scripts/split_api_by_layer.py --validate-only

# See what would happen
python scripts/split_api_by_layer.py --dry-run
```

### 5. Validate Symbols

Validate all symbol files for correctness:

```bash
# Validate all domains
python scripts/validate_symbols.py

# Validate specific domain
python scripts/validate_symbols.py --domain=ui

# Verbose output
python scripts/validate_symbols.py --verbose

# Exit codes for CI/CD:
# 0 = Valid (no errors or warnings)
# 1 = Warnings (stale files, minor issues)
# 2 = Errors (missing files, schema violations)
```

### 6. Query Symbols

Use `symbol_tools.py` in your code or via the codebase-explorer agent:

```python
from symbol_tools import load_domain, load_api_layer, search_patterns

# Load entire domain
ui_symbols = load_domain('ui')
web_symbols = load_domain('web')

# Load specific API layer (50-80% token reduction)
routers = load_api_layer('routers')
services = load_api_layer('services')
repositories = load_api_layer('repositories')

# Search across domains with layer filtering
results = search_patterns(
    ['Button', 'PromptCard'],
    domains=['ui'],
    layers=['component']
)
```

### 7. Integrate with CLAUDE.md (Optional)

Add symbols guidance to your CLAUDE.md:

```bash
# Safely add symbols section to CLAUDE.md
python scripts/update_claude_md.py

# Dry run to see changes
python scripts/update_claude_md.py --dry-run

# Specify project root
python scripts/update_claude_md.py --project-root /path/to/project
```

Uses HTML comment markers for safe updates:
```markdown
<!-- BEGIN SYMBOLS SECTION -->
...symbols guidance...
<!-- END SYMBOLS SECTION -->
```

## Layer-Based Chunking

The API domain is split into 5 layer-specific files for token efficiency:

### Layer Architecture

```
symbols-api.json (unified, 3,041 symbols, ~1.7MB)
    ↓ split_api_by_layer.py
    ├── symbols-api-routers.json      (HTTP entry points)
    ├── symbols-api-services.json     (business logic)
    ├── symbols-api-repositories.json (data access)
    ├── symbols-api-schemas.json      (DTOs/types)
    └── symbols-api-cores.json        (auth, observability, utils)
```

### Layer Mapping (from symbols.config.json)

Symbols are assigned to layers based on their file path:

```python
LAYER_PATH_MAPPING = {
    'router': ['app/api/', 'app/api/endpoints/'],
    'service': ['app/services/'],
    'repository': ['app/repositories/'],
    'schema': ['app/schemas/'],
    'core': ['app/core/', 'app/db/', 'app/models/', 'auth/',
             'app/middleware/', 'app/cache/', 'app/observability/']
}
```

### Usage Patterns

```python
# Working on API routes? Load only routers (fastest)
from symbol_tools import load_api_layer
routers = load_api_layer('routers')

# Working on business logic? Load only services
services = load_api_layer('services')

# Need data layer? Load only repositories
repos = load_api_layer('repositories')

# Working on DTOs? Load only schemas
schemas = load_api_layer('schemas')

# Need auth/observability? Load cores
cores = load_api_layer('cores')

# Token Savings:
# - Full API: ~1.7MB (3,041 symbols)
# - Single layer: ~200-400KB (50-80% reduction)
```

## Common Workflows

### Workflow 1: Initial Setup for New Project

```bash
# 1. Initialize configuration
cd /path/to/project
python .claude/skills/symbols/scripts/init_symbols.py --auto-detect

# 2. Extract all symbols
python scripts/extract_symbols_typescript.py apps/web --output=ai/symbols-web-raw.json --exclude-tests
python scripts/extract_symbols_typescript.py packages/ui --output=ai/symbols-ui-raw.json --exclude-tests
python scripts/extract_symbols_python.py services/api --output=ai/symbols-api-raw.json --exclude-tests

# 3. Add layer tags to all
python scripts/add_layer_tags.py --all --inplace

# 4. Split API for token efficiency
python scripts/split_api_by_layer.py

# 5. Validate everything
python scripts/validate_symbols.py

# 6. Integrate with CLAUDE.md
python scripts/update_claude_md.py
```

### Workflow 2: Update Symbols After Code Changes

```bash
# 1. Re-extract changed domain (e.g., UI after adding components)
python scripts/extract_symbols_typescript.py packages/ui \
  --output=ai/symbols-ui-new.json \
  --exclude-tests

# 2. Merge with existing symbols
python scripts/merge_symbols.py \
  --domain=ui \
  --input=ai/symbols-ui-new.json \
  --validate \
  --backup

# 3. Re-tag with layers
python scripts/add_layer_tags.py --input=ai/symbols-ui.json --output=ai/symbols-ui.json

# 4. Validate
python scripts/validate_symbols.py --domain=ui
```

### Workflow 3: Add New Backend Feature

```bash
# 1. Extract updated API symbols
python scripts/extract_symbols_python.py services/api \
  --output=ai/symbols-api-new.json \
  --exclude-tests

# 2. Merge into existing
python scripts/merge_symbols.py \
  --domain=api \
  --input=ai/symbols-api-new.json \
  --validate \
  --backup

# 3. Add layer tags
python scripts/add_layer_tags.py --input=ai/symbols-api.json --output=ai/symbols-api.json

# 4. Re-split by layers
python scripts/split_api_by_layer.py

# 5. Validate
python scripts/validate_symbols.py --domain=api
```

### Workflow 4: Debug Symbol Issues

```bash
# 1. Validate with verbose output
python scripts/validate_symbols.py --verbose

# 2. Check specific domain
python scripts/validate_symbols.py --domain=api --verbose

# 3. Validate schema compliance
python scripts/validate_schema.py ai/symbols-ui.json

# 4. Check layer split integrity
python scripts/split_api_by_layer.py --validate-only
```

### Workflow 5: Migrate Old Symbol Files

```bash
# Backfill old symbol files to latest schema
python scripts/backfill_schema.py ai/symbols-api.json

# Then re-tag and re-split
python scripts/add_layer_tags.py --input=ai/symbols-api.json --output=ai/symbols-api.json
python scripts/split_api_by_layer.py
```

## Symbol File Schema

All symbol files follow this schema:

```typescript
{
  "metadata": {
    "version": "2.0",
    "generated": "2025-11-03T18:00:00Z",
    "source": "MeatyPrompts monorepo",
    "symbolCount": 755
  },
  "symbols": [
    {
      "name": "PromptCard",
      "kind": "component",
      "path": "packages/ui/src/components/PromptCard.tsx",
      "line": 42,
      "signature": "function PromptCard(props: PromptCardProps): JSX.Element",
      "summary": "Display a prompt with metadata and actions",
      "layer": "component"  // Added by add_layer_tags.py
    },
    {
      "name": "get_prompt",
      "kind": "function",
      "path": "services/api/app/repositories/prompt_repository.py",
      "line": 127,
      "signature": "async def get_prompt(db: Session, prompt_id: str, user_id: str) -> Optional[Prompt]",
      "summary": "Retrieve a single prompt by ID with RLS enforcement",
      "layer": "repository"
    }
  ]
}
```

### Symbol Kinds

**TypeScript/JavaScript:**
- `component` - React components
- `hook` - Custom React hooks (useXxx)
- `interface` - TypeScript interfaces
- `type` - Type aliases
- `function` - Regular functions
- `class` - Class declarations

**Python:**
- `class` - Class declarations
- `function` - Module-level functions
- `method` - Class methods
- `async_function` - Async functions
- `async_method` - Async methods

### Architectural Layers

- **router** - HTTP endpoints (FastAPI routers)
- **service** - Business logic services
- **repository** - Data access layer (DB queries, RLS)
- **schema** - DTOs (Pydantic models for serialization)
- **model** - ORM models (SQLAlchemy)
- **core** - Core utilities (auth, config, error handling)
- **auth** - Authentication and authorization
- **middleware** - HTTP middleware
- **observability** - Logging, tracing, metrics
- **component** - UI components
- **hook** - React hooks
- **page** - Next.js pages
- **util** - Utility functions
- **test** - Test code

## Performance Comparison

| Approach | Duration | Token Usage | Cost | Best For |
|----------|----------|-------------|------|----------|
| **Symbol Query** | 0.1s | ~10KB | ~$0.001 | "What and where" - finding code |
| **Full Exploration** | 2-3 min | ~250KB+ | ~$0.01-0.02 | "How and why" - understanding patterns |

**Token Efficiency Example:**

Traditional approach (reading 5-10 similar files):
- Context loaded: ~250KB
- Time: 30-60 seconds

Symbol-based approach:
- Context loaded: ~10KB (96% reduction)
- Time: 0.1 seconds
- Load specific files only after finding them

## Integration with Agents

The symbols system is used by the `codebase-explorer` agent:

```markdown
# Quick discovery (0.1s, 95-99% token reduction)
Task("codebase-explorer", "Find all Button component implementations")

# Deep analysis (2-3 min, full context)
Task("explore", "Analyze authentication flow in detail")

# Optimal workflow: Phase 1 → Phase 2
Task("codebase-explorer", "Find all repository patterns")
→ Get instant symbol inventory
→ Identify key files (e.g., prompt_repository.py:127)

Task("explore", "Analyze repository patterns in prompt_repository.py and user_repository.py")
→ Get full implementation context
→ Generate pattern recommendations
```

## CI/CD Integration

```bash
# Validate symbols in CI
python scripts/validate_symbols.py
exit_code=$?

if [ $exit_code -eq 2 ]; then
  echo "Symbol validation failed"
  exit 1
elif [ $exit_code -eq 1 ]; then
  echo "Symbol validation warnings"
  # Optional: fail or continue
fi

# Update symbols automatically
python scripts/extract_symbols_typescript.py apps/web --output=ai/symbols-web.json
python scripts/extract_symbols_python.py services/api --output=ai/symbols-api.json
python scripts/add_layer_tags.py --all --inplace
python scripts/split_api_by_layer.py
git add ai/symbols-*.json
git commit -m "chore: update symbols"
```

## Troubleshooting

### Configuration not found
```bash
# Run init wizard
python scripts/init_symbols.py --auto-detect
```

### Stale symbols (validation warnings)
```bash
# Re-extract and update
python scripts/extract_symbols_typescript.py <path> --output=<domain>.json
python scripts/add_layer_tags.py --input=<domain>.json --output=<domain>.json
```

### Schema validation errors
```bash
# Check schema version
python scripts/validate_schema.py ai/symbols-api.json

# Backfill to latest schema
python scripts/backfill_schema.py ai/symbols-api.json
```

### Layer split issues
```bash
# Validate split without writing
python scripts/split_api_by_layer.py --validate-only

# Re-run split
python scripts/split_api_by_layer.py
```

## Files Generated

After running the complete lifecycle, you'll have:

```
ai/
├── symbols-ui.json              (755 symbols, ~191KB)
├── symbols-ui-tests.json        (383 symbols, test helpers)
├── symbols-web.json             (1,088 symbols, ~500KB)
├── symbols-api.json             (3,041 symbols, ~1.7MB, unified)
├── symbols-api-routers.json     (HTTP endpoints)
├── symbols-api-services.json    (business logic)
├── symbols-api-repositories.json (data access)
├── symbols-api-schemas.json     (DTOs)
├── symbols-api-cores.json       (core utilities)
└── symbols-api-tests.json       (3,621 symbols, test helpers)
```

## Best Practices

1. **Run extraction regularly** - After significant code changes
2. **Use layer chunking** - Split API symbols for token efficiency
3. **Validate before committing** - Catch issues early
4. **Keep configuration updated** - Re-run init_symbols.py when project structure changes
5. **Use backup flag** - When merging symbols, use `--backup` to preserve old versions
6. **Exclude tests by default** - Load test symbols only when debugging tests
7. **Query before reading** - Use codebase-explorer to find code, then read specific files

## See Also

- `/docs/development/symbols-best-practices.md` - Comprehensive usage guide
- `/docs/testing/symbols_vs_explore_validation_report.md` - Performance validation
- `symbols.config.json` - Active configuration
- `symbol_tools.py` - Core query library
