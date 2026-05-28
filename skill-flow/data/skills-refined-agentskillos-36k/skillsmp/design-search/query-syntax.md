# Search Query Syntax and Patterns

Query patterns, search strategies, and command syntax for design documentation
search.

## Search Strategies

### Strategy 1: Keyword Search

Simple keyword or phrase search:

```bash
grep -rin "cache optimization" .claude/design/
```

**Best for:**

- Finding specific topics
- Locating documentation mentions
- Quick lookups

**Examples:**

```bash
# Single keyword
grep -rin "observability" .claude/design/

# Phrase search
grep -rin "event-based architecture" .claude/design/

# Case-sensitive
grep -rn "EventEmitter" .claude/design/
```

### Strategy 2: Multi-Term Search

Search for multiple related terms:

```bash
grep -rin "cache.*optimization\|optimization.*cache" .claude/design/
```

**Best for:**

- Flexible term ordering
- Related concepts
- Variations in terminology

**Examples:**

```bash
# Either term order
grep -rin "type.*loading\|loading.*type" .claude/design/

# Multiple alternatives
grep -rin "cache\|caching\|cached" .claude/design/

# Word boundaries
grep -rinw "cache" .claude/design/
```

### Strategy 3: Section-Specific Search

Search within specific sections only:

1. Read all docs
2. Extract section content
3. Search within section
4. Return with section context

**Best for:**

- Finding all decisions (Rationale sections)
- Finding implementations (Current State)
- Finding future work (Future Enhancements)

**Process:**

```bash
# For each doc:
# 1. Read file
# 2. Extract section between ## Rationale and next ##
# 3. Search within that section
# 4. Return with section context
```

### Strategy 4: Metadata Search

Search by frontmatter metadata:

```bash
# Find all performance docs
grep -l "category: performance" .claude/design/**/*.md

# Find all current status docs
grep -l "status: current" .claude/design/**/*.md

# Find docs updated recently
grep -l "updated: 2026-01" .claude/design/**/*.md
```

**Best for:**

- Finding docs by category
- Finding docs by status
- Finding docs by module
- Finding recently updated docs

## Search Patterns

### Pattern 1: Find Decisions

Search for design decisions:

**Query variations:**

- "why did we"
- "decision:"
- "options considered"
- "chosen because"
- "trade-off"
- "alternatives"

**Target section:** Rationale

**Example queries:**

```bash
# Decision rationale
grep -rin "decision:" .claude/design/

# Alternatives considered
grep -rin "options considered\|alternatives" .claude/design/

# Trade-offs
grep -rin "trade-off\|tradeoff" .claude/design/
```

### Pattern 2: Find Implementations

Search for current implementation:

**Query variations:**

- "implemented"
- "current implementation"
- "src/"
- "location:"
- "packages/"
- "pkgs/"

**Target section:** Current State, Implementation Details

**Example queries:**

```bash
# Implementation locations
grep -rin "src/.*\.ts" .claude/design/

# Current state
grep -rin "current implementation\|currently implemented" .claude/design/

# File references
grep -rin "packages/\|pkgs/" .claude/design/
```

### Pattern 3: Find TODOs

Search for future work:

**Query variations:**

- "TODO"
- "future"
- "planned"
- "Phase 1/2/3"
- "enhancement"
- "roadmap"

**Target section:** Future Enhancements

**Example queries:**

```bash
# TODO items
grep -rin "TODO\|FIXME\|XXX" .claude/design/

# Planned work
grep -rin "planned\|future" .claude/design/

# Phased work
grep -rin "Phase [123]" .claude/design/
```

### Pattern 4: Find Trade-offs

Search for trade-offs:

**Query variations:**

- "trade-off"
- "sacrifice"
- "cost:"
- "gain:"
- "downside"
- "benefit"

**Target section:** Rationale, Trade-offs

**Example queries:**

```bash
# Trade-offs
grep -rin "trade-off\|tradeoff" .claude/design/

# Cost-benefit analysis
grep -rin "cost:.*gain:\|benefit.*downside" .claude/design/

# Sacrifices
grep -rin "sacrifice\|gave up" .claude/design/
```

## Query Operators

### Grep Options

**Case sensitivity:**

```bash
# Case-insensitive (default recommended)
grep -rin "query" path/

# Case-sensitive
grep -rn "Query" path/
```

**Word boundaries:**

```bash
# Match whole words only
grep -rinw "cache" path/

# Allows partial matches
grep -rin "cache" path/
```

**Context lines:**

```bash
# 2 lines before and after (default)
grep -rin -C 2 "query" path/

# 5 lines before and after
grep -rin -C 5 "query" path/

# 3 before, 2 after
grep -rin -B 3 -A 2 "query" path/
```

**File filtering:**

```bash
# Only markdown files
grep -rin "query" path/ --include="*.md"

# Exclude specific files
grep -rin "query" path/ --exclude="README.md"
```

### Regular Expressions

**Basic patterns:**

```bash
# Either/or
grep -rin "cache\|caching" path/

# Any character
grep -rin "type.loading" path/

# Start of line
grep -rin "^## Overview" path/

# End of line
grep -rin "complete$" path/
```

**Advanced patterns:**

```bash
# Optional character
grep -rin "optimizations\?" path/

# One or more
grep -rin "cache[sd]\+" path/

# Character class
grep -rin "optimization[123]" path/

# Range
grep -rin "[0-9]\{1,3\}%" path/
```

## Query Best Practices

### Start Broad, Then Narrow

1. **Initial broad search:**

   ```bash
   grep -rin "performance" .claude/design/
   ```

2. **Add category filter:**

   ```bash
   grep -l "category: performance" .claude/design/**/*.md | \
     xargs grep -rin "optimization"
   ```

3. **Add section filter:**
   Search Rationale sections in performance docs

### Use Multiple Searches

For complex queries, combine results:

```bash
# Find docs about caching
grep -l "caching\|cache" .claude/design/**/*.md

# Then search within those for optimization
grep -rin "optimization" {cached-doc-list}
```

### Leverage Frontmatter

Filter by metadata before content search:

```bash
# Find current architecture docs
grep -l "status: current" .claude/design/**/*.md | \
  xargs grep -l "category: architecture" | \
  xargs grep -rin "your query"
```

## Common Query Patterns

### Find All Architecture Docs

```bash
grep -l "category: architecture" .claude/design/**/*.md
```

### Find Recent Updates

```bash
# Updated in last 30 days (manual date check)
grep -l "updated: 2026-01" .claude/design/**/*.md
```

### Find Incomplete Docs

```bash
# Stub status
grep -l "status: stub" .claude/design/**/*.md

# Low completeness
grep -l "completeness: [0-2][0-9]" .claude/design/**/*.md
```

### Find Related Docs

```bash
# Has cross-references
grep -l "^related:" .claude/design/**/*.md

# Specific related doc
grep -l "related:.*observability" .claude/design/**/*.md
```

### Find Code References

```bash
# TypeScript files
grep -rin "\.ts[\"']" .claude/design/

# Package names
grep -rin "@effect/\|effect-type-registry" .claude/design/

# File paths
grep -rin "src/.*\.ts\|packages/" .claude/design/
```

## Output Formatting

### Show Line Numbers

```bash
# With line numbers (default)
grep -rn "query" path/

# Without line numbers
grep -r "query" path/
```

### Show File Names Only

```bash
# List matching files
grep -rl "query" path/

# Count matches per file
grep -rc "query" path/
```

### Show Context

```bash
# Compact context
grep -rin -C 2 "query" path/

# More context for understanding
grep -rin -C 5 "query" path/

# Full paragraph context
grep -rin -C 10 "query" path/
```

## Performance Tips

### Limit Search Scope

```bash
# Search specific module
grep -rin "query" .claude/design/effect-type-registry/

# Search specific file pattern
grep -rin "query" .claude/design/**/*-architecture.md
```

### Use File Lists

For multiple searches on same set:

```bash
# Create file list once
ARCH_DOCS=$(grep -l "category: architecture" .claude/design/**/*.md)

# Reuse for multiple queries
echo "$ARCH_DOCS" | xargs grep -rin "query1"
echo "$ARCH_DOCS" | xargs grep -rin "query2"
```

### Exclude Large Sections

```bash
# Skip example code blocks
grep -rin "query" path/ | grep -v "^[[:space:]]*```"
```
