---
name: patterns/command-interpreter
description: Use this skill when you need to implement command and interpreter patterns in C for handling complex user inputs and commands.
---

# Command and Interpreter Patterns

## Overview

This skill combines the Command and Interpreter patterns to manage user inputs effectively, particularly in applications like REPLs (Read-Eval-Print Loops) and DSLs (Domain-Specific Languages).

## Command Pattern

Encapsulate a request as an object, allowing parameterization, queuing, and undo functionality. In C, this can be implemented using a struct that contains a function pointer and its arguments.

### Example Command Struct

```c
typedef struct {
    const char *name; // Command name
    res_t (*execute)(ik_repl_ctx_t *repl, const char *args); // Function to execute
    const char *help; // Help text for the command
} ik_command_t;
```

### Applications

- Each command (e.g., `/clear`, `/mark`, `/rewind`) is a discrete operation that can be executed.
- Commands can be logged, serialized, or replayed, enhancing functionality.

## Interpreter Pattern

Define a grammar and interpreter for a language. This involves parsing input into an Abstract Syntax Tree (AST) and evaluating it by walking the tree.

### Applications

- **Slash Commands:** For simple commands, direct string matching may suffice. However, as command syntax grows complex (with flags, subcommands, or expressions), a proper parser with grammar definition is recommended.
- **Future DSL Possibilities:**
  - Query language for conversation search
  - Filter expressions for message selection
  - Template syntax for prompts

### ANSI Parsing

Terminal escape sequences can be interpreted using a state machine, providing a lightweight interpreter for handling complex input.

## When to Use

Consider using this combined skill when developing applications that require sophisticated command handling and parsing capabilities, especially in interactive environments or when building DSLs.