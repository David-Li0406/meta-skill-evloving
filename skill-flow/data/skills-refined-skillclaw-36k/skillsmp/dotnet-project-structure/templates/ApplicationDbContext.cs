// =============================================================================
// .NET 10 ApplicationDbContext Template
// =============================================================================
// This is the EF Core DbContext - the main database access point.
// Replaces Laravel's Eloquent model configurations and database/migrations.
// =============================================================================

using Microsoft.EntityFrameworkCore;
using ProjectName.Models.Entities;

namespace ProjectName.Data;

public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    // ==========================================================================
    // DbSets (equivalent to Eloquent Models)
    // ==========================================================================
    
    public DbSet<User> Users => Set<User>();
    public DbSet<Product> Products => Set<Product>();
    public DbSet<Category> Categories => Set<Category>();
    public DbSet<Order> Orders => Set<Order>();
    public DbSet<OrderItem> OrderItems => Set<OrderItem>();

    // ==========================================================================
    // Model Configuration (replaces Eloquent $fillable, $casts, relationships)
    // ==========================================================================
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Apply all configurations from the current assembly
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationDbContext).Assembly);

        // Or configure inline:
        ConfigureUser(modelBuilder);
        ConfigureProduct(modelBuilder);
    }

    private static void ConfigureUser(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<User>(entity =>
        {
            entity.HasKey(e => e.Id);
            
            entity.HasIndex(e => e.Email).IsUnique();
            
            entity.Property(e => e.Email)
                .IsRequired()
                .HasMaxLength(255);

            entity.Property(e => e.PasswordHash)
                .IsRequired();

            // Soft delete filter (replaces SoftDeletes trait)
            entity.HasQueryFilter(e => e.DeletedAt == null);
        });
    }

    private static void ConfigureProduct(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Product>(entity =>
        {
            entity.HasKey(e => e.Id);
            
            entity.HasIndex(e => e.Slug).IsUnique();

            entity.Property(e => e.Price)
                .HasColumnType("decimal(18,2)");

            // belongsTo Category
            entity.HasOne(e => e.Category)
                .WithMany(c => c.Products)
                .HasForeignKey(e => e.CategoryId)
                .OnDelete(DeleteBehavior.Restrict);

            // Soft delete filter
            entity.HasQueryFilter(e => e.DeletedAt == null);
        });
    }

    // ==========================================================================
    // Automatic Timestamps (replaces Laravel $timestamps = true)
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
}

// =============================================================================
// Timestamp Interface (apply to entities that need automatic timestamps)
// =============================================================================

public interface IHasTimestamps
{
    DateTime CreatedAt { get; set; }
    DateTime? UpdatedAt { get; set; }
}

// =============================================================================
// Soft Delete Interface (apply to entities that need soft delete)
// =============================================================================

public interface ISoftDelete
{
    DateTime? DeletedAt { get; set; }
}
