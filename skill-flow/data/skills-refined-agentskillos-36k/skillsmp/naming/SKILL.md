---
name: naming
description: Naming Conventions skill for the ikigai project
---

# Naming Conventions

## Description
Load naming conventions for ikigai C codebase.

## Public Symbol Pattern

All public symbols follow: `ik_MODULE_THING`
- `ik_` - namespace prefix
- `MODULE` - single word (config, protocol, openai, handler)
- `THING` - descriptive name with approved abbreviations

Examples:
- `ik_cfg_load()` - function
- `ik_protocol_msg_t` - type
- `ik_httpd_shutdown` - global variable

**Module Organization:** One subdirectory = One module. All symbols from a module use the same prefix regardless of file location.

## Approved Abbreviations

MUST use these consistently (types, functions, fields, variables):

| Full Word | Abbrev | Domain |
|-----------|--------|--------|
| configuration | `cfg` | Universal |
| message | `msg` | Universal |
| context | `ctx` | Universal |
| connection | `conn` | Networking |
| request | `req` | HTTP |
| response | `resp` | HTTP |
| buffer | `buf` | Universal |
| length | `len` | Universal |
| string | `str` | Universal |
| pointer | `ptr` | Universal |
| temporary | `tmp` | Universal |
| error | `err` | Universal |
| result | `res` | Universal |
| WebSocket | `ws` | Networking |
| session | `sess` | Web |
| correlation | `corr` | Distributed |

## Words That Must NOT Be Abbreviated

Always spell out completely:
- `handler`, `manager`, `server`, `client`
- `function`, `parameter`, `shutdown`, `payload`
- `protocol`, `openai`, `httpd`

## Special Conventions

**Raw pointers into buffers** use `_ptr` suffix:
```c
bool *visible_ptr;         // Raw pointer to external storage
const char **text_ptr;     // Raw pointer to external string pointer
```

**Global variables** use `g_` prefix:
```c
extern volatile sig_atomic_t g_httpd_shutdown;
```

**Internal static symbols** don't need `ik_` prefix.

## External Library Wrappers

**DO NOT use `ik_` prefix** - these are link seams for testing.

**Library wrappers** (talloc, yyjson) use **trailing underscore**:
```c
talloc_zero_(ctx, size)           // wraps talloc_zero_size()
yyjson_read_file_(path, flg, ...)  // wraps yyjson_read_file()
```

**POSIX wrappers** use **`posix_` prefix + trailing underscore**:
```c
posix_open_(pathname, flags)      // wraps open()
posix_write_(fd, buf, count)      // wraps write()
```

---

**Complete reference:** See `project/naming.md` for full details, rationale, and examples.
