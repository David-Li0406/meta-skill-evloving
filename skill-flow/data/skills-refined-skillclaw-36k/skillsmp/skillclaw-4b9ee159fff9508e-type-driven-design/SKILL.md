---
name: type-driven-design
description: Use this skill when you want to leverage the type system to prevent invalid states and ensure compile-time validation in your designs.
---

# Type-Driven Design

> **Layer 1: Language Mechanics**

## Core Question

**How can the type system prevent invalid states?**

Before reaching for runtime checks:
- Can the compiler catch this error?
- Can invalid states be unrepresentable?
- Can the type encode the invariant?

---

## Error → Design Question

| Pattern | Don't Just Say | Ask Instead |
|---------|----------------|-------------|
| Primitive obsession | "It's just a string" | What does this value represent? |
| Boolean flags | "Add an is_valid flag" | Can states be types? |
| Optional everywhere | "Check for None" | Is absence really possible? |
| Validation at runtime | "Return Err if invalid" | Can we validate at construction? |

---

## Thinking Prompt

Before adding runtime validation:

1. **Can the type encode the constraint?**
   - Numeric range → bounded types or newtypes
   - Valid states → type state pattern
   - Semantic meaning → newtype

2. **When is validation possible?**
   - At construction → validated newtype
   - At state transition → type state
   - Only at runtime → Result with clear error

3. **Who needs to know the invariant?**
   - Compiler → type-level encoding
   - API users → clear type signatures
   - Runtime only → documentation

---

## Trace Up ↑

When type design is unclear:

```
"Need to validate email format"
    ↑ Ask: Is this a domain value object?
    ↑ Check: m09-domain (Email as Value Object)
    ↑ Check: domain-* (validation requirements)
```

| Situation | Trace To | Question |
|-----------|----------|----------|
| What types to create | m09-domain | What's the domain model? |
| State machine design | m09-domain | What are valid transitions? |
| Marker trait usage | m04-zero-cost | Static or dynamic dispatch? |

---

## Trace Down ↓

From design to implementation:

```
"Need type-safe wrapper for primitives"
    ↓ Newtype: struct UserId(u64);

"Need compile-time state validation"
    ↓ Type State: Connection<Connected>

"Need to track phantom type parameters"
    ↓ PhantomData: PhantomData<T>

"Need capability markers"
    ↓ Marker Trait: trait Validated {}

"Need gradual construction"
    ↓ Builder: Builder::new().field(x).build()
```

---

## Quick Reference

| Pattern | Purpose | Example |
|---------|---------|---------|
| Newtype | Encapsulate a primitive type | `struct UserId(u64);` |
| Type State | Represent valid states | `Connection<Connected>` |
| PhantomData | Track type parameters | `PhantomData<T>` |
| Marker Trait | Indicate capabilities | `trait Validated {}` |
| Builder Pattern | Gradual construction | `Builder::new().field(x).build()` |