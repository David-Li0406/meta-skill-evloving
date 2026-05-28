---
name: generating-rbs-inline
description: Use this skill when you need to generate or update RBS-inline type annotations directly in Ruby source files as comments.
---

# RBS-Inline Generation Skill

Generate or update RBS-inline type annotations as comments directly in Ruby source files. This skill supports both full generation from scratch and partial updates for individual changed files. Unlike pure RBS which uses separate `.rbs` files, rbs-inline embeds type information as structured comments within Ruby code.

## Instructions

When generating RBS-inline annotations, always follow these steps.

Copy this checklist and track your progress:

```
RBS-Inline Generation Progress:
- [ ] Step 1: Analyze the Ruby source
- [ ] Step 2: Add RBS-inline annotations
- [ ] Step 3: Eliminate `untyped` types in annotations
- [ ] Step 4: Review and refine annotations
- [ ] Step 5: Validate annotations
- [ ] Step 6: Ensure type safety (only if steep is configured)
```

## Rules

- You MUST NOT run Ruby code of the project.
- You MUST NOT use `untyped`. Infer the proper type instead.
- You MUST ask the user to provide more details if something is not clear.
- You MUST prepend any command with `bundle exec` if the project has a Gemfile.
- You MUST use `# @rbs` comment syntax for inline annotations.
- You MUST NOT use regular RBS signatures and `.rbs` files in the project.

## Multi-File Processing

When processing multiple Ruby files, create a tracking file to ensure all files are covered:

1. **Create tracking file** `.rbs-inline-generation-todo.tmp`:
   ```
   [ ] app/models/user.rb
   [ ] app/models/post.rb
   [ ] app/services/auth_service.rb
   ```

2. **Process files one by one**:
   - Take the next pending `[ ]` entry
   - Complete all steps (1-6) for that file
   - Mark as processed `[x]`
   - Save the tracking file
   - Continue to the next pending entry

3. **Cleanup**: Remove the tracking file after all files are processed:
   ```bash
   rm .rbs-inline-generation-todo.tmp
   ```

If interrupted, the tracking file allows resuming from where you left off.

## 1. Analyze the Ruby Source

Always perform this step.

Read and understand the Ruby source file:
- Identify all classes, modules, methods, constants, and instance variables.
- Note inheritance, module inclusion, and definitions based on metaprogramming.
- Note visibility modifiers - `public`, `private`, `protected`.
- Note type parameters for generic classes.

## 2. Add RBS-Inline Annotations

Always perform this step.

1. First, add the magic comment at the top of the Ruby file to enable rbs-inline processing:
    ```ruby
    # rbs_inline: enabled
    ```

2. Then add type annotations as comments directly in the Ruby source file using rbs-inline syntax:

**Example - Before:**
```ruby
class User
  attr_reader :name, :age

  def initialize(name, age)
    @name = name
    @age = age
  end

  def greet(greeting)
    "#{greeting}, #{@name}!"
  end
end
```

**Example - After:**
```ruby
# rbs_inline: enabled

class User
  attr_reader :name #: String
  attr_reader :age #: Integer

  # @rbs name: String
  # @rbs age: Integer
  # @rbs return: void
  def initialize(name, age)
    @name = name
    @age = age
  end
end
```