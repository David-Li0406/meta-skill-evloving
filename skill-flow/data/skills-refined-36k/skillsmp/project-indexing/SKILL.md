---
name: Project Indexing
description: This skill should be used when the user asks to "index the project", "scan project structure", "detect languages", "analyze dependencies", "generate project index", or when the /index-project command is invoked. Provides polyglot language detection, dependency extraction, and automated index generation for multi-language codebases.
version: 1.0.0
---

# Project Indexing Skill

## Purpose

Analyze and index multi-language project structures to enable efficient navigation, understanding, and context-aware operations. Generate comprehensive project metadata including language breakdown, dependency graphs, key file identification, and structural organization.

## Supported Languages

This skill detects and analyzes 8 programming languages:

- **Python** - .py files, requirements.txt, setup.py, pyproject.toml, Pipfile
- **Rust** - .rs files, Cargo.toml, Cargo.lock
- **Go** - .go files, go.mod, go.sum
- **Julia** - .jl files, Project.toml, Manifest.toml
- **Elixir** - .ex, .exs files, mix.exs, mix.lock
- **C++** - .cpp, .cc, .cxx, .h, .hpp files, CMakeLists.txt, Makefile
- **Zig** - .zig files, build.zig
- **JavaScript/TypeScript** - .js, .ts, .jsx, .tsx files, package.json, package-lock.json

## When to Use

Index projects when:
- User explicitly requests indexing with /index-project or similar commands
- Entering a new project directory for the first time
- Significant file structure changes detected (10+ new/deleted files)
- Index is stale (>24 hours old) and user is working on code
- Switching between projects in multi-project workflow
- User asks about project structure, languages, or dependencies

## Core Indexing Process

### Step 1: Language Detection

Scan project directory recursively to identify programming languages:

**File-based detection:**
```bash
# Count files by extension
find . -type f -name "*.py" | wc -l    # Python
find . -type f -name "*.rs" | wc -l    # Rust
find . -type f -name "*.go" | wc -l    # Go
# ... repeat for all 8 languages
```

**Manifest-based confirmation:**
```bash
# Verify language presence via package managers
[ -f requirements.txt ] && echo "Python confirmed"
[ -f Cargo.toml ] && echo "Rust confirmed"
[ -f go.mod ] && echo "Go confirmed"
# ... check all manifest files
```

**Output structure:**
```json
{
  "languages": {
    "Python": {
      "file_count": 145,
      "percentage": 45.2,
      "primary": true
    },
    "Rust": {
      "file_count": 89,
      "percentage": 27.8,
      "primary": false
    }
  }
}
```

### Step 2: Dependency Extraction

Parse package manifests to extract dependencies:

**Python dependencies:**
```bash
# requirements.txt
grep -v '^#' requirements.txt | grep -v '^$' | cut -d'=' -f1 | cut -d'>' -f1 | cut -d'<' -f1

# pyproject.toml
grep '^\[tool.poetry.dependencies\]' -A 50 pyproject.toml | grep '=' | cut -d'=' -f1 | tr -d ' '
```

**Rust dependencies:**
```bash
# Cargo.toml [dependencies] section
sed -n '/^\[dependencies\]/,/^\[/p' Cargo.toml | grep '=' | cut -d'=' -f1 | tr -d ' '
```

**Go dependencies:**
```bash
# go.mod require statements
grep '^[[:space:]]*require' go.mod | awk '{print $2}'
```

**JavaScript dependencies:**
```bash
# package.json dependencies + devDependencies
jq -r '.dependencies | keys[]' package.json
jq -r '.devDependencies | keys[]' package.json
```

**Output structure:**
```json
{
  "dependencies": {
    "Python": ["requests", "numpy", "pandas"],
    "Rust": ["tokio", "serde", "anyhow"],
    "Go": ["github.com/gin-gonic/gin"]
  }
}
```

### Step 3: Key File Identification

Identify critical files for quick navigation:

**Entry points:**
- Python: `main.py`, `__main__.py`, `app.py`, `manage.py`
- Rust: `src/main.rs`, `src/lib.rs`
- Go: Files with `package main` and `func main()`
- JavaScript: `index.js`, `server.js`, `app.js`

**Configuration files:**
- `.env`, `.env.example`, `config.yaml`, `settings.py`
- Docker: `Dockerfile`, `docker-compose.yml`
- CI/CD: `.github/workflows/*.yml`, `.gitlab-ci.yml`

**Documentation:**
- `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`
- `docs/` directory contents
- `CLAUDE.md` for project-specific AI guidance

**Test directories:**
- Python: `tests/`, `test_*.py`, `*_test.py`
- Rust: `tests/`, `*_test.rs`
- Go: `*_test.go`
- JavaScript: `__tests__/`, `*.test.js`, `*.spec.js`

**Output structure:**
```json
{
  "key_files": {
    "entry_points": ["src/main.rs", "scripts/server.py"],
    "configs": [".env.example", "config/production.yaml"],
    "documentation": ["README.md", "docs/architecture.md"],
    "tests": ["tests/", "src/lib_test.rs"]
  }
}
```

### Step 4: Project Structure Analysis

Analyze directory organization patterns:

**Detect architecture patterns:**
- Monorepo: Multiple language roots, shared workspace configs
- Microservices: Multiple service directories with independent configs
- Monolith: Single language, standard directory structure
- Library: `src/` + `tests/` + language-specific packaging

**Directory categorization:**
```bash
# Identify directory purposes
[[ -d "src" ]] && echo "Source directory: src/"
[[ -d "tests" || -d "test" ]] && echo "Test directory: tests/"
[[ -d "docs" ]] && echo "Documentation: docs/"
[[ -d "scripts" ]] && echo "Utilities: scripts/"
[[ -d "config" ]] && echo "Configuration: config/"
```

**Output structure:**
```json
{
  "structure": {
    "architecture": "monorepo",
    "root_dirs": ["src", "tests", "docs", "config", "scripts"],
    "depth": 5,
    "total_files": 320,
    "total_size_mb": 12.4
  }
}
```

### Step 5: Generate Index JSON

Create `.claude/.project-index.json` with complete metadata:

**Full index schema:**
```json
{
  "indexed_at": "2026-01-22T15:30:00Z",
  "project_root": "/home/ubuntu/qenex",
  "languages": {
    "Python": {"file_count": 145, "percentage": 45.2, "primary": true},
    "Rust": {"file_count": 89, "percentage": 27.8, "primary": false}
  },
  "dependencies": {
    "Python": ["requests", "numpy"],
    "Rust": ["tokio", "serde"]
  },
  "key_files": {
    "entry_points": ["src/main.rs"],
    "configs": [".env.example"],
    "documentation": ["README.md"],
    "tests": ["tests/"]
  },
  "structure": {
    "architecture": "monorepo",
    "root_dirs": ["src", "tests", "docs"],
    "depth": 5,
    "total_files": 320,
    "total_size_mb": 12.4
  },
  "git": {
    "branch": "master",
    "has_changes": true,
    "last_commit": "a34a001"
  }
}
```

**Write atomically with backup:**
```bash
# Create backup if exists
[ -f .claude/.project-index.json ] && \
  cp .claude/.project-index.json .claude/.project-index.json.bak

# Write new index
echo "$INDEX_JSON" > .claude/.project-index.json.tmp
mv .claude/.project-index.json.tmp .claude/.project-index.json
```

## Automation and Triggers

### Auto-Indexing Conditions

Automatically trigger indexing when:

1. **Project switch detected** - Working directory changed to new project
2. **Index missing** - `.claude/.project-index.json` doesn't exist
3. **Index stale** - Last indexed >24 hours ago
4. **Significant changes** - 10+ files added/deleted since last index
5. **User request** - Explicit /index-project command or "scan project"

### Update Strategy

**Incremental updates:**
- Language counts: Re-scan only changed directories
- Dependencies: Re-parse only modified manifest files
- Key files: Quick check for new entry points

**Full re-index:**
- User explicit request
- Architecture pattern changes detected
- Major restructuring (50+ files changed)

## Integration with Other Components

### Commands

**`/index-project`** - Invokes full project indexing
- Calls this skill for language detection and analysis
- Displays progress during scan
- Shows summary after completion

**`/context-summary`** - Uses index for project overview
- Reads `.claude/.project-index.json`
- Displays language breakdown and structure

**`/chunk`** - Uses index for semantic chunking
- Language data informs chunk boundaries
- Dependency graph guides related file grouping

### Agents

**`project-indexer` agent** - Autonomous indexing
- Monitors project state for triggers
- Invokes this skill automatically
- Updates index in background

**`context-tracker` agent** - Session management
- Checks index freshness on SessionStart
- Warns if index is stale (>24 hours)

### Hooks

**SessionStart hook** - Initial check
- Reads existing index if present
- Calculates index age
- Suggests re-indexing if stale

## Output and Feedback

### User-Facing Messages

**During indexing:**
```
Scanning project structure...
  • Detected 3 languages: Python (45%), Rust (28%), Go (27%)
  • Found 234 dependencies across 3 package managers
  • Identified 12 entry points and 45 test files
  • Analyzing directory structure...

✓ Index generated: .claude/.project-index.json (2.4 KB)
```

**Quick summary:**
```
Project: qenex-trading-platform
Languages: Python (primary), Rust, Go
Dependencies: 234 total (Python: 89, Rust: 78, Go: 67)
Structure: Monorepo with 5 root directories
Last indexed: 2 hours ago
```

### Error Handling

**Missing tools:**
```bash
# Check required tools
command -v jq >/dev/null || echo "Warning: jq not found, JSON parsing limited"
command -v git >/dev/null || echo "Warning: git not found, version info unavailable"
```

**Parse failures:**
- Skip malformed manifest files with warning
- Continue indexing other components
- Log errors to `.claude/.index-errors.log`

**Permission issues:**
- Skip directories without read access
- Note restricted paths in index
- Warn user about incomplete scan

## Performance Considerations

**Large projects (1000+ files):**
- Use `find -print0 | xargs -0` for efficient file counting
- Parallel language detection with background processes
- Cache results for unchanged directories

**Optimization flags:**
```bash
# Exclude common ignore patterns upfront
find . -type f \
  ! -path "*/node_modules/*" \
  ! -path "*/.git/*" \
  ! -path "*/venv/*" \
  ! -path "*/__pycache__/*"
```

**Timeout limits:**
- Max 60 seconds for full index
- Abort if exceeds threshold
- Suggest targeted re-index for huge repos

## Additional Resources

### Reference Files

For detailed implementation guidance:
- **`references/language-detection.md`** - Complete detection algorithms for all 8 languages
- **`references/dependency-parsing.md`** - Package manager parsing techniques
- **`references/index-schema.md`** - Full JSON schema specification

### Example Files

Working examples in `examples/`:
- **`sample-index.json`** - Complete index example for polyglot project
- **`monorepo-index.json`** - Index structure for monorepo architecture

### Utility Scripts

Helper scripts in `scripts/`:
- **`detect-languages.py`** - Comprehensive language detection
- **`scan-dependencies.sh`** - Extract dependencies from all package managers
- **`generate-index.py`** - Create index JSON from collected data
