---
name: rust-skill-creator
description: Use this skill when creating skills for Rust crates or standard library documentation.
---

# Rust Skill Creator

> Create dynamic skills for Rust crates and std library documentation.

## When to Use

This skill handles requests to create skills for:
- Third-party crates (e.g., tokio, serde, axum)
- Rust standard library (e.g., std::sync, std::marker)
- Any Rust documentation URL

## Workflow

### 1. Identify the Target

| User Request | Target Type | URL Pattern |
|--------------|-------------|-------------|
| "create tokio skill" | Third-party crate | `docs.rs/tokio/latest/tokio/` |
| "create Send trait skill" | Std library | `doc.rust-lang.org/std/marker/trait.Send.html` |
| "create skill from URL" + URL | Custom URL | User-provided URL |

### 2. Execute the Command

Use the `/create-llms-for-skills` command:

```
/create-llms-for-skills <url> [requirements]
```

**Examples:**

```bash
# For third-party crate
/create-llms-for-skills https://docs.rs/tokio/latest/tokio/

# For std library
/create-llms-for-skills https://doc.rust-lang.org/std/marker/trait.Send.html

# With specific requirements
/create-llms-for-skills https://docs.rs/axum/latest/axum/ "Focus on routing and extractors"
```

### 3. Follow-up with Skill Creation

After `llms.txt` is generated, use:

```
/create-skills-via-llms <crate_name> <llms_path> [version]
```

## URL Construction Helper

| Target | URL Template |
|--------|--------------|
| Crate overview | `https://docs.rs/{crate}/latest/{crate}/` |
| Crate module | `https://docs.rs/{crate}/latest/{crate}/{module}/` |
| Std trait | `https://doc.rust-lang.org/std/{module}/trait.{Name}.html` |
| Std struct | `https://doc.rust-lang.org/std/{module}/struct.{Name}.html` |
| Std module | `https://doc.rust-lang.org/std/{module}/index.html` |

## Common Std Library Paths

| Item | Path |
|------|------|
| Send, Sync, Copy, Clone | `std/marker/trait.{Name}.html` |
| Arc, Mutex, RwLock | `std/sync/struct.{Name}.html` |
| Rc, Weak | `std/rc/struct.{Name}.html` |
| RefCell, Cell | `std/cell/struct.{Name}.html` |
| Box | `std/boxed/struct.Box.html` |
| Vec | `std/vec/struct.Vec.html` |
| String | `std/string/struct.String.html` |
| Option | `std/option/enum.Option.html` |