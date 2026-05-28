# RSPress Guide Generation - Detailed Instructions

This document provides detailed instructions for generating RSPress learning
guides.

## Parameter Processing

### Module Resolution

1. Read `.claude/design/design.config.json`
2. Find module in `modules` section
3. Validate `userDocs.siteDocs` is configured
4. Get `designDocsPath` for content source

Example configuration:

```json
"rspress-plugin-api-extractor": {
  "path": "pkgs/rspress-plugin-api-extractor",
  "designDocsPath": ".claude/design/rspress-plugin-api-extractor",
  "userDocs": {
    "siteDocs": "website/docs/en/packages/rspress-plugin-api-extractor"
  }
}
```

### Topic Processing

- Convert topic to kebab-case for filename
- Preserve original topic for page title
- Example: "Caching Strategy" → `caching-strategy.mdx`

### Type Validation

Valid types:

- `concept` - Conceptual explanation
- `guide` - Task-oriented how-to
- `example` - Real-world scenario

## Template System

### Default Templates

Located in `.claude/templates/`:

- `rspress-concept.mdx` - Concept page template
- `rspress-guide.mdx` - Guide page template
- `rspress-example.mdx` - Example page template

### Template Variables

Templates use placeholder syntax:

```text
{module.name} - Module display name
{module.packageName} - npm package name
{topic} - Page topic/title
{date} - Current date (YYYY-MM-DD)
{description} - Generated description
```

### Custom Templates

Users can provide custom templates via `--template` flag. Custom templates
must follow the same structure as default templates.

## Content Generation

### Concept Pages

**Structure:**

1. Opening paragraph (what and why)
2. Understanding section (clear explanation)
3. How It Works (technical details with code)
4. Common Patterns (2-3 patterns)
5. Related Concepts
6. API Reference links

**Content Sources:**

- Design docs (architecture sections)
- Existing code examples
- API documentation structure

**Code Examples:**

- Demonstrate the concept
- Show type inference
- Use real module APIs

### Guide Pages

**Structure:**

1. Introduction (what this accomplishes)
2. Prerequisites
3. Step-by-step instructions (3-5 steps)
4. Complete Example
5. Troubleshooting
6. Next Steps

**Content Sources:**

- Design docs (usage sections)
- README examples
- Integration patterns

**Code Examples:**

- Build progressively (step by step)
- Complete working solution at end
- Handle realistic scenarios

### Example Pages

**Structure:**

1. Scenario description
2. Solution (annotated code)
3. Explanation (how it works)
4. Variations (alternative approaches)
5. Related Examples

**Content Sources:**

- Design docs (use cases)
- Test files
- Real-world integrations

**Code Examples:**

- Complete, production-ready
- Show best practices
- Demonstrate patterns

## Twoslash Code Block Generation

### Basic Structure

All code blocks use `typescript twoslash vfs`:

````markdown
```typescript twoslash vfs
import { Something } from "module-name";

const example = new Something();
```
````

### Dependency Detection

Read `rspress.config.ts` to find available packages:

```typescript
ApiExtractorPlugin({
  autoDetectDependencies: {
    dependencies: true,
    devDependencies: true,
    peerDependencies: true,
  }
})
```

These packages are available in Twoslash without explicit VFS setup.

### Import Requirements

Every code block must:

- Import all types used
- Import all functions/classes used
- Be a complete TypeScript program
- Compile without errors

### Cut Notations

Hide boilerplate while maintaining functionality:

````markdown
```typescript twoslash vfs
import { Something } from "module-name";

// ---cut-before---

const example = new Something();
```
````

Result: Only `const example = new Something();` is shown to users.

### Progressive Examples

Use tabs for alternative approaches:

```markdown
<Tabs>
  <Tab label="Basic">
    (basic code example)
  </Tab>
  <Tab label="Advanced">
    (advanced code example)
  </Tab>
</Tabs>
```

## Cross-Referencing

### API Documentation Links

Auto-generated API docs are in `{siteDocs}/api/`:

```markdown
See [`ClassName`](../api/classes/classname) for details.

Configure using [`Options`](../api/interfaces/options).
```

### Internal Links

Link to related content:

```markdown
Learn about [Related Concept](../concepts/related-concept).

See [How to Task](../guides/task) for implementation.

Check out [Example](../examples/scenario) for usage.
```

### Link Validation

Verify all links resolve:

- Internal links point to existing files
- API links match generated structure
- Anchors exist if specified

## Navigation Updates

### Directory Structure

```text
website/docs/en/packages/{module}/
├── concepts/
│   ├── concept-1.mdx
│   └── _meta.json
├── guides/
│   ├── guide-1.mdx
│   └── _meta.json
└── examples/
    ├── example-1.mdx
    └── _meta.json
```

### _meta.json Structure

```json
{
  "index": {
    "title": "Overview"
  },
  "topic-name": {
    "title": "Topic Display Name"
  }
}
```

### Update Process

1. Read existing `_meta.json`
2. Add new entry with topic filename and title
3. Sort entries logically (not alphabetically)
4. Write updated `_meta.json`

## Frontmatter Generation

Every page needs frontmatter:

```yaml
---
title: Page Title
description: Brief description for SEO
---
```

Additional fields for landing pages:

```yaml
---
title: Module Name
description: SEO description
overview: false
head:
  - - meta
    - property: og:title
      content: Module Name
  - - meta
    - property: og:description
      content: Full description
---
```

## Validation Steps

### MDX Syntax

Check for common issues:

- Unclosed JSX tags
- Invalid component imports
- Malformed code blocks
- Incorrect frontmatter

### Twoslash Compilation

Verify code blocks compile:

- Extract code from blocks
- Add to TypeScript program
- Check for compilation errors

### Cross-Reference Verification

Check all links:

- Relative paths resolve
- API docs exist
- Anchors are valid

### Navigation Consistency

Ensure navigation is correct:

- `_meta.json` is valid JSON
- All entries reference existing files
- Titles match frontmatter

## Error Handling

### Module Not Found

Error: Module not in design.config.json

Solution: Add module configuration or use correct module name

### Missing Site Docs Path

Error: Module has no siteDocs configured

Solution: Add `userDocs.siteDocs` to module config

### Template Not Found

Error: Custom template path invalid

Solution: Use default template or fix template path

### Invalid Type

Error: Type must be concept, guide, or example

Solution: Use valid type value

## Best Practices

### Content Quality

- Start with clear purpose
- Use active voice
- Be concise and scannable
- Explain why, not just how

### Code Examples

- Test that examples compile
- Use realistic scenarios
- Show progressive complexity
- Include error handling

### Navigation

- Group related pages
- Order basic → advanced
- Use descriptive titles
- Link related content

### Maintenance

- Keep examples up to date
- Update links when APIs change
- Review for clarity regularly
- Validate Twoslash blocks
