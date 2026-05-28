---
name: verify-app
description: Validate application behavior with tests and manual verification steps. Use after feature changes or before deploys.
---

# Application Verification

## Workflow

1. Inspect project structure and test setup.
2. Run existing tests and capture results.
3. Propose additional tests if gaps exist.
4. Verify app startup and basic flows.
5. Report findings with clear next steps.

## Common commands

- Node.js/TypeScript: `npm test`, `npm run test:coverage`, `npm run dev`
- Go: `go test ./...`, `go test -cover ./...`, `go run main.go`
- Python: `pytest`, `pytest --cov`
- Rust: `cargo test`, `cargo run`

## Report format

```
## Application Verification Report

### Timestamp
YYYY-MM-DD HH:MM

### Environment
- OS:
- Runtime version:
- Dependency versions:

### Test results
- total / passed / failed / skipped
- coverage (if available)

### App startup
- status
- notes

### Issues
1. [Severity] description

### Recommended actions
- next steps
```
