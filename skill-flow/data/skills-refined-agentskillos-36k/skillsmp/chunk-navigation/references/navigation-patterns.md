# Navigation Patterns

Advanced navigation techniques and patterns for chunk-based project navigation.

## Overview

Effective navigation patterns enable moving between chunks efficiently, loading relevant context automatically, and maintaining workflow continuity. This document covers sequential, search-based, dependency-driven, and hybrid navigation patterns.

## Sequential Navigation

Move through chunks in defined order.

### Linear Forward/Backward

**Pattern:** Navigate to next or previous chunk in list.

```bash
#!/bin/bash
# Navigate to next chunk

CHUNKS_FILE=".claude/.chunks.json"
CURRENT_ID=$(jq -r '.current_chunk' "$CHUNKS_FILE")
CURRENT_INDEX=$(jq -r ".chunks | map(.id) | index(\"$CURRENT_ID\")" "$CHUNKS_FILE")

NEXT_INDEX=$((CURRENT_INDEX + 1))
TOTAL_CHUNKS=$(jq -r '.chunks | length' "$CHUNKS_FILE")

if [ "$NEXT_INDEX" -lt "$TOTAL_CHUNKS" ]; then
  NEXT_ID=$(jq -r ".chunks[$NEXT_INDEX].id" "$CHUNKS_FILE")
  NEXT_NAME=$(jq -r ".chunks[$NEXT_INDEX].name" "$CHUNKS_FILE")

  # Update current chunk
  jq ".current_chunk = \"$NEXT_ID\"" "$CHUNKS_FILE" > "$CHUNKS_FILE.tmp"
  mv "$CHUNKS_FILE.tmp" "$CHUNKS_FILE"

  echo "Navigated to: $NEXT_NAME"
else
  echo "Already at last chunk"
fi
```

**Use cases:**
- Phase-based development following plan
- Code review of entire project
- Systematic testing of all modules

**Advantages:**
- Predictable progression
- No chunks skipped
- Simple to implement

**Disadvantages:**
- May navigate to irrelevant chunks
- Ignores chunk dependencies
- Fixed order may not match workflow

### Completion-Based Progression

**Pattern:** Navigate to next incomplete chunk.

```bash
#!/bin/bash
# Navigate to next incomplete chunk

CHUNKS_FILE=".claude/.chunks.json"
CURRENT_INDEX=$(jq -r ".chunks | map(.id) | index(\"$(jq -r '.current_chunk' "$CHUNKS_FILE")\")" "$CHUNKS_FILE")

# Find next incomplete chunk after current
NEXT_CHUNK=$(jq -r ".chunks[$((CURRENT_INDEX + 1)):] |
  map(select(.status != \"completed\")) |
  first |
  .id" "$CHUNKS_FILE")

if [ "$NEXT_CHUNK" != "null" ]; then
  jq ".current_chunk = \"$NEXT_CHUNK\"" "$CHUNKS_FILE" > "$CHUNKS_FILE.tmp"
  mv "$CHUNKS_FILE.tmp" "$CHUNKS_FILE"

  NEXT_NAME=$(jq -r ".chunks[] | select(.id == \"$NEXT_CHUNK\") | .name" "$CHUNKS_FILE")
  echo "Navigated to: $NEXT_NAME"
else
  echo "All chunks completed!"
fi
```

**Use cases:**
- Resume work after interruption
- Focus on unfinished work only
- Track project progress

**Advantages:**
- Skips completed work
- Shows real progress
- Efficient for long projects

**Disadvantages:**
- May skip chunks needing review
- Completion status must be maintained
- "Completed" definition varies

### Priority-Based Navigation

**Pattern:** Navigate to highest priority incomplete chunk.

```bash
#!/bin/bash
# Navigate to highest priority chunk

CHUNKS_FILE=".claude/.chunks.json"

# Find incomplete chunk with highest priority
# Assume priority field: 1 (high), 2 (medium), 3 (low)
NEXT_CHUNK=$(jq -r '.chunks |
  map(select(.status != "completed")) |
  sort_by(.priority) |
  first |
  .id' "$CHUNKS_FILE")

if [ "$NEXT_CHUNK" != "null" ]; then
  jq ".current_chunk = \"$NEXT_CHUNK\"" "$CHUNKS_FILE" > "$CHUNKS_FILE.tmp"
  mv "$CHUNKS_FILE.tmp" "$CHUNKS_FILE"

  NEXT_NAME=$(jq -r ".chunks[] | select(.id == \"$NEXT_CHUNK\") | .name" "$CHUNKS_FILE")
  PRIORITY=$(jq -r ".chunks[] | select(.id == \"$NEXT_CHUNK\") | .priority" "$CHUNKS_FILE")
  echo "Navigated to: $NEXT_NAME (Priority: $PRIORITY)"
else
  echo "All chunks completed!"
fi
```

**Use cases:**
- Critical-path development
- Bug fixing (severity-based)
- Deadline-driven projects

**Advantages:**
- Focus on important work
- Flexible ordering
- Adapts to changing priorities

**Disadvantages:**
- Requires priority maintenance
- May create context switching
- Dependencies ignored

## Search-Based Navigation

Find chunks matching criteria.

### Name-Based Search

**Pattern:** Find chunk by name substring.

```bash
#!/bin/bash
# Search for chunk by name

CHUNKS_FILE=".claude/.chunks.json"
SEARCH_TERM="$1"

MATCHING_CHUNKS=$(jq -r ".chunks[] |
  select(.name | test(\"$SEARCH_TERM\"; \"i\")) |
  \"\(.id): \(.name)\"" "$CHUNKS_FILE")

if [ -z "$MATCHING_CHUNKS" ]; then
  echo "No chunks found matching: $SEARCH_TERM"
  exit 1
fi

echo "Matching chunks:"
echo "$MATCHING_CHUNKS"

# Navigate to first match
FIRST_MATCH=$(echo "$MATCHING_CHUNKS" | head -1 | cut -d: -f1)
jq ".current_chunk = \"$FIRST_MATCH\"" "$CHUNKS_FILE" > "$CHUNKS_FILE.tmp"
mv "$CHUNKS_FILE.tmp" "$CHUNKS_FILE"

CHUNK_NAME=$(jq -r ".chunks[] | select(.id == \"$FIRST_MATCH\") | .name" "$CHUNKS_FILE")
echo "Navigated to: $CHUNK_NAME"
```

**Use cases:**
- Jump to known chunk quickly
- Resume specific work area
- Access related functionality

**Advantages:**
- Fast direct access
- Natural query interface
- Supports partial matches

**Disadvantages:**
- Requires knowing chunk names
- Multiple matches need disambiguation
- Case sensitivity issues

### File-Based Search

**Pattern:** Find chunk containing specific file.

```bash
#!/bin/bash
# Find chunk containing file

CHUNKS_FILE=".claude/.chunks.json"
FILE_PATH="$1"

CHUNK_ID=$(jq -r ".chunks[] |
  select(.files | index(\"$FILE_PATH\")) |
  .id" "$CHUNKS_FILE" | head -1)

if [ -z "$CHUNK_ID" ]; then
  echo "No chunk found containing: $FILE_PATH"
  exit 1
fi

jq ".current_chunk = \"$CHUNK_ID\"" "$CHUNKS_FILE" > "$CHUNKS_FILE.tmp"
mv "$CHUNKS_FILE.tmp" "$CHUNKS_FILE"

CHUNK_NAME=$(jq -r ".chunks[] | select(.id == \"$CHUNK_ID\") | .name" "$CHUNKS_FILE")
echo "Navigated to chunk containing $FILE_PATH:"
echo "  $CHUNK_NAME"
```

**Use cases:**
- Navigate from file to chunk
- Find context for specific file
- IDE integration

**Advantages:**
- Context-aware navigation
- Works from any file
- Natural for file-focused work

**Disadvantages:**
- File must be in exactly one chunk
- Shared files ambiguous
- Requires file path normalization

### Tag-Based Search

**Pattern:** Find chunks with specific tags.

```bash
#!/bin/bash
# Search chunks by tag

CHUNKS_FILE=".claude/.chunks.json"
TAG="$1"

MATCHING_CHUNKS=$(jq -r ".chunks[] |
  select(.tags | index(\"$TAG\")) |
  \"\(.id): \(.name)\"" "$CHUNKS_FILE")

if [ -z "$MATCHING_CHUNKS" ]; then
  echo "No chunks found with tag: $TAG"
  exit 1
fi

echo "Chunks with tag '$TAG':"
echo "$MATCHING_CHUNKS" | nl

# Let user select
read -p "Enter chunk number: " choice
SELECTED_ID=$(echo "$MATCHING_CHUNKS" | sed -n "${choice}p" | cut -d: -f1)

jq ".current_chunk = \"$SELECTED_ID\"" "$CHUNKS_FILE" > "$CHUNKS_FILE.tmp"
mv "$CHUNKS_FILE.tmp" "$CHUNKS_FILE"
```

**Example tags:** `security`, `performance`, `refactoring`, `deprecated`

**Use cases:**
- Navigate by concern
- Filter chunks by category
- Cross-cutting features

**Advantages:**
- Flexible categorization
- Multiple tags per chunk
- Query by concern

**Disadvantages:**
- Requires tag maintenance
- Tag taxonomy must be consistent
- Too many tags reduce usefulness

## Dependency-Driven Navigation

Navigate based on chunk relationships.

### Dependency-First Traversal

**Pattern:** Navigate to dependencies before dependent chunks.

```python
def navigate_dependencies_first(chunks_data):
    """Return chunks in dependency order."""
    chunk_map = {c["id"]: c for c in chunks_data["chunks"]}
    visited = set()
    ordered = []

    def visit(chunk_id):
        if chunk_id in visited:
            return
        visited.add(chunk_id)

        chunk = chunk_map[chunk_id]
        for dep_id in chunk["dependencies"]:
            if dep_id in chunk_map:
                visit(dep_id)

        ordered.append(chunk_id)

    for chunk_id in chunk_map:
        visit(chunk_id)

    return ordered

# Navigate through chunks in dependency order
ordered_ids = navigate_dependencies_first(chunks)
for chunk_id in ordered_ids:
    navigate_to_chunk(chunk_id)
    # Work on chunk...
```

**Use cases:**
- Build systems (compile dependencies first)
- Testing (test dependencies before dependents)
- Learning unfamiliar codebase

**Advantages:**
- Respects dependencies
- Logical progression
- Prevents missing context

**Disadvantages:**
- May be slow for large graphs
- Circular dependencies problematic
- Strict ordering inflexible

### Critical Path Navigation

**Pattern:** Navigate through longest dependency chain.

```python
def find_critical_path(chunks_data):
    """Find longest dependency chain."""
    chunk_map = {c["id"]: c for c in chunks_data["chunks"]}

    def depth(chunk_id, visited):
        if chunk_id in visited:
            return 0

        visited.add(chunk_id)
        chunk = chunk_map[chunk_id]

        if not chunk["dependencies"]:
            return 1

        max_depth = 0
        for dep_id in chunk["dependencies"]:
            if dep_id in chunk_map:
                d = depth(dep_id, visited.copy())
                max_depth = max(max_depth, d)

        return max_depth + 1

    # Find chunk with longest path
    depths = {c_id: depth(c_id, set()) for c_id in chunk_map}
    sorted_chunks = sorted(depths.items(), key=lambda x: x[1], reverse=True)

    # Build path from longest to root
    longest_id = sorted_chunks[0][0]
    path = []

    def build_path(chunk_id):
        path.append(chunk_id)
        chunk = chunk_map[chunk_id]

        if chunk["dependencies"]:
            # Follow first dependency
            dep_id = chunk["dependencies"][0]
            if dep_id in chunk_map:
                build_path(dep_id)

    build_path(longest_id)
    return list(reversed(path))
```

**Use cases:**
- Project planning
- Risk analysis
- Timeline estimation

**Advantages:**
- Identifies critical work
- Helps parallelization planning
- Shows bottlenecks

**Disadvantages:**
- Complex calculation
- May not reflect actual workflow
- Single path ignores alternatives

### Related Chunks Navigation

**Pattern:** Show chunks related to current chunk.

```bash
#!/bin/bash
# Find chunks related to current chunk

CHUNKS_FILE=".claude/.chunks.json"
CURRENT_ID=$(jq -r '.current_chunk' "$CHUNKS_FILE")

# Find chunks that depend on current (dependents)
DEPENDENTS=$(jq -r ".chunks[] |
  select(.dependencies | index(\"$CURRENT_ID\")) |
  \"\(.id): \(.name)\"" "$CHUNKS_FILE")

# Find chunks current depends on (dependencies)
DEPENDENCIES=$(jq -r ".chunks[] |
  select(.id as \$dep |
    (.chunks[] | select(.id == \"$CURRENT_ID\") | .dependencies | index(\$dep))) |
  \"\(.id): \(.name)\"" "$CHUNKS_FILE")

echo "Current chunk: $(jq -r ".chunks[] | select(.id == \"$CURRENT_ID\") | .name" "$CHUNKS_FILE")"
echo ""

if [ -n "$DEPENDENCIES" ]; then
  echo "Dependencies (chunks this depends on):"
  echo "$DEPENDENCIES" | sed 's/^/  • /'
  echo ""
fi

if [ -n "$DEPENDENTS" ]; then
  echo "Dependents (chunks that depend on this):"
  echo "$DEPENDENTS" | sed 's/^/  • /'
fi
```

**Use cases:**
- Understanding context
- Impact analysis
- Related work discovery

**Advantages:**
- Shows relationships
- Bidirectional view
- Helps planning

**Disadvantages:**
- May show too many chunks
- Requires well-defined dependencies
- Graph visualization better

## Context Loading Strategies

Automatically load relevant files on navigation.

### Entry Point Loading

**Pattern:** Load primary files first.

```bash
#!/bin/bash
# Load entry points on navigation

CHUNKS_FILE=".claude/.chunks.json"
CURRENT_ID=$(jq -r '.current_chunk' "$CHUNKS_FILE")

# Get entry points
ENTRY_POINTS=$(jq -r ".chunks[] |
  select(.id == \"$CURRENT_ID\") |
  .entry_points[]" "$CHUNKS_FILE")

echo "Loading entry points:"
echo "$ENTRY_POINTS" | while read -r file; do
  if [ -f "$file" ]; then
    echo "  • $file"
    # Claude Code will read this file
  fi
done
```

**Use cases:**
- Quick chunk overview
- Start new work
- Code review

**Advantages:**
- Fast loading
- Most important files first
- Minimal context

**Disadvantages:**
- May miss important files
- Entry points must be well-chosen
- Limited context for complex work

### Smart File Loading

**Pattern:** Load files based on recent edits and importance.

```python
def smart_file_loading(chunk, max_files=5):
    """Intelligently select files to load."""
    files = chunk["files"]

    # Score each file
    scores = {}
    for file in files:
        score = 0

        # Entry point boost
        if file in chunk.get("entry_points", []):
            score += 10

        # Recent edit boost
        mtime = os.path.getmtime(file)
        age_hours = (time.time() - mtime) / 3600
        if age_hours < 24:
            score += 5
        elif age_hours < 168:  # 1 week
            score += 2

        # File size penalty (avoid huge files)
        size_kb = os.path.getsize(file) / 1024
        if size_kb > 1000:
            score -= 5

        # Test file penalty (load after implementation)
        if "test" in file:
            score -= 2

        scores[file] = score

    # Sort by score and take top N
    sorted_files = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [f for f, _ in sorted_files[:max_files]]
```

**Use cases:**
- Resume interrupted work
- Load active development files
- Efficient context loading

**Advantages:**
- Adapts to workflow
- Loads relevant files
- Efficient use of context

**Disadvantages:**
- Complex heuristics
- May miss important files
- Requires tuning

### Lazy Loading

**Pattern:** Load files on demand as needed.

```python
class LazyChunkLoader:
    def __init__(self, chunk):
        self.chunk = chunk
        self.loaded_files = set()

    def load_entry_points(self):
        """Load entry points immediately."""
        for file in self.chunk.get("entry_points", []):
            self.load_file(file)

    def load_file(self, file):
        """Load single file."""
        if file in self.loaded_files:
            return

        with open(file) as f:
            content = f.read()

        self.loaded_files.add(file)
        return content

    def load_related(self, file):
        """Load files related to given file."""
        # Load files in same directory
        dir_files = [f for f in self.chunk["files"]
                     if os.path.dirname(f) == os.path.dirname(file)]

        for f in dir_files:
            if f not in self.loaded_files:
                self.load_file(f)
```

**Use cases:**
- Large chunks (>50 files)
- Limited context window
- Exploratory navigation

**Advantages:**
- Minimal initial load
- Scales to large chunks
- Responsive navigation

**Disadvantages:**
- May need multiple loads
- Requires user interaction
- Slower than eager loading

## Navigation State Management

Track navigation history and patterns.

### Navigation History

**Pattern:** Maintain stack of visited chunks.

```python
class NavigationHistory:
    def __init__(self, max_size=20):
        self.history = []
        self.current_index = -1
        self.max_size = max_size

    def navigate_to(self, chunk_id):
        """Navigate to chunk, adding to history."""
        # Remove forward history
        self.history = self.history[:self.current_index + 1]

        # Add new chunk
        self.history.append(chunk_id)

        # Limit size
        if len(self.history) > self.max_size:
            self.history.pop(0)
        else:
            self.current_index += 1

    def back(self):
        """Navigate backward in history."""
        if self.current_index > 0:
            self.current_index -= 1
            return self.history[self.current_index]
        return None

    def forward(self):
        """Navigate forward in history."""
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            return self.history[self.current_index]
        return None

    def get_current(self):
        """Get current chunk."""
        if self.current_index >= 0:
            return self.history[self.current_index]
        return None
```

**Use cases:**
- Browser-like navigation
- Backtrack after exploration
- Session continuity

**Advantages:**
- Familiar pattern
- Easy backtracking
- Preserves workflow

**Disadvantages:**
- Memory overhead
- May grow large
- Needs size limits

### Breadcrumbs

**Pattern:** Show path to current chunk.

```bash
#!/bin/bash
# Generate breadcrumb trail

CHUNKS_FILE=".claude/.chunks.json"
CURRENT_ID=$(jq -r '.current_chunk' "$CHUNKS_FILE")

# Build path by following dependencies
breadcrumbs=()
chunk_id="$CURRENT_ID"

while [ "$chunk_id" != "null" ]; do
  chunk_name=$(jq -r ".chunks[] | select(.id == \"$chunk_id\") | .name" "$CHUNKS_FILE")
  breadcrumbs=("$chunk_name" "${breadcrumbs[@]}")

  # Get first dependency
  chunk_id=$(jq -r ".chunks[] | select(.id == \"$chunk_id\") | .dependencies[0] // null" "$CHUNKS_FILE")
done

# Print breadcrumb trail
echo "Path: ${breadcrumbs[*]// / → }"
```

**Output:** `Path: Setup → Core Implementation → API Integration → Authentication`

**Use cases:**
- Show context
- Understanding position
- Documentation

**Advantages:**
- Shows context clearly
- Helps orientation
- Useful for complex projects

**Disadvantages:**
- Linear path only
- Doesn't show alternatives
- May be long

## Performance Optimization

Optimize navigation for large projects.

### Chunk Index

**Pattern:** Build search index for fast queries.

```python
class ChunkIndex:
    def __init__(self, chunks_data):
        self.chunks = {c["id"]: c for c in chunks_data["chunks"]}
        self.name_index = {}
        self.file_index = {}
        self.tag_index = {}

        self.build_indexes()

    def build_indexes(self):
        """Build search indexes."""
        for chunk_id, chunk in self.chunks.items():
            # Name index (lowercase for case-insensitive search)
            name_lower = chunk["name"].lower()
            for word in name_lower.split():
                if word not in self.name_index:
                    self.name_index[word] = []
                self.name_index[word].append(chunk_id)

            # File index
            for file in chunk.get("files", []):
                self.file_index[file] = chunk_id

            # Tag index
            for tag in chunk.get("tags", []):
                if tag not in self.tag_index:
                    self.tag_index[tag] = []
                self.tag_index[tag].append(chunk_id)

    def search_by_name(self, query):
        """Search chunks by name."""
        query_lower = query.lower()
        results = set()

        for word in query_lower.split():
            if word in self.name_index:
                results.update(self.name_index[word])

        return [self.chunks[c_id] for c_id in results]

    def find_by_file(self, file):
        """Find chunk containing file."""
        chunk_id = self.file_index.get(file)
        if chunk_id:
            return self.chunks[chunk_id]
        return None
```

**Advantages:**
- Fast lookups
- Supports multiple query types
- Scalable

**Disadvantages:**
- Memory overhead
- Needs updates on changes
- Build time

### Chunk Caching

**Pattern:** Cache loaded chunk data.

```python
from functools import lru_cache

class CachedChunkLoader:
    def __init__(self, chunks_file):
        self.chunks_file = chunks_file

    @lru_cache(maxsize=128)
    def load_chunk_metadata(self, chunk_id):
        """Load chunk metadata with caching."""
        with open(self.chunks_file) as f:
            chunks_data = json.load(f)

        for chunk in chunks_data["chunks"]:
            if chunk["id"] == chunk_id:
                return chunk

        return None

    @lru_cache(maxsize=32)
    def load_chunk_files(self, chunk_id):
        """Load all files in chunk with caching."""
        chunk = self.load_chunk_metadata(chunk_id)
        if not chunk:
            return None

        file_contents = {}
        for file in chunk["files"]:
            with open(file) as f:
                file_contents[file] = f.read()

        return file_contents
```

**Advantages:**
- Reduces I/O
- Faster repeated access
- Automatic eviction

**Disadvantages:**
- Stale data possible
- Memory usage
- Cache invalidation needed

## Integration Patterns

Integrate chunk navigation with other tools.

### IDE Integration

**Pattern:** Sync IDE with chunk navigation.

```python
def sync_ide_workspace(chunk_id, ide="vscode"):
    """Open files from chunk in IDE."""
    chunk = load_chunk_metadata(chunk_id)
    files = chunk.get("entry_points", chunk["files"][:5])

    if ide == "vscode":
        # Open files in VS Code
        subprocess.run(["code"] + files)

    elif ide == "vim":
        # Open files in vim
        subprocess.run(["vim", "-p"] + files)
```

**Use cases:**
- Seamless workflow
- Multi-tool development
- Context synchronization

### Git Integration

**Pattern:** Navigate based on git activity.

```bash
#!/bin/bash
# Navigate to most recently changed chunk

CHUNKS_FILE=".claude/.chunks.json"

# Find files changed recently
RECENT_FILES=$(git diff --name-only HEAD~10..HEAD)

# Find chunk containing most recent files
declare -A chunk_counts

echo "$RECENT_FILES" | while read -r file; do
  chunk_id=$(jq -r ".chunks[] | select(.files | index(\"$file\")) | .id" "$CHUNKS_FILE" | head -1)

  if [ -n "$chunk_id" ]; then
    ((chunk_counts[$chunk_id]++))
  fi
done

# Navigate to chunk with most activity
most_active=$(printf '%s\n' "${!chunk_counts[@]}" | \
  sort -rn -t: -k2 | head -1 | cut -d: -f1)

if [ -n "$most_active" ]; then
  jq ".current_chunk = \"$most_active\"" "$CHUNKS_FILE" > "$CHUNKS_FILE.tmp"
  mv "$CHUNKS_FILE.tmp" "$CHUNKS_FILE"
fi
```

## Additional Resources

For implementation:
- `../SKILL.md` - Core chunk navigation concepts
- `../scripts/create-phases.py` - Chunk generation
- `chunking-algorithms.md` - Chunk creation strategies
- `dependency-analysis.md` - Dependency graph building
