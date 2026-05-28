---
name: generating-type-signatures
description: Use this skill when you need to generate or update type signatures for Ruby source files using either RBS or Sorbet.
---

# Skill body

## Instructions

When generating type signatures, always follow these steps. Copy this checklist and track your progress:

```
Type Signature Generation Progress:
- [ ] Step 1: Analyze the Ruby source
- [ ] Step 2: Generate type signatures
- [ ] Step 3: Eliminate `untyped` or `T.untyped` types in signatures
- [ ] Step 4: Review and refine signatures
- [ ] Step 5: Validate signatures
```

## Rules

- You MUST NOT run Ruby code of the project.
- You MUST NOT use `untyped` or `T.untyped`. Infer the proper type instead.
- You MUST ask the user to provide more details if something is not clear.
- You MUST prepend any command with `bundle exec` if the project has a Gemfile.

## 1. Analyze the Ruby Source

Always perform this step.

Read and understand the Ruby source file:
- Identify all classes, modules, methods, constants, and instance variables.
- Note inheritance, module inclusion, and definitions based on metaprogramming.
- Note visibility modifiers - `public`, `private`, `protected`.
- Note type parameters for generic classes.

## 2. Generate Type Signatures

### For RBS:
- Create necessary `.rbs` files for the target Ruby file.
- Place generated RBS files in the `sig/` directory mirroring the Ruby source structure.

### For Sorbet:
- Create necessary `.rbi` files for the target Ruby file.
- Place RBI files in the `./rbi` directory.

### Common Steps:
- Ensure to follow the syntax conventions for RBS or Sorbet as applicable.
- Use tracking files when processing multiple Ruby files to ensure no files are missed.

## Multi-File Processing

When processing multiple Ruby files, create a tracking file to ensure all files are covered:

1. **Create tracking file** `.generation-todo.tmp`:
   ```
   [ ] app/models/user.rb
   [ ] app/models/post.rb
   [ ] app/services/auth_service.rb
   ```

2. **Process files one by one**:
   - Take the next pending `[ ]` entry.
   - Complete all steps (1-5) for that file.
   - Mark as processed `[x]`.
   - Save the tracking file.
   - Continue to the next pending entry.

3. **Cleanup**: Remove the tracking file after all files are processed:
   ```bash
   rm .generation-todo.tmp
   ```

If interrupted, the tracking file allows resuming from where you left off.