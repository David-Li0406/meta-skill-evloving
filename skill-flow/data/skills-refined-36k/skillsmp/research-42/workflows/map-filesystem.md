# Workflow: Map Filesystem

**Purpose**: Generate comprehensive filesystem reference document
**Use for**: Creating file-system.md, project onboarding, understanding organization
**Estimated time**: 15-30 minutes
**Output**: `/docs/architecture/file-system.md`

## Overview

This workflow generates a complete project structure reference document that enables AI agents and developers to quickly navigate the codebase, understand where code lives, and know where to add new features.

## Required Tools

- **Bash** - Directory listing (ls commands)
- **Read** - Reading critical configuration files
- **Glob** - File pattern discovery (optional)
- **Write** - Creating output document

## Execution Strategy (FAST METHOD)

Use simple sequential `ls` commands instead of complex `find` operations. This approach is proven to be 3-4x faster and more reliable.

### Step-by-Step Execution

**Phase 1: Setup** (1 tool call)
- Identify project root directory
- Determine source directory structure

**Phase 2: Top-level scan** (1 tool call with parallel commands)
```bash
ls -la <project-root>
ls -d <project-root>/*/
```

**Phase 3: Source directory walk** (1 tool call with parallel commands)
```bash
ls <src-dir>/
ls <src-dir>/subdir1/
ls <src-dir>/subdir2/
ls <src-dir>/subdir3/
```

**Phase 4: Subdirectory details** (1 tool call with parallel commands)
```bash
ls <src-dir>/subdir1/nested/
ls <src-dir>/subdir2/nested/
ls <tests-dir>/
ls <docs-dir>/
```

**Phase 5: Critical files** (1 tool call with parallel reads)
```markdown
Read(package.json or pyproject.toml)
Read(tsconfig.json or setup.py)
Read(pytest.ini or jest.config.js)
Read(README.md)
```

**Phase 6: Generate documentation** (1 tool call)
- Write complete file-system.md

**Total**: 6-7 tool calls vs. 20+ with complex find operations

## Configuration

**Settings**:
- `ROOT_DIR`: Project root path (from context or user input)
- `OUTPUT_FILE`: `docs/architecture/file-system.md`
- `MAX_DEPTH`: 3-4 levels (we list explicitly, not recursively)

**Exclude patterns** (don't list these):
- `.venv*`, `venv`, `node_modules`
- `__pycache__`, `.pytest_cache`, `.mypy_cache`
- `.git`, `.github` (unless documenting CI/CD)
- `dist`, `build`, `target`
- `.next`, `.nuxt`, `.output`
- `coverage`, `.coverage`

## Critical Rules

### DO THIS (Fast & Reliable)

1. **Use ls for listings**
   ```bash
   ls <directory>          # List directory contents
   ls -la <directory>      # List with details
   ls -d <directory>/*/    # List only subdirectories
   ```

2. **Batch commands in parallel**
   ```bash
   # Multiple ls commands in one tool call
   ls /project/src/
   ls /project/tests/
   ls /project/docs/
   ```

3. **Walk directories explicitly**
   - List top level
   - List known important subdirectories
   - List their subdirectories if relevant

4. **Use Glob for file patterns** (if needed)
   ```markdown
   Glob: "**/*.service.ts"
   Glob: "**/*test*.py"
   ```

5. **Use Read for specific files**
   ```markdown
   Read: package.json
   Read: pyproject.toml
   ```

### DON'T DO THIS (Slow & Fails)

1. ❌ Complex find with exclusions
   ```bash
   # SLOW - Don't use
   find . -maxdepth 4 -path ./node_modules -prune ...
   ```

2. ❌ tree command
   ```bash
   # Not always available
   tree -L 3
   ```

3. ❌ Recursive file walks
   ```bash
   # SLOW - Don't use
   find . -type f -name "*.py"
   ```

4. ❌ Trying to count everything at once
   ```bash
   # SLOW - Don't use
   find . -type f | wc -l
   ```

## Output Document Structure

Generate markdown file with these exact sections in order:

### 1. File System Overview

```markdown
# File System Overview

**Purpose**: Comprehensive filesystem reference for {project-name}
**Project Root**: {absolute-path}
**Scan Date**: {YYYY-MM-DD}
**Architecture**: {e.g., Clean Architecture with DI, Monorepo, etc.}

## Summary Statistics

| Metric              | Value            |
| ------------------- | ---------------- |
| Total directories   | {count}          |
| Source files        | {approximate}    |
| Languages detected  | {list}           |
| Largest directories | {top 3-5 with approx counts} |
| Excluded patterns   | {list}           |

**Note**: Statistics are approximate based on directory structure analysis.
```

### 2. Directory Tree (Trimmed)

```markdown
## Directory Tree

.
├── src/
│   └── package/
│       ├── __init__.py
│       ├── main.py
│       ├── module1/
│       │   ├── service.py
│       │   └── model.py
│       ├── module2/
│       │   ├── api.py
│       │   └── schemas.py
│       └── utils/
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
├── .env.example
└── pyproject.toml

**Note**: Large directories shown with (... N files) notation
```

### 3. Folder Index & Responsibilities

For each major directory:

```markdown
### `/src/package/` - Application Source

**Path**: `src/package`
**Role**: Main application source code with modular organization

**Notable contents**:
- `main.py` - Application entry point
- `module1/` - {Module purpose}
- `module2/` - {Module purpose}
- `utils/` - Shared utilities

**Conventions**:
- One module per major feature/domain
- Each module has service, model, and API layers
- Tests mirror source structure

**Entry points**:
- `main.py` - CLI/application startup
- `api.py` files - API endpoints
```

### 4. Critical Files Cheat Sheet

```markdown
## Critical Files Cheat Sheet

| File | What it does | Used by | Notes |
| ---- | ------------ | ------- | ----- |
| `pyproject.toml` | Project dependencies and build config | pip, build tools | Source of truth for deps |
| `src/package/__init__.py` | Package initialization | All imports | Version defined here |
| `src/package/main.py` | Application entry point | CLI, deployment | Contains main() |
| `.env.example` | Environment variable template | Developers | Never commit .env |
```

### 5. Dependency & Navigation Hints

```markdown
## Dependency & Navigation Hints

### Module Boundaries (Architecture)

```
Entry Points (main.py, api.py)
         ↓ uses
Services (business logic)
         ↓ uses
Models (data structures)
         ↓ uses
Database/External APIs
```

### Import Patterns

```python
# Standard import pattern
from package.module1 import Service
from package.module2.schemas import UserSchema

# Avoid circular imports by importing at module level
```

### Common Flows

**API Request Flow**:
```
api.py (endpoint)
  → service.py (business logic)
    → model.py (data access)
      → database
```

**CLI Command Flow**:
```
main.py (command)
  → service.py (business logic)
    → model.py (data access)
```
```

### 6. Patterns & Conventions

```markdown
## Patterns & Conventions

### File Naming
- Source files: `snake_case.py` or `kebab-case.ts`
- Test files: `test_{module}.py` or `{module}.test.ts`
- Config files: Standard names (package.json, tsconfig.json)

### Directory Naming
- Features/modules: `snake_case` or `kebab-case`
- Keep consistent within project

### Test Organization
- **Unit tests**: `tests/unit/test_{module}.py`
  - Mock external dependencies
  - Test single units in isolation
- **Integration tests**: `tests/integration/test_{feature}.py`
  - Use real dependencies
  - Test feature workflows

### Configuration Files

**Development**:
- `pyproject.toml` / `package.json` - Dependencies and scripts
- `pytest.ini` / `jest.config.js` - Test configuration
- `.env.example` - Environment variables template

**Build**:
- `Dockerfile` - Container definition
- `docker-compose.yml` - Local development setup

### Environment Variables

```bash
# Example from .env.example
DATABASE_URL - Database connection string
API_KEY - External API authentication
DEBUG - Enable debug mode (true/false)
```

**Security**: Never commit `.env` file with real secrets
```

### 7. Known Hotspots

```markdown
## Known Hotspots (Maintenance Areas)

### Large Directories
- `src/package/models/` - {count} files
  - **Reason**: One file per database model
  - **Consider**: Group related models into subdirectories

### Generated Content
- `dist/` or `build/` - Build artifacts (not committed)
- `__pycache__/`, `.pytest_cache/` - Python caches (not committed)
- `node_modules/` - Dependencies (not committed)

### Configuration Sprawl
- Multiple config files for different tools
- Consider consolidating where possible

### Future Refactors
- {Note any organization issues discovered}
- {Potential improvements}
```

### 8. Glossary & Path Aliases

```markdown
## Glossary

### Domain Terms
- **{Term}**: Definition relevant to this project
- **{Term}**: Definition

### Common Abbreviations
- **{Abbr}**: What it stands for

### Path Aliases (if configured)

```typescript
// Example from tsconfig.json
{
  "@/": "./src/",
  "@components/": "./src/components/"
}
```
```

### 9. How to Extend the Repo

```markdown
## How to Extend the Repo

### Add a New Feature Module

1. **Create directory**: `src/package/new-feature/`
2. **Add files**:
   - `service.py` - Business logic
   - `model.py` - Data models
   - `api.py` - API endpoints
   - `schemas.py` - Data validation
3. **Add tests**: `tests/unit/test_new_feature.py`
4. **Register**: Update main.py or router if needed
5. **Document**: Update relevant docs

### Add a New API Endpoint

1. **Create/update**: `src/package/module/api.py`
2. **Follow pattern**: Match existing endpoint structure
3. **Add tests**: `tests/integration/test_module_api.py`
4. **Document**: Add to API docs

### Add a New Database Model

1. **Create**: `src/package/models/new_model.py`
2. **Define schema**: Using ORM pattern
3. **Create migration**: Using migration tool
4. **Add tests**: Test model behavior
5. **Update relationships**: Link to related models
```

## Execution Example

For a Python project with structure like AgentMap:

```bash
# Phase 1: Top-level
ls -la /project/root
ls -d /project/root/*/

# Phase 2: Source structure
ls /project/root/src/package/
ls /project/root/src/package/agents/
ls /project/root/src/package/services/
ls /project/root/src/package/models/

# Phase 3: Subdirectories
ls /project/root/src/package/services/storage/
ls /project/root/src/package/services/graph/
ls /project/root/tests/
ls /project/root/docs/

# Phase 4: Read critical files
Read(/project/root/pyproject.toml)
Read(/project/root/pytest.ini)
Read(/project/root/src/package/__init__.py)
Read(/project/root/README.md)

# Phase 5: Write documentation
Write(/project/root/docs/architecture/file-system.md)
```

## Success Criteria

The resulting document enables readers to:
- [ ] Locate files quickly by purpose
- [ ] Understand where to add new code
- [ ] Follow execution flows end-to-end
- [ ] Understand architectural boundaries
- [ ] Find examples and patterns
- [ ] Navigate project structure efficiently

## Output Summary

After generating the document, provide summary:

```markdown
## Filesystem Mapping Complete

**Output**: `/docs/architecture/file-system.md`
**Scanned**: {ROOT_DIR}

**Statistics**:
- Directories analyzed: {count}
- Major sections documented: 9
- Largest directories: {list top 3-5}

**Key sections created**:
✓ Directory tree (trimmed for readability)
✓ Folder responsibilities and conventions
✓ Critical files cheat sheet
✓ Navigation hints and common flows
✓ Extension guides

**Next steps**:
- Review generated documentation
- Customize based on project specifics
- Share with team for onboarding
- Keep updated as structure evolves
```

## Tips & Best Practices

### Do's
1. **Create parent directories** if needed: `mkdir -p docs/architecture`
2. **Use relative paths** in documentation (from project root)
3. **Include real examples** from the codebase
4. **Keep sections in order** for consistency
5. **Update exclusion patterns** based on project type

### Don'ts
1. **Don't use placeholders** - Use actual directory names and counts
2. **Don't over-detail** - Collapse large directories with "... N files"
3. **Don't include sensitive info** - Exclude .env, credentials, secrets
4. **Don't analyze excluded dirs** - Skip node_modules, .venv, etc.
5. **Don't use complex find** - Stick to simple ls commands

### Time Optimization
- **Batch ls commands** in parallel (4-6 per tool call)
- **Skip deep nesting** beyond 3-4 levels
- **Focus on source directories** - tests/docs can be lighter
- **Read only critical config files** - not every file

### Customization
Adapt structure based on project type:
- **Monorepo**: Document workspace structure
- **Microservices**: Show service boundaries
- **Full-stack**: Separate frontend/backend sections
- **Library**: Focus on exports and public API

## Related Workflows

- Use **analyze-codebase** for deeper understanding after mapping
- Use **find-patterns** to document conventions found during mapping
- Output feeds into specification-writing and architecture skills

## Related Context Files

- `../context/documentation-standards.md` - Documentation formatting
- `../context/search-strategies.md` - Directory exploration techniques

## Notes

- File is regenerable - safe to overwrite and update
- Can be run periodically to keep documentation current
- Useful for AI agents and human developers alike
- Forms foundation for other research workflows
