# Skill Creator Reference

Advanced patterns and detailed examples for creating Claude Code skills.

## allowed-tools Configuration

Restrict which tools Claude can use when a Skill is active.

### Format

Use YAML list for readability:

```yaml
---
name: code-explorer
description: Explore and analyze code without modifications. Use for read-only codebase analysis.
allowed-tools:
  - Read
  - Grep
  - Glob
---
```

Comma-separated also works but is harder to read: `allowed-tools: Read, Grep, Glob`

### Use Cases

| Use Case           | Tools                  | Why                         |
| ------------------ | ---------------------- | --------------------------- |
| Read-only analysis | `Read, Grep, Glob`     | Shouldn't modify files      |
| Data processing    | `Read, Bash(python:*)` | Run scripts, no file writes |
| Security review    | `Read, Grep, Glob`     | Audit without changes       |
| Documentation gen  | `Read, Grep, Write`    | Read code, write docs only  |

### Behavior

- **With allowed-tools**: Claude uses listed tools without permission prompts
- **Without allowed-tools**: Claude uses standard permission model (may prompt for approval)

## Forked Context

Use `context: fork` to run a Skill in an isolated sub-agent with its own conversation history:

```yaml
---
name: code-analysis
description: Analyze code quality and generate detailed reports. Use for comprehensive codebase analysis.
context: fork
agent: Explore
---
```

### When to Use

- Complex multi-step operations that would clutter main conversation
- Skills generating lots of intermediate output
- Operations needing isolated conversation history

### Agent Options

| Agent             | Use Case                        |
| ----------------- | ------------------------------- |
| `general-purpose` | Default, handles most tasks     |
| `Explore`         | Codebase exploration and search |
| `Plan`            | Implementation planning         |
| Custom agent      | Name from `.claude/agents/`     |

## hooks Configuration

Skills can define lifecycle hooks that run at specific events:

```yaml
---
name: secure-operations
description: Perform operations with security checks
hooks:
  PreToolUse:
    - matcher: 'Bash'
      hooks:
        - type: command
          command: './scripts/security-check.sh $TOOL_INPUT'
          once: true # Only run once per session
  PostToolUse:
    - matcher: 'Write'
      hooks:
        - type: command
          command: './scripts/validate-output.sh'
  Stop:
    - hooks:
        - type: command
          command: './scripts/cleanup.sh'
---
```

### Hook Events

| Event         | When It Fires                  |
| ------------- | ------------------------------ |
| `PreToolUse`  | Before a tool is executed      |
| `PostToolUse` | After a tool completes         |
| `Stop`        | When the skill stops executing |

### Hook Options

| Option    | Purpose                                    |
| --------- | ------------------------------------------ |
| `matcher` | Tool name to match (e.g., "Bash", "Write") |
| `type`    | Hook type (usually "command")              |
| `command` | Shell command to execute                   |
| `once`    | If true, only runs once per session        |

> **Note**: Hooks defined in a Skill are scoped to that Skill's execution and automatically cleaned up when the Skill finishes.

## Visibility Control

Control how skills can be invoked with these frontmatter fields:

| Setting                          | Slash Menu | Skill Tool | Auto-discovery | Use Case                                       |
| -------------------------------- | ---------- | ---------- | -------------- | ---------------------------------------------- |
| `user-invocable: true` (default) | Visible    | Allowed    | Yes            | Skills users invoke directly                   |
| `user-invocable: false`          | Hidden     | Allowed    | Yes            | Claude-only skills, hidden from user           |
| `disable-model-invocation: true` | Visible    | Blocked    | Yes            | User-only skills, Claude can't invoke via tool |

### When to Use Each

**Default (no settings)** - Most skills. Users can type `/skill-name` or Claude can invoke automatically.

**user-invocable: false** - Internal skills that Claude should use automatically but shouldn't clutter the user's slash menu:

```yaml
---
name: internal-code-standards
description: Apply internal code standards when reviewing code
user-invocable: false
---
```

**disable-model-invocation: true** - Skills that should only run when the user explicitly requests them:

```yaml
---
name: dangerous-cleanup
description: Delete old files and reset state. Use when user explicitly requests cleanup.
disable-model-invocation: true
---
```

## Utility Scripts

Scripts in your skill directory execute without loading source into context. Only output consumes tokens.

### Directory Structure

```sh
my-skill/
├── SKILL.md
└── scripts/
    ├── validate.py      # Validation logic
    ├── transform.sh     # Data processing
    └── check-deps.sh    # Dependency checker
```

### Requirements

1. **Make executable**: `chmod +x scripts/*.py scripts/*.sh`
2. **Tell Claude to run (not read)** in SKILL.md:

```markdown
Run the validation script to check the input:

\`\`\`bash
uv run scripts/validate.py input.pdf
\`\`\`
```

### When to Use Scripts

| Use Case                  | Why Scripts Work Better            |
| ------------------------- | ---------------------------------- |
| Complex validation        | Logic verbose to describe in prose |
| Data transformation       | More reliable as tested code       |
| Consistency               | Same behavior across all uses      |
| External tool integration | Wrap CLI tools with error handling |

### Example Validation Script

````python
#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.11"
# ///
"""Validate skill structure."""

import sys
import re
from pathlib import Path

def validate_skill(path: str) -> list[str]:
    """Check skill file for common issues."""
    errors = []
    content = Path(path).read_text()
    lines = content.split('\n')

    # Check frontmatter
    if not content.startswith('---'):
        errors.append("Missing YAML frontmatter (must start with ---)")

    # Check required fields
    if 'name:' not in content:
        errors.append("Missing 'name' in frontmatter")
    if 'description:' not in content:
        errors.append("Missing 'description' in frontmatter")

    # Check line count
    if len(lines) > 500:
        errors.append(f"SKILL.md is {len(lines)} lines (max 500)")

    # Check for code blocks without language
    in_code_block = False
    for i, line in enumerate(lines, 1):
        if line.startswith('```'):
            if not in_code_block:
                # Opening fence - check for language
                if line == '```':
                    errors.append(f"Line {i}: Code block missing language specifier")
            in_code_block = not in_code_block

    return errors

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: validate.py <SKILL.md path>")
        sys.exit(1)

    errors = validate_skill(sys.argv[1])
    if errors:
        print("Validation errors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("✓ Skill validation passed")
        sys.exit(0)
````

## External Dependencies

If your skill requires external packages, document them clearly:

### In Description

```yaml
---
name: pdf-processing
description: Extract text, fill forms, merge PDFs. Requires pypdf and pdfplumber packages.
---
```

### In SKILL.md Body

```markdown
## Requirements

Install required packages before using this skill:

\`\`\`bash
uv pip install pypdf pdfplumber
\`\`\`

Verify installation:

\`\`\`bash
uv run python -c "import pypdf, pdfplumber; print('OK')"
\`\`\`
```

## Code Example Best Practices

### Language Specifiers (MD040)

Always specify language for fenced code blocks:

| Content             | Language   |
| ------------------- | ---------- |
| TypeScript/React    | `tsx`      |
| TypeScript (no JSX) | `ts`       |
| Shell commands      | `bash`     |
| Directory trees     | `sh`       |
| JSON config         | `json`     |
| YAML config         | `yaml`     |
| Markdown templates  | `markdown` |
| Python              | `python`   |

### Show Correct and Incorrect

```tsx
// ✓ Good - specific pattern
function UserProfile({ user }: UserProfileProps) {
  return <div>{user.name}</div>;
}

// ✗ Bad - generic pattern
const UserProfile = (props) => {
  return <div>{props.user.name}</div>;
};
```

### Use Project Conventions

```tsx
// Use project imports
import { Button } from '@oakoss/ui';
import { db } from '@oakoss/database';

// Use type not interface
type ButtonProps = {
  variant: 'default' | 'destructive';
};

// Use function declarations
function MyComponent() {}
```

## Reference.md Patterns

When to split content from SKILL.md to reference.md:

| Content Type                   | Keep in SKILL.md | Move to reference.md |
| ------------------------------ | ---------------- | -------------------- |
| Quick start                    | ✓                |                      |
| Core patterns                  | ✓                |                      |
| Common mistakes                | ✓                |                      |
| Detailed API reference         |                  | ✓                    |
| Long code examples (>50 lines) |                  | ✓                    |
| Configuration tables           |                  | ✓                    |
| Migration guides               |                  | ✓                    |
| Edge cases                     |                  | ✓                    |

### reference.md Structure

```markdown
# <Skill Name> Reference

## <Topic 1>

[Detailed patterns and examples]

## <Topic 2>

[More advanced content]
```

## Plugin Distribution

To distribute skills via plugins:

```sh
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── my-skill/
        ├── SKILL.md
        ├── reference.md
        └── scripts/
            └── validate.py
```

### plugin.json Example

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Plugin with custom skills"
}
```
