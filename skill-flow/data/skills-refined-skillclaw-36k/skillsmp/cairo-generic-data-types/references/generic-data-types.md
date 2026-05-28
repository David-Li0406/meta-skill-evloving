# Cairo Generic Data Types Reference

Source: https://book.cairo-lang.org/ch08-01-generic-data-types.html

## Where generics apply
- Generics can be used in functions, structs, enums, traits, implementations, and methods.

## Syntax
- Generic parameters go in angle brackets after the item name.
- Examples:
  - `struct Point<T> { x: T, y: T }`
  - `struct Pair<T, U> { left: T, right: U }`
  - `enum Option<T> { Some: T, None: () }`
  - `fn identity<T>(value: T) -> T { value }`

## Notes
- Generics improve reuse and reduce duplication, but each concrete type still gets its own compiled implementation.
