---
name: patterns/callback-context-struct-observer
description: Use this skill when implementing state management and event notification patterns in C development.
---

# Callback, Context Struct, and Observer Patterns (C-Specific)

This skill encompasses three related patterns for managing state and event notifications in C programming: the Callback + Context pattern, the Context Struct pattern, and the Observer pattern.

## Callback + Context Pattern

Pair function pointers with `void *` user data to enable callbacks that receive context, allowing state access without relying on global variables. This is a universal pattern for asynchronous and event-driven programming.

### Example Application
```c
typedef void (*chunk_cb_t)(void *user_ctx, const char *data, size_t len);

res_t ik_llm_stream(ik_llm_client_t *client,
                    ik_message_t **msgs,
                    chunk_cb_t on_chunk,
                    void *user_ctx);  // Passed to callback
```
**Usage:** The REPL passes itself as context, and the callback updates the scrollback.

**Convention:** The callback function pointer is followed by a `void *` context parameter, with the context as the first parameter in the callback signature.

**Benefit:** Enables stateful callbacks without globals, allowing each caller to provide its own context.

## Context Struct Pattern

Pass state explicitly as a struct pointer parameter instead of using global variables. The first parameter to functions should be a context containing state and dependencies.

### Example Application
```c
res_t ik_scrollback_append(ik_scrollback_t *ctx, const char *line);
```
**Core Pattern:** Every module utilizes context structs such as:
- `ik_repl_ctx_t` - REPL state
- `ik_term_ctx_t` - Terminal state
- `ik_scrollback_t` - Scrollback state
- `ik_env_t` - Runtime environment (planned)

**Benefits:**
- Eliminates global state
- Allows multiple instances
- Clarifies dependencies
- Enhances testability through mock contexts

## Observer Pattern

Objects can register interest in events and receive notifications when those events occur. This is implemented in C using callback function pointers with context.

### Example Application
```c
typedef void (*chunk_callback_t)(void *ctx, const char *chunk, size_t len);
res_t ik_llm_stream(client, messages, on_chunk, user_ctx);
```
**Use Cases:**
- Streaming response chunks from an LLM client to the REPL
- Notifying the REPL of terminal resize events (e.g., SIGWINCH)
- Future applications may include database change notifications, tool execution progress, and background task completion.

**Convention:** Always pair the callback function pointer with a `void *user_ctx` parameter.

By utilizing these patterns, developers can create more maintainable and testable C applications that effectively manage state and handle events.