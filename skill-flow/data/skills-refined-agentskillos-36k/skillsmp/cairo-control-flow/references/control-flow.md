# Cairo Control Flow Reference

Source: https://www.starknet.io/cairo-book/ch02-05-control-flow.html

## `if` expressions
- `if` is an expression in Cairo.
- Conditions must be `bool`; there is no implicit truthiness for integers.
- `else if` and `else` are supported.
- When used in `let` bindings, both branches must return the same type.

## `loop`
- `loop` repeats indefinitely until `break`.
- Use `continue` to skip to the next iteration.
- `break value;` returns a value from the loop; the loop's type is the type of the break value.

## `while`
- `while` repeats as long as its boolean condition is `true`.
- Prefer `for` loops for iteration when possible, instead of manual indexing.

## `for`
- Iterates over ranges or other iterators.
- Example range syntax: `for n in 1..4_u8 { ... }`.

## Loops and recursion
- The book notes that loops and recursion are conceptually equivalent and compile down to similar low-level representations.
