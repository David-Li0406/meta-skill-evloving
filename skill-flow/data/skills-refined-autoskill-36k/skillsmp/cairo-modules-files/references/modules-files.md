# Cairo Modules in Files Reference

Source: https://www.starknet.io/cairo-book/ch07-05-separating-modules-into-different-files.html

## File layout
- `mod name;` declares a module in the parent file.
- The compiler loads the module body from `name.cairo` or `name/mod.cairo`.

## Submodules
- Declare submodules inside the parent module file with `mod submodule;`.
- Place submodule files at `name/submodule.cairo`.

## Loading rules
- `mod` declarations load modules into the crate; `use` only brings names into scope.
- Each module is declared once in the module tree.
