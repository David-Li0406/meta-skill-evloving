---
name: generating-type-signatures
description: Use this skill when generating or updating type signatures for Ruby source files, either in RBS or Sorbet formats.
---

# Type Signature Generation Skill

Generate or update type signatures for Ruby source files in either RBS or Sorbet formats. This skill supports both full generation from scratch and partial updates for individual changed files.

## Instructions

When generating type signatures, always follow these steps.

Copy this checklist and track your progress:

```
Type Signature Generation Progress:
- [ ] Step 1: Analyze the Ruby source
- [ ] Step 2: Generate type signatures
- [ ] Step 3: Eliminate untyped types in signatures
- [ ] Step 4: Review and refine signatures
- [ ] Step 5: Validate signatures
```

## Rules

- You MUST NOT run Ruby code of the project.
- You MUST NOT use untyped types (e.g., `untyped` or `T.untyped`). Infer the proper type instead.
- You MUST ask the user to provide more details if something is not clear.
- You MUST prepend any command with `bundle exec` if the project has a Gemfile.
- You MUST use a tracking file when processing multiple files to ensure no files are missed.

## Multi-File Processing

When processing multiple Ruby files, create a tracking file to ensure all files are covered:

1. **Create tracking file** (e.g., `.type-signature-generation-todo.tmp`):
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

3. **Cleanup**: Remove the tracking file after all files are processed:
   ```bash
   rm .type-signature-generation-todo.tmp
   ```

If interrupted, the tracking file allows resuming from where you left off.

## 1. Analyze the Ruby Source

Always perform this step.

Read and understand the Ruby source file:
- Identify all classes, modules, methods, constants, and instance variables.
- Note inheritance, module inclusion, and definitions based on metaprogramming.
- Note visibility modifiers - `public`, `private`, `protected`.
- Note type parameters for generic classes.

## 2. Generate Type Signatures

### For RBS

- Create necessary `.rbs` files for the target Ruby file.
- Place generated RBS files in the `sig/` directory mirroring Ruby source structure.
- Follow RBS syntax conventions to describe types for all declarations.

### For Sorbet

- Create necessary `.rbi` files for the target Ruby file.
- Place generated RBI files in the `./rbi` directory.
- Use `sig { }` block syntax for method signatures and add `extend T::Sig` to classes/modules.

## 3. Eliminate Untyped Types in Signatures

Always perform this step.

- Review all signatures and replace untyped types with proper types.
- Use code context, method calls, and tests to infer types.
- Use untyped only as a last resort when the type cannot be determined.

## 4. Review and Refine Signatures

Always perform this step.

- Verify signatures are correct, coherent, and complete.
- Remove unnecessary untyped types.
- Ensure all methods and attributes have signatures.
- Fix any errors and repeat until signatures are correct.

## 5. Validate Signatures

### For RBS

Run `rbs validate` to verify that existing and new `.rbs` files are internally consistent.

### For Sorbet

Run Sorbet type checker to validate signatures:

```bash
srb tc
```

Or with bundle:

```bash
bundle exec srb tc
```

Fix any errors reported and repeat until validation passes.

# References

- [syntax.md](reference/syntax.md) - The full list of RBS and Sorbet types and syntax
- [rbs_by_example.md](reference/rbs_by_example.md) - Short list of RBS signatures examples
- [Sorbet RBI documentation](https://sorbet.org/docs/rbi) - Official RBI docs
- [data_and_struct.md](https://github.com/ruby/rbs/blob/master/docs/data_and_struct.md) - Explanation on Data and Struct types handling