# Cairo Structs Reference

Source: https://www.starknet.io/cairo-book/ch05-01-defining-and-instantiating-structs.html

## Defining structs
- Define with `struct Name { field: Type, ... }`.
- Field order is not significant in initialization.

## Instantiating and accessing
- Create with `let s = Name { field1: value1, field2: value2 };`.
- Access fields with dot syntax: `s.field1`.
- To mutate fields, the entire instance must be declared `mut`.

## Field init shorthand
- When variables match field names, use `Name { field1, field2 }`.

## Struct update syntax
- Use `Name { field1: new_value, ..other }` to reuse remaining fields.
- The update syntax moves fields from `other`; the original cannot be used if non-Copy fields were moved.
- If the moved fields are `Copy`, the original remains usable.
