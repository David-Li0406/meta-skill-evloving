// =============================================================================
// EF Core DbContext Template
// =============================================================================
// This template shows how to configure DbContext for migrated Eloquent models.
// The DbContext is the main entry point for database operations.
// =============================================================================

using Microsoft.EntityFrameworkCore;
using ProjectName.Models.Entities;

namespace ProjectName.Data;

/// <summary>
/// Main database context for the application.
/// Replaces Eloquent's database configuration and model bindings.
/// </summary>
public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    // ==========================================================================
    // DbSets - One per Entity
    // Eloquent: Each Model class is automatically available
    // EF Core: Must explicitly declare DbSet properties
    // ==========================================================================

    public DbSet<User> Users => Set<User>();
    public DbSet<Product> Products => Set<Product>();
    public DbSet<Category> Categories => Set<Category>();
    public DbSet<Order> Orders => Set<Order>();
    public DbSet<OrderItem> OrderItems => Set<OrderItem>();
    public DbSet<Review> Reviews => Set<Review>();
    public DbSet<Tag> Tags => Set<Tag>();
    public DbSet<ProductTag> ProductTags => Set<ProductTag>();
    public DbSet<Image> Images => Set<Image>();

    // ==========================================================================
    // Model Configuration
    // Eloquent: Configuration is in each Model class
    // EF Core: Configuration in OnModelCreating or IEntityTypeConfiguration<T>
    // ==========================================================================

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Apply all configurations from separate configuration classes
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationDbContext).Assembly);

        // Or configure inline (shown below for reference)
        ConfigureProduct(modelBuilder);
        ConfigureProductTag(modelBuilder);
        ConfigureImage(modelBuilder);
    }

    // ==========================================================================
    // Product Configuration
    // ==========================================================================

    private static void ConfigureProduct(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Product>(entity =>
        {
            // Table name (if different from convention)
            // Eloquent: protected $table = 'products';
            entity.ToTable("products");

            // Primary key
            entity.HasKey(e => e.Id);

            // Indexes
            // Eloquent: typically in migrations
            entity.HasIndex(e => e.Slug).IsUnique();
            entity.HasIndex(e => e.CategoryId);
            entity.HasIndex(e => e.IsActive);

            // Property configuration
            entity.Property(e => e.Name)
                .IsRequired()
                .HasMaxLength(255);

            entity.Property(e => e.Slug)
                .IsRequired()
                .HasMaxLength(255);

            entity.Property(e => e.Price)
                .HasColumnType("decimal(18,2)");

            // Soft delete global filter
            // Eloquent: use SoftDeletes; - automatically filters deleted_at IS NULL
            entity.HasQueryFilter(e => e.DeletedAt == null);

            // =================================================================
            // Relationships
            // =================================================================

            // belongsTo Category
            // Eloquent: return $this->belongsTo(Category::class);
            entity.HasOne(e => e.Category)
                .WithMany(c => c.Products)
                .HasForeignKey(e => e.CategoryId)
                .OnDelete(DeleteBehavior.Restrict);

            // belongsTo User (optional/nullable)
            // Eloquent: return $this->belongsTo(User::class, 'created_by_user_id');
            entity.HasOne(e => e.CreatedByUser)
                .WithMany()
                .HasForeignKey(e => e.CreatedByUserId)
                .OnDelete(DeleteBehavior.SetNull);

            // hasMany Reviews
            // Eloquent: return $this->hasMany(Review::class);
            entity.HasMany(e => e.Reviews)
                .WithOne(r => r.Product)
                .HasForeignKey(r => r.ProductId)
                .OnDelete(DeleteBehavior.Cascade);

            // hasMany OrderItems
            entity.HasMany(e => e.OrderItems)
                .WithOne(oi => oi.Product)
                .HasForeignKey(oi => oi.ProductId)
                .OnDelete(DeleteBehavior.Restrict);
        });
    }

    // ==========================================================================
    // Many-to-Many Configuration (ProductTag)
    // Eloquent: return $this->belongsToMany(Tag::class);
    // EF Core: Requires explicit join entity configuration
    // ==========================================================================

    private static void ConfigureProductTag(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<ProductTag>(entity =>
        {
            // Composite primary key
            entity.HasKey(pt => new { pt.ProductId, pt.TagId });

            // Relationship to Product
            entity.HasOne(pt => pt.Product)
                .WithMany(p => p.ProductTags)
                .HasForeignKey(pt => pt.ProductId)
                .OnDelete(DeleteBehavior.Cascade);

            // Relationship to Tag
            entity.HasOne(pt => pt.Tag)
                .WithMany(t => t.ProductTags)
                .HasForeignKey(pt => pt.TagId)
                .OnDelete(DeleteBehavior.Cascade);
        });
    }

    // ==========================================================================
    // Polymorphic Configuration (Image)
    // Eloquent: return $this->morphMany(Image::class, 'imageable');
    // EF Core: Use discriminator pattern
    // ==========================================================================

    private static void ConfigureImage(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Image>(entity =>
        {
            entity.HasKey(e => e.Id);

            // Discriminator for polymorphic relationship
            entity.HasDiscriminator<string>("ImageableType")
                .HasValue<ProductImage>("Product")
                .HasValue<UserImage>("User")
                .HasValue<CategoryImage>("Category");
        });
    }

    // ==========================================================================
    // Automatic Timestamps
    // Eloquent: $timestamps = true (created_at, updated_at)
    // EF Core: Override SaveChanges to set automatically
    // ==========================================================================

    public override Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        UpdateTimestamps();
        return base.SaveChangesAsync(cancellationToken);
    }

    public override int SaveChanges()
    {
        UpdateTimestamps();
        return base.SaveChanges();
    }

    private void UpdateTimestamps()
    {
        var entries = ChangeTracker.Entries()
            .Where(e => e.Entity is IHasTimestamps &&
                       (e.State == EntityState.Added || e.State == EntityState.Modified));

        foreach (var entry in entries)
        {
            var entity = (IHasTimestamps)entry.Entity;

            if (entry.State == EntityState.Added)
            {
                entity.CreatedAt = DateTime.UtcNow;
            }

            entity.UpdatedAt = DateTime.UtcNow;
        }
    }

    // ==========================================================================
    // Soft Delete Helper
    // ==========================================================================

    /// <summary>
    /// Soft delete an entity instead of hard delete.
    /// Eloquent: $model->delete() with SoftDeletes trait
    /// </summary>
    public void SoftDelete<T>(T entity) where T : class, ISoftDelete
    {
        entity.DeletedAt = DateTime.UtcNow;
        Entry(entity).State = EntityState.Modified;
    }

    /// <summary>
    /// Restore a soft-deleted entity.
    /// Eloquent: $model->restore()
    /// </summary>
    public void Restore<T>(T entity) where T : class, ISoftDelete
    {
        entity.DeletedAt = null;
        Entry(entity).State = EntityState.Modified;
    }

    /// <summary>
    /// Include soft-deleted entities in query.
    /// Eloquent: Model::withTrashed()
    /// </summary>
    public IQueryable<T> WithTrashed<T>() where T : class, ISoftDelete
    {
        return Set<T>().IgnoreQueryFilters();
    }

    /// <summary>
    /// Query only soft-deleted entities.
    /// Eloquent: Model::onlyTrashed()
    /// </summary>
    public IQueryable<T> OnlyTrashed<T>() where T : class, ISoftDelete
    {
        return Set<T>().IgnoreQueryFilters().Where(e => e.DeletedAt != null);
    }
}
