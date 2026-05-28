---
name: api-documentation
description: Generates and updates comprehensive API documentation for Merge E-Commerce
trigger: "documentation request OR generate docs OR add swagger comments OR document API"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(dotnet build)
---

# API Documentation Generator

Generates and maintains comprehensive API documentation for the Merge E-Commerce Backend.

## Trigger Conditions

- User says "document this API"
- User says "generate docs"
- User says "add swagger comments"
- New endpoint created
- DTO modified

## Documentation Types

### 1. Controller XML Comments

**Full Controller Documentation:**
```csharp
/// <summary>
/// Products API - Manages product catalog operations
/// </summary>
/// <remarks>
/// This controller handles all product-related operations including:
/// - CRUD operations for products
/// - Product search and filtering
/// - Product variants and attributes
/// - Stock management
///
/// All endpoints require authentication except GET operations.
/// Admin role required for create, update, and delete operations.
/// </remarks>
[ApiController]
[Route("api/v1/[controller]")]
[Produces("application/json")]
[Tags("Products")]
public class ProductsController(ISender sender) : ControllerBase
{
    /// <summary>
    /// Get paginated list of products
    /// </summary>
    /// <remarks>
    /// Sample request:
    ///
    ///     GET /api/v1/products?page=1&amp;pageSize=20&amp;categoryId=xxx&amp;minPrice=100
    ///
    /// Supports filtering by:
    /// - Category ID
    /// - Price range (minPrice, maxPrice)
    /// - Search term (searches name and description)
    /// - Stock status (inStock=true/false)
    /// - Active status
    ///
    /// Results are sorted by:
    /// - name (default)
    /// - price
    /// - createdAt
    /// - popularity
    /// </remarks>
    /// <param name="query">Query parameters for filtering and pagination</param>
    /// <param name="cancellationToken">Cancellation token</param>
    /// <returns>Paginated list of products</returns>
    /// <response code="200">Returns the paginated product list</response>
    /// <response code="400">Invalid query parameters</response>
    [HttpGet]
    [AllowAnonymous]
    [ProducesResponseType<PagedResult<ProductListDto>>(StatusCodes.Status200OK)]
    [ProducesResponseType<ValidationProblemDetails>(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> GetProducts(
        [FromQuery] GetProductsQuery query,
        CancellationToken cancellationToken)
    {
        var result = await sender.Send(query, cancellationToken);
        return Ok(result);
    }

    /// <summary>
    /// Get a product by its unique identifier
    /// </summary>
    /// <remarks>
    /// Returns detailed product information including:
    /// - Basic product info (name, description, price)
    /// - Category information
    /// - Product variants
    /// - Product images
    /// - Stock status
    /// - Average rating and review count
    ///
    /// Sample request:
    ///
    ///     GET /api/v1/products/3fa85f64-5717-4562-b3fc-2c963f66afa6
    ///
    /// </remarks>
    /// <param name="id">The unique product identifier (GUID)</param>
    /// <param name="cancellationToken">Cancellation token</param>
    /// <returns>Product details</returns>
    /// <response code="200">Returns the product details</response>
    /// <response code="404">Product not found</response>
    [HttpGet("{id:guid}")]
    [AllowAnonymous]
    [ProducesResponseType<ProductDetailDto>(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetProduct(
        Guid id,
        CancellationToken cancellationToken)
    {
        var result = await sender.Send(new GetProductByIdQuery(id), cancellationToken);
        return result is not null ? Ok(result) : NotFound();
    }

    /// <summary>
    /// Create a new product
    /// </summary>
    /// <remarks>
    /// Creates a new product in the catalog.
    ///
    /// **Required fields:**
    /// - Name (1-200 characters)
    /// - Price (greater than 0)
    /// - CategoryId (valid category GUID)
    ///
    /// **Optional fields:**
    /// - Description (max 5000 characters)
    /// - SKU (unique, auto-generated if not provided)
    /// - StockQuantity (default: 0)
    /// - Images (array of image URLs)
    /// - Attributes (key-value pairs)
    ///
    /// Sample request:
    ///
    ///     POST /api/v1/products
    ///     {
    ///         "name": "iPhone 15 Pro",
    ///         "description": "Latest Apple smartphone",
    ///         "price": 49999.99,
    ///         "categoryId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    ///         "stockQuantity": 100,
    ///         "attributes": {
    ///             "color": "Space Black",
    ///             "storage": "256GB"
    ///         }
    ///     }
    ///
    /// </remarks>
    /// <param name="command">Product creation data</param>
    /// <param name="cancellationToken">Cancellation token</param>
    /// <returns>The created product</returns>
    /// <response code="201">Product created successfully</response>
    /// <response code="400">Invalid product data (validation errors)</response>
    /// <response code="401">Unauthorized - authentication required</response>
    /// <response code="403">Forbidden - insufficient permissions</response>
    /// <response code="409">Conflict - product with same SKU already exists</response>
    [HttpPost]
    [Authorize(Roles = "Admin,Seller")]
    [ProducesResponseType<ProductDto>(StatusCodes.Status201Created)]
    [ProducesResponseType<ValidationProblemDetails>(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    [ProducesResponseType(StatusCodes.Status403Forbidden)]
    [ProducesResponseType<ProblemDetails>(StatusCodes.Status409Conflict)]
    public async Task<IActionResult> CreateProduct(
        [FromBody] CreateProductCommand command,
        CancellationToken cancellationToken)
    {
        var result = await sender.Send(command, cancellationToken);
        return CreatedAtAction(nameof(GetProduct), new { id = result.Id }, result);
    }

    /// <summary>
    /// Update an existing product
    /// </summary>
    /// <remarks>
    /// Updates all fields of an existing product.
    /// For partial updates, use PATCH endpoint instead.
    ///
    /// **Note:** This is a full update - all fields must be provided.
    /// Fields not included will be reset to their default values.
    ///
    /// Sample request:
    ///
    ///     PUT /api/v1/products/3fa85f64-5717-4562-b3fc-2c963f66afa6
    ///     {
    ///         "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    ///         "name": "iPhone 15 Pro Max",
    ///         "description": "Updated description",
    ///         "price": 54999.99,
    ///         "categoryId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    ///         "stockQuantity": 50,
    ///         "isActive": true
    ///     }
    ///
    /// </remarks>
    /// <param name="id">Product ID from URL</param>
    /// <param name="command">Updated product data</param>
    /// <param name="cancellationToken">Cancellation token</param>
    /// <returns>Updated product</returns>
    /// <response code="200">Product updated successfully</response>
    /// <response code="400">Invalid data or ID mismatch</response>
    /// <response code="401">Unauthorized</response>
    /// <response code="403">Forbidden</response>
    /// <response code="404">Product not found</response>
    [HttpPut("{id:guid}")]
    [Authorize(Roles = "Admin,Seller")]
    [ProducesResponseType<ProductDto>(StatusCodes.Status200OK)]
    [ProducesResponseType<ValidationProblemDetails>(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> UpdateProduct(
        Guid id,
        [FromBody] UpdateProductCommand command,
        CancellationToken cancellationToken)
    {
        if (id != command.Id)
            return BadRequest(new ProblemDetails { Detail = "URL ID and body ID mismatch" });

        var result = await sender.Send(command, cancellationToken);
        return Ok(result);
    }

    /// <summary>
    /// Delete a product
    /// </summary>
    /// <remarks>
    /// Soft deletes a product from the catalog.
    /// The product will be marked as deleted but data is retained for historical purposes.
    ///
    /// **Note:** This action cannot be undone through the API.
    /// Contact administrator for data recovery.
    ///
    /// **Restrictions:**
    /// - Cannot delete products with pending orders
    /// - Admin role required
    /// </remarks>
    /// <param name="id">Product ID to delete</param>
    /// <param name="cancellationToken">Cancellation token</param>
    /// <returns>No content on success</returns>
    /// <response code="204">Product deleted successfully</response>
    /// <response code="401">Unauthorized</response>
    /// <response code="403">Forbidden - Admin role required</response>
    /// <response code="404">Product not found</response>
    /// <response code="409">Cannot delete - product has pending orders</response>
    [HttpDelete("{id:guid}")]
    [Authorize(Roles = "Admin")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType<ProblemDetails>(StatusCodes.Status409Conflict)]
    public async Task<IActionResult> DeleteProduct(
        Guid id,
        CancellationToken cancellationToken)
    {
        await sender.Send(new DeleteProductCommand(id), cancellationToken);
        return NoContent();
    }
}
```

### 2. DTO Documentation

**Request DTO:**
```csharp
/// <summary>
/// Command to create a new product
/// </summary>
public record CreateProductCommand(
    /// <summary>
    /// Product name - must be unique within category
    /// </summary>
    /// <example>iPhone 15 Pro</example>
    [Required]
    [StringLength(200, MinimumLength = 1)]
    string Name,

    /// <summary>
    /// Product description with HTML support
    /// </summary>
    /// <example>The latest iPhone with A17 Pro chip</example>
    [StringLength(5000)]
    string? Description,

    /// <summary>
    /// Product price in TRY (Turkish Lira)
    /// </summary>
    /// <example>49999.99</example>
    [Range(0.01, 9999999.99)]
    decimal Price,

    /// <summary>
    /// Category identifier - must exist in system
    /// </summary>
    /// <example>3fa85f64-5717-4562-b3fc-2c963f66afa6</example>
    [Required]
    Guid CategoryId,

    /// <summary>
    /// Initial stock quantity (default: 0)
    /// </summary>
    /// <example>100</example>
    [Range(0, int.MaxValue)]
    int StockQuantity = 0,

    /// <summary>
    /// Product SKU - auto-generated if not provided
    /// </summary>
    /// <example>IPHONE-15-PRO-256-BLK</example>
    [StringLength(50)]
    string? Sku = null,

    /// <summary>
    /// Product attributes as key-value pairs
    /// </summary>
    /// <example>{"color": "Space Black", "storage": "256GB"}</example>
    Dictionary<string, string>? Attributes = null
) : IRequest<ProductDto>;
```

**Response DTO:**
```csharp
/// <summary>
/// Product detail response
/// </summary>
public record ProductDetailDto(
    /// <summary>
    /// Unique product identifier
    /// </summary>
    Guid Id,

    /// <summary>
    /// Product name
    /// </summary>
    string Name,

    /// <summary>
    /// Product description (may contain HTML)
    /// </summary>
    string? Description,

    /// <summary>
    /// Current price in TRY
    /// </summary>
    decimal Price,

    /// <summary>
    /// Original price before discount (null if no discount)
    /// </summary>
    decimal? OriginalPrice,

    /// <summary>
    /// Discount percentage (0-100)
    /// </summary>
    int DiscountPercentage,

    /// <summary>
    /// Product SKU code
    /// </summary>
    string Sku,

    /// <summary>
    /// Category information
    /// </summary>
    CategoryDto Category,

    /// <summary>
    /// Current stock quantity
    /// </summary>
    int StockQuantity,

    /// <summary>
    /// Whether product is in stock
    /// </summary>
    bool InStock,

    /// <summary>
    /// Whether product is active and visible
    /// </summary>
    bool IsActive,

    /// <summary>
    /// Average rating (1-5 stars)
    /// </summary>
    decimal AverageRating,

    /// <summary>
    /// Total number of reviews
    /// </summary>
    int ReviewCount,

    /// <summary>
    /// Product images (first is primary)
    /// </summary>
    IReadOnlyList<ProductImageDto> Images,

    /// <summary>
    /// Product variants (size, color combinations)
    /// </summary>
    IReadOnlyList<ProductVariantDto> Variants,

    /// <summary>
    /// Product attributes
    /// </summary>
    IReadOnlyDictionary<string, string> Attributes,

    /// <summary>
    /// Creation timestamp (UTC)
    /// </summary>
    DateTime CreatedAt,

    /// <summary>
    /// Last update timestamp (UTC)
    /// </summary>
    DateTime? UpdatedAt
);
```

### 3. Error Response Documentation

**Standard Error Responses:**
```csharp
/// <summary>
/// Standard problem details for API errors
/// </summary>
public record ApiProblemDetails
{
    /// <summary>
    /// A URI reference that identifies the problem type
    /// </summary>
    /// <example>https://api.mergecommerce.com/errors/validation</example>
    public string Type { get; init; }

    /// <summary>
    /// A short, human-readable summary
    /// </summary>
    /// <example>Validation Error</example>
    public string Title { get; init; }

    /// <summary>
    /// The HTTP status code
    /// </summary>
    /// <example>400</example>
    public int Status { get; init; }

    /// <summary>
    /// A human-readable explanation
    /// </summary>
    /// <example>One or more validation errors occurred</example>
    public string Detail { get; init; }

    /// <summary>
    /// The request path
    /// </summary>
    /// <example>/api/v1/products</example>
    public string Instance { get; init; }

    /// <summary>
    /// Validation errors by field (for 400 responses)
    /// </summary>
    /// <example>{"Name": ["Name is required", "Name must be at least 1 character"]}</example>
    public IDictionary<string, string[]>? Errors { get; init; }

    /// <summary>
    /// Correlation ID for request tracing
    /// </summary>
    /// <example>abc123-def456</example>
    public string? TraceId { get; init; }
}
```

### 4. API Versioning Documentation

```csharp
/// <summary>
/// API v1 - Current stable version
/// </summary>
/// <remarks>
/// Version 1 of the Merge E-Commerce API.
///
/// **Base URL:** https://api.mergecommerce.com/api/v1
///
/// **Authentication:** Bearer JWT token in Authorization header
///
/// **Rate Limits:**
/// - Anonymous: 100 requests/minute
/// - Authenticated: 1000 requests/minute
/// - Admin: 5000 requests/minute
///
/// **Response Format:** JSON (application/json)
///
/// **Pagination:** All list endpoints support pagination via page and pageSize query params
/// </remarks>
[ApiVersion("1.0")]
[Route("api/v{version:apiVersion}/[controller]")]
public class BaseApiController : ControllerBase { }
```

## Swagger/OpenAPI Configuration

**Program.cs Configuration:**
```csharp
builder.Services.AddSwaggerGen(options =>
{
    options.SwaggerDoc("v1", new OpenApiInfo
    {
        Version = "v1",
        Title = "Merge E-Commerce API",
        Description = "RESTful API for Merge E-Commerce Platform",
        TermsOfService = new Uri("https://mergecommerce.com/terms"),
        Contact = new OpenApiContact
        {
            Name = "API Support",
            Email = "api@mergecommerce.com",
            Url = new Uri("https://mergecommerce.com/support")
        },
        License = new OpenApiLicense
        {
            Name = "Proprietary",
            Url = new Uri("https://mergecommerce.com/license")
        }
    });

    // Include XML comments
    var xmlFile = $"{Assembly.GetExecutingAssembly().GetName().Name}.xml";
    var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
    options.IncludeXmlComments(xmlPath);

    // JWT Authentication
    options.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
    {
        Description = "JWT Authorization header using Bearer scheme",
        Name = "Authorization",
        In = ParameterLocation.Header,
        Type = SecuritySchemeType.Http,
        Scheme = "bearer",
        BearerFormat = "JWT"
    });

    options.AddSecurityRequirement(new OpenApiSecurityRequirement
    {
        {
            new OpenApiSecurityScheme
            {
                Reference = new OpenApiReference
                {
                    Type = ReferenceType.SecurityScheme,
                    Id = "Bearer"
                }
            },
            Array.Empty<string>()
        }
    });
});
```

## Documentation Generation Process

### Step 1: Find Controllers
```bash
find Merge.API/Controllers -name "*Controller.cs" -type f
```

### Step 2: Check for Missing Documentation
```bash
# Find endpoints without XML comments
grep -rn "\[Http" Merge.API/Controllers/ --include="*.cs" -B1 | grep -v "summary"

# Find DTOs without documentation
grep -rn "public record.*Dto\|public class.*Dto" Merge.Application/ --include="*.cs" | grep -v "summary"
```

### Step 3: Generate Documentation
- Add XML comments to endpoints
- Add ProducesResponseType attributes
- Add example values to DTOs
- Include request/response samples

### Step 4: Verify in Swagger
```bash
dotnet run --project Merge.API
# Open https://localhost:5001/swagger
```

## Output Format

After generating documentation, verify:

```markdown
## Documentation Checklist

### Controller: ProductsController
- [x] Class summary
- [x] GET /products - documented
- [x] GET /products/{id} - documented
- [x] POST /products - documented
- [x] PUT /products/{id} - documented
- [x] DELETE /products/{id} - documented

### DTOs
- [x] CreateProductCommand - all properties documented
- [x] UpdateProductCommand - all properties documented
- [x] ProductDto - all properties documented
- [x] ProductDetailDto - all properties documented

### Response Types
- [x] 200 OK - documented
- [x] 201 Created - documented
- [x] 400 Bad Request - documented
- [x] 401 Unauthorized - documented
- [x] 403 Forbidden - documented
- [x] 404 Not Found - documented
- [x] 409 Conflict - documented
```
