---
name: migration-helper
description: Helps create and manage EF Core migrations with proper naming and rollback strategies
---

# Migration Helper Skill

Bu skill, Merge E-Commerce Backend projesi için EF Core migration yönetimi yapar.

## Ne Zaman Kullan

- "Migration oluştur", "veritabanı güncelle" dendiğinde
- Entity configuration değişikliklerinde
- "Tablo ekle", "kolon ekle" gibi isteklerde

## Migration Komutları

### Migration Oluşturma

```bash
dotnet ef migrations add {MigrationName} \
    --project Merge.Infrastructure \
    --startup-project Merge.API \
    --output-dir Data/Migrations
```

### Migration Uygulama

```bash
dotnet ef database update \
    --project Merge.Infrastructure \
    --startup-project Merge.API
```

### Migration Geri Alma

```bash
# Son migration'ı geri al
dotnet ef database update {PreviousMigrationName} \
    --project Merge.Infrastructure \
    --startup-project Merge.API

# Migration dosyasını sil
dotnet ef migrations remove \
    --project Merge.Infrastructure \
    --startup-project Merge.API
```

### SQL Script Oluşturma

```bash
dotnet ef migrations script \
    --project Merge.Infrastructure \
    --startup-project Merge.API \
    --output migration.sql \
    --idempotent
```

## Migration Naming Convention

| İşlem | Format | Örnek |
|-------|--------|-------|
| Tablo ekleme | `Add{TableName}` | `AddProducts` |
| Kolon ekleme | `Add{Column}To{Table}` | `AddSkuToProducts` |
| Kolon silme | `Remove{Column}From{Table}` | `RemoveDescriptionFromProducts` |
| Index ekleme | `AddIndexOn{Table}{Columns}` | `AddIndexOnProductsCategoryId` |
| FK ekleme | `Add{Child}To{Parent}Relation` | `AddOrderItemsToOrderRelation` |
| Tablo değiştirme | `Alter{Table}{Change}` | `AlterProductsAddAuditFields` |

## Entity Configuration Template

```csharp
public class {Entity}Configuration : IEntityTypeConfiguration<{Entity}>
{
    public void Configure(EntityTypeBuilder<{Entity}> builder)
    {
        // Table name (snake_case, plural)
        builder.ToTable("{entities}");

        // Primary key
        builder.HasKey(x => x.Id);

        // Properties
        builder.Property(x => x.Name)
            .HasColumnName("name")
            .HasMaxLength(200)
            .IsRequired();

        builder.Property(x => x.Price)
            .HasColumnName("price")
            .HasPrecision(18, 2);

        builder.Property(x => x.CreatedAt)
            .HasColumnName("created_at")
            .HasDefaultValueSql("NOW()");

        // Value object conversion
        builder.Property(x => x.Email)
            .HasConversion(
                v => v.Value,
                v => Email.Create(v))
            .HasMaxLength(320);

        // Relationships
        builder.HasOne(x => x.Category)
            .WithMany(c => c.Products)
            .HasForeignKey(x => x.CategoryId)
            .OnDelete(DeleteBehavior.Restrict);

        // Indexes
        builder.HasIndex(x => x.Sku).IsUnique();
        builder.HasIndex(x => new { x.CategoryId, x.IsActive });

        // Soft delete filter
        builder.HasQueryFilter(x => !x.IsDeleted);

        // Ignore
        builder.Ignore(x => x.DomainEvents);
    }
}
```

## Checklist

Migration öncesi kontrol:
- [ ] Entity configuration eklendi/güncellendi
- [ ] DbContext'e DbSet eklendi
- [ ] Naming convention doğru (snake_case)
- [ ] Index'ler tanımlı
- [ ] FK constraint'ler doğru
- [ ] Seed data gerekiyorsa eklendi

Migration sonrası kontrol:
- [ ] Migration dosyası review edildi
- [ ] Down metodu çalışıyor
- [ ] Test veritabanında uygulandı
- [ ] Rollback test edildi
