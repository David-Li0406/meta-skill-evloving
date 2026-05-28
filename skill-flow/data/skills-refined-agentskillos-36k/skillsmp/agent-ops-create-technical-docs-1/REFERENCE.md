# Technical Documentation Reference

## Code Block Syntax

### Basic Format

````markdown
```language title="path/to/file.ext" linenums="start_line"
// code here
```
````

### Examples

**Python with line numbers:**
````markdown
```python title="src/utils/parser.py" linenums="15"
def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown."""
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            return yaml.safe_load(content[3:end])
    return {}
```
````

**TypeScript with highlighting:**
````markdown
```typescript title="src/components/Button.tsx" linenums="1" hl_lines="3 4"
interface ButtonProps {
  label: string;
  onClick: () => void;  // highlighted
  disabled?: boolean;   // highlighted
}
```
````

**Shell commands:**
````markdown
```bash title="Terminal"
uv run pytest tests/ -v
```
````

---

## Topic Templates

### How-To Quick Template

```markdown
# How to [Action]

**Time**: ~X minutes | **Difficulty**: Beginner/Intermediate/Advanced

## Prerequisites
- [ ] Requirement 1
- [ ] Requirement 2

## Steps

### 1. [First Step]
[Brief explanation]

\`\`\`language
// code
\`\`\`

### 2. [Second Step]
...

## Verify It Works
[How to confirm success]

## Common Issues
| Problem | Solution |
|---------|----------|
```

### Explainer Quick Template

```markdown
# Understanding [Concept]

> **TL;DR**: [One sentence summary]

## The Problem
[What problem does this solve?]

## The Solution
[How does this solve it?]

## How It Works
[Step-by-step or diagram]

## When to Use
- Use case 1
- Use case 2

## When NOT to Use
- Anti-pattern 1
```

### Reference Quick Template

```markdown
# [Component] API Reference

## Quick Start
\`\`\`language
// Minimal working example
\`\`\`

## Methods

### `methodName()`
**Signature**: `methodName(param: Type) -> ReturnType`

| Param | Type | Description |
|-------|------|-------------|

**Example**:
\`\`\`language
// usage
\`\`\`
```

---

## Audience Guidelines

| Level | Assumes | Explains |
|-------|---------|----------|
| **Beginner** | Basic programming | All concepts, full examples |
| **Intermediate** | Language proficiency | Domain concepts, key examples |
| **Advanced** | Domain expertise | Edge cases, internals only |

---

## Length Guidelines

| Length | Word Count | Use For |
|--------|------------|---------|
| **Short** | < 500 | Quick tips, single concepts |
| **Medium** | 500-1500 | Standard how-tos, explanations |
| **Long** | > 1500 | Tutorials, deep dives |

---

## Discovery Commands

### Find Documentation Gaps

```markdown
Analyze [folder] and identify undocumented:
- Public APIs (exported functions/classes)
- Configuration options
- Common workflows
- Error handling patterns
```

### Check Existing Coverage

```markdown
List existing documentation in:
- .agent/docs/
- docs/
- README.md

Compare against codebase to find gaps.
```

---

## Output Checklist

Before finalizing any document:

- [ ] Title is action-oriented or clearly descriptive
- [ ] Audience level is stated
- [ ] All code blocks have file paths
- [ ] Line numbers are accurate (verified against source)
- [ ] No placeholder text remains
- [ ] Links to related docs work
- [ ] Examples are runnable/valid
- [ ] No sensitive data exposed
