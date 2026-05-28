# CI Doctor Learnings

Domain-specific corrections and gotchas for CI/CD pipeline fixes.

## Gotchas

### GitHub Alert Dismissal Format
- **Pattern:** Dismissing CodeQL security alerts via API
- **Wrong:** `"reason": "false_positive"` (underscore)
- **Right:** `"reason": "false positive"` (space)
- **Why:** GitHub API expects space-separated words, not snake_case

### Supabase Anon Key False Positives
- **Pattern:** CodeQL flags `SUPABASE_ANON_KEY` as exposed secret
- **Wrong:** Trying to hide/rotate the key
- **Right:** Dismiss as false positive - anon keys are intentionally public
- **Why:** Supabase anon keys are designed to be client-side, RLS provides security

### TypeScript Unused Import Warnings
- **Pattern:** CodeQL `js/unused-local-variable` for imports
- **Wrong:** Prefixing with underscore `_unusedImport`
- **Right:** Remove the import entirely
- **Why:** Unused imports are dead code; underscore convention is for parameters only

## Anti-Patterns

| Don't | Do Instead | Reason |
|-------|------------|--------|
| Re-run CI without investigating | Read error logs first | May mask real issues |
| Add `// @ts-ignore` to fix type errors | Fix the actual type | Ignore hides problems |
| Skip pre-commit hooks with `--no-verify` | Fix what the hook catches | Hooks exist for a reason |

## Sticky Fixes

- **"Generated types changed" failures:** Run `npx supabase gen types...` and commit the result
- **Package-lock.json conflicts:** Delete and run `npm install` to regenerate
- **Biome format failures:** Run `npx @biomejs/biome check --write .` before commit

---

*Update when discovering CI-specific issues that would trip up future debugging.*
