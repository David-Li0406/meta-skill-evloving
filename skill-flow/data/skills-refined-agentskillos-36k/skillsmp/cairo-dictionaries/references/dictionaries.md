# Cairo Dictionaries Reference

Source: https://www.starknet.io/cairo-book/ch03-02-dictionaries.html

## Core traits and types
- Use `Felt252Dict<T>` for key-value storage where keys are `felt252`.
- Import `dict::Felt252DictTrait` for methods.

## Creating a dictionary
- `let mut dict: Felt252Dict<u128> = Default::default();`

## Basic operations
- `insert(key, value)` writes a value for a key.
- `get(key)` reads a value; if the key has never been inserted, it returns the default value for `T`.

## Entry API
- `entry(key)` returns `(Felt252DictEntry<T>, T)` where `T` is the current value.
- Update using the entry, then call `finalize(entry)` to write back and recover the dictionary.
- The entry API is useful for read-modify-write patterns.

## How dictionaries work (squashing)
- Dictionaries are implemented as lists of entries: `(key, prev_value, new_value)`.
- Each `get` or `insert` scans the list to find the latest entry, so worst-case lookup is O(n).
- At destruction, Cairo runs a "squash" step that validates the sequence of updates per key.
- Types that contain dictionaries cannot derive `Drop` because they must use `Destruct` to squash.
