---
name: code-quality
description: Code quality and safety standards. Activates when editing or reviewing code. Use for quality priorities, safety checks, and code correctness verification.
allowed-tools: ["shell", "read_file", "apply_patch"]
metadata:
  short-description: Enforce code quality and safety
---

# Code Quality

**Read these references:**
- `references/quality.md` - Quality priorities (correctness, safety, performance)
- `references/safety.md` - Runtime and security safety guidelines

## Instructions

Apply all guidance from references when writing or reviewing code.

### Quality Priority Order

Per `quality.md`:
1. **Correctness** - Does it work? Handle all cases?
2. **Safety** - Runtime safety (no crashes, race conditions)
3. **Security** - No vulnerabilities, input validation
4. **Performance** - Efficient use of resources
5. **Maintainability** - Clear, consistent, documented

### Safety Checks

Per `safety.md`:
- **Runtime safety**: nil checks, bounds checking, race conditions
- **Error handling**: All errors checked and handled appropriately
- **Resource management**: Proper cleanup, no leaks
- **Input validation**: Sanitize and validate all external input
- **Thread safety**: Mutex usage, data races, concurrent access

### Language-Specific Guidance

For Go projects, also reference:
- `~/.config/agent/domain/coding/go/style.md`
- `~/.config/agent/domain/coding/go/idioms.md`
- `~/.config/agent/domain/coding/go/concurrency.md`
- `~/.config/agent/domain/coding/go/safety.md`

For other languages, check `~/.config/agent/domain/coding/<language>/` if available.

### All Steps Blocking

Quality and safety checks are **blocking** - code must pass all requirements before proceeding. Never compromise on correctness or safety for speed.
