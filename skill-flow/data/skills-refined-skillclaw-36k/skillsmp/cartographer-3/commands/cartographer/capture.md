---
model: haiku
allowed-tools: Task, Glob, Grep, Read, Write, Edit, AskUserQuestion
argument-hint: [--pattern|--antipattern|--task|--observation|--from-staging] [description]
description: Capture knowledge into atlas (patterns, anti-patterns, tasks, observations)
---

## Context

Arguments: `/cartographer:capture [TYPE] [DESCRIPTION]`
- **--pattern** - Capture a new pattern convention
- **--antipattern** - Capture an anti-pattern to avoid
- **--task** - Capture a task mapping or composition
- **--observation** - Capture a stack-specific observation
- **--from-staging** - Process all discoveries from staging file (created by /navigator:review)

If no type specified, interactive mode will ask questions.

Current directory: !`pwd`

## Purpose

Manually capture knowledge into the atlas. Use this command when:
- You discover a reusable pattern during development
- You encounter (and solve) a mistake worth documenting
- You identify a repeatable workflow
- You learn something stack-specific worth remembering

## Workflow

### 1. Pre-flight Checks

**Verify atlas exists:**
```bash
test -f ".claude/skills/atlas/references/schema.yaml" && echo "EXISTS" || echo "NOT_FOUND"
```

**If atlas not found:**
```
❌ No atlas found to capture knowledge into.

Run `/cartographer:chart` to generate an atlas first.
```
**STOP** - Cannot capture without atlas.

### 2. Determine Capture Type

**If type flag provided:**
- Use specified type
- Use description if provided

**If no type, enter interactive mode:**

```
📚 What would you like to capture?

1. Pattern - A reusable file/code convention
2. Anti-pattern - A mistake to avoid
3. Task mapping - A repeatable workflow
4. Observation - A stack-specific insight

Select (1-4):
```

### 3. Capture Pattern (--pattern)

**Gather pattern information:**

```
📝 New Pattern Capture

Pattern ID (snake_case): ___
Keywords (comma-separated): ___
File convention (path template): ___
Test convention (path template): ___
Example files (existing files that follow this pattern):
- ___
- ___
Validation commands:
- ___
Related patterns: ___
```

**Review existing patterns:**
- Read schema.yaml patterns section
- Check for similar existing patterns
- Warn if potential duplicate

**Generate pattern entry:**
```yaml
{pattern_id}:
  keywords:
    - {keyword1}
    - {keyword2}
  file_convention: '{file_convention}'
  test_convention: '{test_convention}'
  example_files:
    - '{example1}'
    - '{example2}'
  validation_commands:
    - '{command}'
  related:
    - {related_pattern}
  anti_patterns_summary: []  # Add with --antipattern
```

**Prompt for confirmation:**
```
Add this pattern to schema.yaml?

{yaml_preview}

[Yes] [Edit] [Cancel]
```

**Update schema.yaml patterns section.**

**Generate pattern guide stub:**

Create `.claude/skills/atlas/references/patterns/{pattern_id}.md`:

```markdown
# {Pattern Name} Pattern

> {Brief description from file_convention context}

## Purpose

<!-- TODO: Describe what this pattern accomplishes -->

## File Convention

**Location:** `{file_convention}`
**Naming:** `{naming convention inferred from examples}`
**Tests:** `{test_convention}`

## Structure

```
{directory containing pattern}/
├── {example1 basename}
├── {example2 basename}
└── ...
```

## Critical Conventions

<!-- TODO: Add 3-5 must-follow rules from codebase analysis -->

1. **TODO**: Add first critical convention
2. **TODO**: Add second critical convention
3. **TODO**: Add third critical convention

## Anti-Patterns

| Don't | Do Instead | Why |
|-------|------------|-----|
| TODO: Add first anti-pattern | TODO: Correct approach | TODO: Reason |

## Template (This Codebase)

```{language inferred from examples}
// TODO: Extract minimal template from example_files
```

## Implementation Checklist

- [ ] Create file following `{file_convention}`
- [ ] Follow naming convention from examples
- [ ] Add tests following `{test_convention}`
{#each registration steps}
- [ ] Register in `{file}`
{/each}

## Reference Implementations

| File | Demonstrates |
|------|--------------|
{#each example_files}
| `{file}` | TODO: What this example shows |
{/each}

## Validation

```bash
{#each validation_commands}
{command}
{/each}
```

{#if related patterns}
## Related Patterns

{#each related}
- [{pattern}](patterns/{pattern}.md) - TODO: Describe relationship
{/each}
{/if}
```

**Report pattern guide creation:**
```
📄 Pattern guide stub created: .claude/skills/atlas/references/patterns/{pattern_id}.md

The guide has TODO placeholders. Complete it by:
1. Reading example files to extract conventions
2. Documenting anti-patterns as you encounter them
3. Adding a minimal template from actual code

Or use /cartographer:explore --pattern {pattern_id} to auto-populate.
```

### 4. Capture Anti-Pattern (--antipattern)

**Gather anti-pattern information:**

```
⚠️ Anti-Pattern Capture

Related pattern ID: ___ (or "new" for global)
Anti-pattern description: "Don't ___"
Correct approach: "Instead, ___"
Why it's wrong: ___
```

**Validate anti-pattern:**
- Should start with "Don't..."
- Should be codebase-specific, not generic
- Should have a clear fix

**If pattern exists, add to anti_patterns_summary:**
```yaml
patterns:
  {pattern_id}:
    anti_patterns_summary:
      - existing item
      - "Don't {new_anti_pattern}"  # NEW
```

**Prompt for confirmation:**
```
Add anti-pattern to {pattern_id}?

"Don't {description}"

[Yes] [Edit] [Cancel]
```

**Update schema.yaml patterns section.**

### 5. Capture Task Mapping (--task)

**Gather task information:**

```
🔄 Task Mapping Capture

Task type:
1. Simple task mapping (single entry point)
2. Composition (multi-pattern workflow)

Select (1-2): ___
```

**For simple task mapping:**
```
Task ID (snake_case): ___
Description: ___
Entry point (directory/file): ___
Associated patterns:
- ___
```

**Generate task mapping:**
```yaml
task_mappings:
  {task_id}:
    description: '{description}'
    entry_point: {entry_point}
    patterns:
      - {pattern1}
      - {pattern2}
```

**For composition:**
```
Composition ID (snake_case): ___
Description: ___
Pattern sequence (in order):
1. ___
2. ___
3. ___
Validation sequence:
- ___
Notes: ___
```

**Generate composition:**
```yaml
compositions:
  {composition_id}:
    description: '{description}'
    patterns:
      - pattern: {pattern1}
        order: 1
      - pattern: {pattern2}
        order: 2
    validation_sequence:
      - '{command1}'
    notes: '{notes}'
```

**Prompt for confirmation and update schema.yaml.**

### 6. Capture Observation (--observation)

**Gather observation information:**

```
💡 Observation Capture

Category:
1. Technology choice
2. Configuration detail
3. Workaround
4. Performance note
5. Other

Select (1-5): ___

Description: ___
Evidence (what you observed): ___
```

**Read existing observations.md:**
```bash
cat .claude/skills/atlas/references/observations.md
```

**Append new observation:**
```markdown
## {Category}

### {Title}

{Description}

**Evidence:**
- {evidence1}
- {evidence2}

**Captured:** {timestamp}
```

**Prompt for confirmation and update observations.md.**

### 7. Process Staging File (--from-staging)

**Check for staging file:**
```bash
test -f ".claude/skills/atlas/staging/discoveries.yaml" && echo "EXISTS" || echo "NOT_FOUND"
```

**If not found:**
```
❌ No staging file found at .claude/skills/atlas/staging/discoveries.yaml

Staging files are created by /navigator:review when it discovers
patterns, anti-patterns, or conventions not in the atlas.

Run a review first, or use manual capture flags:
- /cartographer:capture --pattern
- /cartographer:capture --antipattern
- /cartographer:capture --observation
```

**Read and parse staging file:**
```bash
cat .claude/skills/atlas/staging/discoveries.yaml
```

**Group discoveries by type:**
- `anti_pattern` → Add to schema.yaml patterns.{pattern_id}.anti_patterns_summary
- `convention` → Add to relevant pattern guide or schema.yaml
- `pattern` → Create new pattern entry in schema.yaml

**Present summary for approval:**
```
📋 Staging File Contents

Found {count} discoveries to process:

Anti-Patterns ({count}):
1. [{pattern_id}] "{description}"
2. [{pattern_id}] "{description}"

Conventions ({count}):
1. [{pattern_id}] "{description}"

New Patterns ({count}):
1. [{suggested_id}] "{description}"

Options:
```
- "Process all" → Apply all discoveries
- "Review individually" → Prompt for each item
- "Clear staging" → Delete file without processing
- "Cancel" → Exit without changes

**For "Process all":**

For each discovery:
1. Read current schema.yaml
2. Apply the appropriate update
3. Write updated schema.yaml

**For anti-patterns:**
```yaml
# Add to existing pattern's anti_patterns_summary
patterns:
  {pattern_id}:
    anti_patterns_summary:
      - "existing anti-pattern"
      - "{new_anti_pattern}"  # ADDED
```

**For conventions:**
- If pattern guide exists, append to conventions section
- Otherwise, add as comment in schema.yaml pattern entry

**For new patterns:**
```yaml
# Add new pattern entry
patterns:
  {new_pattern_id}:
    keywords:
      - {keyword1}
      - {keyword2}
    file_convention: '{file_convention}'
    example_files:
      - '{evidence_file1}'
      - '{evidence_file2}'
    validation_commands:
      - 'npm run lint'
    anti_patterns_summary: []
```

**Update keyword_index:**
```yaml
keyword_index:
  {keyword1}: {new_pattern_id}
  {keyword2}: {new_pattern_id}
```

**Generate pattern guide stub for new patterns:**
Create `.claude/skills/atlas/references/patterns/{new_pattern_id}.md` using the pattern template (same as manual capture in Step 3).

**Clear staging file after successful processing:**
```bash
rm .claude/skills/atlas/staging/discoveries.yaml
```

**Report results:**
```markdown
## Staging Processed

**Discoveries applied:** {count}

| Type | Pattern | Description | Status |
|------|---------|-------------|--------|
| Anti-pattern | controllers | Direct DB queries | ✅ Added |
| Convention | providers | DI constructor pattern | ✅ Added |
| New Pattern | background_jobs | Job handler structure | ✅ Created |

**Files updated:**
- `.claude/skills/atlas/references/schema.yaml`
{#if new_patterns}
- `.claude/skills/atlas/references/patterns/{pattern_id}.md` (stub created)
{/if}

**Staging file cleared.**

The atlas is now up to date with these discoveries.

{#if new_patterns}
**Pattern guide stubs created:** {count}
Complete them by reading example files or use `/cartographer:explore --pattern {id}`.
{/if}
```

### 8. Report Completion

```markdown
## Knowledge Captured

**Type:** {pattern|antipattern|task|observation}
**Target file:** {schema.yaml|observations.md}

{Preview of what was added}

{#if type == pattern}
**Pattern guide created:** `.claude/skills/atlas/references/patterns/{pattern_id}.md`

The pattern guide has TODO placeholders. To complete it:
1. Review example files to extract conventions
2. Document anti-patterns as you encounter them
3. Add a minimal template from actual code

Or run `/cartographer:explore --pattern {pattern_id}` to auto-populate.
{/if}

---

The atlas has been updated. This knowledge will be used in future:
- `/navigator:plan` - For research and planning
- `/navigator:build` - For pattern guidance
- `/navigator:review` - For validation
```

---

## Examples

### Capture a new controller pattern:
```
/cartographer:capture --pattern

Pattern ID: api_controllers
Keywords: controller, endpoint, route, api
File convention: src/controllers/{name}.controller.ts
Test convention: src/controllers/__tests__/{name}.controller.test.ts
Example files: src/controllers/user.controller.ts
Validation: npm run lint, npm test -- controllers
```

### Capture an anti-pattern:
```
/cartographer:capture --antipattern

Pattern: controllers
Anti-pattern: "Don't import database clients directly - use the repository layer"
Correct: "Import from repositories/ instead"
```

### Capture a task mapping:
```
/cartographer:capture --task

Type: composition
ID: add_authenticated_endpoint
Description: Add a new API endpoint with auth
Patterns: controllers, middleware, providers
Validation: npm run typecheck, npm test
```

### Capture an observation:
```
/cartographer:capture --observation

Category: Configuration
Description: Redis connection requires explicit timeout
Evidence: Default timeout caused failures in CI, set to 5000ms
```

---

## Error Handling

| Error | Action | Recovery |
|-------|--------|----------|
| No atlas | Block with message | Run /cartographer:chart |
| Pattern exists | Warn, offer merge | User decides |
| Invalid ID | Reject, show rules | User fixes |
| File write fails | Error with details | Check permissions |

## Responsibilities

**YOU (handler):**
- Guide user through capture process
- Validate input format and uniqueness
- Preview changes before applying
- Update appropriate atlas files
- Confirm successful capture

**You grow the atlas. Each capture makes future development faster.**
