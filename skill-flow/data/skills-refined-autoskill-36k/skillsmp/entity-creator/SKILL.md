---
name: entity-creator
description: Creates complete DDD entity with factory method, domain events, value objects, and EF configuration
---

# Entity Creator Skill

Bu skill, Merge E-Commerce Backend projesi için DDD uyumlu entity oluşturur.

## Ne Zaman Kullan

- "Entity oluştur", "aggregate root ekle" dendiğinde
- Yeni bir domain modeli eklenirken
- "Product entity'si yaz" gibi isteklerde

## Oluşturulacak Dosyalar

```
Merge.Domain/{Module}/
├── Entities/
│   └── {Entity}.cs
├── Events/
│   ├── {Entity}CreatedEvent.cs
│   └── {Entity}UpdatedEvent.cs
└── Specifications/
    └── {Entity}ByIdSpec.cs

Merge.Infrastructure/Data/Configurations/
└── {Entity}Configuration.cs
```

## Entity Template

```csharp
public class {Entity} : BaseAggregateRoot
{
    // ============================================
    // PRIVATE SETTERS (encapsulation)
    // ============================================
    public string Name { get; private set; } = null!;
    public bool IsActive { get; private set; }

    // ============================================
    // COLLECTIONS (private backing field)
    // ============================================
    private readonly List<{Related}> _{related}s = [];
    public IReadOnlyCollection<{Related}> {Related}s => _{related}s.AsReadOnly();

    // ============================================
    // PRIVATE CONSTRUCTOR (EF Core)
    // ============================================
    private {Entity}() { }

    // ============================================
    // FACTORY METHOD (ONLY way to create)
    // ============================================
    public static {Entity} Create(string name, /* other params */)
    {
        Guard.AgainstNullOrEmpty(name, nameof(name));

        var entity = new {Entity}
        {
            Id = Guid.NewGuid(),
            Name = name,
            IsActive = true,
            CreatedAt = DateTime.UtcNow
        };

        entity.AddDomainEvent(new {Entity}CreatedEvent(entity.Id, entity.Name));
        return entity;
    }

    // ============================================
    // DOMAIN METHODS (business behavior)
    // ============================================
    public void UpdateName(string newName)
    {
        Guard.AgainstNullOrEmpty(newName, nameof(newName));
        if (Name == newName) return;

        var oldName = Name;
        Name = newName;
        MarkAsUpdated();

        AddDomainEvent(new {Entity}NameChangedEvent(Id, oldName, newName));
    }

    public void Deactivate()
    {
        if (!IsActive) return;

        IsActive = false;
        MarkAsUpdated();

        AddDomainEvent(new {Entity}DeactivatedEvent(Id));
    }
}
```

## Domain Event Template

```csharp
public record {Entity}CreatedEvent(Guid {Entity}Id, string Name) : DomainEvent;
public record {Entity}UpdatedEvent(Guid {Entity}Id) : DomainEvent;
public record {Entity}DeactivatedEvent(Guid {Entity}Id) : DomainEvent;
```

## EF Configuration Template

```csharp
public class {Entity}Configuration : IEntityTypeConfiguration<{Entity}>
{
    public void Configure(EntityTypeBuilder<{Entity}> builder)
    {
        builder.ToTable("{entities}"); // plural, snake_case

        builder.HasKey(x => x.Id);

        builder.Property(x => x.Name)
            .HasMaxLength(200)
            .IsRequired();

        builder.Property(x => x.IsActive)
            .HasDefaultValue(true);

        // Soft delete filter
        builder.HasQueryFilter(x => !x.IsDeleted);

        // Indexes
        builder.HasIndex(x => x.Name);
        builder.HasIndex(x => new { x.IsActive, x.CreatedAt });

        // Ignore domain events
        builder.Ignore(x => x.DomainEvents);
    }
}
```

## Kurallar

1. ASLA public setter kullanma
2. Factory method zorunlu (Create)
3. Her state değişikliğinde domain event
4. Private constructor EF Core için
5. Guard clauses ile validation
6. Collection'lar readonly expose edilmeli
