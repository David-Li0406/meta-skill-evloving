---
name: memory
description: talloc-based memory management and ownership rules for ikigai
---

# Memory Management

talloc hierarchical memory allocator for ikigai. Use this for all new code.

## Why talloc?

- **Automatic cleanup** - Parent context frees all children
- **Ownership hierarchy** - Natural mapping to object lifecycles
- **Debugging built-in** - Leak detection and memory tree reporting
- **Battle-tested** - Used in Samba, proven reliable

## Ownership Rules

1. **Caller owns returned pointers** - Functions transfer ownership
2. **Each allocation has one owner** - That owner frees it
3. **Children freed with parent** - talloc hierarchy does this automatically
4. **Document ownership** - Make it explicit in function comments

## Core API

```c
// Context creation
TALLOC_CTX *talloc_new(const void *parent);

// Allocation (children of ctx)
void *talloc(const void *ctx, type);
void *talloc_zero(const void *ctx, type);
void *talloc_array(const void *ctx, type, count);
char *talloc_strdup(const void *ctx, const char *str);
char *talloc_asprintf(const void *ctx, const char *fmt, ...);

// Deallocation
int talloc_free(void *ptr);  // Frees ptr and ALL children

// Hierarchy manipulation
void *talloc_steal(const void *new_parent, const void *ptr);
void *talloc_reference(const void *ctx, const void *ptr);
```

## Pattern 1: Short-lived Request Processing

```c
void handle_request(const char *input) {
    TALLOC_CTX *req_ctx = talloc_new(NULL);

    // All allocations are children of req_ctx
    res_t res = ik_protocol_msg_parse(req_ctx, input);
    if (is_err(&res)) {
        talloc_free(req_ctx);
        return;
    }
    ik_protocol_msg_t *msg = res.ok;

    // ... process message ...

    talloc_free(req_ctx);  // Frees msg and all children at once
}
```

## Pattern 2: Allocate on Caller's Context

```c
res_t ik_cfg_load(TALLOC_CTX *ctx, const char *path) {
    // Allocate config as child of caller's context
    ik_cfg_t *config = talloc_zero_(ctx, sizeof(ik_cfg_t));
    if (!config) PANIC("Out of memory");

    // Strings are children of config
    config->openai_api_key = talloc_strdup(config, key_from_file);
    config->listen_address = talloc_strdup(config, addr_from_file);

    return OK(config);
}

// Caller owns and frees
TALLOC_CTX *ctx = talloc_new(NULL);
res_t res = ik_cfg_load(ctx, "config.json");
ik_cfg_t *config = res.ok;
// ... use config ...
talloc_free(ctx);  // Frees config and all strings
```

## Pattern 3: Struct Fields as Children

**Correct** - Fields are children of struct:

```c
res_t foo_init(TALLOC_CTX *ctx, foo_t **out) {
    foo_t *foo = talloc_zero_(ctx, sizeof(foo_t));

    // Allocate fields on foo (not on ctx)
    foo->name = talloc_strdup(foo, "example");     // Child of foo
    foo->data = talloc_array(foo, char, 1024);     // Child of foo

    *out = foo;
    return OK(*out);
}

// Now talloc_free(foo) frees name and data automatically
```

**Wrong** - Fields as siblings:

```c
// DON'T DO THIS
foo_t *foo = talloc_zero_(ctx, sizeof(foo_t));
foo->name = talloc_strdup(ctx, "example");  // Sibling, not child!
// Now talloc_free(foo) does NOT free name - memory leak
```

## Pattern 4: Temporary Contexts

```c
res_t process(TALLOC_CTX *ctx, input_t *in) {
    // Temporary context for intermediate work
    TALLOC_CTX *tmp = talloc_new(ctx);

    // Intermediate allocations on tmp
    char *buf = talloc_array(tmp, char, 4096);
    parsed_t *p = talloc_zero(tmp, parsed_t);

    // ... process ...

    // If keeping result, steal it to parent context
    result_t *result = process_internal(tmp, in);
    if (keep_result) {
        talloc_steal(ctx, result);
    }

    talloc_free(tmp);  // Cleans all intermediates
    return OK(result);
}
```

## Avoiding Fixed-Size Allocations

**CRITICAL**: Never use fixed-size allocations unless you know the exact size of the data.

```c
// NEVER: char buffer[1024]; sprintf(buffer, "%s: %s", key, value);
// ALWAYS: char *str = talloc_asprintf(ctx, "%s: %s", key, value);
```

**Strategies for unknown sizes:**

1. **Determine size first**: stat() for files, Content-Length for HTTP
2. **Growable buffers**: Start small, use talloc_realloc() to grow
3. **Read-measure-reread**: Count bytes first pass, allocate exact size, reread
4. **Return errors**: Fail if data exceeds reasonable limit

**Common cases:**
- String building → `talloc_asprintf(ctx, fmt, ...)`
- Path building → `talloc_asprintf(ctx, "%s/%s", dir, file)`
- File reading → `stat()` first, allocate `st.st_size`, then `read()`

**Rule**: If you don't know the size, use dynamic allocation.

## CRITICAL: Error Context Lifetime

**DANGER**: Never allocate errors on temporary contexts.

```c
// WRONG - Error allocated on tmp, then tmp freed = use-after-free
res_t bad_example(TALLOC_CTX *ctx) {
    TALLOC_CTX *tmp = talloc_new(ctx);

    res_t res = some_function(tmp);  // Error on tmp!
    if (is_err(&res)) {
        talloc_free(tmp);  // FREES THE ERROR!
        return res;        // Crash - res.err is freed
    }

    talloc_free(tmp);
    return OK(NULL);
}

// CORRECT - Pass parent context for error allocation
res_t good_example(TALLOC_CTX *ctx) {
    TALLOC_CTX *tmp = talloc_new(ctx);

    res_t res = some_function(ctx);  // Error on ctx (parent)
    if (is_err(&res)) {
        talloc_free(tmp);
        return res;  // Safe - error on ctx
    }

    talloc_free(tmp);
    return OK(NULL);
}
```

**Rule**: Functions that can fail should allocate errors on the parent context (usually first parameter), not on temporary contexts.

## Function Naming Conventions

- `*_init(TALLOC_CTX *ctx, foo_t **out)` - Allocate on ctx, return via out parameter
- `*_create()` - Allocates and returns owned pointer
- `*_load()` - Allocates and returns owned pointer (from file/network)
- `*_free()` - Deallocates object and all children
- `*_parse(TALLOC_CTX *ctx, ...)` - Parse and allocate on ctx

## When NOT to Use talloc

Rare cases for plain `malloc()`:
- FFI boundaries - Libraries expecting `free()`-able memory
- Long-lived singletons - Global state for entire program

**Default**: Use talloc for everything else.

## OOM Handling

Memory allocation failures call `PANIC("Out of memory")` which terminates the process immediately. OOM is not a recoverable error.

```c
void *ptr = talloc_zero(ctx, type);
if (!ptr) PANIC("Out of memory");  // LCOV_EXCL_BR_LINE
```

## Debugging

```c
// Enable leak reporting
talloc_enable_leak_report();
talloc_enable_leak_report_full();

// Dump memory tree
talloc_report_full(context, stdout);

// Report leaks at exit
atexit(talloc_report_full_on_exit);
```

## Common Mistakes

1. **Allocating fields on wrong parent** - Use `talloc_*(struct, ...)` not `talloc_*(ctx, ...)`
2. **Freeing struct but not fields** - Make fields children, not siblings
3. **Error on temp context** - Pass parent context to functions that can fail
4. **talloc_new(NULL) outside main()** - Should receive parent from caller
5. **Mixing malloc/free with talloc** - Pick one, use talloc

## Quick Reference

**Create context:**
```c
TALLOC_CTX *ctx = talloc_new(parent);  // parent=NULL for root
```

**Allocate:**
```c
foo_t *foo = talloc_zero_(ctx, sizeof(foo_t));
char *str = talloc_strdup(ctx, "text");
int *arr = talloc_array(ctx, int, 100);
```

**Free:**
```c
talloc_free(ctx);  // Frees ctx and ALL children recursively
```

**Move ownership:**
```c
talloc_steal(new_parent, ptr);  // ptr is now child of new_parent
```

---

For refactoring existing code, see `/load refactoring/memory`.

For full details, see `project/memory.md`.
