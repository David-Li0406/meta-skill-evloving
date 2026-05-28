---
name: Chunk Navigation
description: This skill should be used when the user asks to "create chunks", "navigate phases", "chunk the project", "go to next phase", "show chunk dependencies", or when the /chunk or /navigate commands are invoked. Provides semantic project chunking, phase-based navigation, and context-aware file loading for large projects.
version: 1.0.0
---

# Chunk Navigation Skill

## Purpose

Break large projects into manageable semantic chunks for focused work. Enable efficient navigation between project phases, modules, or functional areas. Automatically load relevant context when navigating to ensure smooth workflow across different project sections.

## Core Concepts

### What is a Chunk?

A chunk is a logical grouping of related files representing a coherent unit of work:
- **Phase-based chunk**: Files for a specific development phase (e.g., "Authentication", "Database Setup")
- **Module-based chunk**: Files within a module or package
- **File-based chunk**: Related files by dependency or function

### Chunk Definition

Each chunk contains:
- **Chunk ID**: Unique identifier
- **Name**: Human-readable title
- **Description**: What this chunk represents
- **Files**: Array of file paths included
- **Dependencies**: Other chunks this depends on
- **Entry points**: Main files to start with
- **Status**: pending, in_progress, completed

### Chunking Strategies

**Phase-based (Recommended):**
- Organize by development phases or milestones
- Examples: "Setup", "Auth Implementation", "API Integration", "Testing"
- Best for: Projects with clear sequential phases

**Module-based:**
- Organize by code modules or packages
- Examples: "user-service", "payment-processor", "notification-system"
- Best for: Microservices, modular monoliths

**File-based:**
- Organize by file relationships and dependencies
- Group files that change together
- Best for: Refactoring, dependency analysis

## When to Use

Use chunk navigation when:
- User explicitly requests chunking with /chunk or similar commands
- Project has >100 files (manual navigation becomes difficult)
- Working on large multi-phase projects
- User asks to "go to next phase", "navigate to X", "show dependencies"
- Need focused context loading (avoid loading entire project)
- Multiple developers working on different project areas

## Chunk Creation Process

### Step 1: Choose Chunking Strategy

Determine appropriate strategy based on project:

```bash
# Check project size
FILE_COUNT=$(find . -type f \( -name "*.py" -o -name "*.rs" -o -name "*.go" \) \
  ! -path "*/venv/*" ! -path "*/target/*" ! -path "*/node_modules/*" | wc -l)

# Determine strategy
if [ $FILE_COUNT -lt 50 ]; then
  STRATEGY="none"  # Small project, chunking not needed
elif [ -f "PLAN.md" ] || [ -d "/root/.claude/plans" ]; then
  STRATEGY="phase-based"  # Plan exists, use phases
elif [ -d "services" ] || [ -d "packages" ]; then
  STRATEGY="module-based"  # Modular structure
else
  STRATEGY="phase-based"  # Default
fi
```

### Step 2: Analyze Project Structure

Scan project to identify natural boundaries:

**For phase-based:**
- Read plan file if exists (extract phases from headers)
- Infer phases from directory structure (setup/, core/, api/, tests/)
- Check git history for logical groupings

**For module-based:**
- Identify top-level modules (services/, packages/, apps/)
- Map each module to a chunk
- Detect shared/common modules

**For file-based:**
- Parse import/dependency graphs
- Group files with high coupling
- Identify independent file clusters

### Step 3: Create Chunk Definitions

Generate `.claude/.chunks.json`:

```json
{
  "strategy": "phase-based",
  "created_at": "2026-01-22T16:00:00Z",
  "chunks": [
    {
      "id": "chunk_phase_1_setup",
      "name": "Phase 1: Project Setup",
      "description": "Initial project configuration, dependencies, and directory structure",
      "files": [
        "README.md",
        "pyproject.toml",
        "Cargo.toml",
        "go.mod",
        "docker-compose.yml"
      ],
      "entry_points": ["README.md"],
      "dependencies": [],
      "status": "completed",
      "completion": 100
    },
    {
      "id": "chunk_phase_2_database",
      "name": "Phase 2: Database Setup",
      "description": "Database schema, migrations, and ORM configuration",
      "files": [
        "src/database/models.py",
        "src/database/migrations/",
        "tests/test_database.py",
        "alembic.ini"
      ],
      "entry_points": ["src/database/models.py"],
      "dependencies": ["chunk_phase_1_setup"],
      "status": "completed",
      "completion": 100
    },
    {
      "id": "chunk_phase_3_api",
      "name": "Phase 3: API Integration",
      "description": "REST API endpoints, authentication, and request handling",
      "files": [
        "src/api/routes/",
        "src/api/auth.py",
        "src/api/middleware.py",
        "tests/test_api.py"
      ],
      "entry_points": ["src/api/main.py"],
      "dependencies": ["chunk_phase_2_database"],
      "status": "in_progress",
      "completion": 65
    }
  ],
  "current_chunk": "chunk_phase_3_api"
}
```

### Step 4: Store Chunk Metadata

Write chunk definitions atomically:

```bash
# Backup existing chunks if present
[ -f .claude/.chunks.json ] && \
  cp .claude/.chunks.json .claude/.chunks.json.bak

# Write new chunks
echo "$CHUNKS_JSON" > .claude/.chunks.json.tmp
mv .claude/.chunks.json.tmp .claude/.chunks.json
```

Store current chunk separately:

```bash
# .claude/.current-chunk.json
{
  "chunk_id": "chunk_phase_3_api",
  "phase_name": "Phase 3: API Integration",
  "completion": 65,
  "loaded_at": "2026-01-22T16:05:00Z"
}
```

## Navigation Patterns

### Sequential Navigation

Move to next or previous chunk:

```bash
# Get current chunk index
CURRENT_ID=$(jq -r '.current_chunk' .claude/.chunks.json)
CURRENT_INDEX=$(jq -r ".chunks | map(.id) | index(\"$CURRENT_ID\")" .claude/.chunks.json)

# Navigate to next chunk
NEXT_INDEX=$((CURRENT_INDEX + 1))
NEXT_CHUNK=$(jq -r ".chunks[$NEXT_INDEX]" .claude/.chunks.json)

# Check if next chunk exists
if [ "$NEXT_CHUNK" != "null" ]; then
  NEXT_ID=$(echo "$NEXT_CHUNK" | jq -r '.id')
  # Update current chunk
  jq ".current_chunk = \"$NEXT_ID\"" .claude/.chunks.json > .claude/.chunks.json.tmp
  mv .claude/.chunks.json.tmp .claude/.chunks.json
fi
```

**Commands:**
- `/navigate --next` - Go to next chunk
- `/navigate --prev` - Go to previous chunk

### Direct Navigation

Jump to specific chunk by name or ID:

```bash
# Find chunk by name (case-insensitive partial match)
SEARCH_TERM="API"
CHUNK=$(jq -r ".chunks[] | select(.name | test(\"$SEARCH_TERM\"; \"i\"))" \
  .claude/.chunks.json | jq -s '.[0]')

# Or by exact ID
CHUNK=$(jq -r ".chunks[] | select(.id == \"chunk_phase_3_api\")" \
  .claude/.chunks.json)

# Update current chunk
CHUNK_ID=$(echo "$CHUNK" | jq -r '.id')
jq ".current_chunk = \"$CHUNK_ID\"" .claude/.chunks.json > .claude/.chunks.json.tmp
mv .claude/.chunks.json.tmp .claude/.chunks.json
```

**Commands:**
- `/navigate --phase "API Integration"` - Jump by name
- `/navigate --id chunk_phase_3_api` - Jump by ID

### Search Navigation

Find chunks matching criteria:

```bash
# Search by status
jq -r '.chunks[] | select(.status == "in_progress") | .name' \
  .claude/.chunks.json

# Search by file
FILE_TO_FIND="src/api/auth.py"
jq -r ".chunks[] | select(.files | index(\"$FILE_TO_FIND\")) | .name" \
  .claude/.chunks.json

# Search by dependency
DEPENDS_ON="chunk_phase_2_database"
jq -r ".chunks[] | select(.dependencies | index(\"$DEPENDS_ON\")) | .name" \
  .claude/.chunks.json
```

**Commands:**
- `/navigate --search "auth"` - Search chunk names
- `/navigate --file "auth.py"` - Find chunk containing file

## Context Loading Strategies

### Load Files on Navigation

When navigating to a chunk, automatically load relevant files:

```bash
# Get files for current chunk
CHUNK_ID=$(jq -r '.current_chunk' .claude/.chunks.json)
CHUNK_FILES=$(jq -r ".chunks[] | select(.id == \"$CHUNK_ID\") | .files[]" \
  .claude/.chunks.json)

# Load entry points first (max 3)
ENTRY_POINTS=$(jq -r ".chunks[] | select(.id == \"$CHUNK_ID\") | .entry_points[]" \
  .claude/.chunks.json)
echo "$ENTRY_POINTS" | head -3 | while read -r file; do
  if [ -f "$file" ]; then
    echo "Loading: $file"
    # Claude Code will read this file
  fi
done

# Load additional files if configured
MAX_ADDITIONAL_FILES=5
echo "$CHUNK_FILES" | grep -v -F -f <(echo "$ENTRY_POINTS") | \
  head -$MAX_ADDITIONAL_FILES | while read -r file; do
  if [ -f "$file" ]; then
    echo "Loading: $file"
  fi
done
```

**Configurable limits:**
- `load_files_on_navigate`: true/false
- `max_auto_load_files`: Number (default 5)
- `prioritize_entry_points`: true/false

### Show Dependencies

Display chunk dependencies when navigating:

```bash
# Get dependencies for current chunk
DEPS=$(jq -r ".chunks[] | select(.id == \"$CHUNK_ID\") | .dependencies[]" \
  .claude/.chunks.json)

if [ -n "$DEPS" ]; then
  echo "Dependencies:"
  echo "$DEPS" | while read -r dep_id; do
    DEP_NAME=$(jq -r ".chunks[] | select(.id == \"$dep_id\") | .name" \
      .claude/.chunks.json)
    DEP_STATUS=$(jq -r ".chunks[] | select(.id == \"$dep_id\") | .status" \
      .claude/.chunks.json)
    echo "  • $DEP_NAME ($DEP_STATUS)"
  done
fi
```

### Show Dependents

Display chunks that depend on current chunk:

```bash
# Find chunks that list current chunk as dependency
DEPENDENTS=$(jq -r ".chunks[] | select(.dependencies | index(\"$CHUNK_ID\")) | .name" \
  .claude/.chunks.json)

if [ -n "$DEPENDENTS" ]; then
  echo "Used by:"
  echo "$DEPENDENTS" | while read -r dependent; do
    echo "  • $dependent"
  done
fi
```

## Dependency Visualization

### Generate Dependency Graph

Create visual representation of chunk relationships:

```bash
# Generate DOT format for graphviz
cat > .claude/.chunk-graph.dot <<EOF
digraph chunks {
  rankdir=LR;
  node [shape=box];

EOF

# Add nodes
jq -r '.chunks[] | "\(.id) [label=\"\(.name)\n\(.completion)%\"];"' \
  .claude/.chunks.json >> .claude/.chunk-graph.dot

# Add edges
jq -r '.chunks[] | . as $chunk | .dependencies[] | "\(.) -> \($chunk.id);"' \
  .claude/.chunks.json >> .claude/.chunk-graph.dot

echo "}" >> .claude/.chunk-graph.dot

# Generate image if graphviz available
if command -v dot &>/dev/null; then
  dot -Tpng .claude/.chunk-graph.dot -o .claude/.chunk-graph.png
  echo "Dependency graph: .claude/.chunk-graph.png"
fi
```

### Text-based Dependency Tree

For terminal display:

```bash
# Recursive function to print tree
print_chunk_tree() {
  local chunk_id=$1
  local indent=$2

  local name=$(jq -r ".chunks[] | select(.id == \"$chunk_id\") | .name" \
    .claude/.chunks.json)
  local status=$(jq -r ".chunks[] | select(.id == \"$chunk_id\") | .status" \
    .claude/.chunks.json)

  echo "${indent}├─ $name ($status)"

  local deps=$(jq -r ".chunks[] | select(.id == \"$chunk_id\") | .dependencies[]" \
    .claude/.chunks.json)

  if [ -n "$deps" ]; then
    echo "$deps" | while read -r dep; do
      print_chunk_tree "$dep" "${indent}│  "
    done
  fi
}

# Print tree for current chunk
CURRENT_CHUNK=$(jq -r '.current_chunk' .claude/.chunks.json)
echo "Chunk Dependencies:"
print_chunk_tree "$CURRENT_CHUNK" ""
```

## Integration with Other Components

### Commands

**`/chunk` command** - Chunk management:
- `--create` - Generate chunks using chosen strategy
- `--list` - Show all chunks
- `--current` - Display current chunk

**`/navigate` command** - Chunk navigation:
- `--next`/`--prev` - Sequential navigation
- `--phase "name"` - Direct navigation
- `--search "term"` - Search chunks

### Session Management

Store current chunk in session state:

```json
{
  "phase": {
    "name": "Phase 3: API Integration",
    "completion": 65,
    "chunk_id": "chunk_phase_3_api"
  }
}
```

Restore chunk on session resume.

### Plan Mode Integration

Extract phases from plan file to create chunks:

```bash
# Parse plan file for phases
PLAN_FILE="/root/.claude/plans/joyful-juggling-scone.md"
if [ -f "$PLAN_FILE" ]; then
  # Extract markdown headers as phases
  grep '^##' "$PLAN_FILE" | while read -r header; do
    PHASE_NAME=$(echo "$header" | sed 's/^## //')
    # Create chunk for this phase
    # Infer files based on phase name...
  done
fi
```

## Configuration

Configure chunking in `.claude/project-context.local.md`:

```yaml
---
# Chunking preferences
chunk_strategy: "phase-based"  # phase-based, module-based, file-based
auto_chunk: true               # Auto-create chunks on project index
chunk_context_lines: 50        # Lines of context around chunks

# Navigation preferences
show_dependencies_on_navigate: true
load_files_on_navigate: 3
syntax_highlighting: true

# Auto-chunk from plans
auto_chunk_plans: true
---
```

## Performance Considerations

**Chunk file limits:**
- Max 100 files per chunk (split if larger)
- Load max 5 files automatically on navigate
- Lazy-load additional files on demand

**Chunk count:**
- Optimal: 5-15 chunks per project
- Max recommended: 30 chunks
- Too few: Chunks too large, defeats purpose
- Too many: Navigation overhead increases

## Additional Resources

### Reference Files

For detailed algorithms and patterns:
- **`references/chunking-algorithms.md`** - Phase/module/file-based strategies
- **`references/dependency-analysis.md`** - Analyzing file relationships
- **`references/navigation-patterns.md`** - Advanced navigation techniques

### Example Files

Working examples in `examples/`:
- **`chunks-phase-based.json`** - Phase-based chunk structure
- **`chunks-module-based.json`** - Module-based chunk structure
- **`chunk-graph.dot`** - GraphViz dependency graph

### Utility Scripts

Helper scripts in `scripts/`:
- **`create-phases.py`** - Semantic phase detection
- **`render-summary.sh`** - Syntax-highlighted chunk summaries
- **`extract-deps.py`** - Show imports/dependencies for chunk
