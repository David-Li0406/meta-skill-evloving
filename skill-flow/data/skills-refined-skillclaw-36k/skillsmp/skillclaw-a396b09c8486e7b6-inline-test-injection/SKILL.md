---
name: inline-test-injection
description: Use this skill when you need to inject Doc Detective test specs into documentation source files as inline comments, ensuring test steps are placed close to their associated content.
---

# Inline Test Injection

Inject test steps from Doc Detective specs into documentation source files as inline comments, placing each step close to its associated content using semantic pattern matching.

## Workflow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ 1. Parse Spec   │────▶│ 2. Read Source  │────▶│ 3. Match Steps  │
│    (JSON/YAML)  │     │    + Detect Type│     │    Semantically │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                         │
                        ┌─────────────────┐     ┌────────▼────────┐
                        │ 5. Apply/Preview│◀────│ 4. Generate     │
                        │    Changes      │     │    Inline Cmts  │
                        └─────────────────┘     └─────────────────┘
```

## Comment Formats by File Type

| File Type | Extensions | Comment Syntax |
|-----------|------------|----------------|
| Markdown | `.md`, `.markdown` | `<!-- step {...} -->` |
| MDX | `.mdx` | `{/* step {...} */}` |
| HTML | `.html`, `.htm` | `<!-- step {...} -->` |
| XML/DITA | `.xml`, `.dita`, `.ditamap` | `<?doc-detective step {...} ?>` |
| AsciiDoc | `.adoc`, `.asciidoc`, `.asc` | `// (step {...})` |

## Usage

### Using the Script

```bash
# Preview mode (default) - shows diff of planned changes
./scripts/dist/inject-inline <spec-file> <source-file>

# Apply mode - writes changes to file
./scripts/dist/inject-inline <spec-file> <source-file> --apply

# Specify syntax format for inline content
./scripts/dist/inject-inline spec.yaml doc.md --syntax yaml
```

### Manual Injection

When the script cannot run or finer control is needed:

1. **Read the test spec** and identify each step's action and value.
2. **Scan the source file** for content matching the step (links, bold text, action verbs).
3. **Insert inline comment** immediately after the matching content.
4. **Use appropriate comment format** based on file type.

## Semantic Matching

Steps are matched to content based on action type and context relevance.