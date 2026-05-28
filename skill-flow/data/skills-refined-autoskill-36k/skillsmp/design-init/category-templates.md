# Category Inference and Template Selection

Reference guide for determining the appropriate category and template for new
design documents.

## Category Inference Patterns

When category is not explicitly provided, infer from topic name using these
patterns:

### Architecture

**Keywords:** architecture, structure, design, system, component, pattern

**Examples:**

- `api-design` → architecture
- `component-lifecycle` → architecture
- `system-structure` → architecture

### Performance

**Keywords:** performance, optimization, benchmark, speed, efficiency, cache

**Examples:**

- `caching-optimization` → performance
- `query-performance` → performance
- `benchmark-suite` → performance

### Observability

**Keywords:** observability, logging, metrics, events, monitoring, tracking,
telemetry

**Examples:**

- `error-tracking` → observability
- `metrics-collection` → observability
- `event-system` → observability

### Testing

**Keywords:** test, testing, qa, quality

**Examples:**

- `test-strategy` → testing
- `integration-testing` → testing

### Integration

**Keywords:** integration, api, interface, connector

**Examples:**

- `api-integration` → integration
- `third-party-connector` → integration

### Other/Default

When no clear pattern matches, ask user to select category.

## Template Selection

### Step 1: Check for Category-Specific Template

Templates are located at `.claude/skills/design-init/templates/{category}.template.md`:

- `.claude/skills/design-init/templates/architecture.template.md`
- `.claude/skills/design-init/templates/performance.template.md`
- `.claude/skills/design-init/templates/observability.template.md`

### Step 2: Fall Back to Default

If category-specific template doesn't exist:
`.claude/skills/design-init/templates/design-doc.template.md`

## Template Variables

All templates support these variable replacements:

### Frontmatter Variables

- `{module-name}` → actual module name
- `{selected-category}` → chosen category
- `YYYY-MM-DD` → current date (ISO format)
- `stub` → initial status
- `0` → initial completeness

### Content Variables

- `{Document Title}` → Topic in Title Case
- `{System/Feature Name}` → Same as document title
- `{module-name}` → Actual module name
- `{Placeholder}` → Keep for user to fill in

## Title Case Conversion

Convert kebab-case topics to Title Case:

**Examples:**

- `type-loading` → Type Loading
- `api-design` → API Design
- `error-handling-system` → Error Handling System
- `cache-optimization` → Cache Optimization

**Algorithm:**

1. Split on hyphens
2. Capitalize first letter of each word
3. Join with spaces

## Asking User for Category

When category cannot be confidently inferred, present options:

```text
Which category best fits this design doc?

1. architecture - System/component architecture
2. performance - Performance characteristics and optimization
3. observability - Logging, metrics, error tracking
4. testing - Testing strategy and implementation
5. integration - Integration patterns and APIs
6. other - General design documentation
```

Use AskUserQuestion tool with these options.
