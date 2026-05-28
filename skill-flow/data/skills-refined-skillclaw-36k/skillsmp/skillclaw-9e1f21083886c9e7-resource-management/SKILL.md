---
name: resource-management
description: Use this skill when you need to choose the appropriate smart pointer for resource management in Rust, considering ownership patterns and threading contexts.
---

# Resource Management

> **Layer 1: Language Mechanics**

## Core Question

**What ownership pattern does this resource need?**

Before choosing a smart pointer, understand:
- Is ownership single or shared?
- Is access single-threaded or multi-threaded?
- Are there potential cycles?

---

## Error → Design Question

| Error | Don't Just Say | Ask Instead |
|-------|----------------|-------------|
| "Need heap allocation" | "Use Box" | Why can't this be on stack? |
| Rc memory leak | "Use Weak" | Is the cycle necessary in design? |
| RefCell panic | "Use try_borrow" | Is runtime check the right approach? |
| Arc overhead complaint | "Accept it" | Is multi-thread access actually needed? |

---

## Thinking Prompt

Before choosing a smart pointer:

1. **What's the ownership model?**
   - Single owner → Box or owned value
   - Shared ownership → Rc/Arc
   - Weak reference → Weak

2. **What's the thread context?**
   - Single-thread → Rc, Cell, RefCell
   - Multi-thread → Arc, Mutex, RwLock

3. **Are there cycles?**
   - Yes → One direction must be Weak
   - No → Regular Rc/Arc is fine

---

## Trace Up ↑

When pointer choice is unclear, trace to design:

```
"Should I use Arc or Rc?"
    ↑ Ask: Is this data shared across threads?
    ↑ Check: m07-concurrency (thread model)
    ↑ Check: domain-* (performance constraints)
```

| Situation | Trace To | Question |
|-----------|----------|----------|
| Rc vs Arc confusion | m07-concurrency | What's the concurrency model? |
| RefCell panics | m03-mutability | Is interior mutability right here? |
| Memory leaks | m12-lifecycle | Where should cleanup happen? |

---

## Trace Down ↓

From design to implementation:

```
"Need single-owner heap data"
    ↓ Use: Box<T>

"Need shared immutable data (single-thread)"
    ↓ Use: Rc<T>

"Need shared immutable data (multi-thread)"
    ↓ Use: Arc<T>

"Need to break reference cycle"
    ↓ Use: Weak<T>

"Need shared mutable data"
    ↓ Single-thread: Rc<RefCell<T>>
    ↓ Multi-thread: Arc<Mutex<T>> or Arc<RwLock<T>>
```

---

## Quick Reference

| Type | Ownership | Thread-Safe | Use When |
|------|-----------|-------------|----------|
| `Box<T>` | Single | Yes | Heap allocation, recursive types |
| `Rc<T>` | Shared | No | Shared ownership in single-threaded contexts |
| `Arc<T>` | Shared | Yes | Shared ownership in multi-threaded contexts |
| `Weak<T>` | Weak | No | To prevent reference cycles |
| `RefCell<T>` | Shared mutable | No | Interior mutability in single-threaded contexts |
| `Mutex<T>` | Shared mutable | Yes | Interior mutability in multi-threaded contexts |
| `RwLock<T>` | Shared mutable | Yes | Read-write access in multi-threaded contexts |