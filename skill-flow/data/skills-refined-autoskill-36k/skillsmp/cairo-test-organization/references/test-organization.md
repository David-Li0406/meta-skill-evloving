# Cairo Test Organization Reference

Source: https://book.cairo-lang.org/ch10-02-test-organization.html

## Unit tests
- Live in `src` files inside `#[cfg(test)] mod tests`.
- Can test private functions because child modules can access ancestors.

## Integration tests
- Live in a top-level `tests/` directory.
- Each file is compiled as its own crate; import the library with `use <package_name>::...`.
- Files in `tests/` do not need `#[cfg(test)]`.

## Sharing helpers
- Because each file is a separate crate, helper modules are not shared by default.
- Create `tests/lib.cairo` and declare `mod` files to make `tests/` a single crate for shared helpers.
