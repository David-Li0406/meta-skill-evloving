---
name: test-lua
description: Run Lua/Neovim plugin tests
user-invocable: true
allowed-tools: Bash, Read
---

Run the Lua plugin test suite using plenary.nvim.

## Usage

`/test-lua` - Run all Lua tests
`/test-lua server` - Run only server tests
`/test-lua config` - Run only config tests

## Commands

Run all Lua tests:
```bash
make test-unit
```

Run filtered tests (replace FILTER with test name pattern):
```bash
nvim --headless --noplugin -u tests/minimal_init.lua \
  -c "lua require('plenary.test_harness').test_directory('tests/lua/', {minimal_init = 'tests/minimal_init.lua', filter = '$ARGUMENTS'})" \
  -c "qa!"
```

After running tests, report:
1. Total tests run
2. Pass/fail count
3. Any failing test details with file:line references
