# Cairo Modules and Scope Reference

Source: https://www.starknet.io/cairo-book/ch07-02-defining-modules-to-control-scope.html

## Module system
- Modules organize code into namespaces and control privacy.
- The crate root file is the starting point for the module tree.

## Declaring modules
- Use `mod name;` in the parent module to declare a submodule.
- The compiler looks for the module body in `name.cairo` or `name/mod.cairo`.
- Modules can also be declared inline with `mod name { ... }`.

## Privacy
- Items are private by default and are only visible to parent and sibling modules.
- Use `pub` to make modules or items public.
- Making a module `pub` does not automatically make its items public.
