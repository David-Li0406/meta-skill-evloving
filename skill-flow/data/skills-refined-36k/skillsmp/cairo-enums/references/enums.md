# Cairo Enums Reference

Sources:
- https://www.starknet.io/cairo-book/ch06-01-enums.html

## Defining enums
- Define with `enum Name { Variant1: Type1, Variant2: Type2, ... }`.
- Variants can carry data, including tuples or structs as their payload type.
- Construct with `Name::Variant(value)` or `Name::Variant` for unit-like variants.

## Using enums
- Access variant data by pattern matching with `match` or `if let`.
- Enums can be used inside structs or other types to model choices.

## Option enum
- `Option<T>` models an optional value.
- Variants: `Option::Some(value)` and `Option::None`.
- Use pattern matching to handle both cases explicitly.
