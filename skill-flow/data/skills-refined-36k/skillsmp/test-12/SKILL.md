---
name: test
description: Run the test suite for the Ralph CLI
---

# /test - Run Tests

Run the test suite for the Ralph CLI.

## Usage

```
/test           # Run all tests
/test -update   # Update golden files after intentional UI changes
```

## Instructions

### Running Tests

Run the Go tests:

```bash
go test ./... -v
```

### Updating Golden Files

If tests fail due to intentional UI changes, update golden files:

```bash
go test ./internal/commands/... -update
```

### Reporting Results

Report results to the user with:
- Number of tests passed/failed
- Any failing test names and error messages
- Suggestion to run with `-update` if golden file mismatches are detected

## Test Coverage

### Picker TUI

Tests for `internal/commands/picker.go`:
- Initial view
- Navigation with j/down keys

### Run TUI

Tests for `internal/commands/run.go`:
- Progress at 50%
- Complete state (100%)
- No stories state

## Golden Files

Golden files are stored in `internal/commands/testdata/*.golden` and are used for visual regression testing of TUI components.
