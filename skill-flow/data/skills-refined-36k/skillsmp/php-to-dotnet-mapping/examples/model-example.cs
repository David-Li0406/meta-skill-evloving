// =============================================================================
// PHP Eloquent to .NET EF Core Entity Conversion Example
// =============================================================================

// -----------------------------------------------------------------------------
// BEFORE: PHP Laravel Eloquent Model (app/Models/Product.php)
// -----------------------------------------------------------------------------
/*
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class Product extends Model
{
    use HasFactory, SoftDeletes;

    protected $fillable = [
        'name',
        'slug',
        'description',
        'price',
        'category_id',
        'is_active',
    ];

    protected $casts = [
        'price' => 'decimal:2',
        'is_active' => 'boolean',
        'metadata' => 'array',
    ];

    protected $hidden = [
        'created_at',
        'updated_at',
    ];

    // Relationships
    public function category()
    {
        return $this->belongsTo(Category::class);
    }

    public function tags()
    {
        return $this->belongsToMany(Tag::class);
    }

    public function reviews()
    {
        return $this->hasMany(Review::class);
    }

    public function images()
    {
        return $this->morphMany(Image::class, 'imageable');
    }

    // Scopes
    public function scopeActive($query)
    {
        return $query->where('is_active', true);
    }

    public function scopeInCategory($query, $categoryId)
    {
        return $query->where('category_id', $categoryId);
    }

    public function scopePriceRange($query, $min, $max)
    {
        return $query->whereBetween('price', [$min, $max]);
    }

    // Accessors
    public function getFormattedPriceAttribute()
    {
        return '$' . number_format($this->price, 2);
    }

    // Mutators
    public function setNameAttribute($value)
    {
        $this->attributes['name'] = $value;
        $this->attributes['slug'] = Str::slug($value);
    }

    // Business Logic
    public function isAvailable()
    {
        return $this->is_active && $this->stock_quantity > 0;
    }

    public function applyDiscount($percentage)
    {
        return $this->price * (1 - $percentage / 100);
    }
}
*/

// -----------------------------------------------------------------------------
// AFTER: .NET 10 EF Core Entity (Models/Entities/Product.cs)
// -----------------------------------------------------------------------------

using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ProjectName.Models.Entities;

public class Product
{
    public int Id { get; set; }

    [Required]
    [MaxLength(255)]
    public string Name { get; set; } = string.Empty;

    [Required]
    [MaxLength(255)]
    public string Slug { get; set; } = string.Empty;

    public string? Description { get; set; }

    [Column(TypeName = "decimal(18,2)")]
    public decimal Price { get; set; }

    public int CategoryId { get; set; }

    public bool IsActive { get; set; } = true;

    public string? MetadataJson { get; set; }

    public DateTime CreatedAt { get; set; }
    public DateTime? UpdatedAt { get; set; }
    public DateTime? DeletedAt { get; set; } // Soft delete

    // Navigation Properties (replaces Eloquent relationships)
    
    // belongsTo → Reference navigation
    public Category Category { get; set; } = null!;

    // hasMany → Collection navigation
    public ICollection<Review> Reviews { get; set; } = new List<Review>();

    // belongsToMany → Collection via join entity
    public ICollection<ProductTag> ProductTags { get; set; } = new List<ProductTag>();

    // morphMany → Polymorphic (use discriminator pattern)
    public ICollection<Image> Images { get; set; } = new List<Image>();

    // Computed Property (replaces Accessor)
    [NotMapped]
    public string FormattedPrice => $"${Price:N2}";

    // Business Logic Methods
    public bool IsAvailable(int stockQuantity) => IsActive && stockQuantity > 0;

    public decimal ApplyDiscount(decimal percentage) => Price * (1 - percentage / 100);
}

// -----------------------------------------------------------------------------
// DbContext Configuration (Data/ApplicationDbContext.cs)
// -----------------------------------------------------------------------------

using Microsoft.EntityFrameworkCore;
using ProjectName.Models.Entities;

namespace ProjectName.Data;

public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    public DbSet<Product> Products => Set<Product>();
    public DbSet<Category> Categories => Set<Category>();
    public DbSet<Review> Reviews => Set<Review>();
    public DbSet<Tag> Tags => Set<Tag>();
    public DbSet<ProductTag> ProductTags => Set<ProductTag>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Product configuration
        modelBuilder.Entity<Product>(entity =>
        {
            entity.HasKey(e => e.Id);
            
            entity.HasIndex(e => e.Slug).IsUnique();
            
            // Soft delete global filter (replaces SoftDeletes trait)
            entity.HasQueryFilter(e => e.DeletedAt == null);

            // belongsTo relationship
            entity.HasOne(e => e.Category)
                .WithMany(c => c.Products)
                .HasForeignKey(e => e.CategoryId)
                .OnDelete(DeleteBehavior.Restrict);

            // hasMany relationship
            entity.HasMany(e => e.Reviews)
                .WithOne(r => r.Product)
                .HasForeignKey(r => r.ProductId);
        });

        // Many-to-many via join entity (replaces belongsToMany)
        modelBuilder.Entity<ProductTag>(entity =>
        {
            entity.HasKey(pt => new { pt.ProductId, pt.TagId });

            entity.HasOne(pt => pt.Product)
                .WithMany(p => p.ProductTags)
                .HasForeignKey(pt => pt.ProductId);

            entity.HasOne(pt => pt.Tag)
                .WithMany(t => t.ProductTags)
                .HasForeignKey(pt => pt.TagId);
        });
    }

    // Override SaveChanges for timestamps (replaces $timestamps = true)
    public override Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        var entries = ChangeTracker.Entries<Product>();

        foreach (var entry in entries)
        {
            if (entry.State == EntityState.Added)
            {
                entry.Entity.CreatedAt = DateTime.UtcNow;
            }
            else if (entry.State == EntityState.Modified)
            {
                entry.Entity.UpdatedAt = DateTime.UtcNow;
            }
        }

        return base.SaveChangesAsync(cancellationToken);
    }
}

// -----------------------------------------------------------------------------
// Join Entity for Many-to-Many (Models/Entities/ProductTag.cs)
// -----------------------------------------------------------------------------

namespace ProjectName.Models.Entities;

public class ProductTag
{
    public int ProductId { get; set; }
    public Product Product { get; set; } = null!;

    public int TagId { get; set; }
    public Tag Tag { get; set; } = null!;
}

// -----------------------------------------------------------------------------
// Query Extensions for Scopes (Extensions/ProductQueryExtensions.cs)
// -----------------------------------------------------------------------------

namespace ProjectName.Extensions;

public static class ProductQueryExtensions
{
    // Replaces scopeActive
    public static IQueryable<Product> Active(this IQueryable<Product> query)
    {
        return query.Where(p => p.IsActive);
    }

    // Replaces scopeInCategory
    public static IQueryable<Product> InCategory(this IQueryable<Product> query, int categoryId)
    {
        return query.Where(p => p.CategoryId == categoryId);
    }

    // Replaces scopePriceRange
    public static IQueryable<Product> PriceRange(this IQueryable<Product> query, decimal min, decimal max)
    {
        return query.Where(p => p.Price >= min && p.Price <= max);
    }
}

// Usage:
// var products = await _context.Products
//     .Active()
//     .InCategory(5)
//     .PriceRange(10, 100)
//     .ToListAsync();

// -----------------------------------------------------------------------------
// KEY CONVERSION NOTES:
// -----------------------------------------------------------------------------
// 1. $fillable → Not needed, use DTOs for input validation
// 2. $casts → Use data annotations and Column attributes
// 3. $hidden → Use [JsonIgnore] or create separate DTOs
// 4. belongsTo → Navigation property + HasOne/WithMany config
// 5. hasMany → ICollection<T> + HasMany/WithOne config
// 6. belongsToMany → Join entity + explicit configuration
// 7. SoftDeletes → DeletedAt column + HasQueryFilter
// 8. Scopes → Extension methods on IQueryable<T>
// 9. Accessors → [NotMapped] computed properties
// 10. Mutators → Handle in service layer or entity constructor
// 11. $timestamps → Override SaveChangesAsync
