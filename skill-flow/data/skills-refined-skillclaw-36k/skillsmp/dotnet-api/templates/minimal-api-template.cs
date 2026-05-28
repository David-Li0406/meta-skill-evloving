// =============================================================================
// Minimal API Template for ASP.NET Core 8+
// =============================================================================
// This template provides a production-ready starting point for Minimal APIs.
// Replace placeholders (e.g., Product, IProductRepository) with your domain.
// =============================================================================

using FluentValidation;
using Microsoft.AspNetCore.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using System.ComponentModel.DataAnnotations;

var builder = WebApplication.CreateBuilder(args);

// -----------------------------------------------------------------------------
// Service Registration
// -----------------------------------------------------------------------------

// OpenAPI/Swagger
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new Microsoft.OpenApi.Models.OpenApiInfo
    {
        Title = "My API",
        Version = "v1",
        Description = "API description here"
    });
});

// Problem Details for consistent error responses
builder.Services.AddProblemDetails(options =>
{
    options.CustomizeProblemDetails = context =>
    {
        context.ProblemDetails.Extensions["traceId"] = context.HttpContext.TraceIdentifier;
    };
});

// FluentValidation - register all validators from assembly
builder.Services.AddValidatorsFromAssemblyContaining<Program>();

// Health checks
builder.Services.AddHealthChecks()
    .AddCheck("self", () => Microsoft.Extensions.Diagnostics.HealthChecks.HealthCheckResult.Healthy());

// Response caching and compression
builder.Services.AddOutputCache(options =>
{
    options.AddBasePolicy(b => b.Expire(TimeSpan.FromMinutes(5)));
});
builder.Services.AddResponseCompression();

// TODO: Add your services here
// builder.Services.AddScoped<IProductRepository, ProductRepository>();

var app = builder.Build();

// -----------------------------------------------------------------------------
// Middleware Pipeline
// -----------------------------------------------------------------------------

app.UseExceptionHandler();
app.UseResponseCompression();
app.UseOutputCache();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

// -----------------------------------------------------------------------------
// Health Check Endpoints
// -----------------------------------------------------------------------------

app.MapHealthChecks("/health/live", new Microsoft.AspNetCore.Diagnostics.HealthChecks.HealthCheckOptions
{
    Predicate = _ => false // Liveness: just check if app responds
});

app.MapHealthChecks("/health/ready");

// -----------------------------------------------------------------------------
// API Endpoints
// -----------------------------------------------------------------------------

var api = app.MapGroup("/api/v1");

// GET /api/v1/products
api.MapGet("/products", async (
    [FromQuery] int page = 1,
    [FromQuery] int pageSize = 10,
    CancellationToken cancellationToken = default) =>
{
    // TODO: Replace with actual repository call
    var products = new List<Product>
    {
        new(1, "Sample Product", 29.99m, "SAM-0001")
    };

    return Results.Ok(new
    {
        data = products,
        page,
        pageSize,
        total = products.Count
    });
})
.WithName("GetProducts")
.WithTags("Products")
.Produces<object>(StatusCodes.Status200OK)
.WithOpenApi(op =>
{
    op.Summary = "Get all products";
    op.Description = "Returns a paginated list of products";
    return op;
});

// GET /api/v1/products/{id}
api.MapGet("/products/{id:int}", async (
    int id,
    CancellationToken cancellationToken) =>
{
    // TODO: Replace with actual repository call
    if (id == 1)
    {
        return Results.Ok(new Product(1, "Sample Product", 29.99m, "SAM-0001"));
    }

    return Results.NotFound(new ProblemDetails
    {
        Status = StatusCodes.Status404NotFound,
        Title = "Product not found",
        Detail = $"No product found with ID {id}"
    });
})
.WithName("GetProductById")
.WithTags("Products")
.Produces<Product>(StatusCodes.Status200OK)
.Produces<ProblemDetails>(StatusCodes.Status404NotFound)
.WithOpenApi();

// POST /api/v1/products
api.MapPost("/products", async (
    CreateProductRequest request,
    IValidator<CreateProductRequest> validator,
    CancellationToken cancellationToken) =>
{
    // Validate request
    var validationResult = await validator.ValidateAsync(request, cancellationToken);
    if (!validationResult.IsValid)
    {
        return Results.ValidationProblem(validationResult.ToDictionary());
    }

    // TODO: Replace with actual repository call
    var product = new Product(1, request.Name, request.Price, request.Sku);

    return Results.Created($"/api/v1/products/{product.Id}", product);
})
.WithName("CreateProduct")
.WithTags("Products")
.Produces<Product>(StatusCodes.Status201Created)
.Produces<ValidationProblemDetails>(StatusCodes.Status400BadRequest)
.WithOpenApi();

// PUT /api/v1/products/{id}
api.MapPut("/products/{id:int}", async (
    int id,
    UpdateProductRequest request,
    IValidator<UpdateProductRequest> validator,
    CancellationToken cancellationToken) =>
{
    var validationResult = await validator.ValidateAsync(request, cancellationToken);
    if (!validationResult.IsValid)
    {
        return Results.ValidationProblem(validationResult.ToDictionary());
    }

    // TODO: Replace with actual repository call
    // Check if exists, update, return

    return Results.NoContent();
})
.WithName("UpdateProduct")
.WithTags("Products")
.Produces(StatusCodes.Status204NoContent)
.Produces<ProblemDetails>(StatusCodes.Status404NotFound)
.Produces<ValidationProblemDetails>(StatusCodes.Status400BadRequest)
.WithOpenApi();

// DELETE /api/v1/products/{id}
api.MapDelete("/products/{id:int}", async (
    int id,
    CancellationToken cancellationToken) =>
{
    // TODO: Replace with actual repository call
    // Check if exists, delete

    return Results.NoContent();
})
.WithName("DeleteProduct")
.WithTags("Products")
.Produces(StatusCodes.Status204NoContent)
.Produces<ProblemDetails>(StatusCodes.Status404NotFound)
.WithOpenApi();

app.Run();

// -----------------------------------------------------------------------------
// Models
// -----------------------------------------------------------------------------

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

// -----------------------------------------------------------------------------
// Validators
// -----------------------------------------------------------------------------

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
