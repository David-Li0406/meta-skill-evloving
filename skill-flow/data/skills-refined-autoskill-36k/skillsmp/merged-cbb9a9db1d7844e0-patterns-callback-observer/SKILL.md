---
name: patterns/callback-observer
description: Use this skill when implementing callback mechanisms in C to handle events and maintain state without globals.
---

# Callback and Observer Patterns in C

This skill combines the Callback and Observer patterns, allowing objects to register interest in events and receive notifications while maintaining state through user-defined context.

## Callback Pattern

Pair a function pointer with a `void *` user data parameter. The callback receives this user data, enabling state access without relying on global variables. This is a universal pattern for asynchronous and event-driven programming in C.

### Example Application

**Streaming responses:**
```c
typedef void (*chunk_cb_t)(void *user_ctx, const char *data, size_t len);

res_t ik_llm_stream(ik_llm_client_t *client,
                    ik_message_t **msgs,
                    chunk_cb_t on_chunk,
                    void *user_ctx);  // Passed to callback
```

**Usage:** The REPL passes itself as context, and the callback updates the scrollback.

**Convention:** The callback function pointer should be immediately followed by a `void *` context parameter. The callback signature includes the context as the first parameter.

**Benefit:** This approach allows for stateful callbacks without the need for global variables, as each caller can provide its own context.

## Observer Pattern

In this pattern, objects can register their interest in specific events and will be notified when those events occur. In C, this is typically implemented using callback function pointers with context.

### Example Application

**Streaming chunks:** An LLM client notifies the REPL as response chunks arrive:
```c
typedef void (*chunk_callback_t)(void *ctx, const char *chunk, size_t len);
res_t ik_llm_stream(client, messages, on_chunk, user_ctx);
```

**Additional Use Cases:**
- Database change notifications
- Tool execution progress updates
- Background task completion notifications

**Convention:** Always pair the callback function pointer with a `void *user_ctx` parameter to maintain context across callbacks.