---
id: csharp-dotnet-patterns
name: "C# .NET Patterns"
domain: DEV
skill: faion-software-developer
category: "development"
---

# C# .NET Patterns

## Overview

.NET is a modern, cross-platform framework for building web APIs, microservices, and enterprise applications. This methodology covers ASP.NET Core patterns, clean architecture, and best practices for C# development.

## When to Use

- Enterprise web applications
- Microservices architecture
- REST and gRPC APIs
- Cloud-native applications
- Applications requiring high performance

## Key Principles

1. **Dependency injection** - Built-in DI container
2. **Middleware pipeline** - Request/response processing
3. **Configuration** - Environment-based configuration
4. **Async by default** - Async/await everywhere
5. **Minimal APIs** - Lightweight API endpoints

## Best Practices

### Project Structure (Clean Architecture)

```
src/
├── MyApp.Api/                      # Presentation layer
│   ├── Controllers/
│   ├── Filters/
│   ├── Middleware/
│   └── Program.cs
│
├── MyApp.Application/              # Application layer
│   ├── Common/
│   │   ├── Behaviors/
│   │   ├── Interfaces/
│   │   └── Mappings/
│   ├── Users/
│   │   ├── Commands/
│   │   ├── Queries/
│   │   └── EventHandlers/
│   └── DependencyInjection.cs
│
├── MyApp.Domain/                   # Domain layer
│   ├── Entities/
│   ├── ValueObjects/
│   ├── Enums/
│   ├── Events/
│   ├── Exceptions/
│   └── Interfaces/
│
├── MyApp.Infrastructure/           # Infrastructure layer
│   ├── Persistence/
│   ├── Services/
│   └── DependencyInjection.cs
│
└── tests/
    ├── MyApp.Application.Tests/
    ├── MyApp.Domain.Tests/
    └── MyApp.Api.Tests/
```

### Domain Layer

```csharp
// Domain/Entities/BaseEntity.cs
namespace MyApp.Domain.Entities;

public abstract class BaseEntity
{
    public Guid Id { get; protected set; } = Guid.NewGuid();
    public DateTime CreatedAt { get; protected set; } = DateTime.UtcNow;
    public DateTime UpdatedAt { get; protected set; } = DateTime.UtcNow;

    private readonly List<IDomainEvent> _domainEvents = new();
    public IReadOnlyCollection<IDomainEvent> DomainEvents => _domainEvents.AsReadOnly();

    public void AddDomainEvent(IDomainEvent domainEvent)
    {
        _domainEvents.Add(domainEvent);
    }

    public void ClearDomainEvents()
    {
        _domainEvents.Clear();
    }
}

// Domain/Entities/User.cs
namespace MyApp.Domain.Entities;

public class User : BaseEntity
{
    public string Name { get; private set; } = string.Empty;
    public Email Email { get; private set; } = null!;
    public string PasswordHash { get; private set; } = string.Empty;
    public UserRole Role { get; private set; }
    public bool IsActive { get; private set; } = true;
    public Guid OrganizationId { get; private set; }
    public Organization Organization { get; private set; } = null!;

    private readonly List<Post> _posts = new();
    public IReadOnlyCollection<Post> Posts => _posts.AsReadOnly();

    private User() { } // For EF Core

    public static User Create(string name, Email email, string passwordHash, Guid organizationId)
    {
        var user = new User
        {
            Name = name,
            Email = email,
            PasswordHash = passwordHash,
            OrganizationId = organizationId,
            Role = UserRole.Member
        };

        user.AddDomainEvent(new UserCreatedEvent(user.Id, user.Email.Value));
        return user;
    }

    public void UpdateProfile(string name, Email email)
    {
        Name = name;
        Email = email;
        UpdatedAt = DateTime.UtcNow;
    }

    public void Promote()
    {
        if (Role == UserRole.Admin)
            throw new DomainException("User is already an admin");

        Role = UserRole.Admin;
        AddDomainEvent(new UserPromotedEvent(Id));
    }

    public void Deactivate()
    {
        IsActive = false;
        AddDomainEvent(new UserDeactivatedEvent(Id));
    }
}

// Domain/ValueObjects/Email.cs
namespace MyApp.Domain.ValueObjects;

public sealed class Email : ValueObject
{
    public string Value { get; }

    private Email(string value) => Value = value;

    public static Email Create(string email)
    {
        if (string.IsNullOrWhiteSpace(email))
            throw new DomainException("Email cannot be empty");

        if (!IsValidEmail(email))
            throw new DomainException("Invalid email format");

        return new Email(email.ToLowerInvariant());
    }

    private static bool IsValidEmail(string email)
    {
        try
        {
            var addr = new System.Net.Mail.MailAddress(email);
            return addr.Address == email;
        }
        catch
        {
            return false;
        }
    }

    protected override IEnumerable<object> GetEqualityComponents()
    {
        yield return Value;
    }

    public static implicit operator string(Email email) => email.Value;
}
```

### Application Layer (CQRS with MediatR)

```csharp
// Application/Users/Commands/CreateUser/CreateUserCommand.cs
namespace MyApp.Application.Users.Commands.CreateUser;

public record CreateUserCommand(
    string Name,
    string Email,
    string Password,
    Guid OrganizationId
) : IRequest<Guid>;

public class CreateUserCommandValidator : AbstractValidator<CreateUserCommand>
{
    public CreateUserCommandValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty()
            .MinimumLength(2)
            .MaximumLength(100);

        RuleFor(x => x.Email)
            .NotEmpty()
            .EmailAddress();

        RuleFor(x => x.Password)
            .NotEmpty()
            .MinimumLength(8);
    }
}

public class CreateUserCommandHandler : IRequestHandler<CreateUserCommand, Guid>
{
    private readonly IApplicationDbContext _context;
    private readonly IPasswordHasher _passwordHasher;

    public CreateUserCommandHandler(
        IApplicationDbContext context,
        IPasswordHasher passwordHasher)
    {
        _context = context;
        _passwordHasher = passwordHasher;
    }

    public async Task<Guid> Handle(CreateUserCommand request, CancellationToken cancellationToken)
    {
        var email = Email.Create(request.Email);

        var exists = await _context.Users
            .AnyAsync(u => u.Email == email && u.OrganizationId == request.OrganizationId,
                     cancellationToken);

        if (exists)
            throw new ConflictException("User with this email already exists");

        var passwordHash = _passwordHasher.Hash(request.Password);

        var user = User.Create(
            request.Name,
            email,
            passwordHash,
            request.OrganizationId
        );

        _context.Users.Add(user);
        await _context.SaveChangesAsync(cancellationToken);

        return user.Id;
    }
}

// Application/Users/Queries/GetUsers/GetUsersQuery.cs
namespace MyApp.Application.Users.Queries.GetUsers;

public record GetUsersQuery(
    Guid OrganizationId,
    string? Search,
    string? Role,
    int Page = 1,
    int PageSize = 20
) : IRequest<PaginatedList<UserDto>>;

public class GetUsersQueryHandler : IRequestHandler<GetUsersQuery, PaginatedList<UserDto>>
{
    private readonly IApplicationDbContext _context;
    private readonly IMapper _mapper;

    public GetUsersQueryHandler(IApplicationDbContext context, IMapper mapper)
    {
        _context = context;
        _mapper = mapper;
    }

    public async Task<PaginatedList<UserDto>> Handle(
        GetUsersQuery request,
        CancellationToken cancellationToken)
    {
        var query = _context.Users
            .AsNoTracking()
            .Where(u => u.OrganizationId == request.OrganizationId && u.IsActive);

        if (!string.IsNullOrWhiteSpace(request.Search))
        {
            var search = request.Search.ToLower();
            query = query.Where(u =>
                u.Name.ToLower().Contains(search) ||
                u.Email.Value.ToLower().Contains(search));
        }

        if (!string.IsNullOrWhiteSpace(request.Role) &&
            Enum.TryParse<UserRole>(request.Role, true, out var role))
        {
            query = query.Where(u => u.Role == role);
        }

        return await query
            .OrderByDescending(u => u.CreatedAt)
            .ProjectTo<UserDto>(_mapper.ConfigurationProvider)
            .PaginatedListAsync(request.Page, request.PageSize, cancellationToken);
    }
}

// Application/Users/Queries/GetUsers/UserDto.cs
namespace MyApp.Application.Users.Queries.GetUsers;

public record UserDto
{
    public Guid Id { get; init; }
    public string Name { get; init; } = string.Empty;
    public string Email { get; init; } = string.Empty;
    public string Role { get; init; } = string.Empty;
    public bool IsActive { get; init; }
    public DateTime CreatedAt { get; init; }

    private class Mapping : Profile
    {
        public Mapping()
        {
            CreateMap<User, UserDto>()
                .ForMember(d => d.Email, opt => opt.MapFrom(s => s.Email.Value))
                .ForMember(d => d.Role, opt => opt.MapFrom(s => s.Role.ToString()));
        }
    }
}
```

### Infrastructure Layer

```csharp
// Infrastructure/Persistence/ApplicationDbContext.cs
namespace MyApp.Infrastructure.Persistence;

public class ApplicationDbContext : DbContext, IApplicationDbContext
{
    private readonly IMediator _mediator;

    public ApplicationDbContext(
        DbContextOptions<ApplicationDbContext> options,
        IMediator mediator) : base(options)
    {
        _mediator = mediator;
    }

    public DbSet<User> Users => Set<User>();
    public DbSet<Organization> Organizations => Set<Organization>();
    public DbSet<Post> Posts => Set<Post>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly());
        base.OnModelCreating(modelBuilder);
    }

    public override async Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        // Dispatch domain events
        var entities = ChangeTracker
            .Entries<BaseEntity>()
            .Where(e => e.Entity.DomainEvents.Any())
            .Select(e => e.Entity)
            .ToList();

        var domainEvents = entities
            .SelectMany(e => e.DomainEvents)
            .ToList();

        entities.ForEach(e => e.ClearDomainEvents());

        foreach (var domainEvent in domainEvents)
        {
            await _mediator.Publish(domainEvent, cancellationToken);
        }

        return await base.SaveChangesAsync(cancellationToken);
    }
}

// Infrastructure/Persistence/Configurations/UserConfiguration.cs
namespace MyApp.Infrastructure.Persistence.Configurations;

public class UserConfiguration : IEntityTypeConfiguration<User>
{
    public void Configure(EntityTypeBuilder<User> builder)
    {
        builder.ToTable("Users");

        builder.HasKey(u => u.Id);

        builder.Property(u => u.Name)
            .HasMaxLength(100)
            .IsRequired();

        builder.OwnsOne(u => u.Email, email =>
        {
            email.Property(e => e.Value)
                .HasColumnName("Email")
                .HasMaxLength(256)
                .IsRequired();

            email.HasIndex(e => e.Value).IsUnique();
        });

        builder.Property(u => u.PasswordHash)
            .HasMaxLength(256)
            .IsRequired();

        builder.Property(u => u.Role)
            .HasConversion<string>()
            .HasMaxLength(50);

        builder.HasOne(u => u.Organization)
            .WithMany(o => o.Users)
            .HasForeignKey(u => u.OrganizationId)
            .OnDelete(DeleteBehavior.Restrict);

        builder.HasMany(u => u.Posts)
            .WithOne(p => p.Author)
            .HasForeignKey(p => p.AuthorId)
            .OnDelete(DeleteBehavior.Cascade);

        builder.HasIndex(u => new { u.Email, u.OrganizationId });
    }
}
```

### API Layer

```csharp
// Api/Controllers/UsersController.cs
namespace MyApp.Api.Controllers;

[ApiController]
[Route("api/v1/[controller]")]
[Authorize]
public class UsersController : ControllerBase
{
    private readonly ISender _mediator;

    public UsersController(ISender mediator)
    {
        _mediator = mediator;
    }

    [HttpGet]
    [ProducesResponseType(typeof(PaginatedList<UserDto>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetUsers(
        [FromQuery] string? search,
        [FromQuery] string? role,
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 20,
        CancellationToken cancellationToken = default)
    {
        var organizationId = User.GetOrganizationId();
        var query = new GetUsersQuery(organizationId, search, role, page, pageSize);
        var result = await _mediator.Send(query, cancellationToken);
        return Ok(result);
    }

    [HttpGet("{id:guid}")]
    [ProducesResponseType(typeof(UserDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetUser(
        Guid id,
        CancellationToken cancellationToken = default)
    {
        var query = new GetUserQuery(id);
        var result = await _mediator.Send(query, cancellationToken);
        return Ok(result);
    }

    [HttpPost]
    [ProducesResponseType(typeof(Guid), StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> CreateUser(
        [FromBody] CreateUserRequest request,
        CancellationToken cancellationToken = default)
    {
        var organizationId = User.GetOrganizationId();
        var command = new CreateUserCommand(
            request.Name,
            request.Email,
            request.Password,
            organizationId
        );

        var id = await _mediator.Send(command, cancellationToken);
        return CreatedAtAction(nameof(GetUser), new { id }, id);
    }

    [HttpPut("{id:guid}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> UpdateUser(
        Guid id,
        [FromBody] UpdateUserRequest request,
        CancellationToken cancellationToken = default)
    {
        var command = new UpdateUserCommand(id, request.Name, request.Email);
        await _mediator.Send(command, cancellationToken);
        return NoContent();
    }

    [HttpDelete("{id:guid}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    public async Task<IActionResult> DeleteUser(
        Guid id,
        CancellationToken cancellationToken = default)
    {
        var command = new DeleteUserCommand(id);
        await _mediator.Send(command, cancellationToken);
        return NoContent();
    }
}

// Api/Program.cs (Minimal API alternative)
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);

var app = builder.Build();

app.MapGet("/api/v1/users", async (
    ISender mediator,
    [FromQuery] string? search,
    [FromQuery] int page = 1,
    CancellationToken ct = default) =>
{
    var query = new GetUsersQuery(search, page);
    return Results.Ok(await mediator.Send(query, ct));
});

app.MapPost("/api/v1/users", async (
    ISender mediator,
    CreateUserRequest request,
    CancellationToken ct = default) =>
{
    var command = new CreateUserCommand(request.Name, request.Email, request.Password);
    var id = await mediator.Send(command, ct);
    return Results.Created($"/api/v1/users/{id}", id);
});

app.Run();
```

## Anti-patterns

### Avoid: Anemic Domain Model

```csharp
// BAD - domain logic in service
public class User
{
    public UserRole Role { get; set; }
}

public class UserService
{
    public void Promote(User user)
    {
        user.Role = UserRole.Admin;
    }
}

// GOOD - rich domain model
public class User
{
    public UserRole Role { get; private set; }

    public void Promote()
    {
        if (Role == UserRole.Admin)
            throw new DomainException("Already admin");
        Role = UserRole.Admin;
    }
}
```

### Avoid: Exposing Domain Entities

```csharp
// BAD - returns entity directly
[HttpGet("{id}")]
public async Task<User> GetUser(Guid id) =>
    await _context.Users.FindAsync(id);

// GOOD - use DTOs
[HttpGet("{id}")]
public async Task<UserDto> GetUser(Guid id)
{
    var query = new GetUserQuery(id);
    return await _mediator.Send(query);
}
```

## References

- [ASP.NET Core Documentation](https://docs.microsoft.com/aspnet/core)
- [Clean Architecture Template](https://github.com/jasontaylordev/CleanArchitecture)
- [MediatR](https://github.com/jbogard/MediatR)
- [FluentValidation](https://docs.fluentvalidation.net/)
