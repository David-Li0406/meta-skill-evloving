---
name: cqrs-scaffolder
description: Scaffolds complete CQRS command or query with handler, validator, and DTO following Merge project patterns
---

# CQRS Scaffolder Skill

Bu skill, Merge E-Commerce Backend projesi için tam CQRS yapısı oluşturur.

## Ne Zaman Kullan

- Kullanıcı "command oluştur", "query oluştur" dediğinde
- Yeni bir CRUD operasyonu eklenirken
- "handler yaz", "validator ekle" gibi isteklerde

## Command Oluşturma

```
Merge.Application/{Module}/Commands/{Name}/
├── {Name}Command.cs
├── {Name}CommandHandler.cs
└── {Name}CommandValidator.cs
```

### Command Template

```csharp
public record {Name}Command(
    // Properties from user
) : IRequest<{ReturnType}>;
```

### Handler Template

```csharp
public class {Name}CommandHandler(
    IRepository<{Entity}> repository,
    IUnitOfWork unitOfWork,
    IMapper mapper,
    ILogger<{Name}CommandHandler> logger)
    : IRequestHandler<{Name}Command, {ReturnType}>
{
    public async Task<{ReturnType}> Handle(
        {Name}Command request,
        CancellationToken ct)
    {
        logger.LogInformation("Processing {Command}", nameof({Name}Command));

        // Implementation

        await unitOfWork.SaveChangesAsync(ct);
        return mapper.Map<{ReturnType}>(entity);
    }
}
```

### Validator Template

```csharp
public class {Name}CommandValidator : AbstractValidator<{Name}Command>
{
    public {Name}CommandValidator()
    {
        RuleFor(x => x.Property)
            .NotEmpty()
            .WithMessage("Property is required");
    }
}
```

## Query Oluşturma

```
Merge.Application/{Module}/Queries/{Name}/
├── {Name}Query.cs
└── {Name}QueryHandler.cs
```

### Query Template

```csharp
public record {Name}Query(Guid Id) : IRequest<{ReturnType}?>;
```

### Query Handler Template

```csharp
public class {Name}QueryHandler(
    IRepository<{Entity}> repository,
    IMapper mapper,
    ICacheService cache,
    ILogger<{Name}QueryHandler> logger)
    : IRequestHandler<{Name}Query, {ReturnType}?>
{
    public async Task<{ReturnType}?> Handle(
        {Name}Query request,
        CancellationToken ct)
    {
        var cacheKey = $"{entity}:{request.Id}";

        return await cache.GetOrCreateAsync(cacheKey, async () =>
        {
            var entity = await repository.GetByIdAsync(request.Id, ct);
            return entity is null ? null : mapper.Map<{ReturnType}>(entity);
        }, TimeSpan.FromMinutes(5), ct);
    }
}
```

## Kurallar

1. Primary constructor kullan
2. CancellationToken her async metotta olmalı
3. Logger injection zorunlu
4. Validator her command için oluşturulmalı
5. Query'lerde cache kullan
