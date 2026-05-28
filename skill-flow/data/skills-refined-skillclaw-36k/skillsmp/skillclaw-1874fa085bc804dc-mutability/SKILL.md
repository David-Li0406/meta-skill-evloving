---
name: mutability
description: Use this skill when dealing with mutability issues in Rust, particularly when encountering borrow conflicts or deciding on the appropriate mutability patterns.
---

# Mutability

> **Layer 1: Language Mechanics**

## Core Question

**Why does this data need to change, and who can change it?**

Before adding interior mutability, consider:
- Is mutation essential or just adding accidental complexity?
- Who should control mutation?
- Is the mutation pattern safe?

---

## Error → Design Question

| Error | Don't Just Say | Ask Instead |
|-------|----------------|-------------|
| E0596 | "Add mut" | Should this really be mutable? |
| E0499 | "Split borrows" | Is the data structure right? |
| E0502 | "Separate scopes" | Why do we need both borrows? |
| RefCell panic | "Use try_borrow" | Is runtime check appropriate? |

---

## Thinking Prompt

Before adding mutability:

1. **Is mutation necessary?**
   - Consider transforming the data to return a new value.
   - Alternatively, use a builder pattern to construct immutably.

2. **Who controls mutation?**
   - External caller → `&mut T`
   - Internal logic → interior mutability
   - Concurrent access → synchronized mutability

3. **What's the thread context?**
   - Single-thread → Cell/RefCell
   - Multi-thread → Mutex/RwLock/Atomic

---

## Trace Up ↑

When mutability conflicts persist:

```
E0499/E0502 (borrow conflicts)
    ↑ Ask: Is the data structure designed correctly?
    ↑ Check: m09-domain (should data be split?)
    ↑ Check: m07-concurrency (is async involved?)
```

| Persistent Error | Trace To | Question |
|-----------------|----------|----------|
| Repeated borrow conflicts | m09-domain | Should data be restructured? |
| RefCell in async | m07-concurrency | Is Send/Sync needed? |
| Mutex deadlocks | m07-concurrency | Is the lock design right? |

---

## Trace Down ↓

From design to implementation:

```
"Need mutable access from &self"
    ↓ T: Copy → Cell<T>
    ↓ T: !Copy → RefCell<T>

"Need thread-safe mutation"
    ↓ Simple counters → AtomicXxx
    ↓ Complex data → Mutex<T> or RwLock<T>

"Need shared mutable state"
    ↓ Single-thread: Rc<RefCell<T>>
    ↓ Multi-thread: Arc<Mutex<T>>
```

---

## Borrow Rules

```
At any time, you can have EITHER:
├─ Multiple &T (immutable borrows)
└─ OR one &mut T (mutable borrow)

Never both simultaneously.
```

## Quick Reference

| Pattern | Thread-Safe | Runtime Cost | Use When |
|---------|-------------|--------------|----------|