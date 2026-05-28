# Cairo If Let and While Let Reference

Source: https://book.cairo-lang.org/ch06-03-concise-control-flow-with-if-let-and-while-let.html

## If let
- `if let pattern = expr { ... }` is shorthand for a `match` that handles one pattern and ignores the rest.
- Use an optional `else` branch to handle the fallback case.
- Prefer `match` when you need exhaustive handling of all variants.

## While let
- `while let pattern = expr { ... }` loops as long as the pattern matches.
- Commonly used with `Option`-returning operations like popping from a collection.
