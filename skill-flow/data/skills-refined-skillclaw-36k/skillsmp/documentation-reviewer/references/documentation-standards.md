# Documentation Standards

Writing style and structure guidelines for MkDocs documentation.

## Writing Style

### Voice and Tense

- **Use present tense**: "Runs the server" not "Will run the server"
- **Use active voice**: "The script creates a file" not "A file is created by the script"
- **Use imperative mood for instructions**: "Run the command" not "You should run the command"

### Clarity

- Keep sentences short (under 25 words preferred)
- One idea per paragraph
- Lead with the most important information
- Avoid jargon; define technical terms on first use

### Consistency

- Use consistent terminology throughout docs
- Match code names exactly (case-sensitive)
- Use same formatting for similar elements

## Document Structure

### Page Template

```markdown
# Page Title

Brief introduction (1-2 sentences).

## Overview

Expanded context and purpose.

## Prerequisites

What users need before starting.

## Main Content

Organized by task or concept.

## Examples

Practical demonstrations.

## Troubleshooting

Common issues and solutions.

## See Also

Related pages and external resources.
```

### Headings

- **H1 (`#`)**: Page title only, one per page
- **H2 (`##`)**: Major sections
- **H3 (`###`)**: Subsections
- **H4 (`####`)**: Rarely used, prefer restructuring

### File Organization

```
docs/
├── index.md              # Landing page
├── getting-started/      # Onboarding
│   ├── installation.md
│   └── quick-start.md
├── features/             # User-facing functionality
├── architecture/         # Technical deep-dives
├── development/          # Contributor guides
├── api/                  # API reference
└── plans/                # Design documents (optional)
```

## Code Examples

### Requirements

- All code must be runnable and tested
- Include expected output when helpful
- Use realistic variable names
- Add comments for non-obvious logic

### Format

````markdown
```python title="descriptive_name.py"
# Brief comment explaining purpose
def example_function():
    result = do_something()
    return result
```
````

### Command Examples

```markdown
# Good: Show command with context
inv dev.debug  # Start development environment

# Bad: Command without explanation
inv dev.debug
```

## Tables

Use for:
- Comparing options
- Parameter documentation
- Quick reference data

```markdown
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name`    | str  | -       | Required name |
| `count`   | int  | `10`    | Optional count |
```

## Admonitions Usage

| Type | When to Use |
|------|-------------|
| `note` | Additional context, not critical |
| `tip` | Best practices, shortcuts |
| `warning` | Potential issues, gotchas |
| `danger` | Data loss, security risks |
| `info` | Background information |
| `example` | Detailed examples |

## Links

### Internal Links

- Use relative paths: `[Page](../section/page.md)`
- Link to specific sections: `[Section](page.md#heading-anchor)`
- Verify links with `mkdocs build --strict`

### External Links

- Include for official docs, specifications
- Avoid links that may become stale
- Consider adding link text in parentheses: `[MkDocs](https://mkdocs.org) (official docs)`

## Review Checklist

- [ ] Accurate and tested information
- [ ] Consistent with existing docs style
- [ ] All code examples work
- [ ] Internal links valid
- [ ] Added to mkdocs.yml navigation
- [ ] Spelling and grammar checked
- [ ] Page renders correctly in preview
