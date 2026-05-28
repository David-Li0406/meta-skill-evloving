# Symbols Skill - Token-Efficient Codebase Navigation

A token-efficient codebase symbol analysis system for intelligent code discovery. Query pre-generated symbol graphs chunked by domain (UI, Web, API) instead of loading entire files. **Achieve 95-99% token reduction** compared to traditional file reading.

## What Is This?

The symbols skill enables AI agents to navigate codebases efficiently without loading full files. Query structured metadata about functions, classes, components, hooks, and types - get exact file:line references for immediate lookup.

**Key Benefits:**

- **0.1 second** queries vs **2-3 minute** full scans
- **~$0.001** per query vs **~$0.01-0.02** for exploration
- **Domain chunking**: Load only UI (191KB), API (1.7MB), or Web (~500KB)
- **Layer chunking**: Load only routers, services, repositories for 50-80% reduction
- **Architectural awareness**: 8,888+ symbols tagged by layer (router, service, component, etc.)

## Quick Start

```bash
# 1. Initialize configuration (first time only)
python scripts/init_symbols.py --auto-detect

# 2. Extract symbols
python scripts/extract_symbols_typescript.py apps/web --output=ai/symbols-web.json --exclude-tests
python scripts/extract_symbols_python.py services/api --output=ai/symbols-api.json --exclude-tests

# 3. Add layer tags
python scripts/add_layer_tags.py --all --inplace

# 4. Split API for token efficiency (optional but recommended)
python scripts/split_api_by_layer.py

# 5. Validate
python scripts/validate_symbols.py
```

**See [scripts/README.md](./scripts/README.md) for complete workflows and detailed human guide.**

## Documentation Map

| Document | Purpose | Audience |
|----------|---------|----------|
| **[SKILL.md](./SKILL.md)** | Core AI agent reference - essential capabilities and quick start | AI Agents |
| **[references/](./references/)** | Detailed documentation (API, workflows, architecture, performance) | AI Agents |
| **[scripts/README.md](./scripts/README.md)** | Complete human guide - workflows, configuration, troubleshooting | Developers |
| **[symbols.config.json](./symbols.config.json)** | Project configuration - domains, paths, extraction rules | Configuration |
| **[docs/project_plans/impl_tracking/ai/skill-symbol/](../../docs/project_plans/impl_tracking/ai/skill-symbol/)** | Historical docs and detailed planning | Archive |

### Supporting Documentation (references/)

The skill uses **progressive disclosure** with core instructions in SKILL.md (~245 lines) and detailed documentation in supporting files:

- **[symbol-api-reference.md](./references/symbol-api-reference.md)** - Complete API documentation with all parameters and examples
- **[symbol-workflows-by-role.md](./references/symbol-workflows-by-role.md)** - Development workflows for different roles
- **[symbol-script-operations.md](./references/symbol-script-operations.md)** - Script documentation and update procedures
- **[symbol-schema-architecture.md](./references/symbol-schema-architecture.md)** - Symbol schema and architecture integration
- **[symbol-performance-metrics.md](./references/symbol-performance-metrics.md)** - Performance benchmarks and optimization

## Key Capabilities

1. **Query Symbols** - Find specific code by name, kind, domain, or layer
2. **Load Domains** - Get complete symbol set for UI, Web, or API
3. **Load API Layers** - Load only routers, services, repositories, schemas, or cores
4. **Search Patterns** - Advanced regex search with architectural filtering
5. **Get Context** - Detailed information about specific symbols with related entities

## For Distribution

When sharing this skill with other projects:

**Include:**

```text
.claude/skills/symbols/
├── scripts/                    # All Python tools
├── templates/                  # Configuration templates
├── SKILL.md                   # AI agent reference
├── README.md                  # This file
├── symbols-config-schema.json # Configuration schema
└── docs/                      # Guides (optional)
```

**Exclude:**

- `symbols.config.json` (project-specific)
- `ai/symbols-*.json` (generated files)
- `__pycache__/`, `.pytest_cache/` (build artifacts)

**For New Project:**

1. Copy files listed above to target project
2. Run: `python scripts/init_symbols.py --auto-detect`
3. Extract symbols and validate
4. Start querying via agents or Python API

## MeatyPrompts Configuration

Pre-configured with:

**Domains:**

- `ui` - 755 symbols (191KB) - React components, hooks
- `web` - 1,088 symbols (629KB) - Next.js app router
- `api` - 3,041 symbols (1.8MB) - FastAPI backend

**API Layers** (50-80% token reduction):

- `routers` - 289 symbols (HTTP endpoints)
- `services` - 454 symbols (business logic)
- `repositories` - 387 symbols (data access)
- `schemas` - 570 symbols (DTOs)
- `cores` - 1,341 symbols (auth, observability)

**Test Files** (loaded separately):

- `ui-tests` - 383 symbols
- `api-tests` - 3,621 symbols

## Performance

| Metric | Symbol Query | Full Exploration |
|--------|-------------|------------------|
| Duration | 0.1 seconds | 2-3 minutes |
| Token Usage | ~10KB | ~250KB+ |
| Cost | ~$0.001 | ~$0.01-0.02 |
| Best For | "What and where" | "How and why" |

## Integration with Agents

```markdown
# Quick discovery (0.1s, 95-99% token reduction)
Task("codebase-explorer", "Find all Button component implementations")

# Deep analysis (2-3 min, full context)
Task("explore", "Analyze authentication flow patterns")

# Optimal workflow: Phase 1 → Phase 2
Task("codebase-explorer", "Find repository patterns")
→ Get instant symbol inventory
→ Identify key files

Task("explore", "Analyze patterns in prompt_repository.py")
→ Get full implementation context
```

## Common Tasks

### Query symbols programmatically

```python
from symbol_tools import query_symbols, load_domain, load_api_layer

# Find React components
components = query_symbols(kind="component", domain="ui", limit=20)

# Load web app context
web = load_domain(domain="web", max_symbols=100)

# Load only service layer (84% token reduction)
services = load_api_layer("services", max_symbols=50)
```

### Update symbols after code changes

```bash
# Re-extract changed domain
python scripts/extract_symbols_typescript.py packages/ui --output=ai/symbols-ui.json
python scripts/add_layer_tags.py --input=ai/symbols-ui.json --output=ai/symbols-ui.json
python scripts/validate_symbols.py --domain=ui
```

### Validate symbol files

```bash
# Quick check
python scripts/validate_symbols.py

# Detailed report
python scripts/validate_symbols.py --verbose --json
```

**See [scripts/README.md](./scripts/README.md) for complete workflows.**

## Getting Help

- **Understand the skill**: Read [SKILL.md](./SKILL.md) for AI agent reference
- **Set up symbols**: See [scripts/README.md](./scripts/README.md) for complete workflows
- **Configure for your project**: Run `python scripts/init_symbols.py --auto-detect`
- **Troubleshoot issues**: See [scripts/README.md](./scripts/README.md#troubleshooting)

## Summary

The symbols skill provides **token-efficient codebase navigation** through smart symbol discovery:

- Query specific symbols instead of loading full files (95-99% reduction)
- Load only what you need by domain or architectural layer
- Get precise code references with file:line locations
- Follow architectural patterns (Router → Service → Repository)

**Start with [scripts/README.md](./scripts/README.md) for complete workflows, or [SKILL.md](./SKILL.md) for AI agent integration.**
