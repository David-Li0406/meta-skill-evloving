---
name: zero-cost-abstraction
description: Use this skill when deciding between generics and trait objects in Rust to achieve zero-cost abstractions while considering performance and type constraints.
---

# Zero-Cost Abstraction

> **Layer 1: Language Mechanics**

## Core Question

**Do we need compile-time or runtime polymorphism?**

Before choosing between generics and trait objects:
- Is the type known at compile time?
- Is a heterogeneous collection needed?
- What's the performance priority?

---

## Error → Design Question

| Error | Don't Just Say | Ask Instead |
|-------|----------------|-------------|
| E0277 | "Add trait bound" | Is this abstraction at the right level? |
| E0308 | "Fix the type" | Should types be unified or distinct? |
| E0599 | "Import the trait" | Is the trait the right abstraction? |
| E0038 | "Make object-safe" | Do we really need dynamic dispatch? |

---

## Thinking Prompt

Before adding trait bounds:

1. **What abstraction is needed?**
   - Same behavior, different types → trait
   - Different behavior, same type → enum
   - No abstraction needed → concrete type

2. **When is type known?**
   - Compile time → generics (static dispatch)
   - Runtime → trait objects (dynamic dispatch)

3. **What's the trade-off priority?**
   - Performance → generics
   - Compile time → trait objects
   - Flexibility → depends

---

## Trace Up ↑

When type system fights back:

```
E0277 (trait bound not satisfied)
    ↑ Ask: Is the abstraction level correct?
    ↑ Check: m09-domain (what behavior is being abstracted?)
    ↑ Check: m05-type-driven (should use newtype?)
```

| Persistent Error | Trace To | Question |
|-----------------|----------|----------|
| Complex trait bounds | m09-domain | Is the abstraction right? |
| Object safety issues | m05-type-driven | Can typestate help? |
| Type explosion | m10-performance | Accept dyn overhead? |

---

## Trace Down ↓

From design to implementation:

```
"Need to abstract over types with same behavior"
    ↓ Types known at compile time → impl Trait or generics
    ↓ Types determined at runtime → dyn Trait

"Need collection of different types"
    ↓ Closed set → enum
    ↓ Open set → Vec<Box<dyn Trait>>

"Need to return different types"
    ↓ Same type → impl Trait
    ↓ Different types → Box<dyn Trait>
```

---

## Quick Reference

| Pattern | Dispatch | Code Size | Runtime Cost |
|---------|----------|-----------|--------------|
| ...     | ...      | ...       | ...          |