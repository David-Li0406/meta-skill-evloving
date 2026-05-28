# Library Calls Reference

Source: https://www.starknet.io/cairo-book/ch102-03-executing-code-from-another-class.html

## Library calls
- Library calls execute another class's code in the caller's storage context.
- Use a LibraryDispatcher with a class hash for ergonomic calls.

## Low-level syscall
- `library_call_syscall` takes a class hash, selector, and serialized calldata.
- Use `Serde` to serialize inputs and deserialize outputs.
