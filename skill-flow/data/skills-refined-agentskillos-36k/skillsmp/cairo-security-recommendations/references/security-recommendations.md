# General Recommendations Reference

Source: https://www.starknet.io/cairo-book/ch104-01-general-recommendations.html

## Access control and upgrades
- Use clear access control for privileged functions.
- Emit events for sensitive actions like upgrades.
- Avoid unprotected upgrade entry points.

## Cairo pitfalls
- Operator precedence can be surprising (AND has higher precedence than OR).
- Unsigned underflows in loops can cause panics.
- Packing must keep values within storage constraints.

## Interoperability notes
- Token interfaces may differ in naming conventions and return values.
- Validate L1 senders in l1_handler functions.

## Operational safety
- Avoid unbounded loops and excessive storage writes to prevent DoS risks.
