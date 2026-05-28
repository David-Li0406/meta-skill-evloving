# Cairo Match Reference

Source: https://www.starknet.io/cairo-book/ch06-02-the-match-control-flow-construct.html

## Basics
- `match` compares a value against a set of patterns and runs the first matching arm.
- Match arms are written as `pattern => expression`.
- Match is an expression; all arms must return the same type when the result is used.
- Matches must be exhaustive; use `_` as a catch-all when appropriate.

## Enum matching
- Match enum variants with fully qualified names like `EnumName::Variant`.
- Bind variant data in the pattern, for example `Option::Some(x)`.
- `match` is the primary way to access data carried by variants.

## Common patterns
- Use `match` to handle `Option` values safely (`Some` vs `None`).
- Use `_` to ignore values you do not care about.
