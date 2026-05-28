---
id: csharp-xunit-testing
name: "xUnit Testing"
domain: CSHARP
skill: faion-software-developer
category: "backend"
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

### Agent

faion-backend-agent
