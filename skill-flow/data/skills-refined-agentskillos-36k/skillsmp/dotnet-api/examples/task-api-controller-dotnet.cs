// =============================================================================
// Task Management API - Controller-Based Implementation
// =============================================================================
// This is the controller-based version of the Task API. For the Minimal API
// version, see task-api-dotnet.cs. This file shows how to implement the same
// API using the traditional controller pattern.
//
// To use: Add builder.Services.AddControllers() and app.MapControllers()
// =============================================================================

using Asp.Versioning;
using FluentValidation;
using Microsoft.AspNetCore.Mvc;

namespace TaskApi.Controllers;

[ApiController]
[Route("api/v2/[controller]")]
[Produces("application/json")]
[ApiVersion("2.0")]
public class TasksController : ControllerBase
{
    private readonly ITaskRepository _repository;
    private readonly IValidator<CreateTaskRequest> _createValidator;
    private readonly IValidator<UpdateTaskRequest> _updateValidator;
    private readonly ILogger<TasksController> _logger;

    public TasksController(
        ITaskRepository repository,
        IValidator<CreateTaskRequest> createValidator,
        IValidator<UpdateTaskRequest> updateValidator,
        ILogger<TasksController> logger)
    {
        _repository = repository;
        _createValidator = createValidator;
        _updateValidator = updateValidator;
        _logger = logger;
    }

    /// <summary>
    /// Get all tasks with optional filtering and pagination
    /// </summary>
    [HttpGet]
    [ProducesResponseType(typeof(PagedResult<TaskItem>), StatusCodes.Status200OK)]
    public async Task<ActionResult<PagedResult<TaskItem>>> GetAll(
        [FromQuery] TaskStatus? status,
        [FromQuery] TaskPriority? priority,
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 10,
        CancellationToken cancellationToken = default)
    {
        var tasks = await _repository.GetAllAsync(status, priority, page, pageSize, cancellationToken);
        var totalCount = await _repository.GetCountAsync(status, priority, cancellationToken);

        return Ok(new PagedResult<TaskItem>
        {
            Data = tasks,
            Page = page,
            PageSize = pageSize,
            TotalCount = totalCount
        });
    }

    /// <summary>
    /// Get a specific task by ID
    /// </summary>
    [HttpGet("{id:guid}")]
    [ProducesResponseType(typeof(TaskItem), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<ActionResult<TaskItem>> GetById(
        Guid id,
        CancellationToken cancellationToken = default)
    {
        var task = await _repository.GetByIdAsync(id, cancellationToken);

        if (task is null)
        {
            return NotFound(new ProblemDetails
            {
                Title = "Task not found",
                Detail = $"No task found with ID {id}",
                Status = StatusCodes.Status404NotFound
            });
        }

        return Ok(task);
    }

    /// <summary>
    /// Create a new task
    /// </summary>
    [HttpPost]
    [ProducesResponseType(typeof(TaskItem), StatusCodes.Status201Created)]
    [ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<TaskItem>> Create(
        [FromBody] CreateTaskRequest request,
        CancellationToken cancellationToken = default)
    {
        var validationResult = await _createValidator.ValidateAsync(request, cancellationToken);
        if (!validationResult.IsValid)
        {
            return ValidationProblem(new ValidationProblemDetails(validationResult.ToDictionary()));
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

        await _repository.CreateAsync(task, cancellationToken);
        _logger.LogInformation("Created task {TaskId}", task.Id);

        return CreatedAtAction(nameof(GetById), new { id = task.Id }, task);
    }

    /// <summary>
    /// Update an existing task
    /// </summary>
    [HttpPut("{id:guid}")]
    [ProducesResponseType(typeof(TaskItem), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    [ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<TaskItem>> Update(
        Guid id,
        [FromBody] UpdateTaskRequest request,
        CancellationToken cancellationToken = default)
    {
        var validationResult = await _updateValidator.ValidateAsync(request, cancellationToken);
        if (!validationResult.IsValid)
        {
            return ValidationProblem(new ValidationProblemDetails(validationResult.ToDictionary()));
        }

        var existing = await _repository.GetByIdAsync(id, cancellationToken);
        if (existing is null)
        {
            return NotFound(new ProblemDetails
            {
                Title = "Task not found",
                Detail = $"No task found with ID {id}",
                Status = StatusCodes.Status404NotFound
            });
        }

        existing.Title = request.Title ?? existing.Title;
        existing.Description = request.Description ?? existing.Description;
        existing.Status = request.Status ?? existing.Status;
        existing.Priority = request.Priority ?? existing.Priority;
        existing.DueDate = request.DueDate ?? existing.DueDate;
        existing.UpdatedAt = DateTime.UtcNow;

        await _repository.UpdateAsync(existing, cancellationToken);
        _logger.LogInformation("Updated task {TaskId}", id);

        return Ok(existing);
    }

    /// <summary>
    /// Delete a task
    /// </summary>
    [HttpDelete("{id:guid}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Delete(
        Guid id,
        CancellationToken cancellationToken = default)
    {
        var existing = await _repository.GetByIdAsync(id, cancellationToken);
        if (existing is null)
        {
            return NotFound(new ProblemDetails
            {
                Title = "Task not found",
                Detail = $"No task found with ID {id}",
                Status = StatusCodes.Status404NotFound
            });
        }

        await _repository.DeleteAsync(id, cancellationToken);
        _logger.LogInformation("Deleted task {TaskId}", id);

        return NoContent();
    }
}

// =============================================================================
// Shared Models (also defined in task-api-dotnet.cs)
// =============================================================================
// Note: In a real project, these would be in a shared file or assembly.

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

public enum TaskStatus { Pending, InProgress, Completed, Cancelled }
public enum TaskPriority { Low, Medium, High, Critical }

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

public class PagedResult<T>
{
    public IEnumerable<T> Data { get; init; } = Enumerable.Empty<T>();
    public int Page { get; init; }
    public int PageSize { get; init; }
    public int TotalCount { get; init; }
    public int TotalPages => (int)Math.Ceiling((double)TotalCount / PageSize);
}

public interface ITaskRepository
{
    Task<IEnumerable<TaskItem>> GetAllAsync(TaskStatus? status, TaskPriority? priority,
        int page, int pageSize, CancellationToken ct);
    Task<int> GetCountAsync(TaskStatus? status, TaskPriority? priority, CancellationToken ct);
    Task<TaskItem?> GetByIdAsync(Guid id, CancellationToken ct);
    Task CreateAsync(TaskItem task, CancellationToken ct);
    Task UpdateAsync(TaskItem task, CancellationToken ct);
    Task DeleteAsync(Guid id, CancellationToken ct);
}
