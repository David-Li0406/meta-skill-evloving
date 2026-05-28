---
name: parse-ast
description: Parse TCL code and display the AST
user-invocable: true
allowed-tools: Bash, Read, Write
---

Parse TCL code and display the resulting Abstract Syntax Tree.

## Usage

`/parse-ast <file.tcl>` - Parse a TCL file and show AST
`/parse-ast` - Parse code from clipboard/input

## Commands

Parse a TCL file:
```bash
tclsh tcl/core/ast/builder.tcl $ARGUMENTS
```

## Output

Display the JSON AST with:
1. Root node structure
2. Children nodes (procedures, variables, control flow)
3. Comments extracted
4. Any parse errors

## Example

Input:
```tcl
proc hello {name} {
    puts "Hello, $name!"
}
```

Shows AST with procedure definition, parameters, and body.
