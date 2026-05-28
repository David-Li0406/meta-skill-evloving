---
name: patterns/command-interpreter
description: Use this skill when you need to implement command and interpreter patterns in C for handling complex input and operations.
---

# Command and Interpreter Patterns

## Interpreter Pattern

Define a grammar and interpreter for a language. Parse input into an Abstract Syntax Tree (AST) and evaluate it by walking the tree. This pattern is useful for Domain-Specific Languages (DSLs), expressions, and commands.

### Applications
- **Slash commands:** Implement a simple interpreter to parse command names and arguments, dispatching them to the appropriate handler.
- **Future DSL possibilities:**
  - Query language for conversation search
  - Filter expressions for message selection
  - Template syntax for prompts

### Considerations
If command syntax becomes complex (involving flags, subcommands, or expressions), consider developing a proper parser with a defined grammar. For simpler cases, direct string matching may suffice.

## Command Pattern

Encapsulate a request as an object, allowing for parameterization, queuing, and undo functionality. In C, this can be implemented using a struct that contains a function pointer along with its arguments.

### Applications
- **Slash commands:** Each command (e.g., `/clear`, `/mark`, `/rewind`) is treated as a discrete operation:
  ```c
  typedef struct {
      const char *name;
      res_t (*execute)(ik_repl_ctx_t *repl, const char *args);
      const char *help;
  } ik_command_t;
  ```
- **Input actions:** The parser emits action structs that the Read-Eval-Print Loop (REPL) executes.

### Future Uses
- Implementing an undo/redo stack for input editing
- Queued tool executions
- Macro recording and playback

### Benefits
Commands become first-class entities, allowing them to be logged, serialized, or replayed, enhancing the flexibility and maintainability of the code.