---
name: cosmos-patterns
description: Cosmos SDK module development patterns and conventions for Celestia
---

# Cosmos SDK Patterns

Reference guide for Cosmos SDK module development patterns used in Celestia.

## When to Use

- When creating new Cosmos SDK modules
- When reviewing code for pattern compliance
- When onboarding new team members
- As reference during implementation

## Quick Reference

### Module Structure
See [module-structure.md](./references/module-structure.md) for standard layout.

### Proto Conventions
See [proto-conventions.md](./references/proto-conventions.md) for protobuf patterns.

### Keeper Patterns
See [keeper-patterns.md](./references/keeper-patterns.md) for keeper implementation.

## Essential Principles

### 1. Proto First
Always design proto definitions before implementing Go code. The proto defines the API contract.

### 2. Typed Events
Always use `EmitTypedEvent` instead of legacy `EmitEvent`. This ensures type safety and better tooling support.

### 3. Expected Keepers
Define keeper interfaces in `types/expected_keepers.go` to decouple modules and enable testing.

### 4. CamelCase Tests
Use CamelCase for test function names (no underscores): `TestBurnSuccess` not `TestBurn_Success`.

### 5. Godoc Everything
Add godoc comments to all exported types, functions, and packages.

## Common Commands

```bash
# Generate proto files
make proto-gen

# Run tests
go test ./x/[module]/...

# Run linter
golangci-lint run ./x/[module]/...

# Build
go build ./...
```

## References

- [Module Structure](./references/module-structure.md)
- [Proto Conventions](./references/proto-conventions.md)
- [Keeper Patterns](./references/keeper-patterns.md)
