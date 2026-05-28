# Cairo Generics and Traits Reference

Source: https://www.starknet.io/cairo-book/ch08-00-generic-types-and-traits.html

## Core Ideas
- Generics are placeholders for concrete types and reduce code duplication.
- The compiler monomorphizes generics: it generates a concrete implementation for each type used.
- Monomorphization can increase compiled code size, which can matter for Starknet contracts.

## Traits and Bounds
- Traits define shared behavior across types.
- Combine traits with generics to constrain which types are accepted by a function or struct.
- Use `+TraitName<T>` syntax to specify trait bounds (the `+` is required).

## Required Trait Bounds

When writing generic implementations, Cairo needs to know how to handle values of the generic type. Common required bounds:

| Bound | When Required |
|-------|---------------|
| `+Drop<T>` | When values of type T might be dropped (most cases) |
| `+Copy<T>` | When values need to be copied (field access, multiple uses) |
| `+Destruct<T>` | For types that need explicit destruction |

## Implementation Syntax

### Generic Struct with Derives
```cairo
#[derive(Drop, Copy)]
struct Pair<T> {
    first: T,
    second: T,
}
```

### Generic Trait Definition
```cairo
trait Swap<T> {
    fn swap(self: Pair<T>) -> Pair<T>;
}
```

### Generic Implementation with Trait Bounds
```cairo
// Note: +Drop<T> and +Copy<T> are trait bounds
impl PairSwap<T, +Drop<T>, +Copy<T>> of Swap<T> {
    fn swap(self: Pair<T>) -> Pair<T> {
        Pair { first: self.second, second: self.first }
    }
}
```

### Alternative: Trait Generic Over the Whole Type
```cairo
trait SwapTrait<TPair> {
    fn swap(self: TPair) -> TPair;
}

impl PairSwap<T, +Drop<T>, +Copy<T>> of SwapTrait<Pair<T>> {
    fn swap(self: Pair<T>) -> Pair<T> {
        Pair { first: self.second, second: self.first }
    }
}
```

## Common Errors and Fixes

### Error: Missing Drop/Copy implementation
```
error: Trait has no implementation in context: core::traits::Drop<...>
```
**Fix**: Add `+Drop<T>` (and possibly `+Copy<T>`) to the impl signature.

### Error: Struct cannot be dropped
**Fix**: Add `#[derive(Drop)]` or `#[derive(Drop, Copy)]` to the struct definition.

## Complete Working Example

```cairo
#[derive(Drop, Copy)]
struct Pair<T> {
    first: T,
    second: T,
}

trait Swap<T> {
    fn swap(self: Pair<T>) -> Pair<T>;
}

impl PairSwap<T, +Drop<T>, +Copy<T>> of Swap<T> {
    fn swap(self: Pair<T>) -> Pair<T> {
        Pair { first: self.second, second: self.first }
    }
}

fn demo() -> Pair<u32> {
    let pair = Pair { first: 1_u32, second: 2_u32 };
    pair.swap()
}

#[cfg(test)]
mod tests {
    use super::{Pair, Swap};

    #[test]
    fn swap_pair_u32() {
        let pair = Pair { first: 10_u32, second: 20_u32 };
        let swapped = pair.swap();
        assert(swapped.first == 20_u32, 'swap first');
        assert(swapped.second == 10_u32, 'swap second');
    }
}
```
