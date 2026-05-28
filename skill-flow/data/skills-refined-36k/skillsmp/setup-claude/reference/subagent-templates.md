# Subagent Templates Reference

This reference documents the available subagent templates and their configurations.

## Quick Reference

| Template | Tools | Purpose |
|----------|-------|---------|
| planner.md | Read, Glob, Grep | Feature planning without editing |
| code-reviewer.md | Read, Glob, Grep | Quality review without fixes |
| tdd-guide.md | Read, Write, Edit, Bash | Test-first development |
| refactor-cleaner.md | Read, Edit, Grep | Remove dead code |

## Template Details

### planner.md

**Purpose**: Create implementation plans for features without writing code.

**Tool Scope**:
```yaml
allowed-tools:
  - Read      # Read existing code
  - Glob      # Find files
  - Grep      # Search patterns
```

**Workflow**:
1. Read requirements/PRD
2. Explore codebase structure
3. Identify affected files
4. Create step-by-step plan
5. Identify risks and dependencies

**Output**: Implementation plan with:
- File-by-file changes
- Dependency order
- Risk assessment
- Test strategy

**When to Use**:
- Before implementing any significant feature
- When you need to understand scope
- To prevent scope creep during implementation

---

### code-reviewer.md

**Purpose**: Review code quality without making fixes.

**Tool Scope**:
```yaml
allowed-tools:
  - Read      # Read code
  - Glob      # Find related files
  - Grep      # Search patterns
```

**Workflow**:
1. Read changed files
2. Check against conventions
3. Look for security issues
4. Verify error handling
5. Check test coverage
6. Document findings

**Output**: Review report with:
- Issues by severity (critical, important, minor)
- Specific line references
- Suggested fixes (but no edits)
- Approval/rejection recommendation

**When to Use**:
- After completing a feature
- Before merging PR
- Periodic code quality checks

---

### tdd-guide.md

**Purpose**: Implement features using test-driven development.

**Tool Scope**:
```yaml
allowed-tools:
  - Read      # Read existing code
  - Write     # Create new files
  - Edit      # Modify files
  - Glob      # Find files
  - Grep      # Search patterns
  - Bash      # Run tests
```

**Workflow** (Red-Green-Refactor):
1. **Red**: Write failing test first
2. **Green**: Write minimal code to pass
3. **Refactor**: Improve code quality
4. Repeat for each feature piece

**Output**:
- Implemented feature
- Comprehensive test suite
- All tests passing

**When to Use**:
- Features requiring high reliability
- Complex business logic
- When test coverage is important

---

### refactor-cleaner.md

**Purpose**: Remove dead code and clean up unused items.

**Tool Scope**:
```yaml
allowed-tools:
  - Read      # Read code
  - Edit      # Remove code
  - Glob      # Find files
  - Grep      # Find usages
```

**Workflow**:
1. Identify potentially dead code
2. Search for usages across codebase
3. Verify no references exist
4. Remove confirmed dead code
5. Document removals

**Note**: No Write tool - cannot create new files, only modify existing.

**Output**:
- Cleaned codebase
- List of removed items
- Verification of no broken references

**When to Use**:
- Regular codebase maintenance
- After removing features
- Before major refactoring

## Template Structure

All templates follow this format:

```markdown
---
name: template-name
description: Brief description of purpose
allowed-tools:
  - Tool1
  - Tool2
---

# Template Name

You are a specialized agent for [purpose].

## Your Constraints

[What you CAN and CANNOT do]

## Workflow

[Step-by-step process]

## Output Format

[Expected deliverable format]

## Important Rules

[Key behavioral rules]
```

## Customization Guidelines

### Adding Tools

Only add tools when necessary:

```yaml
# Original
allowed-tools:
  - Read
  - Glob
  - Grep

# With WebSearch for external docs
allowed-tools:
  - Read
  - Glob
  - Grep
  - WebSearch
```

### Removing Tools

Remove tools to increase focus:

```yaml
# Original (full dev)
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash

# Read-only analysis
allowed-tools:
  - Read
  - Glob
  - Grep
```

### Creating Custom Templates

1. Copy closest existing template
2. Modify tool scope
3. Update workflow instructions
4. Test with sample task

## Tool Reference

| Tool | Can Do | Cannot Do |
|------|--------|-----------|
| Read | View file contents | Modify files |
| Write | Create new files | Modify existing |
| Edit | Modify existing files | Create new files |
| Glob | Find files by pattern | Read contents |
| Grep | Search file contents | Modify files |
| Bash | Run commands | Direct file editing |
| WebSearch | Search internet | Access local files |
| WebFetch | Fetch URL content | Modify anything |

## Best Practices

### Keep Tools Minimal

More tools = more ways to get distracted.

**Good**: Planner with only Read, Glob, Grep
**Bad**: Planner with full editing capabilities

### Match Tools to Purpose

**Review task**: No Edit (pure observation)
**Implementation**: Full tools (needs to code)
**Cleanup**: Edit but no Write (modify, don't create)

### Document Constraints Clearly

In the template, explicitly state:
- What the subagent should do
- What it should NOT attempt
- How to handle blocked actions

### Test Before Using

Run a sample task to verify:
- Correct tools available
- Workflow makes sense
- Output format works
