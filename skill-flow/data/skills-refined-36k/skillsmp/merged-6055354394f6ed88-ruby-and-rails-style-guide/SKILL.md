---
name: ruby-and-rails-style-guide
description: Use this skill when writing, reviewing, or refactoring Ruby and Rails code to ensure adherence to style conventions.
---

# Ruby and Rails Style Guide

Apply these conventions when writing or modifying Ruby and Rails code.

## Ruby Guidelines

- When writing a Ruby script or CLI, always use [Thor](https://github.com/rails/thor).
- Prefer double quotes for strings; use single quotes only when the string contains double quotes, in shell commands with interpolation, or when following existing code patterns.
- Use parallel assignment for instance variables when initializing from local variables with matching names; split across two lines when assigning 3 or more.
- Indent private methods by 2 additional spaces after the `private` keyword.
- Prefer `case when` over `if elsif` for multiple conditional branches.
- Put `if` and `unless` on a separate line, except when using `return` or `raise` without arguments or with one short argument.
- Use guard clauses for early returns.
- Use safe navigation operator (`&.`) for nil checks.
- Add a blank line after multi-line block headers before the block body.
- Use multi-line, leading-dot chaining when calling more than one method in a row.
- Prefer chaining over temporary variables when it stays readable; `then` and `tap` are often helpful.
- Prefer numbered parameters (`_1`, `_2`) for small blocks; use `it` only when numbered params don't work.
- Prefer endless method definitions for simple, single-expression methods.

## Rails Guidelines

- In HAML, put Ruby expressions on their own line; avoid inline `=`.
  
### Binstubs

When running Rails executables, **always check for binstubs first**:

1. **Check for binstub**: Look for `bin/rails`, `bin/rspec`, `bin/rubocop`, etc.
2. **Use binstub if exists**: Run `bin/rails` instead of `bundle exec rails`.
3. **Fallback to bundle exec**: Only use `bundle exec` if no binstub exists.

```bash
# Good - check for binstub first
bin/rails db:migrate
bin/rspec spec/models/user_spec.rb

# Only if binstubs don't exist
bundle exec rails db:migrate
bundle exec rspec spec/models/user_spec.rb
```

**When bundle exec fails**: Inform the user that a binstub might resolve the issue, as binstubs can have different load paths or configurations.

### Namespaces

Treat each Rails app as divided into namespaces. Common ones are `web`, `admin`, and `users`.

For each namespace:
- Routes live in `config/routes/NAMESPACE.rb`
- Views live in `app/views/NAMESPACE`
- Controllers live in `app/controllers/NAMESPACE`
- Styles live in `app/assets/stylesheets/NAMESPACE.scss`
- JavaScript lives in `app/javascripts/NAMESPACE.js`
- I18n locale files live in `config/locales/NAMESPACE.LOCALE.yml`

Never create a new namespace unless the user explicitly prompts it. If you are unsure which namespace a change belongs to, ask the user.

### Setting datetime/date columns to current time

When setting a datetime or date column to the current time/date, check if the model includes `HasTimestamps[column]`. If so, use the bang method instead of direct assignment:

```ruby
# Bad - direct assignment when HasTimestamps is available
message.update!(sent_at: Time.current)

# Good - use the bang method from HasTimestamps
message.sent!
```