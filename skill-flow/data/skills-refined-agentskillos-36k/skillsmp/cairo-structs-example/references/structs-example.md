# Cairo Structs Example Reference

Source: https://www.starknet.io/cairo-book/ch05-02-an-example-program-using-structs.html

## Progression of the example
- Start with separate `width` and `height` variables.
- Move to a tuple `(width, height)` to group values.
- Refactor to a `Rectangle` struct to name fields and improve readability.

## Rectangle example
- Define `struct Rectangle { width: u64, height: u64 }`.
- Implement an `area(rect: Rectangle) -> u64` function using `rect.width * rect.height`.
- Use field access to avoid positional confusion present in tuples.

## Conversions with traits
- Implement `Into<T>` to define infallible conversions; call with `.into()`.
- The target type for `.into()` must be known from context or annotated.
- Implement `TryInto<T>` for fallible conversions; it returns `Option<T>` in the book example.
- Example: convert a `Square` to a `Rectangle` only when dimensions are valid.
