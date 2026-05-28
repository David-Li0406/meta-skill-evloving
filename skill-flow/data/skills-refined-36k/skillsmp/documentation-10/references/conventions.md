# Documentation Conventions

## Markdown Style

### Headers

- Use ATX style (`#`, `##`, `###`)
- One blank line before and after headers
- Sentence case for headers

### Code Blocks

- Use fenced code blocks with language identifier
- Indent 4 spaces for inline code in lists

```csharp
// Example C# code
public class Example { }
```

### Tables

- Use pipes and dashes
- Align columns for readability
- Header row required

| Column 1 | Column 2 |
| -------- | -------- |
| Data     | Data     |

### Lists

- Use `-` for unordered lists
- Use `1.` for ordered lists
- Indent with 2 spaces for nesting

## File Naming

| Type          | Convention          | Example                  |
| ------------- | ------------------- | ------------------------ |
| Documentation | UPPER-CASE-KEBAB.md | ARCHITECTURE-ANALYSIS.md |
| References    | lower-kebab.md      | contact-handling.md      |
| Code          | PascalCase.cs       | GameManager.cs           |

## Section Templates

### Reference File Template

````markdown
# Topic Name

## Overview

Brief description.

## Key Concepts

| Concept | Description |
| ------- | ----------- |
| ...     | ...         |

## Examples

```csharp
// Code example
```
````

## See Also

- Related topic link

````text

### API Documentation Template
```markdown
## MethodName

Brief description.

**Parameters:**
- `param1` (Type) - Description

**Returns:** Type - Description

**Example:**
```csharp
var result = MethodName(param1);
```
````
