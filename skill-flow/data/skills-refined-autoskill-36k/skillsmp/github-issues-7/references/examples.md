# Issue Examples

## Good Example: Simple Task

```markdown
### Description

The metered usage processor currently looks up a product rate plan based on the product sku id and whether the product rate plan is active ([metered_usage_processor.rb#L197](https://github.com/github/meuse/blob/e510430/app/stream_processors/metered_usage_processor.rb#L197)).

We could get into a situation where that criteria matches multiple records. @RamonPage clarified that we should only have 1 active product rate plan per product sku, but there's nothing enforcing that uniqueness at the moment.

### Acceptance Criteria

Implement a Rails validation that enforces only 1 active product rate plan per product sku.
```

Why this works:
- Context and problem explained in flowing prose
- Code reference embedded as inline link
- Attribution for clarification included naturally
- Acceptance criteria is clear and concise
- No redundant sections

## Good Example: Task with Dependencies

```markdown
Depends on #661

### Description

Create the `Copilot::Policy` ActiveRecord model backed by the `copilot_policies` table. This model represents a policy definition created via stafftools.

The model needs validations for required fields and a uniqueness constraint on `config_name`. One approach would be to add a `visible_to?(entity)` method that checks the entity's plan against the policy's allowed plans.

### Acceptance Criteria

- [ ] Model created with appropriate validations
- [ ] `config_name` uniqueness enforced
- [ ] Tests cover validation and visibility logic
```

Why this works:
- Dependency stated upfront
- Implementation suggestion framed as "one approach would be"
- Acceptance criteria uses checklist for multiple items

## Good Example: Batch Issue

```markdown
### Description

Foundation work required before other Policy Studio batches can begin. Includes database migrations and renaming the existing `Copilot::Policy` module to free up the name.

### Acceptance Criteria

All sub-issues completed.
```

Why this works:
- Batch issues are intentionally brief
- Details live in the sub-issues, not repeated here
- Clear that completion means sub-issues are done

## Bad Example: Repetitive Sections

```markdown
## Summary

Add a validation to enforce uniqueness.

## Background

We need to add a validation to enforce uniqueness because currently there's no validation enforcing uniqueness.

## Scope

- Add validation for uniqueness
- Test the uniqueness validation

## Out of Scope

N/A

## Success Criteria

- [ ] Validation added
- [ ] Tests pass

## Dependencies

None

## References

- None
```

Problems:
- Same information repeated in Summary, Background, and Scope
- Empty sections with "N/A" and "None" add noise
- References section is pointless when empty
- Could be reduced to 2 sections

## Bad Example: Implementation as Requirement

```markdown
### Description

Add the validation.

### Acceptance Criteria

- [ ] Add `validates :product_sku_id, uniqueness: { scope: :active, conditions: -> { where(active: true) } }` to ProductRatePlan model
- [ ] Add migration to add unique index on (product_sku_id, active) where active = true
- [ ] Add test in `test/models/product_rate_plan_test.rb` lines 45-60
```

Problems:
- Description lacks context (why?)
- Implementation details are overly specific
- Developer has no flexibility in approach
- Specific line numbers will become stale

Better:
```markdown
### Description

The metered usage processor assumes only one active product rate plan exists per product sku, but nothing enforces this. We should add a validation to prevent duplicates.

### Acceptance Criteria

Enforce that only one product rate plan can be active per product sku. Consider a database-level constraint for data integrity.
```
