---
name: asp-rules
description: ASP.NET Core Best Practices and Coding Standards for Beyond8 project
---

# ASP.NET Core Best Practices Rules

## Overview
Best practices and coding standards for ASP.NET Core development in the Beyond8 project. Follow these rules to maintain consistency, security, and code quality across all services.

---

## 1. API Design (Minimal APIs)

### Endpoint Organization
- Always organize endpoints using MapGroup with versioning (e.g., /api/v1/...)
- Use static extension methods for API mapping (e.g., MapAuthApi())
- Add descriptive tags, names, and descriptions for OpenAPI documentation
- Always specify return types using .Produces<>() for proper OpenAPI generation
- Explicitly use AllowAnonymous() or RequireAuthorization() on each endpoint
- Apply rate limiting where appropriate using RequireRateLimiting()

### Request/Response Handling
- Always use ApiResponse<T> wrapper for consistent API responses
- Return appropriate HTTP status codes: 200 for success, 400 for bad requests, 401 for unauthorized, 404 for not found, 500 for server errors
- Always handle both success and failure cases in endpoint handlers
- Never return raw exceptions or unhandled errors to clients

---

## 2. Response Consistency

### ApiResponse Pattern
- Always wrap service responses in ApiResponse<T> type
- Use factory methods: SuccessResponse(), FailureResponse(), SuccessPagedResponse()
- Include meaningful messages in all responses for user understanding
- Use SuccessPagedResponse() for paginated data with metadata

### Response Examples
- Success: ApiResponse<T>.SuccessResponse(data, message)
- Failure: ApiResponse<T>.FailureResponse(message)
- Paginated: ApiResponse<List<T>>.SuccessPagedResponse(items, totalItems, pageNumber, pageSize, message)

---

## 3. Error Handling

### Global Exception Middleware
- Always use GlobalExceptionsMiddleware for centralized error handling
- Log all exceptions with appropriate log levels before handling
- Map exceptions to appropriate HTTP status codes using switch expressions
- Never expose sensitive error details to clients in production environment

### Service Layer Error Handling
- Catch and handle specific exceptions in service methods
- Return ApiResponse<T>.FailureResponse() instead of throwing exceptions for business logic errors
- Always log errors with structured logging using ILogger
- Never use generic catch blocks without logging the exception
- Use try-catch blocks for error handling, not for flow control

### Exception Mapping
- UnauthorizedAccessException maps to HTTP 401 Unauthorized
- ArgumentException maps to HTTP 400 Bad Request
- KeyNotFoundException maps to HTTP 404 Not Found
- All other exceptions map to HTTP 500 Internal Server Error

---

## 4. Validation

### FluentValidation (Recommended)
- Always use FluentValidation for request validation in Minimal APIs
- FluentValidation provides better type safety, testability, and separation of concerns
- Create validators in Application/Validators folder, organized by domain (e.g., Auth, Users)
- Register validators using `AddValidatorsFromAssemblyContaining<T>()` in DI container
- Inject validators into endpoint handlers using `IValidator<TRequest>`
- Use ValidationExtensions.ValidateRequest() method for consistent validation handling

### Validator Rules
- Use NotEmpty() instead of Required for non-nullable types
- Provide meaningful error messages in Vietnamese for user-facing validation
- Common rules: NotEmpty(), EmailAddress(), MinimumLength(), MaximumLength(), Matches(), Equal(), NotEqual()
- Use Length(exact) for fixed-length strings like OTP codes
- Chain multiple rules using method chaining for readability
- Use Matches() with regex for complex patterns (passwords, phone numbers)

### Validation in Endpoints
- Always validate request DTOs at the beginning of endpoint handlers
- Pattern: `if (!request.ValidateRequest(validator, out var validationResult)) return validationResult!;`
- Validation errors are automatically formatted as ApiResponse<object>.FailureResponse()
- Never process requests without validation

### Validator Examples
```csharp
public class RegisterRequestValidator : AbstractValidator<RegisterRequest>
{
    public RegisterRequestValidator()
    {
        RuleFor(x => x.Email)
            .NotEmpty().WithMessage("Email không được để trống")
            .EmailAddress().WithMessage("Email không hợp lệ")
            .MaximumLength(256).WithMessage("Email không được vượt quá 256 ký tự");

        RuleFor(x => x.Password)
            .NotEmpty().WithMessage("Password không được để trống")
            .MinimumLength(8).WithMessage("Password tối thiểu 8 ký tự")
            .Matches(@"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)")
            .WithMessage("Password phải có ít nhất 1 chữ thường, 1 chữ hoa và 1 số");
    }
}
```

---

## 5. Security Best Practices

### Password Handling
- Always hash passwords using PasswordHasher<User> before storing
- Never store plain text passwords in database
- Use strong password requirements: minimum length 8 characters, complexity rules
- Validate password strength in service layer before hashing

### JWT Authentication
- Store JWT configuration in appsettings.json, never hardcode
- Use secure token expiration times (typically 15-60 minutes for access tokens)
- Always implement refresh token mechanism for long-lived sessions
- Validate tokens on all protected endpoints using RequireAuthorization()

### Authorization
- Use RequireAuthorization() on all protected endpoints
- Use role-based authorization when user roles are defined
- Always validate user permissions in service layer, not just in API layer
- Never trust client-side authentication state, always verify server-side

---

## 6. Dependency Injection

### Service Registration
- Use extension methods for service registration (e.g., AddApplicationServices())
- Register services with appropriate lifetimes based on usage:
  - Use Scoped for services with database context (IUnitOfWork, services)
  - Use Transient for stateless services without dependencies on context
  - Use Singleton only for thread-safe services (caching, configuration)
- Always register repositories through Unit of Work pattern
- Group related service registrations in extension methods

### Constructor Injection
- Use primary constructors (C# 12) when available for cleaner code
- Always inject interfaces, never concrete classes
- Never use service locator pattern or static service resolution
- Keep constructor parameter lists manageable (consider refactoring if too many)

---

## 7. Repository Pattern & Unit of Work

### Repository Interface
- Define repository interfaces in Domain layer
- Implement repositories in Infrastructure layer
- Use generic repository pattern (IGenericRepository<T>) for common CRUD operations
- Add specific methods only when needed, avoid duplicating generic methods
- Use Unit of Work pattern for transaction management across repositories

### Database Operations
- Always use async methods: FindOneAsync, FindAllAsync, AddAsync, UpdateAsync, SaveChangesAsync
- Use transactions for operations that must succeed together
- Handle database exceptions appropriately with specific error messages
- Never use synchronous database methods (.Result, .Wait())

### Unit of Work Pattern
- Expose repositories as properties through IUnitOfWork interface
- Implement SaveChangesAsync() in UnitOfWork for transaction control
- Use IUnitOfWork for all database operations in service layer

---

## 8. Logging

### Structured Logging
- Always use ILogger<T> for logging in all services
- Use structured logging with parameters, never string interpolation
- Include relevant context in log messages using named parameters
- Use appropriate log levels:
  - LogError for exceptions and critical errors
  - LogWarning for business logic issues and recoverable errors
  - LogInformation for important business events and milestones
  - LogDebug for detailed debugging information (development only)

### Logging Examples
- Good: logger.LogInformation("User registered successfully: {Email}", request.Email)
- Good: logger.LogError(ex, "Error registering user with email {Email}", request.Email)
- Bad: logger.LogInformation($"User registered successfully: {request.Email}")

---

## 9. Async/Await Patterns

### Asynchronous Methods
- Always use async/await for all I/O operations: database, HTTP, file system, external APIs
- Return Task<T> or Task from async methods, never void
- Use ConfigureAwait(false) only when necessary (rare in ASP.NET Core)
- Never use .Result or .Wait() on async methods as it causes deadlocks
- Use async all the way: if a method calls async, it should be async

### Async Best Practices
- Good: public async Task<ApiResponse<T>> MethodAsync() { await ... }
- Bad: public Task<ApiResponse<T>> MethodAsync() { return task.Result; }
- Always await async calls, don't return tasks directly unless intentionally

---

## 10. Clean Architecture Layers

### Layer Responsibilities
- Domain Layer: Contains entities, enums, repository interfaces, domain logic only
- Application Layer: Contains DTOs, service interfaces and implementations, mappings
- Infrastructure Layer: Contains database context, repository implementations, external services
- API Layer: Contains endpoints, request/response handling, middleware configuration

### Dependency Direction
- Maintain strict dependency direction: API → Application → Domain ← Infrastructure
- Keep Domain layer completely independent of all other layers
- Never reference Infrastructure layer from Application layer
- API layer can reference Application and Infrastructure, but not Domain directly

---

## 11. Entity Framework & Database

### Entities
- Always inherit from BaseEntity for common properties: Id, CreatedAt, UpdatedAt
- Use [Required] attribute for required properties with meaningful error messages
- Configure relationships explicitly in DbContext OnModelCreating method
- Use [MaxLength] for string properties to define database column constraints

### Migrations
- Always create migrations for schema changes, never modify database manually
- Apply migrations on application startup in Development environment
- Use CI/CD pipeline for migration application in Production
- Always review migration files before applying to ensure correctness

### Database Context
- Use DbContextFactory for creating contexts in migrations
- Apply migrations using MigrateDbContextAsync<T>() extension method in Program.cs
- Never commit sensitive connection strings to source control

---

## 12. Caching

### Cache Service
- Use ICacheService for all caching operations
- Always set appropriate expiration times for cached data
- Use consistent key naming conventions (e.g., "otp_register:{email}")
- Consider cache invalidation strategy when updating data

### Cache Examples
- Key format: "prefix:identifier" (e.g., "otp_register:{email}")
- Set: await cacheService.SetAsync(key, value, TimeSpan.FromMinutes(5))
- Get: await cacheService.GetAsync<T>(key)
- Always handle cache misses gracefully

---

## 13. Configuration

### appsettings.json
- Store all configuration in appsettings.json and appsettings.Development.json
- Use strongly-typed configuration classes when possible
- Never commit secrets or sensitive data to source control
- Use User Secrets (Development) or environment variables (Production) for sensitive data

### Connection Strings
- Reference connection strings by name using constants (e.g., Const.IdentityServiceDatabase)
- Store connection strings in appsettings.json, never hardcode
- Use extension methods for database configuration (e.g., AddPostgresDatabase<T>())

---

## 14. Code Organization & Naming

### File Structure
- Group related files in folders: Dtos, Services, Entities, Repositories, Mappings
- Use descriptive namespaces matching folder structure exactly
- Keep files focused on single responsibility principle
- Separate concerns: put interfaces in separate files from implementations

### Naming Conventions
- Use PascalCase for classes, methods, properties, interfaces
- Use camelCase for local variables and method parameters
- Prefix interfaces with I (e.g., IAuthService, IUserRepository)
- Use descriptive names that clearly indicate purpose and responsibility
- Use Async suffix for async methods (e.g., RegisterUserAsync)

### Mapping
- Create mapping extension methods in Application/Mappings folder
- Keep mapping logic separate from business logic
- Use consistent naming: ToEntity(), ToDto(), ToUserSimpleResponse()
- Group mappings by domain entity (e.g., RegisterMappings, UserMappings)

---

## 15. Performance & Testing

### Performance Best Practices
- Use FindOneAsync instead of fetching all records and filtering in memory
- Include only necessary data in queries, avoid SELECT * patterns
- Use pagination for large datasets using SuccessPagedResponse()
- Cache frequently accessed data that doesn't change often
- Optimize database queries and ensure proper indexes exist

### Testing Considerations
- Design services to be testable using dependency injection and interfaces
- Mock dependencies in unit tests using test doubles or mocks
- Test business logic separately from infrastructure concerns
- Use integration tests for database operations, unit tests for business logic

---

## Quick Reference

### Common Patterns
- Service Response: ApiResponse<T>.SuccessResponse(data, message)
- Error Response: ApiResponse<T>.FailureResponse(message)
- Paginated Response: ApiResponse<List<T>>.SuccessPagedResponse(items, total, page, size, message)
- Structured Logging: logger.LogInformation("Message with {Parameter}", value)
- Async Query: await repository.FindOneAsync(x => x.Id == id)
- Service Registration: builder.Services.AddScoped<IService, Service>()
- Protected Endpoint: .RequireAuthorization()
- Validation: [Required(ErrorMessage = "Error message")]

### Service Lifetimes
- Scoped: Services with database context (IUnitOfWork, application services)
- Transient: Stateless services without context dependencies
- Singleton: Thread-safe services (cache, configuration readers)

---

## Checklist

Before submitting code, ensure:
- [ ] All API endpoints use ApiResponse<T> wrapper
- [ ] Services return ApiResponse<T> instead of throwing exceptions for business errors
- [ ] All async methods use async/await properly, no .Result or .Wait()
- [ ] DTOs have validation attributes with meaningful error messages in Vietnamese
- [ ] Logging uses structured logging with parameters, not string interpolation
- [ ] Dependencies are injected through constructors, not service locator
- [ ] Repository pattern and Unit of Work are used for all data access
- [ ] Clean architecture layers are respected (no circular dependencies)
- [ ] Security best practices followed (password hashing, JWT, authorization)
- [ ] Error handling is centralized in middleware
- [ ] Configuration stored in appsettings.json, not hardcoded
- [ ] Code follows consistent naming conventions (PascalCase, camelCase)
- [ ] Database operations use async methods only
