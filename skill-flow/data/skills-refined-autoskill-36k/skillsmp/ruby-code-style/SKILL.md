---
name: ruby-code-style
description: Ruby coding conventions and style preferences for the Greenhouse codebase. Use when writing or reviewing Ruby code, writing RSpec tests, refactoring Ruby code, or setting up new Ruby files.
---

# Ruby Code Style

## Hash Syntax

Use Ruby 3 style hashes with implicit values when a variable in scope matches the key name:

- Preferred: `{ organization_id: }`
- Avoid: `{ organization_id: organization_id }`

Apply this to method arguments:

- Preferred: `create(:person, organization:)`
- Avoid: `create(:person, organization: organization)`

## Method Definitions

For one-line methods, use shorthand syntax:

```ruby
def method_name = some-operation
```

For simple blocks, use the implicit `it` variable:

```ruby
models.map { do_this_with(it) }
```

## RSpec Conventions

Prefer `subject(:variable_name) { ... }` over `let(:variable_name) { ... }` when the variable represents the primary subject being tested (typically `described_class.new`).

## Magic Comments

Order magic comments correctly:

```ruby
# frozen_string_literal: true
# typed: true
```

The `# typed: true` comment must always come AFTER `# frozen_string_literal: true`.

## Naming Conventions

Use the suffix `_RE` for regular expression constants:

- Preferred: `MAILTO_RE`
- Avoid: `MAILTO_REGEX`
