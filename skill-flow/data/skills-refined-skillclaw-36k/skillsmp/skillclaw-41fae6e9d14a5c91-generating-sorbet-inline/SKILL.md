---
name: generating-sorbet-inline
description: Use this skill when you need to generate or update Sorbet inline type signatures directly in Ruby source files using `sig` blocks.
---

# Sorbet Inline Generation Skill

Generate or update Sorbet type signatures using `sig {}` blocks directly in Ruby source files. Sorbet signatures are valid Ruby code that enable both static and runtime type checking.

## Instructions

When generating Sorbet inline signatures, always follow these steps.

Copy this checklist and track your progress:

```
Sorbet Inline Generation Progress:
- [ ] Step 1: Analyze the Ruby source
- [ ] Step 2: Add Sorbet signatures
- [ ] Step 3: Eliminate `T.untyped` in signatures
- [ ] Step 4: Review and refine signatures
- [ ] Step 5: Validate signatures with Sorbet
```

## Rules

- You MUST NOT run Ruby code of the project.
- You MUST NOT use `T.untyped`. Infer the proper type instead.
- You MUST NOT use `T.unsafe` - it bypasses type checking entirely.
- You MUST NOT use `T.cast` - it forces types without verification.
- You MUST ask the user to provide more details if something is not clear.
- You MUST prepend any command with `bundle exec` if the project has a Gemfile.
- You MUST use `sig { }` block syntax for method signatures.
- You MUST add `extend T::Sig` to classes/modules before using `sig`.
- You MUST focus on method signatures only. Skip local variables, intermediate expressions, and other non-method annotations.
- You MUST NOT use or generate `.rbi` files. This skill is for inline signatures only.
- You MUST preserve the existing `# typed:` sigil level if one exists. Do not upgrade or change strictness without explicit user consent.

## Multi-File Processing

When processing multiple Ruby files, create a tracking file to ensure all files are covered:

1. **Create tracking file** `.sorbet-inline-generation-todo.tmp`:
   ```
   [ ] app/models/user.rb
   [ ] app/models/post.rb
   [ ] app/services/auth_service.rb
   ```

2. **Process files one by one**:
   - Take the next pending `[ ]` entry
   - Complete all steps (1-5) for that file
   - Mark as processed `[x]`
   - Save the tracking file
   - Continue to the next pending entry

3. **Cleanup**: Remove the tracking file after all files are processed.

## Additional Analysis

When analyzing the Ruby source, ensure to:
- Identify all classes, modules, methods, constants, and instance variables.
- Note inheritance, module inclusion, and definitions based on metaprogramming.
- Note visibility modifiers - `public`, `private`, `protected`.
- Note existing `# typed:` sigil level at the top of the file.
- Note type parameters for generic classes.