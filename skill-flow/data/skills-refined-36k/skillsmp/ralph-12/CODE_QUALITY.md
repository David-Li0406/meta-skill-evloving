# Ralph Code Quality Guidelines

These guidelines are included in Ralph's `prompt.md` and can be reinforced via `guardrails.md`.

## Why Modularity Matters for Ralph

Each Ralph iteration has **fresh context**. Modular code helps because:
- Small files are easier to understand in one context window
- Clear boundaries mean less code to read per task
- Shared utilities can be reused across iterations
- Tests are easier to write for focused modules

## File Size Guidelines

| Lines | Status | Action |
|-------|--------|--------|
| < 150 | Small | Good for utilities, may be over-split |
| 150-500 | Optimal | Sweet spot for AI and human review |
| 500-1000 | Large | Look for natural split points |
| 1000+ | Too large | Must split before continuing |

## Guardrail Seeds for Code Quality

Add these to `.ralph/guardrails.md` if code quality issues occur:

```markdown
## Code Quality (Seeded)

### File Organization
- New features go in dedicated modules, not existing large files
- Shared utilities belong in `utils/` or `lib/`
- Keep handlers/controllers thin, logic in services

### Naming
- Files: snake_case.py, kebab-case.ts
- Functions: verb_noun (process_payment, validate_input)
- Classes: PascalCase (PaymentProcessor, InputValidator)

### Boundaries
- Pure functions have no side effects
- I/O (database, API, files) isolated in handlers
- Business logic separate from framework code
```

## Anti-Patterns to Detect

When Ralph adds guardrails after validation failures, watch for:

| Symptom | Likely Cause | Guardrail to Add |
|---------|--------------|------------------|
| "Can't find function" | Monolithic files | Split file by concern |
| "Merge conflict" | Same file edited | Use smaller, focused files |
| "Test timeout" | Large test file | Split tests by module |
| "Import error" | Circular deps | Extract shared to utils |

## Project-Specific Guidelines

During `/ralph setup`, Clorch should detect and include:

```markdown
## Project Patterns (from analysis)

**Stack:** {framework}
**Style:** {detected patterns}

**File locations:**
- New components: src/components/
- New API routes: src/api/
- Utilities: src/lib/
- Tests mirror source: tests/

**Conventions:**
- {detected naming convention}
- {detected import style}
- {detected error handling pattern}
```

## Validation Commands for Code Quality

Add these to task.md for quality checks:

```markdown
### Lint check
- description: Ensure code passes linting
- validation: `npm run lint` or `ruff check .`
- passes: false

### Type check
- description: Ensure types are correct
- validation: `npm run typecheck` or `pyright`
- passes: false

### File size check
- description: No files over 500 lines
- validation: `find src -name "*.ts" -exec wc -l {} + | awk '$1 > 500 {exit 1}'`
- passes: false
```

## Integration with Tasks

When using Claude Code Tasks, Ralph can create sub-tasks for refactoring:

```
Task: Implement payment feature
  └── Sub-task: Extract payment utils (if logic > 200 lines)
  └── Sub-task: Create payment handler
  └── Sub-task: Add payment tests
```

This keeps each task focused and modular.
