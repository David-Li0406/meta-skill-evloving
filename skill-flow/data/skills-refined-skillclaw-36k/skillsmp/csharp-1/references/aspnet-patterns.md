# ASP.NET Core Best Practices

## Dependency Injection

### Service Registration

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// Transient: New instance every time
builder.Services.AddTransient<IEmailSender, SmtpEmailSender>();

// Scoped: One instance per request
builder.Services.AddScoped<IUserRepository, UserRepository>();
builder.Services.AddScoped<IUserService, UserService>();

// Singleton: One instance for app lifetime
builder.Services.AddSingleton<ICacheService, MemoryCacheService>();

// With factory
builder.Services.AddScoped<IDbConnection>(sp =>
{
    var config = sp.GetRequiredService<IConfiguration>();
    return new NpgsqlConnection(config.GetConnectionString("Default"));
});

// Options pattern
builder.Services.Configure<EmailOptions>(
    builder.Configuration.GetSection("Email"));
```

### Constructor Injection

```csharp
public class UserService : IUserService
{
    private readonly IUserRepository _userRepository;
    private readonly ILogger<UserService> _logger;
    private readonly IOptions<UserOptions> _options;

    public UserService(
        IUserRepository userRepository,
        ILogger<UserService> logger,
        IOptions<UserOptions> options)
    {
        _userRepository = userRepository;
        _logger = logger;
        _options = options;
    }
}
```

## Controller Patterns

### Minimal APIs (Preferred for Simple Endpoints)

```csharp
var app = builder.Build();

app.MapGet("/users/{id:int}", async (
    int id,
    IUserService userService,
    CancellationToken ct) =>
{
    var user = await userService.GetByIdAsync(id, ct);
    return user is null
        ? Results.NotFound()
        : Results.Ok(user);
});

app.MapPost("/users", async (
    CreateUserRequest request,
    IUserService userService,
    IValidator<CreateUserRequest> validator,
    CancellationToken ct) =>
{
    var validation = await validator.ValidateAsync(request, ct);
    if (!validation.IsValid)
        return Results.ValidationProblem(validation.ToDictionary());

    var user = await userService.CreateAsync(request, ct);
    return Results.Created($"/users/{user.Id}", user);
});

// Group related endpoints
var users = app.MapGroup("/api/users")
    .WithTags("Users")
    .RequireAuthorization();

users.MapGet("/", GetUsers);
users.MapGet("/{id}", GetUser);
users.MapPost("/", CreateUser);
```

### Controllers (For Complex Scenarios)

```csharp
[ApiController]
[Route("api/[controller]")]
[Produces("application/json")]
public class UsersController : ControllerBase
{
    private readonly IUserService _userService;
    private readonly ILogger<UsersController> _logger;

    public UsersController(
        IUserService userService,
        ILogger<UsersController> logger)
    {
        _userService = userService;
        _logger = logger;
    }

    [HttpGet("{id:int}")]
    [ProducesResponseType(typeof(UserResponse), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetUser(
        int id,
        CancellationToken ct)
    {
        var user = await _userService.GetByIdAsync(id, ct);
        return user is null ? NotFound() : Ok(user);
    }

    [HttpPost]
    [ProducesResponseType(typeof(UserResponse), StatusCodes.Status201Created)]
    [ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> CreateUser(
        [FromBody] CreateUserRequest request,
        CancellationToken ct)
    {
        var user = await _userService.CreateAsync(request, ct);
        return CreatedAtAction(nameof(GetUser), new { id = user.Id }, user);
    }
}
```

## Async Patterns

### Async All the Way

```csharp
// ✅ Async throughout the stack
public async Task<User?> GetUserAsync(int id, CancellationToken ct = default)
{
    return await _context.Users
        .FirstOrDefaultAsync(u => u.Id == id, ct);
}

// ✅ Use CancellationToken
public async Task ProcessAsync(CancellationToken ct)
{
    await foreach (var item in GetItemsAsync(ct))
    {
        ct.ThrowIfCancellationRequested();
        await ProcessItemAsync(item, ct);
    }
}

// ❌ Don't block on async
public User GetUser(int id)
{
    // Deadlock risk!
    return GetUserAsync(id).Result;
}

// ✅ Parallel async operations
public async Task<(User user, List<Order> orders)> GetUserWithOrdersAsync(
    int userId,
    CancellationToken ct)
{
    var userTask = _userService.GetByIdAsync(userId, ct);
    var ordersTask = _orderService.GetByUserIdAsync(userId, ct);

    await Task.WhenAll(userTask, ordersTask);

    return (userTask.Result, ordersTask.Result);
}
```

### ConfigureAwait in Libraries

```csharp
// In library code, use ConfigureAwait(false)
public class ExternalApiClient
{
    public async Task<Response> GetAsync(string url, CancellationToken ct)
    {
        var response = await _httpClient.GetAsync(url, ct)
            .ConfigureAwait(false);

        var content = await response.Content.ReadAsStringAsync(ct)
            .ConfigureAwait(false);

        return JsonSerializer.Deserialize<Response>(content);
    }
}
```

## Validation

### FluentValidation

```csharp
public class CreateUserRequestValidator : AbstractValidator<CreateUserRequest>
{
    private readonly IUserRepository _userRepository;

    public CreateUserRequestValidator(IUserRepository userRepository)
    {
        _userRepository = userRepository;

        RuleFor(x => x.Name)
            .NotEmpty()
            .MaximumLength(100);

        RuleFor(x => x.Email)
            .NotEmpty()
            .EmailAddress()
            .MustAsync(BeUniqueEmail)
            .WithMessage("Email already exists");

        RuleFor(x => x.Age)
            .InclusiveBetween(0, 150);
    }

    private async Task<bool> BeUniqueEmail(
        string email,
        CancellationToken ct)
    {
        return !await _userRepository.ExistsByEmailAsync(email, ct);
    }
}

// Registration
builder.Services.AddValidatorsFromAssemblyContaining<CreateUserRequestValidator>();
```

### Data Annotations

```csharp
public record CreateUserRequest(
    [Required]
    [StringLength(100, MinimumLength = 2)]
    string Name,

    [Required]
    [EmailAddress]
    string Email,

    [Range(0, 150)]
    int? Age
);
```

## Error Handling

### Global Exception Handler

```csharp
public class GlobalExceptionHandler : IExceptionHandler
{
    private readonly ILogger<GlobalExceptionHandler> _logger;

    public GlobalExceptionHandler(ILogger<GlobalExceptionHandler> logger)
    {
        _logger = logger;
    }

    public async ValueTask<bool> TryHandleAsync(
        HttpContext httpContext,
        Exception exception,
        CancellationToken ct)
    {
        var (statusCode, title) = exception switch
        {
            NotFoundException => (StatusCodes.Status404NotFound, "Not Found"),
            ValidationException => (StatusCodes.Status400BadRequest, "Validation Error"),
            UnauthorizedAccessException => (StatusCodes.Status401Unauthorized, "Unauthorized"),
            _ => (StatusCodes.Status500InternalServerError, "Server Error")
        };

        _logger.LogError(exception, "Exception occurred: {Message}", exception.Message);

        var problem = new ProblemDetails
        {
            Status = statusCode,
            Title = title,
            Detail = exception.Message,
            Instance = httpContext.Request.Path
        };

        httpContext.Response.StatusCode = statusCode;
        await httpContext.Response.WriteAsJsonAsync(problem, ct);

        return true;
    }
}

// Registration
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();
builder.Services.AddProblemDetails();

var app = builder.Build();
app.UseExceptionHandler();
```

## Configuration

### Options Pattern

```csharp
public record EmailOptions
{
    public const string SectionName = "Email";

    public required string Host { get; init; }
    public int Port { get; init; } = 587;
    public required string Username { get; init; }
    public required string Password { get; init; }
    public TimeSpan Timeout { get; init; } = TimeSpan.FromSeconds(30);
}

// Registration with validation
builder.Services.AddOptions<EmailOptions>()
    .BindConfiguration(EmailOptions.SectionName)
    .ValidateDataAnnotations()
    .ValidateOnStart();

// Usage
public class EmailService
{
    private readonly EmailOptions _options;

    public EmailService(IOptions<EmailOptions> options)
    {
        _options = options.Value;
    }
}
```

### appsettings.json Structure

```json
{
  "Email": {
    "Host": "smtp.example.com",
    "Port": 587,
    "Username": "user@example.com",
    "Password": "from-secrets",
    "Timeout": "00:00:30"
  },
  "ConnectionStrings": {
    "Default": "Host=localhost;Database=app"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  }
}
```

## Middleware

### Custom Middleware

```csharp
public class RequestLoggingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestLoggingMiddleware> _logger;

    public RequestLoggingMiddleware(
        RequestDelegate next,
        ILogger<RequestLoggingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        var sw = Stopwatch.StartNew();

        try
        {
            await _next(context);
        }
        finally
        {
            sw.Stop();
            _logger.LogInformation(
                "{Method} {Path} responded {StatusCode} in {Elapsed}ms",
                context.Request.Method,
                context.Request.Path,
                context.Response.StatusCode,
                sw.ElapsedMilliseconds);
        }
    }
}

// Registration
app.UseMiddleware<RequestLoggingMiddleware>();

// Or as extension
public static class MiddlewareExtensions
{
    public static IApplicationBuilder UseRequestLogging(
        this IApplicationBuilder builder)
    {
        return builder.UseMiddleware<RequestLoggingMiddleware>();
    }
}
```

## Health Checks

```csharp
builder.Services.AddHealthChecks()
    .AddNpgSql(connectionString, name: "database")
    .AddRedis(redisConnectionString, name: "redis")
    .AddUrlGroup(new Uri("https://api.example.com/health"), name: "external-api");

var app = builder.Build();

app.MapHealthChecks("/health", new HealthCheckOptions
{
    ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
});

app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});

app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = _ => false  // Just checks if app responds
});
```
