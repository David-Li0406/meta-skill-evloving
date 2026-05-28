// =============================================================================
// Controller-Based API Template for ASP.NET Core 8+
// =============================================================================
// This template provides a production-ready starting point for controller APIs.
// Replace placeholders (e.g., Product, IProductRepository) with your domain.
// =============================================================================

using FluentValidation;
using Microsoft.AspNetCore.Mvc;
using Microsoft.OpenApi.Models;
using System.Reflection;

var builder = WebApplication.CreateBuilder(args);

// -----------------------------------------------------------------------------
// Service Registration
// -----------------------------------------------------------------------------

// Controllers with Problem Details
builder.Services.AddControllers()
    .ConfigureApiBehaviorOptions(options =>
    {
        options.InvalidModelStateResponseFactory = context =>
        {
            var problemDetails = new ValidationProblemDetails(context.ModelState)
            {
                Type = "https://tools.ietf.org/html/rfc7231#section-6.5.1",
                Title = "Validation failed",
                Status = StatusCodes.Status400BadRequest,
                Instance = context.HttpContext.Request.Path
            };
            problemDetails.Extensions["traceId"] = context.HttpContext.TraceIdentifier;
            return new BadRequestObjectResult(problemDetails);
        };
    });

// OpenAPI/Swagger
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo
    {
        Title = "My API",
        Version = "v1",
        Description = "API description here",
        Contact = new OpenApiContact
        {
            Name = "API Support",
            Email = "support@example.com"
        }
    });

    // Include XML comments if available
    var xmlFile = $"{Assembly.GetExecutingAssembly().GetName().Name}.xml";
    var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
    if (File.Exists(xmlPath))
    {
        options.IncludeXmlComments(xmlPath);
    }
});

// Problem Details
builder.Services.AddProblemDetails(options =>
{
    options.CustomizeProblemDetails = context =>
    {
        context.ProblemDetails.Extensions["traceId"] = context.HttpContext.TraceIdentifier;
    };
});

// FluentValidation
builder.Services.AddValidatorsFromAssemblyContaining<Program>();

// Health checks
builder.Services.AddHealthChecks()
    .AddCheck("self", () => Microsoft.Extensions.Diagnostics.HealthChecks.HealthCheckResult.Healthy());

// Response caching
builder.Services.AddResponseCaching();
builder.Services.AddOutputCache(options =>
{
    options.AddPolicy("Products", b => b.Expire(TimeSpan.FromMinutes(10)).Tag("products"));
});

// TODO: Add your services here
// builder.Services.AddScoped<IProductRepository, ProductRepository>();

var app = builder.Build();

// -----------------------------------------------------------------------------
// Middleware Pipeline
// -----------------------------------------------------------------------------

app.UseExceptionHandler();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(options =>
    {
        options.SwaggerEndpoint("/swagger/v1/swagger.json", "v1");
    });
}

app.UseResponseCaching();
app.UseOutputCache();

app.MapControllers();

// Health checks
app.MapHealthChecks("/health/live");
app.MapHealthChecks("/health/ready");

app.Run();

// =============================================================================
// Controllers
// =============================================================================

namespace MyApi.Controllers;

/// <summary>
/// Manages product resources.
/// </summary>
[ApiController]
[Route("api/v1/[controller]")]
[Produces("application/json")]
public class ProductsController : ControllerBase
{
    private readonly ILogger<ProductsController> _logger;
    private readonly IValidator<CreateProductRequest> _createValidator;
    private readonly IValidator<UpdateProductRequest> _updateValidator;
    // TODO: Add repository
    // private readonly IProductRepository _repository;

    public ProductsController(
        ILogger<ProductsController> logger,
        IValidator<CreateProductRequest> createValidator,
        IValidator<UpdateProductRequest> updateValidator)
    {
        _logger = logger;
        _createValidator = createValidator;
        _updateValidator = updateValidator;
    }

    /// <summary>
    /// Gets all products with pagination.
    /// </summary>
    /// <param name="page">Page number (default: 1)</param>
    /// <param name="pageSize">Items per page (default: 10)</param>
    /// <param name="cancellationToken">Cancellation token</param>
    /// <returns>Paginated list of products</returns>
    [HttpGet]
    [ProducesResponseType(typeof(PagedResult<Product>), StatusCodes.Status200OK)]
    public async Task<ActionResult<PagedResult<Product>>> GetAll(
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 10,
        CancellationToken cancellationToken = default)
    {
        _logger.LogInformation("Getting products page {Page} with size {PageSize}", page, pageSize);

        // TODO: Replace with actual repository call
        var products = new List<Product>
        {
            new(1, "Sample Product", 29.99m, "SAM-0001")
        };

        var result = new PagedResult<Product>
        {
            Data = products,
            Page = page,
            PageSize = pageSize,
            TotalCount = products.Count
        };

        return Ok(result);
    }

    /// <summary>
    /// Gets a specific product by ID.
    /// </summary>
    /// <param name="id">Product ID</param>
    /// <param name="cancellationToken">Cancellation token</param>
    /// <returns>The requested product</returns>
    [HttpGet("{id:int}")]
    [ProducesResponseType(typeof(Product), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<ActionResult<Product>> GetById(
        int id,
        CancellationToken cancellationToken = default)
    {
        _logger.LogInformation("Getting product {ProductId}", id);

        // TODO: Replace with actual repository call
        if (id == 1)
        {
            return Ok(new Product(1, "Sample Product", 29.99m, "SAM-0001"));
        }

        return NotFound(new ProblemDetails
        {
            Status = StatusCodes.Status404NotFound,
            Title = "Product not found",
            Detail = $"No product found with ID {id}",
            Instance = HttpContext.Request.Path
        });
    }

    /// <summary>
    /// Creates a new product.
    /// </summary>
    /// <param name="request">Product creation request</param>
    /// <param name="cancellationToken">Cancellation token</param>
    /// <returns>The created product</returns>
    [HttpPost]
    [ProducesResponseType(typeof(Product), StatusCodes.Status201Created)]
    [ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<Product>> Create(
        [FromBody] CreateProductRequest request,
        CancellationToken cancellationToken = default)
    {
        var validationResult = await _createValidator.ValidateAsync(request, cancellationToken);
        if (!validationResult.IsValid)
        {
            return ValidationProblem(new ValidationProblemDetails(
                validationResult.ToDictionary()));
        }

        _logger.LogInformation("Creating product {ProductName}", request.Name);

        // TODO: Replace with actual repository call
        var product = new Product(1, request.Name, request.Price, request.Sku);

        return CreatedAtAction(
            nameof(GetById),
            new { id = product.Id },
            product);
    }

    /// <summary>
    /// Updates an existing product.
    /// </summary>
    /// <param name="id">Product ID</param>
    /// <param name="request">Product update request</param>
    /// <param name="cancellationToken">Cancellation token</param>
    [HttpPut("{id:int}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Update(
        int id,
        [FromBody] UpdateProductRequest request,
        CancellationToken cancellationToken = default)
    {
        var validationResult = await _updateValidator.ValidateAsync(request, cancellationToken);
        if (!validationResult.IsValid)
        {
            return ValidationProblem(new ValidationProblemDetails(
                validationResult.ToDictionary()));
        }

        _logger.LogInformation("Updating product {ProductId}", id);

        // TODO: Replace with actual repository call
        // Check if exists, update

        return NoContent();
    }

    /// <summary>
    /// Deletes a product.
    /// </summary>
    /// <param name="id">Product ID</param>
    /// <param name="cancellationToken">Cancellation token</param>
    [HttpDelete("{id:int}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Delete(
        int id,
        CancellationToken cancellationToken = default)
    {
        _logger.LogInformation("Deleting product {ProductId}", id);

        // TODO: Replace with actual repository call
        // Check if exists, delete

        return NoContent();
    }
}

// =============================================================================
// Models
// =============================================================================

public record Product(int Id, string Name, decimal Price, string Sku);

public record CreateProductRequest
{
    public string Name { get; init; } = string.Empty;
    public decimal Price { get; init; }
    public string Sku { get; init; } = string.Empty;
}

public record UpdateProductRequest
{
    public string Name { get; init; } = string.Empty;
    public decimal Price { get; init; }
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

public class CreateProductRequestValidator : AbstractValidator<CreateProductRequest>
{
    public CreateProductRequestValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Name is required")
            .MaximumLength(100).WithMessage("Name must not exceed 100 characters");

        RuleFor(x => x.Price)
            .GreaterThan(0).WithMessage("Price must be greater than 0")
            .PrecisionScale(10, 2, false).WithMessage("Price must have at most 2 decimal places");

        RuleFor(x => x.Sku)
            .NotEmpty().WithMessage("SKU is required")
            .Matches(@"^[A-Z]{3}-\d{4}$").WithMessage("SKU must be in format XXX-0000");
    }
}

public class UpdateProductRequestValidator : AbstractValidator<UpdateProductRequest>
{
    public UpdateProductRequestValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Name is required")
            .MaximumLength(100).WithMessage("Name must not exceed 100 characters");

        RuleFor(x => x.Price)
            .GreaterThan(0).WithMessage("Price must be greater than 0");
    }
}

// Make Program accessible for integration tests
public partial class Program { }
