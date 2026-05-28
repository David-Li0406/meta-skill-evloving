# Cairo References and Snapshots Reference

Source: https://www.starknet.io/cairo-book/ch04-02-references-and-snapshots.html

## Snapshots
- A snapshot (`@T`) is an immutable view of a value at a moment in time.
- Create a snapshot with the `@` operator, for example `let s = @value;`.
- A snapshot can be passed without moving ownership of the original value.
- Accessing fields of a snapshot yields snapshots of those fields.
- Use the desnap operator `*snapshot` to obtain a value when the inner type is `Copy`.
- Snapshots always implement `Drop` and never implement `Destruct`.

## References (`ref`)
- Use `ref` parameters to allow a function to mutate a value and return it implicitly.
- The argument passed to a `ref` parameter must be declared `mut`.
- `ref` parameters are passed by value and returned to the caller at the end of the call.

## Passing patterns
- Pass by value when ownership transfer is desired.
- Pass by snapshot (`@T`) for read-only access without moving ownership.
- Pass by `ref` for in-place mutation while keeping ownership in the caller.

## Boxes
- Use `Box<T>` to move large values efficiently; it gives heap ownership and cheap moves.
