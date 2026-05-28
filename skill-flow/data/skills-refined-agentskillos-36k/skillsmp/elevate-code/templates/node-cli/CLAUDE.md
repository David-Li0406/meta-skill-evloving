# My Tool - AI Collaboration Guide

## Project Overview

My Tool is a Node.js CLI tool that [describe what it does].

**Tech Stack**: Node.js 18+, Commander, Vitest

## Architecture

```
Input → [Processing] → Output
```

## Key Files

| File | Purpose |
|------|---------|
| `src/cli.js` | Entry point, argument parsing |
| `src/processor.js` | Core business logic |
| `src/state.js` | State persistence |
| `tests/setup.js` | Shared test mocks |

## Patterns

### The Triad
- **Doctor**: `cli.js:doctor()` checks dependencies
- **Safety Net**: TODO - implement deletion log
- **Statekeeper**: TODO - implement state persistence

### Conventions
- CommonJS modules (ESM deps via dynamic import)
- JSDoc comments for types
- No circular requires

## Testing

```bash
# Run tests
npm test

# Watch mode
npm run test:watch
```

## Common Tasks

### Adding a new command

1. Add command in `cli.js`
2. Create handler in appropriate module
3. Add tests

### Adding a dependency check

Add to `cli.js:doctor()`:
```javascript
['binary-name', checkBinary('binary-name')],
```
