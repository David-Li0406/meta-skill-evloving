# Acceptance Criteria Writing Guide

Acceptance criteria (AC) define testable outcomes that verify a spec is correctly implemented. Well-written AC make implementation clear and testing straightforward.

## Format: Given/When/Then

Every AC follows a three-part structure:

```yaml
given: <precondition or context>
when: <action or trigger>
then: <expected observable result>
```

### Examples

**Good AC:**
```yaml
given: a user with valid credentials
when: they submit the login form
then: they are redirected to the dashboard with a success message
```

**Avoid vague AC:**
```yaml
# Bad - not testable
given: a user
when: they log in
then: it works correctly
```

The "then" clause must describe something observable and verifiable.

## Principles

### Each AC Should Be Independently Testable

- One behavior per AC
- Avoid compound conditions ("X and Y and Z")
- A test should fail if this specific AC is broken

```yaml
# Good - separate AC for each behavior
- given: valid input
  when: command runs
  then: exits with code 0

- given: valid input
  when: command runs
  then: outputs result to stdout
```

```yaml
# Avoid - compound AC
- given: valid input
  when: command runs
  then: exits with code 0 and outputs result to stdout and logs to file
```

### Use Concrete Examples

Replace abstract descriptions with specific values:

| Vague | Concrete |
|-------|----------|
| "handles errors correctly" | "returns JSON with error field containing message" |
| "displays appropriate message" | "shows 'Task completed successfully'" |
| "processes input" | "parses YAML and returns structured object" |

### Cover Happy Path + Key Edge Cases

- Don't enumerate every possible edge case
- Focus on behaviors users care about
- **3-5 AC per spec is typical**

```yaml
# Happy path
- given: valid task reference
  when: user runs task complete
  then: task status changes to completed

# Key edge case
- given: invalid task reference
  when: user runs task complete
  then: error message shows "Task not found: @ref"

# Another edge case
- given: task already completed
  when: user runs task complete
  then: error message shows "Task is already completed"
```

## Writing Patterns

### For CLI Commands

Cover these aspects:
1. **Success case** - What happens with valid input
2. **Input validation** - What happens with invalid input
3. **Output format** - What the output looks like
4. **Exit codes** - When to use 0 vs non-zero

```yaml
- given: valid ref and message
  when: user runs "kspec task note @ref message"
  then: note is added and confirmation shown

- given: non-existent ref
  when: user runs "kspec task note @invalid message"
  then: exits with code 1 and shows "Reference not found"
```

### For Data Operations

Cover CRUD patterns:
1. **Create** - What's created and where
2. **Read** - What's returned and format
3. **Update** - What changes and what's preserved
4. **Delete** - What's removed and confirmations

```yaml
- given: parent module exists
  when: user adds feature under parent
  then: feature is created with parent reference set

- given: item has notes
  when: item is deleted
  then: confirmation required mentioning note count
```

### For Cross-Cutting Behaviors

When behavior applies to multiple specs, consider:
- Should this be a trait instead?
- Reference the trait in AC if applicable

```yaml
- given: --json flag provided
  when: command completes successfully
  then: output is valid JSON (inherits from @trait-json-output)
```

## Commands Reference

```bash
# Add AC to a spec
kspec item ac add <ref> --given "..." --when "..." --then "..."

# List AC for a spec
kspec item ac list <ref>

# Update an existing AC
kspec item ac set <ref> <ac-id> --given "..." --when "..." --then "..."

# Remove an AC
kspec item ac remove <ref> <ac-id> [--force]
```

## Validation

Use `kspec validate` to check AC quality:

```bash
kspec validate
```

The validator reports:
- Specs without any AC (warning)
- Specs with AC that lack "then" clauses
- Broken references in AC

**Best practice**: Run validation after adding or updating AC.

## Common Mistakes

### Vague AC
```yaml
# Bad
then: system behaves correctly

# Good
then: returns status code 200 with JSON body containing "success: true"
```

### Missing AC
Specs without AC are incomplete. Every feature and requirement should have at least one AC.

### Too Granular
Don't write one AC per line of code. AC describe user-visible behavior, not implementation details.

```yaml
# Too granular
- then: variable x is set to 5
- then: loop iterates 3 times
- then: function returns true

# Right level
- then: calculation returns correct total
```

### Untestable AC
If you can't write a test for it, rewrite it:

```yaml
# Untestable
then: performance is acceptable

# Testable
then: response completes within 100ms
```

## Related

- [Back to Spec Overview](../SKILL.md)
- [Item Types Reference](item-types.md) - When to use features vs requirements
- [Traits Reference](traits.md) - Reusable AC bundles
