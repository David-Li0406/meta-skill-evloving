---
name: unison-development
description: Use this skill when writing, testing, and updating Unison code with the Unison MCP tool, particularly for Unison language files (.u extension) and UCM operations.
---

# Unison Development

- Uses `development` and `xp` skills for a TDD workflow, enhanced with Unison-specific tooling.
- Use the Unison MCP server commands for all operations.

## Core Principles

1. **NEVER run UCM commands on the command line** — use MCP tools only.
2. Code is stored by the Unison Code Manager (UCM), not Git.
3. **TDD is mandatory** — be aware UCM may enter "Handling typecheck errors after update."
4. **Always** use fully qualified names in `scratch.u`.
5. **Never** create multiple scratch files.
6. **ALWAYS** wait for user confirmation after `update` before continuing.
7. **ALWAYS** typecheck code with the Unison MCP server before adding to the scratch file.
8. Write code to the `scratch.u` file in the current directory after it typechecks.
9. After a successful update, you may delete the scratch file.
10. Use the MCP service tool to explore the codebase before writing code.

## Workflow

### 1. Research & Understanding

Use MCP tools to explore before writing:

- `view-definitions` for existing implementations.
- `search-definitions-by-name` for related functions.
- `docs` for library functions.

### 2. Branch

Ask the user to create a feature branch before beginning.

### 3. Clear Scratch Files

Ask the user if they want `scratch.u` deleted.

### 4. Write Tests First

Use `test.verify`, `labeled`, and `ensureEqual`:

```unison
projectName.module.tests.featureTest : '{IO, Exception} [Result]
projectName.module.tests.featureTest = do
  test.verify do
    labeled "Description" do
      use test ensureEqual
      result = performOperation testData
      ensureEqual result expectedValue
```

### 5. Typecheck Incrementally

```
mcp__unison__typecheck-code with {"text": "code here"}
```

Iterate until clean — fix type errors, add imports, verify effects.

### 6. Add to Scratch.u with Fully Qualified Names

- **WRONG:** `foo : Text -> ...`
- **CORRECT:** `projectName.module.foo : Text -> ...`

**Why:** Without fully qualified names, Unison creates a new function instead of modifying existing functions.

Typecheck output indicators:

- `+` (added) — new definition
- `~` (modified) — updated existing

**Verify you see `~` for modifications!**

### 7. Final Typecheck

```
mcp__unison__typecheck-code with {"filePath": "/path/to/scratch.u"}
```

### 8. UPDATE MODE: Handling Typecheck Errors

If UCM adds this comment after an update:

```
-- The definitions below no longer typecheck with the changes above.
-- Please fix the errors and try `update` again.
```

**CRITICAL:**

- **DO NOT** delete functions from `scratch.u` — they will be removed from the codebase.
- Repair broken code, typechecking as you go.
- Ask the user to verify via UCM output.
- After a successful update, you may remove code from `scratch.u`.

## Success Criteria

- All code typechecks successfully.
- Tests written before implementation.
- Fully qualified names in `scratch.u`.
- Modified functions show `~` not `+`.
- Comprehensive test coverage.

### Modifying Abilities

When modifying `abilities`, it is easier to modify the ability first, ask the user to `update` in the UCM which will result in an `update` branch, fix the code in the `update` branch, then ask the user to `update`.