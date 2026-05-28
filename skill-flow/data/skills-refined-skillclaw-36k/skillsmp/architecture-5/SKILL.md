---
name: architecture
description: Service layer patterns, project responsibilities, dependency injection, and API contracts for RSSVibe. Use this skill when creating services, organizing code, or understanding project structure.
---

# Project Architecture

## Service Layer (`RSSVibe.Services`)

- MUST implement all business logic in the `RSSVibe.Services` project
- MUST define service interfaces (e.g., `IAuthService`, `IFeedService`) for dependency injection
- MUST use command/result patterns for service operations
- Services SHOULD be organized by domain area in folders (e.g., `Auth/`, `Feeds/`)
- MUST inject repositories, `UserManager`, and other infrastructure dependencies into services
- SHOULD use primary constructors for service classes
- Service implementations MUST be `internal sealed` (only interfaces and models are `public`)
- Each project MUST provide an `IServiceCollection` extension method to register its services

---

## Project Responsibilities

| Project | Responsibility |
|---------|---------------|
| `RSSVibe.Contracts` | API request/response DTOs, shared domain models |
| `RSSVibe.Services` | Business logic, validation, orchestration |
| `RSSVibe.Data` | Entity models, DbContext, configurations, migrations |
| `RSSVibe.ApiService` | Minimal API endpoints, routing, middleware |
| `RSSVibe.Web` | Blazor UI components and pages |

---

## Service Layer Patterns

```csharp
// Service interface (PUBLIC)
public interface IAuthService
{
    Task<RegisterUserResult> RegisterUserAsync(RegisterUserCommand command, CancellationToken ct);
}

// Service implementation with primary constructor (INTERNAL SEALED)
internal sealed class AuthService(
    UserManager<ApplicationUser> userManager,
    ILogger<AuthService> logger) : IAuthService
{
    public async Task<RegisterUserResult> RegisterUserAsync(
        RegisterUserCommand command,
        CancellationToken ct)
    {
        // Business logic here
    }
}

// Command model (PUBLIC - in same file as service or separate Commands/ folder)
public sealed record RegisterUserCommand(
    string Email,
    string Password,
    string DisplayName,
    bool MustChangePassword
);

// Result model (PUBLIC - in same file as service or separate Results/ folder)
public sealed record RegisterUserResult
{
    public bool Success { get; init; }
    public Guid UserId { get; init; }
    public string? Email { get; init; }
    public RegistrationError? Error { get; init; }
}
```

---

## Service Registration Pattern

**Each project MUST provide an extension method to register its services**

**Location**: `{ProjectName}/Extensions/ServiceCollectionExtensions.cs`

```csharp
// In RSSVibe.Services/Extensions/ServiceCollectionExtensions.cs
namespace RSSVibe.Services.Extensions;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddRssVibeServices(this IServiceCollection services)
    {
        // Register all services from this project
        services.AddScoped<IAuthService, AuthService>();
        services.AddScoped<IFeedService, FeedService>();
        // ... other services

        return services;
    }
}

// In Program.cs (RSSVibe.ApiService)
builder.Services.AddRssVibeServices(); // Single call registers all services
```

**Benefits**:
- Encapsulates service registration logic within each project
- `Program.cs` remains clean with single method calls per project
- Internal implementations hidden from consuming projects
- Easy to maintain and test service registration

---

## Dependency Injection

- MUST use scoped lifetime for request-specific services
- MUST use singleton lifetime for stateless services
- MUST register services via extension methods (e.g., `AddRssVibeServices()`)
- Extension methods SHOULD be named `Add{ProjectName}` (e.g., `AddRssVibeServices`, `AddRssVibeDatabase`)
- Service implementations MUST be `internal sealed` to prevent external instantiation

---

## API Contracts

- MUST define all API request/response models in the `RSSVibe.Contracts` project
- API contracts are shared between frontend and backend services via project reference
- MUST use positional records for all contract models (immutability and clarity)
- MUST document contract changes in commit messages and ADRs when adding new endpoints or modifying existing ones
- Contracts include DTOs for API requests, responses, and domain models exposed to clients
- **Shared contracts** like `PagingDto` are placed in the root `RSSVibe.Contracts` namespace and reused across multiple feature areas (e.g., Feeds, FeedAnalyses, FeedItems) to ensure consistency
