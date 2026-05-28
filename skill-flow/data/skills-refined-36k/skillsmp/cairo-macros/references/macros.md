# Cairo Macros Reference

Source: https://www.starknet.io/cairo-book/ch12-05-macros.html

## Macro vs function
- Macros expand at compile time and can generate code.
- Macros accept variable numbers of arguments and can implement traits.
- Macro definitions are more complex and must be in scope before use.

## Declarative macros
- Define with `macro name { (pattern) => { expansion }; ... }`.
- Patterns match code structure, not runtime values.
- Example repetition: `$($x:expr), *` and expansion `$(...)*`.

## Hygiene
- `$defsite::` resolves at macro definition site.
- `$callsite::` resolves at macro invocation site.
- `expose!` can surface variables to the callsite.
