# Cairo Use Keyword Reference

Source: https://www.starknet.io/cairo-book/ch07-04-bringing-paths-into-scope-with-the-use-keyword.html

## Basics
- `use` brings a path into scope for the current module only.
- Use absolute or relative paths inside `use` statements.

## Idioms
- For functions, import the parent module and call with the function name.
- For types, structs, or enums, import the full item path.

## Aliases and grouping
- Use `as` to rename imports when there are conflicts.
- Use braces to bring multiple items into scope: `use foo::{bar, baz};`.

## Re-exporting
- Use `pub use` to re-export an item from a different module.
