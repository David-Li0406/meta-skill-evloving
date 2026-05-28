# Cairo Module Paths Reference

Source: https://www.starknet.io/cairo-book/ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html

## Path types
- Absolute paths start at the crate root (often written with `crate::`).
- Relative paths start from the current module.

## Keywords
- `crate::` refers to the crate root.
- `super::` refers to the parent module.

## Visibility
- Every module and item in the path must be visible (public) to the caller.
- Making a module `pub` does not automatically make its items public.
