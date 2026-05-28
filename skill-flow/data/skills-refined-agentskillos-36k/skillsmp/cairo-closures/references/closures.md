# Cairo Closures Reference

Source: https://book.cairo-lang.org/ch11-01-closures.html

## Basics
- Closures are anonymous functions that can capture values from their environment.
- Syntax: `let c = |x| x * 2;` with parameters between pipes.
- Bodies can be single-expression or block bodies with `{}`.
- Types are inferred from usage; add annotations when inference is ambiguous.
- Closures were introduced in Cairo 2.9 and remain under active development.

## Capturing environment
- Closures can read bindings from their enclosing scope.
- Currently, closures cannot capture mutable variables.

## Fn traits
- `FnOnce`: moves captured values out; callable once.
- `FnMut`: mutates captured values; callable multiple times with mutable access.
- `Fn`: does not move or mutate captured values; callable multiple times.

## Passing closures
- Functions accept closures via traits like `core::ops::Fn` with an associated `Output` type.
- Example in array helpers: `map` and `filter` accept closures with `Fn` bounds.
