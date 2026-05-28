---
name: validate-schema
description: Validate TCL AST against Lua schema definitions
user-invocable: true
allowed-tools: Bash, Read
---

## Usage

- `/validate-schema` - Validate all fixture files against schema
- `/validate-schema <file.tcl>` - Validate a specific TCL file

## What This Does

This skill validates that the TCL parser output conforms to the expected AST schema defined in Lua. It helps detect serialization drift between the TCL and Lua components.

## Implementation

1. Parse TCL file(s) with the TCL parser to get JSON AST
2. Validate the JSON against `lua/tcl-lsp/parser/schema.lua`
3. Report any schema violations with paths and error messages

## Commands

```bash
# Validate all fixtures
./scripts/validate-schema.sh

# Validate specific file
./scripts/validate-schema.sh path/to/file.tcl

# Run via make
make validate-schema
```

## Output

- **OK**: File validates successfully against schema
- **ERROR**: Schema violation found with path and message

## Example

```
$ /validate-schema

[INFO] Starting schema validation...
[INFO] Valid: basic.tcl
[INFO] Valid: procedures.tcl
[ERROR] Validation failed: namespace.tcl
  ERROR: Missing required field 'name' for node type 'namespace' at root.children[1]
[ERROR] Schema validation failed: 1/3 file(s) with drift
```
