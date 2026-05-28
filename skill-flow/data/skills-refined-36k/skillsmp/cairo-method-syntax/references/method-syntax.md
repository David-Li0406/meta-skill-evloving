# Cairo Method Syntax Reference

Source: https://www.starknet.io/cairo-book/ch05-03-method-syntax.html

## Defining methods
- Methods are defined in traits and implemented in `impl` blocks.
- The first parameter is `self`, `@self`, or `ref self`.
- Use `#[generate_trait]` on an `impl` block to auto-generate the trait definition.

## Choosing the `self` form
- `self` moves ownership into the method.
- `@self` borrows immutably using a snapshot.
- `ref self` borrows mutably and returns ownership to the caller.

## Associated functions
- Functions without a `self` parameter are associated functions.
- Use associated functions for constructors and helpers (for example, `square`).
- Call with `TraitName::function(...)` or `TypeName::function(...)` when in scope.

## Example patterns
- `fn area(self: @Rectangle) -> u64` for read-only methods.
- `fn can_hold(self: @Rectangle, other: @Rectangle) -> bool` for comparisons.
- `fn square(size: u64) -> Rectangle` as a constructor.
