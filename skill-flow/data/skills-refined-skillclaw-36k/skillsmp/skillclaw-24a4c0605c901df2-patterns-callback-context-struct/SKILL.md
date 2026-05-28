---
name: patterns/callback-context-struct-observer
description: Use this skill when implementing callback mechanisms in C that require state management without relying on global variables.
---

# Callback Context and Observer Pattern (C-Specific)

This skill combines the Callback Context and Observer patterns to manage state in C applications effectively. It emphasizes passing context explicitly through function parameters, allowing for stateful callbacks without global variables.

## Core Pattern

1. **Callback Function Signature**: Always define callback functions to accept a `void *` context parameter as the first argument. This allows the callback to access necessary state without using global variables.

   ```c
   typedef void (*callback_t)(void *user_ctx, const char *data, size_t len);
   ```

2. **Function Implementation**: When implementing functions that utilize callbacks, ensure the context is passed along with the callback.

   ```c
   res_t ik_llm_stream(ik_llm_client_t *client,
                       ik_message_t **msgs,
                       callback_t on_chunk,
                       void *user_ctx);  // user_ctx is passed to the callback
   ```

## Benefits

- **State Management**: By passing a context struct, you can maintain state across multiple invocations without relying on global variables.
- **Multiple Instances**: This pattern allows for multiple instances of the same context, making it easier to manage different states in concurrent scenarios.
- **Testability**: The explicit context makes it easier to inject mock contexts for testing purposes.

## Example Usage

### Streaming Responses

In a REPL application, you can use the callback to handle streaming responses:

```c
void on_chunk(void *user_ctx, const char *data, size_t len) {
    // Handle the incoming data chunk
}

res_t result = ik_llm_stream(client, messages, on_chunk, repl_context);
```

### Observer Pattern Implementation

You can also implement an observer pattern where objects register interest in events and get notified via callbacks:

```c
void notify_observers(void *ctx, const char *event_data) {
    // Notify registered observers with the event data
}
```

### Conclusion

This combined pattern is a powerful approach for managing state and implementing callbacks in C, making your code cleaner, more modular, and easier to maintain.