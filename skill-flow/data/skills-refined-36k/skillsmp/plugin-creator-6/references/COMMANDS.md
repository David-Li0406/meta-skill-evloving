# Commands Reference

Detailed guide for creating user-invoked slash commands.

> **📘 New to commands?** Start with [COMPONENTS.md](COMPONENTS.md#command-templates) for complete templates with examples.
>
> **This file provides:** Advanced patterns, argument handling strategies, and real-world examples beyond the basic templates.

## Quick Links

- [File Format](#file-format)
- [Frontmatter Fields](#frontmatter-fields)
- [Argument Handling](#argument-handling)
- [Error Handling](#error-handling)
- [Advanced Patterns](#advanced-patterns)
- [Real Examples](#examples)

## File Format

`commands/command-name.md`

## Template

```markdown
---
description: Brief description shown in autocomplete (max 100 chars)
args:
  - name: arg_name
    description: Argument description
    required: true
  - name: optional_arg
    description: Optional argument
    required: false
---

# Command Title

System instructions for how Claude should execute this command.

## Process

1. Step 1
2. Step 2
3. Step 3

## Examples

- `command-name arg1` - What happens
- `command-name arg1 --flag` - With flag

## Error Handling

[Common errors and how to handle them]
```

## Frontmatter Fields

### Required

- `description`: Shown in autocomplete, max 100 chars

### Optional

- `args`: Array of argument definitions
  - `name`: Argument name
  - `description`: What the argument does
  - `required`: true/false

## Best Practices

1. **Clear names**: Use verb-based names (`commit`, not `create-commit`)
2. **Concise descriptions**: Under 100 characters
3. **Document arguments**: All args must have descriptions
4. **Provide examples**: Show common usage patterns
5. **Handle errors**: Document error cases
6. **Use imperative form**: "Create file" not "Creates file"

## Common Use Cases

### Code Generation

```markdown
---
description: Generate boilerplate code for components
args:
  - name: component_type
    description: Type of component (react, vue, etc.)
    required: true
  - name: component_name
    description: Name of the component
    required: true
---

Generate a new component based on the type and name.
```

### Analysis

```markdown
---
description: Analyze code for security vulnerabilities
---

Scan the codebase for common security issues.
```

### Quick Actions

```markdown
---
description: Format all code files in the project
---

Run formatting tools on all source files.
```

## Examples

### Example 1: Git Commit

```markdown
---
description: Create a git commit with proper formatting
args:
  - name: message
    description: Commit message
    required: true
---

Create a git commit following best practices:

1. Stage all changes
2. Create commit with message: "message\n\nCo-Authored-By: Claude"
3. Show commit status
```

### Example 2: Run Tests

```markdown
---
description: Run test suite and show results
---

Run the test suite:

1. Find test command (package.json, Makefile, etc.)
2. Execute tests
3. Parse and display results
4. Highlight failures
```

### Example 3: Generate Docs

```markdown
---
description: Generate documentation from code comments
args:
  - name: format
    description: Output format (markdown, html, pdf)
    required: false
---

Generate documentation from code comments.

If no format specified, use markdown.
```

## Argument Handling

### Required Arguments

```markdown
args:
  - name: file_path
    description: Path to the file
    required: true
```

### Optional Arguments

```markdown
args:
  - name: output_dir
    description: Where to save output
    required: false
```

### Flags

```markdown
args:
  - name: verbose
    description: Show detailed output
    required: false
```

## Error Handling

### Validation

```markdown
Before executing:
1. Validate arguments exist if required
2. Check file paths are valid
3. Verify dependencies are installed
```

### Error Messages

```markdown
If error occurs:
- Show clear error message
- Suggest how to fix
- Don't use technical jargon
```

## Advanced Patterns

### Command + Agent

```markdown
Launch the analyzer agent using the Task tool:
- subagent_type: "code-analyzer"
- description: "Analyze codebase structure"
```

### Command + Skill

```markdown
Use the Skill tool to invoke "react-patterns".
Apply the patterns to the current code.
```

### Command with Confirmation

```markdown
Before making destructive changes:
1. Describe what will happen
2. Ask user to confirm
3. Proceed only if confirmed
```
