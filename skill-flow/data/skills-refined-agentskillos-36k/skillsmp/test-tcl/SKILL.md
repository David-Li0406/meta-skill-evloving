---
name: test-tcl
description: Run TCL parser tests
user-invocable: true
allowed-tools: Bash, Read
---

Run the TCL parser test suite.

## Usage

`/test-tcl` - Run all TCL tests
`/test-tcl json` - Run only JSON module tests
`/test-tcl procedures` - Run only procedure parser tests

## Commands

Run all TCL tests:
```bash
tclsh tests/tcl/core/ast/run_all_tests.tcl
```

Run specific module test:
```bash
tclsh tcl/core/ast/$ARGUMENTS.tcl
```

Run parser-specific test:
```bash
tclsh tests/tcl/core/ast/parsers/test_$ARGUMENTS.tcl
```

After running tests, report:
1. Total tests run
2. Pass/fail count
3. Any failing test details
