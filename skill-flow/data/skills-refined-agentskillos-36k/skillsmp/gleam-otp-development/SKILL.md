---
name: gleam-otp-development
description: Guides Claude through building concurrent, fault-tolerant applications with Gleam OTP. Use when creating actors, supervision trees, or building distributed BEAM applications.
---

# Gleam OTP Development Skill

This skill guides Claude Code through building concurrent, fault-tolerant applications with Gleam OTP.

## Primary Sources

1. **[Gleam OTP Documentation](https://hexdocs.pm/gleam_otp/)** - Complete OTP reference
2. **[Gleam OTP GitHub Examples](https://github.com/gleam-lang/otp)** - Official examples
3. **[Gleam OTP: Using Supervisors](https://vpgleam.substack.com/p/gleam-otp-using-supervisors)** - Supervisor tutorial
4. **[Gleam OTP Design Principals](https://github.com/wmealing/gleam-otp-design-principals)** - Design patterns
5. **[Actor Documentation](https://hexdocs.pm/gleam_otp/gleam/otp/actor.html)** - Actor API reference
6. **[Supervisor Documentation](https://hexdocs.pm/gleam_otp/gleam/otp/supervisor.html)** - Supervisor API reference

## Quick Reference

### Core Modules
- `gleam/otp/actor` - Actor processes with type-safe messaging
- `gleam/otp/supervisor` - Supervision trees
- `gleam/otp/static_supervisor` - Static supervision configuration
- `gleam/otp/task` - One-off concurrent tasks
- `gleam/erlang/process` - Low-level process operations

See: [Gleam OTP Modules](https://hexdocs.pm/gleam_otp/)

## Common Workflows

### Creating a New OTP Application

```bash
gleam new my_otp_app
cd my_otp_app
gleam add gleam_otp gleam_erlang
```

### Basic Actor Pattern

Consult the actor documentation for:
- Creating actors: [Actor - start](https://hexdocs.pm/gleam_otp/gleam/otp/actor.html#start)
- Message handling: [Actor - Next](https://hexdocs.pm/gleam_otp/gleam/otp/actor.html#Next)
- Calling actors: [Actor - call](https://hexdocs.pm/gleam_otp/gleam/otp/actor.html#call)

### Supervision Tree Setup

For supervision patterns, see:
- [Supervisor - start](https://hexdocs.pm/gleam_otp/gleam/otp/supervisor.html#start)
- [Supervisor - add](https://hexdocs.pm/gleam_otp/gleam/otp/supervisor.html#add)
- [Supervisor - worker](https://hexdocs.pm/gleam_otp/gleam/otp/supervisor.html#worker)

Example structure:
```
Application Supervisor
├── Database Pool Supervisor
│   ├── Connection 1
│   ├── Connection 2
│   └── Connection N
├── Web Server Supervisor
│   ├── HTTP Listener
│   └── Request Handlers
└── Background Job Supervisor
    └── Worker Pool
```

See: [Gleam OTP: Using Supervisors](https://vpgleam.substack.com/p/gleam-otp-using-supervisors)

### One-Off Tasks

For concurrent one-off operations:
[Task Module](https://hexdocs.pm/gleam_otp/gleam/otp/task.html)

Alternative with more features:
[Taskle Library](https://hexdocs.pm/taskle/)

## Design Patterns

### GenServer-Style Actor

```gleam
// State, Message types, start function, handle function
```

See complete examples: [Actor Examples](https://hexdocs.pm/gleam_otp/gleam/otp/actor.html)

### Worker Pool

For worker pool implementation patterns:
[Gleam OTP Design Principals](https://github.com/wmealing/gleam-otp-design-principals)

### Event Manager

For pub/sub patterns, consult:
- [Process - send](https://hexdocs.pm/gleam_erlang/gleam/erlang/process.html#send)
- Custom event manager implementations

### Registry Pattern

For process registration and discovery:
[Process - register](https://hexdocs.pm/gleam_erlang/gleam/erlang/process.html)

## Supervision Strategies

Choose the right restart strategy:

### OneForOne
Restart only the failed child.
Use for: Independent workers

### OneForAll
Restart all children if one fails.
Use for: Tightly coupled processes

### RestForOne
Restart failed child and all started after it.
Use for: Dependent process chains

See: [Supervisor Strategies](https://hexdocs.pm/gleam_otp/gleam/otp/supervisor.html)

## Testing OTP Applications

### Testing Actors

```gleam
import gleam/otp/actor

pub fn actor_test() {
  let assert Ok(actor.Started(subject, _)) = start_my_actor()
  let result = actor.call(subject, waiting: 100, sending: fn(s) { MyMessage(s) })
  let assert expected = result
}
```

### Testing Supervisors

Test supervision behavior:
- Child starts correctly
- Child restarts on crash
- Supervisor respects max restart limits

See: [Testing Guide](../../rules/testing-practices.md)

## Monitoring and Debugging

### Erlang Observer

Monitor your OTP application:
```bash
iex -S mix  # For Elixir projects
erl  # For Erlang projects
```

Then: `:observer.start()`

### Process Monitoring

Use process monitoring functions:
[Process - monitor](https://hexdocs.pm/gleam_erlang/gleam/erlang/process.html)

### Logging

Integrate logging:
[Palabres - OTP Logging](https://hexdocs.pm/palabres/)

## Common Anti-Patterns

Refer to: [OTP Anti-Patterns](../../rules/otp-patterns.md)

Key anti-patterns to avoid:
- Processes as state (use variables instead)
- Unsupervised processes
- Large messages between processes
- Using processes for code organization

## Libraries for OTP Development

### Core
- **[gleam_otp](https://hexdocs.pm/gleam_otp/)** - OTP framework
- **[gleam_erlang](https://hexdocs.pm/gleam_erlang/)** - Erlang runtime

### Extended
- **[taskle](https://hexdocs.pm/taskle/)** - Elixir-like Task functionality
- **[glixir](https://hexdocs.pm/glixir/)** - Safe Gleam-Elixir OTP interop

### Utilities
- **[palabres](https://hexdocs.pm/palabres/)** - Logging for OTP apps

## Hot Code Reloading

Gleam supports Erlang's hot code reloading, but type safety isn't guaranteed during upgrades.

See: [Gleam FAQ - Hot Code Reloading](https://gleam.run/frequently-asked-questions/)

## Deployment Considerations

### Release Building

Use Gleam's Erlang release functionality:
```bash
gleam export erlang-shipment
```

See: [Deploying to Fly.io](https://gleam.run/deployment/fly/)

### Configuration

Use environment variables:
[Envoy Library](https://hexdocs.pm/envoy/)

### Clustering

For distributed Erlang clusters, consult:
- [Gleam Erlang - Node](https://hexdocs.pm/gleam_erlang/)
- Erlang distribution documentation

## Example Applications

Find complete OTP application examples:
- [Gleam OTP Examples](https://github.com/gleam-lang/otp/tree/main/examples)
- Community projects using OTP

## When to Use OTP

✅ Use OTP when you need:
- Long-running stateful services
- Fault tolerance and automatic restarts
- Concurrent independent operations
- Process isolation

❌ Don't use OTP for:
- Simple pure computations
- Organizing code (use modules)
- Holding simple state (use variables)

See: [OTP Patterns](../../rules/otp-patterns.md)

---

**Remember**: OTP is powerful but has specific use cases. Consult official documentation for current patterns and best practices.
