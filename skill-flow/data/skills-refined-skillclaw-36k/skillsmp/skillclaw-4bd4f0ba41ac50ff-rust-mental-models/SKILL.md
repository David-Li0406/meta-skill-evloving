---
name: rust-mental-models
description: Use this skill when learning or explaining Rust concepts, particularly around ownership, borrowing, and memory management.
---

# Mental Models

> **Layer 2: Design Choices**

## Core Question

**What's the right way to think about this Rust concept?**

When learning or explaining Rust:
- What's the correct mental model?
- What misconceptions should be avoided?
- What analogies help understanding?

---

## Key Mental Models

| Concept | Mental Model | Analogy |
|---------|--------------|---------|
| Ownership | Unique key | Only one person has the house key |
| Move | Key handover | Giving away your key |
| `&T` | Lending for reading | Lending a book |
| `&mut T` | Exclusive editing | Only you can edit the document |
| Lifetime `'a` | Valid scope | "Ticket valid until..." |
| `Box<T>` | Heap pointer | Remote control to TV |
| `Rc<T>` | Shared ownership | Multiple remotes, last turns off |
| `Arc<T>` | Thread-safe Rc | Remotes from any room |

---

## Coming From Other Languages

| From | Key Shift |
|------|-----------|
| Java/C# | Values are owned, not references by default |
| C/C++ | Compiler enforces safety rules |
| Python/Go | No GC, deterministic destruction |
| Functional | Mutability is safe via ownership |
| JavaScript | No null, use Option instead |

---

## Thinking Prompt

When confused about Rust:

1. **What's the ownership model?**
   - Who owns this data?
   - How long does it live?
   - Who can access it?

2. **What guarantee is Rust providing?**
   - No data races
   - No dangling pointers
   - No use-after-free

3. **What's the compiler telling me?**
   - Error = violation of safety rule
   - Solution = work with the rules

---

## Trace Up ↑

To design understanding (Layer 2):

```
"Why can't I do X in Rust?"
    ↑ Ask: What safety guarantee would be violated?
    ↑ Check: m01-m07 for the rule being enforced
    ↑ Ask: What's the intended design pattern?
```

---

## Trace Down ↓

To implementation (Layer 1):

```
"I understand the concept, now how do I implement?"
    ↓ m01-ownership: Ownership patterns
    ↓ m02-resource: Smart pointer choice
    ↓ m07-concurrency: Thread safety
```

---

## Common Misconceptions

| Error | Wrong Model | Correct Model |
|-------|-------------|---------------|
| Example Error | Example Wrong Model | Example Correct Model |