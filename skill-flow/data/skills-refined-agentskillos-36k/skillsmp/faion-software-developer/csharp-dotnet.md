# C# .NET Core Backend Development

**C# backend patterns for production-grade applications with ASP.NET Core and Entity Framework.**

---

## ASP.NET Core Patterns

### Problem
Structure ASP.NET Core applications with clean architecture.

### Framework: Controller Structure

```csharp
// Controllers/UsersController.cs

using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;

namespace MyApp.Controllers;

[ApiController]
[Route("api/v1/[controller]")]
[Authorize]
public class UsersController : ControllerBase
{
    private readonly IUserService _userService;
    private readonly ILogger<UsersController> _logger;

    public UsersController(IUserService userService, ILogger<UsersController> logger)
    {
        _userService = userService;
        _logger = logger;
    }

    [HttpGet]
    public async Task<ActionResult<PagedResult<UserDto>>> GetUsers(
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 20)
    {
        var result = await _userService.GetAllAsync(page, pageSize);
        return Ok(result);
    }

    [HttpGet("{id:int}")]
    public async Task<ActionResult<UserDto>> GetUser(int id)
    {
        var user = await _userService.GetByIdAsync(id);
        if (user == null)
            return NotFound();
        return Ok(user);
    }

    [HttpPost]
    public async Task<ActionResult<UserDto>> CreateUser(CreateUserDto dto)
    {
        var user = await _userService.CreateAsync(dto);
        return CreatedAtAction(nameof(GetUser), new { id = user.Id }, user);
    }

    [HttpPut("{id:int}")]
    public async Task<ActionResult<UserDto>> UpdateUser(int id, UpdateUserDto dto)
    {
        var user = await _userService.UpdateAsync(id, dto);
        if (user == null)
            return NotFound();
        return Ok(user);
    }

    [HttpDelete("{id:int}")]
    public async Task<IActionResult> DeleteUser(int id)
    {
        var success = await _userService.DeleteAsync(id);
        if (!success)
            return NotFound();
        return NoContent();
    }
}
```

### Service Layer

```csharp
// Services/UserService.cs

namespace MyApp.Services;

public interface IUserService
{
    Task<PagedResult<UserDto>> GetAllAsync(int page, int pageSize);
    Task<UserDto?> GetByIdAsync(int id);
    Task<UserDto> CreateAsync(CreateUserDto dto);
    Task<UserDto?> UpdateAsync(int id, UpdateUserDto dto);
    Task<bool> DeleteAsync(int id);
}

public class UserService : IUserService
{
    private readonly IUserRepository _repository;
    private readonly IMapper _mapper;
    private readonly IPasswordHasher<User> _passwordHasher;

    public UserService(
        IUserRepository repository,
        IMapper mapper,
        IPasswordHasher<User> passwordHasher)
    {
        _repository = repository;
        _mapper = mapper;
        _passwordHasher = passwordHasher;
    }

    public async Task<PagedResult<UserDto>> GetAllAsync(int page, int pageSize)
    {
        var users = await _repository.GetPagedAsync(page, pageSize);
        return _mapper.Map<PagedResult<UserDto>>(users);
    }

    public async Task<UserDto?> GetByIdAsync(int id)
    {
        var user = await _repository.GetByIdAsync(id);
        return user == null ? null : _mapper.Map<UserDto>(user);
    }

    public async Task<UserDto> CreateAsync(CreateUserDto dto)
    {
        var user = _mapper.Map<User>(dto);
        user.PasswordHash = _passwordHasher.HashPassword(user, dto.Password);

        await _repository.AddAsync(user);
        await _repository.SaveChangesAsync();

        return _mapper.Map<UserDto>(user);
    }

    public async Task<UserDto?> UpdateAsync(int id, UpdateUserDto dto)
    {
        var user = await _repository.GetByIdAsync(id);
        if (user == null)
            return null;

        _mapper.Map(dto, user);
        await _repository.SaveChangesAsync();

        return _mapper.Map<UserDto>(user);
    }

    public async Task<bool> DeleteAsync(int id)
    {
        var user = await _repository.GetByIdAsync(id);
        if (user == null)
            return false;

        _repository.Remove(user);
        await _repository.SaveChangesAsync();
        return true;
    }
}
```

---

## Entity Framework Patterns

### Problem
Efficient database access with EF Core.

### Framework: Entity Configuration

```csharp
// Entities/User.cs

namespace MyApp.Entities;

public class User
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string PasswordHash { get; set; } = string.Empty;
    public bool IsActive { get; set; } = true;
    public DateTime CreatedAt { get; set; }
    public DateTime? UpdatedAt { get; set; }

    // Navigation properties
    public ICollection<Role> Roles { get; set; } = new List<Role>();
    public ICollection<Order> Orders { get; set; } = new List<Order>();
}

// Data/Configurations/UserConfiguration.cs

using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace MyApp.Data.Configurations;

public class UserConfiguration : IEntityTypeConfiguration<User>
{
    public void Configure(EntityTypeBuilder<User> builder)
    {
        builder.ToTable("users");

        builder.HasKey(u => u.Id);

        builder.Property(u => u.Name)
            .IsRequired()
            .HasMaxLength(100);

        builder.Property(u => u.Email)
            .IsRequired()
            .HasMaxLength(255);

        builder.HasIndex(u => u.Email)
            .IsUnique();

        builder.Property(u => u.CreatedAt)
            .HasDefaultValueSql("CURRENT_TIMESTAMP");

        builder.HasMany(u => u.Roles)
            .WithMany(r => r.Users)
            .UsingEntity<Dictionary<string, object>>(
                "user_roles",
                j => j.HasOne<Role>().WithMany().HasForeignKey("RoleId"),
                j => j.HasOne<User>().WithMany().HasForeignKey("UserId")
            );

        builder.HasMany(u => u.Orders)
            .WithOne(o => o.User)
            .HasForeignKey(o => o.UserId)
            .OnDelete(DeleteBehavior.SetNull);
    }
}
```

### Repository Pattern

```csharp
// Repositories/UserRepository.cs

namespace MyApp.Repositories;

public interface IUserRepository
{
    Task<User?> GetByIdAsync(int id);
    Task<User?> GetByEmailAsync(string email);
    Task<PagedResult<User>> GetPagedAsync(int page, int pageSize);
    Task AddAsync(User user);
    void Remove(User user);
    Task SaveChangesAsync();
}

public class UserRepository : IUserRepository
{
    private readonly AppDbContext _context;

    public UserRepository(AppDbContext context)
    {
        _context = context;
    }

    public async Task<User?> GetByIdAsync(int id)
    {
        return await _context.Users
            .Include(u => u.Roles)
            .FirstOrDefaultAsync(u => u.Id == id);
    }

    public async Task<User?> GetByEmailAsync(string email)
    {
        return await _context.Users
            .FirstOrDefaultAsync(u => u.Email == email.ToLower());
    }

    public async Task<PagedResult<User>> GetPagedAsync(int page, int pageSize)
    {
        var query = _context.Users
            .AsNoTracking()
            .OrderByDescending(u => u.CreatedAt);

        var totalCount = await query.CountAsync();
        var items = await query
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync();

        return new PagedResult<User>(items, totalCount, page, pageSize);
    }

    public async Task AddAsync(User user)
    {
        await _context.Users.AddAsync(user);
    }

    public void Remove(User user)
    {
        _context.Users.Remove(user);
    }

    public async Task SaveChangesAsync()
    {
        await _context.SaveChangesAsync();
    }
}
```

---

## xUnit Testing

### Problem
Write comprehensive tests for .NET applications.

### Framework: Controller Tests

```csharp
// Tests/Controllers/UsersControllerTests.cs

using Microsoft.AspNetCore.Mvc;
using Moq;
using Xunit;

namespace MyApp.Tests.Controllers;

public class UsersControllerTests
{
    private readonly Mock<IUserService> _mockService;
    private readonly UsersController _controller;

    public UsersControllerTests()
    {
        _mockService = new Mock<IUserService>();
        _controller = new UsersController(
            _mockService.Object,
            Mock.Of<ILogger<UsersController>>()
        );
    }

    [Fact]
    public async Task GetUser_WhenUserExists_ReturnsOkWithUser()
    {
        // Arrange
        var userDto = new UserDto { Id = 1, Name = "John", Email = "john@example.com" };
        _mockService.Setup(s => s.GetByIdAsync(1))
            .ReturnsAsync(userDto);

        // Act
        var result = await _controller.GetUser(1);

        // Assert
        var okResult = Assert.IsType<OkObjectResult>(result.Result);
        var returnedUser = Assert.IsType<UserDto>(okResult.Value);
        Assert.Equal(1, returnedUser.Id);
        Assert.Equal("John", returnedUser.Name);
    }

    [Fact]
    public async Task GetUser_WhenUserNotFound_ReturnsNotFound()
    {
        // Arrange
        _mockService.Setup(s => s.GetByIdAsync(999))
            .ReturnsAsync((UserDto?)null);

        // Act
        var result = await _controller.GetUser(999);

        // Assert
        Assert.IsType<NotFoundResult>(result.Result);
    }

    [Fact]
    public async Task CreateUser_WithValidData_ReturnsCreatedAtAction()
    {
        // Arrange
        var createDto = new CreateUserDto
        {
            Name = "John",
            Email = "john@example.com",
            Password = "password123"
        };
        var userDto = new UserDto { Id = 1, Name = "John", Email = "john@example.com" };

        _mockService.Setup(s => s.CreateAsync(createDto))
            .ReturnsAsync(userDto);

        // Act
        var result = await _controller.CreateUser(createDto);

        // Assert
        var createdResult = Assert.IsType<CreatedAtActionResult>(result.Result);
        Assert.Equal(nameof(UsersController.GetUser), createdResult.ActionName);
        Assert.Equal(1, createdResult.RouteValues?["id"]);
    }
}
```

### Integration Tests

```csharp
// Tests/Integration/UsersApiTests.cs

using Microsoft.AspNetCore.Mvc.Testing;
using System.Net.Http.Json;
using Xunit;

namespace MyApp.Tests.Integration;

public class UsersApiTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public UsersApiTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task GetUsers_ReturnsSuccessAndCorrectContentType()
    {
        // Act
        var response = await _client.GetAsync("/api/v1/users");

        // Assert
        response.EnsureSuccessStatusCode();
        Assert.Equal("application/json; charset=utf-8",
            response.Content.Headers.ContentType?.ToString());
    }

    [Fact]
    public async Task CreateUser_WithValidData_ReturnsCreated()
    {
        // Arrange
        var createDto = new CreateUserDto
        {
            Name = "Test User",
            Email = "test@example.com",
            Password = "password123"
        };

        // Act
        var response = await _client.PostAsJsonAsync("/api/v1/users", createDto);

        // Assert
        Assert.Equal(HttpStatusCode.Created, response.StatusCode);

        var user = await response.Content.ReadFromJsonAsync<UserDto>();
        Assert.NotNull(user);
        Assert.Equal("Test User", user.Name);
    }
}
```

---

## Background Services

### Problem
Process background tasks in ASP.NET Core.

### Framework: Hosted Service

```csharp
// Services/BackgroundOrderProcessor.cs

namespace MyApp.Services;

public class BackgroundOrderProcessor : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<BackgroundOrderProcessor> _logger;
    private readonly Channel<int> _orderChannel;

    public BackgroundOrderProcessor(
        IServiceProvider serviceProvider,
        ILogger<BackgroundOrderProcessor> logger,
        Channel<int> orderChannel)
    {
        _serviceProvider = serviceProvider;
        _logger = logger;
        _orderChannel = orderChannel;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("Order processor started");

        await foreach (var orderId in _orderChannel.Reader.ReadAllAsync(stoppingToken))
        {
            try
            {
                await ProcessOrderAsync(orderId, stoppingToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing order {OrderId}", orderId);
            }
        }
    }

    private async Task ProcessOrderAsync(int orderId, CancellationToken ct)
    {
        using var scope = _serviceProvider.CreateScope();
        var orderService = scope.ServiceProvider.GetRequiredService<IOrderService>();

        _logger.LogInformation("Processing order {OrderId}", orderId);
        await orderService.ProcessAsync(orderId, ct);
        _logger.LogInformation("Order {OrderId} processed", orderId);
    }
}

// Queue service
public interface IOrderQueue
{
    ValueTask QueueOrderAsync(int orderId);
}

public class OrderQueue : IOrderQueue
{
    private readonly Channel<int> _channel;

    public OrderQueue(Channel<int> channel)
    {
        _channel = channel;
    }

    public async ValueTask QueueOrderAsync(int orderId)
    {
        await _channel.Writer.WriteAsync(orderId);
    }
}
```

### Timed Background Service

```csharp
// Services/CleanupService.cs

namespace MyApp.Services;

public class CleanupService : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<CleanupService> _logger;
    private readonly TimeSpan _period = TimeSpan.FromHours(1);

    public CleanupService(
        IServiceProvider serviceProvider,
        ILogger<CleanupService> logger)
    {
        _serviceProvider = serviceProvider;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        using var timer = new PeriodicTimer(_period);

        while (!stoppingToken.IsCancellationRequested &&
               await timer.WaitForNextTickAsync(stoppingToken))
        {
            try
            {
                await DoCleanupAsync(stoppingToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error during cleanup");
            }
        }
    }

    private async Task DoCleanupAsync(CancellationToken ct)
    {
        using var scope = _serviceProvider.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();

        var cutoff = DateTime.UtcNow.AddDays(-30);

        var deleted = await context.AuditLogs
            .Where(a => a.CreatedAt < cutoff)
            .ExecuteDeleteAsync(ct);

        _logger.LogInformation("Deleted {Count} old audit logs", deleted);
    }
}
```

---

## Sources

- [ASP.NET Core Documentation](https://docs.microsoft.com/en-us/aspnet/core/)
- [Entity Framework Core](https://docs.microsoft.com/en-us/ef/core/)
