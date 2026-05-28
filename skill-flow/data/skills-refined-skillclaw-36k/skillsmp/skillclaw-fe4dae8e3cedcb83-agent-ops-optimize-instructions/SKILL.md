---
name: agent-ops-optimize-instructions
description: Use this skill when you need to optimize agent instruction files by extracting sections into separate files and referencing them, reducing context size while preserving information.
---

# Instruction File Optimization Workflow

## Purpose

Optimize agent or instruction files (AGENTS.md, copilot-instructions.md, SKILL.md, etc.) by:

1. Identifying logical sections that can be extracted.
2. Moving verbose content to separate reference files.
3. Replacing with concise summaries and links.
4. Reducing total context size while preserving information.

This helps keep prompt context within token limits while maintaining comprehensive guidance.

## When to Use

- Instruction file exceeds recommended size (~2000 lines).
- File contains large code examples or detailed procedures.
- Multiple sections could be shared across files.
- Agent consistently runs out of context.
- Preparing instructions for smaller context models.

## Optimization Strategies

### Strategy 1: Section Extraction

Extract large, self-contained sections into reference files.

**Before:**
```markdown
# AGENTS.md

## API Guidelines
{500 lines of detailed API guidelines}

## Testing Patterns
{300 lines of testing examples}
```

**After:**
```markdown
# AGENTS.md

## API Guidelines
See: [api-guidelines.md](.github/reference/api-guidelines.md)
Key points: REST conventions, error handling, versioning.

## Testing Patterns  
See: [testing-patterns.md](.github/reference/testing-patterns.md)
Key points: pytest fixtures, mocking, coverage targets.
```

### Strategy 2: Example Consolidation

Move detailed examples to reference files, keeping summaries inline.

**Before:**
```markdown
### Example: Complex Query
```python
def complex_query(db, filters, pagination, sorting):
    # 50 lines of example code
    ...
```
```

**After:**
```markdown
### Example: Complex Query
See: [examples/complex-query.py](.github/reference/examples/complex-query.py)
Pattern: Filter → Paginate → Sort → Execute
```

### Strategy 3: Conditional Loading

Mark sections as "load on demand" for agents that support it.

```markdown
## Advanced Configuration
<!-- LOAD_ON_DEMAND: Only load when user asks about configuration -->
See: [advanced-config.md](.github/reference/advanced-config.md)
```

### Strategy 4: Tiered Detail

Keep high-level summaries inline, linking to detailed content as needed.