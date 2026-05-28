---
name: debugging
description: Systematic debugging of code to find root causes, fix bugs, and prevent regressions. Use whenever an error, bug, or unexpected behavior appears.
---

# Debugging Skill

When debugging code, follow this strict process:

## Debugging Checklist

1. **Understand the bug**
   - What is the expected behavior?
   - What actually happens?
   - Is the bug reproducible?

2. **Locate the source**
   - Identify the exact file, function, or component
   - Check recent changes related to the issue

3. **Analyze the cause**
   - Logic errors
   - State issues
   - Async / timing problems
   - Edge cases or missing validations

4. **Fix with minimal change**
   - Do not refactor unless necessary
   - Keep the fix scoped and safe

5. **Prevent regression**
   - Add or update tests if applicable
   - Mention similar areas that could break

## How to respond

- Explain the root cause clearly
- Show the exact code change needed
- Warn if the issue can appear again elsewhere
- Prefer simple and predictable fixes
