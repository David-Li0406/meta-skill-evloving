# Cairo Operator Overloading Reference

Source: https://www.starknet.io/cairo-book/ch12-03-operator-overloading.html

## Core idea
- Operator overloading is done by implementing traits from `core::ops`.
- Example: `impl PotionAdd of Add<Potion> { fn add(lhs: Potion, rhs: Potion) -> Potion { ... } }`.

## Guidance
- Use operator overloading only when the operator meaning is clear for your type.
