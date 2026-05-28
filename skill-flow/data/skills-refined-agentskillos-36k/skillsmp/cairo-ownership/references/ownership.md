# Cairo Ownership Reference

Source: https://www.starknet.io/cairo-book/ch04-01-what-is-ownership.html

## Ownership rules
- Each variable has an owner.
- There can only be one owner at a time.
- When the owner goes out of scope, the value is destroyed.

## Moves and scope
- Assigning a value to another variable or passing it to a function moves ownership.
- After a move, the original variable cannot be used.
- Destruction happens automatically at end of scope or explicitly via `destruct()` if needed.

## Copy
- Types that implement `Copy` can be duplicated instead of moved.
- Most small scalar types are `Copy`; arrays and dictionaries are not.
- A struct can derive `Copy` only if all its fields are `Copy`.

## Drop and Destruct
- `Drop` indicates no special destruction logic; it can be derived for many types.
- `Destruct` runs custom logic when a value is destroyed (for example, dictionary squashing).
- Types containing dictionaries cannot derive `Drop` because they must use `Destruct`.

## Linear type system
- Cairo uses a linear type system: values must be used exactly once (moved or destroyed).
- Compile-time errors often surface as "variable not dropped" or use-after-move errors.
