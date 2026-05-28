# Cairo Functions Reference

Source: https://www.starknet.io/cairo-book/ch02-03-functions.html

## Function definitions
- Syntax: `fn name(param: Type, ...) { ... }`.
- Use snake_case names.
- Functions can be defined in any order.
- Parameters must include type annotations.

## Calling functions
- Positional calls: `add(2, 3)`.
- Named arguments: `add(x: 2, y: 3)`.
- Shorthand for matching names: `add(:x, :y)` when variables are named `x` and `y`.

## Statements vs expressions
- Statements end with `;` and do not return a value.
- Expressions produce a value.
- A function body is a sequence of statements with an optional final expression.

## Return values
- Specify a return type with `-> Type`.
- Use a tail expression without `;` to return a value.
- Adding `;` to the tail expression makes it a statement, which yields `()`.
- You can also use `return value;` for early returns.

## Const functions
- Declare with `const fn` to make a function usable in constant contexts.
- The compiler can evaluate `const fn` at compile time when used in constant expressions.
- Bodies are restricted to operations allowed in constant evaluation (such as arithmetic and calls to other const functions).
