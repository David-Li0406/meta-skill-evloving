# RSPress Guide Generation Examples

Examples of generated learning guides for RSPress documentation.

## Example 1: Concept Page

### Example 1 Command

```bash
/rspress-guide effect-type-registry --type=concept --topic="Caching Strategy"
```

### Example 1 Generated File

**Location:** `website/docs/en/packages/effect-type-registry/concepts/caching-strategy.mdx`

**Content Structure:**

- Opening paragraph explaining what caching strategy is and why it matters
- "Understanding Caching" section with clear explanation
- Mermaid flowchart showing cache lookup process
- "How It Works" section with Twoslash code example
- "Common Patterns" showing basic and advanced caching usage
- Links to related concepts (Performance, Configuration)
- Links to API docs (CacheLayer, CacheOptions)

**Key Features:**

- Complete Twoslash code blocks with imports
- Progressive disclosure (basic → advanced patterns)
- Visual diagrams for complex concepts
- Cross-references to API documentation

## Example 2: Guide Page

### Example 2 Command

```bash
/rspress-guide rspress-plugin-api-extractor --type=guide --topic="Testing Hooks"
```

### Example 2 Generated File

**Location:** `website/docs/en/packages/rspress-plugin-api-extractor/guides/testing-hooks.mdx`

**Content Structure:**

- Introduction explaining what this guide helps accomplish
- Prerequisites (knowledge of hooks, testing frameworks)
- Step 1: Setup test environment
- Step 2: Configure plugin with test hooks
- Step 3: Write hook tests
- Step 4: Verify hook execution
- Complete working example
- Troubleshooting section (common issues and solutions)
- Next steps (advanced testing, integration tests)

**Key Features:**

- Task-oriented structure
- Step-by-step code examples
- Complete working solution at end
- Troubleshooting for common problems
- Links to next logical steps

## Example 3: Example Page

### Command

```bash
/rspress-guide website --type=example --topic="Blog Integration"
```

### Generated File

**Location:** `website/docs/en/examples/blog-integration.mdx`

**Content Structure:**

- Scenario describing real-world blog integration need
- Complete solution with detailed code annotations
- Explanation of how the solution works
- Variations showing alternative approaches (static vs dynamic)
- Links to related examples (RSS feed, pagination)

**Key Features:**

- Real-world scenario
- Production-ready code
- Multiple approaches shown via tabs
- Best practices demonstrated
- Complete, runnable examples

## Navigation Updates

### Before Generation

```json
{
  "index": {
    "title": "Overview"
  }
}
```

### After Generating Concept

```json
{
  "index": {
    "title": "Overview"
  },
  "caching-strategy": {
    "title": "Caching Strategy"
  }
}
```

### After Generating Multiple Pages

```json
{
  "index": {
    "title": "Overview"
  },
  "caching-strategy": {
    "title": "Caching Strategy"
  },
  "performance": {
    "title": "Performance"
  },
  "architecture": {
    "title": "Architecture"
  }
}
```

## Twoslash Code Block Examples

### Basic Twoslash Block

The generated concept page includes a working TypeScript example with full
type checking.

**Features:**

- Explicit imports
- Complete program
- Type inference shown
- Compiles without errors

### Progressive Example with Tabs

Guide pages use tabs to show multiple approaches. Each tab contains a complete
Twoslash code block.

**Benefits:**

- Users choose their approach
- Progressive complexity
- All examples tested

### Cut Notations

Example pages hide boilerplate while maintaining functionality:

- Import statements before cut
- Core example shown
- Verification code after cut

**Result:** Users see focused code while TypeScript validates everything.

## Quality Checklist

Generated pages meet these criteria:

- ✅ Valid MDX syntax
- ✅ Complete frontmatter
- ✅ Working Twoslash code blocks
- ✅ Cross-references to API docs
- ✅ Navigation metadata updated
- ✅ Clear structure (intro, content, links)
- ✅ Progressive learning path
- ✅ Accessible heading hierarchy
