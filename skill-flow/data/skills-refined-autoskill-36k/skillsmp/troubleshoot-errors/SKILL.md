---
name: troubleshoot-errors
description: Diagnose common LikeC4 errors (element not found, unknown kinds, invalid relationships). Provides causes and solutions.
---

# Troubleshoot LikeC4 Errors

Use this skill when resolving common LikeC4 syntax or reference errors.

## Common Issues

### "Element not found"
- **Cause:** Using short name instead of FQN
- **Solution:** Use `mySystem.api` not `api` for nested elements

### "Unknown element kind"
- **Cause:** Invalid or generic element kind
- **Solution:** Check `projects/shared/spec-*.c4` for valid kinds; use specific kinds like `Container_Api` not `Container`

### "Invalid relationship kind"
- **Cause:** Undefined relationship type
- **Solution:** Use defined kinds: `calls`, `async`, `reads`, `writes`, `uses` (model) or `http`, `https`, `tcp` (deployment)

### Diagram shows unexpected elements
- **Cause:** Over-broad wildcard includes like `include **`
- **Solution:** Use scoped wildcards: `include mySystem.*` or `include mySystem.* ->`

### "instanceOf target not found"
- **Cause:** Referencing non-existent or wrong element type
- **Solution:** Ensure target is a Container from model, use FQN: `instanceOf mySystem.api`
