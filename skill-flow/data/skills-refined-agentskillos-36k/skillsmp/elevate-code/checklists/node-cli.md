# Node.js CLI Checklist

Complete validation checklist for Node.js CLI tools.

---

## Project Structure

- [ ] `package.json` with `"bin"` field
- [ ] Entry point with shebang: `#!/usr/bin/env node`
- [ ] `src/` directory for source files
- [ ] `src/cli.js` for argument parsing
- [ ] `tests/` directory with setup file
- [ ] `README.md` with installation and usage
- [ ] `CLAUDE.md` with architecture and patterns
- [ ] `.gitignore` excluding `node_modules/`, `dist/`
- [ ] Module system declared (`"type": "commonjs"` or `"module"`)

## The Triad

### Health (Doctor)
- [ ] `<tool> setup` or `<tool> doctor` command exists
- [ ] Checks external binaries with version validation
- [ ] Checks required environment variables
- [ ] Checks credentials/config files exist
- [ ] Error messages include: what's missing + how to fix
- [ ] Interactive setup wizard for first-time users

### Safety (Safety Net)
- [ ] `--dry-run` flag for destructive operations
- [ ] Batch operations require `--dry-run` or `--yes`
- [ ] Deletion log (`~/.config/<tool>/deletion-log.json`)
- [ ] `<tool> restore` command to undo deletions
- [ ] Log BEFORE executing destructive action

### Resilience (Statekeeper)
- [ ] Long operations checkpoint after each item
- [ ] State file uses atomic writes (temp + rename)
- [ ] Resume detection on restart
- [ ] API calls retry with exponential backoff
- [ ] Graceful shutdown on SIGINT/SIGTERM

## Data Models

- [ ] JSDoc comments with `@typedef` for complex types
- [ ] TypeScript definitions (`.d.ts`) if publishing
- [ ] No raw objects in function signatures
- [ ] Enums as frozen objects or string constants
- [ ] Serialization functions for persistence

## Code Organization

- [ ] `cli.js` only parses arguments (no business logic)
- [ ] One file = one responsibility
- [ ] No circular requires
- [ ] Files under ~300 lines
- [ ] `utils.js` contains pure functions only
- [ ] ESM imports dynamic for chalk/ora (if using CommonJS)

## Error Handling

- [ ] Custom error classes extend `Error`
- [ ] Error messages include: what, why, fix
- [ ] Transient errors retry with backoff
- [ ] Non-retryable errors fail fast
- [ ] Silent fallback for non-critical failures (return defaults)

## Testing

- [ ] Vitest or Jest configured
- [ ] `tests/setup.js` with global mocks
- [ ] `__mocks__/` for manual mocks (googleapis, etc.)
- [ ] External APIs mocked (no real network calls)
- [ ] Core business logic has good coverage
- [ ] Tests run in <10 seconds

## Build & Deploy

- [ ] `package.json` with `"bin"` entry
- [ ] `"engines"` specifies Node.js version
- [ ] `"files"` limits published files
- [ ] `npm run test` configured
- [ ] `npm run lint` configured (ESLint)
- [ ] `prepublishOnly` runs tests
- [ ] GitHub Actions for CI
- [ ] GitHub Actions for npm publish

## CLI UX

- [ ] `--help` shows usage, options, examples
- [ ] `--version` shows version number
- [ ] `--json` outputs machine-readable JSON
- [ ] `--quiet` suppresses non-essential output
- [ ] `--verbose` shows detailed progress
- [ ] Spinner for indeterminate operations (`ora`)
- [ ] Colored output (`chalk`) with fallback
- [ ] Interactive prompts for setup

## Documentation

- [ ] README has: installation, quick start, all commands
- [ ] CLAUDE.md has: architecture, key files, patterns
- [ ] JSDoc comments on public functions
- [ ] Examples in README
- [ ] Troubleshooting section

## State Persistence

- [ ] Config in `~/.config/<tool>/`
- [ ] Per-account state: `state-<account>.json`
- [ ] All writes are atomic
- [ ] Graceful handling of corrupt/missing files
- [ ] Auto-cleanup of old state entries

---

## Quick Validation

```bash
# Check project structure
ls package.json src/ tests/
cat package.json | jq '.bin'

# Check Triad patterns
grep -rE "(doctor|setup|check)" src/   # Health
grep -rE "(undo|restore|deletion)" src/ # Safety
grep -rE "(state|checkpoint|resume)" src/ # Resilience

# Check tests
npm test -- --listTests 2>/dev/null || npm test

# Run lint
npm run lint
```
