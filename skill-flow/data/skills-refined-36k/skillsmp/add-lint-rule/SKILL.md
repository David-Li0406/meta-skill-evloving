---
name: add-lint-rule
description: Add a new lint rule to the validator
license: MIT OR Apache-2.0
---

# Add Lint Rule

Guide for adding a new lint rule to skilo.

## Steps

1. Choose a diagnostic code (E0XX for errors, W0XX for warnings)
2. Add the code to `DiagnosticCode` enum
3. Create the rule implementation
4. Register the rule in the Validator
5. Add configuration option if needed
6. Add tests
7. Update documentation

## File Locations

| File                     | Purpose                                   |
|--------------------------|-------------------------------------------|
| `src/skill/validator.rs` | `DiagnosticCode` enum, `Validator` struct |
| `src/skill/rules/mod.rs` | Rule trait, module exports                |
| `src/skill/rules/*.rs`   | Individual rule implementations           |
| `src/config.rs`          | Configuration options                     |

## Rule Trait

```rust
pub trait Rule: Send + Sync {
    fn name(&self) -> &'static str;
    fn check(&self, manifest: &Manifest) -> Vec<Diagnostic>;
}
```

## Example Rule

```rust
pub struct MyRule;

impl Rule for MyRule {
    fn name(&self) -> &'static str {
        "my-rule"
    }

    fn check(&self, manifest: &Manifest) -> Vec<Diagnostic> {
        // Validation logic here
        Vec::new()
    }
}
```

## Configuration

For threshold-based rules, use `Threshold` type:

```rust
// In config.rs
#[serde(deserialize_with = "deserialize_threshold")]
pub my_rule: Threshold,

// In validator.rs
if let Some(max) = config.rules.my_rule.resolve(DEFAULT) {
    rules.push(Box::new(MyRule::new(max)));
}
```
