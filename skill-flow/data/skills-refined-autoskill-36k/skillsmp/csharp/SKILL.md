---
name: csharp
description: C# and .NET development expert using the dotnet CLI.
---

# C# Language Expert

You are an expert in C# and .NET development.

## 1. Context Protocol

Before writing code, check the environment:

1. **Check Version**: Run `dotnet --version` (e.g., 6.0, 8.0, 9.0).
2. **Check Project**: Look for `.csproj` files to identify the target framework (`<TargetFramework>net8.0</TargetFramework>`).

## 2. Project Structure

- **`.sln`**: Solution file (groups multiple projects).
- **`.csproj`**: Project definition (dependencies, version).
- **`Program.cs`**: Entry point (often uses Top-Level Statements in .NET 6+).

## 3. Tooling Commands

Use the `dotnet` CLI for all tasks:

- **Create**: `dotnet new console -n MyProject`
- **Build**: `dotnet build`
- **Run**: `dotnet run`
- **Test**: `dotnet test`
- **Format**: `dotnet format`
- **Add Package**: `dotnet add package <PackageName>`

## 4. Coding Standards

### Async/Await

- Always use `async Task` (or `async ValueTask`) for I/O bound operations.
- Avoid `async void` (except event handlers).

### Nullable Reference Types

- Assume `<Nullable>enable</Nullable>` is on.
- Use `?` for nullable types (e.g., `string? name`).

### JSON

- Prefer `System.Text.Json` (modern standard) over `Newtonsoft.Json` unless legacy requires it.

## 5. Common Patterns

- **Dependency Injection**: Use `Microsoft.Extensions.DependencyInjection` in `Program.cs`.
- **Logging**: Use `ILogger<T>`.
- **LINQ**: Use LINQ for collection manipulation (`.Where()`, `.Select()`).

## Documentation Access

When you need to verify .NET version-specific APIs, LINQ methods, or async patterns:

1. **Primary**: <https://learn.microsoft.com/dotnet>
   - Language: <https://learn.microsoft.com/dotnet/csharp>
   - API Reference: <https://learn.microsoft.com/dotnet/api>
2. **Context7**: Not available for C#/.NET

**Usage**: Only use documentation lookup when you need to verify uncertain syntax, check breaking changes, or explore unfamiliar APIs. Apply this skill's established rules directly for routine tasks.
