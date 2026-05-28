# Cairo Variables and Mutability Reference

Source: https://www.starknet.io/cairo-book/ch02-01-variables-and-mutability.html

## Core rules
- Cairo uses an immutable memory model, so variables are immutable by default.
- Reassigning an immutable binding is a compile-time error.
- `let mut x = ...` enables reassignment. Mutation is syntactic sugar over rebinding, but the type cannot change.

## Constants
- Declare with `const NAME: Type = value;`.
- `const` is always immutable; `mut` is not allowed.
- Must include a type annotation and a constant expression.
- Can be declared only in global scope.
- Naming convention: ALL_CAPS_WITH_UNDERSCORES.
- Can use any data type, including structs, enums, and fixed-size arrays.

## Shadowing
- Shadow by re-declaring with `let` using the same name.
- Shadowing creates a new variable and can change the type.
- Shadowing is scope-based; inner shadowing ends when the scope ends.
- Use shadowing when you want to transform or change type while keeping the same name.

## Mutability vs. shadowing
- `mut` allows value changes, but the type stays fixed.
- Shadowing allows both value and type changes.
