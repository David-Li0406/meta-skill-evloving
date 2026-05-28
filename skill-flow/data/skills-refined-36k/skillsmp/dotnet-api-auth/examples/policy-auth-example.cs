// Policy-Based Authorization with Custom Requirements
// Complete example for ASP.NET Core Web API

using Microsoft.AspNetCore.Authorization;
using System.Security.Claims;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();

// Configure Authorization with Policies
builder.Services.AddAuthorizationBuilder()
    // Simple role-based policy
    .AddPolicy("AdminOnly", policy =>
        policy.RequireRole("Admin"))

    // Multiple roles (OR condition)
    .AddPolicy("AdminOrManager", policy =>
        policy.RequireRole("Admin", "Manager"))

    // Require specific claim
    .AddPolicy("PremiumUser", policy =>
        policy.RequireClaim("Subscription", "Premium", "Enterprise"))

    // Require authenticated user
    .AddPolicy("AuthenticatedUser", policy =>
        policy.RequireAuthenticatedUser())

    // Custom requirement - Minimum Age
    .AddPolicy("MinimumAge18", policy =>
        policy.Requirements.Add(new MinimumAgeRequirement(18)))

    // Custom requirement - Department Access
    .AddPolicy("EngineeringDepartment", policy =>
        policy.Requirements.Add(new DepartmentRequirement("Engineering")))

    // Combined requirements (AND condition)
    .AddPolicy("SeniorEngineer", policy =>
    {
        policy.RequireRole("Engineer");
        policy.Requirements.Add(new MinimumExperienceRequirement(5));
    });

// Register custom authorization handlers
builder.Services.AddSingleton<IAuthorizationHandler, MinimumAgeHandler>();
builder.Services.AddSingleton<IAuthorizationHandler, DepartmentHandler>();
builder.Services.AddSingleton<IAuthorizationHandler, MinimumExperienceHandler>();
builder.Services.AddScoped<IAuthorizationHandler, DocumentAuthorizationHandler>();

// Register IAuthorizationService for resource-based authorization
builder.Services.AddScoped<IDocumentRepository, DocumentRepository>();

var app = builder.Build();

app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();

app.Run();

// ============================================
// Custom Requirements
// ============================================

/// <summary>
/// Requires user to be at least a certain age
/// </summary>
public class MinimumAgeRequirement : IAuthorizationRequirement
{
    public int MinimumAge { get; }

    public MinimumAgeRequirement(int minimumAge)
    {
        MinimumAge = minimumAge;
    }
}

/// <summary>
/// Requires user to belong to a specific department
/// </summary>
public class DepartmentRequirement : IAuthorizationRequirement
{
    public string Department { get; }

    public DepartmentRequirement(string department)
    {
        Department = department;
    }
}

/// <summary>
/// Requires user to have minimum years of experience
/// </summary>
public class MinimumExperienceRequirement : IAuthorizationRequirement
{
    public int MinimumYears { get; }

    public MinimumExperienceRequirement(int minimumYears)
    {
        MinimumYears = minimumYears;
    }
}

// ============================================
// Authorization Handlers
// ============================================

public class MinimumAgeHandler : AuthorizationHandler<MinimumAgeRequirement>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        MinimumAgeRequirement requirement)
    {
        var dateOfBirthClaim = context.User.FindFirst(c => c.Type == "DateOfBirth");

        if (dateOfBirthClaim == null)
        {
            return Task.CompletedTask; // Requirement not satisfied
        }

        if (DateTime.TryParse(dateOfBirthClaim.Value, out var dateOfBirth))
        {
            var age = DateTime.Today.Year - dateOfBirth.Year;
            if (dateOfBirth.Date > DateTime.Today.AddYears(-age))
            {
                age--;
            }

            if (age >= requirement.MinimumAge)
            {
                context.Succeed(requirement);
            }
        }

        return Task.CompletedTask;
    }
}

public class DepartmentHandler : AuthorizationHandler<DepartmentRequirement>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        DepartmentRequirement requirement)
    {
        var departmentClaim = context.User.FindFirst("department");

        if (departmentClaim != null &&
            departmentClaim.Value.Equals(requirement.Department, StringComparison.OrdinalIgnoreCase))
        {
            context.Succeed(requirement);
        }

        return Task.CompletedTask;
    }
}

public class MinimumExperienceHandler : AuthorizationHandler<MinimumExperienceRequirement>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        MinimumExperienceRequirement requirement)
    {
        var experienceClaim = context.User.FindFirst("YearsOfExperience");

        if (experienceClaim != null &&
            int.TryParse(experienceClaim.Value, out var years) &&
            years >= requirement.MinimumYears)
        {
            context.Succeed(requirement);
        }

        return Task.CompletedTask;
    }
}

// ============================================
// Resource-Based Authorization
// ============================================

public class Document
{
    public int Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;
    public string OwnerId { get; set; } = string.Empty;
    public string Department { get; set; } = string.Empty;
    public bool IsPublic { get; set; }
}

public static class Operations
{
    public static OperationAuthorizationRequirement Create = new() { Name = nameof(Create) };
    public static OperationAuthorizationRequirement Read = new() { Name = nameof(Read) };
    public static OperationAuthorizationRequirement Update = new() { Name = nameof(Update) };
    public static OperationAuthorizationRequirement Delete = new() { Name = nameof(Delete) };
}

public class DocumentAuthorizationHandler :
    AuthorizationHandler<OperationAuthorizationRequirement, Document>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        OperationAuthorizationRequirement requirement,
        Document resource)
    {
        var userId = context.User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
        var userDepartment = context.User.FindFirst("department")?.Value;
        var isAdmin = context.User.IsInRole("Admin");

        // Admins can do anything
        if (isAdmin)
        {
            context.Succeed(requirement);
            return Task.CompletedTask;
        }

        switch (requirement.Name)
        {
            case nameof(Operations.Read):
                // Users can read public documents or documents they own or in their department
                if (resource.IsPublic ||
                    resource.OwnerId == userId ||
                    resource.Department == userDepartment)
                {
                    context.Succeed(requirement);
                }
                break;

            case nameof(Operations.Update):
                // Users can only update their own documents
                if (resource.OwnerId == userId)
                {
                    context.Succeed(requirement);
                }
                break;

            case nameof(Operations.Delete):
                // Users can only delete their own documents
                if (resource.OwnerId == userId)
                {
                    context.Succeed(requirement);
                }
                break;

            case nameof(Operations.Create):
                // Any authenticated user can create
                if (userId != null)
                {
                    context.Succeed(requirement);
                }
                break;
        }

        return Task.CompletedTask;
    }
}

// ============================================
// Controllers Using Policies
// ============================================

[ApiController]
[Route("api/[controller]")]
public class AdminController : ControllerBase
{
    [HttpGet("dashboard")]
    [Authorize(Policy = "AdminOnly")]
    public IActionResult GetDashboard()
    {
        return Ok("Admin dashboard data");
    }

    [HttpGet("reports")]
    [Authorize(Policy = "AdminOrManager")]
    public IActionResult GetReports()
    {
        return Ok("Reports for admins and managers");
    }
}

[ApiController]
[Route("api/[controller]")]
public class PremiumController : ControllerBase
{
    [HttpGet("features")]
    [Authorize(Policy = "PremiumUser")]
    public IActionResult GetPremiumFeatures()
    {
        return Ok("Premium features");
    }

    [HttpGet("age-restricted")]
    [Authorize(Policy = "MinimumAge18")]
    public IActionResult GetAgeRestrictedContent()
    {
        return Ok("Age-restricted content");
    }
}

[ApiController]
[Route("api/[controller]")]
[Authorize]
public class DocumentsController : ControllerBase
{
    private readonly IAuthorizationService _authorizationService;
    private readonly IDocumentRepository _repository;

    public DocumentsController(
        IAuthorizationService authorizationService,
        IDocumentRepository repository)
    {
        _authorizationService = authorizationService;
        _repository = repository;
    }

    [HttpGet("{id}")]
    public async Task<IActionResult> Get(int id)
    {
        var document = await _repository.GetByIdAsync(id);
        if (document == null)
            return NotFound();

        var authResult = await _authorizationService.AuthorizeAsync(
            User, document, Operations.Read);

        if (!authResult.Succeeded)
            return Forbid();

        return Ok(document);
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> Update(int id, [FromBody] DocumentUpdateRequest request)
    {
        var document = await _repository.GetByIdAsync(id);
        if (document == null)
            return NotFound();

        var authResult = await _authorizationService.AuthorizeAsync(
            User, document, Operations.Update);

        if (!authResult.Succeeded)
            return Forbid();

        document.Title = request.Title;
        document.Content = request.Content;
        await _repository.UpdateAsync(document);

        return Ok(document);
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        var document = await _repository.GetByIdAsync(id);
        if (document == null)
            return NotFound();

        var authResult = await _authorizationService.AuthorizeAsync(
            User, document, Operations.Delete);

        if (!authResult.Succeeded)
            return Forbid();

        await _repository.DeleteAsync(id);
        return NoContent();
    }

    [HttpPost]
    public async Task<IActionResult> Create([FromBody] DocumentCreateRequest request)
    {
        var document = new Document
        {
            Title = request.Title,
            Content = request.Content,
            OwnerId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value!,
            Department = User.FindFirst("department")?.Value ?? "",
            IsPublic = request.IsPublic
        };

        var authResult = await _authorizationService.AuthorizeAsync(
            User, document, Operations.Create);

        if (!authResult.Succeeded)
            return Forbid();

        var created = await _repository.CreateAsync(document);
        return CreatedAtAction(nameof(Get), new { id = created.Id }, created);
    }
}

public record DocumentCreateRequest(string Title, string Content, bool IsPublic);
public record DocumentUpdateRequest(string Title, string Content);

// Repository Interface
public interface IDocumentRepository
{
    Task<Document?> GetByIdAsync(int id);
    Task<Document> CreateAsync(Document document);
    Task UpdateAsync(Document document);
    Task DeleteAsync(int id);
}

// Simple in-memory implementation for demonstration
public class DocumentRepository : IDocumentRepository
{
    private readonly List<Document> _documents = new();
    private int _nextId = 1;

    public Task<Document?> GetByIdAsync(int id)
    {
        return Task.FromResult(_documents.FirstOrDefault(d => d.Id == id));
    }

    public Task<Document> CreateAsync(Document document)
    {
        document.Id = _nextId++;
        _documents.Add(document);
        return Task.FromResult(document);
    }

    public Task UpdateAsync(Document document)
    {
        var index = _documents.FindIndex(d => d.Id == document.Id);
        if (index >= 0)
            _documents[index] = document;
        return Task.CompletedTask;
    }

    public Task DeleteAsync(int id)
    {
        _documents.RemoveAll(d => d.Id == id);
        return Task.CompletedTask;
    }
}
