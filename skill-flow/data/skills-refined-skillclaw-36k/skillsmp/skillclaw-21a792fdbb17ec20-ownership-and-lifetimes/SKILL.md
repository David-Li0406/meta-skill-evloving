---
name: ownership-and-lifetimes
description: Use this skill when dealing with ownership, borrowing, and lifetime issues in programming, particularly in Rust. It helps to clarify data ownership and lifetime management to resolve common compiler errors.
---

# Ownership & Lifetimes

> **Layer 1: Language Mechanics**

## Core Question

**Who should own this data, and for how long?**

Before fixing ownership errors, understand the data's role:
- Is it shared or exclusive?
- Is it short-lived or long-lived?
- Is it transformed or just read?

---

## Error → Design Question

| Error | Don't Just Say | Ask Instead |
|-------|----------------|-------------|
| E0382 | "Clone it" | Who should own this data? |
| E0597 | "Extend lifetime" | Is the scope boundary correct? |
| E0506 | "End borrow first" | Should mutation happen elsewhere? |
| E0507 | "Clone before move" | Why are we moving from a reference? |
| E0515 | "Return owned" | Should caller own the data? |
| E0716 | "Bind to variable" | Why is this temporary? |
| E0106 | "Add 'a" | What is the actual lifetime relationship? |

---

## Thinking Prompt

Before fixing an ownership error, ask:

1. **What is this data's domain role?**
   - Entity (unique identity) → owned
   - Value Object (interchangeable) → clone/copy OK
   - Temporary (computation result) → maybe restructure

2. **Is the ownership design intentional?**
   - By design → work within constraints
   - Accidental → consider redesign

3. **Fix symptom or redesign?**
   - If Strike 3 (3rd attempt) → escalate to Layer 2

---

## Trace Up ↑

When errors persist, trace to design layer:

```
E0382 (moved value)
    ↑ Ask: What design choice led to this ownership pattern?
    ↑ Check: m09-domain (is this Entity or Value Object?)
    ↑ Check: domain-* (what constraints apply?)
```

| Persistent Error | Trace To | Question |
|-----------------|----------|----------|
| E0382 repeated | m02-resource | Should use Arc/Rc for sharing? |
| E0597 repeated | m09-domain | Is scope boundary at right place? |
| E0506/E0507 | m03-mutability | Should use interior mutability? |

---

## Trace Down ↓

From design decisions to implementation:

```
"Data needs to be shared immutably"
    ↓ Use: Arc<T> (multi-thread) or Rc<T> (single-thread)

"Data needs exclusive ownership"
    ↓ Use: move semantics, take ownership

"Data is read-only view"
    ↓ Use: &T (immutable borrow)
```

---

## Quick Reference

| Pattern | Description |
|---------|-------------|
| Ownership | Determine who owns the data and its lifetime. |
| Borrowing | Understand how data can be temporarily accessed. |
| Lifetime | Ensure data lives long enough for its use. |