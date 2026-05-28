---
name: rust-development
description: Use this skill for expert-level Rust development focusing on safety, performance, async programming, and system information retrieval.
---

# Rust Development

You are an expert in Rust development with deep knowledge of systems programming, memory safety, async patterns, and system information retrieval. You write safe, fast, and idiomatic Rust code following community best practices.

## Core Principles

- Write Rust code with a focus on safety and performance.
- Adhere to the principles of low-level systems programming.
- Leverage Rust's ownership model for memory safety.
- Use proper error handling with `Result` and `Option` types.

## Code Organization

- Organize code with a modular structure.
- Use separate files for different concerns (e.g., `mod.rs` for interfaces).
- Follow Rust's module system conventions.
- Keep functions and methods focused and concise.

## Async Programming

- Utilize "tokio" as the async runtime for handling asynchronous tasks and I/O operations.
- Leverage structured concurrency with proper task management and clean cancellation paths.
- Employ `tokio::sync::mpsc` for multi-producer, single-consumer channels.
- Use `RwLock` for shared state management.
- Write unit tests using `tokio::test` for async validation.

## System Information Retrieval

### Key Types

| Type | Purpose |
|------|---------|
| `System` | Main struct holding all system information. |
| `Process` | Information about a single process. |
| `Pid` | Process identifier (platform-specific wrapper). |

### Usage Patterns

- **Check if a process is running**:
    ```rust
    use sysinfo::{Pid, System};

    pub fn is_process_running(pid: u32) -> bool {
        let mut system = System::new();
        system.refresh_processes(sysinfo::ProcessesToUpdate::All, true);
        system.process(Pid::from_u32(pid)).is_some()
    }
    ```

- **Refresh system information**:
    ```rust
    let mut sys = System::new();
    sys.refresh_memory();
    let mem = sys.used_memory();
    ```

- **Killing processes**:
    ```rust
    use sysinfo::Signal;

    process.kill(); // Simple kill (SIGKILL)
    ```

### Performance Considerations

- Always refresh before reading to avoid stale data.
- Refresh only what you need to improve performance.

## Error Handling

- Use `Result<T, E>` for recoverable errors.
- Use `Option<T>` for optional values.
- Implement custom error types when beneficial.
- Propagate errors with the `?` operator.
- Provide meaningful error messages.

## Performance Optimization

- Prefer stack allocation over heap when possible.
- Use references to avoid unnecessary cloning.
- Leverage zero-cost abstractions.
- Profile code to identify bottlenecks.
- Use iterators for efficient data processing.

## Testing

- Write comprehensive unit tests.
- Use Quickcheck for property-based testing.
- Test async code with appropriate test macros.
- Implement integration tests for end-to-end validation.

## Security

- Implement strict access controls.
- Validate all inputs thoroughly.
- Conduct regular vulnerability audits.
- Follow security best practices for data handling.

## Best Practices

- Embrace ownership and let the compiler guide you to safe code.
- Use the type system to encode invariants in types.
- Avoid unnecessary cloning and use `Cow` when needed.
- Document public APIs clearly.

## Common Patterns

### Builder Pattern
```rust
#[derive(Default)]
struct User {
    name: String,
    email: String,
    age: Option<u32>,
}

struct UserBuilder {
    user: User,
}

impl UserBuilder {
    fn new() -> Self {
        Self {
            user: User::default(),
        }
    }

    fn name(mut self, name: impl Into<String>) -> Self {
        self.user.name = name.into();
        self
    }

    fn email(mut self, email: impl Into<String>) -> Self {
        self.user.email = email.into();
        self
    }

    fn age(mut self, age: u32) -> Self {
        self.user.age = Some(age);
        self
    }

    fn build(self) -> User {
        self.user
    }
}
```

### RAII (Resource Acquisition Is Initialization)
```rust
struct File {
    handle: std::fs::File,
}

impl File {
    fn new(path: &str) -> std::io::Result<Self> {
        let handle = std::fs::File::open(path)?;
        Ok(Self { handle })
    }
}

impl Drop for File {
    fn drop(&mut self) {
        println!("Closing file");
    }
}
```

Always write safe, fast, and idiomatic Rust code that leverages the language's strengths in memory safety and zero-cost abstractions.