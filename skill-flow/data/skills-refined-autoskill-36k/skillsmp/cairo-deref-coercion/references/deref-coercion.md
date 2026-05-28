# Cairo Deref Coercion Reference

Source: https://www.starknet.io/cairo-book/ch12-09-deref-coercion.html

## Deref and DerefMut
- `Deref` and `DerefMut` enable implicit coercion to a target type.
- `Deref` trait:
  - `type Target`
  - `fn deref(self: T) -> Self::Target`
- `DerefMut` trait:
  - `type Target`
  - `fn deref_mut(ref self: T) -> Self::Target`

## Behavior
- Coercion allows accessing members of the target type directly on the wrapper.
- `DerefMut` applies only to mutable variables; it does not grant mutable access by itself.
