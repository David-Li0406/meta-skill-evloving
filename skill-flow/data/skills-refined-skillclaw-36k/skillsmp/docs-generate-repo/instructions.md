# Repository Documentation Generation Instructions

Detailed step-by-step instructions for generating Level 2 repository
documentation.

## Implementation Steps

### Step 1: Load Configuration

```bash
# Read design configuration
cat .claude/design/design.config.json
```

Extract:

- Module path and design docs path
- Repository docs configuration
- Quality standards for Level 2
- Output directory structure

### Step 2: Load Design Documentation

```bash
# Find all design docs for module
find .claude/design/{module.designDocsPath} -name "*.md" -type f
```

For each design doc:

- Read frontmatter (status, category, completeness)
- Parse main sections
- Extract code examples
- Identify integration points

### Step 3: Identify Documentation Topics

Map design doc categories to user-facing topics:

**From design doc categories:**

- `architecture` → Architecture overview, Components, Data flow
- `performance` → Performance guide, Optimization tips
- `observability` → Monitoring and logging guide
- `integration` → Integration guides by tool

**Topic extraction rules:**

1. One architecture overview doc (combines multiple architecture design docs)
2. One guide per major feature/capability
3. One integration guide per external tool
4. One troubleshooting doc (combines issues from all design docs)

### Step 4: Generate Architecture Documentation

**File:** `docs/architecture/overview.md`

**Content from design docs:**

- High-level system design
- Major components and their roles
- Data flow through the system
- Key design decisions (simplified)

**Transformation:**

- Remove implementation details
- Focus on user-observable behavior
- Add diagrams where helpful
- Explain "why" certain design choices benefit users

### Step 5: Generate Topic Guides

For each identified topic, create `docs/guides/{topic}.md`:

**Structure:**

1. **Overview** - What this topic covers
2. **Concepts** - Key concepts explained simply
3. **Usage** - How to use this feature
4. **Examples** - Basic and advanced examples
5. **API Reference** - Related API methods
6. **Troubleshooting** - Common issues

**Content extraction:**

- Find design docs related to topic
- Extract usage patterns
- Simplify code examples
- Add troubleshooting from known issues

### Step 6: Generate Integration Guides

For each external tool integration:

**File:** `docs/integration/{tool}.md`

**Content:**

- Why integrate with this tool
- Installation and setup
- Configuration example
- Complete working example
- Common patterns
- Troubleshooting

**Example tools:**

- RSPress (for rspress-plugin-api-extractor)
- Twoslash (for effect-type-registry)
- Effect-TS (for packages using Effect)

### Step 7: Generate Getting Started Guide

**File:** `docs/guides/getting-started.md`

**Content:**

- Installation (detailed)
- First example (step-by-step)
- Common patterns
- Next steps

**Difference from README quick start:**

- More detailed explanations
- Multiple examples
- Configuration options
- Link to specific guides

### Step 8: Create Documentation Index

**File:** `docs/README.md`

**Content:**

- Brief description
- Documentation structure
- Links to all guides organized by category
- Quick navigation

**Example structure:**

```markdown
# {Module} Documentation

## Architecture

- [Overview](./architecture/overview.md)
- [Components](./architecture/components.md)

## Guides

- [Getting Started](./guides/getting-started.md)
- [Caching](./guides/caching.md)
- [Performance](./guides/performance.md)

## Integration

- [RSPress Integration](./integration/rspress.md)

## Reference

- [API Documentation](./api/README.md)
- [Troubleshooting](./troubleshooting.md)
```

### Step 9: Write All Files

For each document:

1. Load repo-doc template
2. Fill in content sections
3. Add table of contents if >800 words
4. Validate markdown

Write to configured output directory:

```bash
# Default: {module.path}/docs/
mkdir -p {outputDir}/{architecture,guides,integration}
```

### Step 10: Validate Output

Run validation checks:

```bash
# Check word count for each document
for file in docs/**/*.md; do
  wc -w "$file"
done

# Validate markdown
markdownlint docs/**/*.md

# Check cross-references
grep -r '\[.*\](\..*\.md)' docs/
```

## Topic Mapping Examples

### Architecture Design Docs → User Docs

**Design doc: `architecture.md`**

Contains:

- Layer architecture with Effect-TS
- Service dependency injection
- Error handling strategy

**Maps to:**

- `docs/architecture/overview.md` - High-level architecture
- `docs/guides/error-handling.md` - How to handle errors

### Performance Design Docs → User Docs

**Design doc: `performance.md`**

Contains:

- Caching strategy (LRU, disk, TTL)
- HTTP client optimization
- Benchmark results

**Maps to:**

- `docs/guides/caching.md` - Using the cache effectively
- `docs/guides/performance.md` - Performance tips

### Integration Design Docs → User Docs

**Design doc: `integration.md`**

Contains:

- RSPress plugin integration
- Twoslash VFS generation
- API Extractor model parsing

**Maps to:**

- `docs/integration/rspress.md` - RSPress integration guide
- `docs/integration/twoslash.md` - Twoslash integration guide

## Content Transformation

### Technical Architecture → User Architecture

**Design doc:**

> The system uses a layered Effect-TS architecture with three layers:
> PackageFetcher, CacheManager, and TypeRegistry. Dependencies are
> injected via Layer.provide().

**User doc:**

> The package is organized into three main components:
>
> - **Package Fetcher** - Downloads type definitions from npm
> - **Cache Manager** - Stores definitions for fast repeated access
> - **Type Registry** - Coordinates fetching and caching
>
> These components work together automatically - you don't need to
> configure them individually.

### Implementation Pattern → Usage Pattern

**Design doc:**

> The VFS generation uses pipe() to compose operations:
> fetchTypes, parseDeclarations, and generateVFS.

**User doc:**

> To generate a virtual file system for TypeScript:
>
> ```typescript
> const vfs = await registry.generateVFS(['zod@3.22.0']);
> ```
>
> The VFS includes all type definitions and can be used with
> TypeScript's language service.

## Quality Standards

Level 2 repository docs must meet:

- **Length:** 500-2000 words per document
- **Code Examples:** At least 2 per guide
- **Cross-references:** Each doc links to 1-3 related docs
- **Table of Contents:** For docs >800 words
- **Markdown:** Valid GitHub-flavored markdown
- **Line Length:** ≤120 characters

## Error Handling

### No Design Docs Found

If module has no design docs:

```text
Warning: No design docs found for module '{module}'
Cannot generate repository documentation without design docs
Consider creating design docs first with /design-init
```

### Missing Module Configuration

If module not in design.config.json:

```text
Error: Module '{module}' not found in design configuration
Available modules: {list}
```

### Empty Topic

If a topic has insufficient content:

```text
Warning: Topic '{topic}' has insufficient content
Skipping this topic (need at least 300 words)
```
