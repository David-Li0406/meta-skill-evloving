# Cairo Associated Items Reference

Source: https://www.starknet.io/cairo-book/ch12-10-associated-items.html

## Kinds of associated items
- Associated functions (including methods)
- Associated types
- Associated constants
- Associated implementations

## Associated types
- Declared in traits as placeholders (e.g., `type Result;`).
- Implementations choose the concrete type.
- Methods can return `Self::Result` without extra generic parameters.

## When to use
- Use associated types to keep trait signatures simpler than adding extra generic type parameters.
