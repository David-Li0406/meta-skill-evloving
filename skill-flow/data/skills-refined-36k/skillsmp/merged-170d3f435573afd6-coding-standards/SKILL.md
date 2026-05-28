---
name: coding-standards
description: Use this skill when writing or editing HTML, Jinja, or Python code to ensure adherence to coding standards and best practices.
---

# Coding Standards

## HTML Coding Standards

### Syntax & Style
- **Spacing**: Keep vertical spacing compact (no excessive blank lines).
- **Readability**: Prioritize readable code over "clever" one-liners.

### CSS
- **In-line CSS**: Prefer use of classes from .css files to in-line CSS, unless explicitly justified.

### JavaScript
- **In-line JS**: Prefer including functions from .js files to in-line JS, unless explicitly justified.

## Python Coding Standards

### Mandatory Metadata
- **Function/Class Header**: Every function or class must have the following comment header:
  ```python
  # [Created-or-Modified] by [Model_Name] | YYYY-MM-DD_[Iteration]
  # Example: # Modified by Claude-3.5-Sonnet | 2024-10-27_01
  ```

### Syntax & Style
- **Quotes**: Enforce double quotes (") over single quotes (').
  - Good: `x += "."`
  - Bad: `x += '.'`
- **SQL**: Always use multi-line strings (""") for SQL queries.
- **Templates**: Set language mode to Jinja-HTML.
- **Spacing**: Keep vertical spacing compact (no excessive blank lines).
- **Readability**: Prioritize readable code over "clever"/compact one-liners.

### Comments
- **Preserve Comments**: Do NOT delete existing, still relevant comments.
- **Comment Liberally**: Explain why, not just what.

## Logic & Operations
- **File Collisions**: If a file exists, append _[timestamp] to the new filename.
- **Simplicity**: Choose the simplest working solution.

## Tooling Preference (Web)
- **Primary**: Use `browser_action` (ALWAYS try this first).
- **Fallback**: Use other browser tools (only if `browser_action` fails).