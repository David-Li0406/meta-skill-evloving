---
name: csharp
description: "C# development process and modern practices review. Use when writing C# code, reviewing C# PRs, working with ASP.NET Core applications, implementing async patterns, or setting up project structure. Also use when nullable reference types are disabled, code uses `.Result` or `.Wait()`, records aren't used for DTOs, dependency injection is misused, or LINQ is inefficient. Essential for Entity Framework Core, minimal APIs, pattern matching, and modern C# (10+) features."
---

# C# Skill

## Overview

Modern C# is expressive and safe. This skill guides writing clean, maintainable C# that leverages nullable reference types, records, and async patterns properly.

**Core principle:** Embrace null safety and immutability. C# 10+ gives you records, nullable reference types, and pattern matching—use them to make invalid states unrepresentable.

## The C# Development Process

### Phase 1: Enable Safety Features

**Before writing implementation:**

1. **Enable Nullable Reference Types**
   - `<Nullable>enable</Nullable>` in project file
   - Forces explicit null handling
   - Catches null errors at compile time

2. **Use Records for Data**
   - Immutable by default
   - Value semantics for equality
   - `with` expressions for updates

3. **Plan Async Flow**
   - Async all the way
   - No blocking on async code
   - CancellationToken support

### Phase 2: Implement Safely

**Write modern C#:**

1. **Use Nullable Reference Types**
   ```csharp
   // ✅ Explicit nullability
   public string? GetMiddleName(User user) => user.MiddleName;

   public string GetDisplayName(User user)
   {
       return user.DisplayName ?? user.Email ?? "Anonymous";
   }

   // ❌ Disabled nullable types
   #nullable disable
   public string GetName(User user) // Null is implicit everywhere
   ```

2. **Use Records for DTOs**
   ```csharp
   // ✅ Immutable record
   public record User(string Name, string Email, int Age);

   // Update with 'with' expression
   var updated = user with { Email = "new@example.com" };

   // ❌ Mutable class
   public class User
   {
       public string Name { get; set; }  // Mutable
       public string Email { get; set; }
   }
   ```

3. **Async All the Way**
   ```csharp
   // ✅ Async through the stack
   public async Task<User> GetUserAsync(int id, CancellationToken ct = default)
   {
       return await _repository.GetByIdAsync(id, ct);
   }

   // ❌ Blocking on async
   public User GetUser(int id)
   {
       return _repository.GetByIdAsync(id).Result;  // Deadlock risk!
   }
   ```

### Phase 3: Review for Quality

**Before approving:**

1. **Check Null Safety**
   - Nullable enabled project-wide?
   - No `!` null-forgiving without justification?
   - Proper null checks at boundaries?

2. **Check Async Patterns**
   - No `.Result` or `.Wait()`?
   - CancellationToken passed through?
   - ConfigureAwait used in libraries?

3. **Check DI Patterns**
   - Constructor injection used?
   - Correct lifetime (Scoped, Transient, Singleton)?
   - No service locator pattern?

## Red Flags - STOP and Fix

### Async Red Flags

```csharp
// .Result or .Wait() - deadlock risk
var user = GetUserAsync().Result;
await GetUserAsync().Wait();

// async void - fire and forget, no error handling
async void HandleClick() { }  // Only for event handlers!

// Missing ConfigureAwait in libraries
await SomeAsync();  // In library code, use ConfigureAwait(false)

// Not passing CancellationToken
await LongOperation();  // How do you cancel this?
```

### Null Safety Red Flags

```csharp
// Excessive null-forgiving operator
string name = GetName()!;  // Hiding potential null

// Nullable disabled
#nullable disable  // Loses compile-time null safety

// Null checks everywhere instead of proper types
if (user != null && user.Name != null)  // Use nullable types properly
```

### DI Red Flags

```csharp
// Service locator pattern
var service = serviceProvider.GetService<IMyService>();

// Wrong lifetime
services.AddSingleton<DbContext>();  // DbContext should be Scoped!

// Captive dependencies
// Singleton holding Scoped service = bug
public class MySingleton
{
    private readonly IScopedService _scoped;  // Wrong!
}
```

## Common Rationalizations - Don't Accept These

| Excuse | Reality |
|--------|---------|
| "Nullable types are noisy" | They prevent null reference exceptions. Enable them. |
| ".Result is fine here" | It causes deadlocks. Use async all the way. |
| "Records are just for DTOs" | Records are great for any immutable data. |
| "We need to support old .NET" | .NET 6+ is LTS. Upgrade or use polyfills. |
| "ConfigureAwait is obsolete" | It matters in libraries. Use it there. |
| "Singleton is simpler" | Wrong lifetime = bugs. Use correct scope. |

## C# Quality Checklist

Before approving C# code:

- [ ] **Nullable enabled**: Project-wide `<Nullable>enable</Nullable>`
- [ ] **Records used**: For DTOs and immutable data
- [ ] **Async proper**: No `.Result`/`.Wait()`, tokens passed
- [ ] **DI correct**: Constructor injection, correct lifetimes
- [ ] **Pattern matching**: Switch expressions, property patterns
- [ ] **LINQ efficient**: No multiple enumeration
- [ ] **Tests present**: Unit and integration tests

## Quick Patterns

### Minimal API

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddScoped<IUserService, UserService>();

var app = builder.Build();

app.MapGet("/users/{id}", async (int id, IUserService service, CancellationToken ct) =>
{
    var user = await service.GetByIdAsync(id, ct);
    return user is null ? Results.NotFound() : Results.Ok(user);
});

app.MapPost("/users", async (CreateUserRequest request, IUserService service, CancellationToken ct) =>
{
    var user = await service.CreateAsync(request, ct);
    return Results.Created($"/users/{user.Id}", user);
});

app.Run();
```

### Controller Pattern

```csharp
[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    private readonly IUserService _userService;

    public UsersController(IUserService userService)
    {
        _userService = userService;
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<User>> GetUser(int id, CancellationToken ct)
    {
        var user = await _userService.GetByIdAsync(id, ct);
        return user is null ? NotFound() : Ok(user);
    }

    [HttpPost]
    public async Task<ActionResult<User>> CreateUser(
        CreateUserRequest request,
        CancellationToken ct)
    {
        var user = await _userService.CreateAsync(request, ct);
        return CreatedAtAction(nameof(GetUser), new { id = user.Id }, user);
    }
}
```

### Service Pattern

```csharp
public interface IUserService
{
    Task<User?> GetByIdAsync(int id, CancellationToken ct = default);
    Task<User> CreateAsync(CreateUserRequest request, CancellationToken ct = default);
}

public class UserService : IUserService
{
    private readonly AppDbContext _context;
    private readonly ILogger<UserService> _logger;

    public UserService(AppDbContext context, ILogger<UserService> logger)
    {
        _context = context;
        _logger = logger;
    }

    public async Task<User?> GetByIdAsync(int id, CancellationToken ct = default)
    {
        return await _context.Users.FindAsync(new object[] { id }, ct);
    }

    public async Task<User> CreateAsync(CreateUserRequest request, CancellationToken ct = default)
    {
        var user = new User(request.Name, request.Email);
        _context.Users.Add(user);
        await _context.SaveChangesAsync(ct);

        _logger.LogInformation("Created user {UserId}", user.Id);
        return user;
    }
}
```

## Quick Commands

```bash
# Build
dotnet build

# Test
dotnet test

# Run
dotnet run

# Format
dotnet format

# Check outdated packages
dotnet list package --outdated

# Add package
dotnet add package PackageName

# Publish
dotnet publish -c Release
```

## References

Detailed patterns and examples in `references/`:
- `modern-csharp.md` - C# 10+ features
- `aspnet-patterns.md` - ASP.NET Core best practices
- `ef-core-patterns.md` - Entity Framework Core patterns
