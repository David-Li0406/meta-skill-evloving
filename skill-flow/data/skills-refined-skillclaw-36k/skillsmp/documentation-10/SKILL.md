---
name: documentation
description: This skill should be used when the user asks about "update documentation", "CLAUDE.md", "README.md", "documentation conventions", "document this", "add to docs", "update the readme", or discusses project documentation maintenance and standards.
version: 0.5.0
---

# Documentation

Expert knowledge of Zero-Day Attack documentation conventions, structure, and maintenance for CLAUDE.md, README.md, and project documentation.

## Documentation Files

### CLAUDE.md

Primary guidance file for Claude Code:

| Section                      | Purpose                |
| ---------------------------- | ---------------------- |
| Project Overview             | What the project is    |
| Build Commands               | How to build/deploy    |
| Required Build Configuration | Platform settings      |
| Architecture                 | Code organization      |
| Key Namespaces               | Namespace purposes     |
| Singleton Managers           | Global access patterns |
| Board SDK Components         | SDK overview           |
| Project Structure            | File organization      |
| SVG Import Settings          | Sprite sizing rules    |
| Visual Style Guide           | Colors summary         |
| Layout Configuration         | Layout constants       |
| Testing                      | Test instructions      |
| Unity MCP Integration        | MCP setup/usage        |

### README.md

User-facing project introduction:

| Section                 | Purpose                  |
| ----------------------- | ------------------------ |
| Game Overview           | What the game is         |
| Digitization Approach   | Hybrid input model       |
| Tech Stack              | Engine, platform, SDK    |
| Getting Started         | Setup instructions       |
| Building & Deploying    | Build commands           |
| Simulation              | Testing without hardware |
| Project Structure       | Directory overview       |
| Documentation           | Doc file index           |
| AI-Assisted Development | MCP quick start          |
| Credits                 | Attribution              |

### Skill Reference Folders

Domain knowledge is distributed across plugin skill reference folders:

| Skill                  | Domain          | Key References                          |
| ---------------------- | --------------- | --------------------------------------- |
| `zero-day-rules`       | Game mechanics  | complete-rules.md, phase-mechanics.md   |
| `board-sdk`            | SDK integration | vendor-docs/, contact-handling.md       |
| `project-architecture` | Code patterns   | layer-model.md, data-flow.md            |
| `layout-sizing`        | Screen math     | coordinate-systems.md, layout-config.md |
| `visual-style-guide`   | Visual specs    | color-system.md, rendering-order.md     |
| `unity-mcp-tools`      | MCP tools       | tool-reference.md, tool-groups.md       |
| `unity-testing`        | Tests           | test-patterns.md, existing-tests.md     |

Load skills with `/zero-day-dev:{skill-name}` before spawning agents.

## Documentation Conventions

### Markdown Formatting

Use consistent formatting:

- Headers: `#` for title, `##` for sections, `###` for subsections
- Code blocks: Triple backticks with language
- Tables: Pipe-separated with header row
- Lists: `-` for unordered, `1.` for ordered

### Code Examples

Always include language identifier:

````markdown
```csharp
public class Example { }
```

```bash
bdb install app.apk
```
````

### Tables

Use for structured data:

```markdown
| Column 1 | Column 2 |
| -------- | -------- |
| Value 1  | Value 2  |
```

### File References

For project files, use relative paths:

```markdown
Located in `Assets/Scripts/Config/`
```

For domain knowledge, load skills:

```markdown
Load `/zero-day-dev:project-architecture` for architecture details
Load `/zero-day-dev:board-sdk` for SDK integration patterns
```

## Updating CLAUDE.md

### When to Update

Update CLAUDE.md when:

- New namespaces/classes added
- Architecture changes
- Build process changes
- New SDK features used
- Configuration changes

### Update Process

1. Identify section needing update
2. Keep format consistent with existing sections
3. Update related sections if affected
4. Keep concise - detail goes in skill references

### Key Sections to Maintain

**Script Organization**: Update when adding folders/namespaces

```markdown
Assets/Scripts/
├── NewFolder/ # Purpose
│ └── NewClass.cs # Description
```

**Key Namespaces**: Update when adding namespaces

```markdown
| `ZeroDayAttack.NewNamespace` | Purpose |
```

**Singleton Managers**: Update when adding managers

```markdown
- `NewManager.Instance` - Description
```

## Updating README.md

### When to Update README.md

Update README.md when:

- User-facing features change
- Setup process changes
- Dependencies change
- Credits need updating

### Keep User-Focused

README is for users, not AI:

- Clear setup instructions
- Practical examples
- Troubleshooting tips
- Working commands

## Skill Reference Updates

### When to Update Skill References

Update skill reference files when:

- Significant implementation changes
- New systems added
- Algorithms change
- Rules clarified

### Routing Guide

| Change Type       | Update Skill                       |
| ----------------- | ---------------------------------- |
| Game mechanics    | `zero-day-rules/references/`       |
| Code architecture | `project-architecture/references/` |
| SDK patterns      | `board-sdk/references/`            |
| Layout/sizing     | `layout-sizing/references/`        |
| Visual specs      | `visual-style-guide/references/`   |
| MCP tools         | `unity-mcp-tools/references/`      |
| Test patterns     | `unity-testing/references/`        |

### Naming Convention

Use lowercase-with-dashes for reference files:

```text
new-feature.md
system-name.md
```

## Plugin Documentation

### Skills Updates

Update skill SKILL.md files when:

- New trigger phrases needed
- New reference files added
- Procedures change
- Best practices evolve

### Agent Updates

Update agent .md files when:

- Expertise changes
- Trigger conditions change
- Tool access changes

### Command Updates

Update command .md files when:

- Arguments change
- Behavior changes
- New features added

## Documentation Templates

### New Feature Documentation Template

```markdown
# Feature Name Analysis

## Overview

Brief description of the feature.

## Implementation

### Architecture

How it fits in the codebase.

### Key Classes

| Class     | Purpose     |
| --------- | ----------- |
| ClassName | Description |

### Data Flow

How data moves through the system.

## Usage

How to use the feature.

## Testing

How to test the feature.
```

### API Reference Template

````markdown
## ClassName

Brief description.

### Properties

| Property | Type | Description  |
| -------- | ---- | ------------ |
| Name     | Type | What it does |

### Methods

#### MethodName

```csharp
public ReturnType MethodName(ParamType param)
```

Description of method.

**Parameters:**

- `param`: Description

**Returns:** Description
````

## Keeping Docs in Sync

### Documentation Checklist

After significant changes:

- [ ] CLAUDE.md updated if architecture/build changed
- [ ] README.md updated if user-facing changed
- [ ] Skill references updated if domain knowledge changed
- [ ] SKILL.md updated if triggers/guidance changed
- [ ] Comments in code are accurate

### Cross-Reference Check

Ensure consistency between:

- CLAUDE.md ↔ skill reference summaries
- README.md ↔ CLAUDE.md (no conflicts)
- Skills ↔ their reference folders

## Additional Resources

### Reference Files

Study existing documentation:

- **CLAUDE.md** - AI guidance format
- **README.md** - User documentation format
- **Skill references** - Domain knowledge format (see routing guide above)

### Style Guidelines

- Concise but complete
- Code examples over prose
- Tables for structured data
- Keep CLAUDE.md actionable
- Keep README.md approachable
