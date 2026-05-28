---
title: CLAUDE.md Sign Format
description: Format specification for writing learning signs to CLAUDE.md files. Used by /m42-signs:apply command.
keywords: claude-md, signs, format, learnings, markdown
skill: managing-signs
---

# CLAUDE.md Sign Format

## Section Location

Signs are stored in a dedicated `## Signs` section within CLAUDE.md files.

| Element | Level | Example |
|---------|-------|---------|
| Signs section header | `## Signs` | `## Signs` |
| Individual sign | `### <Title>` | `### Quote Variables in yq` |

## Sign Structure

```markdown
### <Title>
**Problem**: <problem description>
**Solution**: <solution description>
**Origin**: <origin reference>
```

## Field Specifications

| Field | Format | Required | Description |
|-------|--------|----------|-------------|
| Title | `###` header | Yes | Short, descriptive title (1 line) |
| Problem | `**Problem**:` | Yes | What went wrong or issue encountered |
| Solution | `**Solution**:` | Yes | How to fix or avoid the issue |
| Origin | `**Origin**:` | Yes | Source tracking for the learning |

## Origin Format

### Extracted Learnings

```
Extracted from session (Tool: <tool-name>) [<confidence> confidence]
```

Example:
```
Extracted from session (Tool: Bash) [high confidence]
```

### Manual Learnings

```
Manual addition via /m42-signs:add
```

## Complete Examples

### Single Sign

```markdown
## Signs

### Quote Variables in yq
**Problem**: yq expressions with special characters fail without proper quoting in shell scripts
**Solution**: Always wrap yq expressions in single quotes and use double quotes for string values inside
**Origin**: Extracted from session (Tool: Bash) [high confidence]
```

### Multiple Signs

```markdown
## Signs

### Quote Variables in yq
**Problem**: yq expressions with special characters fail without proper quoting in shell scripts
**Solution**: Always wrap yq expressions in single quotes and use double quotes for string values inside
**Origin**: Extracted from session (Tool: Bash) [high confidence]

### Check File Exists Before Read
**Problem**: Read tool fails with cryptic error when file doesn't exist
**Solution**: Use preflight check with `test -f` before Read operations
**Origin**: Manual addition via /m42-signs:add

### Use Absolute Paths in Scripts
**Problem**: Relative paths break when script is called from different directories
**Solution**: Use `$(dirname "$0")` or `${BASH_SOURCE[0]}` to construct absolute paths
**Origin**: Extracted from session (Tool: Bash) [medium confidence]
```

## Section Placement

Signs section should be placed:
- After main content sections
- Before any appendix or reference sections
- At end of file if no clear placement

```markdown
# Project CLAUDE.md

## Overview
Project description...

## Build Commands
- npm run build
- npm run test

## Code Style
Guidelines...

## Signs

### Sign Title
**Problem**: ...
**Solution**: ...
**Origin**: ...
```

## Creating New Section

When CLAUDE.md has no Signs section:

1. Add blank line at end of file
2. Add `## Signs` header
3. Add blank line
4. Add first sign

```markdown
<existing content>

## Signs

### First Sign Title
**Problem**: Description
**Solution**: Description
**Origin**: Source
```

## Appending to Existing Section

When Signs section exists:

1. Find last `###` entry in Signs section
2. Add blank line after last entry
3. Add new sign

```markdown
## Signs

### Existing Sign
**Problem**: ...
**Solution**: ...
**Origin**: ...

### New Sign
**Problem**: ...
**Solution**: ...
**Origin**: ...
```

## Multiline Content

Problem and Solution fields support multiline content:

```markdown
### Complex Error Handling
**Problem**: Error messages span multiple lines and include stack traces.
The original error context is lost when rethrowing.
**Solution**: Use error chaining pattern:
- Wrap original error as cause
- Add context to message
- Preserve stack trace
**Origin**: Manual addition via /m42-signs:add
```

## Integration with Native Injection

CLAUDE.md files are automatically injected into Claude Code context. Signs section becomes part of Claude's working knowledge for the project scope where the CLAUDE.md resides.

| CLAUDE.md Location | Scope |
|-------------------|-------|
| `./CLAUDE.md` | Project root - applies to entire project |
| `./src/CLAUDE.md` | src directory subtree |
| `./tests/CLAUDE.md` | tests directory subtree |
| `~/.claude/CLAUDE.md` | Global user scope |
