# README Generation Instructions

Detailed step-by-step instructions for generating package README files.

## Implementation Steps

### Step 1: Load Configuration

```bash
# Read design configuration
cat .claude/design/design.config.json
```

Extract:

- Module path and package location
- Design docs path
- User docs configuration
- Quality standards for Level 1

### Step 2: Load Module Metadata

```bash
# Read package.json for module
cat {module.path}/package.json
```

Extract:

- Package name
- Version
- Description
- License
- Dependencies (for installation notes)
- Repository URL
- Homepage URL

### Step 3: Load Design Documentation

```bash
# Find all design docs for module
find .claude/design/{module.designDocsPath} -name "*.md" -type f
```

For each design doc:

- Read frontmatter (status, completeness)
- Extract overview section
- Extract features/capabilities
- Find usage examples
- Identify integration points

### Step 4: Extract Content for README

**Description (1-2 sentences):**

- Take from package.json description
- Enhance with design doc overview if needed
- Focus on "what problem does this solve?"

**Features (3-5 bullet points):**

From design docs, extract:

- Key capabilities
- Unique features
- Performance characteristics
- Integration capabilities

Transform to user benefits:

- "Effect-TS based" → "Fault-tolerant with graceful error handling"
- "Disk caching with TTL" → "Fast repeated lookups with automatic cache
  invalidation"
- "HTTP retry with exponential backoff" → "Reliable fetching even with network
  issues"

**Quick Start:**

Find simplest working example:

1. Look for "Quick Start" or "Getting Started" in design docs
2. Look for common patterns in "Usage" sections
3. Simplify to minimal code (5-15 lines)
4. Ensure all imports are included
5. Add comments for clarity

**API Overview:**

List main exports:

1. Find exported types/functions from design docs
2. Group by category (classes, functions, types)
3. One-line description per export
4. Link to full API documentation

### Step 5: Apply Template

Load template:

```bash
cat .claude/skills/docs-generate-readme/templates/readme.template.md
```

Replace placeholders:

- `{module.name}` → package name
- `{module.description}` → short description
- `{module.overview}` → overview paragraph
- `{module.features}` → feature bullet points
- `{module.packageName}` → npm package name
- `{module.quickStart}` → example code
- `{module.apiOverview}` → API summary
- `{module.apiDocsLink}` → link to full API docs
- `{module.documentationLinks}` → links to docs, examples
- `{module.license}` → license type

### Step 6: Write Output

**New README mode:**

```bash
# Write to module's README location
cat > {module.path}/README.md <<'EOF'
{generated content}
EOF
```

**Update mode:**

1. Parse existing README.md
2. Identify standard sections vs custom sections
3. Update standard sections only
4. Preserve custom sections (badges, screenshots, etc.)
5. Merge and write

**Dry-run mode:**

1. Generate content
2. Display to user
3. Don't write file

### Step 7: Validate Output

Run validation checks:

```bash
# Check word count
wc -w {module.path}/README.md

# Check line length
grep -n '.\{81,\}' {module.path}/README.md

# Validate markdown
markdownlint {module.path}/README.md

# Check for broken links (simple)
grep -o '\[.*\](.*\.md)' {module.path}/README.md
```

Validation criteria:

- ✅ Word count: 200-500 (warn if >800)
- ✅ Line length: ≤80 characters
- ✅ Required sections present
- ✅ No markdown errors
- ✅ Code blocks have language specifiers
- ✅ All links are valid

## Content Transformation Rules

### Simplify Technical Language

| Internal Term | User-Friendly |
| ------------ | ------------- |
| "Effect-TS Layer system" | "Dependency injection" |
| "VFS for Twoslash" | "Virtual file system for type checking" |
| "CDN fetching with retry" | "Reliable package downloads" |
| "Disk-based caching with TTL" | "Fast caching with auto-cleanup" |
| "Observability events" | "Logging and monitoring" |

### Extract User Benefits from Features

**Technical feature:**

> "Uses Effect-TS Layer system for dependency injection with testable services"

**User benefit:**

> "Easy to test and configure with built-in dependency injection"

**Technical feature:**

> "Exponential backoff retry with jitter for HTTP requests"

**User benefit:**

> "Automatic retry on network failures for reliability"

### Create Quick Start Examples

**From design doc usage:**

```typescript
// Internal usage example
const registry = pipe(
  TypeRegistry.make(),
  Effect.provide(PackageFetcher.layer),
  Effect.provide(CacheManager.layer)
);
```

**For README quick start:**

```typescript
import { createRegistry } from 'effect-type-registry';

// Create a registry with default configuration
const registry = createRegistry();

// Fetch type definitions for a package
const types = await registry.getTypeDefinitions('zod', '3.22.0');
```

## Update Mode Preservation

When updating an existing README, preserve:

- Custom badges and shields
- Screenshots and GIFs
- Additional examples beyond quick start
- Custom sections (Roadmap, FAQ, etc.)
- Sponsors/acknowledgments sections
- Custom formatting and styling

Update only standard sections:

- Description
- Features list
- Installation command
- Quick start example
- API overview
- Standard links (docs, contributing, license)

## Quality Standards

### Level 1 README Requirements

From `.claude/design/design.config.json`:

```json
"userDocs": {
  "level1": {
    "targetWordCount": [200, 500],
    "maxLineLength": 80,
    "requireSections": ["Features", "Installation", "Usage"]
  }
}
```

### Readability Guidelines

- Use active voice ("You can..." not "The user can...")
- Use present tense ("It does..." not "It will do...")
- Avoid passive constructions
- Keep sentences short (< 25 words)
- Use simple words (avoid jargon)
- Include code examples for complex concepts

### Example Quality

All code examples must:

- Be copy-paste ready (include all imports)
- Use realistic, meaningful variable names
- Include comments for non-obvious parts
- Be syntactically valid TypeScript
- Work with the latest package version
- Show common use cases (not edge cases)

## Error Handling

### Missing Configuration

If module not found in `design.config.json`:

```text
Error: Module 'xyz' not found in design configuration
Available modules: effect-type-registry, rspress-plugin-api-extractor, website
```

### No Design Docs

If module has no design docs:

```text
Warning: No design docs found for module 'xyz'
Generating README from package.json only
Consider adding design docs for richer content
```

### Missing package.json

If package.json not found:

```text
Error: package.json not found at {module.path}/package.json
Cannot generate README without package metadata
```

### Update Mode Conflicts

If updating README with conflicting custom sections:

```text
Warning: Custom 'Features' section found in existing README
Options:
  1. Keep custom features (skip update)
  2. Replace with generated features
  3. Merge both (manual review required)
```

## Output Examples

See `examples.md` for complete before/after transformations.
