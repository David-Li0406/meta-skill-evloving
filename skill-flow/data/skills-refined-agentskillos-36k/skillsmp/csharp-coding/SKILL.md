---
name: csharp-coding
description: C# 14 and .NET 10 coding patterns, idioms, and conventions
---

# C# Coding Skill

Patterns and idioms for writing modern C# code.

This skill covers C# 14 language features, .NET 10 conventions, and idiomatic C# development. Load
this skill before writing or modifying C# code.

## Required Language Features

- File-scoped namespaces: `namespace MyApp.Core;`
- Primary constructors: `class Service(IDep dep, ILogger logger)`
- Collection expressions (MANDATORY): `[]`, `[item]`, `[..spread]`
  - NEVER use `new[]`, `new List<T>()`, `Array.Empty<T>()`
  - For type inference, prefer `[new T { }, new T { }]` over casts
  - Use `T[] x = [...]` only when simpler forms fail
- Records for DTOs, `init` setters
- Pattern matching: `is not null`, switch expressions
- Spread operator for collections: `[..first, ..second]`

## C# 14 Features (.NET 10)

- `field` keyword: `public string Name { get; set => field = value ?? throw; } = "";`
- Extension blocks: `extension(T src) { public bool IsEmpty => !src.Any(); }` (properties + statics)
- Null-conditional assignment: `obj?.Prop = value;` (RHS evaluated only if obj not null)
- Lambda modifiers without types: `(text, out result) => int.TryParse(text, out result)`

Migration: Use new syntax for new code; opportunistically refactor existing code when revisiting.

## Required Idioms

### Visibility

- Use `internal` for implementation classes (CLI apps, service implementations)
- Use `public` only for genuine external APIs
- Concrete classes implementing public interfaces should be `internal`

### Data Modeling

- Records for data models
- Favor immutability where reasonable
- Use immutable collections: `IReadOnlyCollection`, `IReadOnlyDictionary`

### JSON Serialization

- System.Text.Json: Use `JsonSerializerOptions` for convention/style settings applied uniformly
- Reserve attributes (`[JsonPropertyName]`, etc.) for special cases only
- Check for existing options configuration before creating new instances

### UsedImplicitly Attribute

Mark runtime-used members (deserialization, reflection, DI):

- `[UsedImplicitly]` - type instantiated implicitly (DI, empty marker records)
- `[UsedImplicitly(ImplicitUseKindFlags.Assign)]` - properties set via deserialization
- `[UsedImplicitly(..., ImplicitUseTargetFlags.WithMembers)]` - applies to type AND all members
- Common for DTOs: `[UsedImplicitly(ImplicitUseKindFlags.Assign,
  ImplicitUseTargetFlags.WithMembers)]`

### Warning Suppression

- NEVER use `#pragma warning disable`
- Use `[SuppressMessage]` with `Justification` on class/method level
- Prefer class-level when multiple members need same suppression

### LINQ

- LINQ method chaining over loops
- LINQ method syntax only; NEVER use query syntax (from/where/select keywords)

### Method Calls

- Named arguments for boolean literals: `new Options(SendInfo: false, SendEmpty: true)`
- Named arguments for consecutive same-type parameters to clarify intent

### Async

- `ValueTask` for hot paths
- `CancellationToken` everywhere (use `ct` for variable name)

### Interfaces

- Avoid interface pollution: not every service class must have an interface
- Add interfaces when justified (testability, more than one implementation)

### Local Functions

- Local functions go after `return`/`continue` statements
- Add explicit `return;` or `continue;` if needed to separate main logic from local function defs

## Design Principles

### Quality Gates

- Zero warnings/analysis issues - treat warnings as errors
- All code must pass static analysis before commit

### Abstraction

- Prefer polymorphism over enums when modeling behavior or extensibility
- Propose enum vs polymorphism tradeoffs for discussion rather than defaulting to enums
- Every abstraction must justify its existence with concrete current needs

### Dependency Injection

- MUST use DI for all dependencies; NEVER manually `new` service objects in production code
- Concrete implementations get injected; tests can substitute
- Search existing registrations before adding new ones

## Comment Guidelines

Comments must earn their place by reducing cognitive load. When to comment:

- LINQ chains (3+ operations): Brief comment stating transformation goal
- Conditional blocks with non-obvious purpose: One-line comment (e.g., `// Explicit: user
  specified`)
- Private methods: Block comment if name + parameters don't make purpose self-evident
- Early returns/continues: Include reason if not obvious from context
- Complex algorithms: Comment explaining approach at top, not line-by-line
- General: Any code where a reader would pause and wonder "why?" or "what's happening here?"

NEVER:

- XML doc comments (unless public API library)
- Commented-out code
- Restating what code literally does

## Tooling

### Formatting

- CSharpier is the ONLY formatting tool
- NEVER use `dotnet format` or other formatters
- Run pre-commit hooks on all changed files

### dotnet CLI

- Use dotnet CLI for: adding/removing packages, adding projects to solution
- Central package management via `Directory.Packages.props` - specify versions there, not in csproj
- Avoid `--no-build` or `--no-restore` flags; `dotnet test` handles restore + build automatically
- Minimal verbosity for build/test: `dotnet build -v m --no-incremental`, `dotnet test -v m`
- For verbose debugging, pipe to file: `dotnet test -v d 2>&1 > /tmp/test.log` then search with `rg`

### Project Structure

- SLNX format preferred over traditional SLN
- One Autofac/DI module per library to keep registration modular
- Dotnet tools configured in `.config/dotnet-tools.json`
