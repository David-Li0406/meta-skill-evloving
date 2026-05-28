# Traits Reference

Traits are reusable bundles of acceptance criteria for cross-cutting concerns. When a spec implements a trait, it inherits all of the trait's AC as additional requirements.

## What Are Traits?

Traits solve a common problem: multiple specs need the same behavior. Instead of duplicating AC across specs, define the behavior once as a trait and apply it where needed.

**Example use cases**:
- JSON output mode (many commands support `--json`)
- Confirmation prompts (destructive operations need `--force`)
- Pagination/filtering (list commands share filtering behavior)
- Error message format (consistent error structure)

**How inheritance works**:
```
Trait: @json-output
  AC: --json flag outputs valid JSON
  AC: JSON contains all displayed data
  AC: No ANSI codes in JSON mode

Spec: @my-command (implements @json-output)
  Own AC: specific behavior for this command
  Inherited AC: all 3 AC from @json-output
```

When you run `kspec item get @my-command`, you see both the spec's own AC and inherited trait AC.

## Discovering Traits

Every kspec project can define its own traits. Discover what's available:

```bash
# List all traits with AC counts
kspec trait list

# Get details on a specific trait
kspec trait get @trait-name
```

Example output:
```
$ kspec trait list
@trait-json-output     (6 AC) JSON Output Mode
@trait-confirmation    (4 AC) Confirmation Prompt
@trait-filterable      (7 AC) Filterable List Commands
```

## Applying Traits to Specs

### Add a Trait

```bash
kspec item trait add <spec-ref> <trait-ref>
```

Example:
```bash
# Add JSON output trait to a command spec
kspec item trait add @my-export-command @trait-json-output
```

This is idempotent - adding the same trait twice has no effect.

### Remove a Trait

```bash
kspec item trait remove <spec-ref> <trait-ref>
```

### View Applied Traits

```bash
kspec item get <spec-ref>
```

The output shows the `traits` array listing all applied traits.

## Creating New Traits

Create traits when you identify patterns shared by multiple specs.

### When to Create a Trait

- Same AC applies to **3 or more specs**
- Behavior is **cross-cutting** (not specific to one feature)
- You want to **enforce consistency** across implementations

### How to Create

```bash
# 1. Create the trait
kspec trait add "Trait Name" --description "What this trait ensures" --slug my-trait

# 2. Add acceptance criteria to the trait
kspec item ac add @my-trait --given "..." --when "..." --then "..."
kspec item ac add @my-trait --given "..." --when "..." --then "..."

# 3. Apply to relevant specs
kspec item trait add @spec-1 @my-trait
kspec item trait add @spec-2 @my-trait
kspec item trait add @spec-3 @my-trait
```

### Trait Design Guidelines

1. **Name clearly** - The trait name should convey what behavior it ensures
2. **Document purpose** - Use description to explain when to apply it
3. **Keep focused** - One trait = one cohesive behavior pattern
4. **Make AC generic** - AC should apply to any spec implementing the trait

## When to Use Traits

| Situation | Use Trait? |
|-----------|-----------|
| Same flags across multiple commands | Yes |
| Similar output format across commands | Yes |
| One-off command behavior | No |
| Feature-specific requirement | No |
| Cross-module consistency need | Yes |

### Decision Guide

```
Does this behavior apply to 3+ specs?
  No → Don't create a trait, just add AC to each spec
  Yes ↓

Is the behavior truly identical across specs?
  No → Each spec needs its own AC
  Yes ↓

Will you want to change this behavior uniformly?
  No → Maybe not worth the abstraction
  Yes → Create a trait
```

## Trait vs Spec AC

Understanding the difference:

| Trait AC | Spec AC |
|----------|---------|
| Inherited by all specs with the trait | Specific to one spec |
| Changed in one place, affects all | Changed per-spec |
| Cross-cutting concerns | Feature-specific behavior |
| Generic (applies to any implementer) | Concrete (applies to this spec) |

A spec can have both:
- **Trait AC** (inherited): Ensures standard behaviors
- **Spec AC** (own): Defines unique functionality

## Validation

`kspec validate` checks trait usage:

```bash
kspec validate
```

Reports:
- Traits with no AC (warning)
- Broken trait references
- Specs referencing non-existent traits

## Example Workflow

```bash
# 1. Notice pattern: several commands need --dry-run support
kspec trait add "Dry Run Preview" --description "Commands support --dry-run to preview changes" --slug dry-run

# 2. Define the expected behavior
kspec item ac add @dry-run --given "--dry-run flag provided" --when "command runs" --then "changes are shown but not applied"
kspec item ac add @dry-run --given "--dry-run flag provided" --when "command runs" --then "output clearly indicates preview mode"

# 3. Apply to relevant commands
kspec item trait add @task-delete @dry-run
kspec item trait add @item-delete @dry-run
kspec item trait add @inbox-clear @dry-run

# 4. Verify
kspec trait get @dry-run  # Shows trait and which specs use it
```

## Related

- [Back to Spec Overview](../SKILL.md)
- [Acceptance Criteria Guide](acceptance-criteria.md) - Writing AC for traits
- [Item Types Reference](item-types.md) - Trait as an item type
