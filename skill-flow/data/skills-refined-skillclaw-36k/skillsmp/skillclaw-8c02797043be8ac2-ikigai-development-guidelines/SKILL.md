---
name: ikigai-development-guidelines
description: Use this skill when you need to understand the coding standards and source code structure for the Ikigai project.
---

# Ikigai Development Guidelines

## Overview

This document provides a comprehensive reference for the coding standards and source code organization for the Ikigai project, covering both the structure of the source code and the style conventions to follow during development.

## Source Code Structure

### Core Infrastructure

- `src/main.c`: Main entry point for the REPL application, loads configuration and initializes the event loop.
- `src/shared.c`: Shared context initialization for terminal, rendering, database, and history.
- `src/panic.c`: Panic handler for unrecoverable errors with safe async-signal-safe cleanup.
- `src/error.c`: Error handling wrapper using talloc-based allocator for consistent memory management.
- `src/config.c`: Configuration file loading and parsing with tilde expansion and default config creation.
- `src/credentials.c`: API key management with environment variable and JSON file (~/.ikigai/credentials.json) support.
- `src/logger.c`: Thread-safe logging system with ISO 8601 timestamps and local timezone support.
- `src/uuid.c`: UUID generation using base64url encoding for compact agent identifiers.

### Memory Management

- `src/array.c`: Generic expandable array implementation with configurable element size and growth strategy.
- `src/byte_array.c`: Typed wrapper for byte (uint8_t) arrays built on top of the generic array.
- `src/line_array.c`: Typed wrapper for line (char*) arrays built on top of the generic array.
- `src/json_allocator.c`: Talloc-based allocator for yyjson providing consistent memory management.

### Terminal Management

- `src/terminal.c`: Raw mode and alternate screen buffer management with CSI u support detection.
- `src/signal_handler.c`: Signal handling infrastructure for SIGWINCH (terminal resize) events.
- `src/ansi.c`: ANSI escape sequence parsing and color code generation utilities.

### Rendering System

- `src/render.c`: Direct ANSI terminal rendering with text and cursor positioning.
- `src/render_cursor.c`: Cursor screen position calculation accounting for UTF-8 widths and line wrapping.
- `src/layer.c`: Output buffer management for composable rendering layers.
- `src/layer_scrollback.c`: Scrollback layer wrapper that renders conversation history.
- `src/layer_input.c`: Input buffer layer wrapper that renders the current user input.
- `src/layer_separator.c`: Separator layer wrapper that renders horizontal separators with debug info and navigation context.
- `src/layer_spinner.c`: Spinner layer wrapper for animated loading indicators with frame cycling.

## Code Style Conventions

### Comments

- Use `//` style only (never `/* ... */`).
- Comment why, not what.
- Use comments sparingly.

### Numeric Types

- Always use `<inttypes.h>` for numeric types and format specifiers.
- Never use primitive types (`int`, `long`, etc.); use explicit sized types: `int8_t`, `int16_t`, `int32_t`, `int64_t`, `uint8_t`, etc.
- Use `size_t` for sizes and counts.
- Use `PRId32`, `PRIu64`, etc. for printf format specifiers.
- Use `SCNd32`, `SCNu64`, etc. for scanf format specifiers.

Example:
```c
#include <inttypes.h>

int32_t count = 42;
uint64_t size = 1024;
printf("Count: %" PRId32 ", Size: %" PRIu64 "\n", count, size);
```

### Include Order

Follow Google C++ style guide for `#include` ordering:

1. Own header first (e.g., `config.h` in `config.c`) - catches missing dependencies.
2. Project headers (`"header.h"`) - alphabetically sorted.
3. System/library headers (`<header.h>`) - alphabetically sorted.

Example:
```c
#include "config.h"           // Own header

#include "json_allocator.h"   // Project headers (alphabetical)
#include "logger.h"
#include "panic.h"
#include "wrapper.h"

#include <errno.h>            // System headers (alphabetical)
#include <stdlib.h>
#include <string.h>
```

### Avoid Static Functions

Do not use `static` helper functions in implementation files. Instead, inline the code directly.

**Why:** LCOV exclusion markers (`LCOV_EXCL_BR_LINE`) on PANIC/assert calls inside static functions are not reliably honored, breaking 90% branch coverage requirements.

**Exception:** MOCKABLE wrapper functions (see `wrapper.h`) - these use static functions by design for the mocking interface.

**Instead of:**
```c
static yyjson_mut_val *build_param(yyjson_mut_doc *doc, const char *desc)
{
    yyjson_mut_val *p = yyjson_mut_obj(doc);
    if (p == NULL) PANIC("Out of memory"); // LCOV_EXCL_BR_LINE - NOT HONORED!
    return p;
}
```

**Do:**
```c
// Inline the code at each call site
yyjson_mut_val *p = yyjson_mut_obj(doc);
if (p == NULL) PANIC("Out of memory"); // LCOV_EXCL_BR_LINE - works
```

### Test Code Style

Always add a blank line between `END_TEST` and `START_TEST`.