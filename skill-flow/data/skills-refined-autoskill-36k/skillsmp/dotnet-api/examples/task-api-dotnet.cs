// =============================================================================
// Task Management API - .NET Implementation
// =============================================================================
// This example implements the Task Management API from the api-design skill's
// task-management-api.yaml specification. It demonstrates both Minimal API and
// Controller approaches in a single file for comparison.
// =============================================================================

using Asp.Versioning;
using FluentValidation;
using Microsoft.AspNetCore.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using Microsoft.OpenApi.Models;
using System.Collections.Concurrent;

var builder = WebApplication.CreateBuilder(args);

// -----------------------------------------------------------------------------
// Service Registration
// -----------------------------------------------------------------------------

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "Task Management API",
        Version = "v1",
        Description = "API for managing tasks with full CRUD operations"
    });
});

builder.Services.AddProblemDetails(options =>
{
    options.CustomizeProblemDetails = context =>
    {
        context.ProblemDetails.Extensions["traceId"] = context.HttpContext.TraceIdentifier;
        context.ProblemDetails.Instance = context.HttpContext.Request.Path;
    };
});

builder.Services.AddValidatorsFromAssemblyContaining<Program>();
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();

// Health checks
builder.Services.AddHealthChecks()
    .AddCheck("self", () => Microsoft.Extensions.Diagnostics.HealthChecks.HealthCheckResult.Healthy(),
        tags: new[] { "live" });

// Output caching
builder.Services.AddOutputCache(options =>
{
    options.AddPolicy("Tasks", b => b.Expire(TimeSpan.FromMinutes(5)).Tag("tasks"));
});

// Register in-memory repository (replace with real implementation)
builder.Services.AddSingleton<ITaskRepository, InMemoryTaskRepository>();

// API Versioning
builder.Services.AddApiVersioning(options =>
{
    options.DefaultApiVersion = new ApiVersion(1, 0);
    options.AssumeDefaultVersionWhenUnspecified = true;
    options.ReportApiVersions = true;
    options.ApiVersionReader = ApiVersionReader.Combine(
        new UrlSegmentApiVersionReader(),
        new HeaderApiVersionReader("X-Api-Version"));
});

var app = builder.Build();

// -----------------------------------------------------------------------------
// Middleware Pipeline
// -----------------------------------------------------------------------------

app.UseExceptionHandler();
app.UseOutputCache();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

// Health checks
app.MapHealthChecks("/health/live");
app.MapHealthChecks("/health/ready");

// =============================================================================
// APPROACH 1: Minimal API Implementation
// =============================================================================

var api = app.MapGroup("/api/v1/tasks")
    .WithTags("Tasks (Minimal API)")
    .WithOpenApi();

// GET /api/v1/tasks - List all tasks with filtering
api.MapGet("/", async (
    [FromQuery] TaskStatus? status,
    [FromQuery] TaskPriority? priority,
    [FromQuery] int page = 1,
    [FromQuery] int pageSize = 10,
    [FromServices] ITaskRepository repository,
    CancellationToken cancellationToken) =>
{
    var tasks = await repository.GetAllAsync(status, priority, page, pageSize, cancellationToken);
    var totalCount = await repository.GetCountAsync(status, priority, cancellationToken);

    return Results.Ok(new PagedResult<TaskItem>
    {
        Data = tasks,
        Page = page,
        PageSize = pageSize,
        TotalCount = totalCount
    });
})
.WithName("GetTasks")
.Produces<PagedResult<TaskItem>>(StatusCodes.Status200OK)
.CacheOutput("Tasks");

// GET /api/v1/tasks/{id} - Get a specific task
api.MapGet("/{id:guid}", async (
    Guid id,
    ITaskRepository repository,
    CancellationToken cancellationToken) =>
{
    var task = await repository.GetByIdAsync(id, cancellationToken);

    return task is null
        ? Results.Problem(
            title: "Task not found",
            detail: $"No task found with ID {id}",
            statusCode: StatusCodes.Status404NotFound)
        : Results.Ok(task);
})
.WithName("GetTaskById")
.Produces<TaskItem>(StatusCodes.Status200OK)
.Produces<ProblemDetails>(StatusCodes.Status404NotFound);

// POST /api/v1/tasks - Create a new task
api.MapPost("/", async (
    CreateTaskRequest request,
    IValidator<CreateTaskRequest> validator,
    ITaskRepository repository,
    IOutputCacheStore cacheStore,
    CancellationToken cancellationToken) =>
{
    var validationResult = await validator.ValidateAsync(request, cancellationToken);
    if (!validationResult.IsValid)
    {
        return Results.ValidationProblem(validationResult.ToDictionary());
    }

    var task = new TaskItem
    {
        Id = Guid.NewGuid(),
        Title = request.Title,
        Description = request.Description,
        Status = TaskStatus.Pending,
        Priority = request.Priority,
        DueDate = request.DueDate,
        CreatedAt = DateTime.UtcNow,
        UpdatedAt = DateTime.UtcNow
    };

    await repository.CreateAsync(task, cancellationToken);
    await cacheStore.EvictByTagAsync("tasks", cancellationToken);

    return Results.Created($"/api/v1/tasks/{task.Id}", task);
})
.WithName("CreateTask")
.Produces<TaskItem>(StatusCodes.Status201Created)
.Produces<ValidationProblemDetails>(StatusCodes.Status400BadRequest);

// PUT /api/v1/tasks/{id} - Update a task
api.MapPut("/{id:guid}", async (
    Guid id,
    UpdateTaskRequest request,
    IValidator<UpdateTaskRequest> validator,
    ITaskRepository repository,
    IOutputCacheStore cacheStore,
    CancellationToken cancellationToken) =>
{
    var validationResult = await validator.ValidateAsync(request, cancellationToken);
    if (!validationResult.IsValid)
    {
        return Results.ValidationProblem(validationResult.ToDictionary());
    }

    var existing = await repository.GetByIdAsync(id, cancellationToken);
    if (existing is null)
    {
        return Results.Problem(
            title: "Task not found",
            detail: $"No task found with ID {id}",
            statusCode: StatusCodes.Status404NotFound);
    }

    existing.Title = request.Title ?? existing.Title;
    existing.Description = request.Description ?? existing.Description;
    existing.Status = request.Status ?? existing.Status;
    existing.Priority = request.Priority ?? existing.Priority;
    existing.DueDate = request.DueDate ?? existing.DueDate;
    existing.UpdatedAt = DateTime.UtcNow;

    await repository.UpdateAsync(existing, cancellationToken);
    await cacheStore.EvictByTagAsync("tasks", cancellationToken);

    return Results.Ok(existing);
})
.WithName("UpdateTask")
.Produces<TaskItem>(StatusCodes.Status200OK)
.Produces<ProblemDetails>(StatusCodes.Status404NotFound)
.Produces<ValidationProblemDetails>(StatusCodes.Status400BadRequest);

// PATCH /api/v1/tasks/{id}/status - Update task status only
api.MapPatch("/{id:guid}/status", async (
    Guid id,
    UpdateStatusRequest request,
    ITaskRepository repository,
    IOutputCacheStore cacheStore,
    CancellationToken cancellationToken) =>
{
    var task = await repository.GetByIdAsync(id, cancellationToken);
    if (task is null)
    {
        return Results.Problem(
            title: "Task not found",
            detail: $"No task found with ID {id}",
            statusCode: StatusCodes.Status404NotFound);
    }

    task.Status = request.Status;
    task.UpdatedAt = DateTime.UtcNow;

    await repository.UpdateAsync(task, cancellationToken);
    await cacheStore.EvictByTagAsync("tasks", cancellationToken);

    return Results.Ok(task);
})
.WithName("UpdateTaskStatus")
.Produces<TaskItem>(StatusCodes.Status200OK)
.Produces<ProblemDetails>(StatusCodes.Status404NotFound);

// DELETE /api/v1/tasks/{id} - Delete a task
api.MapDelete("/{id:guid}", async (
    Guid id,
    ITaskRepository repository,
    IOutputCacheStore cacheStore,
    CancellationToken cancellationToken) =>
{
    var existing = await repository.GetByIdAsync(id, cancellationToken);
    if (existing is null)
    {
        return Results.Problem(
            title: "Task not found",
            detail: $"No task found with ID {id}",
            statusCode: StatusCodes.Status404NotFound);
    }

    await repository.DeleteAsync(id, cancellationToken);
    await cacheStore.EvictByTagAsync("tasks", cancellationToken);

    return Results.NoContent();
})
.WithName("DeleteTask")
.Produces(StatusCodes.Status204NoContent)
.Produces<ProblemDetails>(StatusCodes.Status404NotFound);

app.Run();

// =============================================================================
// APPROACH 2: Controller Implementation (Alternative)
// =============================================================================
// See task-api-controller-dotnet.cs for the full controller-based implementation
// of this same API. Add builder.Services.AddControllers() and app.MapControllers()
// to use controllers instead of or alongside Minimal APIs.
// =============================================================================

// =============================================================================
// Domain Models
// =============================================================================

public class TaskItem
{
    public Guid Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public string? Description { get; set; }
    public TaskStatus Status { get; set; }
    public TaskPriority Priority { get; set; }
    public DateTime? DueDate { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
}

public enum TaskStatus
{
    Pending,
    InProgress,
    Completed,
    Cancelled
}

public enum TaskPriority
{
    Low,
    Medium,
    High,
    Critical
}

// =============================================================================
// Request/Response Models
// =============================================================================

public record CreateTaskRequest
{
    public string Title { get; init; } = string.Empty;
    public string? Description { get; init; }
    public TaskPriority Priority { get; init; } = TaskPriority.Medium;
    public DateTime? DueDate { get; init; }
}

public record UpdateTaskRequest
{
    public string? Title { get; init; }
    public string? Description { get; init; }
    public TaskStatus? Status { get; init; }
    public TaskPriority? Priority { get; init; }
    public DateTime? DueDate { get; init; }
}

public record UpdateStatusRequest
{
    public TaskStatus Status { get; init; }
}

public class PagedResult<T>
{
    public IEnumerable<T> Data { get; init; } = Enumerable.Empty<T>();
    public int Page { get; init; }
    public int PageSize { get; init; }
    public int TotalCount { get; init; }
    public int TotalPages => (int)Math.Ceiling((double)TotalCount / PageSize);
    public bool HasNextPage => Page < TotalPages;
    public bool HasPreviousPage => Page > 1;
}

// =============================================================================
// Validators
// =============================================================================

public class CreateTaskRequestValidator : AbstractValidator<CreateTaskRequest>
{
    public CreateTaskRequestValidator()
    {
        RuleFor(x => x.Title)
            .NotEmpty().WithMessage("Title is required")
            .MaximumLength(200).WithMessage("Title must not exceed 200 characters");

        RuleFor(x => x.Description)
            .MaximumLength(2000).WithMessage("Description must not exceed 2000 characters");

        RuleFor(x => x.Priority)
            .IsInEnum().WithMessage("Invalid priority value");

        RuleFor(x => x.DueDate)
            .GreaterThan(DateTime.UtcNow)
            .When(x => x.DueDate.HasValue)
            .WithMessage("Due date must be in the future");
    }
}

public class UpdateTaskRequestValidator : AbstractValidator<UpdateTaskRequest>
{
    public UpdateTaskRequestValidator()
    {
        RuleFor(x => x.Title)
            .MaximumLength(200).WithMessage("Title must not exceed 200 characters")
            .When(x => x.Title is not null);

        RuleFor(x => x.Description)
            .MaximumLength(2000).WithMessage("Description must not exceed 2000 characters")
            .When(x => x.Description is not null);

        RuleFor(x => x.Status)
            .IsInEnum().WithMessage("Invalid status value")
            .When(x => x.Status.HasValue);

        RuleFor(x => x.Priority)
            .IsInEnum().WithMessage("Invalid priority value")
            .When(x => x.Priority.HasValue);
    }
}

// =============================================================================
// Repository Interface and Implementation
// =============================================================================

public interface ITaskRepository
{
    Task<IEnumerable<TaskItem>> GetAllAsync(
        TaskStatus? status, TaskPriority? priority, int page, int pageSize,
        CancellationToken cancellationToken);
    Task<int> GetCountAsync(TaskStatus? status, TaskPriority? priority, CancellationToken cancellationToken);
    Task<TaskItem?> GetByIdAsync(Guid id, CancellationToken cancellationToken);
    Task CreateAsync(TaskItem task, CancellationToken cancellationToken);
    Task UpdateAsync(TaskItem task, CancellationToken cancellationToken);
    Task DeleteAsync(Guid id, CancellationToken cancellationToken);
}

public class InMemoryTaskRepository : ITaskRepository
{
    private readonly ConcurrentDictionary<Guid, TaskItem> _tasks = new();

    public Task<IEnumerable<TaskItem>> GetAllAsync(
        TaskStatus? status, TaskPriority? priority, int page, int pageSize, CancellationToken ct)
    {
        var query = _tasks.Values.AsQueryable();
        if (status.HasValue) query = query.Where(t => t.Status == status.Value);
        if (priority.HasValue) query = query.Where(t => t.Priority == priority.Value);
        var result = query.OrderByDescending(t => t.CreatedAt)
            .Skip((page - 1) * pageSize).Take(pageSize).ToList();
        return Task.FromResult<IEnumerable<TaskItem>>(result);
    }

    public Task<int> GetCountAsync(TaskStatus? status, TaskPriority? priority, CancellationToken ct)
    {
        var query = _tasks.Values.AsQueryable();
        if (status.HasValue) query = query.Where(t => t.Status == status.Value);
        if (priority.HasValue) query = query.Where(t => t.Priority == priority.Value);
        return Task.FromResult(query.Count());
    }

    public Task<TaskItem?> GetByIdAsync(Guid id, CancellationToken ct)
    {
        _tasks.TryGetValue(id, out var task);
        return Task.FromResult(task);
    }

    public Task CreateAsync(TaskItem task, CancellationToken ct)
    {
        _tasks[task.Id] = task;
        return Task.CompletedTask;
    }

    public Task UpdateAsync(TaskItem task, CancellationToken ct)
    {
        _tasks[task.Id] = task;
        return Task.CompletedTask;
    }

    public Task DeleteAsync(Guid id, CancellationToken ct)
    {
        _tasks.TryRemove(id, out _);
        return Task.CompletedTask;
    }
}

// =============================================================================
// Global Exception Handler
// =============================================================================

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
        CancellationToken cancellationToken)
    {
        _logger.LogError(exception, "An unhandled exception occurred");

        var problemDetails = new ProblemDetails
        {
            Status = StatusCodes.Status500InternalServerError,
            Title = "An error occurred while processing your request",
            Detail = httpContext.RequestServices.GetService<IHostEnvironment>()?.IsDevelopment() == true
                ? exception.Message
                : "Please try again later or contact support if the problem persists."
        };

        httpContext.Response.StatusCode = problemDetails.Status.Value;
        await httpContext.Response.WriteAsJsonAsync(problemDetails, cancellationToken);

        return true;
    }
}

// Make Program accessible for integration tests
public partial class Program { }
