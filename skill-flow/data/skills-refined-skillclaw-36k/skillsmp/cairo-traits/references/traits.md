# Cairo Traits Reference

Source: https://book.cairo-lang.org/ch08-02-traits-in-cairo.html

## Defining traits
- Traits group method signatures that define shared behavior.
- Traits can be generic: `pub trait Summary<T> { fn summarize(self: @T) -> ByteArray; }`.

## Implementing traits
- Implement with `impl ImplName of Trait<Type> { ... }`.
- Example: `impl NewsArticleSummary of Summary<NewsArticle> { ... }`.
- The trait must be in scope for its methods to be callable.

## Default implementations
- Trait methods can include a body to provide a default implementation.
- Implementors can keep defaults or override them.

## Bounds and advanced features
- Bounds use `+Trait<T>` or `impl Name: Trait<T>` in generic parameter lists.
- Impl aliases can expose specific concrete implementations: `pub impl U8Two = one_based::TwoImpl<u8>;`.
- Negative impls are experimental and require `experimental-features = ["negative_impls"]` in `Scarb.toml`.
