---
id: csharp-aspnet-core
name: "ASP.NET Core Patterns"
domain: CSHARP
skill: faion-software-developer
category: "backend"
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

### Agent

faion-backend-agent
