---
name: api-endpoint
description: Creates REST API controller with proper versioning, authorization, and OpenAPI documentation
---

# API Endpoint Creator Skill

Bu skill, Merge E-Commerce Backend projesi için REST API endpoint oluşturur.

## Ne Zaman Kullan

- "Controller oluştur", "endpoint ekle" dendiğinde
- Yeni bir API resource eklenirken
- "Products API'si yaz" gibi isteklerde

## Oluşturulacak Dosya

```
Merge.API/Controllers/v1/{Entity}sController.cs
```

## Controller Template

```csharp
/// <summary>
/// Manages {entity} operations.
/// </summary>
[ApiController]
[ApiVersion("1.0")]
[Route("api/v{version:apiVersion}/[controller]")]
[Produces("application/json")]
[Authorize]
public class {Entity}sController(ISender mediator) : ControllerBase
{
    /// <summary>
    /// Gets all {entities} with pagination.
    /// </summary>
    [HttpGet]
    [ProducesResponseType(typeof(PagedResult<{Entity}Dto>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetAll(
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 10,
        CancellationToken ct = default)
    {
        var query = new Get{Entity}sQuery(page, pageSize);
        var result = await mediator.Send(query, ct);
        return Ok(result);
    }

    /// <summary>
    /// Gets a {entity} by ID.
    /// </summary>
    [HttpGet("{id:guid}")]
    [ProducesResponseType(typeof({Entity}Dto), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetById(Guid id, CancellationToken ct)
    {
        var query = new Get{Entity}ByIdQuery(id);
        var result = await mediator.Send(query, ct);
        return Ok(result);
    }

    /// <summary>
    /// Creates a new {entity}.
    /// </summary>
    [HttpPost]
    [ProducesResponseType(typeof({Entity}Dto), StatusCodes.Status201Created)]
    [ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> Create(
        [FromBody] Create{Entity}Command command,
        CancellationToken ct)
    {
        var result = await mediator.Send(command, ct);
        return CreatedAtAction(nameof(GetById), new { id = result.Id }, result);
    }

    /// <summary>
    /// Updates an existing {entity}.
    /// </summary>
    [HttpPut("{id:guid}")]
    [ProducesResponseType(typeof({Entity}Dto), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Update(
        Guid id,
        [FromBody] Update{Entity}Command command,
        CancellationToken ct)
    {
        var result = await mediator.Send(command with { Id = id }, ct);
        return Ok(result);
    }

    /// <summary>
    /// Deletes a {entity}.
    /// </summary>
    [HttpDelete("{id:guid}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> Delete(Guid id, CancellationToken ct)
    {
        await mediator.Send(new Delete{Entity}Command(id), ct);
        return NoContent();
    }
}
```

## Nested Resource Template

```csharp
/// <summary>
/// Gets {child}s for a specific {parent}.
/// </summary>
[HttpGet("{parentId:guid}/{children}")]
[ProducesResponseType(typeof(List<{Child}Dto>), StatusCodes.Status200OK)]
public async Task<IActionResult> Get{Children}(
    Guid parentId,
    CancellationToken ct)
{
    var query = new Get{Children}By{Parent}IdQuery(parentId);
    var result = await mediator.Send(query, ct);
    return Ok(result);
}
```

## Kurallar

1. Controller THIN olmalı - sadece MediatR çağrısı
2. Primary constructor kullan
3. Her endpoint için ProducesResponseType
4. CancellationToken zorunlu
5. Authorize attribute zorunlu
6. API versioning kullan (v1)
7. XML documentation ekle
